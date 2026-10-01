#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static const char *file_type(mode_t mode)
{
    if (S_ISREG(mode)) return "regular";
    if (S_ISDIR(mode)) return "directory";
    if (S_ISLNK(mode)) return "symlink";
    return "other";
}

static int write_all(int fd, const char *data, size_t length)
{
    size_t written = 0U;

    while (written < length) {
        ssize_t n = write(fd, data + written, length - written);
        if (n < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        if (n == 0) {
            errno = EIO;
            return -1;
        }
        written += (size_t)n;
    }
    return 0;
}

static int print_status(const char *label, const struct stat *st)
{
    printf("%s: type=%s size=%" PRIdMAX " inode=%" PRIuMAX "\n",
           label,
           file_type(st->st_mode),
           (intmax_t)st->st_size,
           (uintmax_t)st->st_ino);
    return 0;
}

static int query_stat(const char *label, const char *path, int follow)
{
    struct stat st;
    int result;

    errno = 0;
    result = follow ? stat(path, &st) : lstat(path, &st);
    if (result == -1) {
        printf("%s: %s errno=%d (%s)\n",
               label, follow ? "stat" : "lstat", errno, strerror(errno));
        return -1;
    }
    return print_status(label, &st);
}

int main(void)
{
    const char *target = "stat_lstat_target.tmp";
    const char *link = "stat_lstat_link.tmp";
    const char payload[] = "target data\n";
    int fd = -1;
    int status = EXIT_FAILURE;

    if (unlink(link) == -1 && errno != ENOENT) {
        fprintf(stderr, "unlink %s: %s\n", link, strerror(errno));
        return EXIT_FAILURE;
    }
    if (unlink(target) == -1 && errno != ENOENT) {
        fprintf(stderr, "unlink %s: %s\n", target, strerror(errno));
        return EXIT_FAILURE;
    }

    fd = open(target, O_WRONLY | O_CREAT | O_EXCL, 0640);
    if (fd == -1) {
        fprintf(stderr, "open %s: %s\n", target, strerror(errno));
        goto cleanup;
    }
    if (write_all(fd, payload, sizeof(payload) - 1U) == -1) {
        fprintf(stderr, "write %s: %s\n", target, strerror(errno));
        goto cleanup;
    }
    if (close(fd) == -1) {
        fprintf(stderr, "close %s: %s\n", target, strerror(errno));
        fd = -1;
        goto cleanup;
    }
    fd = -1;

    if (symlink(target, link) == -1) {
        fprintf(stderr, "symlink %s -> %s: %s\n",
                link, target, strerror(errno));
        goto cleanup;
    }

    if (query_stat("target via stat", target, 1) == -1) goto cleanup;
    if (query_stat("link via stat", link, 1) == -1) goto cleanup;
    if (query_stat("link via lstat", link, 0) == -1) goto cleanup;

    if (unlink(target) == -1) {
        fprintf(stderr, "unlink %s: %s\n", target, strerror(errno));
        goto cleanup;
    }

    (void)query_stat("broken link via stat", link, 1);
    (void)query_stat("broken link via lstat", link, 0);
    status = EXIT_SUCCESS;

cleanup:
    if (fd != -1 && close(fd) == -1) {
        fprintf(stderr, "close %s: %s\n", target, strerror(errno));
        status = EXIT_FAILURE;
    }
    if (unlink(link) == -1 && errno != ENOENT) {
        fprintf(stderr, "cleanup unlink %s: %s\n", link, strerror(errno));
        status = EXIT_FAILURE;
    }
    if (unlink(target) == -1 && errno != ENOENT) {
        fprintf(stderr, "cleanup unlink %s: %s\n", target, strerror(errno));
        status = EXIT_FAILURE;
    }
    return status;
}
