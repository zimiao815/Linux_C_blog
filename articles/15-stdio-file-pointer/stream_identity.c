#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s input-file\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }

    int status = EXIT_FAILURE;
    int fd = fileno(fp);
    if (fd == -1) {
        perror("fileno");
        goto cleanup;
    }
    int initial_eof = !!feof(fp);
    int initial_error = !!ferror(fp);

    int first = fgetc(fp);
    if (ferror(fp)) {
        perror("first fgetc");
        goto cleanup;
    }
    int first_eof = !!feof(fp);
    int second = fgetc(fp);
    if (ferror(fp)) {
        perror("second fgetc");
        goto cleanup;
    }

    if (printf("fp=%p, fd=%d\n"
               "initial: eof=%d, error=%d\n"
               "first=%d, eof=%d\n"
               "second_is_EOF=%d, eof=%d, error=%d\n",
               (void *)fp, fd, initial_eof, initial_error,
               first, first_eof, second == EOF,
               !!feof(fp), !!ferror(fp)) < 0) {
        perror("printf");
        goto cleanup;
    }
    status = EXIT_SUCCESS;

cleanup:
    if (fclose(fp) == EOF) {
        perror("fclose");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF) {
        perror("fflush stdout");
        status = EXIT_FAILURE;
    }
    return status;
}
