#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int main(void) {
    /* 同一文件开两次，各自的偏移量是否独立 */
    int fd1 = open("offset.txt", O_RDONLY);
    int fd2 = open("offset.txt", O_RDONLY);
    if (fd1 < 0 || fd2 < 0) {
        fprintf(stderr, "open: %s\n", strerror(errno));
        return 1;
    }

    char c1, c2;
    read(fd1, &c1, 1);   /* fd1 读第 1 个字节 */
    read(fd2, &c2, 1);   /* fd2 也读第 1 个字节，而不是第 2 个 */

    printf("fd1 read 1 byte: '%c'\n", c1);
    printf("fd2 read 1 byte: '%c'\n", c2);
    printf("fd1 offset = %lld, fd2 offset = %lld\n",
           (long long)lseek(fd1, 0, SEEK_CUR),
           (long long)lseek(fd2, 0, SEEK_CUR));

    close(fd1);
    close(fd2);
    return 0;
}
