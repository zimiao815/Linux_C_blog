from pathlib import Path
import json,re
from PIL import Image
from bs4 import BeautifulSoup
art=Path(__file__).resolve().parent
md=(art/'正文.md').read_text()
html=(art/'wechat.html').read_text()
soup=BeautifulSoup(html,'html.parser')
images=soup.find_all('img')
sources=[(art/name).read_text().strip() for name in ('fclose_short.c', 'save_flow.pseudocode')]
blocks=re.findall(r'```c\n(.*?)```',md,re.S)
short=json.loads((art/'short-verification.json').read_text())
plain=re.sub(r'\s+','',soup.get_text())
checks={
 'source_matches_article': [b.strip() for b in blocks]==sources,
 'source_survives_html': all(re.sub(r'\s+','',s) in plain for s in sources),
 'no_python_in_article':'```python' not in md and 'run_short_limited.py' not in md,
 'shell_verified':all(r['exit']==1 and r['file_bytes']==0 and r['stderr'].strip() in md for r in json.loads((art/'shell-verification.json').read_text())),
 'nine_cases_verified':len(json.loads((art/'verification.json').read_text())['records'])==9,
 'four_rejection_cases_verified':len(json.loads((art/'verification.json').read_text())['rejected'])==4,
 'three_descriptor_checks':len(json.loads((art/'verification.json').read_text())['fd_checks'])==3,
 'launcher_matches_article': (art/'run_limited.sh').read_text().strip() in [b.strip() for b in re.findall(r'```sh\n(.*?)```',md,re.S)],
 'launcher_survives_html':re.sub(r'\s+','',(art/'run_limited.sh').read_text()) in plain,
 'short_code_and_pseudocode':len(blocks)==2 and all(len(b.strip().splitlines())<=20 for b in blocks),
 'pseudocode_label':'C 语言伪代码，不能直接编译' in md,
 'record_is_ten_bytes':len(short['records'][0]['content'].encode())==10 and '10 字节' in md and re.search(r'(?<![0-9])9 ?字节',md) is None,
 'new_ai_images_used':all(name in md for name in ('fclose-buffer-failure-ai-v2.png','fclose-check-once-ai.png')),
 'chinese_comments':all(re.search(r'(?:/\*|//)[^\n]*[\u4e00-\u9fff]',b) for b in blocks),
 'short_probes_verified':len(short['records'])==3 and [r['exit'] for r in short['records']]==[0,1,1],
 'save_function_verified':len(short['saves'])==3 and [r['exit'] for r in short['saves']]==[0,1,1],
 'save_open_failures':len(short['failures'])==2 and all(r['exit']==1 for r in short['failures']),
 'new_output_in_article':all(r['stderr'].strip() in md for r in short['records']),
 'five_h2':len(re.findall(r'^## ',md,re.M))==5,
 'three_images':len(images)==3,
 'local_images_exist':all((art/i['src']).is_file() for i in images),
 'no_placeholder':'[配图' not in md,
 'no_svg_refs':'.svg)' not in md,
 'inline_highlighting':bool(re.search(r'style="[^"]*color:',html)),
 'no_token_classes':not re.search(r'class="(?:kt|n|k|s)"',html),
 'no_style_tag':soup.find('style') is None,
 'single_footer':soup.get_text().count('本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。')==1,
 'experiment_limit_stated':'未在 Linux 主机实测' in md,
 'cover_dimensions':Image.open(art/'cover-20-fclose-errors-900.png').size==(900,383),
}
(art/'article-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(checks.values())
