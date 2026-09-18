/*
 * short_write.c — 证明 write 会「短写」：一次 write 请求写一大块，可能只写出一部分。
 *
 * 方法：
 *   1. 把管道写端设为非阻塞，持续写直到 EAGAIN（写满管道）；
 *   2. 从读端读走一小部分（腾出一点点空间）；
 *   3. 再尝试写一大块，此时只能写出「空出来的那一点」，即短写。
 */
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>

static void say(const char *s) {
    write(1, s, strlen(s));
}

static void put_u(char *dst, long v) {
    char tmp[24];
    int i = 0, j;
    if (v == 0) { dst[0] = '0'; dst[1] = 0; return; }
    while (v > 0) { tmp[i++] = (char)('0' + (v % 10)); v /= 10; }
    for (j = 0; j < i; j++) dst[j] = tmp[i - 1 - j];
    dst[i] = 0;
}

int main(void) {
    int fds[2];
    if (pipe(fds) < 0) { say("pipe failed\n"); return 1; }

    int flags = fcntl(fds[1], F_GETFL);
    fcntl(fds[1], F_SETFL, flags | O_NONBLOCK);

    char buf[65536];
    memset(buf, 'x', sizeof buf);
    char num[24];

    /* 第一步：把管道写满 */
    ssize_t filled = 0;
    for (;;) {
        ssize_t w = write(fds[1], buf, sizeof buf);
        if (w > 0) { filled += w; continue; }
        if (w < 0 && errno == EAGAIN) break;   /* 写满了 */
        say("write error while filling\n");
        return 1;
    }
    say("pipe filled: "); put_u(num, filled); say(num); say(" bytes\n");

    /* 第二步：读走 100 字节，腾出一点点空间 */
    char drain[100];
    ssize_t got = read(fds[0], drain, sizeof drain);
    say("drained "); put_u(num, got); say(num); say(" bytes to make room\n");

    /* 第三步：再写一大块，只能写出腾出的那 100 字节 → 短写 */
    ssize_t w = write(fds[1], buf, sizeof buf);
    if (w >= 0) {
        say("write #after-drain: asked "); put_u(num, (long)sizeof buf); say(num);
        say(" bytes, wrote "); put_u(num, (long)w); say(num);
        say(" bytes (SHORT WRITE)\n");
    } else {
        say("write after drain failed\n");
    }

    close(fds[0]);
    close(fds[1]);
    return 0;
}
