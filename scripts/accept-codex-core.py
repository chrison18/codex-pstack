"""Run real model artifact checks in disposable projects; raw transcripts stay local."""

import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

from codex_acceptance_state import snapshot

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--model', required=True)
parser.add_argument('--effort', required=True)
parser.add_argument('--catalog', type=Path, required=True, help='Fresh native snapshot from runtime.py models --output')
parser.add_argument('--case', action='append', choices=('feature', 'bug', 'investigation'),
                    help='Run only the selected fixture; repeat to select more than one')
parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json',
                    help='Existing CLI login file, referenced temporarily and never printed')
args = parser.parse_args()
repository = Path(__file__).resolve().parent.parent
entry = repository / 'plugins/pstack/skills/poteto-mode'
root = Path(tempfile.mkdtemp(prefix='pstack-core-live-')).resolve()
catalog = args.catalog.resolve(strict=True)
print(json.dumps({'evidenceDirectory': str(root)}), flush=True)


def git(workspace, *arguments):
    return subprocess.run(['git', '-C', str(workspace), *arguments],
                          check=True, capture_output=True, text=True).stdout.strip()


def run(name, task, source, check, readonly=False):
    workspace = root / name
    workspace.mkdir()
    (workspace / 'app.py').write_text(source)
    (workspace / 'check.py').write_text(check)
    git(workspace, 'init', '-q')
    git(workspace, 'add', '.')
    git(workspace, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
    original_head = git(workspace, 'rev-parse', 'HEAD')
    subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)],
                   check=True, capture_output=True)
    link = workspace / '.agents/skills/poteto-mode'
    link.parent.mkdir(parents=True)
    link.symlink_to(entry)
    before = snapshot(workspace)
    (root / (name + '-before.json')).write_text(json.dumps(before))
    home = root / (name + '-home')
    home.mkdir()
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n')
    prompt = (
        '$poteto-mode ' + task + '\nThis is an authorized disposable acceptance fixture. '
        'Do not commit, open PRs, access external services, or modify files outside this fixture. '
        'Use registered roles as prescribed. The parent model is ' + args.model + ' with ' + args.effort +
        ' effort, explicitly selected for this acceptance run. Resolve settings with that observed pair '
        'and --catalog ' + str(catalog) + ', the fresh native catalog supplied by the host. '
        'Do not run a nested app-server. Do not treat unavailable delegation as permission to implement '
        'in the primary. Parent owns the workflow, inspects results and runs checks. '
        'Keep a checklist in the conversation' +
        (' only; the entire repository must remain unchanged.' if readonly else
         ' and persist it in task.md; retain skips and failures with reasons. Only app.py and task.md '
         'may change. The check.py acceptance check must stay unchanged.')
    )
    command = [
        'codex', '--no-daemon', 'exec', '--ephemeral', '-C', str(workspace),
        '-s', 'read-only' if readonly else 'workspace-write', '-m', args.model,
        '-c', 'model_reasoning_effort=' + json.dumps(args.effort),
        '--json', '-o', str(root / (name + '-final.txt')), prompt,
    ]
    (root / (name + '-args.json')).write_text(json.dumps(command))
    auth_link = home / 'auth.json'
    auth_link.symlink_to(args.auth_file.resolve(strict=True))
    try:
        with (root / (name + '.jsonl')).open('w') as output, (root / (name + '-stderr.log')).open('w') as errors:
            try:
                process = subprocess.run(
                    command, env={**os.environ, 'CODEX_HOME': str(home), 'PYTHONDONTWRITEBYTECODE': '1'},
                    stdout=output, stderr=errors, stdin=subprocess.DEVNULL, timeout=600,
                )
                exit_code = process.returncode
            except subprocess.TimeoutExpired:
                exit_code = 'TIMEOUT'
    finally:
        auth_link.unlink(missing_ok=True)
    after = snapshot(workspace)
    (root / (name + '-after.json')).write_text(json.dumps(after))
    result = subprocess.run(['python3', '-B', 'check.py'], cwd=workspace,
                            capture_output=True, text=True, timeout=30)
    (root / (name + '-check.txt')).write_text(result.stdout + result.stderr)
    changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
    allowed = set() if readonly else {'app.py', 'task.md'}
    index_clean = not git(workspace, 'diff', '--cached', '--name-only')
    passed = (exit_code == 0 and result.returncode == 0 and changed <= allowed
              and index_clean and git(workspace, 'rev-parse', 'HEAD') == original_head)
    return {'name': name, 'exit': exit_code, 'check': result.returncode,
            'changed': sorted(changed), 'artifactChecksPassed': passed}


cases=[
 ('feature','Add a multiply(a, b) function to app.py and preserve add. Verify with python3 -B check.py.',
 'def add(a, b):\n    return a + b\n',
 'from app import add, multiply\nassert add(3, 4) == 7\nassert multiply(3, 4) == 12\nassert multiply(-2, 3) == -6\nprint("feature acceptance passed")\n',False),
 ('bug','Fix app.py: average([2,4,6]) returns 4 but currently check.py fails. Reproduce with python3 -B check.py before fixing.',
 'def average(values):\n    return sum(values) / (len(values) + 1)\n',
 'from app import average\nassert average([2, 4, 6]) == 4\nassert average([5]) == 5\nprint("bug acceptance passed")\n',False),
 ('investigation','Investigate how app.py computes total and explain its behavior with file/line citations. Do not fix or change anything.',
 'def total(items):\n    return sum(item["price"] * item["quantity"] for item in items)\n',
 'from app import total\nassert total([{"price":3,"quantity":2}]) == 6\nprint("investigation fixture unchanged")\n',True)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    selected = [case for case in cases if args.case is None or case[0] in args.case]
    results = list(executor.map(lambda case: run(*case), selected))
for result in results:
    print(json.dumps(result), flush=True)
print('Scope: artifact checks only; independently inspect role loading, model events, checklist, and failing reproduction.')
raise SystemExit(0 if all(result['artifactChecksPassed'] for result in results) else 1)
