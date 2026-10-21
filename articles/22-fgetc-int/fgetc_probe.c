#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 2; ++i) { /* 只观察两次，不运行错误循环 */
        int ch = fgetc(stdin);   /* 先保留原始返回值 */
        if (ferror(stdin)) { perror("fgetc"); return 1; }
        char small = (char)ch;   /* 故意缩窄，观察丢失的信息 */
        if (printf("int=%d char=%d eof=%d\n",
                   ch, (int)small, feof(stdin) != 0) < 0) {
            perror("printf"); return 1;
        }
    }
    if (fflush(stdout) == EOF) { perror("fflush"); return 1; }
    return 0;
}
