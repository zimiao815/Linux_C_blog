#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int save_fd(int fd, const char *text);

// 只替换测试构建中的 fdopen，模拟分配失败；不改动被传入的 fd。
FILE *fail_fdopen(int fd, const char *mode)
{
    (void)fd;
    (void)mode;
    errno = ENOMEM;
    return NULL;
}
int main(void)
{
    int fd = open("/dev/null", O_WRONLY);
    if (fd == -1) return 1;
    int rc = save_fd(fd, "ok");
    int allocation_error = errno == ENOMEM;
    errno = 0;
    int closed = fcntl(fd, F_GETFD) == -1 && errno == EBADF;
    printf("injected_failure rc=%d errno_preserved=%d closed_fd=%d\n",
           rc, allocation_error, closed);
    return !(rc == -1 && allocation_error && closed);
}
