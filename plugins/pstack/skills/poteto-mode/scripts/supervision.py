"""Durable guards for foreground Orca supervision, not a scheduler."""
import argparse
import json
from pathlib import Path
import secrets
import subprocess
import time
import lifecycle
import continuation
from task_event import resolve_cli


def checked(directory, workspace, owner):
    state = lifecycle.read_state(directory, workspace)
    continuation.validate(state.get('continuation'))
    if state['context']['owner'] != owner or continuation.grant_context(state) != state['continuation']['frozen']:
        raise ValueError('Wrong owner or changed frozen contract')
    run = state.get('supervision')
    if run and (run['task_dir'] != str(directory) or run['workspace'] != state['workspace']):
        raise ValueError('Copied supervision binding')
    return state


def commit(directory, state, action):
    state['revision'] += 1
    state['history'].append(dict(revision=state['revision'], action='supervision:'+action))
    lifecycle.save(directory,state)


def proof(state, unit, response, settled=False):
    if not isinstance(response,dict) or response.get('ok') is not True:
        raise ValueError('Actual successful worker-show response required')
    result=response.get('result')
    if not isinstance(result,dict):raise ValueError('Malformed worker-show result')
    d=result.get('dispatch'); p=result.get('projection')
    if not isinstance(d,dict) or not isinstance(p,dict) or not isinstance(p.get('workspace'),dict):
        raise ValueError('Malformed dispatch/projection/workspace proof')
    if (d.get('taskId') != unit['task_id'] or d.get('runId') != state['supervision']['run_id']
        or not lifecycle.text(d.get('id')) or p.get('dispatchId') != d['id']
        or p.get('taskId') != unit['task_id'] or p.get('runId') != d['runId']
        or not str(p.get('workspace',{}).get('id','')).endswith('::'+state['workspace'])):
        raise ValueError('Wrong host Run/Task/Dispatch/workspace proof')
    if unit.get('dispatch_id') and unit['dispatch_id'] != d['id']:
        raise ValueError('Different dispatch cannot replace bound attempt')
    if settled:
        if d.get('status') != 'completed' or not d.get('completedAt') or p.get('outcome') != 'succeeded':
            raise ValueError('Exact accepted successful settlement required; failure/unknown HOLD')
    elif d.get('status') != 'dispatched' or p.get('outcome') != 'in_progress':
        raise ValueError('Live authoritative dispatch required to claim')
    return d['id']


def mutation_guard(directory,state,action,delivery,token):
    run=state.get('supervision')
    if not run or action=='cancel': return
    if run['task_dir']!=str(directory) or run['workspace']!=state['workspace']:
        raise ValueError('Copied supervision binding')
    units=run['units']; active=units[-1] if units else None
    if action=='close':
        if any(u['status']!='settled' for u in units):raise ValueError('Unsettled writer; cannot close')
        return
    if action not in ('next','finish','checkpoint') or not active or active['status']!='claimed' or active['token']!=token:
        raise ValueError('Claimed supervised writer token required')
    if action in ('next','finish') and delivery!=active['delivery']:
        raise ValueError('Only assigned operation delivery is authorized')
    if action=='next':
        if time.time()>=run['deadline']:raise ValueError('Supervision deadline reached; no new effect')
        pending=[k for k,v in state['operations'].items() if v['status']=='pending']
        if not pending or pending[0]!=active['operation']:raise ValueError('Only assigned operation is authorized')


def apply(directory,workspace,owner,action,revision=None,run_id=None,task_id=None,
          limit=None,seconds=None,token=None,response=None,evidence=None):
    with lifecycle.locked(directory) as directory:
        state=checked(directory,workspace,owner); run=state.get('supervision')
        if action=='status':return dict(disposition='inspect-only',state=state)
        if state['continuation']['status']!='active' and action!='settle':
            return dict(disposition='terminal-no-start',state=state)
        if action=='prepare' and run and any(u['task_id']==task_id for u in run['units']):
            return dict(disposition='duplicate-no-start',state=state)
        if action=='settle' and run and run['units'] and run['units'][-1]['status']=='settled':
            return dict(disposition='duplicate-settlement-no-advance',state=state)
        if revision!=state['revision']:raise ValueError('Stale revision')
        if action=='enable':
            if run or state.get('active_event'):raise ValueError('Already owned by another delivery mode')
            if not lifecycle.text(run_id) or type(limit)!=int or limit<1 or type(seconds)!=int or seconds<1:
                raise ValueError('Run identity and finite dispatch/time limits required')
            if any(o['status']=='started' for o in state['operations'].values()):raise ValueError('Reconcile uncertain effects first')
            state['supervision']=dict(run_id=run_id,task_dir=str(directory),workspace=state['workspace'],limit=limit,deadline=time.time()+seconds,units=[])
            result=dict(disposition='enabled')
        elif action=='prepare':
            if not run:raise ValueError('Enable supervision first')
            if run['units'] and run['units'][-1]['status']!='settled':return dict(disposition='unsettled-start-hold',state=state)
            if time.time()>=run['deadline'] or len(run['units'])>=run['limit']:return dict(disposition='bound-no-start',state=state)
            if state['context']['blockers'] or any(o['status']=='started' for o in state['operations'].values()):return dict(disposition='uncertain-or-blocked-hold',state=state)
            pending=[k for k,o in state['operations'].items() if o['status']=='pending']
            if not pending:return dict(disposition='verify-before-close',state=state)
            if not lifecycle.text(task_id):raise ValueError('Precreated Orca Task ID required')
            unit=dict(task_id=task_id,operation=pending[0],delivery='supervised:'+task_id,token=secrets.token_hex(24),status='intent')
            run['units'].append(unit); result=dict(disposition='start-once',unit=unit)
        elif action in ('claim','settle','receipt'):
            if not run or not run['units']:raise ValueError('No intended worker')
            unit=run['units'][-1]
            if unit['task_id']!=task_id:raise ValueError('Wrong task')
            if action=='receipt':
                # Raw host outcome is retained, never interpreted as settlement or permission to retry.
                unit['start_receipt']=response; result=dict(disposition='receipt-recorded-inspect-dispatch')
            elif action=='claim':
                if time.time()>=run['deadline']:return dict(disposition='deadline-no-execution',state=state)
                if token!=unit['token']:raise ValueError('Wrong writer token')
                if unit['status']=='claimed':return dict(disposition='duplicate-claim-no-execution',state=state)
                if unit['status']!='intent':raise ValueError('Writer no longer owns unit')
                unit['dispatch_id']=proof(state,unit,response);unit['status']='claimed';result=dict(disposition='claimed',unit=unit)
            else:
                if unit['status']!='claimed':raise ValueError('Unclaimed/unknown start HOLD')
                proof(state,unit,response,True)
                if not lifecycle.text(evidence):raise ValueError('Primary artifact/resource reconciliation evidence required')
                if state['operations'][unit['operation']]['status']!='completed':raise ValueError('Unit effects incomplete/uncertain')
                if state['continuation']['deliveries'].get(unit['delivery'],{}).get('status')!='settled':raise ValueError('Operation receipt missing')
                unit.update(status='settled',settlement=response,evidence=evidence);result=dict(disposition='settled')
        else:raise ValueError('Unknown action')
        commit(directory,state,action);result['state']=state;return result


def start(directory,workspace,owner,revision,task_id,model=None,effort=None):
    if effort and not model:raise ValueError('Effort requires an explicit model')
    result=apply(directory,workspace,owner,'prepare',revision,task_id=task_id)
    if result['disposition']!='start-once':return result
    # Intent is durable; never repeat this host mutation, including after timeout/crash.
    with lifecycle.locked(directory) as d:
        s=checked(d,workspace,owner)
        if s['continuation']['status']!='active' or time.time()>=s['supervision']['deadline']:
            return dict(disposition='terminal-or-deadline-no-start')
        argv=[resolve_cli(),'orchestration','worker-start','--run',s['supervision']['run_id'],'--task',task_id,'--worktree','path:'+s['workspace'],'--agent','codex','--json']
        if model:argv.extend(['--model',model])
        if effort:argv.extend(['--effort',effort])
        s['supervision']['units'][-1].update(argv=argv,cwd=s['workspace'])
        commit(d,s,'launch-command')
    try:
        r=subprocess.run(argv,cwd=s['workspace'],capture_output=True,text=True,timeout=90)
        try: receipt=json.loads(r.stdout)
        except ValueError:receipt=dict(ok=False,reason='unparseable',returncode=r.returncode)
    except (OSError,subprocess.TimeoutExpired) as error:receipt=dict(ok=False,reason=type(error).__name__)
    # A worker may already claim/finish before the launch reply; merge under current revision.
    with lifecycle.locked(directory) as d:
        s=checked(d,workspace,owner);u=s['supervision']['units'][-1]
        if u['task_id']!=task_id:raise ValueError('Start ownership changed')
        u['start_receipt']=receipt;commit(d,s,'receipt')
    return dict(disposition='start-returned-not-settled',receipt=receipt,state=s)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['enable','status','start','claim','settle'])
    p.add_argument('workspace');p.add_argument('--task-dir',required=True);p.add_argument('--owner',required=True)
    p.add_argument('--revision',type=int);p.add_argument('--run-id');p.add_argument('--task-id')
    p.add_argument('--model');p.add_argument('--effort')
    p.add_argument('--limit',type=int);p.add_argument('--seconds',type=int);p.add_argument('--token');p.add_argument('--input');p.add_argument('--evidence')
    a=p.parse_args()
    try:
        if a.action=='start':r=start(a.task_dir,a.workspace,a.owner,a.revision,a.task_id,a.model,a.effort)
        else:r=apply(a.task_dir,a.workspace,a.owner,a.action,a.revision,a.run_id,a.task_id,a.limit,a.seconds,a.token,json.loads(Path(a.input).read_text()) if a.input else None,a.evidence)
        print(json.dumps(r,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(1,str(e)+'\n')


if __name__=='__main__':main()
