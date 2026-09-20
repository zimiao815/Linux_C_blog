#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void die(const char *message)
{
    perror(message);
    exit(EXIT_FAILURE);
}

static void write_all(int fd, const char *label, const char *text)
{
    size_t remaining = 0U;
    while (text[remaining] != '\0') {
        remaining++;
    }
    size_t offset = 0U;
    while (offset < remaining) {
        ssize_t count = write(fd, text + offset, remaining - offset);
        if (count < 0) {
            die("write");
        }
        if (count == 0) {
            fprintf(stderr, "write returned zero\n");
            exit(EXIT_FAILURE);
        }
        offset += (size_t)count;
    }
    printf("write(%s) = %zu\n", label, remaining);
}

int main(void)
{
    int data_fd = open("sync_data.txt", O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (data_fd == -1) {
        die("open data");
    }
    write_all(data_fd, "data", "payload-123\n");
    if (fsync(data_fd) == -1) {
        die("fsync data");
    }
    printf("fsync(data) = 0\n");
    if (close(data_fd) == -1) {
        die("close data");
    }

    int meta_fd = open("sync_meta.txt", O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (meta_fd == -1) {
        die("open meta");
    }
    write_all(meta_fd, "meta", "payload-123\n");
    if (fdatasync(meta_fd) == -1) {
        die("fdatasync meta");
    }
    printf("fdatasync(meta) = 0\n");
    if (close(meta_fd) == -1) {
        die("close meta");
    }

    sync();
    puts("sync() requested");

    if (unlink("sync_data.txt") == -1 || unlink("sync_meta.txt") == -1) {
        die("unlink");
    }
    return EXIT_SUCCESS;
}
