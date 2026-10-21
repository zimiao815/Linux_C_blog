#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

static int state(const char *label, FILE *fp)
{
    return printf("%s eof=%d error=%d\n", label,
                  feof(fp) != 0, ferror(fp) != 0) < 0 ? -1 : 0;
}

int main(void)
{
    FILE *fp = tmpfile();
    if (fp == NULL) {
        perror("tmpfile");
        return EXIT_FAILURE;
    }
    int status = EXIT_FAILURE;
    if (fputs("A", fp) == EOF) {
        perror("fputs");
        goto cleanup;
    }
    if (fseek(fp, 0, SEEK_SET) != 0) {
        perror("fseek");
        goto cleanup;
    }
    if (fgetc(fp) != 'A' || state("after-byte", fp) == -1)
        goto cleanup;
    if (fgetc(fp) != EOF || ferror(fp) || state("after-end", fp) == -1)
        goto cleanup;
    if (fgetc(fp) != EOF || ferror(fp) || state("read-again", fp) == -1)
        goto cleanup;
    clearerr(fp);
    if (state("after-clearerr", fp) == -1)
        goto cleanup;
    if (fgetc(fp) != EOF || ferror(fp) || state("still-at-end", fp) == -1)
        goto cleanup;
    if (fseek(fp, 0, SEEK_SET) != 0) {
        perror("fseek");
        goto cleanup;
    }
    if (state("after-seek", fp) == -1 || fgetc(fp) != 'A')
        goto cleanup;
    status = EXIT_SUCCESS;
cleanup:
    if (fclose(fp) == EOF) {
        perror("fclose");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF)
        status = EXIT_FAILURE;
    return status;
}
