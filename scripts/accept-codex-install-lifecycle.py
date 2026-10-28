"""Model-free host lifecycle acceptance in one retained, exclusively owned fixture."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from codex_acceptance_state import snapshot

REPO = Path(__file__).resolve().parent.parent
ENTRY = REPO / 'plugins/pstack/skills/poteto-mode'


def main():
    capture = Path(tempfile.mkdtemp(prefix='pstack-install-lifecycle-'))
    project = capture / 'workspace'
    project.mkdir()
    (project / '.codex').mkdir()
    (project / '.codex/config.toml').write_text('# unrelated sentinel\nmodel_reasoning_effort = "medium"\n')
    (project / '.codex/pstack-models.json').write_text(
        '{"schema":1,"roles":{"feature":{"model":"gpt-6-luna","effort":"medium"}}}\n')
    (project / 'README.md').write_text('Owned host lifecycle fixture. No model task.\n')
    audit = {'checkout': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
             'project': str(project), 'events': [], 'before': snapshot(project),
             'resourceHashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted((ENTRY / 'resources/agents').glob('*.toml'))}}
    print(str(capture), flush=True)

    def run(script, *args):
        command = [sys.executable, str(script), *map(str, args)]
        result = subprocess.run(command, capture_output=True, text=True)
        audit['events'].append({'command': command, 'returncode': result.returncode,
                                'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            raise RuntimeError('Host command failed; retained fixture, no retry or bypass')
        return result.stdout

    try:
        run(REPO / 'scripts/link-codex-entry.py', project)
        runtime = ENTRY / 'scripts/runtime.py'
        assert json.loads(run(runtime, 'install', project))['status'] == 'installed'
        run(runtime, 'verify', project)
        audit['installed'] = snapshot(project)
        assert json.loads(run(runtime, 'install', project))['status'] == 'already-installed'
        assert snapshot(project) == audit['installed']
        for key, value in audit['before'].items():
            assert snapshot(project)[key] == value, key
        run(runtime, 'uninstall', project)
        alias = project / '.agents/skills/poteto-mode'
        assert alias.is_symlink() and alias.resolve(strict=True) == ENTRY.resolve(strict=True)
        alias.unlink()
        # Remove only task-created empty directories, never recursive deletion.
        for relative in ('.codex/agents', '.agents/skills', '.agents'):
            (project / relative).rmdir()
        audit['after'] = snapshot(project)
        assert audit['after'] == audit['before']
        audit['verdict'] = 'PASS: host install/idempotence/verify/remove; not Chat registration or upgrade'
    except Exception as error:
        audit['verdict'] = 'FAIL/BLOCKED: ' + str(error)
        raise
    finally:
        (capture / 'result.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(audit['verdict'])


if __name__ == '__main__':
    main()
