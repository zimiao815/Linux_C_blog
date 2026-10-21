#include <stdio.h>
int copy_stream(FILE *, FILE *);
int main(void)
{
    if (copy_stream(stdin, stdout) == -1) {
        perror("copy_stream"); return 1;
    }
    return 0;
}
