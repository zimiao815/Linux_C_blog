#define _DARWIN_C_SOURCE
#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int write_all(int fd, const char *data, size_t length)
{
    size_t written = 0U;
    while (written < length) {
        ssize_t n = write(fd, data + written, length - written);
        if (n < 0) {
            if (errno == EINTR)
                continue;
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

static int print_stat(const char *label, const char *path)
{
    struct stat st;
    if (stat(path, &st) == -1)
        return -1;
    if (printf("%s: dev=%ju ino=%ju nlink=%ju size=%ju\n",
               label, (uintmax_t)st.st_dev, (uintmax_t)st.st_ino,
               (uintmax_t)st.st_nlink, (uintmax_t)st.st_size) < 0) {
        errno = EIO;
        return -1;
    }
    return 0;
}

static int read_and_print(const char *path)
{
    int fd = open(path, O_RDONLY);
    if (fd == -1)
        return -1;
    char buffer[64];
    int status = -1;
    for (;;) {
        ssize_t n = read(fd, buffer, sizeof buffer);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            goto done;
        }
        if (n == 0) {
            status = 0;
            break;
        }
        if (fwrite(buffer, 1, (size_t)n, stdout) != (size_t)n) {
            errno = EIO;
            goto done;
        }
    }
done:
    {
        int saved_errno = errno;
        if (close(fd) == -1) {
            status = -1;
            saved_errno = errno;
        }
        if (status == -1)
            errno = saved_errno;
    }
    return status;
}

int main(void)
{
    char directory[] = "hardlink-demo-XXXXXX";
    if (mkdtemp(directory) == NULL) {
        perror("mkdtemp");
        return EXIT_FAILURE;
    }

    char original[64];
    char second[64];
    int n1 = snprintf(original, sizeof original, "%s/original.txt", directory);
    int n2 = snprintf(second, sizeof second, "%s/second-name.txt", directory);
    if (n1 < 0 || n2 < 0 || (size_t)n1 >= sizeof original ||
        (size_t)n2 >= sizeof second) {
        fprintf(stderr, "path construction failed\n");
        rmdir(directory);
        return EXIT_FAILURE;
    }

    int status = EXIT_FAILURE;
    int fd = open(original, O_WRONLY | O_CREAT | O_EXCL, 0644);
    if (fd == -1) {
        perror("open");
        goto cleanup_directory;
    }
    const char content[] = "same inode, two names\n";
    if (write_all(fd, content, sizeof content - 1U) == -1) {
        perror("write");
        close(fd);
        goto cleanup_original;
    }
    if (close(fd) == -1) {
        perror("close");
        goto cleanup_original;
    }

    if (link(original, second) == -1) {
        perror("link");
        goto cleanup_original;
    }
    if (print_stat("original", original) == -1 ||
        print_stat("second", second) == -1) {
        perror("stat");
        goto cleanup_second;
    }

    if (unlink(original) == -1) {
        perror("unlink");
        goto cleanup_second;
    }
    if (printf("after unlink original: ") < 0 ||
        print_stat("second", second) == -1) {
        perror("output/stat");
        goto cleanup_second;
    }
    if (printf("content: ") < 0 || read_and_print(second) == -1 ||
        fflush(stdout) == EOF) {
        perror("read/output");
        goto cleanup_second;
    }
    status = EXIT_SUCCESS;

cleanup_second:
    if (unlink(second) == -1 && errno != ENOENT) {
        perror("cleanup second");
        status = EXIT_FAILURE;
    }
cleanup_original:
    if (unlink(original) == -1 && errno != ENOENT) {
        perror("cleanup original");
        status = EXIT_FAILURE;
    }
cleanup_directory:
    if (rmdir(directory) == -1) {
        perror("rmdir");
        status = EXIT_FAILURE;
    }
    return status;
}
