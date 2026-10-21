from pathlib import Path
art=Path(__file__).resolve().parent
article=(art/'article-template.md').read_text()
for key,name in {'@@PROBE@@':'feof_short.c','@@ENGINEERING@@':'copy_stream.c'}.items():
    article=article.replace(key,(art/name).read_text().strip())
assert '@@' not in article
(art/'正文.md').write_text(article)
print('Composed revised feof article')
