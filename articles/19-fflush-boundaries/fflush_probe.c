#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    static char buffer[4096];
    int status = EXIT_FAILURE;
    int do_flush, do_sync;
    char release;
    ssize_t count;

    if (argc != 2 ||
        (strcmp(argv[1], "buffered") != 0 &&
         strcmp(argv[1], "flush") != 0 &&
         strcmp(argv[1], "sync-only") != 0 &&
         strcmp(argv[1], "flush-sync") != 0)) {
        fputs("usage: fflush_probe buffered|flush|sync-only|flush-sync\n",
              stderr);
        return EXIT_FAILURE;
    }
    do_flush = strcmp(argv[1], "flush") == 0 ||
               strcmp(argv[1], "flush-sync") == 0;
    do_sync = strcmp(argv[1], "sync-only") == 0 ||
              strcmp(argv[1], "flush-sync") == 0;

    if (setvbuf(stdout, buffer, _IOFBF, sizeof buffer) != 0) {
        fputs("setvbuf failed\n", stderr);
        goto cleanup;
    }
    if (fputs("record=42\n", stdout) == EOF) {
        perror("fputs stdout");
        goto cleanup;
    }
    if (fputs("fputs: accepted\n", stderr) == EOF ||
        fflush(stderr) == EOF)
        goto cleanup;

    if (do_flush && fflush(stdout) == EOF) {
        perror("fflush stdout");
        goto cleanup;
    }
    if (do_sync) {
        int fd = fileno(stdout);
        if (fd == -1) {
            perror("fileno stdout");
            goto cleanup;
        }
        int result;
        do {
            result = fsync(fd);
        } while (result == -1 && errno == EINTR);
        if (result == -1) {
            perror("fsync stdout");
            goto cleanup;
        }
    }
    if (fputs("checkpoint: inspect now\n", stderr) == EOF ||
        fflush(stderr) == EOF)
        goto cleanup;
    do {
        count = read(STDIN_FILENO, &release, 1);
    } while (count == -1 && errno == EINTR);
    if (count == -1) {
        perror("read gate");
        goto cleanup;
    }
    if (count == 0) {
        fputs("stdin ended before release\n", stderr);
        goto cleanup;
    }
    status = EXIT_SUCCESS;

cleanup:
    if (fclose(stdout) == EOF) {
        perror("fclose stdout");
        status = EXIT_FAILURE;
    }
    return status;
}
