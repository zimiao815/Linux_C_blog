#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

/* 只等待当前调用者负责回收的那个子进程。 */
static int wait_child(pid_t child, int *status)
{
    pid_t result;
    do {
        result = waitpid(child, status, 0);
    } while (result == -1 && errno == EINTR);
    return result == -1 ? -1 : 0;
}

int main(void)
{
    /* 在任何 stdout 操作之前设置，避免缓冲干扰观察。 */
    if (setvbuf(stdout, NULL, _IONBF, 0) != 0) {
        fputs("setvbuf failed\n", stderr);
        return EXIT_FAILURE;
    }
    if (printf("before: self=%ld\n", (long)getpid()) < 0) {
        perror("printf before");
        return EXIT_FAILURE;
    }

    pid_t pid = fork();
    if (pid == -1) {
        perror("fork");
        return EXIT_FAILURE;
    }

    int output_ok = printf("after: self=%ld fork_return=%ld\n",
                           (long)getpid(), (long)pid) >= 0;
    if (!output_ok)
        perror("printf after");

    if (pid == 0) {
        /* stdout 已无缓冲；子进程到此结束。 */
        _exit(output_ok ? EXIT_SUCCESS : EXIT_FAILURE);
    }

    int status;
    if (wait_child(pid, &status) == -1) {
        perror("waitpid");
        return EXIT_FAILURE;
    }
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0)
        return EXIT_FAILURE;
    return output_ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
