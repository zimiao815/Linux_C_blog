"""Check the assembled article against its code, evidence and local assets."""
from pathlib import Path
import hashlib
import json
import re
from bs4 import BeautifulSoup
from PIL import Image

art = Path(__file__).resolve().parent
md = (art / "正文.md").read_text()
html = (art / "wechat.html").read_text()
soup = BeautifulSoup(html, "html.parser")
normalize = lambda s: re.sub(r"\s+", "", s)
code = normalize((art / "fork_demo.c").read_text())
blocks = re.findall(r"```c\n(.*?)```", md, re.S)
images = soup.find_all("img")
checks = {
    "compilation_and_runs_passed": json.loads((art / "verification.json").read_text())["passed"],
    "four_c_blocks_match_source": len(blocks) == 4 and all(normalize(b) in code for b in blocks),
    "code_survives_html": all(normalize(b) in normalize(soup.get_text()) for b in blocks),
    "actual_output_matches": (art / "sample-output.txt").read_text().strip() in md,
    "environment_limit_present": "未在 Linux 主机实测" in md and "未在 Linux 主机实测" in soup.get_text(),
    "five_h2_sections": len(soup.find_all("h2")) == 5,
    "two_images_exist": len(images) == 2 and all((art / img["src"]).is_file() for img in images),
    "cover_size": Image.open(art / "cover-34-fork.png").size == (900, 383),
    "inline_token_color": bool(re.search(r'<span style="color:', html)),
    "no_pygments_classes": not re.search(r'class="(?:kt|n|o|s|k|p)"', html),
    "no_style_blocks": soup.find("style") is None,
    "single_guide": soup.get_text().count("这篇文章怎么读") == 1,
    "single_footer": soup.get_text().count("本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。") == 1,
    "no_placeholders": not any(p in md + html for p in ["[配图", "CODEBLOCK", "TODO", "Lorem ipsum"]),
}
result = {"passed": all(checks.values()), "checks": checks,
          "sha256": {name: hashlib.sha256((art / name).read_bytes()).hexdigest()
                     for name in ["正文.md", "wechat.html", "fork_demo.c", "cover-34-fork.png", "img-fork-branches.png"]}}
(art / "article-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["passed"] else 1)
