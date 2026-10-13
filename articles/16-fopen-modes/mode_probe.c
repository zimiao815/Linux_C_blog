#define _POSIX_C_SOURCE 200809L

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(int argc, char **argv)
{
    if (argc != 3 && argc != 4) {
        fprintf(stderr, "usage: %s mode path [text]\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *fp = fopen(argv[2], argv[1]);
    if (fp == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }

    int status = EXIT_FAILURE;
    int fd = fileno(fp);
    struct stat st;
    if (fd == -1) {
        perror("fileno");
        goto cleanup;
    }
    if (fstat(fd, &st) == -1) {
        perror("fstat");
        goto cleanup;
    }
    if (!S_ISREG(st.st_mode)) {
        fprintf(stderr, "experiment requires a regular file\n");
        goto cleanup;
    }
    if (printf("mode=%s opened_size=%jd\n",
               argv[1], (intmax_t)st.st_size) < 0) {
        perror("printf");
        goto cleanup;
    }

    if (argc == 4) {
        if (fseek(fp, 0L, SEEK_SET) != 0) {
            perror("fseek");
            goto cleanup;
        }
        if (fputs(argv[3], fp) == EOF) {
            perror("fputs");
            goto cleanup;
        }
    }
    status = EXIT_SUCCESS;

cleanup:
    if (fclose(fp) == EOF) {
        perror("fclose");
        status = EXIT_FAILURE;
    }
    if (fflush(stdout) == EOF) {
        perror("fflush stdout");
        status = EXIT_FAILURE;
    }
    return status;
}
