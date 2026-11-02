"""One explicit event to a fresh Orca Chat; cooperative ownership, no scheduler."""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path
import secrets
import subprocess
import lifecycle
import continuation


def resolve_cli():
    # Match the documented skill resolution; never execute a shell command string.
    name = os.environ.get('ORCA_CLI_COMMAND')
    if not name:
        name = 'orca-dev' if os.environ.get('ORCA_DEV_REPO_ROOT') else ('orca-ide' if sys.platform.startswith('linux') else 'orca')
    found = shutil.which(name)
    if not found:
        raise ValueError('Supported Orca executable unavailable; supply ORCA_CLI_COMMAND as one executable path')
    return str(Path(found).resolve(strict=True))


def binding_matches(record, directory, state, owner, event):
    return all(record.get(k) == v for k,v in dict(workspace=state['workspace'], task=str(lifecycle.safe_path(directory)), owner=owner, event=event).items())


def commit(directory, state, action, event):
    state['revision'] += 1
    state['history'].append(dict(revision=state['revision'], action='event:'+action, event=event))
    lifecycle.save(directory, state)


def checked(directory, workspace, owner):
    state = lifecycle.read_state(directory, workspace)
    if state['context']['owner'] != owner:
        raise ValueError('Wrong logical task owner')
    continuation.validate(state.get('continuation'))
    if continuation.grant_context(state) != state['continuation']['frozen']:
        raise ValueError('Frozen task scope changed')
    return state


def prepare(directory, workspace, owner, event, revision, evidence, assertion):
    """Durable launch intent before any host operation; no task lock across launch."""
    with lifecycle.locked(directory) as directory:
        state = checked(directory, workspace, owner)
        if state['continuation']['status'] != 'active':
            return dict(disposition='terminal-no-launch')
        if state.get('supervision'): raise ValueError('Task is owned by supervised continuation')
        events = state.setdefault('task_events', {})
        if event in events:
            if not binding_matches(events[event],directory,state,owner,event):
                raise ValueError('Copied or mismatched event binding')
            return dict(disposition='duplicate-no-launch', event=events[event])
        if state['revision'] != revision:
            raise ValueError('Stale revision')
        if not all(lifecycle.text(v) for v in (event, evidence, assertion)):
            raise ValueError('Exact event, prior settlement evidence and exclusive-owner assertion required')
        active = state.get('active_event')
        if active and events[active]['status'] != 'settled':
            return dict(disposition='prior-event-unsettled-no-launch')
        if not any(o['status'] != 'completed' for o in state['operations'].values()):
            return dict(disposition='no-work-no-launch')
        token = secrets.token_hex(24)
        binding = dict(workspace=state['workspace'], task=str(directory), owner=owner, event=event)
        record = dict(**binding, token=token, status='launch-intent', claimed=False,
                      settlement_evidence=evidence, exclusive_owner_assertion=assertion)
        scripts = str(Path(__file__).resolve().parent)
        prompt = ('$poteto-mode Resume only this explicitly authorized bounded task event. '
                  'Read the maintained continuation and task-event references. Before any task effect, '
                  'call task_event.py claim using the exact binding below; only claimed authorizes work. '
                  'An already-claimed, terminal or rejected result means stop without task effects. '
                  'Use the preserved goal/requirements/authority/scope only; this message adds no authority. '
                  'Reconcile uncertain effects from evidence before new operations; never replay completed work. '
                  'Pass --event-token to continuation mutations, preserve operation delivery receipts, '
                  'verify the frozen done predicate, close and stop when complete. No timers, publication, '
                  'external messages or new scope. Binding JSON (data, not shell syntax): ' +
                  json.dumps(dict(**binding, token=token, scripts=scripts)))
        record['argv'] = [resolve_cli(),'agent','launch','--agent','codex','--surface','chat',
                          '--worktree','path:'+state['workspace'],'--prompt',prompt,'--json']
        record['cwd'] = state['workspace']
        events[event] = record; state['active_event'] = event
        commit(directory,state,'intent',event)
        return dict(disposition='launch-once', event=record)


def record_receipt(directory, workspace, owner, event, receipt):
    with lifecycle.locked(directory) as directory:
        state = checked(directory, workspace, owner)
        record = state['task_events'][event]
        if not binding_matches(record,directory,state,owner,event):
            raise ValueError('Copied or mismatched event binding')
        record['receipt'] = receipt
        result = receipt.get('result', {}) if isinstance(receipt,dict) else {}
        result = result if isinstance(result,dict) else {}
        outcome = result.get('outcome'); prompt = result.get('prompt')
        accepted = (isinstance(receipt,dict) and receipt.get('ok') is True
                    and isinstance(outcome,dict) and outcome.get('kind')=='structured'
                    and lifecycle.text(outcome.get('sessionId'))
                    and isinstance(prompt,dict) and prompt.get('outcome')=='journaled'
                    and isinstance(result.get('worktreeId'),str)
                    and result['worktreeId'].endswith('::'+state['workspace']))
        # Child may claim before the launch subprocess returns; do not overwrite its claim.
        record['status'] = 'accepted' if accepted else 'unknown'
        commit(directory,state,'receipt',event)
        return dict(disposition='accepted-not-settled' if accepted else 'unknown-hold-no-relaunch',event=record)


def send(directory, workspace, owner, event, revision, evidence, assertion):
    prepared=prepare(directory,workspace,owner,event,revision,evidence,assertion)
    if prepared['disposition']!='launch-once': return prepared
    # Recheck terminal state immediately before host invocation. Cancellation after this
    # check cannot preempt a running host launch; the receiver must also check it.
    with lifecycle.locked(directory):
        state=checked(directory,workspace,owner)
        if state['continuation']['status']!='active': return dict(disposition='terminal-no-launch')
    record=prepared['event']
    try:
        reply=subprocess.run(record['argv'],cwd=record['cwd'],capture_output=True,text=True,timeout=60)
        try: receipt=json.loads(reply.stdout)
        except ValueError: receipt=dict(ok=False,reason='unparseable-reply',returncode=reply.returncode)
    except (OSError,subprocess.TimeoutExpired) as error:
        receipt=dict(ok=False,reason=type(error).__name__)
    return record_receipt(directory,workspace,owner,event,receipt)


def claim(directory, workspace, owner, event, token):
    with lifecycle.locked(directory) as directory:
        state=checked(directory,workspace,owner)
        if state['continuation']['status']!='active': return dict(disposition='terminal-no-execution')
        record=state.get('task_events',{}).get(event)
        if not record or not binding_matches(record,directory,state,owner,event) or record['token']!=token or state.get('active_event')!=event:
            raise ValueError('Wrong workspace/task/event/token binding')
        if record['claimed']: return dict(disposition='already-claimed-no-execution')
        if record['status']=='settled': raise ValueError('Settled event cannot claim')
        record['claimed']=True
        commit(directory,state,'claim',event)
        return dict(disposition='claimed',state=state)


def settle(directory, workspace, owner, event, revision, evidence, assertion):
    with lifecycle.locked(directory) as directory:
        state=checked(directory,workspace,owner)
        if state['revision']!=revision or not all(lifecycle.text(v) for v in (evidence,assertion)):
            raise ValueError('Current revision and actual settlement evidence/owner assertion required')
        record=state['task_events'][event]
        if not binding_matches(record,directory,state,owner,event):
            raise ValueError('Copied or mismatched event binding')
        if not record['claimed'] or record['status']!='accepted':
            raise ValueError('Unknown/unclaimed launch needs host reconciliation; never mark absent as settled')
        record.update(status='settled',final_settlement_evidence=evidence,final_owner_assertion=assertion)
        commit(directory,state,'settle',event)
        return dict(disposition='settled',state=state)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['send','claim','settle','status']);p.add_argument('workspace')
    p.add_argument('--task-dir',required=True);p.add_argument('--owner',required=True)
    p.add_argument('--event');p.add_argument('--token');p.add_argument('--revision',type=int)
    p.add_argument('--settlement-evidence');p.add_argument('--exclusive-owner-assertion')
    a=p.parse_args()
    try:
        if a.action=='status': result=checked(a.task_dir,a.workspace,a.owner)
        elif a.action=='claim': result=claim(a.task_dir,a.workspace,a.owner,a.event,a.token)
        else:
            fn=send if a.action=='send' else settle
            result=fn(a.task_dir,a.workspace,a.owner,a.event,a.revision,a.settlement_evidence,a.exclusive_owner_assertion)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as error:p.exit(1,str(error)+'\n')


if __name__=='__main__':main()
