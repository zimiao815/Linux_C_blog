from pathlib import Path
import json, urllib.request, concurrent.futures
art=Path(__file__).resolve().parent
urls={
'posix-unlink.html':'https://pubs.opengroup.org/onlinepubs/9799919799/functions/unlink.html',
'posix-rmdir.html':'https://pubs.opengroup.org/onlinepubs/9799919799/functions/rmdir.html',
'linux-unlink.html':'https://man7.org/linux/man-pages/man2/unlink.2.html',
'linux-rmdir.html':'https://man7.org/linux/man-pages/man2/rmdir.2.html',
'linux-remove.html':'https://man7.org/linux/man-pages/man3/remove.3.html',
'linux-path-resolution.html':'https://man7.org/linux/man-pages/man7/path_resolution.7.html',
'kernel-namei.c':'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/namei.c',
'kernel-ext4-namei.c':'https://raw.githubusercontent.com/torvalds/linux/v6.6/fs/ext4/namei.c',
'kernel-fs.h':'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fs.h',
'kernel-fdtable.h':'https://raw.githubusercontent.com/torvalds/linux/v6.6/include/linux/fdtable.h',
}
(art/'sources/urls.json').write_text(json.dumps(urls,indent=2)+'\n')
def fetch(pair):
 name,url=pair
 with urllib.request.urlopen(url,timeout=40) as r: data=r.read()
 (art/'sources'/name).write_bytes(data)
 return name,len(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for result in pool.map(fetch,urls.items()): print(result,flush=True)
