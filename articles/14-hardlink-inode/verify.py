from pathlib import Path
import json, platform, shutil, subprocess, tempfile, re
art=Path(__file__).resolve().parent
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]
def run(label,args,cwd,expected=0):
 r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 records.append({'label':label,'command':args,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==expected,(label,r.returncode,r.stderr)
 return r
with tempfile.TemporaryDirectory(prefix='hardlink-verify-') as root:
 p=Path(root)
 for stem in ('hardlink_demo','link_errors'):
  shutil.copy2(art/(stem+'.c'),p/(stem+'.c'))
  run('compile-'+stem,['cc',*flags,stem+'.c','-o',stem],p)
  assert records[-1]['stderr']==''
 demo=run('demo',['./hardlink_demo'],p)
 assert re.search(r'original: dev=\d+ ino=\d+ nlink=2 size=22\n',demo.stdout)
 assert re.search(r'second: dev=\d+ ino=\d+ nlink=2 size=22\n',demo.stdout)
 assert 'after unlink original: second: ' in demo.stdout and 'nlink=1' in demo.stdout
 assert demo.stdout.endswith('content: same inode, two names\n')
 errors=run('errors',['./link_errors'],p)
 assert errors.stdout=='existing destination: File exists\ndirectory source: Operation not permitted\n'
report={'environment':platform.platform(),'compiler':subprocess.check_output(['cc','--version'],text=True),'flags':flags,'records':records,'all_passed':True,'limitations':'macOS host; Linux source review; no cross-filesystem or concurrent race run.'}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(art/'actual-output.txt').write_text('\n'.join(f"[{r['label']}] exit={r['returncode']}\nstdout:\n{r['stdout']}stderr:\n{r['stderr']}" for r in records))
for r in records:
 print(r['label'],r['returncode']); print(r['stdout']+r['stderr'],end='')
