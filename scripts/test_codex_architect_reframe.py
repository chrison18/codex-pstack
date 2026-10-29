"""Temporary-auth cleanup must survive a client shutdown failure."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

spec = importlib.util.spec_from_file_location('reframe', Path(__file__).with_name('accept-codex-architect-reframe.py'))
reframe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reframe)


class CleanupTest(unittest.TestCase):
    def test_close_failure_still_unlinks_and_records_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'dummy.txt'; target.write_text('not credentials')
            auth = root / 'auth.json'; auth.symlink_to(target)
            client = Mock(); client.close.side_effect = RuntimeError('simulated shutdown failure')
            result = {'round1': 'completed', 'round2': 'completed'}
            reframe.finalize_capture(client, auth, root, result)
            self.assertFalse(auth.is_symlink())
            self.assertEqual(target.read_text(), 'not credentials')
            self.assertEqual(result['cleanupErrors'][0]['operation'], 'client.close')
            self.assertEqual(json.loads((root / 'result.json').read_text()), result)

    def test_unlink_failure_is_recorded_not_hidden(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            auth = Mock(); auth.unlink.side_effect = PermissionError('simulated unlink denial')
            result = {}
            reframe.finalize_capture(None, auth, root, result)
            self.assertEqual(result['cleanupErrors'][0]['operation'], 'auth.unlink')
            self.assertEqual(json.loads((root / 'result.json').read_text()), result)


if __name__ == '__main__':
    unittest.main()
