# Ace EL1 寄存器诊断模块

模块初始化只执行 `MIDR_EL1`、`ID_AA64MMFR0_EL1`、`CNTFRQ_EL0` 三次 MRS 并打印结果，退出函数为空。没有 MMIO、系统寄存器写入、SMC/HVC、存储写入或持久 hook。源码不负责固定 CPU；需要逐核测量时由调用进程的 CPU affinity 保证每次执行位置。

这不是 iOS 内核或启动镜像。

## 已验证结果

原候选保存在忽略目录 `research/ace-kbuild-path-20261019/module/ace_read_regs.ko`，131,864 字节，SHA256：

```
12655d3b3d8ecc3818d4541c800416975335cba37da2ef59f9cc228da3eac782
```

该候选由正常 Android external-module Kbuild、正常 modpost 和 LTO/CFI 最终链接生成。真实 OEM 模块提供所需 symbol CRC，精确 live kheaders 提供布局，不手造 struct module、不伪造 CRC、不 force-load、不移除 CFI。输出 `__this_module` 的 1024 字节大小、64 字节对齐及 init/exit 的 400/960 重定位偏移与 OEM 模块一致。完整证据在私有目录的 `report.md`、`candidate-verification.json` 和 `verification.json`。

- 同一原厂内核的 QEMU 测试 run3：普通 `finit_module(...,0)`、模块 printk、普通卸载全部通过，随后关机；11.697 秒退出 0，无超时。run2 的模块加载/卸载也成功，但 PID1 缺少关机调用导致 harness 超时，不能把 run2 整体算作通过。
- 真机普通加载/卸载成功；单次采样 MMFR0=`0x101122`、CNTFRQ=13 MHz。之后用单 CPU affinity 逐核验证 8 核：CPU0–3 MIDR=`0x412fd050`，CPU4–7=`0x411fd411`；所有核 MMFR0=`0x101122`、TGran16=1、CNTFRQ=13 MHz。每次模块均已卸载，暂存文件已清理。
- 这些结果证明这一个诊断模块的 ABI/CFI 路径以及手机 CPU 的 16 KiB 页能力，不能证明 XNU、iOS 启动、UFS、显示或触摸适配已完成。

运行证据：`research/ace-module-qemu-20261019/run3/result.json`、`research/ace-module-live-20261019/result.json`、`research/ace-module-live-20261019/per-cpu/result.json`。设备二进制、头文件、CRC 清单和运行日志不放入 git。

## 主机重建

```sh
python3 diagnostics/ace-read-regs/rebuild.py --check-only
python3 diagnostics/ace-read-regs/rebuild.py
```

脚本无网络、sudo、ADB、fastboot 或模块加载命令。它复用现有忽略目录中的准备树；缺少输入时明确失败，不自动替代为另一份内核。依赖现有 Clang/LLVM/LLD 18、AArch64 binutils、GCC、Make 和 Python 3。

脚本校验 kheaders 原始归档、OEM 模块、stock config、官方 scripts 归档和 Makefile 的固定 SHA256，再逐文件核对归档内全部普通 header/script 源文件。不会重新生成 live 头文件或运行 Kconfig。`Module.symvers` 是从真实 OEM `__versions` 解码生成的**部分重建数据**，仅含本模块需要的 printk/module_layout；导出 owner/class/namespace 最初依据同代官方源码 `EXPORT_SYMBOL` 推定，随后由同原厂内核和真机普通加载获得验证。它不是完整原版 symvers；新增导入必须重新获取真实版本信息，不能猜 CRC。

正常构建保留 full LTO、strict CFI、SCS/x18、PAC/BTI、UBSAN、stack protector 和 zero-init。兼容修改只有去除 Clang18 已移除的 zero-init acknowledgement 参数，实际 `-ftrivial-auto-var-init=zero` 保留。源码快照和补丁的哈希/来源记录在私有构建目录，不冒称精确 OEM 全源码或原 Clang12 输出。

重建写入 `research/ace-kbuild-path-20261019/module-rebuilt/`，保留已验证原候选。模块名仍为 `ace_read_regs`；源码路径、调试信息、编译器或源码 SCM 状态可能改变 SHA256/scmversion。**新重编产物必须重新校验、再在同一原厂内核 QEMU 验证；此前成功只绑定上面的原候选 SHA256。** 主机脚本不自动部署。

## 公开依据

[Android12-5.10 modpost](https://android.googlesource.com/kernel/common/+/refs/heads/android12-5.10/scripts/mod/modpost.c)、[模块最终链接](https://android.googlesource.com/kernel/common/+/refs/heads/android12-5.10/scripts/Makefile.modfinal)、[CFI linker script](https://android.googlesource.com/kernel/common/+/refs/heads/android12-5.10/scripts/module.lds.S)。纯 upstream 5.10 的构建脚本不能直接替代这些 Android LTO/CFI 环节。

本轮脚本实际独立重建候选 SHA256 `7e04f00c3dede4e00cd27aea1acf90e7c9edbbe225e564bbb265f33e58c05fc1`，131,896 字节，另经 QEMU run4-rebuilt 加载/卸载/关机通过（14.150 秒退出 0）。该重建候选未在手机加载；手机证据仍只绑定前述原候选。
