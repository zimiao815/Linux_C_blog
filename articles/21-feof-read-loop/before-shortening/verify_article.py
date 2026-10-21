from pathlib import Path
import json,re
from PIL import Image
from bs4 import BeautifulSoup
art=Path(__file__).resolve().parent
md=(art/'正文.md').read_text()
html=(art/'wechat.html').read_text()
soup=BeautifulSoup(html,'html.parser')
images=soup.find_all('img')
source=(art/'read_loop.c').read_text().strip()
plain=re.sub(r'\s+','',soup.get_text())
checks={
 'source_matches_article': re.findall(r'```c\n(.*?)```',md,re.S)[0].strip()==source,
 'source_survives_html': re.sub(r'\s+','',source) in plain,
 'observations_match_article':(art/'observations.md').read_text().strip() in md,
 'four_inputs_verified':len(json.loads((art/'verification.json').read_text())['records'])==4,
 'four_failure_cases_verified':len(json.loads((art/'verification.json').read_text())['failures'])==4,
 'three_bounded_bad_loop_cases':len(json.loads((art/'verification.json').read_text())['bad_loop'])==3,
 'state_recovery_verified':json.loads((art/'verification.json').read_text())['states']['exit']==0,
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
