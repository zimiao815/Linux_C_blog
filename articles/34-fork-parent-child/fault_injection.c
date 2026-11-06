/* 测试专用：替换 API 入口；不声称触发了真实系统资源耗尽。 */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static int wait_calls;

static pid_t test_fork(void)
{
    const char *fault = getenv("FORK_DEMO_FAULT");
    if (fault != NULL && strcmp(fault, "fork_eagain") == 0) {
        errno = EAGAIN;
        return -1;
    }
    return fork();
}

static pid_t test_waitpid(pid_t pid, int *status, int options)
{
    const char *fault = getenv("FORK_DEMO_FAULT");
    ++wait_calls;
    if (fault != NULL && strcmp(fault, "wait_eintr") == 0 && wait_calls == 1) {
        errno = EINTR;
        return -1;
    }
    if (fault != NULL && strcmp(fault, "wait_echild") == 0) {
        errno = ECHILD;
        return -1;
    }
    return waitpid(pid, status, options);
}

#define fork test_fork
#define waitpid test_waitpid
#define main article_main
#include "fork_demo.c"
#undef fork
#undef waitpid
#undef main

int main(void)
{
    const char *fault = getenv("FORK_DEMO_FAULT");
    if (fault != NULL && strcmp(fault, "wait_echild") == 0) {
        /* 直接测试帮助函数，不创建会无人回收的子进程。 */
        int status = 0;
        int result = wait_child((pid_t)123, &status);
        if (result != -1 || errno != ECHILD || wait_calls != 1)
            return EXIT_FAILURE;
        return puts("injected ECHILD: propagated, no retry") < 0
                   ? EXIT_FAILURE : EXIT_SUCCESS;
    }
    int result = article_main();
    if (fault != NULL && strcmp(fault, "wait_eintr") == 0) {
        if (result != 0 || wait_calls != 2)
            return EXIT_FAILURE;
        if (puts("injected EINTR: retried and reaped") < 0)
            return EXIT_FAILURE;
    }
    return result;
}
