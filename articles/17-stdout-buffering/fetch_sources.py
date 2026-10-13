from pathlib import Path
import concurrent.futures, json, urllib.request
from bs4 import BeautifulSoup
art = Path(__file__).resolve().parent
urls = {'glibc-concepts.html': 'https://sourceware.org/glibc/manual/2.40/html_node/Buffering-Concepts.html', 'posix-stdin.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/stdin.html', 'posix-fflush.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fflush.html', 'posix-exit.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/exit.html', 'linux-stdio.3': 'https://raw.githubusercontent.com/mkerrisk/man-pages/master/man3/stdio.3', 'glibc-filedoalloc.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/filedoalloc.c', 'glibc-stdfiles.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/stdfiles.c', 'glibc-fileops.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/fileops.c', 'glibc-struct_FILE.h': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/bits/types/struct_FILE.h', 'glibc-buffering.html': 'https://sourceware.org/glibc/manual/2.40/html_node/Flushing-Buffers.html', 'kernel-fdtable.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fdtable.h', 'kernel-fs.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fs.h'}
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
