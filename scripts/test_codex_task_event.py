"""Owned one-shot delivery tests; fake host observes actual subprocess/crash boundaries."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'plugins/pstack/skills/poteto-mode/scripts'
sys.path.insert(0,str(SCRIPTS))
import lifecycle,continuation,task_event

class EventTests(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'ORCA_CLI_COMMAND':sys.executable});self.env.start()
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        self.w=self.root/'workspace';self.w.mkdir();self.t=self.root/'task'
        self.ctx=dict(goal='Write a then b',requirements=['No replay'],authority='Owned files only',scope=['out'],owner='primary',evidence=[],blockers=[],next_action='Write a')
        lifecycle.initialize(self.t,self.w,self.ctx,{'a':'Write a','b':'Write b'})
        continuation.apply(self.t,self.w,'primary','enable',0,grant='Bounded task',predicate='Exact a b',limit=2)
    def tearDown(self):self.tmp.cleanup();self.env.stop()
    def state(self):return lifecycle.read_state(self.t,self.w)
    def prepare(self,event='e'):
        return task_event.prepare(self.t,self.w,'primary',event,self.state()['revision'],'Mapped prior completed turn plus artifact check','Prior writer settled; sole owner of this exact task')
    def test_binding_claim_and_terminal_guards(self):
        p=self.prepare();token=p['event']['token']
        with self.assertRaises(ValueError):continuation.apply(self.t,self.w,'primary','next',self.state()['revision'],delivery='a')
        copied=self.root/'copied';shutil.copytree(self.t,copied)
        with self.assertRaises(ValueError):task_event.claim(copied,self.w,'primary','e',token)
        wrong=self.root/'wrong';wrong.mkdir()
        with self.assertRaises(ValueError):task_event.claim(self.t,wrong,'primary','e',token)
        with self.assertRaises(ValueError):task_event.claim(self.t,self.w,'primary','other',token)
        with self.assertRaises(ValueError):task_event.claim(self.t,self.w,'primary','e','wrong')
        self.assertEqual(task_event.claim(self.t,self.w,'primary','e',token)['disposition'],'claimed')
        self.assertEqual(task_event.claim(self.t,self.w,'primary','e',token)['disposition'],'already-claimed-no-execution')
        copied_claimed=self.root/'copied-claimed';shutil.copytree(self.t,copied_claimed)
        with self.assertRaises(ValueError):
            continuation.apply(copied_claimed,self.w,'primary','next',self.state()['revision'],delivery='bad',event_token=token)
        self.assertEqual(continuation.apply(self.t,self.w,'primary','next',self.state()['revision'],delivery='a',event_token=token)['operation'],'a')
        continuation.apply(self.t,self.w,'primary','cancel',self.state()['revision'],reason='Cancel during launch')
        self.assertEqual(task_event.claim(self.t,self.w,'primary','e',token)['disposition'],'terminal-no-execution')
        self.assertEqual(self.prepare('later')['disposition'],'terminal-no-launch')
    def test_crash_before_and_after_host_effect_no_relaunch(self):
        self.prepare() # crashed after intent, before host invocation
        with patch.object(task_event.subprocess,'run') as run:
            self.assertEqual(task_event.send(self.t,self.w,'primary','e',1,'proof','owner')['disposition'],'duplicate-no-launch');run.assert_not_called()
        self.assertEqual(self.prepare('other')['disposition'],'prior-event-unsettled-no-launch')
        # Real child process writes host effect, then waits: kill sender while receipt is absent.
        other=self.root/'second';lifecycle.initialize(other,self.w,self.ctx,{'a':'a'})
        continuation.apply(other,self.w,'primary','enable',0,grant='bounded',predicate='a',limit=1)
        code=f"import sys,time;sys.path.insert(0,{str(SCRIPTS)!r});import task_event;from pathlib import Path;p=task_event.prepare({str(other)!r},{str(self.w)!r},'primary','x',1,'proof','owner');Path({str(self.root/'host-effect')!r}).write_text('one launch');time.sleep(30)"
        proc=subprocess.Popen([sys.executable,'-B','-c',code])
        try:
            for _ in range(100):
                if (self.root/'host-effect').exists():break
                time.sleep(.01)
            self.assertTrue((self.root/'host-effect').exists())
        finally:proc.terminate();proc.wait(timeout=5)
        with patch.object(task_event.subprocess,'run') as run:
            self.assertEqual(task_event.send(other,self.w,'primary','x',1,'proof','owner')['disposition'],'duplicate-no-launch');run.assert_not_called()
    def test_concurrent_events_one_intent(self):
        base=[sys.executable,'-B','-c']
        def code(e):return f"import sys,json;sys.path.insert(0,{str(SCRIPTS)!r});import task_event;print(json.dumps(task_event.prepare({str(self.t)!r},{str(self.w)!r},'primary',{e!r},1,'proof','owner')))"
        children=[subprocess.Popen(base+[code(e)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for e in ['x','y']]
        replies=[c.communicate(timeout=5) for c in children]
        self.assertEqual(sum(c.returncode==0 and json.loads(r[0])['disposition']=='launch-once' for c,r in zip(children,replies)),1)
        self.assertEqual(len(self.state()['task_events']),1)
    def test_lost_reply_cancel_during_host_call_and_receiver_completion(self):
        def host(*args,**kwargs):
            continuation.apply(self.t,self.w,'primary','cancel',self.state()['revision'],reason='Cancel while host executes')
            raise subprocess.TimeoutExpired('orca',60)
        with patch.object(task_event.subprocess,'run',side_effect=host):
            self.assertEqual(task_event.send(self.t,self.w,'primary','e',1,'proof','owner')['disposition'],'unknown-hold-no-relaunch')
        self.assertEqual(self.state()['continuation']['status'],'cancelled')
        self.assertFalse(self.state()['task_events']['e']['claimed'])
    def test_malformed_receipts_hold(self):
        self.prepare()
        for receipt in [[],{'ok':True,'result':[]},{'ok':True,'result':{'outcome':[],'prompt':None}}]:
            self.assertEqual(task_event.record_receipt(self.t,self.w,'primary','e',receipt)['disposition'],'unknown-hold-no-relaunch')

    def test_accept_claim_race_settlement_and_complete_no_wake(self):
        def host(*args,**kwargs):
            token=self.state()['task_events']['e']['token']
            task_event.claim(self.t,self.w,'primary','e',token)
            return subprocess.CompletedProcess(args,0,json.dumps({'ok':True,'result':{'outcome':{'kind':'structured','sessionId':'test'},'prompt':{'outcome':'journaled'},'operationId':'op-test','worktreeId':'fixture::'+str(self.w)}}),'')
        with patch.object(task_event.subprocess,'run',side_effect=host):task_event.send(self.t,self.w,'primary','e',1,'proof','owner')
        self.assertTrue(self.state()['task_events']['e']['claimed'])
        token=self.state()['task_events']['e']['token']
        for event in ['a','b']:
            continuation.apply(self.t,self.w,'primary','next',self.state()['revision'],delivery=event,event_token=token)
            with (self.w/'out').open('a') as f:f.write(event+'\n')
            continuation.apply(self.t,self.w,'primary','finish',self.state()['revision'],delivery=event,evidence=['Read exact prefix'],event_token=token)
        self.assertEqual((self.w/'out').read_text(),'a\nb\n')
        continuation.apply(self.t,self.w,'primary','close',self.state()['revision'],evidence=['Exact a b'],event_token=token)
        with patch.object(task_event.subprocess,'run') as run:
            self.assertEqual(task_event.send(self.t,self.w,'primary','new',self.state()['revision'],'proof','owner')['disposition'],'terminal-no-launch');run.assert_not_called()
        task_event.settle(self.t,self.w,'primary','e',self.state()['revision'],'Mapped completion and verified output','No writer remains')
        self.assertEqual(self.state()['task_events']['e']['status'],'settled')

if __name__=='__main__':unittest.main()
