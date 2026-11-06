#include <stdio.h>

int main(void)
{
    unsigned char data[12] = {0};
    FILE *fp = tmpfile();
    if (fp == NULL)
        return 1;

    size_t n = fwrite(data, 4, 3, fp);
    int flushed = fflush(fp);
    long pos = ftell(fp);
    if (pos < 0 || printf("normal returned=%zu requested=3 bytes=%zu flush=%d pos=%ld error=%d\n",
                          n, n * 4, flushed, pos, ferror(fp) != 0) < 0) {
        fclose(fp);
        return 1;
    }
    if (fclose(fp) == EOF)
        return 1;

    FILE *readonly = fopen("/dev/null", "r");
    if (readonly == NULL)
        return 1;
    n = fwrite(data, 4, 3, readonly);
    if (printf("readonly returned=%zu requested=3 error=%d\n",
               n, ferror(readonly) != 0) < 0) {
        fclose(readonly);
        return 1;
    }
    if (fclose(readonly) == EOF)
        return 1;
    return 0;
}
