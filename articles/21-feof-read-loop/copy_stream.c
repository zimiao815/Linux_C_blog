#include <stdio.h>

int copy_stream(FILE *src, FILE *dst)
{
    int ch;
    while ((ch = fgetc(src)) != EOF) { /* 只复制有效字节 */
        if (fputc(ch, dst) == EOF)
            return -1; /* 写入错误立即向上传递 */
    }
    if (ferror(src))
        return -1;     /* 不能把读取错误当成正常结束 */
    return fflush(dst) == EOF ? -1 : 0; /* 还要检查输出刷新 */
}
