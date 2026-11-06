# fork

> Source: https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html

<<<
Previous
Home
Next
>>>

The Open Group Base Specifications Issue 8

IEEE Std 1003.1-2024

Copyright © 2001-2024 The IEEE and The Open Group

NAME

fork — create a new process

SYNOPSIS

#include <unistd.h>

pid_t fork(void);

pid_t _Fork(void);

DESCRIPTION

The fork() function shall create a new process. The new process (child process) shall be an exact copy of the calling
process (parent process) except as detailed below:

The child process shall have a unique process ID.

The child process ID also shall not match any active process group ID.

The child process shall have a different parent process ID, which shall be the process ID of the calling process.

The child process shall have its own copy of the parent's file descriptors, except for those whose FD_CLOFORK flag is set (see
fcntl()). Each of the child's file descriptors shall refer to the same open file
description with the corresponding file descriptor of the parent.

The child process shall have its own copy of the parent's open directory streams. Each open directory stream in the child
process may share directory stream positioning with the corresponding directory stream of the parent.

The child process shall have its own copy of the parent's message catalog descriptors.

The child process values of tms_utime, tms_stime, tms_cutime, and tms_cstime shall be set to 0.

The time left until an alarm clock signal shall be reset to zero, and the alarm, if any, shall be canceled; see alarm().

[XSI]
All semadj values shall be cleared.

Process-owned file locks set by the parent process shall not be inherited by the child process.

The set of signals pending for the child process shall be initialized to the empty set.

[XSI]
Interval timers shall be reset in the child process.

Any semaphores that are open in the parent process shall also be open in the child process.

[ML]  The
child process shall not inherit any address space memory locks established by the parent process via calls to mlockall() or mlock().

Memory mappings created in the parent shall be retained in the child process. MAP_PRIVATE mappings inherited from the parent
shall also be MAP_PRIVATE mappings in the child, and any modifications to the data in these mappings made by the parent prior to
calling fork() shall be visible to the child. Any modifications to the data in MAP_PRIVATE mappings made by the parent after
fork() returns shall be visible only to the parent. Modifications to the data in MAP_PRIVATE mappings made by the child
shall be visible only to the child.

[PS]  For
the SCHED_FIFO and SCHED_RR scheduling policies, the child process shall inherit the policy and priority settings of the parent
process during a fork() function. For other scheduling policies, the policy and priority settings on fork() are
implementation-defined.

Per-process timers created by the parent shall not be inherited by the child process.

[MSG]
The child process shall have its own copy of the message queue descriptors of the parent. Each of the message descriptors of the
child shall refer to the same open message queue description as the corresponding message descriptor of the parent.

No asynchronous input or asynchronous output operations shall be inherited by the child process. Any use of asynchronous control
blocks created by the parent produces undefined behavior.

A process shall be created with a single thread. If a multi-threaded process calls fork(), the new process shall contain
a replica of the calling thread and its entire address space, possibly including the states of mutexes and other resources.
Consequently, the application shall ensure that the child process only executes async-signal-safe operations until such time as one
of the exec functions is successful.

Any locks held by any thread in the calling process that have been set to be process-shared shall not be held by the child
process. For locks held by any thread in the calling process that have not been set to be process-shared, any attempt by the child
process to perform any operation on the lock results in undefined behavior (regardless of whether the calling process is
single-threaded or multi-threaded).

[CPT]
The initial value of the CPU-time clock of the child process shall be set to zero.

[TCT]
The initial value of the CPU-time clock of the single thread of the child process shall be set to zero.

All other process characteristics defined by POSIX.1-2024 shall be the same in the parent and child processes. The inheritance
of process characteristics not defined by POSIX.1-2024 is unspecified by POSIX.1-2024.

After fork(), both the parent and the child processes shall be capable of executing independently before either one
terminates.

The _Fork() function shall be equivalent to fork(), except that fork handlers established by means of the pthread_atfork() function shall not be called and _Fork() shall be
async-signal-safe.

RETURN VALUE

Upon successful completion, fork() shall return 0 to the child process and shall return the process ID of the child
process to the parent process. Both processes shall continue to execute from the fork() function. Otherwise, -1 shall be
returned to the parent process, no child process shall be created, and errno shall be set to indicate the error.

ERRORS

These functions shall fail if:

[EAGAIN]
The system lacked the necessary resources to create another process, or the system-imposed limit on the total number of
processes under execution system-wide or by a single user {CHILD_MAX} would be exceeded.

These functions may fail if:

[ENOMEM]
Insufficient storage space is available.

The following sections are informative.

EXAMPLES

None.

APPLICATION USAGE

When a multi-threaded process calls fork() or _Fork(), there is no guarantee that thread-specific memory, such as
stacks or thread-local storage, associated with threads in the parent other than the calling thread will still be available in the
child. This is because threads in the parent other than the calling thread do not exist in the child. Consequently, the
implementation of fork() or _Fork() could remove that memory from the address space in the child, or reuse it for
other purposes before returning or (in the case of fork()) calling any of the fork handlers registered by pthread_atfork(). Therefore, applications should avoid using any pointers to
thread-specific memory in the child that were passed to the calling thread from other threads in the parent.

RATIONALE

Many historical implementations have timing windows where a signal sent to a process group (for example, an interactive SIGINT)
just prior to or during execution of fork() is delivered to the parent following the fork() but not to the child
because the fork() code clears the child's set of pending signals. This volume of POSIX.1-2024 does not require, or even
permit, this behavior. However, it is pragmatic to expect that problems of this nature may continue to exist in implementations
that appear to conform to this volume of POSIX.1-2024 and pass available verification suites. This behavior is only a consequence
of the implementation failing to make the interval between signal generation and delivery totally invisible. From the application's
perspective, a fork() call should appear atomic. A signal that is generated prior to the fork() should be delivered
prior to the fork(). A signal sent to the process group after the fork() should be delivered to both parent and
child. The implementation may actually initialize internal data structures corresponding to the child's set of pending signals to
include signals sent to the process group during the fork(). Since the fork() call can be considered as atomic from
the application's perspective, the set would be initialized as empty and such signals would have arrived after the fork();
see also <signal.h>.

One approach that has been suggested to address the problem of signal inheritance across fork() is to add an [EINTR]
error, which would be returned when a signal is detected during the call. While this is preferable to losing signals, it was not
considered an optimal solution. Although it is not recommended for this purpose, such an error would be an allowable extension for
an implementation.

The [ENOMEM] error value is reserved for those implementations that detect and distinguish such a condition. This condition
occurs when an implementation detects that there is not enough memory to create the process. This is intended to be returned when
[EAGAIN] is inappropriate because there can never be enough memory (either primary or secondary storage) to perform the operation.
Since fork() duplicates an existing process, this must be a condition where there is sufficient memory for one such process,
but not for two. Many historical implementations actually return [ENOMEM] due to temporary lack of memory, a case that is not
generally distinct from [EAGAIN] from the perspective of a conforming application.

Part of the reason for including the optional error [ENOMEM] is because the SVID specifies it and it should be reserved for the
error condition specified there. The condition is not applicable on many implementations.

IEEE Std 1003.1-1988 neglected to require concurrent execution of the parent and child of fork(). A system that
single-threads processes was clearly not intended and is considered an unacceptable "toy implementation" of this volume of
POSIX.1-2024. The only objection anticipated to the phrase "executing independently" is testability, but this assertion should be
testable. Such tests require that both the parent and child can block on a detectable action of the other, such as a write to a
pipe or a signal. An interactive exchange of such actions should be possible for the system to conform to the intent of this volume
of POSIX.1-2024.

The [EAGAIN] error exists to warn applications that such a condition might occur. Whether it occurs or not is not in any
practical sense under the control of the application because the condition is usually a consequence of the user's use of the
system, not of the application's code. Thus, no application can or should rely upon its occurrence under any circumstances, nor
should the exact semantics of what concept of "user" is used be of concern to the application developer. Validation writers
should be cognizant of this limitation.

There are two reasons why POSIX programmers call fork(). One reason is to create a new thread of control within the same
program (which was originally only possible in POSIX by creating a new process); the other is to create a new process running a
different program. In the latter case, the call to fork() is soon followed by a call to one of the exec functions.

The general problem with making fork() work in a multi-threaded world is what to do with all of the threads. There are
two alternatives. One is to copy all of the threads into the new process. This causes the programmer or implementation to deal with
threads that are suspended on system calls or that might be about to execute system calls that should not be executed in the new
process. The other alternative is to copy only the thread that calls fork(). This creates the difficulty that the state of
process-local resources is usually held in process memory. If a thread that is not calling fork() holds a resource, that
resource is never released in the child process because the thread whose job it is to release the resource does not exist in the
child process.

When a programmer is writing a multi-threaded program, the first described use of fork(), creating new threads in the
same program, is provided by the pthread_create() function. The fork()
function is thus used only to run new programs, and the effects of calling functions that require certain resources between the
call to fork() and the call to an exec function are undefined.

The addition of the forkall() function to the standard was considered and rejected. The forkall() function lets
all the threads in the parent be duplicated in the child. This essentially duplicates the state of the parent in the child. This
allows threads in the child to continue processing and allows locks and the state to be preserved without explicit pthread_atfork() code. The calling process has to ensure that the threads processing
state that is shared between the parent and child (that is, file descriptors or MAP_SHARED memory) behaves properly after
forkall(). For example, if a thread is reading a file descriptor in the parent when forkall() is called, then two
threads (one in the parent and one in the child) are reading the file descriptor after the forkall(). If this is not desired
behavior, the parent process has to synchronize with such threads before calling forkall().

When forkall() is called, threads, other than the calling thread, that are in functions that can return with an [EINTR]
error may have those functions return [EINTR] if the implementation cannot ensure that the function behaves correctly in the parent
and child. In particular, pthread_cond_clockwait(), pthread_cond_timedwait(), and pthread_cond_wait() need to return in order to ensure that the condition has not
changed. These functions can be awakened by a spurious condition wakeup rather than returning [EINTR].

FUTURE DIRECTIONS

None.

SEE ALSO

alarm(), exec, fcntl(), pthread_atfork(), semop(), signal(), times()

XBD 4.15.2 Memory Synchronization, <sys/types.h>, <unistd.h>

CHANGE HISTORY

First released in Issue 1. Derived from Issue 1 of the SVID.

Issue 5

The DESCRIPTION is changed for alignment with the POSIX Realtime Extension and the POSIX Threads Extension.

Issue 6

The following new requirements on POSIX implementations derive from alignment with the Single UNIX Specification:

The requirement to include <sys/types.h> has been removed. Although
<sys/types.h> was required for conforming implementations of previous POSIX
specifications, it was not required for UNIX applications.

The following changes were made to align with the IEEE P1003.1a draft standard:

The effect of fork() on a pending alarm call in the child process is clarified.

The description of CPU-time clock semantics is added for alignment with IEEE Std 1003.1d-1999.

The description of tracing semantics is added for alignment with IEEE Std 1003.1q-2000.

IEEE Std 1003.1-2001/Cor 1-2002, item XSH/TC1/D6/17 is applied, adding text to the DESCRIPTION and RATIONALE
relating to fork handlers registered by the pthread_atfork() function and
async-signal safety.

Issue 7

Austin Group Interpretation 1003.1-2001 #080 is applied, clarifying the status of asynchronous input and asynchronous output
operations and asynchronous control lists in the DESCRIPTION.

Functionality relating to the Asynchronous Input and Output, Memory Mapped Files, Timers, and Threads options is moved to the
Base.

Functionality relating to message catalog descriptors is moved from the XSI option to the Base.

POSIX.1-2008, Technical Corrigendum 2, XSH/TC2-2008/0123 [858] is applied.

Issue 8

Austin Group Defects 62, 1361, and 1383 are applied, adding the _Fork() function and removing the requirement for
fork() to be async-signal-safe.

Austin Group Defect 768 is applied, adding OFD-owned file locks.

Austin Group Defect 1112 is applied, clarifying the requirements for a child of a multi-threaded process and for process-shared
and non-process-shared locks held by any thread in the calling process.

Austin Group Defect 1114 is applied, changing the APPLICATION USAGE section.

Austin Group Defect 1216 is applied, adding pthread_cond_clockwait().

Austin Group Defect 1318 is applied, adding FD_CLOFORK.

Austin Group Defect 1330 is applied, removing obsolescent interfaces.

End of informative text.

return to top of page

UNIX® is a registered Trademark of The Open Group.

POSIX™ is a Trademark of The IEEE.

Copyright © 2001-2024 The IEEE and The Open Group, All Rights Reserved

[ Main Index | XBD | XSH | XCU | XRAT
]

<<<
Previous
Home
Next
>>>
