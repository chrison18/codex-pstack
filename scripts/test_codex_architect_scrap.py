"""The controlled friction fixture must expose two independent failures, not one short circuit."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('scrap', Path(__file__).with_name('accept-codex-architect-scrap.py'))
scrap = importlib.util.module_from_spec(spec); spec.loader.exec_module(scrap)


class FixtureProofTest(unittest.TestCase):
    def test_two_failures_and_control_then_reference_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / 'fixture'
            scrap.write_fixture(workspace)
            self.assertEqual(scrap.check(workspace, 'ReceiptContract.test_simple')['exitCode'], 0)
            for name in ('retained_quotes', 'nested_render'):
                result = scrap.check(workspace, 'ReceiptContract.test_' + name)
                self.assertNotEqual(result['exitCode'], 0)
                self.assertIn('FAIL: test_' + name, result['stderr'])
            suite = scrap.check(workspace)
            self.assertIn('Ran 3 tests', suite['stderr'])
            self.assertIn('failures=2', suite['stderr'])
            # Host-only witness: not placed in the native fixture or its prompt.
            (workspace / 'app.py').write_text('''def prepare(customer, rows):
    return Receipt(customer, tuple(rows))


class Receipt:
    def __init__(self, customer, rows):
        self.customer, self.rows = customer, rows

    def render(self, before_render=None):
        if before_render is not None:
            before_render()
        return {"customer": self.customer, "total": sum(p*q for p,q in self.rows)}
''')
            self.assertEqual(scrap.check(workspace)['exitCode'], 0)


if __name__ == '__main__':
    unittest.main()
