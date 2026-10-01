#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
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
    if (S_ISCHR(mode)) return "char-device";
    if (S_ISBLK(mode)) return "block-device";
    if (S_ISFIFO(mode)) return "fifo";
    if (S_ISSOCK(mode)) return "socket";
    return "unknown";
}

static int write_all(int fd, const char *data, size_t length)
{
    size_t written = 0;

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

static int print_stat(const char *path)
{
    struct stat st;

    if (stat(path, &st) == -1) {
        fprintf(stderr, "stat %s: %s\n", path, strerror(errno));
        return -1;
    }

    printf("%s: type=%s size=%lld inode=%llu nlink=%llu mode=%#o\n",
           path,
           file_type(st.st_mode),
           (long long)st.st_size,
           (unsigned long long)st.st_ino,
           (unsigned long long)st.st_nlink,
           (unsigned int)(st.st_mode & 07777));
    return 0;
}

int main(void)
{
    const char *file_path = "stat_demo_file.tmp";
    const char *dir_path = "stat_demo_dir.tmp";
    const char payload[] = "hello\n";
    int fd = -1;
    int status = EXIT_FAILURE;

    if (unlink(file_path) == -1 && errno != ENOENT) {
        fprintf(stderr, "unlink %s: %s\n", file_path, strerror(errno));
        return EXIT_FAILURE;
    }
    if (rmdir(dir_path) == -1 && errno != ENOENT) {
        fprintf(stderr, "rmdir %s: %s\n", dir_path, strerror(errno));
        return EXIT_FAILURE;
    }

    fd = open(file_path, O_WRONLY | O_CREAT | O_EXCL, 0640);
    if (fd == -1) {
        fprintf(stderr, "open %s: %s\n", file_path, strerror(errno));
        goto cleanup;
    }
    if (write_all(fd, payload, sizeof(payload) - 1U) == -1) {
        fprintf(stderr, "write %s: %s\n", file_path, strerror(errno));
        goto cleanup;
    }
    if (close(fd) == -1) {
        fprintf(stderr, "close %s: %s\n", file_path, strerror(errno));
        fd = -1;
        goto cleanup;
    }
    fd = -1;

    if (print_stat(file_path) == -1) goto cleanup;

    if (mkdir(dir_path, 0750) == -1) {
        fprintf(stderr, "mkdir %s: %s\n", dir_path, strerror(errno));
        goto cleanup;
    }
    if (print_stat(dir_path) == -1) goto cleanup;

    status = EXIT_SUCCESS;

cleanup:
    if (fd != -1 && close(fd) == -1) {
        fprintf(stderr, "close %s: %s\n", file_path, strerror(errno));
        status = EXIT_FAILURE;
    }
    if (unlink(file_path) == -1 && errno != ENOENT) {
        fprintf(stderr, "unlink %s: %s\n", file_path, strerror(errno));
        status = EXIT_FAILURE;
    }
    if (rmdir(dir_path) == -1 && errno != ENOENT) {
        fprintf(stderr, "rmdir %s: %s\n", dir_path, strerror(errno));
        status = EXIT_FAILURE;
    }
    return status;
}
