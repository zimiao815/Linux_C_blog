#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int mode;
    if (argc != 3 ||
        (strcmp(argv[2], "newline") != 0 &&
         strcmp(argv[2], "partial") != 0)) {
        fprintf(stderr, "usage: %s full|line|none newline|partial\n",
                argv[0]);
        return EXIT_FAILURE;
    }
    if (strcmp(argv[1], "full") == 0) mode = _IOFBF;
    else if (strcmp(argv[1], "line") == 0) mode = _IOLBF;
    else if (strcmp(argv[1], "none") == 0) mode = _IONBF;
    else {
        fputs("unknown buffering mode\n", stderr);
        return EXIT_FAILURE;
    }

    static char buffer[4096];
    char *storage = mode == _IONBF ? NULL : buffer;
    size_t capacity = mode == _IONBF ? 0 : sizeof buffer;
    int status = EXIT_FAILURE;

    /* No earlier operation has used stdout. */
    if (setvbuf(stdout, storage, mode, capacity) != 0) {
        fputs("setvbuf failed\n", stderr);
        goto cleanup;
    }
    const char *text = strcmp(argv[2], "newline") == 0
                       ? "ready\n" : "ready> ";
    if (fputs(text, stdout) == EOF) {
        perror("fputs stdout");
        goto cleanup;
    }
    if (fputs("[checkpoint] press Enter\n", stderr) == EOF ||
        fflush(stderr) == EOF) {
        perror("checkpoint");
        goto cleanup;
    }

    /* POSIX read avoids an extra stdio input-triggered flush. */
    char key;
    ssize_t count;
    do {
        count = read(STDIN_FILENO, &key, 1);
    } while (count < 0 && errno == EINTR);
    if (count < 0) {
        perror("read stdin");
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
