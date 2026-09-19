#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void die(const char *message)
{
    perror(message);
    exit(EXIT_FAILURE);
}

static off_t current_offset(int fd)
{
    off_t offset = lseek(fd, 0, SEEK_CUR);
    if (offset == (off_t)-1) {
        die("lseek");
    }
    return offset;
}

int main(void)
{
    const char *path = "dup_demo_data.txt";
    const char *redirect_path = "dup_demo_stdout.txt";
    int fd = open(path, O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (fd == -1) {
        die("open data");
    }

    const char initial[] = "abc";
    if (write(fd, initial, sizeof(initial) - 1U) != (ssize_t)(sizeof(initial) - 1U)) {
        die("write initial");
    }

    int duplicate = dup(fd);
    if (duplicate == -1) {
        die("dup");
    }
    printf("original fd = %d, duplicate fd = %d\n", fd, duplicate);

    if (lseek(fd, 1, SEEK_SET) == (off_t)-1) {
        die("lseek set");
    }
    printf("after lseek(original, 1): original offset = %lld, duplicate offset = %lld\n",
           (long long)current_offset(fd), (long long)current_offset(duplicate));

    const char replacement = 'X';
    ssize_t written = write(duplicate, &replacement, sizeof(replacement));
    if (written != (ssize_t)sizeof(replacement)) {
        die("write duplicate");
    }
    printf("write(duplicate, \"X\", 1) = %lld, original offset = %lld, duplicate offset = %lld\n",
           (long long)written, (long long)current_offset(fd), (long long)current_offset(duplicate));

    if (lseek(fd, 0, SEEK_SET) == (off_t)-1) {
        die("lseek readback");
    }
    char content[4] = {0};
    ssize_t read_count = read(fd, content, sizeof(content) - 1U);
    if (read_count != 3) {
        die("readback");
    }
    printf("file content = %s\n", content);

    int saved_stdout = dup(STDOUT_FILENO);
    if (saved_stdout == -1) {
        die("dup stdout");
    }
    int output = open(redirect_path, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (output == -1) {
        die("open redirect");
    }
    if (dup2(output, STDOUT_FILENO) == -1) {
        die("dup2");
    }
    if (close(output) == -1) {
        die("close redirect fd");
    }
    if (dprintf(STDOUT_FILENO, "hello through dup2\n") < 0) {
        die("dprintf redirected");
    }
    if (dup2(saved_stdout, STDOUT_FILENO) == -1) {
        die("restore stdout");
    }
    if (close(saved_stdout) == -1) {
        die("close saved stdout");
    }

    int captured = open(redirect_path, O_RDONLY);
    if (captured == -1) {
        die("open captured");
    }
    char line[64] = {0};
    ssize_t line_count = read(captured, line, sizeof(line) - 1U);
    if (line_count < 0) {
        die("read captured");
    }
    if (line_count > 0 && line[line_count - 1] == '\n') {
        line[line_count - 1] = '\0';
    }
    printf("redirected output = %s\n", line);

    if (close(captured) == -1 || close(duplicate) == -1 || close(fd) == -1) {
        die("close");
    }
    if (unlink(path) == -1 || unlink(redirect_path) == -1) {
        die("unlink");
    }
    return EXIT_SUCCESS;
}
