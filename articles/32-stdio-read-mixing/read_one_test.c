#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stddef.h>
int read_one_via_fd(FILE *fp, unsigned char *out);

static int test(size_t length)
{
    FILE *fp = tmpfile();
    if (fp == NULL) return 1;
    int status = 1;
    for (size_t i = 0; i < length; ++i)
        if (fputc((int)(i % 256), fp) == EOF) goto done;
    if (fseek(fp, 0, SEEK_SET) != 0) goto done;
    // 先进入输入阶段，空文件会设置 EOF。
    unsigned char byte;
    size_t first = fread(&byte, 1, 1, fp);
    if (first != (length > 0 ? 1u : 0u)) goto done;
    if (first && byte != 0) goto done;
    if (ferror(fp)) goto done;
    for (size_t i = first; i < length; ++i) {
        int n = i % 2 ? read_one_via_fd(fp, &byte)
                      : (int)fread(&byte, 1, 1, fp);
        if (n != 1 || byte != (unsigned char)(i % 256)) goto done;
    }
    if (read_one_via_fd(fp, &byte) != 0) goto done;
    if (fread(&byte, 1, 1, fp) != 0 || !feof(fp) || ferror(fp)) goto done;
    printf("length=%zu exact=1 eof=1\n", length);
    status = 0;
done:
    if (fclose(fp) == EOF) status = 1;
    return status;
}
int main(void)
{
    return test(0) || test(1) || test(26) || test(10000);
}
