"""Capture real Codex research delegation in disposable read-only Git projects."""

import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time

from codex_acceptance_state import snapshot


class Client:
    def __init__(self, executable, workspace, home, log_root):
        self.events = []
        self.pending = queue.Queue()
        self.identifier = 0
        self.errors = (log_root / 'server-stderr.log').open('w')
        self.log = (log_root / 'events.jsonl').open('w')
        self.process = subprocess.Popen(
            [executable, '--no-daemon', 'app-server', '--listen', 'stdio://'], cwd=workspace,
            env={**os.environ, 'CODEX_HOME': str(home), 'PYTHONDONTWRITEBYTECODE': '1'},
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.errors, text=True)
        def read():
            for line in self.process.stdout:
                self.pending.put(json.loads(line))
            self.pending.put(None)
        threading.Thread(target=read, daemon=True).start()

    def send(self, value):
        self.process.stdin.write(json.dumps(value) + '\n')
        self.process.stdin.flush()

    def receive(self, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Codex acceptance deadline exceeded')
        value = self.pending.get(timeout=remaining)
        if value is None:
            raise RuntimeError('Codex app-server closed')
        self.events.append(value)
        self.log.write(json.dumps(value) + '\n')
        self.log.flush()
        if 'id' in value and 'method' in value:
            self.send({'id': value['id'], 'error': {'code': -32000, 'message': 'Acceptance harness cannot approve extra actions'}})
        return value

    def rpc(self, method, params):
        self.identifier += 1
        identifier = self.identifier
        self.send({'id': identifier, 'method': method, 'params': params})
        deadline = time.monotonic() + 60
        while True:
            value = self.receive(deadline)
            if value.get('id') == identifier and 'method' not in value:
                if 'error' in value:
                    raise RuntimeError(json.dumps(value['error']))
                return value['result']

    def run(self, workspace, model, effort, prompt):
        self.rpc('initialize', {'clientInfo': {'name': 'pstack-research-acceptance', 'version': '0.3.0'},
                                'capabilities': {'experimentalApi': True}})
        self.send({'method': 'initialized'})
        started = self.rpc('thread/start', {'cwd': str(workspace), 'model': model,
            'approvalPolicy': 'never', 'sandbox': 'read-only', 'ephemeral': True,
            'config': {'model_reasoning_effort': effort}, 'experimentalRawEvents': True})
        thread = started['thread']['id']
        self.rpc('turn/start', {'threadId': thread, 'effort': effort,
                               'input': [{'type': 'text', 'text': prompt}]})
        deadline = time.monotonic() + 900
        while True:
            value = self.receive(deadline)
            params = value.get('params', {})
            if value.get('method') == 'turn/completed' and params.get('threadId') == thread:
                return thread, params['turn']['status']

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)
        self.process.stdin.close()
        self.process.stdout.close()
        self.errors.close()
        self.log.close()



def summarize_events(events, thread):
    activities = {}
    requests = []
    finals = []
    for event in events:
        params = event.get('params', {})
        item = params.get('item', {})
        if item.get('type') == 'subAgentActivity' and item.get('model'):
            activities[item['agentThreadId']] = {'model': item['model'], 'effort': item.get('reasoningEffort')}
        if (event.get('method') == 'rawResponseItem/completed' and item.get('type') == 'function_call'
                and item.get('name', '').split('.')[-1] == 'spawn_agent'):
            arguments = json.loads(item['arguments'])
            requests.append({key: arguments.get(key) for key in ('task_name', 'agent_type', 'model', 'reasoning_effort')})
        if (event.get('method') == 'item/completed' and params.get('threadId') == thread
                and item.get('type') == 'agentMessage' and item.get('phase') == 'final_answer'):
            finals.append(item['text'])
    return {'spawnRequests': requests, 'resolvedAgentStarts': activities}, '\n\n'.join(finals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home() / '.codex/auth.json')
    parser.add_argument('--case', action='append', choices=('how-simple', 'how-complex', 'why', 'fallback', 'review'))
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    entry = repo / 'plugins/pstack/skills/poteto-mode'
    root = Path(tempfile.mkdtemp(prefix='pstack-research-live-')).resolve()
    catalog = args.catalog.resolve(strict=True)
    print(json.dumps({'evidenceDirectory': str(root)}), flush=True)
    tasks = {
        'how-simple': 'How does totals.total calculate its result? Explain edge cases with file/line citations.',
        'how-complex': 'Explain the architecture and complete runtime flow from api.handle through normalization and aggregation to the returned total. Trace the cross-module ownership and data transformations. Use the complex How route.',
        'why': 'Why is BATCH_SIZE 5 and TIMEOUT_SECONDS 11? I assume both were chosen for speed. Investigate the actual local history and distinguish known motivation from unknown reasons.',
        'review': 'Interrogate the latest commit against the shipping fee requirement: zero quantity has zero fee; positive quantity has fee 3. Review only; do not fix. Use two independent reviewers with task selections gpt-6.1-sol/low and gpt-6-luna/medium. State concrete counterexamples and distinguish findings from suggestions.',
        'fallback': 'How does totals.total calculate its result? Do not delegate or install/configure anything; use the documented primary-only read path.',
    }
    results = []
    for case, task in tasks.items():
        if args.case and case not in args.case:
            continue
        log_root = root / case
        log_root.mkdir()
        workspace, home = log_root / 'workspace', log_root / 'home'
        workspace.mkdir()
        home.mkdir()
        def git(*arguments):
            return subprocess.run(['git', '-C', str(workspace), *arguments], check=True,
                                  capture_output=True, text=True).stdout.strip()
        (workspace / 'totals.py').write_text('def total(items):\n    return sum(item["price"] * item["quantity"] for item in items)\n')
        (workspace / 'normalize.py').write_text('def normalize(rows):\n    return [{"price": int(row["price"]), "quantity": int(row["quantity"])} for row in rows]\n')
        (workspace / 'api.py').write_text('from normalize import normalize\nfrom totals import total\n\ndef handle(rows):\n    return {"total": total(normalize(rows))}\n')
        (workspace / 'limits.py').write_text('BATCH_SIZE = 3\nTIMEOUT_SECONDS = 11\n')
        if case == 'review':
            (workspace / 'shipping.py').write_text('def shipping_fee(quantity):\n    return 0 if quantity == 0 else 3\n')
        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Initialize example request pipeline')
        (workspace / 'limits.py').write_text('BATCH_SIZE = 5\nTIMEOUT_SECONDS = 11\n')
        if case == 'review':
            (workspace / 'shipping.py').write_text('def shipping_fee(quantity):\n    return 3\n')
            git('add', 'shipping.py')
        git('add', 'limits.py')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Limit batches to five because the partner endpoint rejects larger batches')
        link = workspace / '.agents/skills/poteto-mode'
        link.parent.mkdir(parents=True)
        link.symlink_to(entry)
        if case != 'fallback':
            subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'install', str(workspace)],
                           check=True, capture_output=True)
        if case == 'how-simple':
            subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'configure', str(workspace),
                            'how-explainer', 'gpt-6-luna', '--effort', 'medium', '--catalog', str(catalog)],
                           check=True, capture_output=True)
        if case == 'why':
            subprocess.run(['python3', '-B', str(entry / 'scripts/runtime.py'), 'configure', str(workspace),
                            'why-synthesizer', 'gpt-6-luna', '--effort', 'medium', '--catalog', str(catalog)],
                           check=True, capture_output=True)
        (home / 'config.toml').write_text('[projects.' + json.dumps(str(workspace)) + ']\ntrust_level="trusted"\n'
            '[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n')
        before = snapshot(workspace)
        head = git('rev-parse', 'HEAD')
        index = git('diff', '--cached', '--binary')
        auth = home / 'auth.json'
        auth.symlink_to(args.auth_file.resolve(strict=True))
        prompt = '$poteto-mode ' + task + '\nThis is a disposable read-only acceptance fixture. '
        prompt += ('Delegate using the prescribed native roles. ' if case != 'fallback' else '')
        prompt += ('Only local files and local Git history are in scope. Do not access external services, '
                   'create files, execute application code, change config, commit or open PRs. '
                   'Keep the checklist in conversation. The parent model/effort explicitly selected for this run is '
                   + args.model + '/' + args.effort + '. Resolve each research role using that observed pair and --catalog '
                   + str(catalog) + '. Do not run a nested app-server. Pass explicit resolved model and reasoning_effort '
                   'to the native spawn. Missing capability or rejected selection is not permission to claim delegation ran.')
        if case == 'review':
            prompt += ' Resolve the whole panel before spawning via resolve-panel with task selections [{"model":"gpt-6.1-sol","effort":"low"},{"model":"gpt-6-luna","effort":"medium"}].'
        if case == 'why':
            prompt += ' Task model override for why-synthesizer: --model ' + args.model + ' --effort high; do not save this override.'
        (log_root / 'prompt.txt').write_text(prompt)
        client = None
        thread = None
        status = 'error'
        try:
            client = Client(args.codex, workspace, home, log_root)
            thread, status = client.run(workspace, args.model, args.effort, prompt)
        except (RuntimeError, queue.Empty, TimeoutError) as error:
            (log_root / 'harness-error.txt').write_text(str(error))
        finally:
            if client:
                client.close()
            auth.unlink(missing_ok=True)
        after = snapshot(workspace)
        (log_root / 'before.json').write_text(json.dumps(before, sort_keys=True))
        (log_root / 'after.json').write_text(json.dumps(after, sort_keys=True))
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        events = client.events if client else []
        summary, final = summarize_events(events, thread)
        (log_root / 'final.txt').write_text(final)
        result = {'case': case, 'status': status, 'changed': changed, **summary,
                  'artifactChecksPassed': status == 'completed' and not changed
                  and git('rev-parse', 'HEAD') == head and git('diff', '--cached', '--binary') == index}
        results.append(result)
        (log_root / 'result.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result), flush=True)
    print('Scope: local native backend; inspect delegation, model events, citations and confidence manually. Not desktop UI or live connector evidence.')
    return 0 if all(result['artifactChecksPassed'] for result in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
