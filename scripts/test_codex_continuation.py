"""Continuation boundaries with real subprocess deliveries and owned side effects."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'plugins/pstack/skills/poteto-mode/scripts'
sys.path.insert(0,str(SCRIPTS))
import lifecycle
import continuation


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        self.project=self.root/'project';self.project.mkdir();self.task=self.root/'task'
        self.ctx=dict(goal='Append a and b once',requirements=['Exact ordered lines'],authority='Owned local files only',scope=['out'],owner='primary',evidence=[],blockers=[],next_action='Append a')
        lifecycle.initialize(self.task,self.project,self.ctx,{'a':'Append a','b':'Append b'})
        self.do('enable',predicate='out bytes equal a newline b newline',grant='User authorized this bounded local task',limit=2)

    def tearDown(self): self.tmp.cleanup()

    def do(self,action,**kwargs):
        state=lifecycle.read_state(self.task,self.project)
        return continuation.apply(self.task,self.project,'primary',action,revision=state['revision'],**kwargs)

    def cli(self,*args):
        return [sys.executable,'-B',str(SCRIPTS/'continuation.py'),*args,str(self.project),'--task-dir',str(self.task),'--owner','primary']

    def test_fresh_process_delivery_restart_duplicate_and_completion_stop(self):
        first=self.do('next',delivery='event-1');self.assertEqual(first['operation'],'a')
        (self.project/'out').write_text('a\n')
        self.do('finish',delivery='event-1',evidence=['Observed one a line'])
        result=subprocess.run(self.cli('next')+['--delivery','event-1','--revision','0'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0)
        self.assertEqual(json.loads(result.stdout)['disposition'],'duplicate-no-execution')
        claimed=self.do('next',delivery='event-2');self.assertEqual(claimed['operation'],'b')
        with (self.project/'out').open('a') as f:f.write('b\n')
        self.do('finish',delivery='event-2',evidence=['Observed exactly a then b'])
        self.assertEqual(self.do('next',delivery='event-3')['disposition'],'verify-predicate-before-close')
        with self.assertRaises(ValueError):self.do('close')
        self.assertEqual((self.project/'out').read_text(),'a\nb\n')
        self.do('close',evidence=['Independently read exact bytes a newline b newline'])
        before=(self.task/'state.json').read_bytes()
        self.assertEqual(self.do('next',delivery='later')['disposition'],'completed-no-execution')
        with self.assertRaises(ValueError):lifecycle.mutate(self.task,self.project,5,'primary','begin','a')
        self.assertEqual((self.task/'state.json').read_bytes(),before)

    def test_cancel_between_issue_and_finish_preserves_uncertainty(self):
        self.do('next',delivery='inflight')
        (self.project/'out').write_text('a\n')
        self.do('cancel',reason='User cancelled while result receipt missing')
        for action,kwargs in [('next',dict(delivery='new')),('finish',dict(delivery='inflight',evidence=['a exists'])),('close',dict(evidence=['done']))]:
            self.assertEqual(self.do(action,**kwargs)['disposition'],'cancelled-no-execution')
        state=lifecycle.read_state(self.task,self.project)
        self.assertEqual(state['operations']['a']['status'],'started')
        self.assertEqual(state['operations']['b']['status'],'pending')
        with self.assertRaises(ValueError):lifecycle.mutate(self.task,self.project,state['revision'],'primary','complete','a',['a exists'])
        self.assertEqual((self.project/'out').read_text(),'a\n')

    def test_restart_uncertainty_requires_evidence_not_replay(self):
        self.do('next',delivery='original')
        (self.project/'out').write_text('a\n')
        state=lifecycle.read_state(self.task,self.project)
        restart=subprocess.run(self.cli('next')+['--delivery','restart','--revision',str(state['revision'])],capture_output=True,text=True)
        self.assertEqual(json.loads(restart.stdout)['disposition'],'uncertain-no-execution')
        self.do('finish',delivery='original',evidence=['After settled previous writer, independently found exact a line'])
        self.assertEqual((self.project/'out').read_text(),'a\n')
        self.assertEqual(self.do('next',delivery='restart')['operation'],'b')

    def test_concurrent_claims_only_one_issues_work(self):
        rev=str(lifecycle.read_state(self.task,self.project)['revision'])
        commands=[self.cli('next')+['--revision',rev,'--delivery',key] for key in ('x','y')]
        children=[subprocess.Popen(c,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for c in commands]
        results=[c.communicate(timeout=5) for c in children]
        self.assertEqual(sum(c.returncode==0 and json.loads(r[0])['disposition']=='execute-one' for c,r in zip(children,results)),1)
        state=lifecycle.read_state(self.task,self.project)
        self.assertEqual(len(state['continuation']['deliveries']),1)
        self.assertEqual([op['status'] for op in state['operations'].values()],['started','pending'])

    def test_budget_and_scope_fail_closed(self):
        # A distinct declared small-budget run, not a reset of the configured task.
        task=self.root/'limited';lifecycle.initialize(task,self.project,self.ctx,{'a':'a','b':'b'})
        def call(action,**kw):
            return continuation.apply(task,self.project,'primary',action,lifecycle.read_state(task,self.project)['revision'],**kw)
        call('enable',predicate='Both verified',grant='Only one step authorized this slice',limit=1)
        call('next',delivery='one');call('finish',delivery='one',evidence=['Fixture operation observed'])
        r=call('next',delivery='two');self.assertEqual(r['disposition'],'budget-exhausted-no-execution')
        self.assertTrue(r['state']['context']['blockers']);self.assertEqual(r['state']['operations']['b']['status'],'pending')
        with self.assertRaises(ValueError):call('close',evidence=['not done'])
        changed=dict(self.ctx,scope=['unrelated'])
        with self.assertRaises(ValueError):self.do('checkpoint',context=changed,reason='not authorized')
        self.do('checkpoint',context=dict(self.ctx,blockers=['Dependency unavailable']),reason='Observed missing dependency')
        self.assertEqual(self.do('next',delivery='blocked')['disposition'],'blocked-no-execution')


if __name__=='__main__': unittest.main()
