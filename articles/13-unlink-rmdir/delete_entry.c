#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 3 || (strcmp(argv[1], "unlink") != 0 &&
                      strcmp(argv[1], "rmdir") != 0)) {
        fprintf(stderr, "usage: %s unlink|rmdir PATH\n", argv[0]);
        return EXIT_FAILURE;
    }

    int rc = strcmp(argv[1], "unlink") == 0
           ? unlink(argv[2]) : rmdir(argv[2]);
    if (rc == -1) {
        int saved = errno;
        fprintf(stderr, "%s %s: %s\n", argv[1], argv[2], strerror(saved));
        return EXIT_FAILURE;
    }
    if (printf("%s %s: ok\n", argv[1], argv[2]) < 0 ||
        fflush(stdout) == EOF) {
        perror("stdout");
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
