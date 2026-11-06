from pathlib import Path
import subprocess, tempfile, json, platform, re
from bs4 import BeautifulSoup
from PIL import Image
art = Path(__file__).resolve().parent
flags = ['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow','-O0','-g']
records = []
with tempfile.TemporaryDirectory(prefix='memory-streams-') as d:
    for name, sources in [('fixed', ['fixed_example.c']), ('dynamic', ['dynamic_example.c']), ('probe', ['report.c', 'memory_probe.c']), ('boundaries', ['report.c', 'memory_test.c'])]:
        cmd = ['cc', *flags, *sources, '-o', str(Path(d)/name)]
        built = subprocess.run(cmd, cwd=art, capture_output=True, text=True)
        assert built.returncode == 0 and not built.stderr, built.stderr
        run = subprocess.run([str(Path(d)/name)], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        records.append(dict(name=name, sources=sources, flags=flags,
                            exit=run.returncode, stdout=run.stdout, stderr=run.stderr))
    for cap in (6, 5, 4):
        source = Path(d) / f'fixed-{cap}.c'
        source.write_text((art/'fixed_example.c').read_text().replace('buf[16]', f'buf[{cap}]'))
        executable = Path(d) / f'fixed-{cap}'
        built = subprocess.run(['cc', *flags, str(source), '-o', str(executable)], capture_output=True, text=True)
        assert built.returncode == 0 and not built.stderr, built.stderr
        run = subprocess.run([str(executable)], capture_output=True, text=True)
        expected = 0 if cap >= 6 else 1
        assert run.returncode == expected
        assert run.stdout == ('hello\n' if expected == 0 else '')
        records.append(dict(name=f'fixed-cap-{cap}', sources=['fixed_example.c'],
            variation=f'buf[{cap}]', flags=flags, exit=run.returncode,
            stdout=run.stdout, stderr=run.stderr))
assert records[0]['stdout'] == 'hello\n'
assert records[1]['stdout'] == 'text=hello, len=5\n'
(art/'verification.json').write_text(json.dumps(dict(environment=platform.platform(),
    compiler=subprocess.check_output(['cc','--version'],text=True),
    linux_tested=False, records=records),ensure_ascii=False,indent=2)+'\n')
(art/'actual-output.txt').write_text(''.join(r['stdout'] for r in records))
md=(art/'正文.md').read_text()
soup=BeautifulSoup((art/'wechat.html').read_text(),'html.parser')
blocks=re.findall(r'```c\n(.*?)```',md,re.S)
sources=[p.read_text() for p in art.glob('*.c')]
norm=lambda s:'\n'.join(x.lstrip() for x in s.strip().splitlines())
plain=lambda s:re.sub(r'\s+','',s)
checks=dict(
    code_matches_source=all(any(norm(b) in norm(s) for s in sources) for b in blocks),
    code_survives_html=all(plain(b) in plain(soup.get_text()) for b in blocks),
    short_c_blocks=all(len(b.strip().splitlines())<=6 for b in blocks),
    actual_output_embedded=all(line in md for r in records[:2] for line in r['stdout'].splitlines()),
    two_images=len(soup.find_all('img'))==2,
    images_exist=all((art/i['src']).is_file() for i in soup.find_all('img')),
    cover_size=Image.open(art/'cover-33-memory-streams.png').size==(900,383),
    single_footer=soup.get_text().count('本文为公众号')==1,
    no_placeholder='[配图' not in md and '[MECHANISM_IMAGE]' not in md and 'CODEBLOCK' not in str(soup),
    title=soup.h1.get_text()=='fmemopen 和 open_memstream 怎么用？',
)
(art/'article-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(checks.values())
print((art/'actual-output.txt').read_text())
