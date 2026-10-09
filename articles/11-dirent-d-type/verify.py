from pathlib import Path
import json, os, platform, socket, subprocess, tempfile
art=Path(__file__).resolve().parent
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]
def run(label,args,cwd,expect=0,env=None):
 r=subprocess.run(args,cwd=cwd,text=True,capture_output=True,env=env)
 records.append(dict(label=label,command=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
 assert r.returncode==expect,(label,r.returncode,r.stderr)
 return r
helpers=r'''
#include <unistd.h>
static const char *test_case(void) {
    const char *v = getenv("DTYPE_TEST");
    return v == NULL ? "" : v;
}
static int test_stat(int fd, const char *name, struct stat *st, int flags) {
    static int interrupted = 0;
    if (strcmp(test_case(), "eintr") == 0 && interrupted++ == 0) {
        errno = EINTR; return -1;
    }
    if (strcmp(name, "note.txt") == 0) {
        if (strcmp(test_case(), "eacces") == 0) { errno = EACCES; return -1; }
        if (strcmp(test_case(), "removed") == 0) {
            if (unlinkat(fd, name, 0) == -1) return -1;
        }
    }
    return fstatat(fd, name, st, flags);
}
static struct dirent *test_read(DIR *dir) {
    if (strcmp(test_case(), "read-error") == 0) { errno = EIO; return NULL; }
    return readdir(dir);
}
static int test_fd(DIR *dir) {
    if (strcmp(test_case(), "fd-error") == 0) { errno = EBADF; return -1; }
    return dirfd(dir);
}
static int test_close(DIR *dir) {
    int rc = closedir(dir);
    fprintf(stderr, "TEST: directory closed\n");
    if (strcmp(test_case(), "close-error") == 0) { errno = EIO; return -1; }
    return rc;
}
'''
with tempfile.TemporaryDirectory(prefix='dtype-verify-') as root:
 p=Path(root)
 source=(art/'entry_types.c').read_text()
 (p/'entry_types.c').write_text(source)
 run('compile',['cc',*flags,'entry_types.c','-o','entry_types'],p)
 d=p/'demo';d.mkdir();(d/'note.txt').write_text('hello\n');(d/'sub').mkdir()
 (d/'link').symlink_to('note.txt');(d/'dangling').symlink_to('missing')
 os.mkfifo(d/'pipe');sock=socket.socket(socket.AF_UNIX);sock.bind(str(d/'sock'))
 expected={'note.txt':'file','sub':'directory','link':'symlink','dangling':'symlink','pipe':'fifo','sock':'socket'}
 for label,extra in [('normal',[]),('forced-unknown',['--unknown'])]:
  r=run(label,['./entry_types','demo',*extra],p)
  rows={line.split()[0]:line.split()[1] for line in r.stdout.splitlines()}
  assert rows==expected
  if extra:assert all(line.endswith('via=fstatat') for line in r.stdout.splitlines())
 (p/'empty').mkdir();assert not run('empty',['./entry_types','empty'],p).stdout
 run('missing-dir',['./entry_types','missing'],p,1)
 run('not-directory',['./entry_types','demo/note.txt'],p,1)
 run('usage',['./entry_types'],p,1)
 # Change only call sites after declarations; retain the platform's native readdir ABI.
 injected=source.replace('rc = fstatat(', 'rc = test_stat(').replace('e = readdir(', 'e = test_read(').replace('base = dirfd(', 'base = test_fd(').replace('if (closedir(dir)', 'if (test_close(dir)')
 injected=injected.replace('static const char *mode_type',helpers+'\nstatic const char *mode_type')
 (p/'injected.c').write_text(injected)
 run('compile-injection',['cc',*flags,'injected.c','-o','injected'],p)
 for case,status in [('eintr',0),('eacces',1),('read-error',1),('fd-error',1),('close-error',1),('removed',1)]:
  r=run(case,['./injected','demo','--unknown'],p,status,{**os.environ,'DTYPE_TEST':case})
  assert r.stderr.count('TEST: directory closed')==1
  if case=='eintr':assert len(r.stdout.splitlines())==6
  if case in ('eacces','removed'):
   assert 'note.txt:' in r.stderr and 'note.txt ' not in r.stdout
   assert len(r.stdout.splitlines())==5
 sock.close()
report={'environment':platform.platform(),'compiler':subprocess.check_output(['cc','--version'],text=True),'flags':flags,'records':records,'all_passed':True,'limitations':'macOS host; Linux source review only. --unknown and injected failures are controlled tests, not observed filesystem behavior.'}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for r in records:
 print(r['label'],r['returncode'])
 if r['label'] in ('normal','forced-unknown','removed'):print(r['stdout']+r['stderr'])
