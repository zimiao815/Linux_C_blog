from pathlib import Path
import json, os, platform, resource, signal, subprocess, tempfile

art = Path(__file__).resolve().parent
flags = '-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()
def limit_output():
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))

records, copies, failures = [], [], []
with tempfile.TemporaryDirectory(prefix='feof-short-') as tmp:
    work = Path(tmp)
    for binary, sources in [('feof_short', ['feof_short.c']), ('copy', ['copy_stream.c', 'copy_main.c'])]:
        run = subprocess.run(['cc', *flags, *[str(art / s) for s in sources], '-o', str(work / binary)], capture_output=True, text=True)
        assert run.returncode == 0 and run.stderr == '', run.stderr
    for label, data in [('empty', b''), ('single', b'A'), ('newline', b'A\n'), ('binary', b'\x00\xff')]:
        run = subprocess.run([str(work / 'feof_short')], input=data, capture_output=True, timeout=10)
        expected = 'start: eof=0 error=0\n' + ''.join(f'byte={b} eof=0 error=0\n' for b in data) + 'stop: EOF eof=1 error=0\n'
        assert run.returncode == 0 and run.stderr == b'' and run.stdout.decode() == expected
        records.append(dict(case=label, exit=run.returncode, stdout=run.stdout.decode()))
    for label, data in [('empty', b''), ('all-bytes', bytes(range(256)))]:
        run = subprocess.run([str(work / 'copy')], input=data, capture_output=True, timeout=10)
        assert run.returncode == 0 and run.stderr == b'' and run.stdout == data
        copies.append(dict(case=label, exit=run.returncode, exact_match=True, bytes=len(data)))
    for binary in ('feof_short', 'copy'):
        fd = os.open(work, os.O_RDONLY)
        try:
            run = subprocess.run([str(work / binary)], stdin=fd, capture_output=True, text=True, timeout=10)
        finally:
            os.close(fd)
        assert run.returncode == 1 and 'Is a directory' in run.stderr
        if binary == 'feof_short': assert run.stdout == 'start: eof=0 error=0\nstop: EOF eof=0 error=1\n'
        failures.append(dict(program=binary, case='directory', exit=run.returncode, stdout=run.stdout, stderr=run.stderr))
        with (work / f'output-{binary}').open('xb') as output:
            run = subprocess.run([str(work / binary)], input=b'A', stdout=output, stderr=subprocess.PIPE, timeout=10, preexec_fn=limit_output)
        assert run.returncode == 1 and b'File too large' in run.stderr
        failures.append(dict(program=binary, case='output-limit', exit=run.returncode, stderr=run.stderr.decode()))
report = dict(environment=platform.platform(), flags=flags, records=records, copies=copies, failures=failures)
(art / 'short-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('PASS: 4 short inputs, 2 exact copies, 4 read/write failures; strict compilation without warnings')
