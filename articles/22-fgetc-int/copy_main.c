#include <stdio.h>

int copy_bytes(FILE *src, FILE *dst);

int main(void)
{
    if (copy_bytes(stdin, stdout) == -1) {
        perror("copy_bytes");
        return 1;
    }
    return 0;
}
