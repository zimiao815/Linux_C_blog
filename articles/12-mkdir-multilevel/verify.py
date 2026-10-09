from pathlib import Path
import json, os, platform, shutil, subprocess, tempfile
art=Path(__file__).resolve().parent
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]
def run(label,args,cwd,expect=0):
 r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 records.append({'label':label,'command':args,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==expect,(label,r.returncode,r.stderr)
 return r
with tempfile.TemporaryDirectory(prefix='mkdir-verify-') as root:
 p=Path(root)
 for source in ('mkdir_once.c','mkdir_p.c'):
  shutil.copy2(art/source,p/source)
 for source,exe in [('mkdir_once.c','mkdir_once'),('mkdir_p.c','mkdir_p')]:
  run('compile-'+exe,['cc',*flags,source,'-o',exe],p)
 run('single-missing-parent',['./mkdir_once','one/two'],p,1)
 assert 'No such file or directory' in records[-1]['stderr']
 run('recursive-create',['./mkdir_p','one/two/three'],p)
 assert (p/'one/two/three').is_dir()
 run('recursive-repeat',['./mkdir_p','one/two/three'],p)
 (p/'one/file').write_text('x')
 run('component-is-file',['./mkdir_p','one/file/child'],p,1)
 assert 'Not a directory' in records[-1]['stderr']
 run('empty-path',['./mkdir_p',''],p,1)
 run('absolute-path',['./mkdir_p',str(p/'absolute/a/b')],p)
 assert (p/'absolute/a/b').is_dir()
 run('trailing-slash',['./mkdir_p','one/two/three/'],p)
 run('usage',['./mkdir_p'],p,1)
report={'environment':platform.platform(),'compiler':subprocess.check_output(['cc','--version'],text=True),'flags':flags,'records':records,'all_passed':True,'limitations':'macOS host; no concurrent race or Linux filesystem run.'}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for r in records:
 print(r['label'],r['returncode'])
 if r['label'] in ('single-missing-parent','recursive-create','recursive-repeat','component-is-file'):
  print(r['stdout']+r['stderr'],end='')
