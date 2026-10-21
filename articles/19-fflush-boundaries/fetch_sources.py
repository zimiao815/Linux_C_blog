from pathlib import Path
import concurrent.futures, json, urllib.request
from bs4 import BeautifulSoup
art = Path(__file__).resolve().parent
urls = {'posix-fflush.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fflush.html', 'posix-fsync.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fsync.html', 'posix-fclose.html': 'https://pubs.opengroup.org/onlinepubs/9799919799/functions/fclose.html', 'glibc-flushing.html': 'https://sourceware.org/glibc/manual/2.40/html_node/Flushing-Buffers.html', 'glibc-iofflush.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/iofflush.c', 'glibc-fileops.c': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/fileops.c', 'glibc-struct_FILE.h': 'https://raw.githubusercontent.com/bminor/glibc/glibc-2.40/libio/bits/types/struct_FILE.h', 'kernel-fdtable.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fdtable.h', 'kernel-fs.h': 'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fs.h', 'linux-fsync.html': 'https://man7.org/linux/man-pages/man2/fsync.2.html', 'linux-fflush.html': 'https://man7.org/linux/man-pages/man3/fflush.3.html', 'linux-write.html': 'https://man7.org/linux/man-pages/man2/write.2.html'}
(art/'sources/urls.json').write_text(json.dumps(urls, indent=2)+'\n')
def fetch(item):
 name, url = item
 try:
  if (art/'sources'/name).exists(): data=(art/'sources'/name).read_bytes()
  else:
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
