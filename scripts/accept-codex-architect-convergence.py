"""Controlled existing-artifact comparison, not independent candidate-generation proof."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('scrap', Path(__file__).with_name('accept-codex-architect-scrap.py'))
scrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scrap)

CANDIDATE_A = '''# Proposal A: receipt fields

## Usage and signatures
`first = prepare("Ada", [(3, 2)])`; prepare another receipt; `first.render()` still returns Ada/6. A callback can prepare another receipt without changing the first result. Public signatures remain `prepare(customer, rows)` and `Receipt.render(before_render=None)`.

## Types, module map and pseudocode
Keep app.py as the only implementation module. Receipt owns private customer and a tuple of materialized rows for its entire lifetime.
prepare(customer, rows): materialize rows to tuple; return Receipt(customer, tuple).
Receipt.render(callback=None): invoke callback if present; return a new mapping containing owned customer and sum(price * quantity for owned rows).
Bodies are design pseudocode, not implemented code.

## Rationale and risks
Per-handle ownership removes the module-wide current receipt. Every render computes from retained rows after the callback; no consumer coordination or extra public API. Reject shared state with save/restore because nested calls make it fragile. Retaining all rows costs O(rows) memory and repeated renders repeat summation. Customer/number mutation and exception timing beyond the fixed contract are unspecified.
'''
CANDIDATE_B = '''# Proposal B: receipt closure

## Usage and signatures
`first = prepare("Ada", [(3, 2)])`; prepare another receipt; `first.render()` still returns Ada/6. A callback can prepare another receipt without changing the first result. Public signatures remain `prepare(customer, rows)` and `Receipt.render(before_render=None)`.

## Types, module map and pseudocode
Keep app.py as the only implementation module. Each Receipt owns a private render closure capturing customer and a tuple of materialized rows for the handle's entire lifetime.
prepare(customer, rows): materialize rows to tuple; define render_value() returning a new mapping of captured customer and sum(price * quantity for captured rows); return Receipt(render_value).
Receipt.render(callback=None): invoke callback if present; return this handle's render_value().
Bodies are design pseudocode, not implemented code.

## Rationale and risks
The closure hides receipt storage behind a callable boundary. Every render computes from retained rows after the callback; no consumer coordination or extra public API. Reject shared state with save/restore because nested calls make it fragile. Retaining all rows costs O(rows) memory and repeated renders repeat summation. Customer/number mutation and exception timing beyond the fixed contract are unspecified.
'''


def write_fixture(workspace):
    scrap.write_fixture(workspace)
    for name, content in [('candidate-1', CANDIDATE_A), ('candidate-2', CANDIDATE_B)]:
        path = workspace / 'artifacts' / name / 'proposal.md'
        path.parent.mkdir(parents=True)
        path.write_text(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    root = Path(tempfile.mkdtemp(prefix='pstack-architect-convergence-')).resolve()
    workspace, home = root / 'workspace', root / 'home'
    write_fixture(workspace); home.mkdir()
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    def git(*words):
        return subprocess.run(['git', '-C', str(workspace), *words], check=True, capture_output=True, text=True).stdout.strip()
    git('init', '-q'); git('add', '.')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Seed fixed contract and two existing design proposals')
    entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
    subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)], check=True, capture_output=True)
    link = workspace / '.agents/skills/poteto-mode'; link.parent.mkdir(parents=True); link.symlink_to(entry)
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
    for name in ('synthesis', 'revisions'):
        (workspace / 'artifacts' / name).mkdir()
    before = snapshot(workspace); head = git('rev-parse', 'HEAD')
    (root / 'before.json').write_text(json.dumps(before, sort_keys=True))
    pair = {'model': args.model, 'effort': args.effort}
    prompt = ('$poteto-mode Continue Architect from the existing proposal packages artifacts/candidate-1/proposal.md and artifacts/candidate-2/proposal.md. '
        'They are manually authored fixture inputs, not outputs from agents in this session. Assess them through the workflow before deciding the next action for the fixed requirements in DESIGN.md. '
        'Preserve both original proposal directories, DESIGN.md, consumers.py and check.py unchanged. '
        'Primary owns artifacts/synthesis and may implement app.py after the required design comparison is complete; primary alone may execute python3 -B check.py. '
        'Any new design delegates may write only disjoint subdirectories of artifacts/revisions; research and judge are read-only and all delegates are static-only, without application imports or execution. '
        'Keep checklist in conversation; use artifacts/synthesis for grounding and decision records. '
        'No nested delegation, commits, external services, global configuration, installation or nested app-server. '
        'Use task selections ' + json.dumps([pair, pair]) + ' for architect-runner and ' + json.dumps(pair) +
        ' for how-explainer, why-investigator, why-synthesizer and arena-judge as applicable. Parent model/effort is ' + args.model + '/' + args.effort +
        '; resolve with --catalog ' + str(args.catalog.resolve(strict=True)) + '. Registered roles are installed. Ownership paths do not establish separate OS sandboxes.')
    (root / 'prompt.txt').write_text(prompt)
    auth = home / 'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True))
    client = None; result = {'status': 'error'}
    try:
        client = scrap.research.Client(args.codex, workspace, home, root)
        thread, result['status'] = client.run(workspace, args.model, args.effort, prompt, sandbox='workspace-write')
        summary, final = scrap.research.summarize_events(client.events, thread); result.update(summary)
        (root / 'final.txt').write_text(final)
        after = snapshot(workspace); (root / 'after.json').write_text(json.dumps(after, sort_keys=True))
        result['changed'] = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        result['scopePreserved'] = all(k == 'app.py' or k.startswith('artifacts/synthesis/') or k.startswith('artifacts/revisions/') for k in result['changed'])
        result['headIndexPreserved'] = git('rev-parse', 'HEAD') == head and not git('diff', '--cached', '--binary')
        result['appChanged'] = before.get('app.py') != after.get('app.py')
        result['verification'] = scrap.check(workspace)
    except (RuntimeError, TimeoutError, scrap.research.queue.Empty) as error:
        result['error'] = str(error)
    finally:
        scrap.reframe.finalize_capture(client, auth, root, result)
        result['behaviorVerdict'] = 'UNREVIEWED: inspect actual judge/primary comparison, replacement count or honest stop, and implementation authority; unchanged failing app can be a valid stop'
        (root / 'result.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
    return 0 if result['status'] == 'completed' and result.get('scopePreserved') and result.get('headIndexPreserved') and not result['cleanupErrors'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
