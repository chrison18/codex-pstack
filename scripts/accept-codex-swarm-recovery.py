"""Real native Swarm race, evidence-retry/interruption and conflict acceptance.

Faults are applied to actual published artifacts, not declared by model prose. Reports
and raw events remain in temporary projects; automated checks still require manual audit.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import tempfile
import time

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('research', Path(__file__).with_name('accept-codex-research.py'))
research = importlib.util.module_from_spec(spec); spec.loader.exec_module(research)

RACE_STAGES = {'race': ('first-pass', 'rank-all', 'best-of'),
               'race-ties': ('rank-all', 'best-of')}


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), *args], check=True, capture_output=True, text=True).stdout.strip()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp'); temporary.write_text(json.dumps(data, indent=2) + '\n'); temporary.replace(path)


def expected_report(base):
    return {'baseSha': base, 'total': 11, 'checks': [
        {'kind': 'empty', 'result': 0}, {'kind': 'zero', 'result': 0},
        {'kind': 'negative', 'result': 'ValueError'}, {'kind': 'ordinary', 'result': 11}]}


def grade(report, base):
    if not isinstance(report, dict):
        return {'valid': False, 'score': 0}
    reference = expected_report(base)
    valid = report.get('baseSha') == base and report.get('total') == reference['total']
    method = report.get('method', {})
    valid = valid and isinstance(method, dict) and method.get('sampleCount') == 1 and bool(method.get('sampleDefinition')) and bool(method.get('order'))
    commands = report.get('commands', [])
    valid = valid and isinstance(commands, list) and bool(commands) and all(
        isinstance(command, str) and bool(command.strip()) and not re.search(r'\bCOMMAND\b', command) for command in commands)
    checks = report.get('checks', [])
    score = sum(any(isinstance(c, dict) and all(c.get(k) == v for k, v in expected.items()) for c in checks) for expected in reference['checks']) if isinstance(checks, list) else 0
    # Optional correct, unique extra examples distinguish quality among eligible results.
    extras = report.get('extraChecks', [])
    seen = set()
    for example in extras[:2] if isinstance(extras, list) else []:
        try:
            items = example['items']; key = json.dumps(items, sort_keys=True)
            expected = 'ValueError' if any(row['quantity'] < 0 for row in items) else sum(row['price'] * row['quantity'] for row in items)
            if key not in seen and example['result'] == expected:
                seen.add(key)
        except (TypeError, KeyError):
            pass
    return {'valid': bool(valid and score == 4), 'score': score + len(seen)}


def interrupted_running_dropout(events):
    calls = {}
    for event in events:
        if event.get('method') != 'rawResponseItem/completed': continue
        item = event.get('params', {}).get('item', {})
        if item.get('type') == 'function_call' and item.get('name', '').split('.')[-1] == 'interrupt_agent':
            try:
                target = json.loads(item['arguments']).get('target', '')
                if target == 'dropout' or target.endswith('/dropout'): calls[item['call_id']] = True
            except (ValueError, KeyError, TypeError, AttributeError): pass
        elif item.get('type') == 'function_call_output' and item.get('call_id') in calls:
            try:
                if json.loads(item['output']).get('previous_status') == 'running': return True
            except (ValueError, KeyError, TypeError, AttributeError): pass
    return False


def operation(root, args):
    contract = json.loads((root / 'contract.json').read_text()); case = contract['case']
    stage = getattr(args, 'stage', None)
    if args.operation == 'declare':
        assert case in RACE_STAGES and stage in RACE_STAGES[case]
        folder = root / 'cases' / stage
        assert not list(folder.glob('*/receipt-*.json')), 'Declare before any submissions'
        save(folder / 'rule.json', {'rule': stage, 'declaredAtNs': time.time_ns(), 'tieBreak': 'arm id ascending', 'score': 'four mandatory cases plus up to two correct unique extra examples'})
        print('Declared ' + stage); return 0
    if args.operation == 'hold':
        assert case == 'recovery'
        save(root / 'dropout-ready.json', {'pid': os.getpid(), 'atNs': time.time_ns()})
        deadline = time.monotonic() + 180
        while not (root / 'dropout-release').exists() and time.monotonic() < deadline:
            time.sleep(0.1)
        print('Injected delivery stopped; no report artifact was produced')
        return 98
    if args.operation in ('apply-a', 'check-b'):
        assert case == 'conflict'
        arm = 'a' if args.operation == 'apply-a' else 'b'
        patch = subprocess.run(['git', '-C', contract['workers'][arm], 'diff', contract['baseSha'], '--', 'calc.py'], check=True, capture_output=True, text=True).stdout
        command = ['git', '-C', contract['integration'], 'apply']
        if args.operation == 'check-b': command.append('--check')
        result = subprocess.run(command + ['-'], input=patch, capture_output=True, text=True)
        record = {'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'atNs': time.time_ns()}
        save(root / 'reports' / (args.operation + '.json'), record)
        print(json.dumps(record)); return result.returncode
    if args.operation == 'publish':
        arm = args.arm
        if case in RACE_STAGES:
            assert stage in RACE_STAGES[case]
            folder = root / 'cases' / stage / arm
            assert (folder.parent / 'rule.json').exists(), 'No declared rule'
            earlier = ('a' if case == 'race' and stage == 'first-pass' and arm == 'b' else
                       'b' if case == 'race-ties' and arm == 'a' else None)
            if earlier:
                deadline = time.monotonic() + 300
                while not (folder.parent / earlier / 'receipt-1.json').exists():
                    if time.monotonic() > deadline: raise TimeoutError('Earlier arm did not submit')
                    time.sleep(0.1)
                time.sleep(0.1)
        else:
            assert case == 'recovery' and arm in ('healthy', 'once', 'twice')
            folder = root / 'cases' / arm
        proposal = json.loads((folder / 'proposal.json').read_text())
        attempt = len(list(folder.glob('receipt-*.json'))) + 1
        assert attempt <= (1 if case in RACE_STAGES or arm == 'healthy' else 2), 'Retry budget exhausted'
        injected = None
        if case == 'race' and stage == 'first-pass' and arm == 'a':
            proposal['total'] = proposal.get('total', 0) + 1; injected = 'corrupt-total'
        if case == 'race' and ((stage == 'rank-all' and arm == 'a') or (stage == 'best-of' and arm == 'b')):
            proposal.pop('extraChecks', None); injected = 'remove-optional-quality-evidence'
        if case == 'race-ties':
            proposal.pop('extraChecks', None); injected = 'remove-optional-quality-evidence-for-tie'
        if case == 'recovery' and arm == 'once' and attempt == 1:
            proposal.pop('baseSha', None); injected = 'missing-sha'
        if case == 'recovery' and arm == 'twice':
            proposal.pop('method', None); injected = 'missing-method'
        save(folder / ('report-' + str(attempt) + '.json'), proposal)
        save(folder / ('receipt-' + str(attempt) + '.json'), {'atNs': time.time_ns(), 'attempt': attempt, 'injected': injected})
        print(json.dumps({'published': str(folder / ('report-' + str(attempt) + '.json')), 'attempt': attempt}))
        return 0
    if args.operation == 'validate':
        folder = root / 'cases' / stage / args.arm if case in RACE_STAGES else root / 'cases' / args.arm
        files = sorted(folder.glob('report-*.json'))
        result = grade(json.loads(files[-1].read_text()), contract['baseSha']) if files else {'valid': False, 'score': 0}
        print(json.dumps(result)); return 0
    raise ValueError('Unsupported operation')


def prepare(root, case, entry):
    workspace = root / 'workspace'; workspace.mkdir(parents=True)
    git(workspace, 'init', '-q', '-b', 'main')
    (workspace / 'calc.py').write_text('def total(values):\n    return sum(values)\n' if case == 'conflict' else
        'def quote(items):\n    if any(row["quantity"] < 0 for row in items):\n        raise ValueError("negative quantity")\n    return sum(row["price"] * row["quantity"] for row in items)\n')
    (workspace / 'input.json').write_text('[{"price":3,"quantity":2},{"price":5,"quantity":1}]\n')
    git(workspace, 'add', '.')
    git(workspace, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Initialize bounded Swarm fixture')
    base = git(workspace, 'rev-parse', 'HEAD')
    contract = {'case': case, 'workspace': str(workspace), 'baseSha': base}
    if case == 'conflict':
        workers = {}
        for arm in ('a','b'):
            path = root / ('worker-' + arm)
            git(workspace, 'worktree', 'add', '-q', '-b', 'conflict-' + arm, str(path), base)
            workers[arm] = str(path)
        target = root / 'integration'
        git(workspace, 'worktree', 'add', '-q', '-b', 'integration', str(target), base)
        contract.update(workers=workers, integration=str(target))
    link = workspace / '.agents/skills/poteto-mode'; link.parent.mkdir(parents=True); link.symlink_to(entry)
    subprocess.run(['python3','-B',str(entry / 'scripts/runtime.py'),'install',str(workspace)],check=True,capture_output=True)
    stages = RACE_STAGES.get(case, ('healthy','once','twice'))
    for stage in stages:
        if case in RACE_STAGES:
            for arm in ('a','b'): (root / 'cases' / stage / arm).mkdir(parents=True)
        else: (root / 'cases' / stage).mkdir(parents=True)
    (root / 'reports').mkdir()
    save(root / 'contract.json', contract)
    return contract


def common_prompt(root, contract, args, entry):
    helper = 'python3 -B ' + str(Path(__file__).resolve()) + ' --fixture ' + str(root)
    text = ('$poteto-mode Use Swarm. Read the contract at ' + str(root / 'contract.json') + '. '
        'The entry directory is ' + str(entry) + '; resolve every swarm-worker through its scripts/runtime.py before starting. '
        'Observed parent is ' + args.model + '/' + args.effort + ', catalog ' + str(args.catalog.resolve(strict=True)) + '. '
        'Use registered poteto-agent, fork_turns none and explicit resolved model/effort; use Sol/low for arm a or healthy, Luna/medium for others. '
        'Do not change roles, config, Git metadata, HEAD/index, commit, send external messages or clean worktrees. No external services or nested delegation. '
        'Keep checklist in conversation; primary writes consolidated report and summary only under reports. '
        'Reports must cite exact base SHA and the actual method; missing artifact evidence cannot be supplied from the primary\'s knowledge or inline worker prose. '
        'Inspect actual artifacts and command results, not self-reported status. Do not read the harness events.jsonl or home directory. Helper commands are ' + helper + ' --operation NAME [--stage STAGE] [--arm ARM]. ')
    if contract['case'] != 'conflict':
        text += ('The source repository is read-only. Workers may execute its pure quote function using python3 -B, but must not write source/config. '
            'All worker artifacts are outside the repository under cases. Each owns only its assigned stage/arm directory and proposal.json. '
            'The report proposal schema is {baseSha, total, checks:[{kind,result}], method:{sampleCount:1,sampleDefinition,order}, commands:[actual command strings],extraChecks:[{items:[{price,quantity}],result}]}. '
            'total is quote(input.json). checks must evaluate one batch in this order: empty [] -> result; zero [{price:9,quantity:0}]; negative [{price:3,quantity:-1}] -> exception class string; '
            'ordinary input.json. kind labels empty/zero/negative/ordinary. One sample means one full four-case batch, not a timing benchmark. '
            'commands must contain literal runnable commands actually executed, with no COMMAND placeholder; use a separate bounded evaluation command before writing the proposal to avoid self-referential command recording. Validate your proposal before its one allowed initial publication. Include two correct extraChecks examples distinct from each other; these are optional quality evidence, not eligibility requirements. Only the publish helper writes report-N.json and receipt-N.json. Workers author proposal.json then call publish; inspect the published artifact and report truthfully. '
            'Do not bypass faults or repair published reports directly. The helper supplies no answers, but injects the specified fault. '
            'Worker final replies name artifact paths/status; substantive refs/method must be in the published report artifact. ')
    if contract['case'] == 'race':
        text += ('Run three consecutive races first-pass, rank-all, best-of, two independent arms each with IDENTICAL task briefs. Reuse the same two agents via followup_task after draining each stage; do not recursively delegate. '
            'Before any stage submissions call declare --stage STAGE. Eligibility requires four correct mandatory cases, total, exact SHA and method. Score adds one point for each of up to two unique correctly computed extraChecks. The publisher strips optional extras from a in rank-all and b in best-of, leaving valid but lower-scoring artifacts. Tie-break arm id ascending. '
            'In first-pass only, publish corrupts a\'s total and delays b until a submitted, guaranteeing the earliest artifact is invalid. Each arm gets one publish only in each race. '
            'Validate artifacts in submission order with validate. Select first eligible completed submission for first-pass (completion = immutable publish timestamp), '
            'rank every eligible arm for rank-all, and choose one highest-scoring eligible arm for best-of; invalid arms are excluded but reported. Drain both workers every stage. '
            'After each stage write cases/STAGE/selection.json as {rule,selected:[arm ids],drained:[arm ids],invalid:[arm ids]} under primary ownership. '
            'This selection file is the one exception to the primary reports-only path. Do not change the rule after outcomes. Report convergence/ties honestly.')
    elif contract['case'] == 'race-ties':
        text += ('Run two consecutive identical-brief races, rank-all then best-of, with independent arms a and b. Reuse the same two agents via followup_task after draining each stage. '
            'Declare each stage rule before spawning or sending its briefs: call declare --stage STAGE. Eligibility requires four correct mandatory cases, total, exact SHA and method. '
            'The publisher removes optional extraChecks from BOTH arms, so eligible reports tie at score 4; it holds a until b publishes, making b the earlier completed report. '
            'Tie-break is arm id ascending, declared before outcomes. Completion time must not replace this tie-break. One publish per arm per stage; no repair of published reports. '
            'Validate and inspect every published artifact, wait for both terminal results, and drain both workers before advancing. '
            'For rank-all return the complete ordered eligible set; for best-of select one highest-scoring eligible arm using the same tie-break. Do not invent a quality difference. '
            'After each stage write cases/STAGE/selection.json as {rule,selected:[arm ids],drained:[arm ids],invalid:[arm ids]}; this is the one exception to primary reports-only ownership. '
            'Report the actual scores, submission order and declared tie decision, retaining any incomplete/invalid arm as a gap rather than fabricating coverage.')
    elif contract['case'] == 'recovery':
        text += ('Partition into four required slices with exact native task names healthy, once, twice, dropout; do not replace missing coverage. Resolve/start four independent workers. '
            'healthy publishes one full report; once loses baseSha on its first publish and can restore it on the second; twice loses method on both allowed publishes. '
            'Ask the same worker ONCE to republish missing evidence; after a second miss record GAP, no third request or guessed completion. '
            'Start dropout last. It must call hold, keep waiting on any yielded tool session and produce no artifact; it must not return a final reply while its hold is active. When dropout-ready.json appears, immediately use native interrupt_agent on that still-running worker before processing other results; '
            'then primary creates dropout-release so its held helper exits without report. This is a controlled real interruption, not a simulated prose claim. '
            'Do not interrupt healthy workers. Retain partial valid slices and leave whole coverage incomplete. '
            'Write reports/summary.json as {complete:false,statuses:{healthy:"PASS",once:...,twice:...,dropout:...},retries:{once:N,twice:N},gaps:[slice ids]}. '
            'Actual status strings for missing evidence/dropout may be GAP or BLOCKED; never PASS. Drain started workers before the final report.')
    else:
        text += ('Prepare two independent code writers in the precreated workers a/b worktrees, verify branch and exact base before writes. Each owns ONLY its calc.py and runs its own bounded checks with python3 -B. '
            'a adds rejection of negative values (ValueError), preserving total(values) and one-shot iterables. b independently adds optional fee=0 to total(values), preserving keyword calls. '
            'These changes intentionally overlap the same baseline lines. Neither worker reads the other code. Primary waits for both terminal results and reviews actual diffs. '
            'Then primary calls apply-a, followed by check-b. check-b must attempt actual git apply --check; the expected nonzero result is an integration conflict, not permission to discard either requirement. '
            'After seeing that conflict, manually reconcile ONLY integration/calc.py to support both negative rejection and fee, retaining keyword/one-shot calls. '
            'Run combined acceptance independently: empty=0; [2,3] fee4=9; generator(2,3) fee4=9; [-1] raises ValueError; total(values=[2,3],fee=4)=9. '
            'Do not modify workers after completion. reports/summary.json must record conflictObserved and integrationVerified with actual commands; primary workspace remains unchanged.')
    return text


def audit(root, contract, events, thread, status, before, heads, indexes):
    scopes = {'workspace': Path(contract['workspace'])}
    if contract['case'] == 'conflict': scopes.update({**{k:Path(v) for k,v in contract['workers'].items()}, 'integration':Path(contract['integration'])})
    after = {n:snapshot(p) for n,p in scopes.items()}; save(root / 'after.json', after)
    changed = {n:sorted(k for k in set(before[n])|set(after[n]) if before[n].get(k)!=after[n].get(k)) for n in scopes}
    checks = {'scope':all(not paths if n=='workspace' else set(paths)=={'calc.py'} for n,paths in changed.items()),
              'headsAndIndexes':all(git(p,'rev-parse','HEAD')==heads[n] and git(p,'diff','--cached','--binary')==indexes[n] for n,p in scopes.items())}
    try:
        if contract['case'] in RACE_STAGES:
            for stage in RACE_STAGES[contract['case']]:
                folder=root/'cases'/stage; rule=json.loads((folder/'rule.json').read_text())
                submissions=[]
                for arm in ('a','b'):
                    receipt=json.loads((folder/arm/'receipt-1.json').read_text())
                    data=json.loads((folder/arm/'report-1.json').read_text()); g=grade(data,contract['baseSha'])
                    submissions.append((arm,receipt['atNs'],g['valid'],g['score']))
                valid=[x for x in submissions if x[2]]
                expected=([min(valid,key=lambda x:x[1])[0]] if stage=='first-pass' else
                    [x[0] for x in sorted(valid,key=lambda x:(-x[3],x[0]))][:1 if stage=='best-of' else len(valid)])
                selection=json.loads((folder/'selection.json').read_text())
                checks[stage]=selection['rule']==stage and rule['rule']==stage and rule['declaredAtNs']<min(x[1] for x in submissions) and selection['selected']==expected and sorted(selection['drained'])==['a','b'] and sorted(selection['invalid'])==sorted(x[0] for x in submissions if not x[2])
                if contract['case']=='race-ties':
                    checks[stage+'-tied-valid-scores'] = len(valid)==2 and all(x[3]==4 for x in valid)
                    checks[stage+'-reverse-completion'] = submissions[1][1] < submissions[0][1]
                    checks[stage+'-declared-tie-break'] = rule['tieBreak']=='arm id ascending'
                elif stage != 'first-pass': checks[stage+'-score-separation'] = len({x[3] for x in valid}) > 1
                checks[stage+'-single-publish']=all(len(list((folder/a).glob('receipt-*.json')))==1 for a in ('a','b'))
        elif contract['case']=='recovery':
            summary=json.loads((root/'reports/summary.json').read_text()); statuses=summary['statuses']
            checks['boundedRetries']=all(len(list((root/'cases'/a).glob('receipt-*.json')))==n for a,n in [('healthy',1),('once',2),('twice',2)]) and summary['retries']=={'once':1,'twice':1}
            checks['validRecovered']=all(grade(json.loads((root/'cases'/a/filename).read_text()),contract['baseSha'])['valid'] for a,filename in [('healthy','report-1.json'),('once','report-2.json')])
            checks['gapsNotPass']=not summary['complete'] and statuses['healthy']==statuses['once']=='PASS' and all(statuses[a] in ('GAP','BLOCKED') for a in ('twice','dropout')) and sorted(summary['gaps'])==['dropout','twice']
            checks['runningDropoutInterrupted']=interrupted_running_dropout(events)
            checks['dropoutNoArtifact']=json.loads((root/'cleanup.json').read_text())['releaseExistedBeforeCleanup'] and (root/'dropout-ready.json').exists() and (root/'dropout-release').exists() and not (root/'cases/dropout').exists()
        else:
            conflict=json.loads((root/'reports/check-b.json').read_text())
            checks['realConflict']=conflict['exitCode']!=0 and 'patch' in conflict['stderr'].lower()
            target=Path(contract['integration'])
            code='from calc import total\nassert total([])==0\nassert total([2,3],fee=4)==9\nassert total(iter([2,3]),fee=4)==9\nassert total(values=[2,3],fee=4)==9\ntry:\n total([-1])\nexcept ValueError: pass\nelse: raise AssertionError("negative accepted")\nprint("conflict integration passed")\n'
            p=subprocess.run(['python3','-B','-c',code],cwd=target,capture_output=True,text=True)
            save(root/'verification.json',{'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
            checks['combinedVerification']=p.returncode==0
    except (OSError,ValueError,KeyError,TypeError,IndexError): checks['evidenceComplete']=False
    summary,final=research.summarize_events(events,thread); (root/'final.txt').write_text(final)
    result={'case':contract['case'],'status':status,'changed':changed,'checks':checks,**summary,'artifactChecksPassed':status=='completed' and all(checks.values())}
    save(root/'result.json',result); return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path); parser.add_argument('--operation',choices=('declare','publish','validate','hold','apply-a','check-b'))
    parser.add_argument('--stage'); parser.add_argument('--arm')
    parser.add_argument('--case',choices=('race','race-ties','recovery','conflict')); parser.add_argument('--codex',default='codex')
    parser.add_argument('--model'); parser.add_argument('--effort'); parser.add_argument('--catalog',type=Path)
    parser.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    args=parser.parse_args()
    if args.operation: return operation(args.fixture.resolve(strict=True),args)
    if not all((args.case,args.model,args.effort,args.catalog)): parser.error('case/model/effort/catalog required')
    root=Path(tempfile.mkdtemp(prefix='pstack-swarm-'+args.case+'-')).resolve(); print(json.dumps({'evidenceDirectory':str(root)}),flush=True)
    entry=Path(__file__).resolve().parent.parent/'plugins/pstack/skills/poteto-mode'; contract=prepare(root,args.case,entry)
    workspace=Path(contract['workspace']); home=root/'home'; home.mkdir()
    (home/'config.toml').write_text('[projects.'+json.dumps(str(workspace))+']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n[sandbox_workspace_write]\nwritable_roots=['+json.dumps(str(root))+']\n')
    scopes={'workspace':workspace}
    if args.case=='conflict':scopes.update({**{k:Path(v) for k,v in contract['workers'].items()},'integration':Path(contract['integration'])})
    before={n:snapshot(p) for n,p in scopes.items()}; heads={n:git(p,'rev-parse','HEAD') for n,p in scopes.items()}; indexes={n:git(p,'diff','--cached','--binary') for n,p in scopes.items()}; save(root/'before.json',before)
    prompt=common_prompt(root,contract,args,entry); (root/'prompt.txt').write_text(prompt)
    auth=home/'auth.json'; auth.symlink_to(args.auth_file.resolve(strict=True)); client=None; thread=None; status='error'
    try:
        client=research.Client(args.codex,workspace,home,root)
        thread,status=client.run(workspace,args.model,args.effort,prompt,sandbox='workspace-write',timeout_seconds=1800)
    except (RuntimeError,queue.Empty,TimeoutError,KeyboardInterrupt) as error:(root/'harness-error.txt').write_text(str(error))
    finally:
        save(root/'cleanup.json', {'releaseExistedBeforeCleanup': (root/'dropout-release').exists()})
        (root/'dropout-release').touch()
        if client:client.close()
        auth.unlink(missing_ok=True)
    result=audit(root,contract,client.events if client else [],thread,status,before,heads,indexes)
    print(json.dumps(result),flush=True)
    return 0 if result['artifactChecksPassed'] else 1


if __name__=='__main__': raise SystemExit(main())
