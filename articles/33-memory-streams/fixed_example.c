#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char buf[16] = {0};
    FILE *fp = fmemopen(buf, sizeof buf, "w");
    if (fp == NULL) return 1;

    int n = fprintf(fp, "hello");
    int rc = fclose(fp);              // 关闭前，把尚未写出的内容送入 buf
    if (n < 0 || (size_t)n >= sizeof buf || rc == EOF)
        return 1;

    if (puts(buf) == EOF) return 1;
    return 0;
}
