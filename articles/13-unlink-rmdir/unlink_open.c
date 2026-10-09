#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE_TO_UNLINK\n", argv[0]);
        return EXIT_FAILURE;
    }
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        perror("open");
        return EXIT_FAILURE;
    }
    int status = EXIT_FAILURE;
    if (unlink(argv[1]) == -1) {
        perror("unlink");
        goto done;
    }
    struct stat st;
    if (fstat(fd, &st) == -1) {
        perror("fstat");
        goto done;
    }
    if (printf("after unlink: nlink=%ju\n", (uintmax_t)st.st_nlink) < 0)
        goto output_error;

    char buffer[64];
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof buffer);
        if (n == -1) {
            if (errno == EINTR)
                continue;
            perror("read");
            goto done;
        }
        if (n == 0)
            break;
        if (fwrite(buffer, 1, (size_t)n, stdout) != (size_t)n)
            goto output_error;
    }
    status = EXIT_SUCCESS;
    goto done;
output_error:
    perror("stdout");
done:
    if (close(fd) == -1) {
        perror("close");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF) {
        perror("fflush");
        status = EXIT_FAILURE;
    }
    return status;
}
