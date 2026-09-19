#define _POSIX_C_SOURCE 200809L
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>

static int write_all(int fd, const char *p, size_t n) {
    size_t done = 0;
    while (done < n) {
        ssize_t w = write(fd, p + done, n - done);
        if (w < 0) { if (errno == EINTR) continue; return -1; }
        if (w == 0) { errno = EIO; return -1; }
        done += (size_t)w;
    }
    return 0;
}

static int show_size(const char *name) {
    struct stat st;
    if (stat(name, &st) < 0) return -1;
    printf("file size = %lld bytes\n", (long long)st.st_size);
    return 0;
}

int main(void) {
    const char *name = "lseek-demo.tmp";
    unlink(name);
    int fd = open(name, O_CREAT | O_TRUNC | O_RDWR, 0600);
    if (fd < 0) { perror("open"); return 1; }
    if (write_all(fd, "abc", 3) < 0) { perror("write"); close(fd); return 1; }
    off_t pos = lseek(fd, 0, SEEK_CUR);
    if (pos < 0) { perror("lseek"); close(fd); return 1; }
    printf("after writing 3 bytes, offset = %lld\n", (long long)pos);
    pos = lseek(fd, 5, SEEK_SET);
    if (pos < 0) { perror("lseek"); close(fd); return 1; }
    printf("seek to offset 5, lseek returned = %lld\n", (long long)pos);
    if (write_all(fd, "Z", 1) < 0) { perror("write"); close(fd); return 1; }
    pos = lseek(fd, 0, SEEK_CUR);
    printf("after writing one byte, offset = %lld\n", (long long)pos);
    if (show_size(name) < 0) { perror("stat"); close(fd); return 1; }
    close(fd);

    fd = open(name, O_WRONLY | O_APPEND);
    if (fd < 0) { perror("open append"); unlink(name); return 1; }
    pos = lseek(fd, 0, SEEK_SET);
    if (pos < 0) { perror("append lseek"); close(fd); unlink(name); return 1; }
    printf("append fd seek to 0, offset = %lld\n", (long long)pos);
    if (write_all(fd, "Q", 1) < 0) { perror("append write"); close(fd); unlink(name); return 1; }
    pos = lseek(fd, 0, SEEK_CUR);
    printf("after O_APPEND write, offset = %lld\n", (long long)pos);
    if (show_size(name) < 0) { perror("stat"); close(fd); unlink(name); return 1; }
    close(fd); unlink(name); return 0;
}
