/*
 * rw_all.c — 工程上正确的「完整读 / 完整写」写法：循环 + 累计，
 * 三个终止条件：读满/写满、EOF（仅读）、真错误。EINTR 单独重试。
 *
 * 演示：read_all 从 data.txt 读 10 字节 → write_all 写到 copy.txt
 * → 再 read_all 读回来，验证两边一致。
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

/* 完整读：循环直到读满 n 字节、读到 EOF、或出错 */
static ssize_t read_all(int fd, void *buf, size_t n) {
    char *p = buf;
    size_t done = 0;
    while (done < n) {
        ssize_t r = read(fd, p + done, n - done);
        if (r < 0) {
            if (errno == EINTR)
                continue;              /* 被信号打断，重试 */
            return -1;                 /* 真正的错误 */
        }
        if (r == 0)
            break;                     /* EOF：读到头了，返回已读到的部分 */
        done += (size_t)r;
    }
    return (ssize_t)done;
}

/* 完整写：循环直到写满 n 字节，或出错 */
static ssize_t write_all(int fd, const void *buf, size_t n) {
    const char *p = buf;
    size_t done = 0;
    while (done < n) {
        ssize_t w = write(fd, p + done, n - done);
        if (w < 0) {
            if (errno == EINTR)
                continue;              /* 被信号打断，重试 */
            return -1;                 /* 真正的错误 */
        }
        done += (size_t)w;             /* 防短写：只累计实际写出的 */
    }
    return (ssize_t)done;
}

int main(void) {
    char buf[16];
    char num[24];

    int in = open("data.txt", O_RDONLY);
    if (in < 0) { say("open data.txt failed\n"); return 1; }

    ssize_t got = read_all(in, buf, 10);
    if (got < 0) { say("read_all failed\n"); return 1; }
    say("read_all got "); put_u(num, got); say(num); say(" bytes: [");
    write(1, buf, (size_t)got);
    say("]\n");
    close(in);

    int out = open("copy.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out < 0) { say("open copy.txt failed\n"); return 1; }
    if (write_all(out, buf, (size_t)got) < 0) { say("write_all failed\n"); return 1; }
    close(out);

    int back = open("copy.txt", O_RDONLY);
    if (back < 0) { say("open copy.txt failed\n"); return 1; }
    char buf2[16];
    ssize_t got2 = read_all(back, buf2, (size_t)got);
    if (got2 != got || memcmp(buf, buf2, (size_t)got) != 0) {
        say("copy mismatch!\n");
        return 1;
    }
    say("copy verified: write_all wrote all "); put_u(num, got); say(num); say(" bytes\n");
    close(back);
    return 0;
}
