from pathlib import Path
import json, platform, resource, signal, subprocess, sys, tempfile

art = Path(__file__).resolve().parent
flags = '-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g'.split()
def limited(amount):
    def setup():
        signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE, (amount, amount))
    return setup

records, saves, failures = [], [], []
with tempfile.TemporaryDirectory(prefix='fclose-short-') as tmp:
    work = Path(tmp)
    for binary, sources in [('fclose_short', ['fclose_short.c']), ('save', ['save_record.c', 'save_main.c'])]:
        run = subprocess.run(['cc', *flags, *[str(art / s) for s in sources], '-o', str(work / binary)], capture_output=True, text=True)
        assert run.returncode == 0 and run.stderr == '', run.stderr
    for limit in (None, 0, 4):
        target = work / f'probe-{limit}'
        setup = None if limit is None else limited(limit)
        with target.open('xb') as output:
            run = subprocess.run([str(work / 'fclose_short')], stdout=output, stderr=subprocess.PIPE, text=True, preexec_fn=setup, timeout=10)
        expected = 'fputs: accepted\nfclose: ' + ('success\n' if limit is None else 'File too large\n')
        assert run.returncode == (0 if limit is None else 1) and run.stderr == expected, run
        assert target.read_bytes() == (b'record=42\n' if limit is None else b'record=42\n'[:limit])
        records.append(dict(limit=limit, exit=run.returncode, stderr=run.stderr, content=target.read_text()))
        target = work / f'save-{limit}'
        run = subprocess.run([str(work / 'save'), str(target)], capture_output=True, text=True, preexec_fn=setup, timeout=10)
        assert run.returncode == (0 if limit is None else 1)
        assert run.stderr == ('' if limit is None else 'save_record: File too large\n')
        assert target.read_bytes() == (b'record=42\n' if limit is None else b'record=42\n'[:limit])
        saves.append(dict(limit=limit, exit=run.returncode, stderr=run.stderr, content=target.read_text()))
    target = work / 'keep'; target.write_text('KEEP\n')
    for label, path in [('existing', target), ('missing-parent', work / 'missing' / 'out')]:
        run = subprocess.run([str(work / 'save'), str(path)], capture_output=True, text=True, timeout=10)
        assert run.returncode == 1 and run.stderr.startswith('save_record:')
        failures.append(dict(case=label, exit=run.returncode, stderr=run.stderr))
    assert target.read_text() == 'KEEP\n'
    run = subprocess.run([sys.executable, str(art / 'run_short_limited.py')], cwd=work, capture_output=True, text=True, timeout=15)
    assert run.returncode == 1 and run.stdout == 'exit=1\n' and run.stderr == records[1]['stderr']
    assert (work / 'limited.txt').read_bytes() == b''
    launcher = dict(exit=run.returncode, stdout=run.stdout, stderr=run.stderr)
report = dict(environment=platform.platform(), flags=flags, records=records, saves=saves, failures=failures, launcher=launcher)
(art / 'short-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('PASS: 3 short probes, 3 saves, 2 open failures, 1 launcher; strict compilation without warnings')
