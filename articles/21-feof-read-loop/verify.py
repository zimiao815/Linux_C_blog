from pathlib import Path
import json, platform, resource, signal, subprocess, tempfile

art=Path(__file__).resolve().parent
flags='-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()

def limit_output():
    signal.signal(signal.SIGXFSZ,signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))

with tempfile.TemporaryDirectory(prefix='feof-verify-') as tmp:
    work=Path(tmp)
    for name in ('read_loop','bad_loop_probe','eof_state'):
        run=subprocess.run(['cc',*flags,str(art/(name+'.c')),'-o',str(work/name)],capture_output=True,text=True)
        assert run.returncode==0 and run.stderr=='',run.stderr
    records=[]
    for name,content in [('empty',b''),('single',b'A'),('newline',b'A\n'),('binary',bytes([0,255]))]:
        source=work/(name+'.bin');source.write_bytes(content)
        run=subprocess.run([str(work/'read_loop'),str(source)],capture_output=True,text=True,timeout=10)
        expected='start: eof=0 error=0\n'+''.join(f'byte={value} eof=0 error=0\n' for value in content)+'stop: EOF eof=1 error=0\n'
        assert run.returncode==0 and run.stderr=='' and run.stdout==expected,run
        records.append(dict(case=name,bytes=list(content),exit=run.returncode,stdout=run.stdout,stderr=run.stderr))
    failures=[]
    for name,args,needle in [('missing-argument',[],'usage:'),('missing-file',[str(work/'absent')],'fopen:'),('read-directory',[str(work)],'fgetc: Is a directory')]:
        run=subprocess.run([str(work/'read_loop'),*args],capture_output=True,text=True,timeout=10)
        assert run.returncode==1 and needle in run.stderr,run
        if name=='read-directory': assert run.stdout=='start: eof=0 error=0\nstop: EOF eof=0 error=1\n'
        failures.append(dict(case=name,exit=run.returncode,stdout=run.stdout,stderr=run.stderr))
    with (work/'output.txt').open('wb') as output:
        run=subprocess.run([str(work/'read_loop'),str(work/'single.bin')],stdout=output,stderr=subprocess.PIPE,text=True,timeout=10,preexec_fn=limit_output)
        assert run.returncode==1 and 'fflush stdout: File too large' in run.stderr
        failures.append(dict(case='output-size-limit-zero',exit=run.returncode,stderr=run.stderr,output_bytes=(work/'output.txt').stat().st_size))
    bad=[]
    for name,path in [('empty',work/'empty.bin'),('single',work/'single.bin'),('directory',work)]:
        run=subprocess.run([str(work/'bad_loop_probe'),str(path)],capture_output=True,text=True,timeout=10)
        assert run.stderr=='' and run.returncode==(1 if name=='directory' else 0)
        if name=='empty': assert run.stdout=='step=1 result=EOF eof=1 error=0\n'
        elif name=='single': assert run.stdout=='step=1 byte=65 eof=0 error=0\nstep=2 result=EOF eof=1 error=0\n'
        else: assert run.stdout==''.join(f'step={i} result=EOF eof=0 error=1\n' for i in range(1,4))+'cap reached; !feof still true\n'
        bad.append(dict(case=name,exit=run.returncode,stdout=run.stdout))
    run=subprocess.run([str(work/'eof_state')],capture_output=True,text=True,timeout=10)
    expected='after-byte eof=0 error=0\nafter-end eof=1 error=0\nread-again eof=1 error=0\nafter-clearerr eof=0 error=0\nstill-at-end eof=1 error=0\nafter-seek eof=0 error=0\n'
    assert run.returncode==0 and run.stderr=='' and run.stdout==expected,run
    states=dict(exit=run.returncode,stdout=run.stdout)
report=dict(environment=dict(system=platform.platform(),compiler=subprocess.check_output(['cc','--version'],text=True),flags=flags),records=records,failures=failures,bad_loop=bad,states=states)
for name in ('verification.json','actual-output.txt'):
    (art/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
