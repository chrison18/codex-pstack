"""Model-free safety checks for the new task-owned Arena cleanup boundary."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('arena', Path(__file__).with_name('accept-codex-arena-worktrees.py'))
arena = importlib.util.module_from_spec(spec); spec.loader.exec_module(arena)


def events():
    result = []
    for n in ('a', 'b', 'judge'):
        result += [
            {'method': 'rawResponseItem/completed', 'params': {'item': {'type': 'function_call', 'name': 'spawn_agent', 'call_id': n}}},
            {'method': 'item/completed', 'params': {'item': {'type': 'subAgentActivity', 'kind': 'started', 'agentThreadId': n}}},
            {'method': 'turn/completed', 'params': {'threadId': n, 'turn': {'status': 'completed'}}}]
    return result


class CleanupTests(unittest.TestCase):
    def test_unknown_or_timeout_never_calls_git_remove(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            variants = [('error', events()), ('completed', events()[:-1]), ('completed', events() + [{'method': 'turn/started', 'params': {'threadId': 'a'}}])]
            for status, capture in variants:
                with patch.object(arena, 'git') as mocked:
                    result = arena.cleanup(root, {}, {'primary': root}, arena.settled_evidence(capture, status))
                    self.assertTrue(result)
                    mocked.assert_not_called()

    def test_settled_archives_only_owned_worktrees_and_preserves_wrong_head(self):
        with tempfile.TemporaryDirectory(prefix='pstack-arena-cleanup-test-') as d:
            root = Path(d).resolve()
            entry = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode'
            contract = arena.swarm.prepare(root, entry)
            scopes = {'primary': Path(contract['primary']), 'a': Path(contract['writers']['a']['path']),
                      'b': Path(contract['writers']['b']['path']), 'integration': Path(contract['integration'])}
            ids = arena.identities(scopes)
            self.assertEqual(len({x['gitDir'] for x in ids.values()}), 4)
            self.assertEqual(len({x['indexPath'] for x in ids.values()}), 4)
            self.assertNotEqual(contract['primarySha'], contract['baseSha'])
            for n in ('a', 'b', 'integration'):
                self.assertEqual(ids[n]['head'], contract['baseSha'])
                self.assertFalse((scopes[n] / 'main-only.txt').exists())
            # An unexpected commit must be preserved, even with known terminal activity.
            arena.git(scopes['a'], '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm', 'Unexpected task state')
            errors = arena.cleanup(root, contract, scopes, arena.settled_evidence(events(), 'completed'))
            self.assertEqual(len(errors), 1)
            self.assertTrue(scopes['a'].exists())
            self.assertTrue(scopes['primary'].exists())
            for n in ('b', 'integration'):
                self.assertFalse(scopes[n].exists())
                self.assertTrue((root / 'archived-worktrees' / n / 'alpha.py').exists())
            self.assertEqual(len(arena.git(scopes['primary'], 'worktree', 'list').splitlines()), 2)


if __name__ == '__main__':
    unittest.main()
