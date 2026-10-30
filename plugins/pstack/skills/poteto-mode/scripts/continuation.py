"""Bounded cooperative continuation of one phase4 task; no scheduler or executor."""
import argparse
import copy
import json
from pathlib import Path
import lifecycle

FROZEN = ('goal', 'requirements', 'authority', 'scope', 'owner')


def grant_context(state):
    return {key: copy.deepcopy(state['context'][key]) for key in FROZEN}


def validate(run):
    if not isinstance(run, dict) or run.get('schema') != 1 or run.get('status') not in ('active','cancelled','completed'):
        raise ValueError('Invalid continuation state')
    if type(run.get('limit')) is not int or run['limit'] < 1 or not isinstance(run.get('deliveries'),dict):
        raise ValueError('Invalid budget/deliveries')
    if not lifecycle.text(run.get('predicate')) or not lifecycle.text(run.get('grant')) or not isinstance(run.get('frozen'),dict):
        raise ValueError('Invalid grant')
    for key, value in run['deliveries'].items():
        if not lifecycle.text(key) or not isinstance(value,dict) or not lifecycle.text(value.get('operation')):
            raise ValueError('Invalid delivery receipt')


def apply(directory, workspace, owner, action, revision=None, delivery=None, evidence=None,
          predicate=None, grant=None, limit=None, reason=None, context=None):
    with lifecycle.locked(directory) as directory:
        state = lifecycle.read_state(directory, workspace)
        if owner != state['context']['owner']:
            raise ValueError('Wrong task owner')
        run = state.get('continuation')
        if action == 'enable':
            if run is not None: raise ValueError('Continuation already configured; never reset receipts')
        else:
            validate(run)
            if action == 'status': return dict(state=state, disposition=run['status'])
            # Duplicate deliveries never authorize an operation, even after restart/termination.
            if action == 'next' and delivery in run['deliveries']:
                return dict(state=state, disposition='duplicate-no-execution', receipt=run['deliveries'][delivery])
            if run['status'] != 'active':
                return dict(state=state, disposition=run['status'] + '-no-execution')
        if type(revision) is not int or revision != state['revision']:
            raise ValueError('Stale revision; read status before writing')
        if action == 'enable':
            if not lifecycle.text(predicate) or not lifecycle.text(grant) or type(limit) is not int or limit < 1:
                raise ValueError('Explicit grant, done predicate and positive operation budget required')
            if any(op['status']=='started' for op in state['operations'].values()):
                raise ValueError('Reconcile phase4 uncertainty before enabling continuation')
            run = dict(schema=1,status='active',predicate=predicate,grant=grant,limit=limit,
                       frozen=grant_context(state),deliveries={})
            state['continuation'] = run
            disposition='enabled'
        elif action == 'cancel':
            if not lifecycle.text(reason): raise ValueError('Cancellation reason required')
            run['status']='cancelled'
            state['context']['next_action']='Stopped by cancellation; inspect any started effects without replay'
            disposition='cancelled-no-execution'
        else:
            if grant_context(state) != run['frozen']:
                raise ValueError('Task goal/authority/scope changed; existing continuation cannot authorize work')
            if action == 'next':
                if not lifecycle.text(delivery): raise ValueError('Stable delivery ID required')
                if any(op['status']=='started' for op in state['operations'].values()):
                    return dict(state=state,disposition='uncertain-no-execution')
                if state['context']['blockers']:
                    return dict(state=state,disposition='blocked-no-execution')
                pending=[key for key,op in state['operations'].items() if op['status']=='pending']
                if not pending: return dict(state=state,disposition='verify-predicate-before-close')
                if len(run['deliveries']) >= run['limit']:
                    state['context']['blockers']=['Continuation operation budget exhausted; work remains incomplete']
                    state['context']['next_action']='Report remaining work and budget limit; preserve this record for an authorized successor'
                    disposition='budget-exhausted-no-execution'
                else:
                    operation=pending[0]
                    state['operations'][operation]['status']='started'
                    run['deliveries'][delivery]=dict(operation=operation,status='issued')
                    disposition='execute-one'
            elif action == 'finish':
                if not isinstance(evidence,list) or not evidence or not all(lifecycle.text(v) for v in evidence):
                    raise ValueError('Observed evidence required')
                receipt=run['deliveries'][delivery]
                op=state['operations'][receipt['operation']]
                if op['status'] != 'started' or receipt['status'] != 'issued':
                    raise ValueError('Already settled or invalid delivery')
                op.update(status='completed',evidence=evidence)
                receipt['status']='settled'
                disposition='settled'
            elif action == 'checkpoint':
                lifecycle.validate_context(context)
                if {key: context[key] for key in FROZEN} != run['frozen'] or not lifecycle.text(reason):
                    raise ValueError('Checkpoint must preserve grant and explain progress/blocker changes')
                state['context']=context
                disposition='checkpointed'
            elif action == 'close':
                if any(op['status']!='completed' for op in state['operations'].values()):
                    raise ValueError('Incomplete or uncertain operations remain')
                if state['context']['blockers'] or not isinstance(evidence,list) or not evidence or not all(lifecycle.text(v) for v in evidence):
                    raise ValueError('Independent done-predicate evidence and no blockers required')
                run.update(status='completed',completion_evidence=evidence)
                state['context']['next_action']='Complete; do not issue further work or wakes'
                disposition='completed-no-execution'
            else:
                raise ValueError('Unknown action')
        state['revision']+=1
        state['history'].append(dict(revision=state['revision'],action='continuation:'+action,
                                     delivery=delivery,evidence=evidence,reason=reason,disposition=disposition))
        lifecycle.save(directory,state)
        result=dict(state=state,disposition=disposition)
        if disposition=='execute-one': result['operation']=run['deliveries'][delivery]['operation']
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['enable','status','next','finish','close','cancel','checkpoint'])
    p.add_argument('workspace');p.add_argument('--task-dir',required=True);p.add_argument('--owner',required=True)
    p.add_argument('--revision',type=int);p.add_argument('--delivery');p.add_argument('--predicate');p.add_argument('--grant')
    p.add_argument('--input');p.add_argument('--limit',type=int);p.add_argument('--reason');p.add_argument('--evidence',action='append')
    a=p.parse_args()
    try:
        print(json.dumps(apply(a.task_dir,a.workspace,a.owner,a.action,a.revision,a.delivery,a.evidence,a.predicate,a.grant,a.limit,a.reason,json.loads(Path(a.input).read_text()) if a.input else None),indent=2))
    except (ValueError,KeyError,TypeError,OSError) as error:
        p.exit(1,str(error)+'\n')


if __name__=='__main__': main()
