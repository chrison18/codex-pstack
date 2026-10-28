"""Exercise native Arena synthesis and Architect checkpoint/default implementation in disposable projects.

Artifact checks are necessary but not a semantic verdict. Inspect native events, candidate
ownership, judge ordering, full-artifact reads and structural diversity before recording a pass.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('research', Path(__file__).with_name('accept-codex-research.py'))
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)


def missing_output_evidence(outputs, candidates):
    """Require explicit reduced coverage and no invented second artifact."""
    try:
        coverage = json.loads((outputs / 'synthesis/coverage.json').read_text())
        return (coverage['complete'] is False
                and coverage['completed'] == ['candidate-1']
                and coverage['missing'] == ['candidate-2']
                and isinstance(coverage['reason'], str) and bool(coverage['reason'].strip())
                and candidates == [True, False]
                and not any((outputs / 'candidate-2').iterdir()))
    except (OSError, ValueError, KeyError, TypeError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    parser.add_argument('--case', action='append', choices=('arena', 'arena-same-model', 'arena-invalid-pool', 'arena-dropout', 'architect-checkpoint', 'architect-implement'))
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    entry = repo / 'plugins/pstack/skills/poteto-mode'
    root = Path(tempfile.mkdtemp(prefix='pstack-design-live-')).resolve()
    catalog = args.catalog.resolve(strict=True)
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    results = []
    for case in ('arena', 'arena-same-model', 'arena-invalid-pool', 'arena-dropout', 'architect-checkpoint', 'architect-implement'):
        if not args.case and case in ('arena-same-model', 'arena-invalid-pool', 'arena-dropout'):
            continue
        if args.case and case not in args.case:
            continue
        logs = root / case
        workspace, home = logs / 'workspace', logs / 'home'
        workspace.mkdir(parents=True)
        home.mkdir()
        def git(*arguments):
            return subprocess.run(['git', '-C', str(workspace), *arguments], check=True, capture_output=True, text=True).stdout.strip()
        (workspace / 'app.py').write_text('def total(items):\n    return sum(price * quantity for price, quantity in items)\n')
        (workspace / 'check.py').write_text('from app import total\nassert total([]) == 0\nassert total([(3, 2), (5, 1)]) == 11\nassert total([(9, 0)]) == 0\ntry:\n    total([(3, -1)])\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError("negative quantity must fail")\nprint("design acceptance passed")\n')
        git('init', '-q'); git('add', '.')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Initialize total API; existing callers pass price quantity tuples')
        link = workspace / '.agents/skills/poteto-mode'
        link.parent.mkdir(parents=True); link.symlink_to(entry)
        subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)], check=True, capture_output=True)
        outputs = workspace / 'artifacts'
        for name in ('candidate-1', 'candidate-2', 'synthesis'):
            (outputs / name).mkdir(parents=True)
        (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n'
            '[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
        before = snapshot(workspace); head = git('rev-parse', 'HEAD'); index = git('diff', '--cached', '--binary')
        task = ('Use Arena to produce two independent Python artifact candidates for the total API, then crossjudge, synthesize into artifacts/synthesis/app.py and verify that exact synthesized file. ' if case in ('arena', 'arena-same-model', 'arena-invalid-pool', 'arena-dropout') else
                'Use Architect for the total API: compare at least two structurally different designs (for example validated records versus a pure functional boundary), then crossjudge and synthesize the design package. ')
        task += ('Preserve total(items) callers with (price, quantity) tuples, sum price*quantity, empty input 0, zero quantity 0; reject negative quantity with ValueError. '
                 'Candidate outputs are non-production artifact packages under the precreated artifacts/candidate-1 and artifacts/candidate-2 only. '
                 'Each runner owns only its assigned directory, must produce a rationale and concrete inspectable artifacts, and must not edit app.py, check.py, configuration, or other candidate directories. '
                 'Primary writes grounding and synthesized design only under artifacts/synthesis. Judge is read-only. No nested delegation by runners/judge. ')
        if case == 'architect-checkpoint':
            task += 'STOP after showing the synthesized design; wait for my approval before implementation. Do not implement or execute app.py; keep production app.py and check.py byte-identical. '
        elif case == 'architect-implement':
            task += 'Continue through the default implementation phase without an extra approval checkpoint. Grounding, candidate and judge work must be static: no delegate may execute or import app.py or check.py. Pass that restriction explicitly to every assignment, including the How explainer. After design synthesis, primary alone may implement app.py and run python3 -B check.py; do not change check.py. '
        else:
            task += 'Do not change production app.py or check.py. Verify the synthesized artifact by loading its absolute path and applying the check.py contract. '
        pool = 'arena-runner' if case in ('arena', 'arena-same-model', 'arena-invalid-pool', 'arena-dropout') else 'architect-runner'
        selections = ([{'model': args.model, 'effort': args.effort}] * 2 if case in ('arena-same-model', 'arena-dropout') else
                      [{'model': 'gpt-6.1-sol', 'effort': 'low'}, {'model': 'gpt-6-luna', 'effort': 'medium'}])
        if case == 'arena-invalid-pool':
            selections = [{'model': args.model, 'effort': args.effort},
                          {'model': 'pstack-unavailable-acceptance-model', 'effort': args.effort}]
        task += ('Resolve the complete ' + pool + ' pool with task selections ' + json.dumps(selections) + '. '
                 'Resolve arena-judge with task model gpt-6-luna and effort medium. These choices are ephemeral. '
                 'The observed parent model/effort is ' + args.model + '/' + args.effort + '; use --catalog ' + str(catalog) + '. '
                 'Native role installation is already complete. Use explicit resolved model and reasoning_effort in native spawn; global defaults deliberately differ. '
                 'No external services, nested app-server, commits, PRs, role installation, model preference writes or configuration changes. '
                 'Keep checklist in conversation. This is a disposable workspace-write fixture; directory ownership is a task constraint, not a per-agent sandbox guarantee.')
        if case == 'arena-same-model':
            task += ' This is an explicitly same-model runner pool. Preserve both selections; independent candidates do not imply model diversity. Report pool diversity separately from judge identity. '
        if case == 'arena-invalid-pool':
            task += ' The exact explicit pool is mandatory: if resolution fails, stop before any delegation or artifact writes, disclose the prerequisite failure and do not substitute models, perform primary-only synthesis, or install/change configuration. '
        if case == 'arena-dropout':
            task += (' Controlled missing-output scenario: start both selected runners independently. '
                     'Runner 1 owns candidate-1 and produces the normal artifact. Runner 2 owns candidate-2 but must simulate an unavailable required input: '
                     'read the entry and grounding, then return BLOCKED with no files or candidate content, no retries and no substitute. '
                     'Pass this instruction only to runner 2; do not fabricate its report. Wait for both terminal results. '
                     'The user explicitly permits N-1 synthesis here: judge and verify only actual completed candidate 1, disclose missing candidate 2 and reduced coverage. '
                     'Do not claim two candidates, a comparison victory, or process-crash recovery. Write artifacts/synthesis/coverage.json '
                     'as {complete:false,completed:["candidate-1"],missing:["candidate-2"],reason:TEXT}. '
                     'No replacement worker, no nested delegation, and no writing candidate-2 on its behalf.')
        if case in ('arena-same-model', 'arena-dropout'):
            task += ' All runner and judge spawns must use fork_turns none with a self-contained scoped brief and absolute entry/grounding pointers; do not inherit the parent conversation. '
        prompt = '$poteto-mode ' + task
        (logs / 'prompt.txt').write_text(prompt)
        auth = home / 'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True))
        client = None; thread = None; status = 'error'; interrupted = False
        try:
            client = research.Client(args.codex, workspace, home, logs)
            thread, status = client.run(workspace, args.model, args.effort, prompt, sandbox='workspace-write')
        except (RuntimeError, queue.Empty, TimeoutError, KeyboardInterrupt) as error:
            interrupted = isinstance(error, KeyboardInterrupt)
            status = 'interrupted' if interrupted else 'error'
            (logs / 'harness-error.txt').write_text(str(error))
        finally:
            if client:
                client.close()
            auth.unlink(missing_ok=True)
        after = snapshot(workspace)
        (logs / 'before.json').write_text(json.dumps(before, sort_keys=True))
        (logs / 'after.json').write_text(json.dumps(after, sort_keys=True))
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        unexpected = [k for k in changed if not k.startswith('artifacts/') and not (case == 'architect-implement' and k == 'app.py')]
        summary, final = research.summarize_events(client.events if client else [], thread)
        (logs / 'final.txt').write_text(final)
        verify = None
        if status == 'completed' and case not in ('architect-checkpoint', 'arena-invalid-pool'):
            target = outputs / 'synthesis/app.py' if case in ('arena', 'arena-same-model', 'arena-invalid-pool', 'arena-dropout') else workspace / 'app.py'
            code = 'import runpy\ntotal = runpy.run_path(' + repr(str(target)) + ')["total"]\n' + (workspace / 'check.py').read_text().split('\n', 1)[1]
            run = subprocess.run(['python3', '-B', '-c', code], cwd=workspace, capture_output=True, text=True)
            verify = {'exitCode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}
            (logs / 'verification.json').write_text(json.dumps(verify, indent=2))
        candidates = [any((outputs / name).rglob('*.md')) for name in ('candidate-1', 'candidate-2')]
        result = {'case': case, 'status': status, 'changed': changed, 'unexpectedChanges': unexpected,
                  'candidateRationalesPresent': candidates, **summary,
                  'artifactChecksPassed': status == 'completed' and not unexpected and all(candidates)
                  and git('rev-parse', 'HEAD') == head and git('diff', '--cached', '--binary') == index
                  and (verify is None or verify['exitCode'] == 0)}
        if case == 'arena-dropout':
            result['dropoutEvidence'] = missing_output_evidence(outputs, candidates)
            result['artifactChecksPassed'] = (status == 'completed' and not unexpected
                and result['dropoutEvidence'] and verify is not None and verify['exitCode'] == 0
                and git('rev-parse', 'HEAD') == head and git('diff', '--cached', '--binary') == index)
        if case == 'arena-invalid-pool':
            result['artifactChecksPassed'] = (status == 'completed' and not changed
                and not summary['spawnRequests'] and not summary['resolvedAgentStarts']
                and git('rev-parse', 'HEAD') == head and git('diff', '--cached', '--binary') == index)
        result['behaviorVerdict'] = 'UNREVIEWED: inspect resolution, reads, delegation ordering and final claims'
        (logs / 'result.json').write_text(json.dumps(result, indent=2)); results.append(result)
        print(json.dumps(result), flush=True)
        if interrupted:
            break
    print('Scope: native backend artifact candidates; manually audit semantics/ordering. Not desktop UI or code-worktree isolation evidence.')
    return 0 if all(r['artifactChecksPassed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
