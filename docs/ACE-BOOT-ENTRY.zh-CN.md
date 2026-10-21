# Ace：LK 到内核的交接证据（2026-10-19）

目标是当前 PGKM10 / MT6895 的启动路径。本文是已取得固件的静态分析及受控仿真实验记录；真机 iOS 尚未启动。

## 固件身份

通过现有无线 ADB 的 su 只读取得当前 B 槽 lk_b、tee_b，各 5,242,880 字节。读取前后设备 SHA-256、主机重新读取 SHA-256 与长度均一致。

| 内容 | SHA-256 |
| --- | --- |
| live lk_b 分区 | `6c87c7158605359cc89404d9630632ca9455f31cc7b4b367ff9a6271c6b05ba8` |
| live tee_b 分区 | `11d84b56101eb117410d710bc533272b795c39edc1ff6b706994910c11c96d13` |
| LK 第一 ARM64 段 | `9e3f9fd53316fe7d64a5ed70eea5374489f9aed3e33b20511437f21e269e8511` |
| ATF ARM64 段 | `082d229cc11e996b9b77dde9a88b52065ff9599be39626ae1d22b5badba71724` |

live LK 的前 4,153,344 字节与已保存的原厂 lk.img 完全相同，剩余分区尾部为零。ATF 是 tee_b 内第一 MTK 段：512 字节头后 289,656 字节；与同版本 OTA 的 ATF 内容一致。原始分区、提取段及 REA 快照保存在 Git 忽略的私有 research 目录。

REA 使用 Ghidra 12.1.4、ARM64 raw、分析基址 0。下列地址均为文件偏移/合成分析地址，不能直接当作真机物理地址。独立 GNU objdump 核对关键指令。

## LK 解压与交接

`boot_linux_fdt` 位于 `0xcf74..0xde77`，其调用方 `boot_linux_from_storage` 位于 `0xde78`。已观察到：

1. v3/v4 头路径从 vendor_boot 取得 DTB，进行 DTBO 合并及最终 DT 更新。
2. 内核窗口分配请求为 `0x7c80000` 字节；DTB 请求为 4 MiB。原厂 vendor_boot v4 的内核地址 `0x40000000`、DTB 地址 `0x47c80000`、ramdisk 地址 `0x66f00000` 是输入配置，不能据此认定任意替换镜像安全。
3. `0xbcfc` 通过 gzip/deflate 解压内核；这条路径不是直接跳到未经封装的 Mach-O XNU。
4. 尾部经 `0x26ff0` 清理缓存、转换回调/跳板地址；`0x26da8` 跳板关闭 EL1 MMU，然后跳转到回调 `0xde6c` 的物理副本。
5. 回调执行 `SMC #0`。最终调用参数为 `x0=0xc2000115`、`x1=kernel`、`x2=DTB`、`x3=0`、`x4=1`。这些是 SMC 的参数，不等于最终内核入口的 x0..x4。

REA 证据：`ev_495f802fa41870a2842d758c0ab458eca229e7344ac0dd591cf9a4a889a57019`（主函数）、`ev_51b8efa9ed774e7a200d8dc3de6c3e91e3a780004fe5b98e54e80caa6de100ac`（解压）、`ev_191f9115aa1ef846bf4ef0511c33a6d0c9291c11ccc18564a25828f007584ce1`（主函数汇编）、`ev_e759165448683a86b8af95adbe450d42d65ec09d63469873afaf996ab4e3ceec`（交接汇编）。完整保存在 `research/ace-boot-entry-20261019/rea-lk-handoff-snapshot.json`。

既有命令注册表及运行记录没有建立标准临时 `fastboot boot` 在本机可用的证据。此分析没有改变 bootloader，也没有添加该命令。

## ATF 选择异常级别

ATF 的 `MTK_SIP_KERNEL_BOOT` 表记录同时列出 `0x82000115` / `0xc2000115`，handler 指针对应文件偏移 `0x69c8`。handler 调用 `0x64c4` 准备非安全世界入口。

在 64 位路径中，`0x64f4` 读取 `ID_AA64PFR0_EL1`，检查 `[11:8]`：

- EL2 字段非零：入口 SPSR 为 `0x3c9`，即 EL2h、DAIF 屏蔽。
- EL2 字段为零：入口 SPSR 为 `0x3c5`，即 EL1h、DAIF 屏蔽。

独立 GNU 汇编补足了 context 到 ERET 的静态链：SIP dispatcher `0x152f0..0x15304` 剔除 FID 后传入 `kernel, DTB, 0, 1`；handler 返回 DTB，`0x1531c` 写入 saved x0。`0x75f0..0x7608` 选择非安全世界 context 为 SP_EL3；返回路径 `0x534c` 载入该 context 的 SCR/SPSR/ELR，`0x59f4` 恢复 x0..x29，最后 `0x5374` ERET。由此，这条首次启动、64 位分支的静态结果是内核 x0=DTB，并按 PFR0 条件进入 EL2h 或 EL1h；尚未在自定义真机镜像中测量。完整汇编保存在 `research/ace-secure-handoff-20261019/atf-context-ereturn-objdump.txt`。

该准备路径还受一次性启动标志及 `0xe1d0` 条件限制；后者读取的文件初值为 1。不能把静态条件选择写成已经测得真机 CurrentEL。`0x7528` 可见相应 EL2 状态初始化；context 恢复已做上述静态核对，完整运行时状态仍需执行证据核对。

REA 证据：`ev_eeed05b09777af7fbe4a31d79eb3ab3a410d8d464440af541380bbd5bfd743c9`（handler）、`ev_ae458d3520a7612ed8d3133a6423bc3cd1ccd91a85ccfc36a0d0eadc26f782eb`（EL 选择）、`ev_27157fec2e343ac8f5f4ff8e71ef954ff50f39cf14c52f1b8bed213ab6ec36fe`（条件）、`ev_0998d373fa1dc8d463e73941827804690bfacffc5dc0055ba479f18dc16b3fe6`（状态准备）。快照：`research/ace-secure-handoff-20261019/rea-atf-handoff-snapshot.json`。

这解释了现有探针的一个适配缺口：它只接受 EL1，会拒绝 EL2。修复的目标是支持在 EL2、MMU off 时采集 CPU 参数；它仍不是 XNU 启动层。

## 原厂 Linux 仿真结果

原厂 boot 中提取的内核通过受控 QEMU 启动：QEMU 8.2.2、TCG virt/GICv3、virtualization on、CPU max、单 CPU、768 MiB、无网络和磁盘。45 秒上限内，首轮 24.351 秒正常退出 0。

实际串口记录含 PID 1、`5.10.236-android12-9-o-g6973d81cd2ac`、三次心跳及 `reboot: Power down`；Protected nVHE KVM 初始化成功。内核没有 panic/BUG，存在非致命 cache hierarchy 检测提示。

内核 Image SHA-256：`8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0`。命令、输入输出校验和及复现脚本位于 `research/ace-stock-qemu-20261019/`。此结果只验证 QEMU 中的原厂 Linux。

## 距离刷入 iOS 的剩余工作

本轮进一步通过正常 Kbuild/modpost/LTO 流程生成最小寄存器诊断模块。使用精确 live kheaders 和原厂模块中真实的 module_layout/printk CRC；partial symvers 的 export 类型/namespace 依据同代官方源码推定。Clang 18 兼容调整保留 strict CFI、full LTO、SCS、PAC/BTI 和 zero-init；不是移除安全检查或强制加载。

候选模块 131,864 字节，SHA-256 `12655d3b3d8ecc3818d4541c800416975335cba37da2ef59f9cc228da3eac782`。它先在同版本原厂内核 QEMU 中以无 force 标志的 finit_module 加载、读取寄存器并正常卸载，11.697 秒退出 0。第一次测试 init 编译缺少等待变量，修正后第二次模块已成功但测试 init 漏了关机调用而超时；两次测试脚手架失败均保留，第三次才是完整通过。

随后在实际手机上，正常 insmod/rmmod 均返回 0。再用 taskset 将每次 insmod 的执行线程限制到 CPU 0..7，记录允许 CPU 列表并逐次加载、读取、卸载：

| CPU | MIDR | MMFR0 | TGran16 | CNTFRQ |
| --- | --- | --- | --- | --- |
| 0–3（A55） | `0x412fd050` | `0x101122` | 1 | 13,000,000 Hz |
| 4–7（A78） | `0x411fd411` | `0x101122` | 1 | 13,000,000 Hz |

这是 **8 核真机的 16KB 页能力位实测**，尚未实际建立 16KB 页表运行 XNU。Android boot_completed 保持 1，诊断模块在 /proc/modules 中已不存在，手机临时文件和目录均清理。内核 tainted 值前后同为 4609。未修改 SELinux、槽位、属性或手机启动/原始分区。

可复用源码及构建说明见 `diagnostics/ace-read-regs/`；私有构建、QEMU、真机证据分别在 `research/ace-kbuild-path-20261019/`、`research/ace-module-qemu-20261019/`、`research/ace-module-live-20261019/`。正常加载成功只验证这份最小模块及其使用的符号，不能推广到任意 vendor 模块 ABI。

还需要验证可观测的裸机自定义代码入口，完成 Ace 的 XNU 平台适配、MTK 存储和显示/输入驱动，并构建能在该交接协议下工作的镜像。尚无通过这些条件的 Ace iOS 启动镜像。

因此本轮不覆盖 userdata 或启动分区。项目规则要求对每一项破坏性写入单独确认；确认前必须先有具体镜像、验证结果及按槽位匹配的恢复方案。
