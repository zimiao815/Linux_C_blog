#include <stdio.h>

int main(void)
{
    char buf[5] = {0};
    FILE *fp = tmpfile();
    if (fp == NULL)
        return 1;

    if (fwrite("abc", 1, 3, fp) != 3 || fflush(fp) != 0 ||
        fseek(fp, 0, SEEK_SET) != 0)
        return 1;
    int first = fgetc(fp);

    if (fseek(fp, 0, SEEK_END) != 0 || fwrite("X", 1, 1, fp) != 1 ||
        fflush(fp) != 0 || fseek(fp, 0, SEEK_SET) != 0)
        return 1;
    if (fread(buf, 1, sizeof buf - 1, fp) != sizeof buf - 1)
        return 1;

    if (printf("write_then_read=%c\nread_then_write=%s\n", first, buf) < 0)
        return 1;
    return fclose(fp) == EOF;
}
