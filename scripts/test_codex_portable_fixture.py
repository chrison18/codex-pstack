"""Exercise actual fixture contracts without models, accounts or a browser installation."""
import importlib.util
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('portable',Path(__file__).with_name('accept-codex-portable.py'))
portable=importlib.util.module_from_spec(spec);spec.loader.exec_module(portable)


class PortableFixtures(unittest.TestCase):
    def setUp(self):
        scratch=tempfile.TemporaryDirectory();self.addCleanup(scratch.cleanup)
        self.root=Path(scratch.name).resolve();self.workspace=self.root/'harbor';self.workspace.mkdir()
        self.outputs=self.root/'proof';self.outputs.mkdir()

    def prepare(self,case):
        portable.prepare(self.workspace,case,self.outputs,self.root)

    def test_generated_skill_scope_allows_its_parent_but_not_siblings(self):
        self.assertTrue(portable.allowed('verification','verification-skills'))
        self.assertTrue(portable.allowed('verification','verification-skills/verify-harbor/SKILL.md'))
        self.assertFalse(portable.allowed('verification','verification-skills/other/SKILL.md'))
        self.assertFalse(portable.allowed('verification','verification-skills/verify-slots/SKILL.md'))
        self.assertFalse(portable.allowed('quality','verification-skills'))

    def test_line_metric_counts_generator_work_instead_of_hiding_it(self):
        self.prepare('measurement')
        def measure():
            result=subprocess.run(['python3','-B','measure.py'],cwd=self.workspace,capture_output=True,text=True,check=True,timeout=10)
            return json.loads(result.stdout)
        baseline=measure()
        (self.workspace/'app.py').write_text('def unique(values):\n    result=[]\n    for value in values:\n        if not any(previous==value for previous in result):\n            result.append(value)\n    return result\n')
        generator=measure()
        self.assertEqual(generator['work'],80)
        self.assertEqual(generator['errors'],0)
        self.assertGreater(generator['value'],baseline['value']*.5)

    def test_zero_regression_executes_through_the_real_consumer(self):
        self.prepare('quality')
        bun=shutil.which('bun')
        self.assertIsNotNone(bun,'Bun is required for the real TypeScript fixture')
        def check():return subprocess.run([bun,'check.ts'],cwd=self.workspace,capture_output=True,text=True,timeout=10)
        before=check();self.assertNotEqual(before.returncode,0);self.assertIn('zero quantity',before.stderr)
        source=self.workspace/'app.ts';source.write_text(source.read_text().replace('(row.quantity || 1)','row.quantity'))
        after=check();self.assertEqual(after.returncode,0,after.stderr);self.assertIn('quality acceptance passed',after.stdout)

    def test_pty_driver_observes_real_prompt_and_command_output(self):
        self.prepare('verification');proof=self.outputs/'greeting.json'
        result=subprocess.run(['python3','-B','drive.py','--command','greet Ada','--output',str(proof)],cwd=self.workspace,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
        evidence=json.loads(proof.read_text());self.assertEqual(evidence['exitCode'],0)
        self.assertIn('Harbor ready',evidence['transcript']);self.assertIn('Hello Ada',evidence['transcript'])

    def test_finite_slot_property_distinguishes_actual_broken_code(self):
        self.prepare('formal');source=self.workspace/'slots.py';code=runpy.run_path(str(source))
        for used in range(4):
            self.assertTrue(0<=code['reserve'](used)<=3);self.assertTrue(0<=code['release'](used)<=3)
        broken=self.root/'broken.py';broken.write_text(source.read_text().replace('used < LIMIT','True'))
        self.assertGreater(runpy.run_path(str(broken))['reserve'](3),3)


if __name__=='__main__':unittest.main()
