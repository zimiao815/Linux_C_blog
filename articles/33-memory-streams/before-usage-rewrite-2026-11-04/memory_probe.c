#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int report_to_memory(char *buf, size_t cap, size_t count);

int main(void)
{
    char fixed[16];
    if (report_to_memory(fixed, sizeof fixed, 3) == -1)
        return 1;
    if (printf("fixed=%s", fixed) < 0) return 1;

    char *text = NULL;
    size_t len = 0;
    FILE *fp = open_memstream(&text, &len);
    if (fp == NULL) return 1;
    int failed = 1;
    if (fputs("hello", fp) == EOF || fflush(fp) == EOF)
        goto finish;
    if (printf("flushed len=%zu text=%s\n", len, text) < 0)
        goto finish;
    if (fputs(", C", fp) == EOF)
        goto finish;
    failed = 0;
finish:
    if (fclose(fp) == EOF) return 1; // 本实验进程直接结束，不再使用失败结果
    if (!failed && printf("closed len=%zu text=%s\n", len, text) < 0)
        failed = 1;
    free(text);                     // 成功关闭后，结果缓冲区由调用者释放
    return failed;
}
