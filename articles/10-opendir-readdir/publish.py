import contextlib, importlib.util, io, json, os, tempfile
from pathlib import Path
from datetime import datetime, timezone
import requests
os.environ['NO_PROXY']=os.environ.get('NO_PROXY','')+',api.weixin.qq.com'
os.environ['no_proxy']=os.environ['NO_PROXY']
from bs4 import BeautifulSoup
art=Path(__file__).resolve().parent
secret_path=art.parents[1]/'.env.local'
vals={}
for line in secret_path.read_text().splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1);vals[k.strip()]=v.strip().strip('"').strip("'")
config={'wechat':{'app_id':vals['C_BLOG_WECHAT_APP_ID'],'app_secret':vals['C_BLOG_WECHAT_APP_SECRET'],'default_author':''}}
module_path='/Users/zhaodan/.codex/skills/workbuddy-wechat-publisher/skills/wechat-draft-publisher/scripts/publish_draft.py'
spec=importlib.util.spec_from_file_location('wechat_publisher',module_path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
fd,name=tempfile.mkstemp(prefix='wechat-article10-',suffix='.json')
try:
    os.fchmod(fd,0o600)
    with os.fdopen(fd,'w') as fp:json.dump(config,fp)
    logs=io.StringIO()
    with contextlib.redirect_stdout(logs):
        pub=module.WeChatPublisher(name)
        kwargs=dict(html_content=(art/'wechat.html').read_text(),html_path=str(art/'wechat.html'),cover_path=str(art/'cover-10-opendir-readdir.png'),digest='用 opendir/readdir 遍历目录，分清读完和出错。')
        existing=art/'wechat-draft.json'
        if existing.exists():
            old=json.loads(existing.read_text())
            result=pub.update_draft(old['draft_id'],**kwargs)
        else:
            result=pub.add_draft(**kwargs)
        if not result.get('success'):
            raise RuntimeError('WeChat draft operation failed')
        result['created_at']=datetime.now(timezone.utc).isoformat()
        existing.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        r=requests.post('https://api.weixin.qq.com/cgi-bin/draft/get',params={'access_token':pub.get_access_token()},json={'media_id':result['draft_id']},timeout=30)
        r.raise_for_status();data=r.json()
    item=data['news_item'][0];soup=BeautifulSoup(item['content'],'html.parser')
    checks={
        'title':item['title']==result['title'],
        'body_images':len(soup.find_all('img'))==4,
        'remote_images':all(i.get('src','').startswith(('http://','https://')) for i in soup.find_all('img')),
        'recap':bool(soup.find('a',href='https://mp.weixin.qq.com/s/gz_j5CZMWcnXFcqblTCtGw')),
        'guide':'这篇文章怎么读' in item['content'],
        'mechanism':'getdents64' in item['content'] and 'struct dirent' in soup.get_text(),
        'cover':bool(item.get('thumb_media_id')),
    }
    (art/'wechat-verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    if not all(checks.values()): raise RuntimeError('draft readback mismatch')
    print(json.dumps({'success':True,'draft_id':result['draft_id'],'title':result['title'],'readback':checks},ensure_ascii=False))
except BaseException as exc:
    print('Upload/readback failed:',type(exc).__name__)
    import re
    message=logs.getvalue() if 'logs' in locals() else ''
    for value in vals.values():
        if value: message=message.replace(value,'[redacted]')
    if 'pub' in locals() and getattr(pub,'_access_token',None): message=message.replace(pub._access_token,'[redacted]')
    message=re.sub(r'(access_token|secret)=([^&\s]+)',r'\1=[redacted]',message)
    print(message)
    raise SystemExit(1)
finally:
    Path(name).unlink(missing_ok=True)
