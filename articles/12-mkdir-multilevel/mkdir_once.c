#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s DIRECTORY\n", argv[0]);
        return EXIT_FAILURE;
    }
    if (mkdir(argv[1], 0777) == -1) {
        int saved_errno = errno;
        fprintf(stderr, "mkdir %s: %s\n", argv[1], strerror(saved_errno));
        return EXIT_FAILURE;
    }
    printf("created: %s\n", argv[1]);
    return EXIT_SUCCESS;
}
