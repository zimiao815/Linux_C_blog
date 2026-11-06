#include <stdio.h>

int main(void)
{
    unsigned char src[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    unsigned char buf[12] = {0};
    FILE *fp = tmpfile();
    if (fp == NULL)
        return 1;
    if (fwrite(src, 1, sizeof src, fp) != sizeof src) {
        fclose(fp);
        return 1;
    }

    rewind(fp);
    size_t n = fread(buf, 4, 3, fp);
    long pos = ftell(fp);
    if (pos < 0 || printf("size=4 nmemb=3 returned=%zu complete_bytes=%zu pos=%ld eof=%d\n",
                          n, n * 4, pos, feof(fp) != 0) < 0) {
        fclose(fp);
        return 1;
    }

    rewind(fp);
    n = fread(buf, 1, sizeof src, fp);
    pos = ftell(fp);
    if (pos < 0 || printf("size=1 nmemb=10 returned=%zu complete_bytes=%zu pos=%ld eof=%d\n",
                          n, n, pos, feof(fp) != 0) < 0) {
        fclose(fp);
        return 1;
    }

    fclose(fp);
    return 0;
}
