from pathlib import Path
import json, os, platform, resource, select, signal, subprocess, tempfile

art=Path(__file__).resolve().parent
env=dict(os.environ,LC_ALL='C')
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]; errors=[]; builds=[]

def drain(fd):
    chunks=[]
    while select.select([fd],[],[],0.1)[0]:
        data=os.read(fd,4096)
        if not data: break
        chunks.append(data)
    return b''.join(chunks)

with tempfile.TemporaryDirectory(prefix='setvbuf-probe-') as directory:
    tmp=Path(directory)
    compiler=subprocess.run(['cc','--version'],capture_output=True,text=True,check=True)
    for source in ('setvbuf_probe','invalid_mode'):
        (tmp/(source+'.c')).write_bytes((art/(source+'.c')).read_bytes())
        cmd=['cc',*flags,source+'.c','-o',source]
        built=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True)
        assert built.returncode==0 and not built.stderr,built.stderr
        builds.append({'command':cmd,'exit':built.returncode,'stderr':built.stderr})
    for target in ('file','pipe'):
        for mode in ('full','line','none'):
            for payload in ('newline','partial'):
                file=(tmp/'out.txt').open('wb') if target=='file' else None
                cmd=['./setvbuf_probe',mode,payload]
                p=subprocess.Popen(cmd,cwd=tmp,env=env,stdin=subprocess.PIPE,
                                   stdout=file if file else subprocess.PIPE,stderr=subprocess.PIPE)
                try:
                    assert select.select([p.stderr],[],[],5)[0], 'checkpoint timeout'
                    checkpoint=p.stderr.readline()
                    assert checkpoint==b'[checkpoint] press Enter\n',checkpoint
                    assert p.poll() is None,'must still be waiting'
                    before=(tmp/'out.txt').read_bytes() if file else drain(p.stdout.fileno())
                    remainder,stderr=p.communicate(input=b'\n',timeout=5)
                    complete=(tmp/'out.txt').read_bytes() if file else before+remainder
                    message=b'ready\n' if payload=='newline' else b'ready> '
                    expected=message if mode=='none' or (mode=='line' and payload=='newline') else b''
                    assert before==expected,(target,mode,payload,before)
                    assert complete==message and p.returncode==0 and not stderr,(complete,p.returncode,stderr)
                    records.append({'target':target,'mode':mode,'payload':payload,'command':cmd,
                                    'before_release':before.decode(),'after_close':complete.decode(),
                                    'exit':p.returncode,'checkpoint':checkpoint.decode()})
                finally:
                    if p.poll() is None: p.kill(); p.wait()
                    for stream in (p.stdin,p.stdout,p.stderr):
                        if stream: stream.close()
                    if file: file.close()
    for args,input_data,marker in ((['full','newline'],b'','stdin ended'),(['invalid','newline'],b'','unknown buffering mode'),([],b'','usage:')):
        failed=subprocess.run(['./setvbuf_probe',*args],cwd=tmp,env=env,input=input_data,capture_output=True)
        assert failed.returncode==1 and marker in failed.stderr.decode()
        errors.append({'case':marker,'command':['./setvbuf_probe',*args],'exit':failed.returncode,'stderr':failed.stderr.decode()})
    def limit_file_size():
        signal.signal(signal.SIGXFSZ,signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))
    for mode in ('full','none'):
        with (tmp/'limited.txt').open('wb') as out:
            failed=subprocess.run(['./setvbuf_probe',mode,'newline'],cwd=tmp,env=env,input=b'\n',stdout=out,stderr=subprocess.PIPE,preexec_fn=limit_file_size)
        marker=b'fclose stdout' if mode=='full' else b'fputs stdout'
        assert failed.returncode==1 and marker in failed.stderr and b'File too large' in failed.stderr
        errors.append({'case':'RLIMIT_FSIZE=0: '+mode,'exit':failed.returncode,'stderr':failed.stderr.decode()})
    badmode=subprocess.run(['./invalid_mode'],cwd=tmp,env=env,capture_output=True)
    assert badmode.returncode==0 and badmode.stderr==b'invalid mode rejected: yes\n'
    errors.append({'case':'setvbuf invalid mode (expected rejection)','exit':badmode.returncode,'stderr':badmode.stderr.decode()})

report={'system':platform.platform(),'compiler':compiler.stdout,'flags':flags,'builds':builds,
        'linux_runtime_tested':False,'records':records,'errors':errors,'checks_passed':True}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['target | mode | payload | before release | after close | exit']
for r in records:
    lines.append(f"{r['target']} | {r['mode']} | {r['payload']} | {json.dumps(r['before_release'])} | {json.dumps(r['after_close'])} | {r['exit']}")
(art/'actual-output.txt').write_text('\n'.join(lines)+'\n\n'+json.dumps(errors,ensure_ascii=False,indent=2)+'\n')
print('\n'.join(lines)); print(json.dumps(errors,ensure_ascii=False,indent=2))
