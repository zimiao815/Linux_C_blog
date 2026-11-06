"""Compile real examples and retain actual outputs, including injected failures."""
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile

art = Path(__file__).resolve().parent
flags = "-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -O0 -g".split()
records = []

def run(args, **kwargs):
    result = subprocess.run(args, capture_output=True, text=True, timeout=20, **kwargs)
    records.append({"command": args, "exit": result.returncode,
                    "stdout": result.stdout, "stderr": result.stderr})
    return result

def check_output(result):
    assert result.returncode == 0 and result.stderr == "", result
    lines = result.stdout.splitlines()
    assert len(lines) == 3, lines
    before = re.fullmatch(r"before: self=(\d+)", lines[0])
    assert before, lines
    parent_pid = int(before[1])
    after = [re.fullmatch(r"after: self=(\d+) fork_return=(\d+)", line)
             for line in lines[1:]]
    assert all(after), lines
    values = [(int(m[1]), int(m[2])) for m in after]
    parent = [v for v in values if v[0] == parent_pid]
    child = [v for v in values if v[1] == 0]
    assert len(parent) == len(child) == 1, values
    assert parent[0][1] == child[0][0] != parent_pid, values
    return "parent-first" if values[0] == parent[0] else "child-first"

environment = {
    "system": platform.platform(),
    "mac_ver": platform.mac_ver()[0],
    "compiler": run(["cc", "--version"]).stdout,
    "flags": flags,
    "linux_executed": platform.system() == "Linux",
}
with tempfile.TemporaryDirectory(prefix="fork-article34-") as temporary:
    root = Path(temporary)
    for source, binary in [("fork_demo.c", "fork-demo"), ("fault_injection.c", "fault-test")]:
        result = run(["cc", *flags, str(art / source), "-o", str(root / binary)])
        assert result.returncode == 0 and not result.stderr, result
    first = run([str(root / "fork-demo")])
    orders = {"parent-first": 0, "child-first": 0}
    orders[check_output(first)] += 1
    (art / "sample-output.txt").write_text(first.stdout)
    for _ in range(19):
        orders[check_output(run([str(root / "fork-demo")]))] += 1
    # 普通文件重定向单独验证，不只观察 Python 捕获的管道。
    target = root / "redirected.txt"
    with target.open("w") as out:
        result = subprocess.run([str(root / "fork-demo")], stdout=out,
                                stderr=subprocess.PIPE, text=True, timeout=20)
    redirected = subprocess.CompletedProcess(result.args, result.returncode,
                                             target.read_text(), result.stderr)
    check_output(redirected)
    records.append({"case": "regular-file-redirection", "exit": result.returncode,
                    "stdout": redirected.stdout, "stderr": result.stderr})
    for fault in ["fork_eagain", "wait_eintr", "wait_echild"]:
        result = run([str(root / "fault-test")],
                     env={**os.environ, "FORK_DEMO_FAULT": fault})
        records[-1]["injected_fault"] = fault
        if fault == "fork_eagain":
            assert result.returncode != 0 and "after:" not in result.stdout
            assert "fork:" in result.stderr
        else:
            assert result.returncode == 0 and result.stderr == ""
            assert "injected" in result.stdout
    # 将 stdout 指向只读描述符，验证首次输出失败后不创建子进程。
    with open(os.devnull, "r") as readonly:
        result = subprocess.run([str(root / "fork-demo")], stdout=readonly,
                                stderr=subprocess.PIPE, text=True, timeout=20)
    assert result.returncode != 0 and "printf before:" in result.stderr
    records.append({"case": "stdout-read-only", "exit": result.returncode,
                    "stdout": "", "stderr": result.stderr})

report = {"passed": True, "environment": environment, "observed_orders": orders,
          "scope": "20 captured runs; regular-file redirection; injected EAGAIN/EINTR/ECHILD; stdout failure",
          "records": records}
(art / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
(art / "actual-output.txt").write_text("\n".join(
    json.dumps({k: v for k, v in record.items() if k not in {"stdout", "stderr"}}, ensure_ascii=False)
    + "\nstdout:\n" + record["stdout"] + "stderr:\n" + record["stderr"]
    for record in records))
print(json.dumps({"passed": True, "environment": environment, "observed_orders": orders}, ensure_ascii=False))
