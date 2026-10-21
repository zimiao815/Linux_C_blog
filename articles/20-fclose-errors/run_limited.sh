(
    set -C                 # 不覆盖已有的实验文件
    trap '' XFSZ           # 写出失败时返回错误，不让信号终止程序
    ulimit -f 0 || exit 1   # 只在这个子 shell 中禁止文件增长
    ./fclose_short > limited.txt
)
