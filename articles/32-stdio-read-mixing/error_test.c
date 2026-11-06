#define _POSIX_C_SOURCE 200809L
#undef read
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
int read_one_via_fd(FILE *fp, unsigned char *out);
static int mode, calls;

// 测试构建中的替身：第一次注入 EINTR，或注入 EIO。
ssize_t test_read(int fd, void *buf, size_t count)
{
    ++calls;
    if (mode == 1) { errno = EIO; return -1; }
    if (calls == 1) { errno = EINTR; return -1; }
    return read(fd, buf, count);
}
int main(void)
{
    FILE *fp = tmpfile();
    if (fp == NULL) return 1;
    int status = 1;
    unsigned char c;
    if (fputs("abc", fp) == EOF || fseek(fp, 0, SEEK_SET) != 0 ||
        fread(&c, 1, 1, fp) != 1) goto done;
    if (read_one_via_fd(fp, &c) != 1 || c != 'b' || calls != 2) goto done;
    puts("injected_eintr retry=ok byte=b");
    mode = 1;
    int n = read_one_via_fd(fp, &c);
    if (n != -1 || errno != EIO) goto done;
    puts("injected_eio result=-1 errno_preserved=1");
    status = 0;
done:
    if (fclose(fp) == EOF) status = 1; // helper 只借用流
    return status;
}
