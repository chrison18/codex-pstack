"""Explicit task checkpoints and conservative read-only Git audit (POSIX hosts)."""
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tempfile

FIELDS = ('goal', 'requirements', 'authority', 'scope', 'owner', 'evidence', 'blockers', 'next_action')


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_context(value):
    if not isinstance(value, dict) or set(value) != set(FIELDS):
        raise ValueError('Context requires exactly: ' + ', '.join(FIELDS))
    for key in FIELDS:
        if key in ('requirements', 'scope', 'evidence', 'blockers'):
            if not isinstance(value[key], list) or not all(text(v) for v in value[key]):
                raise ValueError('Invalid context list: ' + key)
        elif not text(value[key]):
            raise ValueError('Empty context: ' + key)
    if not value['requirements'] or not value['scope']:
        raise ValueError('Requirements and scope cannot be empty')


def safe_path(value):
    path = Path(os.path.abspath(value))
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ValueError('Symlink paths are not supported')
    return path


def read_state(directory, workspace):
    path = safe_path(directory) / 'state.json'
    safe_path(path)
    state = json.loads(path.read_text())
    if not isinstance(state, dict) or state.get('schema') != 1 or state.get('workspace') != str(Path(workspace).resolve(strict=True)):
        raise ValueError('Wrong schema or workspace identity')
    validate_context(state['context'])
    if type(state.get('revision')) is not int or state['revision'] < 0:
        raise ValueError('Invalid revision')
    if not isinstance(state.get('history'), list) or not isinstance(state.get('operations'), dict):
        raise ValueError('Invalid task record')
    for name, op in state['operations'].items():
        if not text(name) or not isinstance(op, dict) or op.get('status') not in ('pending', 'started', 'completed') or not text(op.get('description')):
            raise ValueError('Invalid operation')
        if not isinstance(op.get('evidence'), list) or not all(text(v) for v in op['evidence']):
            raise ValueError('Invalid operation evidence')
        if op['status'] == 'completed' and not op['evidence']:
            raise ValueError('Completed operation needs evidence')
    return state


@contextlib.contextmanager
def locked(directory):
    directory = safe_path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    lock = safe_path(directory / '.lock')
    with lock.open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield directory


def save(directory, state):
    target = safe_path(directory / 'state.json')
    with tempfile.NamedTemporaryFile(mode='w', dir=directory, delete=False) as handle:
        tmp = Path(handle.name)
        json.dump(state, handle, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(tmp, target)
        fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        tmp.unlink(missing_ok=True)


def initialize(directory, workspace, context, operations):
    validate_context(context)
    if not isinstance(operations, dict) or not operations or not all(text(k) and text(v) for k, v in operations.items()):
        raise ValueError('Operations must map stable IDs to descriptions')
    workspace = str(Path(workspace).resolve(strict=True))
    with locked(directory) as directory:
        if (directory / 'state.json').exists():
            raise ValueError('Task already exists')
        state = dict(schema=1, workspace=workspace, revision=0, context=context,
                     operations={k: dict(description=v, status='pending', evidence=[]) for k, v in operations.items()},
                     history=[dict(revision=0, action='init', context=context)])
        save(directory, state)
    return state


def mutate(directory, workspace, revision, owner, action, operation=None, evidence=None, context=None, reason=None):
    with locked(directory) as directory:
        state = read_state(directory, workspace)
        if 'continuation' in state:
            raise ValueError('Continuation owns mutations; use continuation.py, never bypass terminal state')
        if state['revision'] != revision or state['context']['owner'] != owner:
            raise ValueError('Stale revision or wrong owner; recover before writing')
        if action == 'checkpoint':
            validate_context(context)
            if context['owner'] != owner or not text(reason):
                raise ValueError('Keep owner; context changes require a reason')
            state['context'] = context
        else:
            op = state['operations'][operation]
            if action == 'begin':
                if op['status'] != 'pending':
                    raise ValueError('Refusing duplicate/uncertain operation; reconcile evidence')
                op['status'] = 'started'
            elif action == 'complete':
                if op['status'] != 'started' or not evidence or not all(text(v) for v in evidence):
                    raise ValueError('Completion requires started intent and concrete evidence')
                op.update(status='completed', evidence=evidence)
            else:
                raise ValueError('Unknown mutation')
        state['revision'] += 1
        state['history'].append(dict(revision=state['revision'], action=action, operation=operation,
                                     evidence=evidence, reason=reason, context=state['context']))
        save(directory, state)
        return state


def recover(directory, workspace):
    state = read_state(directory, workspace)
    return dict(state=state, completed=[k for k,v in state['operations'].items() if v['status']=='completed'],
                pending=[k for k,v in state['operations'].items() if v['status']=='pending'],
                uncertain=[k for k,v in state['operations'].items() if v['status']=='started'])


def audit(workspace, base, observations):
    """Observations are operator evidence, not independently discovered host truth."""
    workspace = str(Path(workspace).resolve(strict=True))
    def git(*args):
        return subprocess.run(['git', '--no-optional-locks', '-C', workspace, *args],
                              capture_output=True, text=True, timeout=15)
    reasons = []
    status = git('status', '--porcelain=v1', '--untracked-files=all')
    head = git('rev-parse', 'HEAD')
    merged = git('merge-base', '--is-ancestor', 'HEAD', base)
    if status.returncode or head.returncode or merged.returncode not in (0,1):
        reasons.append('git-state-unknown')
    if status.stdout: reasons.append('dirty')
    if merged.returncode != 0: reasons.append('not-proven-merged')
    if observations.get('workspace') != workspace or observations.get('head') != head.stdout.strip():
        reasons.append('observation-identity-mismatch')
    for key, clear in (('session', 'settled'), ('pr', 'none')):
        item = observations.get(key, {})
        if not isinstance(item, dict) or item.get('status') != clear or not text(item.get('evidence')):
            reasons.append(key + '-active-open-or-unknown')
    return dict(workspace=workspace, head=head.stdout.strip(), base=base, reasons=reasons,
                verdict='hold' if reasons else 'review-only', safe_to_delete=False,
                limitation='Session/PR observations are supplied; recheck liveness and PR state before any cleanup')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init','recover','history','begin','complete','checkpoint','audit'])
    parser.add_argument('workspace')
    parser.add_argument('--task-dir')
    parser.add_argument('--input', help='JSON context/operations, updated context, or audit observations')
    parser.add_argument('--revision', type=int)
    parser.add_argument('--owner')
    parser.add_argument('--operation')
    parser.add_argument('--evidence', action='append')
    parser.add_argument('--reason')
    parser.add_argument('--base')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text()) if args.input else None
        if args.action == 'audit':
            if not args.base: raise ValueError('Audit requires an explicit base')
            result = audit(args.workspace, args.base, data or {})
        else:
            if not args.task_dir: raise ValueError('Explicit task directory required')
            if args.action == 'init':
                result = initialize(args.task_dir, args.workspace, data['context'], data['operations'])
            elif args.action in ('recover','history'):
                result = recover(args.task_dir, args.workspace)
                if args.action == 'history': result = result['state']['history']
            else:
                result = mutate(args.task_dir, args.workspace, args.revision, args.owner, args.action,
                                args.operation, args.evidence, data, args.reason)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
