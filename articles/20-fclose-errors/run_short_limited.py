import resource, signal, subprocess, sys

def limit_child():
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))

with open("limited.txt", "xb") as output:  # 新建文件，不覆盖旧结果
    result = subprocess.run(
        ["./fclose_short"], stdout=output,
        preexec_fn=limit_child, timeout=10)
print(f"exit={result.returncode}", flush=True)
sys.exit(result.returncode)
