#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

// 仅用于独占访问的 POSIX 普通可定位文件；调用前 fp 处于读取阶段。
// 返回 1=读到字节，0=文件结束，-1=失败（调用者停止本轮读取）。
// 借用 fp，不关闭流或 fd；out 指向可写的一个字节。
int read_one_via_fd(FILE *fp, unsigned char *out)
{
    int fd = fileno(fp);
    if (fd == -1 || fflush(fp) == EOF)
        return -1;                     // 先把流位置交给 fd

    ssize_t n;
    do {
        n = read(fd, out, 1);
    } while (n == -1 && errno == EINTR);
    if (n == -1)
        return -1;

    off_t pos = lseek(fd, 0, SEEK_CUR);  // 取得 read 后的偏移
    if (pos == (off_t)-1 || fseeko(fp, pos, SEEK_SET) != 0)
        return -1;                     // 再把位置交回流
    return (int)n;
}
