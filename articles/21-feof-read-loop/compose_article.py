from pathlib import Path
import json
art=Path(__file__).resolve().parent
article=(art/'article-template.md').read_text()
for key,name in {'@@PROBE@@':'feof_short.c','@@ENGINEERING@@':'copy_stream.c','@@CALLER@@':'copy_main.c'}.items():
    article=article.replace(key,(art/name).read_text().strip())
report=json.loads((art/'short-verification.json').read_text())
single=next(r['stdout'].strip() for r in report['records'] if r['case']=='single')
article=article.replace('@@SINGLE@@',single).replace('@@OBSERVATIONS@@',(art/'observations.md').read_text().strip())
assert '@@' not in article
(art/'正文.md').write_text(article)
print('Composed revised feof article')
