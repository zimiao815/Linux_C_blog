from pathlib import Path
import subprocess, tempfile, json, platform, re
from bs4 import BeautifulSoup
from PIL import Image

art = Path(__file__).resolve().parent
flags = ['-std=c17', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wshadow']
cases = [
    ('sequence', ['read_one.c', 'mixing_probe.c'], []),
    ('boundaries', ['read_one.c', 'read_one_test.c'], []),
    ('injected_errors', ['read_one.c', 'error_test.c'], ['-Dread=test_read']),
]
records = []
with tempfile.TemporaryDirectory(prefix='stdio-mixing-') as d:
    for name, sources, extra in cases:
        command = ['cc', *flags, *extra, *sources, '-o', str(Path(d)/name)]
        built = subprocess.run(command, cwd=art, capture_output=True, text=True)
        assert built.returncode == 0 and not built.stderr, built.stderr
        run = subprocess.run([str(Path(d)/name)], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        records.append(dict(case=name, sources=sources, flags=flags+extra,
                            exit=run.returncode, stdout=run.stdout, stderr=run.stderr))
report = dict(environment=platform.platform(), compiler=subprocess.check_output(['cc','--version'],text=True),
              linux_tested=False, records=records)
(art/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(art/'actual-output.txt').write_text(''.join(r['stdout'] for r in records))
md = (art/'正文.md').read_text()
soup = BeautifulSoup((art/'wechat.html').read_text(), 'html.parser')
blocks = re.findall(r'```c\n(.*?)```', md, re.S)
source = (art/'read_one.c').read_text()
norm = lambda s: '\n'.join(x.lstrip() for x in s.strip().splitlines())
plain = lambda s: re.sub(r'\s+', '', s)
checks = dict(
    c_fragments_match_source=all(norm(b) in norm(source) for b in blocks),
    c_fragments_survive_html=all(plain(b) in plain(soup.get_text()) for b in blocks),
    short_c_blocks=all(len(b.strip().splitlines())<=12 for b in blocks),
    actual_output_embedded=records[0]['stdout'].strip() in md,
    one_cover_image=len(soup.find_all('img'))==1,
    local_images_exist=all((art/i['src']).is_file() for i in soup.find_all('img')),
    cover_size=Image.open(art/'cover-32-stdio-mixing.png').size==(900,383),
    single_footer=soup.get_text().count('本文为公众号')==1,
    no_placeholder='[配图' not in md and '[MECHANISM_IMAGE]' not in md and 'CODEBLOCK' not in str(soup),
    title=soup.h1.get_text()=='fread 读了一个字节，read 为什么接不上？',
    posix_scope='ISO C' in md and '未在 Linux 主机实测' in md,
)
(art/'article-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(checks.values())
print((art/'actual-output.txt').read_text())
