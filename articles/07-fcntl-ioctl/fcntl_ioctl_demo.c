#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <unistd.h>

int main(void)
{
    const char *path = "fcntl_demo.txt";
    int fd = open(path, O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (fd == -1) {
        perror("open");
        return EXIT_FAILURE;
    }

    int before = fcntl(fd, F_GETFL);
    if (before == -1) {
        perror("fcntl(F_GETFL)");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    if (fcntl(fd, F_SETFL, before | O_APPEND) == -1) {
        perror("fcntl(F_SETFL)");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    int after = fcntl(fd, F_GETFL);
    if (after == -1) {
        perror("fcntl(F_GETFL)");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    printf("fcntl O_APPEND: before=%s after=%s\n",
           (before & O_APPEND) != 0 ? "on" : "off",
           (after & O_APPEND) != 0 ? "on" : "off");

    int copy = fcntl(fd, F_DUPFD_CLOEXEC, 0);
    if (copy == -1) {
        perror("fcntl(F_DUPFD_CLOEXEC)");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    printf("fcntl duplicated fd: original=%d copy=%d\n", fd, copy);

    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe");
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    if (write(pipefd[1], "abc", 3) != 3) {
        perror("write pipe");
        (void)close(pipefd[0]);
        (void)close(pipefd[1]);
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    int available = 0;
    if (ioctl(pipefd[0], FIONREAD, &available) == -1) {
        perror("ioctl(FIONREAD)");
        (void)close(pipefd[0]);
        (void)close(pipefd[1]);
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    printf("ioctl FIONREAD: %d bytes\n", available);

    if (close(pipefd[0]) == -1 || close(pipefd[1]) == -1 ||
        close(copy) == -1 || close(fd) == -1) {
        perror("close");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
