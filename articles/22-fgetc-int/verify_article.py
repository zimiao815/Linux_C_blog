from pathlib import Path
import json
import re
from bs4 import BeautifulSoup

art = Path(__file__).resolve().parent
md = (art / "正文.md").read_text()
html = (art / "wechat.html").read_text()
soup = BeautifulSoup(html, "html.parser")
report = json.loads((art / "verification.json").read_text())
sources = [(art / name).read_text().strip()
           for name in ("copy_bytes.c", "fgetc_probe.c")]
blocks = re.findall(r"```c\n(.*?)```", md, re.S)
plain = re.sub(r"\s+", "", soup.get_text())
images = soup.find_all("img")
checks = {
    "title": "title: \"以 fgetc 的返回值，解释标准 I/O 的返回值\"" in md,
    "source_matches_article": [b.strip() for b in blocks] == sources,
    "source_survives_html": all(re.sub(r"\s+", "", s) in plain for s in sources),
    "actual_outputs_embedded": all(r["stdout"].strip() in md
                                    for r in report["records"] if r["input"] == "ff"),
    "short_c_blocks": len(blocks) == 2 and all(len(b.strip().splitlines()) <= 16 for b in blocks),
    "chinese_code_comments": all(re.search(r"/\*[^*]*[\u4e00-\u9fff]", b) for b in blocks),
    "four_h2": len(re.findall(r"^## ", md, re.M)) == 4,
    "two_images": len(images) == 2,
    "local_images_exist": all((art / i["src"]).is_file() for i in images),
    "no_kernel_expansion": "_IO_read_ptr" not in md,
    "no_placeholder": "[配图" not in md,
    "no_svg_refs": ".svg)" not in md,
    "single_footer": soup.get_text().count("本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。") == 1,
    "experiment_limit_stated": "未在 Linux 主机实测" in md,
}
(art / "article-verification.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(checks, ensure_ascii=False, indent=2))
assert all(checks.values())
