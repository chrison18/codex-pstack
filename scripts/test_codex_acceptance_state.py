from pathlib import Path
import tempfile
import unittest

from codex_acceptance_state import snapshot


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def test_link_creation_deletion_and_retargeting_are_changes(self):
        before = snapshot(self.root)
        link = self.root / 'link'
        link.symlink_to('missing-one')
        created = snapshot(self.root)
        self.assertNotEqual(created, before)
        link.unlink()
        self.assertEqual(snapshot(self.root), before)
        link.symlink_to('missing-two')
        self.assertNotEqual(snapshot(self.root), created)
        link.unlink()
        self.assertNotEqual(snapshot(self.root), created)

    def test_regular_file_replaced_with_identical_content_link_is_a_change(self):
        target = self.root / 'target'
        target.write_text('same content')
        file = self.root / 'file'
        file.write_text('same content')
        before = snapshot(self.root)
        file.unlink()
        file.symlink_to('target')
        self.assertNotEqual(snapshot(self.root), before)

    def test_empty_directories_and_permissions_are_observable(self):
        file = self.root / 'app.py'
        file.write_text('print(1)')
        file.chmod(0o644)
        before = snapshot(self.root)
        file.chmod(0o755)
        self.assertNotEqual(snapshot(self.root), before)
        file.chmod(0o644)
        directory = self.root / 'empty'
        directory.mkdir()
        self.assertNotEqual(snapshot(self.root), before)
        directory.rmdir()
        self.assertEqual(snapshot(self.root), before)

    def test_does_not_follow_directory_links(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside)
            link = self.root / 'outside'
            link.symlink_to(target, target_is_directory=True)
            before = snapshot(self.root)
            (target / 'secret').write_text('not part of the fixture')
            self.assertEqual(snapshot(self.root), before)
            self.assertEqual(before['outside']['kind'], 'symlink')

    def test_root_git_metadata_is_excluded_but_file_content_is_checked(self):
        metadata = self.root / '.git'
        metadata.mkdir()
        file = self.root / 'app.py'
        file.write_text('before')
        before = snapshot(self.root)
        (metadata / 'config').write_text('Git state is checked separately')
        self.assertEqual(snapshot(self.root), before)
        file.write_text('after')
        self.assertNotEqual(snapshot(self.root), before)


if __name__ == '__main__':
    unittest.main()
