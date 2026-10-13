import contextlib, importlib.util, io, json, os, re, sys, tempfile
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
fd, name = tempfile.mkstemp(prefix='wechat-article17-', suffix='.json')
logs = io.StringIO()
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w') as fp:
        json.dump(config, fp)
    with contextlib.redirect_stdout(logs), contextlib.redirect_stderr(logs):
        pub = module.WeChatPublisher(name)
        kwargs = dict(
            html_content=(art / 'wechat.html').read_text(),
            html_path=str(art / 'wechat.html'),
            cover_path=str(art / 'cover-17-stdout-buffering-900.png'),
            digest='同一行 printf，为什么在终端及时出现，重定向后却留在缓冲中？用九组实验讲清缓冲与刷新。',
        )
        existing = art / 'wechat-draft.json'
        if '--readback-only' in sys.argv:
            result = json.loads(existing.read_text())
            operation = 'readback'
        elif existing.exists():
            old = json.loads(existing.read_text())
            result = pub.update_draft(old['draft_id'], **kwargs)
            operation = 'updated'
        else:
            result = pub.add_draft(**kwargs)
            operation = 'created'
        if not result.get('success'):
            raise RuntimeError('WeChat draft operation failed')
        if operation != 'readback':
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
    body_text = re.sub(r'\s+', ' ', soup.get_text())
    checks = {
        'title': item['title'] == result['title'],
        'title_expected': item['title'] == 'printf 加了换行，重定向后为什么还是没输出？',
        'body_images': len(soup.find_all('img')) == 3,
        'remote_images': all((i.get('src') or i.get('data-src', '')).startswith(('http://', 'https://')) for i in soup.find_all('img')),
        'guide': '这篇文章怎么读' in item['content'],
        'mechanism': all(word in body_text for word in ('fflush', 'stdout', 'stderr', 'fdtable', '行缓冲', '全缓冲')),
        'cover': bool(item.get('thumb_media_id')),
        'code_preserved': re.sub(r'\s+', '', (art / 'stdout_buffer.c').read_text()) in re.sub(r'\s+', '', soup.get_text()),
        'environment_limit': 'macOS 14.8.8' in body_text,
        'observations_table': all(word in body_text for word in ('newline', 'partial', 'flush', '无字节', '接终端（PTY）')),
        'single_footer': body_text.count('本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。') == 1,
    }
    (art / 'wechat-verification.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
    if not all(checks.values()):
        raise RuntimeError('draft readback mismatch')
    print(json.dumps({'success': True, 'operation': operation, 'draft_id': result['draft_id'], 'title': result['title'], 'readback': checks}, ensure_ascii=False))
except BaseException as exc:
    print('Upload/readback failed:', type(exc).__name__)
    message = logs.getvalue()
    if isinstance(locals().get('result'), dict) and not result.get('success'):
        message += '\n' + str(result.get('message', 'unknown API error'))
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
