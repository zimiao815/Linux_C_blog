"""Use workflow formatting, then remove its duplicate reprint footer."""
from pathlib import Path
import subprocess, sys
from bs4 import BeautifulSoup
art=Path(__file__).resolve().parent
workflow=art.parents[2]/'linux_c_blog_workflow'
subprocess.run([sys.executable,str(workflow/'build_html.py'),str(art),'--no-banner'],check=True)
p=art/'wechat.html'
soup=BeautifulSoup(p.read_text(),'html.parser')
footer='本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。'
items=[node for node in soup.find_all('p') if node.get_text(strip=True)==footer]
if len(items)==2:
    extra=items[-1]
    previous=extra.find_previous_sibling()
    if previous is not None and previous.name=='hr': previous.decompose()
    extra.decompose()
assert len([x for x in soup.find_all('p') if x.get_text(strip=True)==footer])==1
p.write_text(str(soup))
print('one reprint footer retained')
