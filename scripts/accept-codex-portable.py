"""Native forward tests for portable 3B routes. Audit raw events as well as artifacts.

Fixtures and auth references are disposable; captured proof remains local. No desktop
Codex automation, remote PR writes, external service calls or repository edits occur.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import time

from codex_acceptance_state import snapshot

spec = importlib.util.spec_from_file_location('research', Path(__file__).with_name('accept-codex-research.py'))
research = importlib.util.module_from_spec(spec)
spec.loader.exec_module(research)

CASES = ('delivery', 'writing', 'teach', 'quality', 'verification', 'formal', 'refactoring', 'prototype', 'measurement', 'planning', 'evaluation', 'visual')


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def git(workspace, *args):
    return subprocess.run(['git', '-C', str(workspace), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit(workspace, message):
    git(workspace, 'add', '.')
    git(workspace, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', message)


def prepare(workspace, case, outputs, node_modules):
    def write(name, text):
        path = workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    write('README.md', 'Harbor is a local fixture. No remote services, credentials or install steps are needed.\n')
    git(workspace, 'init', '-q', '-b', 'main')
    if case in ('writing', 'teach', 'planning', 'evaluation'):
        write('app.py', 'def page_size(value):\n    if not isinstance(value, int) or isinstance(value, bool) or value < 1 or value > 100:\n        raise ValueError("page size must be an integer from 1 to 100")\n    return value\n')
        write('README.md', 'Harbor accepts page sizes 1 through 100. Invalid sizes raise ValueError.\n')
        write('draft.md', 'It is important to note that Harbor leverages a pivotal validation paradigm. Additionally, users can pass any positive integer, including 500. This is not just a feature, but a game changer.\n')
    elif case == 'quality':
        write('app.ts', 'export function total(rows: { price: number; quantity: number }[]): number {\n  // Copyright Fixture authors.\n  return rows.reduce((sum, row) => sum + row.price * (row.quantity || 1), 0);\n}\n')
        write('consumer.ts', 'import { total } from "./app";\nexport const invoice = (price: number, quantity: number) => total([{ price, quantity }]);\n')
        write('check.ts', 'import { invoice } from "./consumer";\nif (invoice(9, 0) !== 0) throw new Error("zero quantity must charge zero");\nif (invoice(3, 2) !== 6) throw new Error("ordinary quantity changed");\nif (invoice(3, -1) !== -3) throw new Error("signed adjustment changed");\nconsole.log("quality acceptance passed");\n')
        commit(workspace, 'First zero-quantity regression: truthy fallback loses valid zero')
        write('app.ts', (workspace/'app.ts').read_text().replace('(row.quantity || 1)', 'row.quantity'))
        commit(workspace, 'Restore zero quantity; remove invalid default')
        write('app.ts', (workspace/'app.ts').read_text().replace('row.price * row.quantity', 'row.price * (row.quantity || 1)'))
    elif case == 'verification':
        write('app.py', '''import sys

def execute(line):
    words = line.split()
    if words and words[0] == 'greet': return 'Hello ' + ' '.join(words[1:])
    if words and words[0] == 'sum': return str(sum(int(x) for x in words[1:]))
    return 'Unknown command'

if __name__ == '__main__':
    print('Harbor ready', flush=True)
    for line in sys.stdin:
        if line.strip() == 'quit': break
        print(execute(line), flush=True)
''')
        write('drive.py', '''import argparse,errno,json,os,pty,select,subprocess,sys,time
p=argparse.ArgumentParser();p.add_argument('--command',required=True);p.add_argument('--output',required=True);a=p.parse_args()
master,slave=pty.openpty();child=subprocess.Popen([sys.executable,'-B','app.py'],stdin=slave,stdout=slave,stderr=slave);os.close(slave)
buffer=b''
try:
 deadline=time.monotonic()+10
 while b'Harbor ready' not in buffer:
  if time.monotonic()>deadline: raise TimeoutError('not ready')
  if select.select([master],[],[],.1)[0]: buffer+=os.read(master,4096)
 os.write(master,(a.command+'\\nquit\\n').encode())
 while time.monotonic()<deadline:
  if select.select([master],[],[],.1)[0]:
   try: data=os.read(master,4096)
   except OSError as error:
    if error.errno==errno.EIO: break
    raise
   if not data: break
   buffer+=data
  elif child.poll() is not None: break
 child.wait(timeout=3)
 from pathlib import Path
 Path(a.output).write_text(json.dumps({'command':a.command,'transcript':buffer.decode(errors='replace'),'exitCode':child.returncode},indent=2))
 print(buffer.decode(errors='replace'));sys.exit(child.returncode)
finally:
 if child.poll() is None: child.terminate();child.wait(timeout=3)
 os.close(master)
''')
        write('README.md', 'Run python3 -B app.py in a terminal. Commands: greet NAME, sum INTEGER..., quit. It announces Harbor ready. Existing PTY harness: python3 -B drive.py --command "greet Ada" --output /absolute/proof.json. No server or dependency install needed. Commands greet and sum are the two user features.\n')
    elif case == 'formal':
        write('slots.py', 'LIMIT = 3\n\ndef reserve(used):\n    return used + 1 if used < LIMIT else used\n\ndef release(used):\n    return used - 1 if used > 0 else used\n')
        write('README.md', 'Harbor has three slots. State used is an integer from 0 to 3. reserve acquires one unless full; release returns one unless empty. Public inputs are only valid states. Verify all valid states and operation sequences up to length 4 on real code; no installed SMT/proof tool is required. This finite bounded check does not prove an arbitrary concurrent system.\n')
    elif case in ('refactoring','measurement'):
        write('app.py', 'def unique(values):\n    result = []\n    for value in values:\n        found = False\n        for previous in result:\n            if previous == value:\n                found = True\n                break\n        if not found:\n            result.append(value)\n    return result\n')
        write('check.py', 'from app import unique\nassert unique([])==[]\nassert unique([3,1,3,2,1])==[3,1,2]\nassert unique([-1,0,-1])==[-1,0]\nassert unique(iter([3,1,3]))==[3,1]\nprint("unique acceptance passed")\n')
        write('measure.py', '''import argparse,json,sys
from pathlib import Path
import app
p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=80);a=p.parse_args()
rows=list(range(a.size));events=0
source=str(Path('app.py').resolve())
def trace(frame,event,arg):
 global events
 if event=='line' and frame.f_code.co_filename==source: events+=1
 return trace
sys.settrace(trace)
try: result=app.unique(rows)
finally: sys.settrace(None)
assert result==rows
print(json.dumps({'metric':'executed Python lines in app.py including nested frames','size':a.size,'value':events,'errors':0,'work':len(result)}))
''')
        write('README.md', 'unique preserves first occurrence order for integers, including zero/negative values and one-shot iterables. check.py is the regression gate. measure.py counts real Python line events in app.py, including generator/comprehension/local helper frames, on distinct integers; it does not measure wall time or internal C operations. Use --size 40 or 80. Keep both files unchanged.\n')
    elif case == 'prototype':
        write('README.md', 'Choose a readable error format for a CLI receiving invalid page size 500. Required facts: supplied value 500, valid range 1..100, no automatic correction. This request chooses a format, not production behavior.\n')
    elif case == 'visual':
        html='<!doctype html><html><head><meta charset="utf-8"><style>body{margin:24px;font-family:Arial}button{font-size:18px}output{margin-left:12px}</style></head><body><h1>Harbor</h1><button>Add</button><output>0</output>SCRIPT</body></html>'
        js="document.querySelector('button').onclick=()=>{const out=document.querySelector('output');out.value=String(Number(out.value)+1)}"
        write('before.html',html.replace('SCRIPT','<script>'+js+'</script>'))
        write('after.html',html.replace('SCRIPT','<script src="counter.js"></script>'))
        write('counter.js',js+'\n')
        write('drive.cjs', '''const fs=require('fs');const path=require('path');const {pathToFileURL}=require('url');const {chromium}=require('playwright');
(async()=>{const mode=process.argv[2],out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true});
try{for(const name of mode==='baseline'?['before']:['after']){const page=await browser.newPage({viewport:{width:480,height:240},deviceScaleFactor:1});await page.goto(pathToFileURL(path.resolve(name+'.html')).href);await page.getByRole('heading',{name:'Harbor'}).waitFor();for(let n=0;n<3;n++){if(n)await page.getByRole('button',{name:'Add',exact:true}).click();if(await page.locator('output').textContent()!==String(n))throw Error('counter behavior');await page.screenshot({path:path.join(out,name+'-'+n+'.png')});}await page.close();}
if(mode==='check'){for(let n=0;n<3;n++){if(!fs.readFileSync(path.join(out,'before-'+n+'.png')).equals(fs.readFileSync(path.join(out,'after-'+n+'.png'))))throw Error('nonzero image diff '+n);}fs.writeFileSync(path.join(out,'comparison.json'),JSON.stringify({states:3,diffBytes:0}));}console.log(mode+' passed');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
''')
        write('README.md', 'Static Harbor counter: before.html inline script; after.html/counter.js extracted equivalent script. Existing browser harness drive.cjs uses local installed Playwright. Run node drive.cjs baseline ABSOLUTE_ARTIFACT_DIR, then node drive.cjs check SAME_DIR. Baseline images and source/harness are immutable. This is a web fixture, not Codex desktop UI.\n')
    commit(workspace, 'Initialize ' + case + ' fixture and actual contract')


def task(case, workspace, outputs):
    where = ' Write evidence/artifacts only under ' + str(outputs) + '. Keep the checklist in conversation. '
    tasks = {
        'delivery': 'Use Opening a PR to prepare a concise local draft title/body for the observed diff. The user requires draft status and has not authorized commit, push, remote PR edits, ready conversion or merge. Inspect branch/state, keep unrelated source unchanged, identify which delivery steps must remain blocked and save only artifacts/pr.md plus artifacts/delivery.md. No role/delegate is needed to review an unchanged preparation fixture; preserve that skip reason. Read Technical writing and Unslop; do not claim actual forge or CI results.',
        'writing': 'Use the writing/help routes. Rewrite draft.md as a short accurate how-to in artifacts/guide.md using app.py as the source. Do not edit the source draft. Apply Technical writing and Unslop. In artifacts/communication.md restate the user goal in your own words, sharpen "make Harbor docs better" into a deeper but bounded prompt leaving product choices open, restate that prompt plainly with Bro, and give a Ketchup update using only this chat state (no invented PRs/decisions). Finally answer how to start pstack for this repo without installing/configuring or starting implementation. Read the respective leaves; no delegation needed for these prose tasks.',
        'teach': 'Teach how page_size works and why its upper bound exists. Source/Git only; exclude other Why source categories explicitly and preserve confidence: a bound in code alone is not intent. Use How and narrow Why native delegates with read-only assignments; no nested delegation. Deliver the short explanation plus a cited scratch evidence report; no code changes.',
        'quality': 'Bug fix: invoice(9,0) must return 0, not 9; ordinary quantities and signed adjustments must remain unchanged. Use TDD for a cheap regression before changing app.ts; use TypeScript practices, Deslop and No comments within app.ts/check.ts only. Read current history with Correct: the same zero-default mistake has occurred twice; choose the highest useful enforcement and demonstrate the regression check catches the actual past broken expression. Use Blast radius to check consumer.ts through real execution, not just grep. Delegate implementation; only one writer at a time. Do not edit consumer.ts or configuration. No product scope expansion, commits or PR operations.',
        'verification': 'Author a project verification skill for Harbor using Create verification skill and the authoring playbook, reusing the actual PTY harness. The explicitly requested generated skill location is verification-skills/verify-harbor/ (ordinary writable candidate path, not native discovery). Generate that directory with a two-feature map for greeting and sum, real commands, doctor/evidence/cleanup, and prove it by driving a mapped feature. Preserve proof after cleanup. No product/harness/config changes. Do not add dependencies or post a PR.',
        'formal': 'Create a project-local bounded property verification skill for slots.py. Read Create formal verification skill. Execute the real code across every valid state and operation sequences up to length 4, assert 0<=used<=3, and demonstrate sensitivity on a scratch broken copy of the actual product code. Do not alter product code or weaken the contract. Record bounds, assumptions, actual covered symbols and sync commit; avoid claiming an unbounded formal proof from enumeration. Prove the generated skill and leave runnable commands under the explicitly requested ordinary writable candidate path verification-skills/verify-slots/; this tests generation rather than native discovery. No tool installation or PR.',
        'refactoring': 'Use Refactoring. Simplify the local unique function while preserving the README contract exactly. First capture executable characterization evidence against the unmodified function, including one-shot input. Do not change check.py, measure.py or README. Keep the public unique(values) signature and do not split modules or expand APIs; Architect exploration is unnecessary for a single local implementation; How still requires one read-only native explainer through its existing role/model contract. Delegate the scoped mechanical change to poteto-agent, then independently replay old/new behavior, review and report reader-load change. Only app.py may change.',
        'prototype': 'Use Prototype to choose an error-message format for invalid page size 500. Read README.md for the decision brief and its required factual constraints; preserve those facts in every variant. Make two labeled throwaway CLI text alternatives in scratch, actually run them, compare readability and preserved facts, recommend one. This is a behavioral/text decision, so terminal output is the matching surface; no screenshot is needed. Do not implement a production feature or write a test suite.',
        'measurement': 'Use Perf issue then bounded in-session Hillclimb on unique. Metric: executed Python line events across app.py including nested frames at size 80 from unchanged measure.py (not wall time or total CPU work). Target at least 50% fewer events with a minimum of two hypothesis attempts; preserve check.py. Ground with How, run contrasting size40/80, profile separately, apply Benchmark checklist before freezing the harness. Alternate baseline/treatment at least five times per side using scratch copies; keep errors/work counts and median/range. Never present interpreter line counts as elapsed-time speedup. Delegate scoped app.py attempts, verify each before the next, keep/revert by the frozen metric and regression gate. Stop within three attempts and report unmet target honestly. Only app.py may change; log every attempt in scratch, no commits/PR/scheduler.',
        'planning': 'Use Multi-phase plan and Figure it out to produce only a manual implementation plan for adding configurable page size across app.py, consumer.py, config.py and docs/usage.md. These latter three files are proposed future files, explicitly distinguish them from observed paths. Preserve existing page_size behavior, no open product choice or empirical unknown needs a prototype now. State dependencies, ownership, concrete unit/live predicates, applicable perf or reason for skip, review and merge approval gates. Write artifacts/plan.md. Do not implement, spawn owners, create branches/PRs, arm timers, claim runs or use the inherited autonomous checker.',
        'evaluation': 'Use the Eval playbook for two documentation approaches. Prepare two sanitized independent project directories named harbor and meadow outside the source repo, each with only page_size source and a style note; variants are terse reference versus task-focused guide. Use sanitized sibling directories under ' + str(outputs.parent.parent / 'projects') + ' (outside the parent case directory). Candidate-visible paths/prompts/files must not disclose experiment, rubric, peer or model identities; give the same organic request to write a short page-size guide. Use independent native default agents fork_turns none so orchestration instructions do not leak through the Poteto role. Resolve both arena-runner settings before any spawn (Sol/low and Luna/medium). After both finish, one read-only poteto-agent judge receives sanitized labels, outputs and a predeclared private rubric, not model labels. Judge choice Luna/medium is explicitly permitted even though different-family coverage is unavailable; disclose this limit. Primary reads both outputs and reconciles rubric results. Do not claim unobservable child reads passed. No product edits or promotion.',
        'visual': 'Use Control UI and Visual parity to verify the provided inline/extracted counter implementations. This task is verification only: no source migration or code writer needed. Read the actual existing drive.cjs harness. Capture baseline screenshots before candidate driving, keep baseline immutable, drive the real browser button across all three states with the harness, then compare actual PNG bytes. Source, harness and baseline must not be edited to force a pass. Save proofs in scratch and report exactly which surface ran. Never call this Codex desktop acceptance. No PR, browser debugging attachment to user apps or scheduling.'
    }
    return tasks[case].replace('artifacts/', str(outputs) + '/') + where


def next_turn(client, thread, effort, prompt):
    client.rpc('turn/start', {'threadId':thread,'effort':effort,'input':[{'type':'text','text':prompt}]})
    deadline = time.monotonic() + 1800
    while True:
        event = client.receive(deadline)
        if event.get('method')=='turn/completed' and event.get('params',{}).get('threadId')==thread:
            return event['params']['turn']['status']


def allowed(case, name):
    if case=='quality': return name in ('app.ts','check.ts')
    if case in ('refactoring','measurement'): return name=='app.py'
    if case in ('verification','formal'):
        target='verification-skills/verify-'+('harbor' if case=='verification' else 'slots')
        return name in ('verification-skills',target) or name.startswith(target+'/')
    return False


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=CASES,required=True)
    p.add_argument('--codex',default='codex');p.add_argument('--model',required=True);p.add_argument('--effort',required=True)
    p.add_argument('--catalog',type=Path,required=True);p.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    p.add_argument('--node-modules',type=Path,required=True)
    p.add_argument('--tool-path',type=Path,action='append',default=[])
    a=p.parse_args()
    root=Path(tempfile.mkdtemp(prefix='pstack-portable-live-')).resolve();logs=root/a.case;logs.mkdir();workspace=logs/'harbor';workspace.mkdir();outputs=logs/'artifacts';outputs.mkdir();home=logs/'home';home.mkdir()
    print(json.dumps({'evidenceDirectory':str(logs)}),flush=True)
    prepare(workspace,a.case,outputs,a.node_modules)
    entry=Path(__file__).resolve().parent.parent/'plugins/pstack/skills/poteto-mode'
    link=workspace/'.agents/skills/poteto-mode';link.parent.mkdir(parents=True);link.symlink_to(entry)
    subprocess.run(['python3','-B',str(entry/'scripts/runtime.py'),'install',str(workspace)],check=True,capture_output=True)
    (home/'config.toml').write_text('[projects.'+json.dumps(str(workspace))+']\ntrust_level="trusted"\n[agents]\ndefault_subagent_model="gpt-6-luna"\ndefault_subagent_reasoning_effort="high"\n[sandbox_workspace_write]\nwritable_roots=['+json.dumps(str(root))+']\n'+('network_access=true\n' if a.case=='visual' else ''))
    prompt=('$poteto-mode '+task(a.case,workspace,outputs)+' The entry is '+str(entry)+'. Read the relevant workflow index/references. Observed parent '+a.model+'/'+a.effort+'; use --catalog '+str(a.catalog.resolve(strict=True))+' for every required model resolution. Registered roles are already installed. Generic implementation workers use swarm-worker; How/Why/comment/judge keep their named role keys. Explicit worker model gpt-6.1-sol/low unless this request says otherwise. Pass resolved model/effort and fork_turns none to native spawn. No nested delegation by children. No role installation, preferences/config changes, external services/messages, commits, PRs, merges, scheduling or reading private chat stores. Do not read the acceptance-driver file '+str(Path(__file__).resolve())+', its home/auth or raw events.jsonl. This does not prohibit reading the project-owned measure.py, drive.py or drive.cjs; inspect those when the selected workflow requires it. Use only task-owned artifacts. This is native backend acceptance, not desktop UI proof.')
    (logs/'prompt.txt').write_text(prompt)
    before=snapshot(workspace);head=git(workspace,'rev-parse','HEAD');index=git(workspace,'diff','--cached','--binary');save(logs/'before.json',before)
    for name in ('app.py','app.ts','slots.py'):
        if (workspace/name).exists(): (logs/('baseline-'+name)).write_bytes((workspace/name).read_bytes())
    auth=home/'auth.json';client=None;thread=None;status='error';turns=[]
    previous_env={k:os.environ.get(k) for k in ('NODE_PATH','PATH')}
    try:
        auth.symlink_to(a.auth_file.resolve(strict=True))
        os.environ['NODE_PATH']=str(a.node_modules.resolve(strict=True))
        os.environ['PATH']=os.pathsep.join([str(path.resolve(strict=True)) for path in a.tool_path]+[os.environ['PATH']])
        client=research.Client(a.codex,workspace,home,logs)
        thread,status=client.run(workspace,a.model,a.effort,prompt,sandbox='workspace-write',timeout_seconds=1800);turns.append(status)
        if status=='completed' and a.case in ('verification','formal'):
            first=snapshot(workspace);save(logs/'first-after.json',first)
            save(logs/'first-head-index.json',{'unchanged':git(workspace,'rev-parse','HEAD')==head and git(workspace,'diff','--cached','--binary')==index})
            if a.case=='verification':
                source=workspace/'app.py';source.write_text(source.read_text().replace("== 'greet'","== 'hello'"));readme=workspace/'README.md';readme.write_text(readme.read_text().replace('greet','hello'))
                follow='The greeting command was intentionally renamed from greet to hello in app.py/README. Use Maintain verification skill to bring the generated skill/map back in sync. Source and live coverage must include both greeting and sum, with read-only source readers and one coordinator owning all PTY driving. Do not modify app.py, drive.py or README; only verification-skills/verify-harbor/ may change; this remains an explicitly located candidate, not native discovery. Exercise both real features and retain proof after cleanup. No PR or product fix; delivery is local changed/clean/blocked with evidence.'
            else:
                source=workspace/'slots.py';source.write_text(source.read_text().replace('def reserve(', 'def claim('));readme=workspace/'README.md';readme.write_text(readme.read_text().replace('reserve','claim'))
                follow='The API was intentionally renamed reserve to claim with the same slot contract. Use Maintain formal verification skill to read the actual covered-code commits and update only verification-skills/verify-slots/, not slots.py or README. Run the old check first, classify drift separately from a product bug, preserve bounds/property, show the updated check still catches a scratch broken real-code variant, restore scratch state and record the actual checked sync commit. No PR or product edit.'
            # Only the harness stages the intentional API change, separately from generated skills.
            git(workspace,'add',source.name,'README.md');git(workspace,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','Rename public command without changing the documented contract')
            head=git(workspace,'rev-parse','HEAD');index=git(workspace,'diff','--cached','--binary');before=snapshot(workspace);save(logs/'maintenance-before.json',before)
            (logs/'followup.txt').write_text(follow)
            status=next_turn(client,thread,a.effort,follow+' Keep the original scope/model/evidence restrictions; scratch evidence belongs under '+str(outputs)+'.');turns.append(status)
    except (RuntimeError,queue.Empty,TimeoutError,KeyboardInterrupt) as error:
        status='error'
        (logs/'harness-error.txt').write_text(str(error))
    finally:
        try:
            if client:client.close()
        finally:
            try:
                auth.unlink(missing_ok=True)
            finally:
                for key,value in previous_env.items():
                    if value is None:os.environ.pop(key,None)
                    else:os.environ[key]=value
    after=snapshot(workspace);save(logs/'after.json',after);changed=[n for n in set(before)|set(after) if before.get(n)!=after.get(n)]
    first_bad=[]
    if (logs/'first-after.json').exists():
        first=json.loads((logs/'first-after.json').read_text());original=json.loads((logs/'before.json').read_text());first_bad=[n for n in set(original)|set(first) if original.get(n)!=first.get(n) and not allowed(a.case,n)]
    unexpected=sorted(n for n in changed if not allowed(a.case,n))+first_bad
    events=client.events if client else [];summary,final=research.summarize_events(events,thread);(logs/'final.txt').write_text(final)
    result={'case':a.case,'status':status,'turns':turns,'changed':sorted(changed),'unexpectedChanges':unexpected,'headAndIndexUnchanged':git(workspace,'rev-parse','HEAD')==head and git(workspace,'diff','--cached','--binary')==index,'firstHeadAndIndexUnchanged':json.loads((logs/'first-head-index.json').read_text())['unchanged'] if (logs/'first-head-index.json').exists() else None,'artifacts':sorted(str(f.relative_to(outputs)) for f in outputs.rglob('*') if f.is_file()),**summary}
    result['captureChecksPassed']=status=='completed' and not unexpected and result['headAndIndexUnchanged'] and result['firstHeadAndIndexUnchanged'] is not False and bool(result['artifacts'])
    result['behaviorVerdict']='UNREVIEWED: capture checks do not establish workflow conformance'
    save(logs/'result.json',result);print(json.dumps(result),flush=True)
    return 0 if result['captureChecksPassed'] else 1


if __name__=='__main__':raise SystemExit(main())
