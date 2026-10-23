"""Capture real principle routing and read-only state evidence; inspect replies manually."""

import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile

from codex_acceptance_state import snapshot

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--codex', default='codex')
parser.add_argument('--model', required=True)
parser.add_argument('--effort', required=True)
parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
parser.add_argument('--case', action='append', choices=('premise', 'isolation'))
args = parser.parse_args()
repository = Path(__file__).resolve().parent.parent
entry = repository / 'plugins/pstack/skills/poteto-mode'
root = Path(tempfile.mkdtemp(prefix='pstack-principles-live-')).resolve()
home, workspace = root / 'home', root / 'workspace'
home.mkdir()
workspace.mkdir()
link = workspace / '.agents/skills/poteto-mode'
link.parent.mkdir(parents=True)
link.symlink_to(entry)
(workspace / 'jobs.py').write_text('def store(jobs, customer, region, value):\n    jobs[customer] = value\n')
(workspace / 'observations.json').write_text(json.dumps({
    'reproduced_serially': True,
    'writes': [['customer-7', 'eu', 10], ['customer-7', 'us', 20]],
    'observed_entries': 1,
    'expected_entries': 2,
    'attempted_fixes': ['retry write 3 times', 'retry write 10 times'],
    'same_failure_after_both': True,
}, indent=2))
(home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n')
auth = home / 'auth.json'
auth.symlink_to(args.auth_file.resolve(strict=True))
print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
cases = {
    'premise': 'Investigate jobs.py and observations.json. Why did both attempted fixes fail? Recommend the next discriminating observation and the smallest appropriate correction. Read applicable principle leaves in full. Do not implement it.',
    'isolation': 'Review this proposed implementation plan: two agents edit jobs.py concurrently in the same checkout after each creates a different branch; they plan to serialize only git commits. Is that sufficient isolation? Recommend the smallest safe plan and explain what would prove the isolation. Read applicable principle leaves in full. Do not execute the plan.',
}
results = []
try:
    for name, task in cases.items():
        if args.case and name not in args.case:
            continue
        before = snapshot(workspace)
        had_git = (workspace / '.git').exists() or (workspace / '.git').is_symlink()
        command = [args.codex, '--no-daemon', 'exec', '--ephemeral', '--skip-git-repo-check',
                   '-C', str(workspace), '-s', 'read-only', '-m', args.model,
                   '-c', 'model_reasoning_effort=' + json.dumps(args.effort),
                   '--json', '-o', str(root / (name + '-final.txt')),
                   '$poteto-mode ' + task + '\nThis is a read-only acceptance investigation. '
                   'Keep the checklist in conversation. Do not delegate, create files, configure roles, '
                   'or contact external services. Missing roles permit the documented primary-only read path.']
        with (root / (name + '.jsonl')).open('w') as output, (root / (name + '-stderr.log')).open('w') as errors:
            result = subprocess.run(command, env={**os.environ, 'CODEX_HOME': str(home),
                                    'PYTHONDONTWRITEBYTECODE': '1'}, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=errors, timeout=600)
        after = snapshot(workspace)
        (root / (name + '-before.json')).write_text(json.dumps(before, sort_keys=True))
        (root / (name + '-after.json')).write_text(json.dumps(after, sort_keys=True))
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        transcript = [json.loads(line) for line in (root / (name + '.jsonl')).read_text().splitlines()]
        observed = '\n'.join(event.get('item', {}).get('aggregated_output', '') for event in transcript
                             if event.get('type') == 'item.completed'
                             and event.get('item', {}).get('type') == 'command_execution'
                             and event.get('item', {}).get('exit_code') == 0)
        final_file = root / (name + '-final.txt')
        reply = final_file.read_text() if final_file.exists() else ''
        unread = []
        for leaf in (entry / 'references/principles').glob('*.md'):
            body = leaf.read_text().strip()
            title = body.splitlines()[0].removeprefix('# ')
            if re.search(re.escape(title), reply, re.IGNORECASE) and body not in observed:
                unread.append(leaf.stem)
        results.append({'case': name, 'exit': result.returncode, 'changed': changed,
                        'namedButUnreadLeaves': sorted(unread),
                        'leafClaimChecksPassed': result.returncode == 0 and not unread,
                        'artifactChecksPassed': result.returncode == 0 and not changed
                        and had_git == ((workspace / '.git').exists() or (workspace / '.git').is_symlink())})
        print(json.dumps(results[-1]), flush=True)
finally:
    auth.unlink(missing_ok=True)
print('Scope: read-only artifact checks. Named leaf claims are checked against returned full content. Inspect reasoning in local transcripts; this is not desktop UI evidence.')
raise SystemExit(0 if all(item['artifactChecksPassed'] and item['leafClaimChecksPassed'] for item in results) else 1)
