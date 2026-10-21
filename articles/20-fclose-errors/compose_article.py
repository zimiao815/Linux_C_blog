from pathlib import Path
import json
art=Path(__file__).resolve().parent
report=json.loads((art/'short-verification.json').read_text())
rows=['| 运行条件 | 实际报告顺序 | 文件内容 |','| --- | --- | --- |']
for r in report['records']:
    label='不额外限额' if r['limit'] is None else f"上限 {r['limit']} 字节"
    result='`fputs` 成功 → `fclose` '+('成功' if r['exit']==0 else '失败')
    content='空文件' if not r['content'] else '`'+r['content'].replace('\n',r'\n')+'`'
    rows.append(f'| {label} | {result} | {content} |')
observations='\n'.join(rows)
(art/'observations.md').write_text(observations+'\n')
article=(art/'article-template.md').read_text()
values={'@@PROBE@@':(art/'fclose_short.c').read_text().strip(),'@@ENGINEERING@@':(art/'save_flow.pseudocode').read_text().strip(),'@@LAUNCHER@@':(art/'run_limited.sh').read_text().strip(),'@@NORMAL@@':report['records'][0]['stderr'].strip(),'@@LIMITED@@':json.loads((art/'shell-verification.json').read_text())[0]['stderr'].strip(),'@@OBSERVATIONS@@':observations}
for key,value in values.items(): article=article.replace(key,value)
assert '@@' not in article
(art/'正文.md').write_text(article)
print('Composed revised fclose article')
