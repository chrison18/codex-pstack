"""Reject false completion and invented artifacts in controlled missing-output evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('design', Path(__file__).with_name('accept-codex-design.py'))
design = importlib.util.module_from_spec(spec)
spec.loader.exec_module(design)


class MissingOutputEvidenceTest(unittest.TestCase):
    def test_rejects_false_coverage_and_invented_second_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = Path(directory)
            (outputs / 'synthesis').mkdir()
            (outputs / 'candidate-2').mkdir()
            path = outputs / 'synthesis/coverage.json'
            valid = {'complete': False, 'completed': ['candidate-1'],
                     'missing': ['candidate-2'], 'reason': 'Required input unavailable'}
            path.write_text(json.dumps(valid))
            self.assertTrue(design.missing_output_evidence(outputs, [True, False]))
            for change in [{'complete': True}, {'completed': ['candidate-1', 'candidate-2']},
                           {'missing': []}, {'reason': '  '}, {'reason': 1}]:
                with self.subTest(change=change):
                    path.write_text(json.dumps(dict(valid, **change)))
                    self.assertFalse(design.missing_output_evidence(outputs, [True, False]))
            path.write_text(json.dumps(valid))
            self.assertFalse(design.missing_output_evidence(outputs, [False, False]))
            (outputs / 'candidate-2/invented.py').write_text('fabricated output')
            self.assertFalse(design.missing_output_evidence(outputs, [True, False]))
            path.write_text('{invalid')
            self.assertFalse(design.missing_output_evidence(outputs, [True, False]))


if __name__ == '__main__':
    unittest.main()
