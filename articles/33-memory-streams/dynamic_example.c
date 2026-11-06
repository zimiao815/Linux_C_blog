#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char *text = NULL;
    size_t len = 0;
    FILE *fp = open_memstream(&text, &len);
    if (fp == NULL) return 1;

    int n = fprintf(fp, "hello");
    if (fclose(fp) == EOF) return 1;   // 关闭失败时，本示例直接结束进程
    if (n < 0) {
        free(text);
        return 1;
    }

    int rc = printf("text=%s, len=%zu\n", text, len);
    free(text);                      // 先使用结果，再释放内存
    return rc < 0;
}
