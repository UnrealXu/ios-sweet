# Ace FDT 用户态诊断

普通 Linux/AArch64 EL0 程序，在 Android shell UID2000、CPU0 上运行同一份
`ace/fdt.c`、`ace/xnu_fdt.c` 和 `ace/xnu_platform.c`。它读取传入的 DTB
与 ADT 副本，仅操作进程内存。
原始 syscall 仅为 openat/read/close/getcpu/getuid/write/exit；没有动态
加载器、libc、特权寄存器、MMIO、驱动调用、物理映射、重启或刷写。

```sh
bash diagnostics/ace-fdt-policy/build.sh NEW_OUTPUT_DIRECTORY
```

构建脚本只使用已有 GNU AArch64 工具链，拒绝已有输出目录。它不连接
手机。当前调用为 `taskset 1 PROGRAM CAPTURED_DTB ACE_ADT`，固定 CPU0；
程序要求 UID2000，不是 root 诊断模块。ELF 的 BSS LOAD 明确页对齐，
STT_FILE 元数据固定，同一源码两次构建字节相同。

程序先以实际 Android 阶段参数 0 调用策略函数，要求返回 -32 且输出
未改变，再以参数 1 **仅重放数值策略**。5–8GiB 等地址从不被映射或
解引用；第二次调用成功不证明手机处在原生启动阶段或拥有该内存。
该程序不执行 XNU materializer，也不复制或跳转内核。

## 平台比较版本真机结果（2026-10-20）

当前程序 23840 字节，SHA256
`c7f813f6511d69c2f970e2a2670202a473251a1e47e4264caf1164455fc8d830`。
真实 CPU0/UID2000 执行退出 0；除内存策略外，FDT/ADT 初始平台契约
比较返回 0，截断和损坏 ADT 均返回 -45。它不调用特权寄存器采样或
materializer，声明一致不能当作控制器或 XNU 已启动。

远端三个文件的哈希、临时目录清理、boot ID 不变及 Android/Enforcing
健康检查通过。证据在私有 `research/ace-platform-20261020/`；完整说明
见 [平台检查](../../docs/ACE-XNU-PLATFORM-CHECK.zh-CN.md)。

## 早期内存检查版本真机结果（2026-10-20）

该早期版本的静态程序 11,720 字节，SHA256：
`1c62ce61e8a97b9c627694bf34f00521e4cb47ca78d5c615743c2c95c19e92cb`。
实际执行 UID2000/CPU0，退出 0；解析 488,371 字节 DTB，1,830 个节点、
9,757 个属性，53 个排除区、两个精确匹配的 Linux CMA 延后声明。
Android 阶段拒绝 -32，进程内策略重放返回 0。远端程序和 DTB 哈希已
核对，暂存文件/目录均已删除，执行前后 boot ID 相同，Android 已启动，
SELinux 保持 Enforcing。最新 FDT 的读取使用既有 root 通道只读获取；
诊断程序本身以 shell 权限执行。

最初默认链接的程序退出 139，临时文件同样已清理。其零文件长度 BSS
段具有超出文件长度的非页对齐文件偏移；改用显式页对齐 ELF 布局后
执行成功。未取得首次故障 PC，因此将 ELF 装载问题保留为诊断推断，
不宣称已定位到某条解析器指令。失败产物和记录均保留，不能用于部署。

证据：私有 `research/ace-native-fdt-20261020/phone-result.json`、原始
stdout、远端哈希、源码哈希、失败记录和重复构建产物。完整边界见
[原生 FDT 检查说明](../../docs/ACE-XNU-FDT.zh-CN.md)。
