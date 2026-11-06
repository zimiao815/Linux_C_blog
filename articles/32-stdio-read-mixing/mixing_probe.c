#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
int read_one_via_fd(FILE *fp, unsigned char *out);

int main(void)
{
    FILE *fp = tmpfile();
    if (fp == NULL) return 1;
    int status = 1;
    unsigned char a = 0, b = 0, c = 0;
    if (fputs("abcdefghijklmnopqrstuvwxyz", fp) == EOF ||
        fseek(fp, 0, SEEK_SET) != 0)
        goto done;

    if (fread(&a, 1, 1, fp) != 1)
        goto done;
    long before = ftell(fp);
    if (before == -1 || read_one_via_fd(fp, &b) != 1)
        goto done;
    long after = ftell(fp);
    if (after == -1 || fread(&c, 1, 1, fp) != 1)
        goto done;
    long end = ftell(fp);
    if (end == -1) goto done;

    if (printf("fread=%c pos=%ld\nread=%c pos=%ld\nfread_again=%c pos=%ld\n",
               a, before, b, after, c, end) < 0)
        goto done;
    status = !(a == 'a' && b == 'b' && c == 'c' &&
               before == 1 && after == 2 && end == 3);
done:
    if (fclose(fp) == EOF) status = 1;
    return status;
}
