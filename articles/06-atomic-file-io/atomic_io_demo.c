#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static int write_all(int fd, const char *buf, size_t len)
{
    size_t done = 0;
    while (done < len) {
        ssize_t n = write(fd, buf + done, len - done);
        if (n < 0) {
            if (errno == EINTR) {
                continue;
            }
            return -1;
        }
        if (n == 0) {
            errno = EIO;
            return -1;
        }
        done += (size_t)n;
    }
    return 0;
}

static int count_lines(const char *path)
{
    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        return -1;
    }
    char buf[256];
    int lines = 0;
    for (;;) {
        ssize_t n = read(fd, buf, sizeof buf);
        if (n == 0) {
            break;
        }
        if (n < 0) {
            if (errno == EINTR) {
                continue;
            }
            (void)close(fd);
            return -1;
        }
        for (ssize_t i = 0; i < n; ++i) {
            if (buf[i] == '\n') {
                ++lines;
            }
        }
    }
    if (close(fd) == -1) {
        return -1;
    }
    return lines;
}

static int append_worker(const char *path, int worker)
{
    int fd = open(path, O_WRONLY | O_APPEND);
    if (fd == -1) {
        return EXIT_FAILURE;
    }
    for (int i = 0; i < 5; ++i) {
        char line[32];
        int length = snprintf(line, sizeof line, "worker-%d record-%d\n", worker, i);
        if (length < 0 || (size_t)length >= sizeof line ||
            write_all(fd, line, (size_t)length) == -1) {
            (void)close(fd);
            return EXIT_FAILURE;
        }
    }
    if (close(fd) == -1) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

int main(void)
{
    const char *append_path = "atomic_append.txt";
    const char *position_path = "atomic_position.txt";
    const char *target_path = "atomic_target.txt";
    const char *temp_path = "atomic_target.tmp";

    int fd = open(append_path, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd == -1 || close(fd) == -1) {
        perror("create append file");
        return EXIT_FAILURE;
    }

    pid_t first = fork();
    if (first == -1) {
        perror("fork");
        return EXIT_FAILURE;
    }
    if (first == 0) {
        return append_worker(append_path, 1);
    }
    pid_t second = fork();
    if (second == -1) {
        perror("fork");
        return EXIT_FAILURE;
    }
    if (second == 0) {
        return append_worker(append_path, 2);
    }
    int status = 0;
    if (waitpid(first, &status, 0) == -1 || !WIFEXITED(status) || WEXITSTATUS(status) != 0 ||
        waitpid(second, &status, 0) == -1 || !WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "append worker failed\n");
        return EXIT_FAILURE;
    }
    int lines = count_lines(append_path);
    if (lines < 0) {
        perror("count lines");
        return EXIT_FAILURE;
    }
    printf("O_APPEND records = %d (expected 10)\n", lines);

    fd = open(position_path, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd == -1) {
        perror("open position file");
        return EXIT_FAILURE;
    }
    if (ftruncate(fd, 10) == -1 || pwrite(fd, "LEFT", 4, 0) != 4 ||
        pwrite(fd, "RIGHT", 5, 5) != 5 || close(fd) == -1) {
        perror("pwrite");
        return EXIT_FAILURE;
    }
    printf("pwrite offsets = 0 and 5 (non-overlapping)\n");

    fd = open(temp_path, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd == -1 || write_all(fd, "complete-new-file\n", 18) == -1 ||
        fsync(fd) == -1 || close(fd) == -1 || rename(temp_path, target_path) == -1) {
        perror("write and rename");
        return EXIT_FAILURE;
    }
    printf("rename replacement = complete-new-file\n");
    return EXIT_SUCCESS;
}
