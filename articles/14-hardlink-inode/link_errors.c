#define _DARWIN_C_SOURCE
#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

static int show_failure(const char *label, int rc, int expected_errno)
{
    if (rc == 0) {
        fprintf(stderr, "%s unexpectedly succeeded\n", label);
        return -1;
    }
    if (errno != expected_errno) {
        fprintf(stderr, "%s: expected %s, got %s\n", label,
                strerror(expected_errno), strerror(errno));
        return -1;
    }
    printf("%s: %s\n", label, strerror(errno));
    return 0;
}

int main(void)
{
    char directory[] = "hardlink-errors-XXXXXX";
    if (mkdtemp(directory) == NULL) {
        perror("mkdtemp");
        return EXIT_FAILURE;
    }
    char source[64];
    char target[64];
    char dir[64];
    int a = snprintf(source, sizeof source, "%s/source", directory);
    int b = snprintf(target, sizeof target, "%s/target", directory);
    int c = snprintf(dir, sizeof dir, "%s/subdir", directory);
    if (a < 0 || b < 0 || c < 0 || (size_t)a >= sizeof source ||
        (size_t)b >= sizeof target || (size_t)c >= sizeof dir) {
        fprintf(stderr, "path construction failed\n");
        return EXIT_FAILURE;
    }
    int fd = open(source, O_WRONLY | O_CREAT | O_EXCL, 0600);
    if (fd == -1) { perror("open"); return EXIT_FAILURE; }
    if (close(fd) == -1) { perror("close"); return EXIT_FAILURE; }
    if (mkdir(dir, 0700) == -1) { perror("mkdir"); return EXIT_FAILURE; }

    int status = EXIT_FAILURE;
    if (show_failure("existing destination", link(source, source), EEXIST) == -1)
        goto cleanup;
    if (show_failure("directory source", link(dir, target), EPERM) == -1)
        goto cleanup;
    status = EXIT_SUCCESS;
cleanup:
    if (unlink(source) == -1) perror("cleanup source");
    if (unlink(target) == -1 && errno != ENOENT) perror("cleanup target");
    if (rmdir(dir) == -1) perror("cleanup directory");
    if (rmdir(directory) == -1) perror("cleanup root");
    return status;
}
