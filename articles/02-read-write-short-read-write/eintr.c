/*
 * eintr.c — 证明阻塞的 read 被信号打断时返回 -1、errno == EINTR，不自动重启。
 *
 * 关键：SIGUSR1 默认动作是「终止进程」，所以必须安装一个信号处理器
 * 让子进程收到信号后不退出，这样 read 才会返回 -1/EINTR 让子进程继续执行。
 */
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <string.h>
#include <errno.h>

static void say(const char *s) {
    write(1, s, strlen(s));
}

/* 空处理器：只为了让 SIGUSR1 不终止进程 */
static void handler(int sig) {
    (void)sig;
}

int main(void) {
    int fds[2];
    if (pipe(fds) < 0) { say("pipe failed\n"); return 1; }

    /* 安装信号处理器 */
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = handler;
    sigemptyset(&sa.sa_mask);
    /* 故意不设 SA_RESTART：这样阻塞中的 read 才会被打断返回 EINTR */
    sigaction(SIGUSR1, &sa, NULL);

    pid_t pid = fork();
    if (pid < 0) { say("fork failed\n"); return 1; }

    if (pid == 0) {
        close(fds[1]);
        char c;
        ssize_t r = read(fds[0], &c, 1);
        if (r < 0) {
            if (errno == EINTR)
                say("child: read interrupted, returned -1, errno == EINTR\n");
            else
                say("child: read failed with non-EINTR errno\n");
        } else {
            say("child: read returned normally (unexpected)\n");
        }
        close(fds[0]);
        return 0;
    }

    close(fds[0]);
    usleep(300000);
    kill(pid, SIGUSR1);

    waitpid(pid, NULL, 0);
    close(fds[1]);
    return 0;
}
