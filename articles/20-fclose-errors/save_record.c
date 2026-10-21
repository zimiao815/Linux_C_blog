#include <errno.h>
#include <stdio.h>

int save_record(const char *path, const char *text)
{
    FILE *fp = fopen(path, "wx"); /* 只新建，不覆盖旧文件 */
    if (fp == NULL) return -1;
    int error = 0;
    if (fputs(text, fp) == EOF)
        error = errno; /* 先保存写入错误，避免被清理覆盖 */
    if (fclose(fp) == EOF && error == 0)
        error = errno; /* 总会关闭一次；优先保留第一个错误 */
    /* fp 已失效，无论关闭是否成功，都不能再用 */
    if (error != 0) { errno = error; return -1; }
    return 0;
}
