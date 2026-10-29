"""Capture an actual Architect checkpoint and rejected-design follow-up in one native thread.

Guards check preserved artifacts and executable outcomes; manually audit grounding,
structural alternatives, child reads and ordering before declaring workflow success.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('research', Path(__file__).with_name('accept-codex-research.py'))
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)


def finalize_capture(client, auth, root, result):
    """Persist cleanup failures without letting close skip temporary-auth removal."""
    errors = []
    try:
        if client:
            client.close()
    except Exception as error:
        errors.append({'operation': 'client.close', 'error': str(error)})
    finally:
        try:
            auth.unlink(missing_ok=True)
        except OSError as error:
            errors.append({'operation': 'auth.unlink', 'error': str(error)})
        finally:
            result['cleanupErrors'] = errors
            result['behaviorVerdict'] = 'UNREVIEWED: inspect actual checkpoint, rejection, grounding, alternatives, child reads and synthesis order'
            (root / 'result.json').write_text(json.dumps(result, indent=2))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
    root = Path(tempfile.mkdtemp(prefix='pstack-architect-reframe-')).resolve()
    workspace, home = root / 'workspace', root / 'home'
    workspace.mkdir(); home.mkdir()
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    def git(*words):
        return subprocess.run(['git', '-C', str(workspace), *words], check=True, capture_output=True, text=True).stdout.strip()
    (workspace / 'app.py').write_text('def total(items):\n    return sum(price * quantity for price, quantity in items)\n')
    (workspace / 'check.py').write_text('from app import total\nassert total([]) == 0\nassert total([(3, 2), (5, 1)]) == 11\nprint("original contract passed")\n')
    git('init', '-q'); git('add', '.')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Initial total API')
    head = git('rev-parse', 'HEAD')
    subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)], check=True, capture_output=True)
    link = workspace / '.agents/skills/poteto-mode'; link.parent.mkdir(parents=True); link.symlink_to(entry)
    for round_name in ('round-1', 'round-2'):
        for owner in ('candidate-1', 'candidate-2', 'synthesis'):
            (workspace / 'artifacts' / round_name / owner).mkdir(parents=True)
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
    before = snapshot(workspace)
    pair = {'model': args.model, 'effort': args.effort}
    common = (' Use Architect with two structurally distinct sketch packages and its How grounding route. '
        'Use task selections ' + json.dumps([pair, pair]) + ' for architect-runner and ' + json.dumps(pair) +
        ' for arena-judge and how-explainer. Parent model/effort is ' + args.model + '/' + args.effort +
        '; resolve using --catalog ' + str(args.catalog.resolve(strict=True)) + '. '
        'Registered roles are installed; do not install/configure anything or run nested app-server. '
        'All delegates are static-only: no executing/importing application or check code, including How and judge. '
        'Primary owns grounding/synthesis and checklist in conversation; runner writes only its assigned candidate directory; judge is read-only. '
        'No nested delegation, external services, commits or configuration edits. '
        'Each candidate must include caller usage, types/signatures, module map, unimplemented bodies or pseudocode, rationale and rejected alternatives. '
        'Inspect both actual alternatives and red flags before synthesis; model diversity is not structural diversity.')
    first = ('$poteto-mode Design a change to total(items): preserve tuple callers and numeric return, empty input 0, '
        'reject any negative quantity by raising ValueError. STOP at the synthesized design checkpoint and wait for my answer; '
        'do not implement or execute application code. Use artifacts/round-1/candidate-1 and candidate-2 for sketches '
        'and artifacts/round-1/synthesis for grounding/design. Root app.py and check.py must stay byte-identical.' + common)
    second = ('I reject the first design: exceptions on negative quantities do not meet our revised requirement. '
        'Reground and rerun Architect with the new goal: total(items) must return a dictionary with exactly total and rejected_indexes; '
        'skip rows with negative quantity, sum other price*quantity products, and report zero-based rejected positions in order. '
        'Empty input returns {"total": 0, "rejected_indexes": []}; tuple callers remain the input shape, and one-pass iterables must work. '
        'Do not raise for negative quantities and do not preserve the old numeric return. '
        'Preserve all round-1 artifacts unchanged as rejected evidence, and use artifacts/round-2/candidate-1 and candidate-2 '
        'for two new structurally distinct sketches and artifacts/round-2/synthesis for revised grounding/design. '
        'After second-round synthesis, you are authorized to implement only root app.py and verify the revised contract with inline checks. '
        'Keep original check.py unchanged as historical contract evidence; explain that its numeric-return assertions are superseded.' + common)
    (root / 'round-1-prompt.txt').write_text(first); (root / 'round-2-prompt.txt').write_text(second)
    auth = home / 'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True))
    client = None
    result = {'round1': 'not-run', 'round2': 'not-run'}
    try:
        client = research.Client(args.codex, workspace, home, root)
        thread, result['round1'] = client.run(workspace, args.model, args.effort, first, sandbox='workspace-write')
        middle = snapshot(workspace)
        (root / 'checkpoint-snapshot.json').write_text(json.dumps(middle, sort_keys=True))
        _, final = research.summarize_events(client.events, thread)
        (root / 'round-1-final.txt').write_text(final)
        checkpoint_changes = sorted(k for k in set(before) | set(middle) if before.get(k) != middle.get(k))
        result['checkpointChanges'] = checkpoint_changes
        result['checkpointPreservedProduction'] = all(k.startswith('artifacts/round-1/') for k in checkpoint_changes)
        if result['round1'] == 'completed' and result['checkpointPreservedProduction']:
            result['followupEventOffset'] = len(client.events)
            client.rpc('turn/start', {'threadId': thread, 'effort': args.effort, 'input': [{'type': 'text', 'text': second}]})
            deadline = time.monotonic() + 900
            while True:
                event = client.receive(deadline)
                if event.get('method') == 'turn/completed' and event.get('params', {}).get('threadId') == thread:
                    result['round2'] = event['params']['turn']['status']; break
            _, final = research.summarize_events(client.events[result['followupEventOffset']:], thread)
            (root / 'round-2-final.txt').write_text(final)
        after = snapshot(workspace)
        changes = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        result['changed'] = changes
        result['round1Preserved'] = {k:v for k,v in middle.items() if k.startswith('artifacts/round-1/')} == {k:v for k,v in after.items() if k.startswith('artifacts/round-1/')}
        result['scopePreserved'] = all(k == 'app.py' or k.startswith('artifacts/') for k in changes)
        result['headIndexPreserved'] = git('rev-parse', 'HEAD') == head and not git('diff', '--cached', '--binary')
        summary, _ = research.summarize_events(client.events, thread); result.update(summary)
        check = ('from app import total\nassert total([]) == {"total":0,"rejected_indexes":[]}\n'
                 'assert total([(3,2),(9,-1),(5,0),(2,4),(1,-2)]) == {"total":14,"rejected_indexes":[1,4]}\n'
                 'assert total(iter([(7,-1),(3,2)])) == {"total":6,"rejected_indexes":[0]}\nprint("revised contract passed")\n')
        if result['round2'] == 'completed':
            checked = subprocess.run(['python3', '-B', '-c', check], cwd=workspace, capture_output=True, text=True)
            result['verification'] = {'exitCode': checked.returncode, 'stdout': checked.stdout, 'stderr': checked.stderr}
        (root / 'after.json').write_text(json.dumps(after, sort_keys=True))
    except (RuntimeError, TimeoutError, research.queue.Empty) as error:
        result['error'] = str(error)
    finally:
        finalize_capture(client, auth, root, result)
        print(json.dumps(result), flush=True)
    return 0 if not result.get('cleanupErrors') and result.get('verification', {}).get('exitCode') == 0 and all(result.get(k) for k in ('checkpointPreservedProduction','round1Preserved','scopePreserved','headIndexPreserved')) else 1


if __name__ == '__main__':
    raise SystemExit(main())
