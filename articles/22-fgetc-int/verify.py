from pathlib import Path
import json, os, platform, resource, signal, subprocess, tempfile

art=Path(__file__).resolve().parent
flags='-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()
def limit_output():
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))

with tempfile.TemporaryDirectory(prefix='fgetc-int-') as tmp:
    work=Path(tmp);records=[];limits=[];copies=[];failures=[]
    for mode,extra in [('default',[]),('signed',['-fsigned-char']),('unsigned',['-funsigned-char'])]:
        for binary,sources in [('probe',['fgetc_probe.c']),('limits',['limits_probe.c']),('copy',['copy_bytes.c','copy_main.c'])]:
            run=subprocess.run(['cc',*flags,*extra,*[str(art/s) for s in sources],'-o',str(work/f'{binary}-{mode}')],capture_output=True,text=True)
            assert run.returncode==0 and run.stderr=='',run.stderr
        env=subprocess.run([str(work/f'limits-{mode}')],capture_output=True,text=True,timeout=10)
        assert env.returncode==0 and env.stderr==''
        signed=mode!='unsigned'
        expected=f'CHAR_BIT=8 UCHAR_MAX=255 INT_MAX=2147483647 CHAR_MIN={-128 if signed else 0} EOF=-1\n'
        assert env.stdout==expected,env.stdout
        limits.append(dict(mode=mode,output=env.stdout))
        for label,data in [('ff',b'\xff'),('ascii',b'A'),('empty',b'')]:
            run=subprocess.run([str(work/f'probe-{mode}')],input=data,capture_output=True,timeout=10)
            raw=list(data[:2]);raw.extend([-1]*(2-len(raw)))
            expected=''
            for value in raw:
                small=((value+128)%256-128) if signed else value%256
                expected+=f'int={value} char={small} eof={int(value==-1)}\n'
            assert run.returncode==0 and run.stderr==b'' and run.stdout.decode()==expected,run
            records.append(dict(mode=mode,input=label,exit=run.returncode,stdout=run.stdout.decode()))
        for label,data in [('all-bytes',bytes(range(256))),('empty',b'')]:
            run=subprocess.run([str(work/f'copy-{mode}')],input=data,capture_output=True,timeout=10)
            assert run.returncode==0 and run.stderr==b'' and run.stdout==data
            copies.append(dict(mode=mode,input=label,bytes=len(data),exact_match=True,exit=run.returncode))
    for binary in ('probe-default','copy-default'):
        fd=os.open(work,os.O_RDONLY)
        try:
            run=subprocess.run([str(work/binary)],stdin=fd,capture_output=True,text=True,timeout=10)
        finally:
            os.close(fd)
        assert run.returncode==1 and 'Is a directory' in run.stderr and run.stdout==''
        failures.append(dict(program=binary,case='directory-input',exit=run.returncode,stderr=run.stderr))
        with (work/(binary+'-limited.txt')).open('wb') as out:
            run=subprocess.run([str(work/binary)],input=b'\xff',stdout=out,stderr=subprocess.PIPE,preexec_fn=limit_output,timeout=10)
        assert run.returncode==1 and b'File too large' in run.stderr
        failures.append(dict(program=binary,case='output-limit-zero',exit=run.returncode,stderr=run.stderr.decode()))

report=dict(environment=dict(system=platform.platform(),compiler=subprocess.check_output(['cc','--version'],text=True),flags=flags),limits=limits,records=records,copies=copies,failures=failures)
for name in ('verification.json','actual-output.txt'):
    (art/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
