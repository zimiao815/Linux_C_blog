from pathlib import Path
import concurrent.futures, json, urllib.request
from bs4 import BeautifulSoup
art = Path(__file__).resolve().parent
urls = {
 'posix-fopen.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fopen.html',
 'posix-open.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/open.html',
 'posix-fclose.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fclose.html',
 'posix-fputs.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fputs.html',
 'glibc-fileops.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/fileops.c',
 'kernel-open.c': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/open.c',
 'kernel-namei.c': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/namei.c',
 'kernel-fdtable.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fdtable.h',
 'kernel-fs.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fs.h',
 'linux-fopen.3': 'https://raw.githubusercontent.com/mkerrisk/man-pages/master/man3/fopen.3',
}
(art/'sources/urls.json').write_text(json.dumps(urls, indent=2)+'\n')
def fetch(item):
 name, url = item
 try:
  with urllib.request.urlopen(url, timeout=45) as r: data = r.read()
  (art/'sources'/name).write_bytes(data)
  if name.endswith('.html'):
   soup = BeautifulSoup(data, 'html.parser')
   for node in soup(['script', 'style']): node.decompose()
   (art/'sources'/name.replace('.html', '.txt')).write_text(soup.get_text('\n',strip=True))
  return {'file':name, 'bytes':len(data), 'ok': True}
 except Exception as e: return {'file':name, 'ok':False, 'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(fetch, urls.items()))
(art/'sources/fetch-results.json').write_text(json.dumps(results, indent=2)+'\n')
for r in results: print(r)
