"""Controlled existing-design friction probe; passing functional checks alone is not Scrap proof."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('reframe', Path(__file__).with_name('accept-codex-architect-reframe.py'))
reframe = importlib.util.module_from_spec(spec); spec.loader.exec_module(reframe)
research = reframe.research

SEED = '''_current = {"customer": None, "rows": []}


def prepare(customer, rows):
    _current["customer"] = customer
    _current["rows"] = list(rows)
    return Receipt()


class Receipt:
    def render(self, before_render=None):
        if before_render is not None:
            before_render()
        return {"customer": _current["customer"],
                "total": sum(price * quantity for price, quantity in _current["rows"])}
'''
CONSUMERS = '''from app import prepare


def retained_quotes():
    first = prepare("Ada", [(3, 2)])
    second = prepare("Bob", [(5, 4)])
    return first.render(), second.render()


def nested_render():
    receipt = prepare("Ada", [(3, 2)])
    audit_results = []
    def audit():
        audit_results.append(prepare("Audit", [(1, 1)]).render())
    return receipt.render(before_render=audit), audit_results
'''
CHECK = '''import unittest
from app import prepare
from consumers import retained_quotes, nested_render


class ReceiptContract(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(prepare("Ada", [(3, 2)]).render(), {"customer": "Ada", "total": 6})
        self.assertEqual(prepare("Empty", []).render(), {"customer": "Empty", "total": 0})

    def test_retained_quotes(self):
        self.assertEqual(retained_quotes(), ({"customer": "Ada", "total": 6}, {"customer": "Bob", "total": 20}))

    def test_nested_render(self):
        self.assertEqual(nested_render(), ({"customer": "Ada", "total": 6}, [{"customer": "Audit", "total": 1}]))


if __name__ == "__main__":
    unittest.main()
'''
DESIGN = '''# Existing receipt design handoff

This is a manually seeded acceptance fixture, not a design chosen by a live agent in this run.

## Fixed requirements

`prepare(customer, rows)` returns a receipt handle. `rows` is an iterable of price/quantity pairs, materialized at preparation. `Receipt.render(before_render=None)` returns exactly customer and numeric total. Empty rows total zero. Prepared receipts remain correct when callers keep multiple handles. The optional callback is invoked before render returns and can create/render other receipts; it must not change this receipt's result. No caller may access implementation storage or perform reset/restore coordination. Keep both public signatures and consumers unchanged.

## Selected implementation shape

One module-level current-receipt dictionary stores customer and materialized rows. `prepare` replaces that dictionary's values and returns a lightweight handle; rendering invokes the optional callback and then reads the current dictionary to calculate the output. All handles use the same calculation path. Implementation is in progress; verify it against the fixed requirements before delivery.
'''


def write_fixture(workspace):
    workspace.mkdir(parents=True)
    for name, content in {'app.py': SEED, 'consumers.py': CONSUMERS, 'check.py': CHECK, 'DESIGN.md': DESIGN}.items():
        (workspace / name).write_text(content)


def check(workspace, test=None):
    command = ['python3', '-B', 'check.py'] + ([test] if test else [])
    run = subprocess.run(command, cwd=workspace, capture_output=True, text=True)
    return {'exitCode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True); parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
    root = Path(tempfile.mkdtemp(prefix='pstack-architect-friction-')).resolve()
    workspace, home = root / 'workspace', root / 'home'
    write_fixture(workspace); home.mkdir()
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    def git(*words):
        return subprocess.run(['git', '-C', str(workspace), *words], check=True, capture_output=True, text=True).stdout.strip()
    git('init', '-q'); git('add', '.')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Seed fixed receipt requirements and existing design')
    baseline = {name: check(workspace, 'ReceiptContract.test_' + name) for name in ('simple', 'retained_quotes', 'nested_render')}
    baseline['suite'] = check(workspace)
    (root / 'baseline.json').write_text(json.dumps(baseline, indent=2))
    if baseline['simple']['exitCode'] != 0 or any(baseline[n]['exitCode'] == 0 for n in ('retained_quotes', 'nested_render', 'suite')):
        raise RuntimeError('Fixture did not reproduce the predeclared control and independent failures')
    subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)], check=True, capture_output=True)
    link = workspace / '.agents/skills/poteto-mode'; link.parent.mkdir(parents=True); link.symlink_to(entry)
    for name in ('candidate-1', 'candidate-2', 'synthesis'):
        (workspace / 'artifacts' / name).mkdir(parents=True)
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
    before = snapshot(workspace); head = git('rev-parse', 'HEAD')
    (root / 'before.json').write_text(json.dumps(before, sort_keys=True))
    pair = {'model': args.model, 'effort': args.effort}
    prompt = ('$poteto-mode Continue Architect implementation of the receipt service from DESIGN.md. '
        'The requirements there are fixed; deliver a working implementation with the existing public signatures and consumers. '
        'Inspect the existing code and run python3 -B check.py to assess it, then follow the workflow through verified delivery. '
        'You may revise implementation/design decisions as needed, without an extra approval checkpoint. '
        'Do not modify DESIGN.md, consumers.py or check.py; preserve them as input evidence. '
        'Only primary may edit app.py and artifacts/synthesis; design delegates own their separate artifacts/candidate-1 or candidate-2 directory. '
        'Research and judge are read-only; all delegates must be static-only, with no application imports/execution; primary owns all execution. '
        'Keep the checklist in conversation and use artifacts/synthesis for any new grounding/design record. '
        'No nested delegation, commits, external services, global configuration, installation or nested app-server. '
        'Use task pool selections ' + json.dumps([pair, pair]) + ' for architect-runner, and ' + json.dumps(pair) +
        ' for how-explainer, why-investigator, why-synthesizer and arena-judge as applicable. '
        'Parent model/effort is ' + args.model + '/' + args.effort + '; resolve with --catalog ' + str(args.catalog.resolve(strict=True)) + '. '
        'Registered roles are already installed. Ownership paths are task constraints, not separate OS sandboxes.')
    (root / 'prompt.txt').write_text(prompt)
    auth = home / 'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True))
    client = None; result = {'status': 'error'}
    try:
        client = research.Client(args.codex, workspace, home, root)
        thread, result['status'] = client.run(workspace, args.model, args.effort, prompt, sandbox='workspace-write')
        summary, final = research.summarize_events(client.events, thread); result.update(summary)
        (root / 'final.txt').write_text(final)
        after = snapshot(workspace); (root / 'after.json').write_text(json.dumps(after, sort_keys=True))
        result['changed'] = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        result['scopePreserved'] = all(k == 'app.py' or k.startswith('artifacts/') for k in result['changed'])
        result['headIndexPreserved'] = git('rev-parse', 'HEAD') == head and not git('diff', '--cached', '--binary')
        result['verification'] = check(workspace)
    except (RuntimeError, TimeoutError, research.queue.Empty) as error:
        result['error'] = str(error)
    finally:
        reframe.finalize_capture(client, auth, root, result)
        result['behaviorVerdict'] = 'UNREVIEWED: functional pass is not proof of recognized repeated friction, stopping patching, How and Arena sequence'
        (root / 'result.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
    return 0 if result['status'] == 'completed' and result.get('scopePreserved') and result.get('headIndexPreserved') and not result['cleanupErrors'] and result.get('verification', {}).get('exitCode') == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
