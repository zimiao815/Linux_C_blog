#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

static int put_uint(char *dst, unsigned int v) {
    char tmp[16];
    int i = 0, j;
    do { tmp[i++] = (char)('0' + (v % 10u)); v /= 10u; } while (v > 0u);
    for (j = 0; j < i; j++) dst[j] = tmp[i - 1 - j];
    return i;
}

int main(void) {
    close(0);  /* 关掉标准输入，让编号从 0 开始，好观察 */

    int fd1 = open("demo.txt", O_RDONLY);
    int fd2 = open("demo.txt", O_RDONLY);
    if (fd1 < 0 || fd2 < 0) {
        const char *msg = strerror(errno);
        write(2, msg, strlen(msg));
        write(2, "\n", 1);
        return 1;
    }

    char buf[64];
    int n = 0;
    const char *p1 = "fd1 = ";
    memcpy(buf + n, p1, 6); n += 6;
    n += put_uint(buf + n, (unsigned int)fd1);
    buf[n++] = ','; buf[n++] = ' ';
    const char *p2 = "fd2 = ";
    memcpy(buf + n, p2, 6); n += 6;
    n += put_uint(buf + n, (unsigned int)fd2);
    buf[n++] = '\n';
    write(1, buf, (size_t)n);

    close(fd1);
    int fd3 = open("demo.txt", O_RDONLY);
    n = 0;
    const char *p3 = "close(";
    memcpy(buf + n, p3, 6); n += 6;
    n += put_uint(buf + n, (unsigned int)fd1);
    const char *p4 = ") 后再 open，拿到 fd = ";
    size_t p4len = strlen(p4);
    memcpy(buf + n, p4, p4len); n += (int)p4len;
    n += put_uint(buf + n, (unsigned int)fd3);
    buf[n++] = '\n';
    write(1, buf, (size_t)n);

    close(fd2);
    close(fd3);
    return 0;
}
