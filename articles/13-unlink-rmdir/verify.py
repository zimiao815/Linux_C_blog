from pathlib import Path
import json, os, platform, shutil, subprocess, tempfile
art=Path(__file__).resolve().parent
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]
def run(label,args,cwd,expected=0):
 r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 records.append(dict(label=label,command=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
 assert r.returncode==expected,(label,r.returncode,r.stderr)
 return r
with tempfile.TemporaryDirectory(prefix='unlink-verify-') as root:
 p=Path(root)
 for stem in ('delete_entry','unlink_open'):
  shutil.copyfile(art/(stem+'.c'),p/(stem+'.c'))
  r=run('compile-'+stem,['cc',*flags,stem+'.c','-o',stem],p)
  assert r.stderr=='',r.stderr
 (p/'empty').mkdir();(p/'full').mkdir();(p/'full/child').write_text('child\n')
 (p/'note.txt').write_text('hello after unlink\n')
 (p/'dir-link').symlink_to('full',target_is_directory=True)
 run('unlink-directory',['./delete_entry','unlink','empty'],p,1)
 assert (p/'empty').is_dir()
 run('rmdir-nonempty',['./delete_entry','rmdir','full'],p,1)
 assert (p/'full/child').read_text()=='child\n'
 run('rmdir-link',['./delete_entry','rmdir','dir-link'],p,1)
 assert (p/'dir-link').is_symlink()
 run('unlink-link',['./delete_entry','unlink','dir-link'],p)
 assert not os.path.lexists(p/'dir-link') and (p/'full/child').is_file()
 r=run('unlink-open',['./unlink_open','note.txt'],p)
 assert r.stdout=='after unlink: nlink=0\nhello after unlink\n'
 assert not (p/'note.txt').exists()
 run('rmdir-empty',['./delete_entry','rmdir','empty'],p)
 assert not (p/'empty').exists()
 run('unlink-child',['./delete_entry','unlink','full/child'],p)
 run('rmdir-now-empty',['./delete_entry','rmdir','full'],p)
 assert not (p/'full').exists()
 run('unlink-missing',['./delete_entry','unlink','missing'],p,1)
 (p/'file').write_text('file');run('rmdir-file',['./delete_entry','rmdir','file'],p,1)
 assert (p/'file').is_file()
 (p/'dangling').symlink_to('absent')
 run('unlink-dangling',['./delete_entry','unlink','dangling'],p)
 assert not os.path.lexists(p/'dangling')
 (p/'hidden-dir').mkdir();(p/'hidden-dir/.keep').touch()
 run('hidden-child',['./delete_entry','rmdir','hidden-dir'],p,1)
 assert (p/'hidden-dir/.keep').exists()
 run('usage',['./delete_entry','bad','file'],p,1)
 run('open-missing',['./unlink_open','missing'],p,1)
 run('unlink-open-directory',['./unlink_open','hidden-dir'],p,1)
 assert (p/'hidden-dir/.keep').exists()
 (p/'readonly-file').write_text('x');(p/'readonly-file').chmod(0o444)
 run('unlink-readonly-file',['./delete_entry','unlink','readonly-file'],p)
 assert not (p/'readonly-file').exists()
 permission_test='skipped: privileged process'
 if os.geteuid()!=0:
  (p/'locked').mkdir();(p/'locked/child').touch();(p/'locked').chmod(0o555)
  try:
   run('parent-no-write',['./delete_entry','unlink','locked/child'],p,1)
   assert (p/'locked/child').exists()
   permission_test='passed: real directory mode 0555'
  finally:
   (p/'locked').chmod(0o700)
report=dict(environment=platform.platform(),kernel=platform.release(),compiler=subprocess.check_output(['cc','--version'],text=True),flags=flags,records=records,permission_test=permission_test,all_passed=True,limitations='macOS host; Linux 6.6 source review; no injected close/read/output errors, no malicious races or physical-space measurement.')
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(art/'actual-output.txt').write_text('\n'.join(f"[{r['label']}] exit={r['returncode']}\nstdout:\n{r['stdout']}stderr:\n{r['stderr']}" for r in records))
for r in records: print(r['label'],r['returncode'],(r['stdout']+r['stderr']).strip())
