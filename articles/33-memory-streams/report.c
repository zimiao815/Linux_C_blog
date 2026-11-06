#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>

// 已有输出函数：只认识 FILE *，不需要知道目标是文件还是内存。
int render_report(FILE *out, size_t count)
{
    return fprintf(out, "count=%zu\n", count);
}

// buf 为调用者提供的 cap 字节数组；失败时不使用其中的部分结果。
int report_to_memory(char *buf, size_t cap, size_t count)
{
    if (cap == 0) { errno = EINVAL; return -1; }
    FILE *fp = fmemopen(buf, cap, "w");
    if (fp == NULL) return -1;
    int n = render_report(fp, count);
    int failed = n < 0 || (size_t)n >= cap; // 给结尾空字符留一格
    int saved = n < 0 ? errno : ENOSPC;
    if (fclose(fp) == EOF) {               // 刷新并关闭，不释放 buf
        if (!failed) saved = errno;
        failed = 1;
    }
    if (failed) { errno = saved; return -1; }
    return 0;
}
