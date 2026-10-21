/* 与 copy_stream.c 一起编译，失败时立即诊断 */
#include <stdio.h>
int copy_stream(FILE *, FILE *);
int main(void)
{
    if (copy_stream(stdin, stdout) == -1) {
        perror("copy_stream"); return 1;
    }
    return 0;
}
