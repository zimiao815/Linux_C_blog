#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int save_fd(int fd, const char *text);

int main(void)
{
    char path[] = "/tmp/save-fd-demo-XXXXXX";
    int fd = mkstemp(path);
    if (fd == -1) return 1;
    if (write(fd, "abc", 3) != 3 || lseek(fd, 0, SEEK_SET) == -1) {
        close(fd); unlink(path); return 1;
    }
    if (save_fd(fd, "X") == -1) { unlink(path); return 1; }
    errno = 0;
    int closed = fcntl(fd, F_GETFD) == -1 && errno == EBADF;
    int input = open(path, O_RDONLY);
    if (input == -1) { unlink(path); return 1; }
    if (unlink(path) == -1) { close(input); return 1; }
    char buf[4] = {0};
    ssize_t n = read(input, buf, 3);
    int rc = close(input);
    if (n != 3 || rc == -1 || strcmp(buf, "Xbc") != 0 || !closed) return 1;
    printf("content=%s closed_fd=%d\n", buf, closed);

    // /dev/null 是现成的可写设备；验证常用的成功路径。
    fd = open("/dev/null", O_WRONLY);
    if (fd == -1 || save_fd(fd, "ok\n") == -1) return 1;
    errno = 0;
    if (!(fcntl(fd, F_GETFD) == -1 && errno == EBADF)) return 1;
    puts("device_write=ok");
    return 0;
}
