"""Generate named article assets through the installed gpt-imagegen skill."""
import os
from pathlib import Path
import subprocess
import sys

art = Path(__file__).resolve().parent
kind = sys.argv[1]
if kind not in {"cover", "branches"}:
    raise SystemExit("choose cover or branches")
env = dict(os.environ)
env["IMAGE_OUTPUT_DIR"] = str(art / "images" / kind / "outputs")
name = "cover-34-fork" if kind == "cover" else "img-fork-branches"
command = [
    sys.executable,
    "/Users/zhaodan/.codex/skills/gpt-imagegen/scripts/image_api.py",
    "generate", "--json", "--name", name,
    "--prompt", (art / "images" / f"{kind}-prompt.txt").read_text(),
    "--output", str(art / f"{name}.png"),
]
raise SystemExit(subprocess.call(command, env=env, cwd=art))
