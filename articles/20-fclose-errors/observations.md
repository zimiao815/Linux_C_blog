| 运行条件 | 实际报告顺序 | 文件内容 |
| --- | --- | --- |
| 不额外限额 | `fputs` 成功 → `fclose` 成功 | `record=42\n` |
| 上限 0 字节 | `fputs` 成功 → `fclose` 失败 | 空文件 |
| 上限 4 字节 | `fputs` 成功 → `fclose` 失败 | `reco` |
