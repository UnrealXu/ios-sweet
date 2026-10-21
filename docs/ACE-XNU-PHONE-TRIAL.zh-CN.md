# Ace 真机 XNU 入口试验记录（2026-10-20）




## 最新真机结果：已越过 RTC 等待，进入根设备查找

修复内核 CI `39365892897` / job `118442546958` 全部成功，提交
`7b7ab595276e0b0dc4f0d0fd29532bd8be9a1ff0`。实际链接内核 SHA256：
`29ced29d720b2c4a6875ca12158da20c7ecb594074ed52bfb492cc16b0be3304`。
确认新的日历及 BSD 检查点已进入产物，原 IORTC 等待路径未进入 Ace 内核。

经九种加载器检查、真实内核 C 入口及四种 Android 回退检查后，64MiB候选
`05179f49f0a61ceedc8391559504a1c5df773cb3ff16a0259d59a1a384226567`
只写入一次 boot_b（Sending1.386s / Writing0.148s），本轮 token
`e7071f55bee79e82`。真机自动回退、约78.1秒恢复 ADB、完整取证及自动回
Fastboot 再次成功，未要求按键，未恢复原始备份；实际 boot/vendor 哈希匹配。

真机 pmsg 6939字节，SHA256：
`ca362464f5d2121bf24f9b9863ec53cb342fa244597ac9ba6f278476b79d6e0d`。
与新 AEE HWT03 中经完整 CRC/长度校验的 SYS_PSTORE_RAW 逐字节一致。
日志确认单次本轮 XNU 入口，原 IORTC wait begin 消失，并依次出现：

```
ACE init: RTC backend unavailable; calendar begin without service wait
ACE init: calendar end
ACE bsd_init: calling vfsinit
SWEET HFS: hfs-627.100.6 registered
ACE bsd_init: calling net_init_run
ACE bsd_init: calling inittodr
ACE bsd_init: calling setconf
```

因此，等待尚不存在的 RTC 服务这一启动阻塞已在真机上修复。硬件 RTC 后端仍未
实现，当前是内核原有的日历回退；网络栈初始化也不等于 MTK 无线网卡已可用。
新停点为 setconf 调用的 IOFindBSDRoot，未出现 vfs_mountroot、根文件系统
挂载或 iOS 用户空间启动证据。下一主线为 MTK UFS 控制器和根设备支持。
手机当前位于可识别 Fastboot，保留本轮实验镜像。

## 2026-10-20 后续：自动真机循环定位到 IORTC 服务等待

诊断内核 CI `39364098289` / job `118436788244` 成功，提交
`800f51c508411000d6479bffbf3318c0993bdb5d`。核对下载 ZIP 哈希并确认检查点
进入实际链接内核，内核 SHA256：
`849c6c92f707051ef2e8aba7a458009c375ff540ff236c90a4ef08744a031e8a`。

新64MiB候选 `1a3e5dcf38f5e81b76ab516e4f5dc3d115d8d19f432e484a827e5e93dc891afc`
实际只写入一次 boot_b（Sending1.386s / Writing0.153s），token
`8bcc77973fc4cff6`。自动循环再次成功，78.1秒返回 ADB，取证、回读 boot/vendor
哈希后自动进入 Fastboot；未要求用户手动按键。写入前曾因用户拔线而拒绝操作，
重新插线后才执行实际写入；第一次守卫拒绝没有发生分区写入。

本轮日志4538字节，SHA256：
`84d16a06907cfe7298d4add6e31174ff61ecd6f965018ea6c3ae7401f74f72ca`，
与完整 CRC 校验通过的 AEE `SYS_PSTORE_RAW` 逐字节一致。实际输出：

```
ACE init: IORTC wait begin ticks=235212007 ctl=1 cval=e06aaff cnt=e050ce7
```

没有读到 wait end 或 calendar begin。固件记录38.139082秒看门狗超时，
CPU 位于 cpu_idle。计数器按13MHz折算约18.09秒，定时器已启用、未屏蔽，
比较值约在8.15ms之后；这不单独证明定时器中断已送达，也不证明不同日志的
时钟原点完全相同。源码确定 IORTC 等待时长为30秒，而 Ace 尚无注册的 RTC 后端。

针对这处已定位等待，新增 `0089-ace-skip-unavailable-rtc-service-wait.patch`
（本地提交 `35968da`）：Ace 不等待尚未实现的 RTC 服务，仍执行原有日历
初始化；不伪造 RTC 服务或写入硬件时间。同时将仅 Ace 启用的 BSD 检查点
改用可进入当前 pmsg 的 printf 路径。六项本地 Mach-O 编译通过，SWEET 代码、
数据和重定位不变。该修复正在构建，尚未进行真机修复验证；RTC 硬件支持及
可用 iOS 仍未完成。

## 最新：失败后自动取日志并返回 Fastboot 已通过真机验证

自动回退实现提交 `7127efa`。本轮64MiB镜像 SHA256：
`4115699ecafe3ed09e0995d299562d18d89a34a2f7980cc01c91112a5ff24b7c`，
本轮 token `99d570dcb4a4177a`。实际只写入一次 boot_b，正常重启后：

1. XNU 真实进入并完成 VM、平台专家和 MAC 框架初始化。
2. 看门狗重启后，同一实验镜像识别本轮未完成标记，自动进入 Android 诊断通路。
3. 约76.1秒出现 ADB；电脑核对当前 token、root、B槽和 boot/vendor 完整哈希。
4. 自动保存 pstore、dmesg 和完整 AEE，然后通过 ADB 自动重启到 Fastboot。
5. Fastboot 回读产品、B槽、解锁状态均匹配，全流程未要求用户按键。

实际诊断属性为 stage5/error-67/fallback0，SHA256：
`17d50af667a5c21b7c7cc3895314d2b086bcb0a4ed63ebb1746bd7d78d340725`。
本轮 pmsg 4463字节，仅有一次 armed 和一次 XNU 入口，SHA256：
`77a063b0a5de35b9cbc85c78ccb3e6e0df5b46db48f343bee535fd66ba078baf`。
这些证据验证了一次真机试启动后的自动诊断回退，没有将 Android 诊断启动当作 iOS 成功。

电脑端流程在 `tools/ace-auto-trial.py`。它消费一次已校验刷写的状态，
不会自行重刷、改槽或恢复备份。以后新候选必须使用新 token，取证后修复源码、
验证并封装新候选，再进入下一轮。当前真机处于可识别的 Fastboot，实验镜像保留。
断电、保留 RAM 丢失、日志环覆盖或更早的固件故障仍可能需要实体按键协助。
存储、显示、触摸和可用 iOS 仍未完成。

## 同日后续：关闭进度图的候选已进行真机试验

修复提交 `02ec955`，64MiB boot_b 候选完整 SHA256：
`9dc91668ddb38809197b2206fd4b38587239ebf7b1bb4db99b21a652012d8c62`，
唯一 token 为 `4e277e71127ec9df`。208项主机检查、8种原生加载器检查、
真实 XNU C 入口检查和4种 Android 拒绝诊断检查通过。未重编相同内核。
实际写入一次（Sending1.632s / Writing0.163s），正常重启后90.2秒未出现
ADB。用户已再次按键进入 Fastboot，下一轮日志读取镜像已写入一次：
`5d9d07d492098ee0cc39d194239633a8a15afa6efa1d1048ecc68fee33fa2fdf`。
其自身 token `6c327eb996a02bef`，只读查找上一轮 `4e277e71127ec9df`。
读取完成前，不能声称原断言已消失或 XNU 已到达更后阶段。未恢复原始备份。

## 2026-10-20 真机已进入 XNU 虚拟内存初始化

读取镜像 f167882c…8c4ae7 成功写入一次 boot_b，正常重启约28秒恢复 ADB。
root 回读 boot_b 完整哈希匹配，vendor_boot_b 哈希未变；未恢复原始备份。
当前288字节诊断属性的 SHA256 为
`b97ddfbc0893ee7da2bfeb84f345da28e5c1026b7fe4a76ba34110a2c9c20bd0`。
只读探测得到有效 pmsg 环（start/size均49777），13条上一轮唯一 token
`f9eb9c6ce0704133` 的 XNU 入口记录。

独立从 Android pstore 提取的49777字节日志 SHA256 为
`3c558d8a64d00aa44e31478f4d78010cd0103100a0c78328f38e3772ff242398`。
其中包含13次 Darwin22.6.0、pmap startup、VM bootstrap done，随后均出现：

```
panic(cpu 0 caller 0xfffffe0007af1cc0): pe_init.c:314 Assertion failed: *delta >= 0
MACH Reboot
```

新取回的 HWT01 解包55个条目全部通过完整 CRC/长度校验，其 SYS_PSTORE_RAW
也有13条相同唯一标记。这是实际手机 XNU 已执行到 C/MMU/虚拟内存初始化的
证据，不是 QEMU 或读取镜像内的字符串。该轮未启动可用 iOS。

现有 BootArgs 视频字段故意为零。XNU 的 OSX 配置默认绘制启动进度图，
显示高度零会使 pe_init.c 的位置调整断言失败。下一候选仅增加内核现有
`-noprogress` 参数，关闭尚无显示驱动可支撑的绘图；保留相同 CI 内核、
日志、原厂 Android 拒绝诊断通路和 Magisk ramdisk。新候选的真机结果
需单独验证；存储、显示、触摸和 iOS 用户空间仍未完成。


最新状态补充：初始化修复源码 9d6ebd9 已通过 207 项测试、8 项加载用例
（含全零日志区进入真实 XNU 的模拟验证）、C 入口及 Android 诊断验证。
新候选 b5a0a166…a38fb3 已实际写入一次并重启；90 秒未检测到 ADB，
还不能据此确认初始化成功或 XNU 执行。没有恢复原始备份。

为读取这轮证据，源码 4f9e6dc 新增专用读取模式：主动在阶段 2 返回
-66，直接进入现有 Android；不尝试 XNU、不写 pmsg。208 项主机测试
及 5 项 QEMU 用例通过，其中一个标记匹配用例明确使用合成输入，只
验证读取机制，不能算作 XNU 执行证据。

读取候选 64 MiB，SHA256：
f167882c8e47c23e59459895fb5f2330170710b38f12ca837a30dd0b948c4ae7。
它将查找上一轮标记 f9eb9c6ce0704133。目前仅已准备，尚未写入；
等待用户按键让手机回到 Fastboot 后，会按已有持续授权直接执行，
不再请求刷写批准。保护分区、GPT 及原始备份保持完整。

## 前一轮已经核对的真机诊断结果

当前真机状态：第三份试验镜像 6196459a…a393c11 已写入 boot_b，
保留安装并成功通过新诊断路径进入 Android。实际读取的 288 字节
设备树属性携带本次标记 bbc504000c851102，证实原生加载器到达阶段 5，
错误 -64，pmsg 底层错误 -3（日志头无效）。它已完成 CPU／设备树／平台
准备，但在物化和跳入 XNU 前停止。**尚无 XNU 真机启动成功证据，
也未实现可用 iOS。**

USB ADB 在重启 28.1 秒后自动返回，Android 启动完成、B 槽、root、
SELinux 及 boot_b／vendor_boot_b 实际哈希均已核对。没有恢复原始
备份。用户最新明确授权：本项目范围内完成镜像、哈希、设备和备份
核验后直接执行后续必要写入，不再逐次询问；保护分区、GPT 和备份
仍保留。见 AGENTS.md。

## 第三份镜像与真机证据

- boot_b SHA256：6196459a8598ea4de4c4fe29281d4ac6e162671e42f479f2bfc143b39a393c11。
- 仅一次 64 MiB 写入：发送 OKAY 1.383 秒、写入 OKAY 0.134 秒，
  总计 1.519 秒。没有写入其他分区或切换槽位。
- 真实原生 Image 地址 0x40000000..0x44a00000；原厂 Android
  入口 0x41400000；复制的诊断设备树 0x44800000。
- 诊断属性 SHA256：5841fc7186c02078c89d73307ae0c7944cb327c28af0bdbd3e99834f8038fbff。
- vendor_boot_b SHA256：bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670，未改变。
- 源码提交 2a1791e；203 项主机测试、7 项加载／拒绝／重定位验证、
  XNU C 入口验证、4 项 Android 诊断通路验证通过。上述模拟证据与
  本段真机属性及哈希证据分别保存，没有把 Android 返回当作 iOS 成功。
- 私有记录：research/ace-xnu-refusal-20261020/phone-trial/。

错误 -3 尚不能区分全零的未初始化区和其他损坏日志头。新提交
2e3d215 提供独立的全零区初始化函数，三个测试通过；非空损坏数据
绝不覆盖。它尚未接入或刷入真机，下一步加入显式开关、重新构建并
验证全零区可进入 XNU的用例，然后继续真机验证。

## 早前试验记录

## 本次具体候选

- 分区：仅当前 B 槽的 `boot_b`，完整 64 MiB。
- 文件：`research/ace-xnu-entrylog-20261020/boot-candidate/experimental-xnu-boot-b.img`
- SHA256：`15498cfc252fa390d376dd5aace4b6a77486ea1833f5e994da7c43b3a995b78e`
- 内嵌实际 XNU SHA256：`c1232a8df639bc0551c69bff9118e4906ea344072ea63ac4e64406e71e18f366`
- 本次运行标记：`6f45b6931edfabcc`，试验前手机 pstore 中未发现该标记。
- 保留原有 Magisk ramdisk；不更改 userdata、vendor_boot、vbmeta、
  bootloader、recovery、modem、persist 或 GPT。
- 沿用旧 AVB 元数据的既有布局方式并重新定位 footer；这不是有效
  签名或认证声明，仍需验证实际 bootloader 是否接受此候选。

## 已有证据及范围

[个人仓库完整 CI 39308647764](https://github.com/UnrealXu/ios-sweet/actions/runs/39308647764)
成功，源提交 `91d962576c40ba56c28eb6712a9a661669d4a5e0`。新增门禁
确认真实链接内核含两个入口符号。下载 ZIP 和内含 SHA256SUMS 均已校验。
内核入口的 676 字节与实际执行过测试的机器码逐字节一致。

使用新内核完成七个完整加载/拒绝/重定位用例。另一次实际 XNU
执行越过 16K 页表初始化，到达 `arm_init` 并执行首条 C 指令；
带本次标记的入口日志仍在 QEMU 物理 RAM 中。以上均为 QEMU 证据，
不能证明手机控制器、固件交接或持久日志在真实复位后的行为。

最初 C 入口验证在页表启用后仍按虚拟地址读取 pmsg 的物理地址，
因此日志提取失败。失败目录已保留；修正为 QEMU 官方支持的
[物理内存读取模式](https://www.qemu.org/docs/master/system/gdb.html#examining-physical-memory)
后重跑通过。未为此修改内核或原生 Image。

原生程序仍依赖固件交接的 RAM 所有权及其他 CPU/DMA 静止条件；
数值边界检查不证明这些条件。候选没有自动返回 Android 的路径，
可能停在早期启动、黑屏或挂起。

## 恢复的具体镜像与条件

- 原始备份：`research/ace-backup-20261019-wireless-v2/boot_b.img`
- 大小：64 MiB，已重新计算并核对 SHA256。
- SHA256：`ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10`
- 试验前安装的诊断镜像 SHA256（现已被原始备份替代）：
  `e2d7475e99d3449e7dbcf16e473a65a27a8f3ceae19278744ae32b3601ed834d`
- 实际恢复：手动按键进入已解锁 USB bootloader，原始备份写回一次。
  Fastboot 发送 OKAY 1.382 秒、写入 OKAY 0.150 秒，总计 1.533 秒。
  松开全部按键后的第二次普通重启返回 Android；本机不支持 fastboot boot。
- 实际读取 boot_b SHA256 与上述原始备份一致；vendor_boot_b SHA256
  为 bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670，未改变。
- 本次仅两次 boot_b 写入：候选一次、已授权恢复一次。无其他分区写入。

本次授权“开始写入试验镜像、试验后恢复原始备份，继续”已全部执行，
不应重复执行。后续遵循用户新的保留试验镜像流程。

## 真机日志与下一步

恢复后 pstore 目录为空。不能据此证明 XNU 没有执行；强制复位和
Fastboot 恢复下载后 RAM 日志是否保留，目前没有证据。
只读提取的 MTK HWT 故障文件，经实际运行的厂商程序和 libaedv.so
逆向分析后，55 个条目已全部解开，并逐项通过长度及完整 CRC 校验。
其 TFA_DEBUG_BUF 记录看门狗超时，CPU0 PC=0x40000114、
LR=0x40000100、SP=0x4103c8a0；三者与本次加载器的停机循环、
native_main 返回地址和栈顶完全吻合。这高度符合加载器主动拒绝继续
启动，但没有唯一试验标记，早期时钟也未校准，仍不能严格归因到某次
启动，更不能证明 XNU 已运行。确切失败阶段和错误码尚未记录。

## 第二份诊断候选（已写入，现保留）

已修改加载器：失败停机时使用不同的 WFE 循环地址编码阶段和错误码，
供固件看门狗记录 PC 后解读；不改变栈，不绕过安全检查，不额外写入
内存或控制器。早期汇编拒绝仍沿用原有独立停机路径。

- 新候选：research/ace-xnu-entrylog-20261020/boot-candidate-haltpc/experimental-xnu-boot-b.img。
- 大小 64 MiB，SHA256：
  2bf31f3fdc525f82fa0b17d16106e4c45f0de0422393f6022213d0c0d727d9c7。
- 含同一已通过 CI 的真实 XNU；新运行标记 ac4d16d6e0c417e9。
- 七项 QEMU 加载／拒绝／重定位验证通过，其中两项实际验证 PC 错误码
  和未改变的栈地址；XNU 16K 页表启动及 arm_init 首条指令验证通过；
  五项原生 Image 测试通过。这些仍只是电脑端证据。
- 用户已明确同意这一次写入，随后重新插紧数据线。设备身份、root、
  B 槽、当前原始分区哈希及 bootloader 写入条件均已核对。
- boot_b 仅写入一次：发送 OKAY 1.374 秒，写入 OKAY 0.143 秒，
  总计 1.519 秒；正常重启后 55 秒未检测到 ADB／Fastboot。
- 用户报告一加标志后黑屏，随后按键进入 Fastboot。当前 B 槽状态
  successful=yes、unbootable=no、retry=1。没有再刷写或切换启动槽。
- 只读执行已核对实现的 oem dump_pllk_log，导出 314113 字节，
  返回成功，耗时 0.752 秒；它只包含当前 PL／LK 启动过程，未找到
  上一次的 TFA CPU0 停机地址。因此这次仍无法解出实际阶段和错误码。
- A 槽备份使用较旧的内核且没有 Magisk 标记，未切换启动它。

后续先实现和验证“原生加载器检查失败时携带诊断结果进入现有 Android”
的可选路径，保留试验 boot 镜像，解决日志读取通路。当前候选没有此
功能；必须先完成边界检查和实际执行验证，再提出新的具体刷写候选。

PC 解码仅用于新镜像：减去实际 Image 加载基址和符号 native_halt_slots
偏移 0x148，确认落在 0x2400 字节表内，然后除以 8 得到槽号；
阶段桶为槽号除以 128，负错误码为槽号模 128 的相反数。阶段桶 8
表示异常／未知阶段，错误桶 127 也可能是超界值。不能用此表解释旧镜像。
