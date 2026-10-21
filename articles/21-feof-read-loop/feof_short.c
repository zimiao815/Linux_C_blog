#include <stdio.h>

int main(void)
{
    int ch, failed = 0;
    if (printf("start: eof=%d error=%d\n",
               feof(stdin) != 0, ferror(stdin) != 0) < 0) return 1;
    while ((ch = fgetc(stdin)) != EOF) { /* 读成功才处理 */
        if (printf("byte=%d eof=%d error=%d\n",
                   ch, feof(stdin) != 0, ferror(stdin) != 0) < 0)
            return 1;
    }
    /* EOF 也可能来自错误，先诊断，再输出状态 */
    if (ferror(stdin)) { perror("fgetc"); failed = 1; }
    if (printf("stop: EOF eof=%d error=%d\n",
               feof(stdin) != 0, ferror(stdin) != 0) < 0) failed = 1;
    if (fflush(stdout) == EOF) { perror("fflush"); failed = 1; }
    return failed;
}
