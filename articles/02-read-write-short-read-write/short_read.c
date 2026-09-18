/*
 * short_read.c — 证明 read 会「短读」：请求读 N 字节，实际可能只返回一部分。
 *
 * 方法：创建一个管道，父进程写一段固定长度（比如 5 字节）的内容，
 * 子进程一次 read 请求 4096 字节，观察返回 5 而不是 4096。
 */
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <errno.h>

static int put_uint(char *dst, long v) {
    char tmp[24];
    int i = 0, j;
    if (v == 0) { dst[0] = '0'; return 1; }
    while (v > 0) { tmp[i++] = (char)('0' + (v % 10)); v /= 10; }
    for (j = 0; j < i; j++) dst[j] = tmp[i - 1 - j];
    return i;
}

static void say(const char *s) {
    write(1, s, strlen(s));
}

int main(void) {
    int fds[2];
    if (pipe(fds) < 0) {
        say("pipe failed\n");
        return 1;
    }

    pid_t pid = fork();
    if (pid < 0) {
        say("fork failed\n");
        return 1;
    }

    if (pid == 0) {
        /* 子进程：只写 5 字节，然后退出 */
        close(fds[0]);
        const char *msg = "hello";
        ssize_t w = write(fds[1], msg, 5);
        (void)w;
        close(fds[1]);
        return 0;
    }

    /* 父进程：请求读 4096 字节 */
    close(fds[1]);

    char buf[4096];
    char line[64];
    int n = 0;

    ssize_t r = read(fds[0], buf, sizeof buf);

    const char *p1 = "请求 read 4096 字节，实际返回 ";
    memcpy(line + n, p1, strlen(p1)); n += (int)strlen(p1);
    n += put_uint(line + n, (long)r);
    line[n++] = '\n';
    write(1, line, (size_t)n);

    close(fds[0]);
    waitpid(pid, NULL, 0);
    return 0;
}
