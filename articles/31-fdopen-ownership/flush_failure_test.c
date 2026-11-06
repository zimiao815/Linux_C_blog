#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>
int save_fd(int fd, const char *text);
int main(void)
{
    int ends[2];
    if (pipe(ends) == -1) return 1;
    if (signal(SIGPIPE, SIG_IGN) == SIG_ERR) return 1;
    if (close(ends[0]) == -1) return 1;
    int rc = save_fd(ends[1], "message");
    int broken_pipe = errno == EPIPE;
    errno = 0;
    int closed = fcntl(ends[1], F_GETFD) == -1 && errno == EBADF;
    printf("write_failure rc=%d epipe=%d closed_fd=%d\n",
           rc, broken_pipe, closed);
    return !(rc == -1 && broken_pipe && closed);
}
