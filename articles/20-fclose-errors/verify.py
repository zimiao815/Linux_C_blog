from pathlib import Path
import json, platform, resource, signal, subprocess, tempfile, sys

art=Path(__file__).resolve().parent
flags='-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()
records=[]
def set_limit(amount):
    def setup():
        signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE,(amount,amount))
    return setup

with tempfile.TemporaryDirectory(prefix='fclose-verify-') as tmp:
    work=Path(tmp)
    for name in ('fclose_probe','close_fd_probe'):
        run=subprocess.run(['cc',*flags,str(art/(name+'.c')),'-o',str(work/name)],capture_output=True,text=True)
        assert run.returncode==0 and run.stderr=='',run.stderr
    for limit in (None,0,4):
        for mode in ('buffered','unbuffered','flush-first'):
            target=work/f'{mode}-{limit}.txt'
            run=subprocess.run([str(work/'fclose_probe'),mode,str(target)],capture_output=True,text=True,timeout=10,preexec_fn=None if limit is None else set_limit(limit))
            content=target.read_bytes()
            assert run.returncode==(0 if limit is None else 1),(mode,limit,run)
            assert content==(b'record=42\n' if limit is None else b'record=42\n'[:limit]),(mode,limit,content)
            if limit is None: assert 'fclose: success' in run.stderr
            elif mode=='buffered': assert run.stderr=='fputs: accepted\nfclose: File too large\n'
            elif mode=='unbuffered': assert 'fputs: File too large' in run.stderr
            else: assert 'fputs: accepted\nfflush: File too large' in run.stderr
            records.append(dict(mode=mode,limit=limit,exit=run.returncode,content=content.decode(),stdout=run.stdout,stderr=run.stderr))
    rejected=[]
    existing=work/'existing.txt';existing.write_text('KEEP\n')
    for label,args,needle in (
        ('missing-argument',[],'usage:'),
        ('unknown-mode',['wrong',str(work/'unknown.txt')],'usage:'),
        ('existing-file',['buffered',str(existing)],'fopen:'),
        ('missing-parent',['buffered',str(work/'missing'/'file.txt')],'fopen:'),
    ):
        run=subprocess.run([str(work/'fclose_probe'),*args],capture_output=True,text=True,timeout=10)
        assert run.returncode==1 and needle in run.stderr
        rejected.append(dict(case=label,exit=run.returncode,stderr=run.stderr))
    assert existing.read_text()=='KEEP\n'
    fd_checks=[]
    for limit in (None,0,4):
        run=subprocess.run([str(work/'close_fd_probe'),str(work/f'fd-{limit}.txt')],capture_output=True,text=True,timeout=10,preexec_fn=None if limit is None else set_limit(limit))
        assert run.returncode==0 and run.stderr==''
        expected='fclose_failed=0 efbig=0 fd_is_ebadf=1\n' if limit is None else 'fclose_failed=1 efbig=1 fd_is_ebadf=1\n'
        assert run.stdout==expected,run.stdout
        fd_checks.append(dict(limit=limit,exit=run.returncode,stdout=run.stdout))
    launcher=subprocess.run([sys.executable,str(art/'run_limited.py')],cwd=work,capture_output=True,text=True,timeout=15)
    assert launcher.returncode==1 and launcher.stdout=='exit=1\n'
    assert launcher.stderr=='fputs: accepted\nfclose: File too large\n'
    assert (work/'limited.txt').read_bytes()==b''

result=dict(environment=dict(system=platform.platform(),compiler=subprocess.check_output(['cc','--version'],text=True),flags=flags),records=records,rejected=rejected,fd_checks=fd_checks,launcher=dict(exit=launcher.returncode,stdout=launcher.stdout,stderr=launcher.stderr))
for name in ('verification.json','actual-output.txt'):
    (art/name).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
