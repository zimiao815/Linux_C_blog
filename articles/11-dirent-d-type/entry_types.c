#define _DEFAULT_SOURCE
#define _DARWIN_C_SOURCE
#define _POSIX_C_SOURCE 200809L

#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

static const char *mode_type(mode_t mode)
{
    if (S_ISREG(mode))  return "file";
    if (S_ISDIR(mode))  return "directory";
    if (S_ISLNK(mode))  return "symlink";
    if (S_ISFIFO(mode)) return "fifo";
    if (S_ISSOCK(mode)) return "socket";
    if (S_ISCHR(mode))  return "char-device";
    if (S_ISBLK(mode))  return "block-device";
    return "other";
}

static const char *entry_type(int base, const struct dirent *e,
                              int force_unknown, const char **source)
{
    unsigned char type = force_unknown ? DT_UNKNOWN : e->d_type;
    *source = "d_type";
    switch (type) {
    case DT_REG:  return "file";
    case DT_DIR:  return "directory";
    case DT_LNK:  return "symlink";
    case DT_FIFO: return "fifo";
    case DT_SOCK: return "socket";
    case DT_CHR:  return "char-device";
    case DT_BLK:  return "block-device";
    default: break;
    }

    struct stat st;
    int rc;
    do {
        rc = fstatat(base, e->d_name, &st, AT_SYMLINK_NOFOLLOW);
    } while (rc == -1 && errno == EINTR);
    if (rc == -1) return NULL;
    *source = "fstatat";
    return mode_type(st.st_mode);
}

int main(int argc, char **argv)
{
    if (argc < 2 || argc > 3 ||
        (argc == 3 && strcmp(argv[2], "--unknown") != 0)) {
        fprintf(stderr, "usage: %s DIRECTORY [--unknown]\n", argv[0]);
        return EXIT_FAILURE;
    }
    DIR *dir = opendir(argv[1]);
    if (dir == NULL) {
        perror("opendir");
        return EXIT_FAILURE;
    }
    int status = EXIT_SUCCESS;
    int base = dirfd(dir);
    if (base == -1) {
        perror("dirfd");
        status = EXIT_FAILURE;
        goto done;
    }
    for (;;) {
        errno = 0;
        struct dirent *e = readdir(dir);
        if (e == NULL) {
            if (errno != 0) {
                perror("readdir");
                status = EXIT_FAILURE;
            }
            break;
        }
        if (strcmp(e->d_name, ".") == 0 || strcmp(e->d_name, "..") == 0)
            continue;
        const char *source;
        const char *type = entry_type(base, e, argc == 3, &source);
        if (type == NULL) {
            int saved = errno;
            fprintf(stderr, "%s: %s\n", e->d_name, strerror(saved));
            status = EXIT_FAILURE;
            continue;
        }
        if (printf("%s  %s  via=%s\n", e->d_name, type, source) < 0) {
            perror("printf");
            status = EXIT_FAILURE;
            break;
        }
    }
done:
    if (closedir(dir) == -1) {
        perror("closedir");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF) {
        perror("fflush");
        status = EXIT_FAILURE;
    }
    return status;
}
