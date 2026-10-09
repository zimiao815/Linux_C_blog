import contextlib, importlib.util, io, json, os, re, tempfile
from pathlib import Path
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

os.environ['NO_PROXY'] = os.environ.get('NO_PROXY', '') + ',api.weixin.qq.com'
os.environ['no_proxy'] = os.environ['NO_PROXY']
art = Path(__file__).resolve().parent
secret_path = art.parents[1] / '.env.local'
vals = {}
for line in secret_path.read_text().splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k, v = line.split('=', 1)
        vals[k.strip()] = v.strip().strip('"').strip("'")
config = {'wechat': {
    'app_id': vals['C_BLOG_WECHAT_APP_ID'],
    'app_secret': vals['C_BLOG_WECHAT_APP_SECRET'],
    'default_author': '',
}}
module_path = '/Users/zhaodan/.codex/skills/workbuddy-wechat-publisher/skills/wechat-draft-publisher/scripts/publish_draft.py'
spec = importlib.util.spec_from_file_location('wechat_publisher', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fd, name = tempfile.mkstemp(prefix='wechat-article11-', suffix='.json')
logs = io.StringIO()
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w') as fp:
        json.dump(config, fp)
    with contextlib.redirect_stdout(logs):
        pub = module.WeChatPublisher(name)
        kwargs = dict(
            html_content=(art / 'wechat.html').read_text(),
            html_path=str(art / 'wechat.html'),
            cover_path=str(art / 'cover-11-dirent-d-type-900.png'),
            digest='d_type 遇到 DT_UNKNOWN 时如何补查，并保持符号链接语义。',
        )
        existing = art / 'wechat-draft.json'
        if existing.exists():
            old = json.loads(existing.read_text())
            result = pub.update_draft(old['draft_id'], **kwargs)
            operation = 'updated'
        else:
            result = pub.add_draft(**kwargs)
            operation = 'created'
        if not result.get('success'):
            raise RuntimeError('WeChat draft operation failed')
        result['created_at'] = datetime.now(timezone.utc).isoformat()
        result['operation'] = operation
        existing.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        response = requests.post(
            'https://api.weixin.qq.com/cgi-bin/draft/get',
            params={'access_token': pub.get_access_token()},
            json={'media_id': result['draft_id']},
            timeout=30,
        )
        response.raise_for_status()
        data = json.loads(response.content.decode('utf-8'))
    item = data['news_item'][0]
    soup = BeautifulSoup(item['content'], 'html.parser')
    checks = {
        'title': item['title'] == result['title'],
        'body_images': len(soup.find_all('img')) == 4,
        'remote_images': all((i.get('src') or i.get('data-src', '')).startswith(('http://', 'https://')) for i in soup.find_all('img')),
        'recap': any('文件与目录 选题预告' in a.get_text() and a.get('href', '').startswith('https://mp.weixin.qq.com/') for a in soup.find_all('a')),
        'guide': '这篇文章怎么读' in item['content'],
        'mechanism': 'getdents64' in item['content'] and 'struct dirent' in soup.get_text(),
        'cover': bool(item.get('thumb_media_id')),
        'title_expected': item['title'] == 'd_type 为何不能直接当作文件类型的答案？',
    }
    (art / 'wechat-verification.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
    if not all(checks.values()):
        raise RuntimeError('draft readback mismatch')
    print(json.dumps({'success': True, 'operation': operation, 'draft_id': result['draft_id'], 'title': result['title'], 'readback': checks}, ensure_ascii=False))
except BaseException as exc:
    print('Upload/readback failed:', type(exc).__name__)
    message = logs.getvalue()
    for value in vals.values():
        if value:
            message = message.replace(value, '[redacted]')
    if 'pub' in locals() and getattr(pub, '_access_token', None):
        message = message.replace(pub._access_token, '[redacted]')
    message = re.sub(r'(access_token|secret)=([^&\s]+)', r'\1=[redacted]', message)
    print(message)
    raise SystemExit(1)
finally:
    Path(name).unlink(missing_ok=True)
