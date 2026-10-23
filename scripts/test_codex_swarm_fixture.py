"""Check the acceptance instrument, independently of model-generated solutions."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest

SCRIPT = Path(__file__).with_name('accept-codex-swarm.py').resolve()
spec = importlib.util.spec_from_file_location('swarm_acceptance', SCRIPT)
swarm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(swarm)


class SwarmFixtureTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()
        entry = SCRIPT.parent.parent / 'plugins/pstack/skills/poteto-mode'
        self.contract = swarm.prepare(self.root, entry)
        for name, scope in self.contract['writers'].items():
            (Path(scope['path']) / 'proposal.py').write_text('def answer():\n    return ' + repr(name) + '\n')

    def command(self, name):
        return [sys.executable, '-B', str(SCRIPT), 'publish', '--fixture-root', str(self.root), '--worker', name]

    def start(self, name):
        process = subprocess.Popen(self.command(name), cwd=self.contract['writers'][name]['path'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def close():
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
            process.stdout.close(); process.stderr.close()
        self.addCleanup(close)
        return process

    def test_rejects_wrong_base_before_any_publish(self):
        self.contract['baseSha'] = '0' * 40
        swarm.save(self.root / 'contract.json', self.contract)
        scope = self.contract['writers']['a']
        target = Path(scope['path']) / scope['module']
        before = target.read_bytes()
        process = subprocess.run(self.command('a'), cwd=scope['path'], capture_output=True, text=True)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('Wrong base SHA', process.stderr)
        self.assertEqual(target.read_bytes(), before)
        self.assertFalse((target.parent / '.writer-entered.json').exists())

    def test_barrier_has_live_independent_writers_and_shared_epoch_order(self):
        started = time.time_ns()
        first = self.start('a')
        entered = Path(self.contract['writers']['a']['path']) / '.writer-entered.json'
        deadline = time.monotonic() + 10
        while not entered.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(entered.exists())
        self.assertFalse((self.root / 'release.json').exists())
        self.assertIn('NotImplementedError', (entered.parent / 'alpha.py').read_text())
        second = self.start('b')
        stop = threading.Event()
        observer = threading.Thread(target=swarm.release_when_ready, args=(self.root, self.contract, stop), daemon=True)
        observer.start()
        self.addCleanup(stop.set)
        for process in (first, second):
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertEqual(json.loads(stdout)['status'], 'published')
        observer.join(timeout=2)
        for scope in self.contract['writers'].values():
            path = Path(scope['path'])
            shutil.copyfile(path / scope['module'], Path(self.contract['integration']) / scope['module'])
            with (path / 'worker-proof.txt').open('a') as handle:
                handle.write('PASS: richer evidence report is allowed\n')
        checks, receipts = swarm.writer_evidence(self.root, self.contract)
        self.assertTrue(all(checks.values()), checks)
        self.assertTrue(all(started <= r['enteredAtNs'] <= r['finishedAtNs'] <= time.time_ns() for r in receipts))
        release = json.loads((self.root / 'release.json').read_text())
        self.assertEqual(set(release['pids']), {first.pid, second.pid})
        # Fabricated non-overlap must fail even when code and worktree identities are valid.
        path = entered.parent / '.writer-entered.json'
        bad = json.loads(path.read_text())
        bad['enteredAtNs'] = max(r['finishedAtNs'] for r in receipts) + 1
        swarm.save(path, bad)
        checks, _ = swarm.writer_evidence(self.root, self.contract)
        self.assertFalse(checks['overlappingWriterIntervals'])
        self.assertFalse(checks['barrierOrderAndLivePids'])


if __name__ == '__main__':
    unittest.main()
