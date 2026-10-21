#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

/* Deliberately flawed condition, bounded for observation.
   No EOF result is processed as a byte. */
int main(int argc, char **argv)
{
    if (argc != 2)
        return EXIT_FAILURE;
    FILE *fp = fopen(argv[1], "rb");
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }
    int status = EXIT_SUCCESS;
    unsigned attempts = 0;
    while (!feof(fp) && attempts < 3U) {
        int ch = fgetc(fp);
        ++attempts;
        int result;
        if (ch == EOF)
            result = printf("step=%u result=EOF eof=%d error=%d\n",
                            attempts, feof(fp) != 0, ferror(fp) != 0);
        else
            result = printf("step=%u byte=%d eof=%d error=%d\n",
                            attempts, ch, feof(fp) != 0, ferror(fp) != 0);
        if (result < 0) {
            status = EXIT_FAILURE;
            break;
        }
    }
    if (ferror(fp))
        status = EXIT_FAILURE;
    if (attempts == 3U && !feof(fp)) {
        if (puts("cap reached; !feof still true") == EOF)
            status = EXIT_FAILURE;
    }
    if (fclose(fp) == EOF) {
        perror("fclose");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF)
        status = EXIT_FAILURE;
    return status;
}
