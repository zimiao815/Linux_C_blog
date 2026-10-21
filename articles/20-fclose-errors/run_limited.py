import resource
import signal
import subprocess
import sys

def limit_child():
    signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))

result = subprocess.run(
    ["./fclose_probe", "buffered", "limited.txt"],
    preexec_fn=limit_child,
    timeout=10,
)
print(f"exit={result.returncode}", flush=True)
sys.exit(result.returncode)
