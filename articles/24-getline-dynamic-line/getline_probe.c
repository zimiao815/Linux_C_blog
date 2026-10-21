#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

int main(void)
{
    char *line = NULL;
    size_t cap = 0;
    ssize_t len;
    int count = 0;

    while ((len = getline(&line, &cap, stdin)) != -1) {
        int newline = len > 0 && line[len - 1] == '\n';
        if (printf("line=%d len=%zd cap=%zu newline=%d\n",
                   ++count, len, cap, newline) < 0) {
            free(line);
            return 1;
        }
    }
    if (ferror(stdin)) {
        perror("getline");
        free(line);
        return 1;
    }
    if (printf("done lines=%d eof=%d\n", count, feof(stdin) != 0) < 0) {
        free(line);
        return 1;
    }
    free(line);
    return 0;
}
