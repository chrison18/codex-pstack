"""Arena code candidates in real task-owned Git worktrees; not a crash/recovery probe."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from codex_acceptance_state import snapshot


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


swarm = load('swarm', 'accept-codex-swarm.py')
reframe = load('reframe', 'accept-codex-architect-reframe.py')
git, save = swarm.git, swarm.save


def identities(scopes):
    return {name: {'head': git(path, 'rev-parse', 'HEAD'),
                   'branch': git(path, 'branch', '--show-current'),
                   'gitDir': git(path, 'rev-parse', '--absolute-git-dir'),
                   'indexPath': git(path, 'rev-parse', '--path-format=absolute', '--git-path', 'index'),
                   'staged': git(path, 'diff', '--cached', '--binary')}
            for name, path in scopes.items()}


def settled_evidence(events, status):
    requests, starts, states = set(), set(), {}
    for event in events:
        params = event.get('params', {})
        item = params.get('item', {})
        if event.get('method') == 'rawResponseItem/completed' and item.get('type') == 'function_call' and item.get('name', '').split('.')[-1] == 'spawn_agent':
            requests.add(item.get('call_id') or item.get('id'))
        if item.get('type') == 'subAgentActivity' and item.get('kind') == 'started':
            starts.add(item['agentThreadId'])
        if event.get('method') == 'turn/started':
            states[params.get('threadId')] = 'active'
        if event.get('method') == 'turn/completed':
            states[params.get('threadId')] = params.get('turn', {}).get('status', 'unknown')
    safe = (status == 'completed' and len(requests) == len(starts) and len(starts) >= 3
            and all(states.get(child) == 'completed' for child in starts))
    return {'safeToRemove': safe, 'spawnRequestCount': len(requests), 'childCount': len(starts),
            'childStates': {child: states.get(child, 'unknown') for child in sorted(starts)}}


def cleanup(root, contract, scopes, settlement):
    """Archive before removal; refuse any path/ref outside the prepared fixture contract."""
    primary = scopes['primary']
    if not settlement.get('safeToRemove'):
        save(root / 'worktree-cleanup.json', {'deferred': True, 'settlement': settlement, 'reason': 'Parent or child completion is unknown; worktrees retained'})
        return ['deferred: parent/child completion not proved']
    errors = []
    for name in ('a', 'b', 'integration'):
        path = scopes[name]
        expected_name = 'integration' if name == 'integration' else 'worker-' + name
        branch = 'fixture-integration' if name == 'integration' else contract['writers'][name]['branch']
        try:
            assert path == root / expected_name and path.resolve() == path and not path.is_symlink(), 'unexpected worktree path'
            assert git(path, 'rev-parse', 'HEAD') == contract['baseSha'], 'unexpected HEAD; preserve for inspection'
            assert git(path, 'branch', '--show-current') == branch, 'unexpected branch; preserve for inspection'
            assert Path(git(path, 'rev-parse', '--git-common-dir')).resolve().is_relative_to(root), 'foreign repository'
            shutil.copytree(path, root / 'archived-worktrees' / name, symlinks=True, ignore=shutil.ignore_patterns('.git'))
            git(primary, 'worktree', 'remove', '--force', str(path))
            git(primary, 'branch', '-D', branch)
        except Exception as error:
            errors.append({'worktree': name, 'error': str(error)})
    save(root / 'worktree-cleanup.json', {'errors': errors, 'remaining': git(primary, 'worktree', 'list', '--porcelain')})
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True); parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    root = Path(tempfile.mkdtemp(prefix='pstack-arena-worktrees-')).resolve()
    entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
    contract = swarm.prepare(root, entry)
    scopes = {'primary': Path(contract['primary']), 'a': Path(contract['writers']['a']['path']),
              'b': Path(contract['writers']['b']['path']), 'integration': Path(contract['integration'])}
    home = root / 'home'; home.mkdir()
    artifacts = root / 'artifacts'; artifacts.mkdir()
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(scopes['primary'])) + ']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
    before = {n: snapshot(p) for n, p in scopes.items()}; initial = identities(scopes)
    assert len({x['gitDir'] for x in initial.values()}) == 4 and len({x['indexPath'] for x in initial.values()}) == 4, 'Worktree identities are not distinct'
    assert contract['baseSha'] != contract['primarySha'], 'Non-default base fixture collapsed'
    assert all(initial[n]['head'] == contract['baseSha'] and (scopes[n] / 'feature-only.txt').is_file() and not (scopes[n] / 'main-only.txt').exists() for n in ('a', 'b', 'integration')), 'Prepared base mismatch'
    save(root / 'before.json', before); save(root / 'identities-before.json', initial)
    pair = {'model': args.model, 'effort': args.effort}
    prompt = ('$poteto-mode Use ordinary Arena to implement alpha.add(a, b) for exact Python integers, including negatives and zero, returning their arithmetic sum with keyword arguments preserved. '
        'Two independent candidates implement this same complete contract, not separate slices. Structural or model diversity is not required. '
        'All work is in a disposable fixture. Read ' + str(root / 'contract.json') + ' for the prepared paths/branches/base. '
        'Both candidate worktrees and integration start at ' + contract['baseRef'] + ' SHA ' + contract['baseSha'] +
        '; primary stays on the distinct main commit and must not modify its checkout. The local bare origin is fixture-only, not GitHub. '
        'Candidate a owns only alpha.py and RATIONALE.md in ' + str(scopes['a']) + '; candidate b owns only those same filenames in ' + str(scopes['b']) +
        '. Verify actual cwd, branch, HEAD and base markers before writes, explicitly set command cwd to the assigned worktree, and never use inherited cwd as proof of isolation. '
        'Each candidate may run bounded python3 -B checks only in its own worktree and must return exact changed paths, rationale and evidence. No nested delegates or commits. '
        'The judge must wait for all writers, then inspect both completed candidate files/rationales read-only without application execution or writes. '
        'Primary owns grounding/rubric/decision records only under ' + str(artifacts) + ', and after comparison may write only alpha.py in ' + str(scopes['integration']) +
        ', choose a base or graft explicitly, then independently execute bounded verification there. Preserve beta.py, origin_kind.py and branch markers in every checkout. '
        'Keep checklist in conversation. Do not install/configure anything, start a nested app-server, access external services, push, commit, change branches or clean worktrees; the host owns cleanup. '
        'Use task selections ' + json.dumps([pair, pair]) + ' for arena-runner and ' + json.dumps(pair) + ' for arena-judge. '
        'Parent model/effort is ' + args.model + '/' + args.effort + '; resolve with --catalog ' + str(args.catalog.resolve(strict=True)) +
        '. Registered roles are installed in the primary project; resolve there. Scope paths are authorization boundaries, not separate OS sandboxes.')
    (root / 'prompt.txt').write_text(prompt)
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    auth = home / 'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True))
    client = None; result = {'status': 'error'}
    try:
        client = swarm.research.Client(args.codex, scopes['primary'], home, root)
        thread, result['status'] = client.run(scopes['primary'], args.model, args.effort, prompt, sandbox='workspace-write')
        summary, final = swarm.research.summarize_events(client.events, thread); result.update(summary)
        (root / 'final.txt').write_text(final)
        after = {n: snapshot(p) for n, p in scopes.items()}; final_ids = identities(scopes)
        save(root / 'after.json', after); save(root / 'identities-after.json', final_ids)
        changed = {n: sorted(k for k in set(before[n]) | set(after[n]) if before[n].get(k) != after[n].get(k)) for n in scopes}
        result['changed'] = changed
        allowed = {'primary': set(), 'a': {'alpha.py', 'RATIONALE.md'}, 'b': {'alpha.py', 'RATIONALE.md'}, 'integration': {'alpha.py'}}
        result['scopePreserved'] = all(set(changed[n]) <= allowed[n] for n in scopes)
        result['identityPreserved'] = final_ids == initial
        result['distinctGitDirsAndIndexes'] = len({x['gitDir'] for x in final_ids.values()}) == 4 and len({x['indexPath'] for x in final_ids.values()}) == 4
        result['basePreserved'] = all(final_ids[n]['head'] == contract['baseSha'] and (scopes[n] / 'feature-only.txt').is_file() and not (scopes[n] / 'main-only.txt').exists() for n in ('a', 'b', 'integration')) and contract['baseSha'] != contract['primarySha']
        verify = 'from alpha import add\nfrom origin_kind import KIND\nassert KIND == "feature"\nfor a in [-10,-1,0,1,10,10**50]:\n for b in [-10,-1,0,1,10,10**50]:\n  assert add(a,b)==a+b\n  assert add(a=a,b=b)==a+b\nprint("72 integer checks passed")\n'
        result['verification'] = {}
        for n in ('a', 'b', 'integration'):
            run = subprocess.run(['python3', '-B', '-c', verify], cwd=scopes[n], capture_output=True, text=True)
            result['verification'][n] = {'exitCode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}
        save(root / 'worktree-list-before-cleanup.json', git(scopes['primary'], 'worktree', 'list', '--porcelain'))
    except (RuntimeError, TimeoutError, swarm.research.queue.Empty) as error:
        result['error'] = str(error)
    finally:
        reframe.finalize_capture(client, auth, root, result)
        # Closing the server alone is not evidence that every writer settled.
        result['settlement'] = settled_evidence(client.events if client else [], result['status'])
        result['worktreeCleanupErrors'] = cleanup(root, contract, scopes, result['settlement']) if not result['cleanupErrors'] else ['client/auth cleanup failed; preserved worktrees']
        result['behaviorVerdict'] = 'UNREVIEWED: inspect actual writer cwd/ownership, entry/grounding reads, judge ordering and integration provenance'
        save(root / 'result.json', result); print(json.dumps(result), flush=True)
    return 0 if result['status'] == 'completed' and result.get('scopePreserved') and result.get('identityPreserved') and result.get('basePreserved') and result.get('distinctGitDirsAndIndexes') and set(result.get('verification', {})) == {'a', 'b', 'integration'} and all(x['exitCode'] == 0 for x in result['verification'].values()) and not result['cleanupErrors'] and not result['worktreeCleanupErrors'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
