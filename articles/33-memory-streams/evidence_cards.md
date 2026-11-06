# 证据卡

资料于本期研究时保存至 sources/。以下结论由 POSIX 规范与 Linux man-pages 交叉核对；运行验证另见 verification.json，仅代表记录中的 macOS 环境。

| 结论 | 原始出处与支持证据 | 条件与限制 | 可信程度及正文位置 |
| --- | --- | --- | --- |
| fmemopen 可把调用者数组关联到 FILE 流，容量固定，关闭不释放该数组 | [POSIX fmemopen](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fmemopen.html) DESCRIPTION；[Linux fmemopen](https://man7.org/linux/man-pages/man3/fmemopen.3.html) DESCRIPTION | 本文传非空 buf；buf=NULL 时由库分配并在关闭时释放，不能混用归属规则 | 高；接口表和工程示例 |
| open_memstream 分配并扩大缓冲区，成功关闭后调用者释放结果 | [POSIX open_memstream](https://pubs.opengroup.org/onlinepubs/9799919799/functions/open_memstream.html) DESCRIPTION；[Linux open_memstream](https://man7.org/linux/man-pages/man3/open_memstream.3.html) DESCRIPTION | 失败不承诺可使用最终结果；本文进程示例不作通用故障恢复 | 高；接口表和动态示例 |
| 成功 fflush/fclose 更新地址及长度，继续写入后需要重新获取 | 同上两份 open_memstream 文档关于 bufp、sizep 和有效期的规定 | 长度不计末尾 NUL；定位会影响 sizep，正文顺序写入，不推广到随机写入 | 高；刷新取结果章节 |
| fmemopen 的容量错误可能延迟至刷新或关闭 | POSIX fmemopen 关于缓冲与失败的说明；Linux fmemopen DESCRIPTION/NOTES | 工程函数还检查 n >= cap，ENOSPC 是适配器自己的约定；测试未模拟内存耗尽 | 高；固定容量章节 |
| 内存流没有底层文件描述符 | 两份 Linux man-pages 的 NOTES | 不涉及 fsync 或磁盘持久化；此处不是 Linux 内核缓存机制 | 高；动态示例后的说明 |

文章按已有报表函数的实际需求组织，不沿用参考手册的栏目顺序。例子、适配函数和容量测试为本期编写；标准条款用中文解释，未大段翻译原文。
