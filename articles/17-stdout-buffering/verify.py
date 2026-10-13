from pathlib import Path
import errno, json, os, platform, pty, resource, select, signal
import subprocess, tempfile, time, tty

art=Path(__file__).resolve().parent
env=dict(os.environ,LC_ALL='C')
flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records=[]

def drain(fd):
    chunks=[]
    while select.select([fd],[],[],0.1)[0]:
        try: data=os.read(fd,4096)
        except OSError as exc:
            if exc.errno==errno.EIO: break
            raise
        if not data: break
        chunks.append(data)
    return b''.join(chunks)

with tempfile.TemporaryDirectory(prefix='stdout-buffer-') as directory:
    tmp=Path(directory)
    (tmp/'stdout_buffer.c').write_bytes((art/'stdout_buffer.c').read_bytes())
    compiler=subprocess.run(['cc','--version'],capture_output=True,text=True,check=True)
    built=subprocess.run(['cc',*flags,'stdout_buffer.c','-o','stdout_buffer'],cwd=tmp,capture_output=True,text=True)
    assert built.returncode==0 and not built.stderr,built.stderr
    for target in ('terminal','file','pipe'):
        for mode in ('newline','partial','flush'):
            file=None; master=slave=None
            if target=='terminal':
                master,slave=pty.openpty(); tty.setraw(slave)
                output=slave
            elif target=='file':
                file=(tmp/'out.txt').open('wb'); output=file
            else: output=subprocess.PIPE
            p=subprocess.Popen(['./stdout_buffer',mode],cwd=tmp,env=env,
                               stdin=subprocess.PIPE,stdout=output,stderr=subprocess.PIPE)
            try:
                # Keep the parent PTY slave open until the final read. On macOS,
                # closing the last slave can discard unread terminal output.
                assert select.select([p.stderr],[],[],5)[0], 'checkpoint timeout'
                checkpoint=p.stderr.readline()
                assert checkpoint==b'[checkpoint] press Enter\n',checkpoint
                assert p.poll() is None, 'must still be waiting at gate'
                if target=='file': before=(tmp/'out.txt').read_bytes()
                else: before=drain(master if target=='terminal' else p.stdout.fileno())
                remainder,stderr=p.communicate(input=b'\n',timeout=5)
                if target=='file': complete=(tmp/'out.txt').read_bytes()
                elif target=='terminal': complete=before+drain(master)
                else: complete=before+remainder
                expected_before=b'ready\n' if mode=='flush' or (target=='terminal' and mode=='newline') else b''
                expected_complete=b'ready> done\n' if mode=='partial' else b'ready\ndone\n'
                assert before==expected_before,(target,mode,before)
                assert complete==expected_complete and p.returncode==0 and not stderr, (target,mode,complete,p.returncode,stderr)
                records.append({'target':target,'mode':mode,'checkpoint':checkpoint.decode(),
                                'before_release':before.decode(),'after_release':complete.decode(),
                                'exit':p.returncode,'stderr_after_checkpoint':stderr.decode()})
            finally:
                if p.poll() is None: p.kill(); p.wait()
                for stream in (p.stdin,p.stdout,p.stderr):
                    if stream is not None: stream.close()
                if slave is not None: os.close(slave)
                if master is not None: os.close(master)
                if file is not None: file.close()
    errors=[]
    eof=subprocess.run(['./stdout_buffer','newline'],cwd=tmp,env=env,input=b'',capture_output=True)
    assert eof.returncode==1 and b'stdin ended' in eof.stderr
    errors.append({'case':'stdin EOF','exit':eof.returncode,'stderr':eof.stderr.decode()})
    usage=subprocess.run(['./stdout_buffer','invalid'],cwd=tmp,env=env,capture_output=True)
    assert usage.returncode==1
    errors.append({'case':'invalid argument','exit':usage.returncode,'stderr':usage.stderr.decode()})
    def limit_file_size():
        signal.signal(signal.SIGXFSZ,signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))
    for mode in ('newline','flush'):
        with (tmp/'limited.txt').open('wb') as out:
            failed=subprocess.run(['./stdout_buffer',mode],cwd=tmp,env=env,input=b'\n',
                                  stdout=out,stderr=subprocess.PIPE,preexec_fn=limit_file_size)
        assert failed.returncode==1 and b'File too large' in failed.stderr
        errors.append({'case':'file size limit: '+mode,'exit':failed.returncode,'stderr':failed.stderr.decode()})
    with (tmp/'readonly.txt').open('wb') as f: f.write(b'')
    with (tmp/'readonly.txt').open('rb') as out:
        failed=subprocess.run(['./stdout_buffer','flush'],cwd=tmp,env=env,input=b'\n',stdout=out,stderr=subprocess.PIPE)
    assert failed.returncode==1 and b'Bad file descriptor' in failed.stderr
    errors.append({'case':'readonly stdout','exit':failed.returncode,'stderr':failed.stderr.decode()})

report={'system':platform.platform(),'compiler':compiler.stdout,'flags':flags,
        'compile_stderr':built.stderr,'linux_runtime_tested':False,
        'records':records,'errors':errors,'checks_passed':True}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['target | mode | before release | after release | exit']
for r in records:
    lines.append(f"{r['target']} | {r['mode']} | {json.dumps(r['before_release'])} | {json.dumps(r['after_release'])} | {r['exit']}")
(art/'actual-output.txt').write_text('\n'.join(lines)+'\n\n'+json.dumps(errors,ensure_ascii=False,indent=2)+'\n')
print('\n'.join(lines))
print(json.dumps(errors,ensure_ascii=False,indent=2))
