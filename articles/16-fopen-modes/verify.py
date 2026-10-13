from pathlib import Path
import json, os, platform, resource, signal, subprocess, tempfile

art = Path(__file__).resolve().parent
flags = ['-std=c17', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion',
         '-Wshadow', '-O0', '-g']
env = dict(os.environ, LC_ALL='C')
records, matrix, writes = [], [], []

def run(args, cwd, **kwargs):
    p = subprocess.run(args, cwd=cwd, env=env, text=True,
                       stderr=subprocess.PIPE, **kwargs)
    records.append({'command': args, 'exit': p.returncode,
                    'stdout': p.stdout or '', 'stderr': p.stderr})
    return p

with tempfile.TemporaryDirectory(prefix='fopen-modes-') as directory:
    tmp = Path(directory)
    (tmp/'mode_probe.c').write_bytes((art/'mode_probe.c').read_bytes())
    run(['cc', '--version'], tmp, stdout=subprocess.PIPE)
    built = run(['cc', *flags, 'mode_probe.c', '-o', 'mode_probe'], tmp,
                stdout=subprocess.PIPE)
    assert built.returncode == 0 and not built.stderr, built.stderr
    for mode in ('r', 'r+', 'w', 'w+', 'a', 'a+'):
        (tmp/'sample.txt').write_bytes(b'OLD')
        p = run(['./mode_probe', mode, 'sample.txt'], tmp, stdout=subprocess.PIPE)
        content = (tmp/'sample.txt').read_bytes()
        assert p.returncode == 0
        expected = b'' if mode.startswith('w') else b'OLD'
        assert content == expected
        assert f'opened_size={len(expected)}' in p.stdout
        missing_path = tmp/('fresh-'+mode)
        missing = run(['./mode_probe', mode, missing_path.name], tmp, stdout=subprocess.PIPE)
        if mode.startswith('r'):
            assert missing.returncode == 1 and not missing_path.exists()
            assert 'No such file or directory' in missing.stderr
        else:
            assert missing.returncode == 0 and missing_path.read_bytes() == b''
        matrix.append({'mode':mode, 'existing_output':p.stdout,
                       'existing_content':content.decode(),
                       'missing_exit':missing.returncode,
                       'missing_output':missing.stdout or missing.stderr,
                       'missing_created':missing_path.exists()})
    for mode, expected in [('r+',b'XLD'),('w+',b'X'),('a',b'OLDX'),('a+',b'OLDX')]:
        (tmp/'sample.txt').write_bytes(b'OLD')
        p=run(['./mode_probe',mode,'sample.txt','X'],tmp,stdout=subprocess.PIPE)
        assert p.returncode==0 and (tmp/'sample.txt').read_bytes()==expected
        writes.append({'mode':mode,'output':p.stdout,'content':expected.decode()})
    (tmp/'sample.txt').write_bytes(b'OLD')
    exclusive=run(['./mode_probe','wx','sample.txt'],tmp,stdout=subprocess.PIPE)
    assert exclusive.returncode==1 and (tmp/'sample.txt').read_bytes()==b'OLD'
    assert 'File exists' in exclusive.stderr
    new_exclusive=run(['./mode_probe','wx','exclusive.txt','X'],tmp,stdout=subprocess.PIPE)
    assert new_exclusive.returncode==0 and (tmp/'exclusive.txt').read_bytes()==b'X'
    no_parent=run(['./mode_probe','w','no-parent/file'],tmp,stdout=subprocess.PIPE)
    assert no_parent.returncode==1 and 'No such file or directory' in no_parent.stderr
    directory_case=run(['./mode_probe','r','.'],tmp,stdout=subprocess.PIPE)
    assert directory_case.returncode==1
    with (tmp/'sample.txt').open('rb') as output:
        output_case=run(['./mode_probe','r','sample.txt'],tmp,stdout=output)
    assert output_case.returncode==1 and ('printf:' in output_case.stderr or 'fflush stdout:' in output_case.stderr)
    def limit_file_size():
        signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    write_failure=run(['./mode_probe','w','limited.txt','X'],tmp,
                      stdout=subprocess.PIPE,preexec_fn=limit_file_size)
    assert write_failure.returncode==1
    assert 'fclose:' in write_failure.stderr or 'fputs:' in write_failure.stderr
    for name in ('existing','writing'):
        shell=(art/(name+'.sh')).read_text()
        example=run(['sh','-eu','-c',shell],tmp,stdout=subprocess.PIPE)
        assert example.returncode==0 and not example.stderr
        (art/(name+'-output.txt')).write_text(example.stdout)
    usage=run(['./mode_probe'],tmp,stdout=subprocess.PIPE)
    assert usage.returncode==1

report={'system':platform.platform(),'mac_ver':platform.mac_ver()[0],
        'linux_runtime_tested':False,'matrix':matrix,'writes':writes,
        'records':records,'checks_passed':True}
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(art/'actual-output.txt').write_text(''.join(
    '$ '+' '.join(r['command'])+'\n'+r['stdout']+r['stderr']+
    f"[exit={r['exit']}]\n\n" for r in records))
print(json.dumps({'system':report['system'],'matrix':matrix,'writes':writes,
                  'checks_passed':True},ensure_ascii=False,indent=2))
