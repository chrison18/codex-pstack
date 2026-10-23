"""Native Swarm acceptance: real worktrees/non-default base and a scoped local-state probe.

The publish subcommand gates model-authored proposals so two distinct writer processes
are active together. It supplies no implementation. Inspect native events as well as
artifact checks; these fixtures do not prove browser or independent OS sandbox parity.
"""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import queue
import secrets
import subprocess
import sys
import tempfile
import threading
import time

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('research', Path(__file__).with_name('accept-codex-research.py'))
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)


def git(root, *arguments):
    return subprocess.run(['git', '-C', str(root), *arguments], check=True, capture_output=True, text=True).stdout.strip()


def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def publish(root, name):
    contract = json.loads((root / 'contract.json').read_text())
    scope = contract['writers'][name]
    worktree = Path(scope['path']).resolve(strict=True)
    assert Path.cwd().resolve() == worktree, 'Set the assigned worktree as command cwd first'
    assert git(worktree, 'rev-parse', 'HEAD') == contract['baseSha'], 'Wrong base SHA'
    assert git(worktree, 'branch', '--show-current') == scope['branch'], 'Wrong branch'
    assert (worktree / 'feature-only.txt').is_file() and not (worktree / 'main-only.txt').exists(), 'Wrong branch contents'
    proposal = (worktree / 'proposal.py').read_bytes()
    entry = {'pid': os.getpid(), 'cwd': str(worktree), 'branch': scope['branch'],
             'head': git(worktree, 'rev-parse', 'HEAD'), 'enteredAtNs': time.time_ns(),
             'gitDir': git(worktree, 'rev-parse', '--absolute-git-dir'),
             'index': git(worktree, 'rev-parse', '--path-format=absolute', '--git-path', 'index')}
    save(worktree / '.writer-entered.json', entry)
    deadline = time.monotonic() + 300
    def wait(predicate):
        while not predicate():
            if time.monotonic() >= deadline:
                raise TimeoutError('Other writer did not reach the bounded publish barrier')
            time.sleep(0.1)
    wait(lambda: (root / 'release.json').exists())
    (worktree / scope['module']).write_bytes(proposal)
    (worktree / 'worker-proof.txt').write_text(name + '\n')
    save(worktree / '.writer-written.json', {'writtenAtNs': time.time_ns(), 'sha256': hashlib.sha256(proposal).hexdigest()})
    wait(lambda: all((Path(s['path']) / '.writer-written.json').exists() for s in contract['writers'].values()))
    save(worktree / '.writer-finished.json', {'finishedAtNs': time.time_ns(), 'pid': os.getpid()})
    print(json.dumps({'status': 'published', **entry, 'module': scope['module']}))


def release_when_ready(root, contract, stop):
    while not stop.wait(0.01):
        paths = [Path(s['path']) / '.writer-entered.json' for s in contract['writers'].values()]
        if not all(p.exists() for p in paths):
            continue
        pids = [json.loads(p.read_text())['pid'] for p in paths]
        live = []
        for pid in pids:
            try:
                os.kill(pid, 0)
                live.append(pid)
            except OSError:
                pass
        save(root / 'release.json', {'releasedAtNs': time.time_ns(), 'pids': pids,
                                    'bothPidsAlive': len(set(live)) == len(paths)})
        return


def writer_evidence(root, contract):
    checks, receipts = {}, []
    integration = Path(contract['integration'])
    try:
        release = json.loads((root / 'release.json').read_text())
        for name, scope in contract['writers'].items():
            path = Path(scope['path'])
            receipts.append({**json.loads((path / '.writer-entered.json').read_text()),
                             **json.loads((path / '.writer-written.json').read_text()),
                             **json.loads((path / '.writer-finished.json').read_text())})
        checks['overlappingWriterIntervals'] = max(r['enteredAtNs'] for r in receipts) < min(r['finishedAtNs'] for r in receipts)
        checks['barrierOrderAndLivePids'] = (release['bothPidsAlive']
            and max(r['enteredAtNs'] for r in receipts) <= release['releasedAtNs']
            <= min(r['writtenAtNs'] for r in receipts)
            and max(r['writtenAtNs'] for r in receipts) <= min(r['finishedAtNs'] for r in receipts))
        checks['distinctGitDirsIndexesAndPids'] = all(len({r[k] for r in receipts}) == len(receipts)
                                                    for k in ('gitDir', 'index', 'pid', 'cwd', 'branch'))
        checks['assignedWriterIdentities'] = all(r['cwd'] == scope['path'] and r['branch'] == scope['branch']
            and r['head'] == contract['baseSha'] for r, scope in zip(receipts, contract['writers'].values()))
        # Workers may turn their own proof files into richer evidence reports; no text format is required.
        proofs = [(Path(s['path']) / 'worker-proof.txt').read_bytes() for s in contract['writers'].values()]
        checks['distinctWorkerProofs'] = all(proofs) and len(set(proofs)) == len(proofs)
        checks['proposalAndIntegrationIdentity'] = all(
            (Path(s['path']) / 'proposal.py').read_bytes() == (Path(s['path']) / s['module']).read_bytes()
            == (integration / s['module']).read_bytes() for s in contract['writers'].values())
    except (OSError, ValueError, KeyError, TypeError):
        checks['writerEvidenceComplete'] = False
    return checks, receipts


def prepare(root, entry):
    primary = root / 'primary'
    primary.mkdir()
    git(primary, 'init', '-q', '-b', 'main')
    for module, function in [('alpha.py', 'add'), ('beta.py', 'multiply')]:
        (primary / module).write_text('def ' + function + '(a, b):\n    raise NotImplementedError\n')
    (primary / 'origin_kind.py').write_text('KIND = "common"\n')
    def commit(message):
        git(primary, 'add', '.')
        git(primary, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', message)
    commit('Initialize arithmetic slices')
    git(primary, 'checkout', '-qb', 'fixture-base')
    (primary / 'origin_kind.py').write_text('KIND = "feature"\n')
    (primary / 'feature-only.txt').write_text('Required non-default branch contract\n')
    commit('Prepare non-default feature contract')
    base = git(primary, 'rev-parse', 'HEAD')
    git(primary, 'checkout', 'main')
    (primary / 'main-only.txt').write_text('Unrelated default-branch change; must not enter integration\n')
    (primary / 'origin_kind.py').write_text('KIND = "main"\n')
    (primary / 'alpha.py').write_text('def unrelated_main_add(a, b):\n    return "not the requested base"\n')
    commit('Add unrelated main-only behavior')
    remote = root / 'fixture-remote.git'
    subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
    git(primary, 'remote', 'add', 'origin', str(remote))
    git(primary, 'push', '-q', 'origin', 'main', 'fixture-base')
    subprocess.run(['git', '--git-dir', str(remote), 'symbolic-ref', 'HEAD', 'refs/heads/main'], check=True)
    git(primary, 'fetch', '-q', 'origin')
    writers = {}
    for name, module in [('a', 'alpha.py'), ('b', 'beta.py')]:
        path = root / ('worker-' + name)
        branch = 'fixture-worker-' + name
        git(primary, 'worktree', 'add', '-q', '-b', branch, str(path), 'origin/fixture-base')
        writers[name] = {'path': str(path), 'branch': branch, 'module': module}
    integration = root / 'integration'
    git(primary, 'worktree', 'add', '-q', '-b', 'fixture-integration', str(integration), 'origin/fixture-base')
    link = primary / '.agents/skills/poteto-mode'
    link.parent.mkdir(parents=True); link.symlink_to(entry)
    subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(primary)], check=True, capture_output=True)
    contract = {'primary': str(primary), 'primarySha': git(primary, 'rev-parse', 'HEAD'),
                'baseRef': 'origin/fixture-base', 'baseSha': base, 'writers': writers,
                'integration': str(integration), 'remote': str(remote)}
    save(root / 'contract.json', contract)
    return contract


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'publish':
        parser = argparse.ArgumentParser()
        parser.add_argument('publish'); parser.add_argument('--fixture-root', required=True, type=Path)
        parser.add_argument('--worker', required=True, choices=('a', 'b'))
        args = parser.parse_args(); publish(args.fixture_root.resolve(strict=True), args.worker)
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex'); parser.add_argument('--model', required=True)
    parser.add_argument('--effort', required=True); parser.add_argument('--catalog', required=True, type=Path)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    args = parser.parse_args()
    entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
    root = Path(tempfile.mkdtemp(prefix='pstack-swarm-live-')).resolve()
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    contract = prepare(root, entry)
    primary = Path(contract['primary']); integration = Path(contract['integration'])
    home = root / 'home'; home.mkdir(); reports = root / 'reports'; reports.mkdir()
    (home / 'config.toml').write_text('[projects.' + json.dumps(str(primary)) + ']\ntrust_level="trusted"\n'
        '[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n'
        '[sandbox_workspace_write]\nnetwork_access=true\nwritable_roots=[' + json.dumps(str(root)) + ']\n')
    token = secrets.token_urlsafe(24); challenge = secrets.token_hex(16); requests = []
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            accepted = self.path == '/probe' and self.headers.get('Authorization') == 'Bearer ' + token
            result = {'authenticated': accepted, 'clientPid': self.headers.get('X-Probe-Pid'), 'at': time.monotonic()}
            requests.append(result)
            self.send_response(200 if accepted else 403); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({'ready': accepted, 'challenge': challenge if accepted else None,
                                       'requestId': len(requests)}).encode())
        def log_message(self, *_):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    local = primary / '.local-state'; local.mkdir()
    (local / 'token').write_text(token)
    (local / 'endpoint').write_text('http://127.0.0.1:' + str(server.server_address[1]) + '/probe')
    (primary / 'local_probe.py').write_text('''from pathlib import Path
import json, os, urllib.request
root = Path.cwd()
assert root.resolve() == Path(__file__).resolve().parent, "Probe requires the primary checkout cwd"
state = root / '.local-state'
request = urllib.request.Request((state / 'endpoint').read_text(), headers={
    'Authorization': 'Bearer ' + (state / 'token').read_text(), 'X-Probe-Pid': str(os.getpid())})
with urllib.request.urlopen(request, timeout=5) as response:
    result = json.load(response)
assert result['ready'] and result['challenge']
print(json.dumps(result))
''')
    isolated = subprocess.run(['python3', '-B', str(primary / 'local_probe.py')], cwd=Path(contract['writers']['a']['path']), capture_output=True, text=True)
    save(root / 'isolated-probe.json', {'exitCode': isolated.returncode, 'stderr': isolated.stderr,
                                      'workerHasLocalState': (Path(contract['writers']['a']['path']) / '.local-state').exists()})
    scopes = {'primary': primary, 'integration': integration, **{n: Path(s['path']) for n, s in contract['writers'].items()}}
    before = {n: snapshot(p) for n, p in scopes.items()}
    heads = {n: git(p, 'rev-parse', 'HEAD') for n, p in scopes.items()}
    indexes = {n: git(p, 'diff', '--cached', '--binary') for n, p in scopes.items()}
    save(root / 'before.json', before)
    stop = threading.Event()
    threading.Thread(target=release_when_ready, args=(root, contract, stop), daemon=True).start()
    prompt = ('$poteto-mode Use Swarm partitioned coverage with three required slices: writer a implements add(a,b) in alpha.py; '
              'writer b implements multiply(a,b) in beta.py; a read-only verifier proves the primary checkout local process/auth state is reachable. '
              'Both APIs must support positional and keyword operands, negative and zero inputs. No commits, PRs, config changes, branch resets, role installation, '
              'nested delegation, external services or worktree cleanup. The fixture remote is a local bare Git repository, not GitHub. '
              'Primary cwd stays on main; do not edit it. Writers and integration start from the pushed non-default origin/fixture-base at ' + contract['baseSha'] + '. '
              'Read contract.json at ' + str(root / 'contract.json') + ' for all precreated worktree paths and branch names. '
              'Writers must verify cwd/branch/HEAD/feature-only.txt/no main-only.txt before writing. Each owns only its worktree, proposal.py, its assigned module, '
              'worker-proof.txt and publisher receipts. No reading other worker code. Write your own implementation to proposal.py, then publish it using '
              'python3 -B ' + str(Path(__file__).resolve()) + ' publish --fixture-root ' + str(root) + ' --worker a (or b) with command cwd explicitly set to your assigned worktree. '
              'This bounded barrier waits for BOTH independent writer processes; it does not supply implementation. Start both workers before waiting for either. '
              'Do not write the tracked module directly or bypass the gate. After publish, each worker verifies its own actual module and reports PASS/ISSUES/BLOCKED, '
              'exact branch/base SHA, changed paths, commands and observed outputs. '
              'The verifier must use the bounded shared-state exception: read-only access to ' + str(primary) + ', invoke python3 -B local_probe.py '
              'with that primary cwd exactly once, and report its primary HEAD, method/sample count one, challenge/requestId and outcome without printing/copying token. '
              'The isolated worktree negative control is recorded at ' + str(root / 'isolated-probe.json') + '. Do not copy the local-state directory or credentials into a worktree. '
              'Only loopback HTTP is allowed; network was enabled in this disposable host config for this probe. '
              'Resolve all three swarm-worker choices before spawning, with observed parent ' + args.model + '/' + args.effort + ' and --catalog ' + str(args.catalog.resolve(strict=True)) + '. '
              'Task pairs are a=gpt-6.1-sol/low, b=gpt-6-luna/medium, verifier=gpt-6-luna/medium. Pass explicit resolved model and reasoning_effort in native spawn. '
              'After all writers finish, primary reads both diffs and integrates ONLY alpha.py from a and beta.py from b into ' + str(integration) + ', '
              'using that base checkout, then tests the combined result and confirms main-only changes are absent. The primary must independently rerun local_probe.py from the primary cwd after '
              'the verifier returns. Keep the checklist in conversation and write one consolidated report under ' + str(reports) + '. '
              'Delegate reports lacking exact SHAs or requested methods are gaps, never passes. File ownership is not a separate OS sandbox guarantee.')
    (root / 'prompt.txt').write_text(prompt)
    client = None; thread = None; status = 'error'; auth = home / 'auth.json'
    auth.symlink_to(args.auth_file.resolve(strict=True))
    try:
        client = research.Client(args.codex, primary, home, root)
        thread, status = client.run(primary, args.model, args.effort, prompt, sandbox='workspace-write')
    except (RuntimeError, queue.Empty, TimeoutError, KeyboardInterrupt) as error:
        (root / 'harness-error.txt').write_text(str(error))
    finally:
        if client: client.close()
        auth.unlink(missing_ok=True); stop.set(); server.shutdown(); server.server_close()
        save(root / 'server-audit.json', requests)
        (local / 'token').unlink(missing_ok=True)
    # Token removal is harness cleanup, so compare against the captured pre-cleanup identity.
    after = {n: snapshot(p) for n, p in scopes.items()}
    before['primary'].pop('.local-state/token', None)
    save(root / 'after.json', after)
    changed = {n: sorted(k for k in set(before[n]) | set(after[n]) if before[n].get(k) != after[n].get(k)) for n in scopes}
    expected = {'primary': set(), 'integration': {'alpha.py', 'beta.py'}}
    for n, s in contract['writers'].items():
        expected[n] = {s['module'], 'proposal.py', 'worker-proof.txt', '.writer-entered.json', '.writer-written.json', '.writer-finished.json'}
    unexpected = {n: sorted(set(paths) - expected[n]) for n, paths in changed.items()}
    checks = {}
    checks['headsAndIndexesUnchanged'] = all(git(p, 'rev-parse', 'HEAD') == heads[n] and git(p, 'diff', '--cached', '--binary') == indexes[n] for n, p in scopes.items())
    checks['basePreserved'] = all(git(scopes[n], 'rev-parse', 'HEAD') == contract['baseSha'] and not (scopes[n] / 'main-only.txt').exists() and (scopes[n] / 'feature-only.txt').exists() for n in ('a', 'b', 'integration'))
    writer_checks, receipts = writer_evidence(root, contract)
    checks.update(writer_checks)
    checks['localStateProof'] = isolated.returncode != 0 and len(requests) >= 2 and all(r['authenticated'] for r in requests) and len({r['clientPid'] for r in requests}) >= 2
    verify = None
    if status == 'completed':
        code = 'from alpha import add\nfrom beta import multiply\nfrom origin_kind import KIND\nassert KIND == "feature"\nassert add(3,4)==7\nassert add(a=-2,b=2)==0\nassert multiply(3,4)==12\nassert multiply(a=-3,b=0)==0\nassert multiply(-3,2)==-6\nprint("swarm integration acceptance passed")\n'
        p = subprocess.run(['python3', '-B', '-c', code], cwd=integration, capture_output=True, text=True)
        verify = {'exitCode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
        save(root / 'verification.json', verify)
    summary, final = research.summarize_events(client.events if client else [], thread)
    (root / 'final.txt').write_text(final)
    result = {'status': status, 'changed': changed, 'unexpectedChanges': unexpected, 'checks': checks,
              'writerReceipts': receipts, 'localProbeRequestCount': len(requests), **summary,
              'artifactChecksPassed': status == 'completed' and not any(unexpected.values()) and all(checks.values()) and verify is not None and verify['exitCode'] == 0}
    save(root / 'result.json', result); print(json.dumps(result), flush=True)
    print('Scope: disposable native backend; manually audit scope, actual starts/commands/integration. Not desktop/browser parity or independent OS sandbox enforcement.')
    return 0 if result['artifactChecksPassed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
