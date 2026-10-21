#include <stdio.h>
int save_record(const char *, const char *);
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    if (save_record(argv[1], "record=42\n") == -1) {
        perror("save_record"); return 1;
    }
    return 0;
}
