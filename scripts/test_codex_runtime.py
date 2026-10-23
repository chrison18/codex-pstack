import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parent.parent / 'plugins/pstack/skills/poteto-mode/scripts/runtime.py'
spec = importlib.util.spec_from_file_location('pstack_runtime', SCRIPT)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
CATALOG = [
    {'model': 'parent-model', 'defaultReasoningEffort': 'low', 'supportedReasoningEfforts': [{'reasoningEffort': v} for v in ('low', 'high')]},
    {'model': 'role-model', 'defaultReasoningEffort': 'medium', 'supportedReasoningEfforts': [{'reasoningEffort': v} for v in ('medium', 'high')]},
]


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def cli(self, action):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), action, str(self.root)], capture_output=True, text=True)

    def test_install_repeat_remove_preserves_other_configuration(self):
        config = self.root / '.codex/config.toml'
        config.parent.mkdir()
        config.write_text('model = "existing"\n')
        other = config.parent / 'agents/user.toml'
        other.parent.mkdir()
        other.write_text('user agent')
        self.assertEqual(self.cli('install').returncode, 0)
        self.assertEqual(self.cli('install').returncode, 0)
        self.assertEqual(self.cli('verify').returncode, 0)
        self.assertEqual(self.cli('uninstall').returncode, 0)
        self.assertEqual(config.read_text(), 'model = "existing"\n')
        self.assertEqual(other.read_text(), 'user agent')
        self.assertFalse((config.parent / 'agents/poteto-agent.toml').exists())

    def test_occupied_path_prevents_partial_install(self):
        occupied = self.root / '.codex/agents/comment-sicko.toml'
        occupied.parent.mkdir(parents=True)
        occupied.write_text('mine')
        self.assertNotEqual(self.cli('install').returncode, 0)
        self.assertEqual(occupied.read_text(), 'mine')
        self.assertFalse(occupied.with_name('poteto-agent.toml').exists())

    def test_edited_role_prevents_any_removal(self):
        runtime.install(self.root)
        role = self.root / '.codex/agents/comment-sicko.toml'
        role.write_text(role.read_text() + '\nmodel = "override"\n')
        self.assertNotEqual(self.cli('uninstall').returncode, 0)
        self.assertTrue(role.with_name('poteto-agent.toml').exists())

    def test_symlink_and_dangling_symlink_preserved(self):
        for name in ('external', 'missing'):
            with self.subTest(name=name):
                link = self.root / '.codex'
                target = self.root / name
                if name == 'external':
                    target.mkdir()
                link.symlink_to(target)
                self.assertNotEqual(self.cli('install').returncode, 0)
                self.assertTrue(link.is_symlink())
                link.unlink()

    def test_model_precedence_and_inheritance(self):
        runtime.install(self.root)
        def resolve(model=None, effort=None):
            return runtime.resolve_choice(self.root, 'feature', 'parent-model', 'high', model, effort, CATALOG)
        self.assertEqual(resolve(), {'source': 'parent', 'model': 'parent-model', 'reasoning_effort': 'high'})
        runtime.configure(self.root, 'feature', 'role-model', None, CATALOG)
        self.assertEqual(resolve(), {'source': 'role', 'model': 'role-model', 'reasoning_effort': 'medium'})
        self.assertEqual(resolve('parent-model', 'low'), {'source': 'task', 'model': 'parent-model', 'reasoning_effort': 'low'})
        self.assertEqual(resolve('inherit'), {'source': 'task', 'model': 'parent-model', 'reasoning_effort': 'high'})
        self.assertEqual(resolve()['model'], 'role-model')
        runtime.configure(self.root, 'feature', 'inherit', None, CATALOG)
        self.assertEqual(resolve()['reasoning_effort'], 'high')

    def test_research_roles_resolve_through_cli_without_changing_other_choices(self):
        runtime.install(self.root)
        runtime.configure(self.root, 'feature', 'parent-model', 'low', CATALOG)
        catalog = self.root / 'catalog.json'
        catalog.write_text(json.dumps({'source': 'codex/model/list', 'capturedAt': time.time(), 'models': CATALOG}))
        for role in ('how-explorer', 'how-explainer', 'why-investigator', 'why-synthesizer'):
            with self.subTest(role=role):
                base = [sys.executable, '-B', str(SCRIPT)]
                resolve = [*base, 'resolve', str(self.root), role, '--parent-model', 'parent-model',
                           '--parent-effort', 'high', '--catalog', str(catalog)]
                def result(arguments):
                    process = subprocess.run(arguments, capture_output=True, text=True)
                    self.assertEqual(process.returncode, 0, process.stderr)
                    return json.loads(process.stdout)
                def selected(model=None, effort=None):
                    return runtime.resolve_choice(self.root, role, 'parent-model', 'high', model, effort, CATALOG)
                self.assertEqual(selected(), {'source': 'parent', 'model': 'parent-model', 'reasoning_effort': 'high'})
                result([*base, 'configure', str(self.root), role, 'role-model', '--catalog', str(catalog)])
                before = (self.root / '.codex/pstack-models.json').read_bytes()
                self.assertEqual(result(resolve), {'source': 'role', 'model': 'role-model', 'reasoning_effort': 'medium'})
                self.assertEqual(selected('parent-model', 'low'),
                                 {'source': 'task', 'model': 'parent-model', 'reasoning_effort': 'low'})
                self.assertEqual(selected('inherit'),
                                 {'source': 'task', 'model': 'parent-model', 'reasoning_effort': 'high'})
                self.assertEqual((self.root / '.codex/pstack-models.json').read_bytes(), before)
                with self.assertRaises(ValueError):
                    selected('missing')
                self.assertEqual((self.root / '.codex/pstack-models.json').read_bytes(), before)
        self.assertEqual(runtime.load_choices(self.root)['roles']['feature'], {'model': 'parent-model', 'effort': 'low'})

    def test_invalid_selection_does_not_change_preferences(self):
        runtime.configure(self.root, 'bug-fix', 'role-model', 'high', CATALOG)
        path = self.root / '.codex/pstack-models.json'
        before = path.read_bytes()
        for model, effort in [('missing', None), ('parent-model', 'medium'), ('inherit', 'high')]:
            with self.subTest(model=model, effort=effort), self.assertRaises(ValueError):
                runtime.configure(self.root, 'bug-fix', model, effort, CATALOG)
            self.assertEqual(path.read_bytes(), before)

    def test_foreign_or_symlinked_preferences_not_overwritten(self):
        directory = self.root / '.codex'
        directory.mkdir()
        preferences = directory / 'pstack-models.json'
        preferences.write_text('{"unrelated": true}')
        with self.assertRaises(ValueError):
            runtime.configure(self.root, 'feature', 'inherit', None, CATALOG)
        self.assertEqual(json.loads(preferences.read_text()), {'unrelated': True})
        preferences.unlink()
        target = self.root / 'external.json'
        target.write_text('untouched')
        preferences.symlink_to(target)
        with self.assertRaises(ValueError):
            runtime.configure(self.root, 'feature', 'inherit', None, CATALOG)
        self.assertEqual(target.read_text(), 'untouched')

    def test_model_preferences_survive_role_uninstall(self):
        runtime.install(self.root)
        runtime.configure(self.root, 'feature', 'inherit', None, CATALOG)
        runtime.uninstall(self.root)
        self.assertTrue((self.root / '.codex/pstack-models.json').is_file())

    def test_catalog_snapshot_requires_native_source_and_freshness(self):
        path = self.root / 'catalog.json'
        path.write_text(json.dumps({'source': 'codex/model/list', 'capturedAt': time.time(), 'models': CATALOG}))
        self.assertEqual(runtime.read_catalog(path), CATALOG)
        for value in [[], {'source': 'guessed', 'capturedAt': time.time(), 'models': CATALOG},
                      {'source': 'codex/model/list', 'capturedAt': time.time() - 3601, 'models': CATALOG}]:
            path.write_text(json.dumps(value))
            with self.assertRaises(ValueError):
                runtime.read_catalog(path)


if __name__ == '__main__':
    unittest.main()
