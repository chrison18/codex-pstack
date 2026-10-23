"""Project-scoped pstack role setup and native Codex model resolution."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time

ROLES = ('feature', 'bug-fix', 'investigation', 'comment-sicko',
         'how-explorer', 'how-explainer', 'why-investigator', 'why-synthesizer',
         'interrogate-reviewer')
AGENTS = ('poteto-agent', 'comment-sicko')
RESOURCE = Path(__file__).resolve().parent.parent / 'resources/agents'


def project_root(value):
    root = Path(value).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Project must be an existing directory')
    return root


def local_path(root, relative):
    path = root / relative
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Refusing symlink at ' + str(current))
    return path


def digest(value):
    return hashlib.sha256(value).hexdigest()


def write_json(path, value, exclusive=False):
    content = json.dumps(value, indent=2) + '\n'
    if exclusive:
        with path.open('x') as handle:
            handle.write(content)
        return
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def expected_roles():
    return {'agents/' + name + '.toml': (RESOURCE / (name + '.toml')).read_bytes()
            for name in AGENTS}


def verify_install(root):
    receipt = local_path(root, '.codex/pstack-agents.json')
    data = json.loads(receipt.read_text())
    expected = expected_roles()
    hashes = {name: digest(content) for name, content in expected.items()}
    if data != {'schema': 1, 'files': hashes}:
        raise ValueError('Ownership receipt does not match this package; inspect before updating')
    for name, content in expected.items():
        target = local_path(root, '.codex/' + name)
        if not target.is_file() or target.read_bytes() != content:
            raise ValueError('Owned role was edited or removed: ' + str(target))
    return receipt, expected


def install(root):
    receipt = local_path(root, '.codex/pstack-agents.json')
    if receipt.exists():
        verify_install(root)
        return {'status': 'already-installed'}
    expected = expected_roles()
    for name in expected:
        target = local_path(root, '.codex/' + name)
        if target.exists():
            raise ValueError('Existing role is not owned by pstack: ' + str(target))
    created = []
    try:
        for name, content in expected.items():
            target = local_path(root, '.codex/' + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as handle:
                created.append(target)
                handle.write(content)
        write_json(receipt, {'schema': 1, 'files': {n: digest(c) for n, c in expected.items()}}, exclusive=True)
    except Exception:
        for target in created:
            target.unlink()
        raise
    return {'status': 'installed', 'next': 'Trust project configuration in Codex if needed; start a new session.'}


def uninstall(root):
    receipt, expected = verify_install(root)
    for name in expected:
        local_path(root, '.codex/' + name).unlink()
    receipt.unlink()
    return {'status': 'removed', 'modelPreferences': 'retained'}


def model_catalog(executable='codex'):
    process = subprocess.Popen([executable, 'app-server', '--listen', 'stdio://'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True)
    messages = queue.Queue()

    def read():
        for line in process.stdout:
            messages.put(line)
        messages.put(None)

    threading.Thread(target=read, daemon=True).start()

    def rpc(identifier, method, params):
        process.stdin.write(json.dumps({'id': identifier, 'method': method, 'params': params}) + '\n')
        process.stdin.flush()
        while True:
            line = messages.get(timeout=30)
            if line is None:
                raise ValueError('Codex app-server closed before model discovery completed')
            value = json.loads(line)
            if value.get('id') == identifier:
                if 'error' in value:
                    raise ValueError('Codex model discovery failed: ' + json.dumps(value['error']))
                return value['result']

    try:
        rpc(1, 'initialize', {'clientInfo': {'name': 'pstack-models', 'version': '0.2.0'},
                              'capabilities': {'experimentalApi': True}})
        process.stdin.write('{"method":"initialized"}\n')
        process.stdin.flush()
        result, cursor, identifier = [], None, 2
        while True:
            page = rpc(identifier, 'model/list', {'limit': 100, 'cursor': cursor})
            result.extend(page['data'])
            cursor = page.get('nextCursor')
            if not cursor:
                return result
            identifier += 1
            if identifier > 100:
                raise ValueError('Model catalog pagination did not terminate')
    except queue.Empty as error:
        raise ValueError('Codex model discovery timed out; no model selection was changed') from error
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        process.stdin.close()
        process.stdout.close()


def selection(model, effort, catalog):
    if model == 'inherit':
        if effort is not None:
            raise ValueError('inherit preserves both parent model and effort; omit --effort')
        return {'model': 'inherit'}
    entry = next((entry for entry in catalog if entry['model'] == model), None)
    if entry is None:
        raise ValueError('Unavailable model: ' + model)
    chosen = effort if effort is not None else entry['defaultReasoningEffort']
    if chosen not in [option['reasoningEffort'] for option in entry['supportedReasoningEfforts']]:
        raise ValueError('Unsupported effort ' + str(chosen) + ' for ' + model)
    return {'model': model, 'effort': chosen}


def read_catalog(path):
    if path is None:
        return model_catalog()
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or data.get('source') != 'codex/model/list' or not isinstance(data.get('capturedAt'), (int, float)):
        raise ValueError('Expected a native catalog snapshot produced by the models command')
    age = time.time() - data['capturedAt']
    if not 0 <= age <= 3600:
        raise ValueError('Catalog snapshot expired; refresh with the models command')
    if not isinstance(data.get('models'), list) or not data['models']:
        raise ValueError('Catalog snapshot contains no models')
    return data['models']


def load_choices(root):
    path = local_path(root, '.codex/pstack-models.json')
    if not path.exists():
        return {'schema': 1, 'roles': {}}
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or set(data) != {'schema', 'roles'} or data['schema'] != 1 or not isinstance(data['roles'], dict):
        raise ValueError('Unrecognized pstack model configuration; refusing to replace it')
    for role, value in data['roles'].items():
        if role not in ROLES or not isinstance(value, dict) or set(value) - {'model', 'effort'} or not isinstance(value.get('model'), str):
            raise ValueError('Invalid role selection: ' + role)
    return data


def configure(root, role, model, effort, catalog):
    chosen = selection(model, effort, catalog)
    data = load_choices(root)
    data['roles'][role] = chosen
    path = local_path(root, '.codex/pstack-models.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, data)
    return data


def resolve_choice(root, role, parent_model, parent_effort, model, effort, catalog):
    verify_install(root)
    if effort is not None and model is None:
        raise ValueError('Task effort requires an explicit --model')
    choices = load_choices(root)['roles']
    source = 'task' if model is not None else 'role' if role in choices else 'parent'
    requested = {'model': model, 'effort': effort} if model is not None else choices.get(role, {'model': 'inherit'})
    chosen = selection(requested['model'], requested.get('effort'), catalog)
    if chosen['model'] == 'inherit':
        chosen = selection(parent_model, parent_effort, catalog)
    return {'source': source, 'model': chosen['model'], 'reasoning_effort': chosen['effort']}


def resolve_panel(root, role, parent_model, parent_effort, selections, catalog):
    if selections is None:
        selections = [{}, {}]
    if not isinstance(selections, list) or len(selections) < 2:
        raise ValueError('A review panel requires at least two selections')
    for item in selections:
        if not isinstance(item, dict) or set(item) - {'model', 'effort'}:
            raise ValueError('Each panel selection accepts only model and effort')
        if 'model' in item and not isinstance(item['model'], str):
            raise ValueError('Panel model must be a string')
        if 'effort' in item and not isinstance(item['effort'], str):
            raise ValueError('Panel effort must be a string')
    reviewers = [resolve_choice(root, role, parent_model, parent_effort,
                               item.get('model'), item.get('effort'), catalog) for item in selections]
    distinct = len({item['model'] for item in reviewers})
    return {'reviewers': reviewers, 'distinctModels': distinct, 'modelDiversity': distinct > 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    models = commands.add_parser('models')
    models.add_argument('--output', type=Path)
    for action in ('install', 'uninstall', 'verify', 'configure', 'resolve'):
        command = commands.add_parser(action)
        command.add_argument('project', type=project_root)
        if action in ('configure', 'resolve'):
            command.add_argument('role', choices=ROLES)
            if action == 'configure':
                command.add_argument('model')
            else:
                command.add_argument('--model')
                command.add_argument('--parent-model', required=True)
                command.add_argument('--parent-effort', required=True)
            command.add_argument('--effort')
            command.add_argument('--catalog', type=Path)
    panel = commands.add_parser('resolve-panel')
    panel.add_argument('project', type=project_root)
    panel.add_argument('role', choices=('interrogate-reviewer',))
    panel.add_argument('--parent-model', required=True)
    panel.add_argument('--parent-effort', required=True)
    panel.add_argument('--selections', type=json.loads, help='JSON array of ephemeral model/effort selections')
    panel.add_argument('--catalog', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'models':
            result = model_catalog()
            if args.output is not None:
                write_json(args.output, {'source': 'codex/model/list', 'capturedAt': time.time(), 'models': result})
        elif args.command == 'install':
            result = install(args.project)
        elif args.command == 'uninstall':
            result = uninstall(args.project)
        elif args.command == 'verify':
            verify_install(args.project)
            result = {'status': 'verified'}
        elif args.command == 'resolve-panel':
            result = resolve_panel(args.project, args.role, args.parent_model, args.parent_effort,
                                   args.selections, read_catalog(args.catalog))
        elif args.command == 'configure':
            result = configure(args.project, args.role, args.model, args.effort, read_catalog(args.catalog))
        else:
            result = resolve_choice(args.project, args.role, args.parent_model, args.parent_effort,
                                    args.model, args.effort, read_catalog(args.catalog))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, 'pstack: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
