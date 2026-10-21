#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("usage: read_loop FILE\n", stderr);
        return EXIT_FAILURE;
    }
    FILE *fp = fopen(argv[1], "rb");
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }
    int status = EXIT_SUCCESS;
    int ch;
    if (printf("start: eof=%d error=%d\n",
               feof(fp) != 0, ferror(fp) != 0) < 0) {
        perror("printf");
        status = EXIT_FAILURE;
        goto cleanup;
    }
    while ((ch = fgetc(fp)) != EOF) {
        /* Process only a successfully read byte. */
        if (printf("byte=%d eof=%d error=%d\n",
                   ch, feof(fp) != 0, ferror(fp) != 0) < 0) {
            perror("printf");
            status = EXIT_FAILURE;
            goto cleanup;
        }
    }
    {
        int has_error = ferror(fp) != 0;
        int read_error = has_error ? errno : 0;
        int at_end = feof(fp) != 0;
        if (has_error) {
            errno = read_error;
            perror("fgetc");
            status = EXIT_FAILURE;
        } else if (!at_end) {
            fputs("unexpected stream state\n", stderr);
            status = EXIT_FAILURE;
        }
        if (printf("stop: EOF eof=%d error=%d\n",
                   at_end, has_error) < 0) {
            perror("printf");
            status = EXIT_FAILURE;
        }
    }
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
