"""Real subprocess interruption and conservative Git audit regression checks."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/pstack/skills/poteto-mode/scripts/lifecycle.py'
spec = importlib.util.spec_from_file_location('lifecycle', SCRIPT)
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.workspace = self.root / 'project'
        self.workspace.mkdir()
        self.task = self.root / 'task'
        self.context = dict(goal='Append two owned records once', requirements=['Keep existing records'],
                            authority='Only this fixture; no external actions', scope=['records.txt'],
                            owner='task-primary', evidence=[], blockers=[], next_action='Append first record')
        lifecycle.initialize(self.task, self.workspace, self.context, {'one':'First append', 'two':'Second append'})

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str,args)], capture_output=True, text=True)

    def test_real_interruption_recovery_never_replays_completed_or_uncertain(self):
        records = self.workspace / 'records.txt'
        lifecycle.mutate(self.task,self.workspace,0,'task-primary','begin','one')
        records.write_text('one\n')
        lifecycle.mutate(self.task,self.workspace,1,'task-primary','complete','one',['records.txt line 1 is one'])
        # Owned child persists intent, performs a side effect, then waits without a receipt.
        code = '''import subprocess,sys,time
from pathlib import Path
subprocess.run([sys.executable,'-B',sys.argv[1],'begin',sys.argv[2],'--task-dir',sys.argv[3],'--owner','task-primary','--revision','2','--operation','two'],check=True,stdout=subprocess.DEVNULL)
with Path(sys.argv[2],'records.txt').open('a') as f:
 f.write('two\\n'); f.flush()
print('side-effect-written',flush=True)
time.sleep(60)
'''
        child = subprocess.Popen([sys.executable,'-u','-c',code,str(SCRIPT),str(self.workspace),str(self.task)],stdout=subprocess.PIPE,text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(),'side-effect-written')
            child.terminate()
            child.wait(timeout=5)
        finally:
            if child.poll() is None:
                child.kill(); child.wait()
            child.stdout.close()
        restarted = self.cli('recover',self.workspace,'--task-dir',self.task)
        self.assertEqual(restarted.returncode,0,restarted.stderr)
        capsule = json.loads(restarted.stdout)
        self.assertEqual(capsule['completed'],['one'])
        self.assertEqual(capsule['uncertain'],['two'])
        self.assertEqual(capsule['state']['context'],self.context)
        for operation in ('one','two'):
            retry = self.cli('begin',self.workspace,'--task-dir',self.task,'--revision',3,'--owner','task-primary','--operation',operation)
            self.assertNotEqual(retry.returncode,0)
        self.assertEqual(records.read_text(),'one\ntwo\n')
        settled = self.cli('complete',self.workspace,'--task-dir',self.task,'--revision',3,'--owner','task-primary','--operation','two','--evidence','Observed records.txt exactly one then two; no replay')
        self.assertEqual(settled.returncode,0,settled.stderr)
        self.assertEqual(lifecycle.recover(self.task,self.workspace)['completed'],['one','two'])
        self.assertEqual(records.read_text(),'one\ntwo\n')

    def test_interrupted_before_effect_uses_evidence_linked_successor(self):
        code = """import subprocess,sys,time
subprocess.run([sys.executable,'-B',sys.argv[1],'begin',sys.argv[2],'--task-dir',sys.argv[3],'--owner','task-primary','--revision','0','--operation','one'],check=True,stdout=subprocess.DEVNULL)
print('intent-only',flush=True)
time.sleep(60)
"""
        child=subprocess.Popen([sys.executable,'-u','-c',code,str(SCRIPT),str(self.workspace),str(self.task)],stdout=subprocess.PIPE,text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(),'intent-only')
            child.terminate();child.wait(timeout=5)
        finally:
            if child.poll() is None: child.kill();child.wait()
            child.stdout.close()
        self.assertFalse((self.workspace/'records.txt').exists())
        original=(self.task/'state.json').read_bytes()
        self.assertEqual(lifecycle.recover(self.task,self.workspace)['uncertain'],['one'])
        successor=self.root/'successor'
        reason='Owned process settled before append; records.txt absent; predecessor task/one remains uncertain'
        context=dict(self.context,evidence=[reason],next_action='Perform missing append once in successor')
        lifecycle.initialize(successor,self.workspace,context,{'missing-one':'Evidence-linked replacement for task/one'})
        lifecycle.mutate(successor,self.workspace,0,'task-primary','begin','missing-one')
        (self.workspace/'records.txt').write_text('one\n')
        lifecycle.mutate(successor,self.workspace,1,'task-primary','complete','missing-one',['Observed one record'])
        with self.assertRaises(ValueError):
            lifecycle.mutate(successor,self.workspace,2,'task-primary','begin','missing-one')
        self.assertEqual((self.task/'state.json').read_bytes(),original)
        self.assertEqual((self.workspace/'records.txt').read_text(),'one\n')
        self.assertIn(reason,lifecycle.recover(successor,self.workspace)['state']['context']['evidence'])

    def test_malformed_context_input_and_record_leave_state_untouched(self):
        original=(self.task/'state.json').read_bytes()
        source=self.root/'input.json'
        for value in ('{bad', '[]', '{"goal":"missing context fields"}'):
            source.write_text(value)
            result=self.cli('checkpoint',self.workspace,'--task-dir',self.task,'--revision',0,'--owner','task-primary','--input',source,'--reason','test')
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((self.task/'state.json').read_bytes(),original)
        for value in ('[]', '{"schema":99}'):
            (self.task/'state.json').write_text(value)
            self.assertNotEqual(self.cli('recover',self.workspace,'--task-dir',self.task).returncode,0)
            self.assertEqual((self.task/'state.json').read_text(),value)

    def test_stale_owner_and_revision_do_not_mutate_history(self):
        before=(self.task/'state.json').read_bytes()
        for revision,owner in ((99,'task-primary'),(0,'other')):
            with self.assertRaises(ValueError): lifecycle.mutate(self.task,self.workspace,revision,owner,'begin','one')
        self.assertEqual((self.task/'state.json').read_bytes(),before)
        changed=dict(self.context,blockers=['Need result evidence'],next_action='Inspect records')
        lifecycle.mutate(self.task,self.workspace,0,'task-primary','checkpoint',context=changed,reason='Interrupted at boundary')
        state=lifecycle.read_state(self.task,self.workspace)
        self.assertEqual(state['history'][0]['context'],self.context)
        self.assertEqual(state['context'],changed)

    def test_history_scoped_identity_and_symlink_refusal(self):
        other=self.root/'other'; other.mkdir()
        (other/'private.txt').write_text('UNRELATED_SECRET')
        denied=self.cli('history',other,'--task-dir',self.task)
        self.assertNotEqual(denied.returncode,0)
        own=self.cli('history',self.workspace,'--task-dir',self.task)
        self.assertEqual(own.returncode,0)
        self.assertNotIn('UNRELATED_SECRET',own.stdout)
        link=self.root/'link'; link.symlink_to(self.task)
        with self.assertRaises(ValueError): lifecycle.recover(link,self.workspace)
        (self.task/'state.json').write_text('{broken')
        self.assertNotEqual(self.cli('recover',self.workspace,'--task-dir',self.task).returncode,0)

    def test_audit_real_git_dirty_active_open_unknown_never_safe(self):
        def git(*args):
            return subprocess.check_output(['git','-C',str(self.workspace),*args],text=True).strip()
        git('init','-q'); (self.workspace/'tracked').write_text('base')
        git('add','tracked');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','base')
        head=git('rev-parse','HEAD')
        observations=dict(workspace=str(self.workspace),head=head,session=dict(status='settled',evidence='Synthetic owned session ended'),pr=dict(status='none',evidence='Offline fixture, no remote or PR'))
        for key,status in (('session','active'),('session','unknown'),('pr','open'),('pr','unknown')):
            changed=dict(observations);changed[key]=dict(status=status,evidence='controlled observation')
            result=lifecycle.audit(self.workspace,head,changed)
            self.assertEqual(result['verdict'],'hold');self.assertFalse(result['safe_to_delete'])
        self.assertEqual(lifecycle.audit(self.workspace,head,{})['verdict'],'hold')
        mismatch=dict(observations,head='wrong-head')
        self.assertIn('observation-identity-mismatch',lifecycle.audit(self.workspace,head,mismatch)['reasons'])
        self.assertEqual(lifecycle.audit(self.workspace,head,observations)['verdict'],'review-only')
        (self.workspace/'tracked').write_text('WIP')
        self.assertIn('dirty',lifecycle.audit(self.workspace,head,observations)['reasons'])
        self.assertEqual((self.workspace/'tracked').read_text(),'WIP')
        self.assertIn('git-state-unknown',lifecycle.audit(self.workspace,'missing-base',observations)['reasons'])


if __name__=='__main__':
    unittest.main()
