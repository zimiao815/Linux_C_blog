#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int report_to_memory(char *buf, size_t cap, size_t count);

static int fixed_case(size_t cap, int success)
{
    unsigned char area[32];
    memset(area, 0xa5, sizeof area);
    int rc = report_to_memory((char *)area, cap, 3);
    int err = errno;
    for (size_t i = cap; i < sizeof area; ++i)
        if (area[i] != 0xa5) return 1;
    if (success) {
        if (rc != 0 || strcmp((char *)area, "count=3\n") != 0) return 1;
    } else if (rc != -1 || err != (cap == 0 ? EINVAL : ENOSPC)) return 1;
    printf("fixed cap=%zu success=%d bounds=ok\n", cap, success);
    return 0;
}
static int dynamic_case(size_t count)
{
    char *text = NULL;
    size_t len = 0;
    FILE *fp = open_memstream(&text, &len);
    if (fp == NULL) return 1;
    int failed = 1;
    for (size_t i = 0; i < count; ++i)
        if (fputc((int)(i % 256), fp) == EOF) goto done;
    if (fflush(fp) == EOF || len != count || text[len] != 0) goto done;
    for (size_t i = 0; i < count; ++i)
        if ((unsigned char)text[i] != (unsigned char)(i % 256)) goto done;
    if (fputc('X', fp) == EOF) goto done;
    failed = 0;
done:
    if (fclose(fp) == EOF) return 1;
    if (!failed && (len != count + 1 || text[count] != 'X' || text[len] != 0))
        failed = 1;
    if (!failed) printf("dynamic bytes=%zu final_len=%zu content=ok\n", count, len);
    free(text);
    return failed;
}
int main(void)
{
    return fixed_case(16, 1) || fixed_case(9, 1) || fixed_case(8, 0) ||
           fixed_case(4, 0) || fixed_case(0, 0) ||
           dynamic_case(0) || dynamic_case(8) || dynamic_case(20000);
}
