---
title: "写入成功了，为什么 fclose 还会失败？"
series: "标准 I/O 库 · 第 6 篇"
core_question: "为什么前面的写入成功了，fclose 仍可能失败？"
scope: "普通文件输出流；关闭时刷新、错误处理与资源生命周期"
standards: "ISO C 关闭语义；POSIX.1-2024；glibc 2.40；Linux v6.6"
experiment_env: "macOS 14.8.8 x86_64，Apple clang 16.0.0；未在 Linux 主机实测"
status: draft
---

# 写入成功了，为什么 fclose 还会失败？

`fputs` 返回成功，程序接着关闭文件，却收到 `fclose: File too large`。错误为什么到最后一步才出现？

> **结论：写入成功可能只表示标准 I/O 库接受了数据；`fclose` 会尝试刷新尚未写出的内容，底层错误可能到这时才暴露。必须检查关闭结果，而且无论返回 0 还是 `EOF`，都不能再次使用原来的流。**

![标准 I/O 库第 6 期封面](cover-20-fclose-errors-900.png)

**这篇文章怎么读？**

先用实验观察报错发生在哪一步，再看关闭过程中发生了什么，以及失败后怎样结束资源使用。

| 你是谁 | 看哪一章 | 会得到什么 |
| --- | --- | --- |
| 搜索者 / 被推荐者 | 第一章 · 先解决问题 | 复现写入成功、关闭失败 |
| 学习者 | 第二章 · 机制解释 | 区分刷新、底层关闭和流资源清理 |
| 编程者 | 第三章 · 工程使用 | 一次关闭、保留错误、不再访问旧流 |
| 求职者 | 第四章 · 面试提炼 | 解释为何关闭报错也不能重试原流 |

## 第一章 · 先解决问题：关闭时才提交的数据，也会在关闭时报错

本次实测环境是 **macOS 14.8.8 x86_64、Apple clang 16.0.0，未在 Linux 主机实测**。Linux/glibc 的机制另外依据规范与源码核对。

实验只做两件事：把 9 字节的 `record=42\n` 写入缓冲，再关闭输出流。用终端重定向把 `stdout` 接到文件，就能省去参数解析和文件打开代码，直接观察报错发生在哪一步。

保存为 `fclose_short.c`。中文注释标出了缓冲的使用期和流的失效位置：

```c
@@PROBE@@
```

正常对照，在实验目录执行：

```sh
cc -std=c17 -Wall -Wextra -Wpedantic \
  -Wconversion -Wshadow -O0 -g fclose_short.c -o fclose_short
(set -C; ./fclose_short > normal.txt)
```

`set -C` 防止重定向覆盖已有文件；重复运行请换新文件名。记录写进文件，以下诊断写到终端的标准错误，退出状态为 0：

```text
@@NORMAL@@
```

### 不填满磁盘，也能复现写出失败

下面的启动器只把测试子进程的文件大小上限设为 0。忽略 `SIGXFSZ`，是为了让写出失败返回错误，而不是直接被信号终止。保存为 `run_short_limited.py`，运行 `python3 run_short_limited.py`：

```python
@@LAUNCHER@@
```

实际结果：

```text
@@LIMITED@@
```

`fputs` 先成功，`fclose` 才报告 `File too large`。此时文件已经创建，大小却是 0；错误来自文件大小限制，不是磁盘写满。这个单线程启动器不改变终端或父进程的资源限制。

把限制改成 `(4, 4)`，并换一个新文件名，还能看到部分写入：

@@OBSERVATIONS@@

正常组退出为 0，两个限额组退出为 1。**关闭失败不意味着一个字节也没写，文件可能已经留下不完整的前缀。**

补充实验还比较了无缓冲和提前 `fflush` 两种用法：无缓冲时，写出错误提早出现在 `fputs`，后面的 `fclose` 可以成功；显式刷新则可能在 `fflush` 处先报错。因此，既要检查写入，也要检查关闭，不能用最后一次成功覆盖先前的失败。

## 第二章 · 机制解释：一个 fclose，包含刷新和关闭两类工作

`FILE` 保存用户态的流状态，缓冲中的字节可能尚未交给内核。只要写入当时被缓冲接收，`fputs` 就可能先返回成功；它不承诺后续刷新一定能完成。

ISO C 规定关闭时处理未写出的缓冲数据，并解除流与文件、缓冲区的关联。POSIX 进一步要求对关联 fd 执行相当于 `close` 的操作，失败时设置 `errno`。**无论关闭调用是否成功，原流都不能继续使用。**

![关闭前的对象关系与刷新、关闭、清理步骤](img-fclose-objects.png)

在 glibc 2.40 的普通文件路径中，`_IO_new_fclose` 调用 `_IO_new_file_close_it`。后者先保存刷新结果，再调用底层关闭，然后解除缓冲关联、清理流状态。外层继续完成流对象清理，最后返回状态。

这段实现没有在“刷新失败”处直接返回、把流留给调用者重试。自动分配的缓冲会释放；调用方通过 `setvbuf` 提供的数组只解除关联，库不会替调用方释放它。示例的局部数组一直活到 `fclose` 返回，满足这个使用期要求。

内核侧，`files_struct.fdt` 指向描述符表，`fdtable.fd[fd]` 指向 `struct file`。这个对象保存偏移 `f_pos`，并通过 `f_inode` 关联 inode。Linux 的 `close` 释放 fd 表项，编号随后可能被复用；文件对象是否能释放，还取决于其他引用。关闭一个流也不等于删除文件。

错误来源也有区别：本次实验在刷新写出时触发 `EFBIG`；底层关闭本身同样可能报告错误，例如某些网络文件系统的延迟 I/O 错误。glibc 文档专门提醒，即使输出缓冲已空，也不能省略关闭检查。本文没有实测网络文件系统故障。

因此，提前 `fflush` 能把一部分错误提早暴露，却不能保证后面的 `fclose` 一定成功。关闭成功也不提供额外的持久化承诺；需要文件同步时，应在流仍有效时完成刷新、`fsync` 和对应检查。

## 第三章 · 工程使用：保留失败结果，只关闭一次

### 可直接复用：保存一段文本，并检查最终关闭

下面的 POSIX 环境用法把文件生命周期收在一个函数里：新建文件、写入、关闭；成功返回 0，失败返回 -1 并保留第一个失败操作的 `errno`。调用方看到 -1 后应及时诊断或保存 `errno`。

```c
@@ENGINEERING@@
```

例如调用 `save_record("new.txt", "record=42\n")`，即可保存一条记录。`"wx"` 要求目标原先不存在，避免覆盖旧文件；参数应是有效路径和以空字符结束的文本。二进制数据应另选能指定长度的接口。

这里把 `fclose(fp)` 放在 `&&` 左侧，因此即使前面的写入已经失败，关闭仍然执行一次。只有尚未记录错误时才采用关闭的错误码；若写入和关闭都失败，这个简化接口返回第一个原因，需要双重诊断的项目可扩展错误结构。

函数已经负责关闭，调用方不用补关。验证覆盖了完整写入、0 和 4 字节限额、目标已存在、父目录不存在；错误均向上传递，旧文件内容保持不变。

![fclose 返回值与流生命周期的处理分支](img-fclose-lifetime.png)

### EOF 是错误通知，不是“流还留着”的凭证

`fclose` 返回 `EOF` 后，再调用 `ferror(fp)`、`fflush(fp)`、`fileno(fp)` 或第二次 `fclose(fp)`，都属于继续使用已关闭的流。不能为了查询错误，反而引入未定义行为。

保存函数中的 `fp` 是局部变量，关闭后直接返回，不再访问它。如果项目把流保存在较长寿命的对象中，应同时清理持有关系；仅给一个指针赋空不能修复其他别名。关闭前必须保证所有使用者都停止访问，库函数内部的流锁不能代替应用管理生命周期。

即使错误码是 `EINTR`，也不要套用 `read` 的重试循环，再次对同一个 `FILE *` 调用 `fclose`。流的寿命已经结束；底层裸 fd 在中断后的具体状态要另查平台规则，不能据此恢复这个流。

也不要提前 `close(fileno(fp))`，再把 `fclose` 当作纯内存清理。在 Linux 上，fd 编号可能被其他打开操作复用，后续刷新或关闭就可能碰到别的文件。关联描述符应由流的关闭流程处理。

### 失败后的文件，交给保存流程处理

4 字节限额的结果只有 `reco`，不是一条完整记录。程序应把这次保存判为失败，保留诊断；是否删除部分文件、写到另一个临时文件或重新生成内容，需要由业务的恢复规则决定。

关闭动作不会回滚已经写出的前缀，也不会替你恢复旧文件。若采用重试，应重新建立一个有效流，并先处理已存在的部分结果，不能直接对旧指针重发。

正常退出时，库会处理尚未关闭的流。但把输出文件留给进程退出清理，就失去了在主流程中检查关闭结果、据此设置退出状态或向调用方报告失败的机会。关键输出应在还能处理错误的位置显式关闭。

## 第四章 · 面试提炼：关闭报错与资源寿命是两个问题

“写入成功为什么关闭还会失败？”可以从缓冲回答：写入可能只进入用户态，关闭时刷新才触发底层错误；即便之前已经刷新成功，底层关闭也仍可能失败。

“报错后再关一次行不行？”需要补上资源规则：`fclose` 返回后，原流无论成败都不可再用。应保存错误并向上传递，而不是根据 `EOF` 推断资源还在。

若追问“只检查关闭够不够”，补充的无缓冲实验给出了反例：写入失败、关闭成功，整体仍然失败。

## 第五章 · 参考资料：关闭语义与实现路径

- [POSIX.1-2024：fclose](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fclose.html)、[fputs](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fputs.html)、[fopen](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fopen.html)：关闭、返回值、流失效与新建文件语义。
- [POSIX.1-2024：getrlimit / setrlimit](https://pubs.opengroup.org/onlinepubs/9799919799/functions/getrlimit.html)：文件大小限制、`SIGXFSZ` 与 `EFBIG`。
- [glibc 2.40：Closing Streams](https://sourceware.org/glibc/manual/2.40/html_node/Closing-Streams.html)：延迟错误与退出时关闭。
- glibc 2.40 源码：[iofclose.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/iofclose.c)、[fileops.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/fileops.c)、[genops.c](https://github.com/bminor/glibc/blob/glibc-2.40/libio/genops.c)：刷新、底层关闭和缓冲清理。
- Linux 手册：[fclose(3)](https://man7.org/linux/man-pages/man3/fclose.3.html)、[close(2)](https://man7.org/linux/man-pages/man2/close.2.html)：错误、关闭后的使用限制及 fd 复用。
- Linux v6.6 源码：[fdtable.h](https://github.com/torvalds/linux/blob/v6.6/include/linux/fdtable.h)、[fs.h](https://github.com/torvalds/linux/blob/v6.6/include/linux/fs.h)：描述符表与文件对象字段。

本文为公众号「理解力笔记」原创。转载请联系作者，并保留出处。
