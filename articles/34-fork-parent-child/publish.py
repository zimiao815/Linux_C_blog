"""Upload the reviewed artifact as a draft and verify the server copy."""
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import requests
from bs4 import BeautifulSoup

art = Path(__file__).resolve().parent
title = "fork 之后，父子进程从哪里继续执行？"
gate = json.loads((art / "article-verification.json").read_text())
assert gate["passed"]
for name, digest in gate["sha256"].items():
    assert hashlib.sha256((art / name).read_bytes()).hexdigest() == digest, name

os.environ["NO_PROXY"] = os.environ.get("NO_PROXY", "") + ",api.weixin.qq.com"
os.environ["no_proxy"] = os.environ["NO_PROXY"]
values = {}
for line in (art.parents[1] / ".env.local").read_text().splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
configuration = {"wechat": {
    "app_id": values["C_BLOG_WECHAT_APP_ID"],
    "app_secret": values["C_BLOG_WECHAT_APP_SECRET"],
    "default_author": "",
}}
module_path = "/Users/zhaodan/.codex/skills/workbuddy-wechat-publisher/skills/wechat-draft-publisher/scripts/publish_draft.py"
spec = importlib.util.spec_from_file_location("wechat_publisher", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fd, temporary_name = tempfile.mkstemp(prefix="wechat-article34-", suffix=".json")
logs = io.StringIO()
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(configuration, stream)
    with contextlib.redirect_stdout(logs), contextlib.redirect_stderr(logs):
        publisher = module.WeChatPublisher(temporary_name)
        existing = art / "wechat-draft.json"
        kwargs = {
            "html_content": (art / "wechat.html").read_text(),
            "html_path": str(art / "wechat.html"),
            "cover_path": str(art / "cover-34-fork.png"),
            "digest": "fork 后从哪里继续？用真实输出看清父子分支、返回值与回收。",
        }
        if "--readback-only" in sys.argv:
            result = json.loads(existing.read_text())
            operation = "readback"
        elif existing.exists():
            previous = json.loads(existing.read_text())
            result = publisher.update_draft(previous["draft_id"], **kwargs)
            operation = "updated"
        else:
            result = publisher.add_draft(**kwargs)
            operation = "created"
        if not result.get("success"):
            raise RuntimeError("draft operation failed")
        if operation != "readback":
            result.update(operation=operation, saved_at=datetime.now(timezone.utc).isoformat())
            existing.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        response = requests.post(
            "https://api.weixin.qq.com/cgi-bin/draft/get",
            params={"access_token": publisher.get_access_token()},
            json={"media_id": result["draft_id"]}, timeout=30)
        response.raise_for_status()
        remote = json.loads(response.content.decode("utf-8"))["news_item"][0]
    remote_soup = BeautifulSoup(remote["content"], "html.parser")
    local_soup = BeautifulSoup((art / "wechat.html").read_text(), "html.parser")
    normalize = lambda s: re.sub(r"\s+", "", s)
    remote_text = remote_soup.get_text()
    checks = {
        "title": remote["title"] == title,
        "body_matches_local": normalize(remote_text) == normalize(local_soup.get_text()),
        "two_remote_images": len(remote_soup.find_all("img")) == 2 and all(
            (img.get("src") or img.get("data-src", "")).startswith(("https://", "http://"))
            for img in remote_soup.find_all("img")),
        "cover_present": bool(remote.get("thumb_media_id")),
        "code_preserved": all(normalize(block) in normalize(remote_text)
            for block in re.findall(r"```c\n(.*?)```", (art / "正文.md").read_text(), re.S)),
        "environment_limit": "未在 Linux 主机实测" in remote_text,
        "single_footer": remote_text.count("本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。") == 1,
    }
    verification = {"passed": all(checks.values()), "checks": checks,
                    "verified_at": datetime.now(timezone.utc).isoformat()}
    (art / "wechat-verification.json").write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n")
    if not verification["passed"]:
        raise RuntimeError("draft readback mismatch")
    print(json.dumps({"success": True, "operation": operation, "title": title,
                      "draft_id": result["draft_id"], "readback": verification}, ensure_ascii=False))
except BaseException as error:
    message = logs.getvalue()
    for value in values.values():
        if value:
            message = message.replace(value, "[redacted]")
    if "publisher" in locals() and getattr(publisher, "_access_token", None):
        message = message.replace(publisher._access_token, "[redacted]")
    message = re.sub(r"(access_token|secret)=([^&\s]+)", r"\1=[redacted]", message)
    print("Draft upload/readback failed:", type(error).__name__)
    print(message)
    raise SystemExit(1)
finally:
    Path(temporary_name).unlink(missing_ok=True)
