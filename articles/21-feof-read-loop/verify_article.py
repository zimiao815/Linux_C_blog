from pathlib import Path
import json,re
from PIL import Image
from bs4 import BeautifulSoup
art=Path(__file__).resolve().parent
md=(art/'正文.md').read_text()
html=(art/'wechat.html').read_text()
soup=BeautifulSoup(html,'html.parser')
images=soup.find_all('img')
sources=[(art/name).read_text().strip() for name in ('feof_short.c', 'copy_stream.c', 'copy_main.c')]
blocks=re.findall(r'```c\n(.*?)```',md,re.S)
short=json.loads((art/'short-verification.json').read_text())
plain=re.sub(r'\s+','',soup.get_text())
engineering=md.split('## 第三章',1)[1].split('## 第四章',1)[0]
checks={
 'source_matches_article': [b.strip() for b in blocks]==sources,
 'source_survives_html': all(re.sub(r'\s+','',s) in plain for s in sources),
 'observations_match_article':(art/'observations.md').read_text().strip() in md,
 'four_inputs_verified':len(json.loads((art/'verification.json').read_text())['records'])==4,
 'four_failure_cases_verified':len(json.loads((art/'verification.json').read_text())['failures'])==4,
 'three_bounded_bad_loop_cases':len(json.loads((art/'verification.json').read_text())['bad_loop'])==3,
 'state_recovery_verified':json.loads((art/'verification.json').read_text())['states']['exit']==0,
 'three_short_real_c_blocks':len(blocks)==3 and all(len(b.strip().splitlines())<=20 for b in blocks),
 'chinese_comments':all(re.search(r'/\*[^*]*[\u4e00-\u9fff]',b) for b in blocks),
 'short_probes_verified':len(short['records'])==4 and all(r['exit']==0 for r in short['records']),
 'copy_verified':len(short['copies'])==2 and all(r['exact_match'] and r['exit']==0 for r in short['copies']),
 'new_failures_verified':len(short['failures'])==4 and all(r['exit']==1 for r in short['failures']),
 'new_output_in_article':all(r['stdout'].strip() in md for r in short['records'] if r['case']=='single'),
 'new_error_in_article':all(r['stderr'].strip() in md for r in short['failures'] if r['program']=='feof_short' and r['case']=='directory'),
 'engineering_real_c_only':len(re.findall(r'```c\n',engineering))==2 and not re.search(r'```(?:sh|bash|shell|zsh|pseudocode)\b|伪代码',engineering),
 'ai_images_used':all(n in md for n in ('feof-timing-ai-v2.png','feof-return-ai.png')),
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
 'cover_dimensions':Image.open(art/'cover-21-feof-read-loop-900.png').size==(900,383),
}
(art/'article-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
assert all(checks.values())
