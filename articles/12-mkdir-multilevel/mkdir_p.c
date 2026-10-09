#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

static int ensure_directory(const char *path, mode_t mode)
{
    if (mkdir(path, mode) == 0)
        return 0;

    if (errno != EEXIST)
        return -1;

    struct stat st;
    if (stat(path, &st) == -1)
        return -1;
    if (!S_ISDIR(st.st_mode)) {
        errno = ENOTDIR;
        return -1;
    }
    return 0;
}

static int mkdir_p(const char *path, mode_t mode)
{
    if (path == NULL || path[0] == '\0') {
        errno = EINVAL;
        return -1;
    }

    char *copy = strdup(path);
    if (copy == NULL)
        return -1;

    size_t length = strlen(copy);
    while (length > 1U && copy[length - 1U] == '/') {
        copy[--length] = '\0';
    }

    for (size_t i = 1U; i <= length; ++i) {
        if (copy[i] != '/' && copy[i] != '\0')
            continue;

        char saved = copy[i];
        copy[i] = '\0';
        if (copy[0] != '\0' && strcmp(copy, ".") != 0 &&
            ensure_directory(copy, mode) == -1) {
            int saved_errno = errno;
            free(copy);
            errno = saved_errno;
            return -1;
        }
        copy[i] = saved;
    }

    free(copy);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s DIRECTORY\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (mkdir_p(argv[1], 0777) == -1) {
        int saved_errno = errno;
        fprintf(stderr, "%s: %s\n", argv[1], strerror(saved_errno));
        return EXIT_FAILURE;
    }

    printf("ok: %s\n", argv[1]);
    return EXIT_SUCCESS;
}
