#include <stdio.h>

int copy_bytes(FILE *src, FILE *dst)
{
    int ch;
    while ((ch = fgetc(src)) != EOF) {
        /* 已排除 EOF，此时才能按需缩窄成字节 */
        unsigned char byte = (unsigned char)ch;
        if (fputc(byte, dst) == EOF)
            return -1; /* 输出失败也要向调用者报告 */
    }
    if (ferror(src))
        return -1;     /* 返回 EOF 也可能是读取错误 */
    return fflush(dst) == EOF ? -1 : 0;
}
