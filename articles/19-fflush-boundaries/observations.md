| 模式 | 观察点前执行的操作 | 另一个进程读到的内容 |
| --- | --- | --- |
| `buffered` | 只调用 `fputs` | 空文件，0 字节 |
| `flush` | `fputs` → `fflush` | `record=42\n`，9 字节 |
| `sync-only` | `fputs` → `fsync` | 空文件，0 字节 |
| `flush-sync` | `fputs` → `fflush` → `fsync` | `record=42\n`，9 字节 |
