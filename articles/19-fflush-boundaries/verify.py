from pathlib import Path
import json, os, platform, resource, select, signal, subprocess, tempfile

art = Path(__file__).resolve().parent
flags = '-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()
records = []
payload = b'record=42\n'

def checkpoint(p):
    lines = []
    while True:
        ready, _, _ = select.select([p.stderr], [], [], 10)
        assert ready, 'checkpoint timeout'
        line = p.stderr.readline()
        assert line, repr(lines)
        lines.append(line.decode().rstrip())
        if line == b'checkpoint: inspect now\n':
            return lines

def limit_file():
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))

with tempfile.TemporaryDirectory(prefix='fflush-verify-') as tmp:
    work = Path(tmp)
    binary = work/'fflush_probe'
    build = subprocess.run(['cc', *flags, str(art/'fflush_probe.c'), '-o', str(binary)], capture_output=True, text=True)
    assert build.returncode == 0 and build.stderr == '', build.stderr
    for mode in ('buffered', 'flush', 'sync-only', 'flush-sync'):
        target = work/(mode+'.txt')
        with target.open('wb') as out:
            p = subprocess.Popen([str(binary), mode], stdin=subprocess.PIPE, stdout=out, stderr=subprocess.PIPE, bufsize=0)
            try:
                lines = checkpoint(p)
                before = target.read_bytes()
                expected = payload if mode in ('flush','flush-sync') else b''
                assert before == expected, (mode, before)
                _, err = p.communicate(b'x', timeout=10)
                assert p.returncode == 0 and err == b''
                assert target.read_bytes() == payload
                records.append(dict(destination='file', mode=mode, before=before.decode(), after=target.read_text(), exit=p.returncode, stderr=lines))
            finally:
                if p.poll() is None: p.kill(); p.wait()
    for mode in ('buffered', 'flush'):
        p = subprocess.Popen([str(binary), mode], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
        try:
            lines = checkpoint(p)
            ready = bool(select.select([p.stdout], [], [], 0)[0])
            assert ready == (mode == 'flush')
            assert p.poll() is None
            # No consumer read before this point. select only observes readiness.
            out, err = p.communicate(b'x', timeout=10)
            assert p.returncode == 0 and out == payload and err == b''
            records.append(dict(destination='pipe', mode=mode, readable_before_consumer_read=ready, after=out.decode(), exit=p.returncode, stderr=lines))
        finally:
            if p.poll() is None: p.kill(); p.wait()

    failures = []
    for label, args, needle in (
        ('missing-argument', [], b'usage:'),
        ('unknown-mode', ['wrong'], b'usage:'),
        ('stdin-eof', ['flush'], b'stdin ended before release'),
        ('fsync-pipe', ['flush-sync'], b'fsync stdout:'),
    ):
        run = subprocess.run([str(binary), *args], input=b'', capture_output=True, timeout=10)
        assert run.returncode == 1 and needle in run.stderr
        failures.append(dict(case=label, exit=run.returncode, stdout=run.stdout.decode(), stderr=run.stderr.decode()))
    with (work/'limited.txt').open('wb') as out:
        run = subprocess.run([str(binary),'flush'], input=b'x', stdout=out, stderr=subprocess.PIPE, preexec_fn=limit_file, timeout=10)
        assert run.returncode == 1 and b'fputs: accepted\n' in run.stderr and b'fflush stdout: File too large' in run.stderr
        failures.append(dict(case='file-size-limit-zero', exit=run.returncode, file_bytes=(work/'limited.txt').stat().st_size, stderr=run.stderr.decode()))

report = dict(environment=dict(system=platform.platform(), compiler=subprocess.check_output(['cc','--version'],text=True), flags=flags), build_stderr=build.stderr, records=records, failures=failures)
(art/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
(art/'actual-output.txt').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
