#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static int lock_region(int fd, short type)
{
    struct flock lock = {
        .l_type = type,
        .l_whence = SEEK_SET,
        .l_start = 0,
        .l_len = 1,
        .l_pid = 0
    };
    return fcntl(fd, F_SETLK, &lock);
}

int main(void)
{
    const char *path = "fcntl_demo.txt";
    int fd = open(path, O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (fd == -1) {
        perror("open");
        return EXIT_FAILURE;
    }

    int before = fcntl(fd, F_GETFL);
    if (before == -1 || fcntl(fd, F_SETFL, before | O_APPEND) == -1) {
        perror("fcntl flags");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    int after = fcntl(fd, F_GETFL);
    if (after == -1) {
        perror("fcntl get flags");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    printf("F_GETFL/F_SETFL: before=%s after=%s\n",
           (before & O_APPEND) != 0 ? "append" : "normal",
           (after & O_APPEND) != 0 ? "append" : "normal");

    int copy = fcntl(fd, F_DUPFD_CLOEXEC, 0);
    if (copy == -1) {
        perror("fcntl duplicate");
        (void)close(fd);
        return EXIT_FAILURE;
    }
    printf("F_DUPFD_CLOEXEC: original=%d copy=%d\n", fd, copy);
    (void)fflush(stdout);

    if (lock_region(fd, F_WRLCK) == -1) {
        perror("fcntl lock parent");
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    pid_t child = fork();
    if (child == -1) {
        perror("fork");
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    if (child == 0) {
        int result = lock_region(fd, F_WRLCK);
        int child_errno = errno;
        if (result == -1 && (child_errno == EACCES || child_errno == EAGAIN)) {
            printf("F_SETLK in child: blocked (%s)\n", strerror(child_errno));
            (void)fflush(stdout);
            _exit(EXIT_SUCCESS);
        }
        _exit(EXIT_FAILURE);
    }
    int status = 0;
    if (waitpid(child, &status, 0) == -1 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "child lock test failed\n");
        (void)close(copy);
        (void)close(fd);
        return EXIT_FAILURE;
    }
    if (lock_region(fd, F_UNLCK) == -1 || close(copy) == -1 || close(fd) == -1) {
        perror("unlock or close");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
