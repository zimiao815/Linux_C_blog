#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>

/* Test-only probe: single-threaded; no descriptor allocation between
   fclose and fcntl. Never inspect the FILE pointer after fclose. */
int main(int argc, char **argv)
{
    char buffer[4096];
    if (argc != 2)
        return EXIT_FAILURE;
    FILE *fp = fopen(argv[1], "wx");
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }
    int status = EXIT_FAILURE;
    if (setvbuf(fp, buffer, _IOFBF, sizeof buffer) != 0) {
        fputs("setvbuf failed\n", stderr);
        goto cleanup;
    }
    int fd = fileno(fp);
    if (fd == -1) {
        perror("fileno");
        goto cleanup;
    }
    if (fputs("record=42\n", fp) == EOF) {
        perror("fputs");
        goto cleanup;
    }
    {
        int close_result = fclose(fp);
        int close_error = close_result == EOF ? errno : 0;
        fp = NULL;
        int probe_result = fcntl(fd, F_GETFD);
        int probe_error = probe_result == -1 ? errno : 0;
        if (printf("fclose_failed=%d efbig=%d fd_is_ebadf=%d\n",
                   close_result == EOF, close_error == EFBIG,
                   probe_result == -1 && probe_error == EBADF) < 0 ||
            fflush(stdout) == EOF)
            return EXIT_FAILURE;
        return probe_result == -1 && probe_error == EBADF
               ? EXIT_SUCCESS : EXIT_FAILURE;
    }
cleanup:
    if (fclose(fp) == EOF)
        perror("fclose cleanup");
    return status;
}
