# Ace 原生加载前的 CPU 检查

`ace/xnu_cpu.c/.h` 为有界 XNU 加载器增加 CPU 检查入口，
`ace/xnu_cpu_capture.S` 提供实际特权寄存器采样。它们已由
[原生 EL1 Image](ACE-XNU-NATIVE-ENTRY.zh-CN.md) 调用，尚未在手机执行，
不能据此宣称 XNU 或 iOS 真机启动。

## 调用约定

采样函数接受调用者拥有的、8 字节对齐的 56 字节正常 RAM。它读取
CurrentEL、活动异常级的 SCTLR、MIDR、MPIDR、MMFR0、CNTFRQ 和 DAIF。
它不使用栈，不执行 MSR、SMC/HVC、MMIO，也不改变 CPU 状态；正常输出
写入仅限该记录。只有返回 0 后记录才有效；寄存器陷阱可能留下部分记录。
EL0 无权读取 CurrentEL，不能从 Android 用户态直接调用此函数。

调用者须先完成独立的 EL1 入口和 DAIF 屏蔽，再取得新记录。初始检查
要求 EL1、Cortex-A55、完整 affinity 为 0、已知 16K 页能力、至少
40 位 PA、13MHz 时基、所有 DAIF 屏蔽，以及 MMU、D-cache、I-cache 和
大端关闭。尚未支持的新页格式会拒绝。EL2 状态会被拒绝，不暗中切换
异常级或关闭正在工作的映射/缓存。

检查使用完整 affinity 掩码，而不是把 Aff0 当作 CPU 编号；定义与
固定 OEM 头文件及 [Linux cputype.h](https://github.com/torvalds/linux/blob/v5.10/arch/arm64/include/asm/cputype.h)
交叉核对。手机此前逐核记录的 Aff1 为 0–7、Aff0 均为 0。

`ace_xnu_prepare_cpu` 和 `ace_xnu_materialize_cpu` 在规划/目标写入之前
执行检查，并将 RAM 限制在初始 40 位 PA 契约内，然后调用既有加载器。
它们仍要求完整的加载器源/目标/保留区契约。CPU 状态通过不表示 FDT
正确、固件/DMA 已释放 RAM、其他核心静止或内存一致性成立。旧 Android
记录和主机构造的状态都不能替代加载前的即时采样。

## 验证结果（2026-10-20）

- 5 项新回归覆盖 CPU 拒绝发生在目标写入之前、完整 affinity、错误
  异常级/型号/缓存/页能力/时基/DAIF，以及既有加载器范围拒绝的保留。
  全部 176 项主机回归通过，33.155 秒。
- C、采样汇编和加载器以 Cortex-A55 freestanding 参数编译并部分链接，
  无未定义运行库符号。采样汇编的反汇编未发现 MSR、SMC/HVC 或调用指令。
- 读取已有真机原生前缀记录核对 SCTLR/MIDR/MMFR0，以及已有 Android
  逐核 MPIDR/时基/DAIF。它们来自不同阶段，不能拼成一次完整启动采样。
  Android DAIF 未屏蔽，因此不会被误当作原生加载就绪状态。
- 实际 Ace 内核载荷经新增接口进入同一个 C materializer，主机校验
  10 段、966,656 字节 BSS、ADT、BootArgs、52 个排除区成功。CPU 状态
  明确为主机夹具，没有把内核复制到手机。
- 采样函数和 C 检查在 QEMU Cortex-A55 的 EL1、EL2，以及 Cortex-A76
  的 EL1 执行。分别因模拟时基 62.5MHz、EL2、错误 CPU 型号拒绝；采样
  记录与预期异常级一致。这只验证采样代码和拒绝路径，不是 XNU 执行。
- 本轮手机只读 USB 检查为在线、Android 启动完成、SELinux Enforcing；
  没有模块加载、重启、分区写入或新增原生代码执行。

私有证据在 `research/ace-cpu-gate-20261020/`。首次回归发现高位 MPIDR
保留位未被拒绝，随后补齐保留位检查并通过全部测试。下一步仍为原生
实时 FDT/内存归属检查和最早 XNU 日志，而后才能提出具体真机启动镜像。
