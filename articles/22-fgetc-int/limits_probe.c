#include <limits.h>
#include <stdio.h>

int main(void)
{
    if (printf("CHAR_BIT=%d UCHAR_MAX=%u INT_MAX=%d CHAR_MIN=%d EOF=%d\n",
               CHAR_BIT, (unsigned int)UCHAR_MAX, INT_MAX, CHAR_MIN, EOF) < 0)
        return 1;
    return fflush(stdout) == EOF ? 1 : 0;
}
