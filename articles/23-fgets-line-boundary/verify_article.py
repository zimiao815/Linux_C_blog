from pathlib import Path
import json
import re
from bs4 import BeautifulSoup
from PIL import Image

art = Path(__file__).resolve().parent
md = (art / "正文.md").read_text()
html = (art / "wechat.html").read_text()
soup = BeautifulSoup(html, "html.parser")
report = json.loads((art / "verification.json").read_text())
source = (art / "fgets_probe.c").read_text().strip()
blocks = re.findall(r"```c\n(.*?)```", md, re.S)
plain = re.sub(r"\s+", "", soup.get_text())
images = soup.find_all("img")
checks = {
    "title": "title: \"fgets 读一行，为什么一次不一定读完整？\"" in md,
    "source_matches_article": len(blocks) == 1 and blocks[0].strip() == source,
    "source_survives_html": re.sub(r"\s+", "", source) in plain,
    "actual_output_embedded": report["outputs"]["long_no_final_newline"].strip() in md,
    "short_code": len(source.splitlines()) <= 24,
    "three_h2": len(re.findall(r"^## ", md, re.M)) == 3,
    "two_images": len(images) == 2,
    "local_images_exist": all((art / image["src"]).is_file() for image in images),
    "cover_dimensions": Image.open(art / "cover-23-fgets-line-boundary.png").size == (900, 383),
    "body_dimensions": Image.open(art / "fgets-chunks-23.png").size == (1536, 1024),
    "no_placeholder": "[配图" not in md,
    "no_svg_refs": ".svg)" not in md,
    "single_footer": soup.get_text().count("本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。") == 1,
    "environment_limit_stated": "未在 Linux 主机实测" in md,
    "no_upload": not (art / "wechat-draft.json").exists(),
}
(art / "article-verification.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(checks, ensure_ascii=False, indent=2))
assert all(checks.values())
