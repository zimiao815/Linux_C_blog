from pathlib import Path
import subprocess, tempfile, json, platform, re
from bs4 import BeautifulSoup
from PIL import Image
art = Path(__file__).resolve().parent
flags = ['-std=c17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow']
records = []
with tempfile.TemporaryDirectory(prefix='memory-streams-') as d:
    for name, main in [('probe','memory_probe.c'), ('boundaries','memory_test.c')]:
        cmd = ['cc', *flags, 'report.c', main, '-o', str(Path(d)/name)]
        built = subprocess.run(cmd, cwd=art, capture_output=True, text=True)
        assert built.returncode == 0 and not built.stderr, built.stderr
        run = subprocess.run([str(Path(d)/name)], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        records.append(dict(name=name, sources=['report.c', main], flags=flags,
                            exit=run.returncode, stdout=run.stdout, stderr=run.stderr))
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
    short_c_blocks=all(len(b.strip().splitlines())<=12 for b in blocks),
    actual_output_embedded=all(line in md for line in records[0]['stdout'].splitlines()),
    two_images=len(soup.find_all('img'))==2,
    images_exist=all((art/i['src']).is_file() for i in soup.find_all('img')),
    cover_size=Image.open(art/'cover-33-memory-streams.png').size==(900,383),
    single_footer=soup.get_text().count('本文为公众号')==1,
    no_placeholder='[配图' not in md and '[MECHANISM_IMAGE]' not in md and 'CODEBLOCK' not in str(soup),
    title=soup.h1.get_text()=='内存流：让 fprintf 直接写进字符串',
)
(art/'article-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(checks.values())
print((art/'actual-output.txt').read_text())
