#include <stdio.h>

int main(void)
{
    FILE *fp = tmpfile();
    int value = -1;
    int first;
    int second;
    int after_second;
    int blocked;
    int recovered;

    if (fp == NULL || fputs("42x\n7\n", fp) == EOF)
        return 1;
    rewind(fp);

    first = fscanf(fp, "%d", &value);
    second = fscanf(fp, "%d", &value);
    after_second = value;
    blocked = fgetc(fp);
    recovered = fscanf(fp, "%d", &value);
    if (printf("first=%d value=42\nsecond=%d value=%d\nblocked=%c\nrecovered=%d value=%d\n",
               first, second, after_second, blocked, recovered, value) < 0) {
        fclose(fp);
        return 1;
    }
    if (fclose(fp) == EOF)
        return 1;
    return 0;
}
