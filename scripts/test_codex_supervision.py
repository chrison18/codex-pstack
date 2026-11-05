"""Owned checkpoint tests with captured-shape host stubs, not model/host certification."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/'plugins/pstack/skills/poteto-mode/scripts'
sys.path.insert(0,str(SCRIPTS))
import lifecycle,continuation,supervision,task_event

class SupervisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.w=self.root/'w';self.w.mkdir();self.d=self.root/'record'
        self.ctx=dict(goal='Write a then b',requirements=['No replay'],authority='Local out only',scope=['out'],owner='primary',evidence=[],blockers=[],next_action='a')
        lifecycle.initialize(self.d,self.w,self.ctx,{'a':'append a','b':'append b'})
        continuation.apply(self.d,self.w,'primary','enable',0,grant='supervise bounded task',predicate='ab',limit=2)
        self.call('enable',run_id='run-1',limit=2,seconds=600)
    def tearDown(self):self.tmp.cleanup()
    def state(self):return lifecycle.read_state(self.d,self.w)
    def call(self,action,**kw):return supervision.apply(self.d,self.w,'primary',action,self.state()['revision'],**kw)
    def host(self,task='task-1',done=False):
        return dict(ok=True,result=dict(dispatch=dict(id='dispatch-'+task,taskId=task,runId='run-1',status='completed' if done else 'dispatched',completedAt='time' if done else None),projection=dict(dispatchId='dispatch-'+task,taskId=task,runId='run-1',workspace=dict(id='repo::'+str(self.w)),outcome='succeeded' if done else 'in_progress')))
    def prepare(self,task='task-1'):
        return self.call('prepare',task_id=task)['unit']
    def claim(self,task='task-1'):
        u=self.prepare(task);self.call('claim',task_id=task,token=u['token'],response=self.host(task));return u
    def effect(self,u):
        r=continuation.apply(self.d,self.w,'primary','next',self.state()['revision'],delivery=u['delivery'],writer_token=u['token'])
        with (self.w/'out').open('a') as f:f.write(r['operation'])
        continuation.apply(self.d,self.w,'primary','finish',self.state()['revision'],delivery=u['delivery'],writer_token=u['token'],evidence=['artifact read '+(self.w/'out').read_text()])
    def test_two_units_settlement_duplicate_and_terminal(self):
        original=self.state()['continuation']['frozen'];u=self.claim();self.effect(u)
        self.assertEqual(self.call('prepare',task_id='task-2')['disposition'],'unsettled-start-hold')
        with self.assertRaises(ValueError):self.call('settle',task_id='task-1',response=self.host(),evidence='read a')
        self.call('settle',task_id='task-1',response=self.host(done=True),evidence='read a; no outstanding resources')
        self.assertEqual(self.call('settle',task_id='task-1')['disposition'],'duplicate-settlement-no-advance')
        oldtoken=u['token'];u=self.claim('task-2')
        with self.assertRaises(ValueError):continuation.apply(self.d,self.w,'primary','next',self.state()['revision'],delivery=u['delivery'],writer_token=oldtoken)
        self.effect(u);self.call('settle',task_id='task-2',response=self.host('task-2',True),evidence='read ab; no resources')
        continuation.apply(self.d,self.w,'primary','close',self.state()['revision'],evidence=['exact ab'])
        self.assertEqual((self.w/'out').read_text(),'ab');self.assertEqual(self.state()['continuation']['frozen'],original)
        with patch.object(supervision.subprocess,'run') as launch:
            r=supervision.start(self.d,self.w,'primary',self.state()['revision'],'later');self.assertEqual(r['disposition'],'terminal-no-start');launch.assert_not_called()
    def test_unknown_receipt_and_restart_never_retry(self):
        with patch.object(supervision,'resolve_cli',return_value='orca'),patch.object(supervision.subprocess,'run',side_effect=subprocess.TimeoutExpired('orca',90)) as host:
            supervision.start(self.d,self.w,'primary',self.state()['revision'],'task-1');self.assertEqual(host.call_count,1)
            self.assertEqual(supervision.start(self.d,self.w,'primary',self.state()['revision'],'task-1')['disposition'],'duplicate-no-start');self.assertEqual(host.call_count,1)
        code=f"import sys;sys.path.insert(0,{str(SCRIPTS)!r});import supervision;print(supervision.apply({str(self.d)!r},{str(self.w)!r},'primary','prepare',{self.state()['revision']},task_id='task-2')['disposition'])"
        self.assertEqual(subprocess.check_output([sys.executable,'-B','-c',code],text=True).strip(),'unsettled-start-hold')
        with self.assertRaises(ValueError):self.call('settle',task_id='task-1',response=self.host(done=True),evidence='cannot infer claim')
    def test_cancellation_during_host_start_and_late_claim(self):
        def host(*a,**kw):
            continuation.apply(self.d,self.w,'primary','cancel',self.state()['revision'],reason='user stop')
            return subprocess.CompletedProcess(a,0,'[]','')
        with patch.object(supervision,'resolve_cli',return_value='orca'),patch.object(supervision.subprocess,'run',side_effect=host):supervision.start(self.d,self.w,'primary',self.state()['revision'],'task-1')
        self.assertEqual(self.state()['continuation']['status'],'cancelled')
        self.assertEqual(self.call('claim',task_id='task-1',token='bad',response=self.host())['disposition'],'terminal-no-start')
        self.assertEqual(self.call('prepare',task_id='task-2')['disposition'],'terminal-no-start')
    def test_exact_binding_and_one_assigned_operation(self):
        u=self.prepare();bad=self.host();bad['result']['dispatch']['runId']='other'
        with self.assertRaises(ValueError):self.call('claim',task_id='task-1',token=u['token'],response=bad)
        self.call('claim',task_id='task-1',token=u['token'],response=self.host())
        copied=self.root/'copy';shutil.copytree(self.d,copied)
        with self.assertRaises(ValueError):supervision.apply(copied,self.w,'primary','status')
        with self.assertRaises(ValueError):continuation.apply(copied,self.w,'primary','next',self.state()['revision'],delivery=u['delivery'],writer_token=u['token'])
        with self.assertRaises(ValueError):continuation.apply(self.d,self.w,'primary','next',self.state()['revision'],delivery='extra',writer_token=u['token'])
        self.effect(u)
        with self.assertRaises(ValueError):continuation.apply(self.d,self.w,'primary','next',self.state()['revision'],delivery='second',writer_token=u['token'])
        with self.assertRaises(ValueError):task_event.prepare(self.d,self.w,'primary','event',self.state()['revision'],'proof','owner')
    def test_cancel_between_intent_and_launch(self):
        original=supervision.apply
        def interleave(*args,**kwargs):
            result=original(*args,**kwargs)
            if args[3]=='prepare':continuation.apply(self.d,self.w,'primary','cancel',self.state()['revision'],reason='stop before host invocation')
            return result
        with patch.object(supervision,'apply',side_effect=interleave),patch.object(supervision.subprocess,'run') as host:
            self.assertEqual(supervision.start(self.d,self.w,'primary',self.state()['revision'],'task-1')['disposition'],'terminal-or-deadline-no-start');host.assert_not_called()

    def test_competing_preparations_reserve_only_one_unit(self):
        rev=self.state()['revision'];children=[]
        for task in ('left','right'):
            code=f"import sys;sys.path.insert(0,{str(SCRIPTS)!r});import supervision;print(supervision.apply({str(self.d)!r},{str(self.w)!r},'primary','prepare',{rev},task_id={task!r})['disposition'])"
            children.append(subprocess.Popen([sys.executable,'-B','-c',code],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
        results=[p.communicate(timeout=10) for p in children]
        self.assertEqual(sum('start-once' in out for out,err in results),1)
        self.assertEqual(len(self.state()['supervision']['units']),1)

    def test_malformed_proof_and_late_claim(self):
        u=self.prepare()
        for value in (None, [], 'bad'):
            for path in (('result',),('result','dispatch'),('result','projection'),('result','projection','workspace')):
                bad=self.host();obj=bad
                for key in path[:-1]:obj=obj[key]
                obj[path[-1]]=value
                with self.assertRaises(ValueError):self.call('claim',task_id='task-1',token=u['token'],response=bad)
        with patch.object(supervision.time,'time',return_value=self.state()['supervision']['deadline']+1):
            self.assertEqual(self.call('claim',task_id='task-1',token=u['token'],response=self.host())['disposition'],'deadline-no-execution')
        self.assertEqual(self.state()['supervision']['units'][0]['status'],'intent')

    def test_count_deadline_and_uncertain_effect_hold(self):
        u=self.claim();r=continuation.apply(self.d,self.w,'primary','next',self.state()['revision'],delivery=u['delivery'],writer_token=u['token'])
        with self.assertRaises(ValueError):self.call('settle',task_id='task-1',response=self.host(done=True),evidence='no effect proof')
        continuation.apply(self.d,self.w,'primary','finish',r['state']['revision'],delivery=u['delivery'],writer_token=u['token'],evidence=['controlled no-op complete'])
        self.call('settle',task_id='task-1',response=self.host(done=True),evidence='verified no-op and resources')
        with patch.object(supervision.time,'time',return_value=self.state()['supervision']['deadline']+1):self.assertEqual(self.call('prepare',task_id='task-2')['disposition'],'bound-no-start')
        # Separate smaller limit is established at enable, never silently reset.
        other=self.root/'small';lifecycle.initialize(other,self.w,self.ctx,{'a':'a','b':'b'})
        continuation.apply(other,self.w,'primary','enable',0,grant='bounded',predicate='ab',limit=2)
        supervision.apply(other,self.w,'primary','enable',1,run_id='run-1',limit=1,seconds=600)
        d=self.d;self.d=other;u=self.claim();self.effect(u);self.call('settle',task_id='task-1',response=self.host(done=True),evidence='artifact checked')
        self.assertEqual(self.call('prepare',task_id='task-2')['disposition'],'bound-no-start');self.d=d

if __name__=='__main__':unittest.main()
