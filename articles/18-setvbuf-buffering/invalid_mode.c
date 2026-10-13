#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    const int invalid = -1;
    if (invalid == _IOFBF || invalid == _IOLBF || invalid == _IONBF)
        return EXIT_FAILURE;
    int result = setvbuf(stdout, NULL, invalid, 0);
    int status = result != 0 ? EXIT_SUCCESS : EXIT_FAILURE;
    if (fprintf(stderr, "invalid mode rejected: %s\n",
                result != 0 ? "yes" : "no") < 0)
        status = EXIT_FAILURE;
    if (fclose(stdout) == EOF) status = EXIT_FAILURE;
    return status;
}
