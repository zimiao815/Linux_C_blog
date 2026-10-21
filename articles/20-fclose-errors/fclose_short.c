#include <stdio.h>

int main(void)
{
    char buffer[4096];
    int failed = 0;
    /* 小记录先进入用户态缓冲，stdout 重定向到文件 */
    if (setvbuf(stdout, buffer, _IOFBF, sizeof buffer) != 0) {
        fputs("setvbuf failed\n", stderr); fclose(stdout); return 1;
    }
    if (fputs("record=42\n", stdout) == EOF) {
        perror("fputs"); failed = 1;
    } else if (fputs("fputs: accepted\n", stderr) == EOF) failed = 1;
    /* 关闭会刷新缓冲；返回后不再使用 stdout */
    if (fclose(stdout) == EOF) {
        perror("fclose"); failed = 1;
    } else if (fputs("fclose: success\n", stderr) == EOF) failed = 1;
    if (fflush(stderr) == EOF) failed = 1;
    return failed;
}
