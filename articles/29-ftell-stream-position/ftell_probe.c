#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    const char text[] = "abcdefghijklmnopqrstuvwxyz";
    FILE *fp = tmpfile();
    if (fp == NULL || fwrite(text, 1, sizeof text - 1, fp) != sizeof text - 1)
        return 1;
    fflush(fp);
    rewind(fp);

    int ch = fgetc(fp);
    long logical = ftell(fp);
    off_t raw = lseek(fileno(fp), 0, SEEK_CUR);
    if (printf("read=%c ftell=%ld fd_offset=%lld\n",
               ch, logical, (long long)raw) < 0)
        return 1;

    if (fseek(fp, 10, SEEK_SET) != 0)
        return 1;
    ch = fgetc(fp);
    logical = ftell(fp);
    raw = lseek(fileno(fp), 0, SEEK_CUR);
    if (printf("after_fseek=%c ftell=%ld fd_offset=%lld\n",
               ch, logical, (long long)raw) < 0)
        return 1;

    return fclose(fp) == EOF;
}
