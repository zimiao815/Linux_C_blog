from pathlib import Path
import json, os, platform, subprocess, tempfile

art = Path(__file__).resolve().parent
flags = ['-std=c17', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion',
         '-Wshadow', '-O0', '-g']
env = dict(os.environ, LC_ALL='C')
records = []

def run(args, cwd, **kwargs):
    p = subprocess.run(args, cwd=cwd, env=env, text=True,
                       stderr=subprocess.PIPE, **kwargs)
    records.append({'command': args, 'exit': p.returncode,
                    'stdout': p.stdout or '', 'stderr': p.stderr})
    return p

with tempfile.TemporaryDirectory(prefix='stdio-identity-') as directory:
    tmp = Path(directory)
    (tmp/'stream_identity.c').write_bytes((art/'stream_identity.c').read_bytes())
    compiler = run(['cc', '--version'], tmp, stdout=subprocess.PIPE)
    built = run(['cc', *flags, 'stream_identity.c', '-o', 'stream_identity'], tmp,
                stdout=subprocess.PIPE)
    assert built.returncode == 0 and not built.stderr, built.stderr
    (tmp/'sample.txt').write_bytes(b'A')
    (tmp/'empty.txt').write_bytes(b'')
    normal = run(['./stream_identity', 'sample.txt'], tmp, stdout=subprocess.PIPE)
    assert normal.returncode == 0
    assert 'initial: eof=0, error=0\nfirst=65, eof=0\nsecond_is_EOF=1, eof=1, error=0\n' in normal.stdout
    empty = run(['./stream_identity', 'empty.txt'], tmp, stdout=subprocess.PIPE)
    assert empty.returncode == 0 and 'second_is_EOF=1, eof=1, error=0' in empty.stdout
    missing = run(['./stream_identity', 'missing.txt'], tmp, stdout=subprocess.PIPE)
    assert missing.returncode != 0 and 'fopen:' in missing.stderr
    usage = run(['./stream_identity'], tmp, stdout=subprocess.PIPE)
    assert usage.returncode != 0 and 'usage:' in usage.stderr
    directory_case = run(['./stream_identity', '.'], tmp, stdout=subprocess.PIPE)
    assert directory_case.returncode != 0
    with (tmp/'sample.txt').open('rb') as readonly_stdout:
        output_error = run(['./stream_identity', 'sample.txt'], tmp, stdout=readonly_stdout)
    assert output_error.returncode != 0
    assert 'printf:' in output_error.stderr or 'fflush stdout:' in output_error.stderr

report = {'system': platform.platform(), 'mac_ver': platform.mac_ver()[0],
          'linux_runtime_tested': False, 'records': records, 'checks_passed': True}
(art/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
(art/'actual-output.txt').write_text(''.join(
    '$ '+' '.join(r['command'])+'\n'+r['stdout']+r['stderr']+
    f"[exit={r['exit']}]\n\n" for r in records))
print(json.dumps(report, ensure_ascii=False, indent=2))
