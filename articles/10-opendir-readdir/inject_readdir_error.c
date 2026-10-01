/* Test-only wrapper: inject EIO after one non-dot entry has been returned. */
#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int article_main(int argc, char **argv);
static int fail_next;

struct dirent *injected_readdir(DIR *dir)
{
    const char *mode = getenv("READDIR_TEST_MODE");
    int stale = mode != NULL && strcmp(mode, "stale") == 0;
    if (fail_next && !stale) {
        errno = EIO;
        return NULL;
    }
    struct dirent *entry = readdir(dir);
    if (entry != NULL && strcmp(entry->d_name, ".") != 0 &&
        strcmp(entry->d_name, "..") != 0) {
        fail_next = 1;
        if (stale) errno = EACCES;
    }
    return entry;
}

int main(int argc, char **argv)
{
    return article_main(argc, argv);
}
