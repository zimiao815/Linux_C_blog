---
title: "while (!feof(fp)) 错在哪里？"
series: "标准 I/O 库 · 第 7 篇"
core_question: "为什么不能只靠 while (!feof(fp)) 控制读取？"
scope: "新打开的字节输入流；读取结果、EOF 标志与错误标志"
standards: "ISO C 流状态语义；POSIX.1-2024；glibc 2.40；Linux v6.6"
experiment_env: "macOS 14.8.8 x86_64，Apple clang 16.0.0；未在 Linux 主机实测"
status: draft
---

# while (!feof(fp)) 错在哪里？

`while (!feof(fp))` 很像“文件没结束就继续读”。但文件中最后一个字节已经读出来了，条件却仍然可能成立；遇到读取错误时，它还可能一直成立。

> **结论：`feof` 查询流中已经记录的文件结束标志，不预测下一次读取。应先调用读取函数，只有成功取得数据才进入处理分支；读取停止后，检查 `ferror`，再确认是否正常遇到文件结束。**

![标准 I/O 库第 7 期封面](cover-21-feof-read-loop-900.png)

**这篇文章怎么读？**

先用第一章的短程序观察循环何时停止；第三章的复制函数可以直接参考使用，第二章解释它背后的流状态与内核读取。

| 你是谁 | 看哪一章 | 会得到什么 |
| --- | --- | --- |
| 搜索者 / 被推荐者 | 第一章 · 先解决问题 | 按读取结果处理数据的循环 |
| 学习者 | 第二章 · 机制解释 | 看清 EOF、流标志与底层读取的区别 |
| 编程者 | 第三章 · 工程使用 | 区分错误、处理状态与资源 |
| 求职者 | 第四章 · 面试提炼 | 解释空文件和最后一个字节的行为 |

## 第一章 · 先解决问题：先读，再决定有没有数据可处理

实测环境是 **macOS 14.8.8 x86_64、Apple clang 16.0.0，未在 Linux 主机实测**。规范与 Linux/glibc 实现会在第二章分开说明。

下面直接从标准输入一次取一个字节，省去参数和文件打开代码，只观察读取前、取字节后和停止时的标志。`ch` 使用 `int`，保留完整返回值；循环体只处理读成功的数据。

保存为 `feof_short.c`：

```c
@@PROBE@@
```

编译后创建一个只有 `A`、没有换行的文件。以下命令请在实验目录中运行：

```sh
cc -std=c17 -Wall -Wextra -Wpedantic \
  -Wconversion -Wshadow -O0 -g feof_short.c -o feof_short
printf A > one.txt
./feof_short < one.txt
```

实际输出如下，退出状态为 0。这里把标志统一转成了 0 或 1，标准接口只保证“零或非零”。

```text
start: eof=0 error=0
byte=65 eof=0 error=0
stop: EOF eof=1 error=0
```

`65` 是本机读到的 `A`。第二行已经取出了文件唯一的字节，但 `feof` 仍是 0。**下一次 `fgetc` 尝试取字节，发现没有数据，返回 `EOF`，这时结束标志才置位。**

如果循环只用 `!feof(fp)` 决定能否进入，那么它会再进一轮。危险在于进入后忽略读取返回值，照常处理 `ch`，把 `EOF` 当成了一份有效输入。

正确循环也需要那次“读不到字节”的尝试。区别是它把检查放在进入循环体之前，让失败结果停在处理分支之外。

### 空文件与读取错误，走的是两种分支

空文件甚至在第一次读取之前就已没有数据，但刚打开时仍然 `feof=0`：

```sh
: > empty.txt
./feof_short < empty.txt
```

```text
start: eof=0 error=0
stop: EOF eof=1 error=0
```

再运行 `./feof_short < .`。本机允许把目录接到标准输入，随后字节读取失败，标准输出与标准错误分别为：

```text
start: eof=0 error=0
stop: EOF eof=0 error=1
```

```text
fgetc: Is a directory
```

退出状态为 1。这里 `fgetc` 同样返回 `EOF`，但 `feof=0、ferror=1`。目录的打开和读取行为依平台而异，这是本机实际走通的错误路径，不能把它当作跨平台的造错接口。

另一个带三次尝试上限的探针也证实：目录读错后三次都是 `feof=0、ferror=1`，`!feof` 一直成立。探针主动停止，没有运行一个真正无界的循环。

几种输入的结果如下。普通文件四组都退出为 0，错误组退出为 1：

| 输入 | 成功交给循环体的字节 | 停止时的状态 |
| --- | --- | --- |
| 空文件 | 无 | `feof=1，ferror=0` |
| 只有 `A` | 65 | `feof=1，ferror=0` |
| `A` 后跟换行 | 65、10 | `feof=1，ferror=0` |
| 二进制 `00 FF` | 0、255 | `feof=1，ferror=0` |
| 目录（本机错误路径） | 无 | `feof=0，ferror=1` |

## 第二章 · 机制解释：EOF 是返回值，feof 查询的是流状态

先区分三个名字：`EOF` 是某些读取函数用来表示“这次没有取得数据”的返回值；`feof` 查询文件结束标志；`ferror` 查询错误标志。两种标志属于 `FILE`，不是磁盘文件末尾藏着的特殊字节。

ISO C 规定这些接口及其流状态语义。POSIX 进一步规定，`fgetc` 遇到读取错误时设置 `errno`；对有效流调用 `feof`、`ferror` 不改变 `errno`。因此示例先查错误标志，确认错误后立即用 `perror` 诊断，再输出状态，避免中间操作干扰错误码。

![FILE 中的状态标志、输入缓冲与底层读取结果](img-feof-objects.png)

glibc 2.40 的 `FILE` 内部用 `_IO_EOF_SEEN` 和 `_IO_ERR_SEEN` 表示这两个状态。`feof`、`ferror` 检查对应标志位，不会为了回答你而先读一个字节，也不会拿文件大小预测下一次读取。

已有数据可能还在用户态输入缓冲里。`fgetc` 可以从缓冲中取走一个字节，不必每次都进入内核。普通文件路径需要补充缓冲时，经 `_IO_new_file_underflow` 等内部函数调用底层读取。

Linux 通过 fd 找到 `files_struct.fdt` 下的描述符表，再从 `fdtable.fd[fd]` 找到 `struct file`；其中有文件偏移 `f_pos`、关联 inode 的 `f_inode` 等字段。glibc 根据底层读取结果更新用户态流：返回正数就补充字节，返回 0 就设置结束标志，返回负值就设置错误标志。

所以，内核 `read` 返回 0 与库函数 `fgetc` 返回 `EOF` 是不同层的结果。后者还可能来自读错误，或者来自流里早已置位的结束标志，不能只看到 `EOF` 就宣布读完成功。

这些字段和调用路径是 glibc/Linux 的实现说明。macOS 的运行结果只用来验证本机行为，没有拿它当成 glibc 的执行轨迹。

## 第三章 · 工程使用：处理返回值，保留停止原因

### 可直接复用：按读取结果复制字节

把实验中的“打印字节值”换成“写入目标流”，就得到下面的复制函数。它借用两个独立的流：`src` 是没有遗留错误、由当前读取流程管理的输入流，`dst` 是可写输出流。

```c
@@ENGINEERING@@
```

例如，`copy_stream(stdin, stdout)` 可以从标准输入复制到标准输出。成功返回 0，失败返回 -1；在 POSIX 环境中，调用方应及时保存或报告 `errno`。测试覆盖了空输入、全部 256 种字节，以及读取和输出失败。

![读取返回值决定数据处理，状态标志解释停止原因](img-read-result-loop.png)

循环退出意味着 `fgetc` 没有取得字节。对于这里没有历史错误的输入流，若 `ferror(src)` 为假，就可以按正常结束处理；不需要在每次读取前查 `feof`。如果有读取错误，就返回失败，不能因为同样得到了 `EOF` 而报告成功。

`fputc` 和最后的 `fflush` 也要检查，否则输入读完了，输出却可能不完整。失败时可能已复制一部分内容，本函数不回滚、不自动重试，刷新成功也不等于磁盘持久化。

函数只借用流，不负责关闭。若调用方通过 `fopen` 创建了它们，应在函数返回后按自己的资源归属分别关闭并检查结果；关闭成功不能覆盖复制失败。`feof`、`ferror` 等状态查询都必须在关闭之前完成。

### clearerr 清的是标志，不是故障原因

结束和错误标志会保留，不是每次查询后自动归零，也不只是“上一次读取的结果”。`clearerr(fp)` 清除这两个标志，但不移动文件位置、不重新打开文件，更不会修好底层 I/O 故障。

对位置仍在末尾、内容没有变化的普通文件，清除结束标志后再读，仍会重新遇到结束。若想从头重读，可以对可定位流检查 `fseek(fp, 0, SEEK_SET)` 的结果；成功定位会清除 EOF 标志，但不要把它说成清除所有错误标志。

同样，不能遇到错误就无限循环 `clearerr` 再读。POSIX 输入可能因 `EINTR` 或非阻塞条件 `EAGAIN` 失败，是否等待、恢复或放弃，需要先判断原因。本例选择把错误向上传递，没有自动重试策略。

如果流曾经经历过错误而代码又继续读取，标志可能带着历史状态。不要把 `feof` 和 `ferror` 当成永远互斥的“二选一”，更不要在未处理错误前清掉线索。由一个读取流程管理流的状态；多个线程之间各自“查一次、再读一次”，不能靠单个库函数的锁保证这两步连在一起。

### 换成其他读取函数，也由结果决定如何处理

`fgets` 应检查是否返回了非空指针，`fread` 应按实际返回的元素数量处理，不能只把 `fgetc` 换掉、继续保留 `!feof` 这个唯一条件。

但不要再概括成“最后一份有效数据返回时，`feof` 一定是 0”。本篇的一字节实验用的是 `fgetc`；`fgets` 可能在取得末尾不足一行的内容后，又在同一次调用中遇到结束，从而返回有效字符串并设置 EOF 标志。先尊重各函数的返回契约，再解释状态标志。

## 第四章 · 面试提炼：feof 不回答“下次能否读到”

解释这个循环的问题，可以直接用单字节文件：读出唯一字节后，结束标志仍为 0，下一轮读取才发现结束。如果不检查本次返回值，就可能处理无效数据；若发生读错误，结束标志还可能一直为 0。

正确写法让读取结果控制循环，退出后用 `ferror` 和 `feof` 区分原因。空文件也遵守同一规则：刚打开时没有记录过结束，第一次读取才会设置标志。

## 第五章 · 参考资料：状态语义与实现分别核对

- POSIX.1-2024：[fgetc](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fgetc.html)、[feof](https://pubs.opengroup.org/onlinepubs/9799919799/functions/feof.html)、[ferror](https://pubs.opengroup.org/onlinepubs/9799919799/functions/ferror.html)、[fputc](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fputc.html)、[fflush](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fflush.html)：读取返回值、流标志、输出及错误码。
- POSIX.1-2024：[clearerr](https://pubs.opengroup.org/onlinepubs/9799919799/functions/clearerr.html)、[fseek](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fseek.html)、[fgets](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fgets.html)、[fread](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fread.html)：清除状态、重新定位与读取结果契约。
- [glibc 2.40：EOF and Errors](https://sourceware.org/glibc/manual/2.40/html_node/EOF-and-Errors.html)：结束和错误状态的含义。
- glibc 2.40 源码：[feof.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/feof.c)、[ferror.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/ferror.c)、[struct_FILE.h](https://github.com/bminor/glibc/blob/glibc-2.40/libio/bits/types/struct_FILE.h)、[fileops.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/fileops.c)：状态位和普通文件缓冲读取路径。
- Linux v6.6 源码：[fdtable.h](https://github.com/torvalds/linux/blob/v6.6/include/linux/fdtable.h)、[fs.h](https://github.com/torvalds/linux/blob/v6.6/include/linux/fs.h)：描述符表与文件对象关系。

本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。
