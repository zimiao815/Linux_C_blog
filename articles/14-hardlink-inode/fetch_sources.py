from pathlib import Path
import json, urllib.request, concurrent.futures
art=Path(__file__).resolve().parent
urls={
'posix-link.html':'https://pubs.opengroup.org/onlinepubs/9799919799/functions/link.html',
'posix-stat.html':'https://pubs.opengroup.org/onlinepubs/9799919799/functions/stat.html',
'linux-link.html':'https://man7.org/linux/man-pages/man2/link.2.html',
'linux-stat.html':'https://man7.org/linux/man-pages/man2/stat.2.html',
'linux-unlink.html':'https://man7.org/linux/man-pages/man2/unlink.2.html',
'linux-inode.html':'https://man7.org/linux/man-pages/man7/inode.7.html',
'kernel-namei.c':'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/namei.c',
'kernel-fs.h':'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fs.h',
'kernel-ext4-namei.c':'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/ext4/namei.c',
}
(art/'sources/urls.json').write_text(json.dumps(urls,ensure_ascii=False,indent=2)+'\n')
def fetch(item):
 name,url=item
 with urllib.request.urlopen(url,timeout=40) as r: data=r.read()
 (art/'sources'/name).write_bytes(data)
 return name,len(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for r in pool.map(fetch,urls.items()): print(r,flush=True)
