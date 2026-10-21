#include <stdio.h>
#include <string.h>

int main(void)
{
    char buf[8];
    int part = 0;

    while (fgets(buf, sizeof buf, stdin) != NULL) {
        size_t n = strlen(buf);
        int newline = n > 0 && buf[n - 1] == '\n';
        if (printf("part=%d len=%zu newline=%d\n",
                   ++part, n, newline) < 0)
            return 1;
    }
    if (ferror(stdin)) {
        perror("fgets");
        return 1;
    }
    return printf("done parts=%d eof=%d\n", part, feof(stdin) != 0) < 0;
}
