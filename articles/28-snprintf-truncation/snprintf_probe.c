#include <stdio.h>

int main(void)
{
    char buf[8];
    int small = snprintf(buf, sizeof buf, "value=%d", 12345);
    if (printf("small ret=%d text=%s truncated=%d\n",
               small, buf, small >= 0 && (size_t)small >= sizeof buf) < 0)
        return 1;

    int exact = snprintf(buf, sizeof buf, "1234567");
    if (printf("exact ret=%d text=%s truncated=%d\n",
               exact, buf, exact >= 0 && (size_t)exact >= sizeof buf) < 0)
        return 1;

    int needed = snprintf(NULL, 0, "value=%d", 12345);
    return printf("probe ret=%d\n", needed) < 0;
}
