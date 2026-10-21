from pathlib import Path
import json
import os
import platform
import subprocess
import tempfile

art = Path(__file__).resolve().parent
flags = ["-std=c17", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion", "-Wshadow", "-O0", "-g"]
with tempfile.TemporaryDirectory(prefix="fgets-boundary-") as tmp:
    exe = Path(tmp) / "fgets_probe"
    build = subprocess.run(["cc", *flags, str(art / "fgets_probe.c"), "-o", str(exe)],
                           capture_output=True, text=True)
    assert build.returncode == 0 and not build.stderr, build.stderr
    cases = {
        "long_no_final_newline": b"abcdefghi\nlast",
        "short_with_newline": b"abc\n",
        "empty": b"",
    }
    outputs = {}
    for name, data in cases.items():
        run = subprocess.run([str(exe)], input=data, capture_output=True, timeout=10)
        assert run.returncode == 0 and not run.stderr, run
        outputs[name] = run.stdout.decode()
    assert outputs["long_no_final_newline"] == (
        "part=1 len=7 newline=0\n"
        "part=2 len=3 newline=1\n"
        "part=3 len=4 newline=0\n"
        "done parts=3 eof=1\n"
    )
    assert outputs["short_with_newline"] == "part=1 len=4 newline=1\ndone parts=1 eof=1\n"
    assert outputs["empty"] == "done parts=0 eof=1\n"
    fd = os.open(tmp, os.O_RDONLY)
    try:
        failed = subprocess.run([str(exe)], stdin=fd, capture_output=True, text=True, timeout=10)
    finally:
        os.close(fd)
    assert failed.returncode == 1 and failed.stderr
    report = {
        "environment": {
            "system": platform.platform(),
            "compiler": subprocess.check_output(["cc", "--version"], text=True),
            "flags": flags,
        },
        "outputs": outputs,
        "directory_error": {"exit": failed.returncode, "stderr": failed.stderr},
    }
    (art / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (art / "actual-output.txt").write_text(outputs["long_no_final_newline"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
