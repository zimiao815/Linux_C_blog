#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 2 || (strcmp(argv[1], "newline") != 0 &&
                      strcmp(argv[1], "partial") != 0 &&
                      strcmp(argv[1], "flush") != 0)) {
        fprintf(stderr, "usage: %s newline|partial|flush\n", argv[0]);
        return EXIT_FAILURE;
    }

    int status = EXIT_FAILURE;
    const char *text = strcmp(argv[1], "partial") == 0
                       ? "ready> " : "ready\n";
    if (printf("%s", text) < 0) {
        perror("printf ready");
        goto cleanup;
    }
    if (strcmp(argv[1], "flush") == 0 && fflush(stdout) == EOF) {
        perror("fflush checkpoint");
        goto cleanup;
    }
    if (fprintf(stderr, "[checkpoint] press Enter\n") < 0 ||
        fflush(stderr) == EOF) {
        perror("stderr checkpoint");
        goto cleanup;
    }

    char ch;
    ssize_t n;
    do {
        n = read(STDIN_FILENO, &ch, 1);
    } while (n == -1 && errno == EINTR);
    if (n == -1) {
        perror("read gate");
        goto cleanup;
    }
    if (n == 0) {
        fprintf(stderr, "stdin ended before release\n");
        goto cleanup;
    }
    if (printf("done\n") < 0) {
        perror("printf done");
        goto cleanup;
    }
    status = EXIT_SUCCESS;

cleanup:
    if (fflush(stdout) == EOF) {
        perror("fflush final");
        status = EXIT_FAILURE;
    }
    return status;
}
