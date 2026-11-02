"""Owned host walkthrough: real published source update, no model or global install."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from codex_acceptance_state import snapshot

REPO = Path(__file__).resolve().parents[1]
OLD = '7c5307971ffcbfae2d90d93da86d246b98de35a1'


def main():
    capture = Path(tempfile.mkdtemp(prefix='pstack-release-')).resolve()
    project = capture / 'workspace'; project.mkdir()
    old = capture / 'old-source'; old.mkdir()
    archive = subprocess.run(['git','archive',OLD],cwd=REPO,check=True,capture_output=True).stdout
    subprocess.run(['tar','-xf','-','-C',str(old)],input=archive,check=True)
    (project/'.codex').mkdir()
    (project/'.codex/config.toml').write_text('# unrelated setting\nmodel_reasoning_effort = "medium"\n')
    (project/'.codex/pstack-models.json').write_text('{"schema":1,"roles":{}}\n')
    (project/'README.md').write_text('Release fixture marker: PSTACK_RELEASE_02\n')
    audit = dict(old=OLD,current=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),events=[],before=snapshot(project))
    def run(source,script,*args):
        r=subprocess.run([sys.executable,'-B',str(source/script),*map(str,args)],capture_output=True,text=True)
        audit['events'].append(dict(script=script,args=list(map(str,args)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
        if r.returncode: raise RuntimeError('Helper refused operation; no bypass or cleanup retry')
        return r.stdout
    runtime='plugins/pstack/skills/poteto-mode/scripts/runtime.py'
    def install(source):
        run(source,'scripts/link-codex-entry.py',project)
        run(source,runtime,'install',project); run(source,runtime,'verify',project)
        installed=snapshot(project)
        assert json.loads(run(source,runtime,'install',project))['status']=='already-installed'
        assert snapshot(project)==installed
        for key,value in audit['before'].items(): assert snapshot(project)[key]==value,key
    def remove(source):
        run(source,runtime,'verify',project); run(source,runtime,'uninstall',project)
        alias=project/'.agents/skills/poteto-mode'
        assert alias.is_symlink() and alias.resolve(strict=True)==(source/'plugins/pstack/skills/poteto-mode').resolve(strict=True)
        alias.unlink()
        for name in ('.codex/agents','.agents/skills','.agents'): (project/name).rmdir()
        assert snapshot(project)==audit['before']
    print(capture,flush=True)
    try:
        install(old); audit['oldInstalled']=snapshot(project)
        old_entry=old/'plugins/pstack/skills/poteto-mode/SKILL.md'; new_entry=REPO/'plugins/pstack/skills/poteto-mode/SKILL.md'
        audit['entryHashes']=[hashlib.sha256(p.read_bytes()).hexdigest() for p in (old_entry,new_entry)]
        assert audit['entryHashes'][0]!=audit['entryHashes'][1]
        remove(old); install(REPO); audit['updatedInstalled']=snapshot(project)
        remove(REPO); audit['after']=snapshot(project)
        audit['verdict']='PASS host install/idempotence/real source update/remove; no new release-version or client discovery claim'
    except Exception as error:
        audit['verdict']='FAIL/BLOCKED: '+str(error)
        raise
    finally:
        (capture/'result.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(audit['verdict'])


if __name__=='__main__': main()
