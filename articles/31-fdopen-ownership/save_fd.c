#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

// 接管有效、可写的 fd；成功或失败返回后，调用者都不能再使用它。
int save_fd(int fd, const char *text)
{
    FILE *fp = fdopen(fd, "w");
    if (fp == NULL) {
        int saved = errno;
        close(fd);                     // 包装失败，仍由本函数清理 fd
        errno = saved;
        return -1;
    }
    int failed = fputs(text, fp) == EOF;
    int saved = errno;
    if (fclose(fp) == EOF) {            // 负责刷新和关闭；失败也不再 close(fd)
        if (!failed) saved = errno;
        failed = 1;
    }
    if (failed) errno = saved;
    return failed ? -1 : 0;
}
