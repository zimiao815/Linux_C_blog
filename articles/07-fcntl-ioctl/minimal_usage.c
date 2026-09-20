#define _POSIX_C_SOURCE 200809L

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    int fd = open("fcntl_demo.txt", O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (fd == -1) return EXIT_FAILURE;
    int before = fcntl(fd, F_GETFL);
    if (before == -1 || fcntl(fd, F_SETFL, before | O_APPEND) == -1) return EXIT_FAILURE;
    int after = fcntl(fd, F_GETFL);
    int copy = fcntl(fd, F_DUPFD_CLOEXEC, 0);
    if (after == -1 || copy == -1) return EXIT_FAILURE;
    printf("F_GETFL/F_SETFL: before=%s after=%s\n",
           (before & O_APPEND) != 0 ? "append" : "normal",
           (after & O_APPEND) != 0 ? "append" : "normal");
    printf("F_DUPFD_CLOEXEC: original=%d copy=%d\n", fd, copy);
    (void)close(copy);
    (void)close(fd);
    return EXIT_SUCCESS;
}
