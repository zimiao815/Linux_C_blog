#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    char buffer[4096];
    int status = EXIT_SUCCESS;

    if (argc != 3 ||
        (strcmp(argv[1], "buffered") != 0 &&
         strcmp(argv[1], "unbuffered") != 0 &&
         strcmp(argv[1], "flush-first") != 0)) {
        fputs("usage: fclose_probe buffered|unbuffered|flush-first NEW_FILE\n",
              stderr);
        return EXIT_FAILURE;
    }
    FILE *fp = fopen(argv[2], "wx");
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }
    int unbuffered = strcmp(argv[1], "unbuffered") == 0;
    if (setvbuf(fp, unbuffered ? NULL : buffer,
                unbuffered ? _IONBF : _IOFBF,
                unbuffered ? 0 : sizeof buffer) != 0) {
        fputs("setvbuf failed\n", stderr);
        status = EXIT_FAILURE;
        goto cleanup;
    }
    if (fputs("record=42\n", fp) == EOF) {
        perror("fputs");
        status = EXIT_FAILURE;
        goto cleanup;
    }
    if (fputs("fputs: accepted\n", stderr) == EOF)
        status = EXIT_FAILURE;

    if (strcmp(argv[1], "flush-first") == 0) {
        if (fflush(fp) == EOF) {
            perror("fflush");
            status = EXIT_FAILURE;
            goto cleanup;
        }
        if (fputs("fflush: success\n", stderr) == EOF)
            status = EXIT_FAILURE;
    }

cleanup:
    {
        int close_result = fclose(fp);
        int close_error = close_result == EOF ? errno : 0;
        fp = NULL;
        if (close_result == EOF) {
            errno = close_error;
            perror("fclose");
            status = EXIT_FAILURE;
        } else if (fputs("fclose: success\n", stderr) == EOF) {
            status = EXIT_FAILURE;
        }
    }
    if (fflush(stderr) == EOF)
        status = EXIT_FAILURE;
    return status;
}
