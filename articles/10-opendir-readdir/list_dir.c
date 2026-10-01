#define _POSIX_C_SOURCE 200809L

#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s DIRECTORY\n", argv[0]);
        return EXIT_FAILURE;
    }

    DIR *dir = opendir(argv[1]);
    if (dir == NULL) {
        int saved = errno;
        fprintf(stderr, "opendir %s: %s\n", argv[1], strerror(saved));
        return EXIT_FAILURE;
    }

    int status = EXIT_SUCCESS;
    for (;;) {
        errno = 0;
        struct dirent *entry = readdir(dir);
        if (entry == NULL) {
            int saved = errno;
            if (saved != 0) {
                fprintf(stderr, "readdir %s: %s\n",
                        argv[1], strerror(saved));
                status = EXIT_FAILURE;
            }
            break;
        }

        if (strcmp(entry->d_name, ".") == 0 ||
            strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        if (printf("%s\n", entry->d_name) < 0) {
            int saved = errno;
            fprintf(stderr, "output: %s\n", strerror(saved));
            status = EXIT_FAILURE;
            break;
        }
    }

    if (closedir(dir) == -1) {
        int saved = errno;
        fprintf(stderr, "closedir %s: %s\n", argv[1], strerror(saved));
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF) {
        int saved = errno;
        fprintf(stderr, "flush output: %s\n", strerror(saved));
        status = EXIT_FAILURE;
    }
    return status;
}
