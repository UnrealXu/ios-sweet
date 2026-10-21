# Ace 真机入口探针：候选与回滚计划

持续目标：在用户的 OnePlus Ace PGKM10／MT6895 真机启动真正的 XNU＋iOS 用户空间，并验证正常操作。诊断模块、QEMU、合成接收程序、Android 启动器均不构成目标完成。最低验收包括系统真实启动、屏幕/触摸/按键、解锁与基本应用、存储持久化和重启稳定性；其余日常功能仍需逐项实现和验证。

## 已取得的真机证据

2026-10-19：USB 与已配对无线 ADB 在线，root/Enforcing/B槽/boot_completed1。只读校验实际 vendor_boot_b 与备份SHA一致。随后执行真实 USB bootloader 往返，只发getvar和普通reboot：产品k6895v1_64、slotb、unlockedyes、非userspace、最大下载0x4000000；返回Android、boot ID变化，boot_b/vendor_boot_b SHA未变。没有flash、erase或set_active。原始证据在忽略目录research/ace-goal-device-20261019/usb-roundtrip。

运行中物理Kernel code从0x40000000开始，initrd为0x66f00000..0x69509a70，pmsg位于已有0x48080000..0x4817ffff保留范围。候选预计在原加载基址后2MiB进入相同内核；这些运行中范围不能完全证明下一次LK handoff的所有动态RAM ownership。

实际备份vendor_boot_b解码出929个CPIO条目。其fastbootd SHA0c7f65e119aad92a4e154792cf3ddac2a5a80c4f4fb1478233ea72de9d67a55d，MTK HAL SHA db2c2f4fcee3764e90fad8619a35215f4e25641bd1492a52b4bcd2e74ac431fb。REA核对：

- fastbootd构造函数建立18个命令处理器，包括download/flash/reboot/oem/fetch等，没有boot/continue；ExecuteCommands查表失败返回Unrecognized command。Evidence ev_bc86678ea38ba056e092f4fd52a0fffbff731934375b4381c4f267d02379b6e0。
- DownloadHandler仅分配/接收数据并返回状态；OemCmdHandler调用HAL，另有一个直接失败的postwipedata特殊匹配。Evidence ev_6a060e44adf3c444d1536407f1845185e2c6d2afed3fa26f887204d980cddd6e。
- 所提取MTK HAL的doOemCommand始终返回status3和不支持消息，没有执行下载内核。Evidence ev_e1599d1d4358f262e74e350d08c83d8e68fd02f3dd8517159365aaa30d008d68。

此为真实载体的静态分析，不是执行了OEM命令，也不是整个固件所有私有入口均不存在的证明；实际HAL服务绑定路径尚未运行核对。两个REA会话均已保存并关闭。它补足先前只参考AOSP的范围限制。

## 本次候选：诊断后继续现有Android

[实现说明](../ace/stock-chain/README.md)。先验证可回到Android的最小自定义入口，再逐步推进XNU与MTK控制器。代码不切EL、不改MMU/GIC/timer、不发送SMC/reset或存储命令。它仅向已有规范DBGC环追加带唯一token的诊断，失败则不写目标并继续原厂内核。

6项QEMU先验检查均完整执行了相同前缀与原厂内核，逐次校验完整运行中kernel dump SHA、交接参数和精确日志；随后正常模块加载/卸载并关机。真实手机接收该镜像、裸机日志保留及驱动仍未验证，不能据此宣称真机启动成功。

唯一当前候选：

- 文件：research/ace-stock-chain-20261019/final-review-candidate/diagnostic-boot-b.img
- 大小：67,108,864字节（64MiB，整分区）。SHA256：e2d7475e99d3449e7dbcf16e473a65a27a8f3ceae19278744ae32b3601ed834d。
- 内嵌原厂kernel原字节SHA：8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0。
- 当前Magisk ramdisk原字节SHA：54961de2dad343c35295905f1f1811b80d176e725b9fa93c48aada8e96fa90d2。
- 日志token：f283070db2b9aa1092d13ca9。
- 只允许本次提议写入boot_b；不写userdata/vendor_boot/vbmeta/GPT/bootloader/recovery/modem/persist，不切槽。

原始firmware与当前Magisk boot的AVB元数据1600字节完全相同（SHA c80565ce5c50d72aecf13bf253071213974c76df6f9fbf9c99a9cda2a68bb16c），但ramdisk长度与footer位置不同，当前手机确实在unlocked/orange状态运行。候选复用这一形状：保留过时的元数据字节，移动到新载荷末尾、更新footer位置并填充至整个64MiB。新载荷不具备有效认证；这种形状在新镜像上是否被LK接受仍需实测。早期review-candidate裸文件遗漏此整分区处理，只保留为历史，不得刷写。

## 执行前门槛与回滚

写入前再次核对唯一正确USB设备、PGKM10/MT6895产品、B槽/unlocked、当前boot/vendor_boot SHA、候选/manifest/证据/源码哈希，以及已有备份。先保存旧pstore。任何不匹配即停止，不以其他镜像替代。项目要求用户单独确认这一具体boot_b写入；当前尚未执行或获得该步骤确认。

回滚载体：research/ace-backup-20261019-wireless-v2/boot_b.img，67,108,864字节，SHA ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10。恢复时只能将此精确文件写回boot_b，随后普通reboot；恢复写入同样须先取得该具体步骤确认。当前已验证USB软件方式进入bootloader与返回Android，**未实际测试按键进bootloader或备份恢复写入**，不能把回滚称为已完成实测。

写入后必须核对flash返回值，普通reboot后等待Android、root、SELinux与USB/无线ADB；读取新boot ID、实际boot_b SHA、物理Kernel code位置和pstore唯一token/原始记录。启动失败则先恢复bootloader连接、核对设备，再处理回滚，不盲目重试或改其他分区。没有token不能假装已取得裸机寄存器证据。Android恢复与回滚完成是各自独立的验收项。

若新内核路径无法启动Android，可能需要人在手机旁通过按键恢复。OnePlus官方支持提供通用的强制重启说明，但不是这台PGKM10按键进入fastboot的实测证据：[官方重启支持](https://service.oneplus.com/in/search/search-detail?id=2235001)。不能依据其他型号的组合键宣称本机恢复通路已验证。

## 真机执行结果（已授权的第一次写入）

已实际写入上述精确候选一次：Sending65536KB OKAY1.379s、Writingboot_b OKAY0.140s、总1.522s。普通fastboot reboot后Android正常启动，root/Enforcing/B槽正常，boot_b哈希等于候选、vendor_boot未变，Kernel code从0x40000000移动至0x40200000。首次pmsg仅62字节，无本次marker；保留这一未完成记录，不虚构寄存器结果。

随后**未再刷写**，只做Android普通reboot。第二次Android正常返回，boot ID再次变化、分区哈希不变；pmsg439字节确实包含唯一token和完整80字节记录（偏移359）。实测EL1、DTB PA0x47c80000、SCTLR0x30d00800（M/C/EE关闭）、MIDR0x412fd050、MMFR00x101122、CNTFRQ13MHz、logger0、原厂内核入口0x40200000。证据在research/ace-stock-chain-20261019/phone-test1/normal-reboot2/result-verified.json。

这验证了真机自定义前缀、普通重启日志保留及Android继续启动；**不是XNU/iOS或16KiB映射/MTK裸机驱动验证**。首次日志缺失的具体原因未确定，不能推断两次启动的全部状态相同或宣称EL2已实测。当前诊断仍在boot_b，原备份尚未恢复；恢复步骤须另行明确确认。
