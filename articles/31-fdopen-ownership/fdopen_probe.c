#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    char path[] = "/tmp/fdopen-demo-XXXXXX";
    int fd = mkstemp(path);             // 创建只属于本次实验的文件
    if (fd == -1) return 1;
    if (unlink(path) == -1) { close(fd); return 1; }
    if (write(fd, "abc", 3) != 3 || lseek(fd, 0, SEEK_SET) == -1) {
        close(fd);
        return 1;
    }

    FILE *fp = fdopen(fd, "r+");         // 包装已有 fd，没有复制
    if (fp == NULL) { close(fd); return 1; }
    int same = fileno(fp) == fd;
    int first = fgetc(fp);
    if (fclose(fp) == EOF) return 1;     // 此处同时关闭关联 fd

    errno = 0;
    int invalid = fcntl(fd, F_GETFD) == -1 && errno == EBADF;
    return printf("same_fd=%d first=%c\nclosed_fd=%d\n",
                  same, first, invalid) < 0;
}
