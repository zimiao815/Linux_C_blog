#define _POSIX_C_SOURCE 200809L

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
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
    printf("fcntl O_APPEND: before=%s after=%s\n",
           (before & O_APPEND) != 0 ? "on" : "off",
           (after & O_APPEND) != 0 ? "on" : "off");
    printf("fcntl duplicated fd: original=%d copy=%d\n", fd, copy);
    int pipefd[2];
    if (pipe(pipefd) == -1 || write(pipefd[1], "abc", 3) != 3) return EXIT_FAILURE;
    int available = 0;
    if (ioctl(pipefd[0], FIONREAD, &available) == -1) return EXIT_FAILURE;
    printf("ioctl FIONREAD: %d bytes\n", available);
    (void)close(pipefd[0]);
    (void)close(pipefd[1]);
    (void)close(copy);
    (void)close(fd);
    return EXIT_SUCCESS;
}
