# Ace XNU 启动层：当前实现与验证边界

目标是在 PGKM10/MT6895 真机运行 XNU，再接通 iOS 所需的存储、显示、
触摸等功能。目前没有可部署的 Ace iOS 镜像。

最新 ADT、时钟交接和个人 fork CI 状态见
[ACE-XNU-ADT.zh-CN.md](ACE-XNU-ADT.zh-CN.md)。

## 完整 Ace 构建修复（2026-10-20）

修复后的第三轮 [CI 39288876908](https://github.com/UnrealXu/ios-sweet/actions/runs/39288876908)
已完整成功（job `118183995118`），来源为个人 fork 的
`5ea487d7f403efb8739115550098bd568c7069b3`。实际产物、指令检查和加载器
校验见 [载荷验证记录](ACE-XNU-PAYLOAD.zh-CN.md)。下述两轮失败是修复前历史。

完整构建 `39283161766` 和带完整日志的 `39287049187` 均失败，尚未产出
Ace 内核。第二轮日志明确显示 14 个 BearSSL 文件找不到 `inner.h`：
源码准备脚本已接受 ACE，但 `libkern/conf/Makefile.template` 的头文件
路径和 `-mgeneral-regs-only` 条件仍仅接受 SWEET。

`0086-ace-bearssl-build-flags.patch` 将该软件依赖条件扩展为 SWEET/ACE，
不启用 Qualcomm 驱动。使用真实 Ace CI 配置和头文件先复现缺头文件，
再用 GNU make 从补丁后的实际模板展开每个对象的参数，相关 19 个对象
均编译为 arm64 Mach-O 成功。GNU make 回归同时检查 SWEET/ACE/VMAPPLE，
完整主机测试 171 项通过。第三轮成功链接确认本次构建故障已修复。

构建流程现将未过滤的 `xnu-build.log` 单独上传，网页仅显示精简错误及
上下文；`pipefail` 保留原构建退出码，避免网页截断约 12 万行日志后
无法定位失败。证据在私有 `research/ace-ci-second-20261020/`。

## 已确认的入口

一次单独授权的 boot_b 诊断写入已执行。自定义前缀在真机记录了 EL1、
13MHz 时基与传入 FDT 地址，然后进入字节不变的原厂 Android 内核。
普通重启后的 pmsg 中取回完整记录。它证明了自定义代码入口和这一轮的
日志保留；没有执行 XNU、16K 页表或 MTK 裸机驱动。

当前诊断 boot_b 保持安装，Android 可正常启动。恢复原 boot_b 的单独
授权仍在等待；本阶段不重复写入诊断镜像，也不改变其他分区。

## 0082：分离固定 Redmi 帧缓冲

现有 SWEET 内核的 `SWEET` 宏同时控制通用 ARM/GIC 改动与 Redmi 专用
早期屏幕输出。直接复用它会在读取平台设备树之前写入 `0x9c000000`，
并在启动页表和最终页表中建立该地址的 32MiB 映射。Ace 的 LK 帧缓冲
元数据不同，其格式、步幅和 16K 对齐后的额外内存归属尚未确认。

`0082-separate-sweet-early-framebuffer.patch` 把以下路径统一放到
`SWEET_HAS_EARLY_FB` 能力开关之后：

- `start.s` 的第一阶段像素写入及启动页表映射；
- `arm_vm_init.c` 的最终映射及控制台地址切换；
- `sweet_early.c` 的屏幕输出和 panic 输出实现。

SWEET 默认值仍为 1。显式设置 `-DSWEET_HAS_EARLY_FB=0` 时，头文件为
调用者提供空操作，不留下待链接的早期屏幕函数。关闭后也没有新增日志
后端；Ace 的 XNU 早期日志及其跨页表映射仍须实现。这个开关仅解决早期
固定地址访问，不能使 SWEET 内核直接用于 Ace。后续 `sweet-fbcon` ADT
驱动、Qualcomm UFS/SPMI/RPMh/USB/触摸路径也没有被这个开关关闭。

## 本地编译验证（2026-10-19）

基线来自成功的 GitHub Actions run `39158169212`、提交
`fdad0de8dc0e75c5ea84762adc03f7232dc91f19` 的缓存源码及生成头文件。
使用该构建树的 `.CFLAGS`、`.SFLAGS` 重放相关编译，Linux clang 18
生成真实 arm64 Mach-O 目标文件；这不是新的 macOS 全内核构建或链接。

`start.s`、`sweet_early.c`、`arm_vm_init.c`、`debug.c`、`pe_serial.c`
分别编译原基线、补丁默认值、补丁关闭值，合计 15 次成功：

- 默认值的 5 个目标文件与原基线逐字节相同。
- 关闭值的 5 个目标文件经 `llvm-nm` 检查均无 `sweet_early` 符号或引用。
- 现有 136 项主机测试通过，耗时 26.347 秒。

重放前必须同步改动的两个 `EXPORT_HDRS` 副本；仅修改源码但复用旧导出
头文件会误测。开发中发现并修正了这一验证环境问题，最终结果在同步后
重新生成。原缓存构建树未修改。

私有证据目录：`research/ace-xnu-console-20261019/`，包括编译脚本、
15 个目标文件、编译结果及哈希、`verification.json` 和测试日志。
`gh auth status` 当前未登录；连接器下载旧 CI 日志又返回 Transport
closed，因此使用缓存的构建参数，没有虚构新 CI run。

本轮只读 USB ADB 检查确认 Android/root/Enforcing 正常，boot_b 和
vendor_boot_b 哈希与此前记录一致；没有重启、刷写、控制器 MMIO 或 DMA。

## 0083：Ace 初始机器配置（源码阶段）

新增 `MACHINE_CONFIG=ACE`、`MASTER.arm64.ace` 和 `ACE.h`。此目标先限制
为一个 CPU，使用已观察的 PPI27，关闭固定 Redmi 帧缓冲。16K 页表和
GICv3 仍需真机执行验证；这些编译选项本身不能证明硬件启动成功。

为复用已有 OSS 密码算法、pthread/HFS 和软件兼容实现，ACE 编译命令
保留历史 `ARM64_BOARD_CONFIG_SWEET` 选择标记，同时增加独立的
`ARM64_BOARD_CONFIG_ACE`。板级头文件优先选择 ACE；Qualcomm 外设代码
明确排除 ACE，不能仅检查 SWEET 标记来决定是否启用硬件驱动。

已排除原 Qualcomm UFS、SPMI、RPMh、USB、按键、触摸六个控制器实现、
电池及帧缓冲实现，以及 UFS root、UFS 日志、后期 Redmi fbcon 的调用。
Ace 的内建匹配表只增加平台专家和启动 CPU，不注册尚未移植的显示、
输入、电池或密钥服务。CPU/平台专家复用现有通用代码，CPU 标签改为
Ace Cortex-A55；其单核 IRQ 和 IOKit 启动路径尚未在真机执行。

还修复了三个依赖暂存脚本原先只接受 SWEET 的问题，使 ACE 也会暂存
同一版本的 OSS pthread、BearSSL 和 HFS。完整构建不能依赖主机缓存里
碰巧已经存在这些源码。

最终本地验证使用真实缓存构建参数、同步后的导出头文件：

- 21 个源文件在基线、SWEET、ACE 三种配置下共 63 次真实 Mach-O 编译成功。
  统一编译路径前缀后，21 个 SWEET 目标文件均与基线逐字节一致。
- `llvm-nm` 确认 ACE 的 9 个上述硬件/早期控制台实现单元无全局符号，
  5 个调用单元没有残留的 UFS/日志/早期 framebuffer 引用。
- 实际 `genassym.c` 在 SWEET 和 ACE 配置下分别生成汇编；每种配置的
  136 个常量全部匹配缓存 `assym.s`。这排除了此次编译复用旧汇编偏移
  的已检查范围，不替代完整配置再生成和全内核链接。
- 5 项新回归测试覆盖真实头文件 ABI、禁止重新启用 Redmi 早期屏幕、
  外设实现排除、IOKit 匹配表、依赖脚本的 ACE 入口。

最终证据：`research/ace-xnu-platform-20261019/verification.json`、
`genassym-verification.json`、编译目标文件、测试日志和源码哈希。
完整内核尚未构建或链接；没有生成/刷写 Ace XNU 镜像或进行新的手机
操作。`gh` 未登录，GitHub 连接器返回仓库权限 `pull=true,push=false`，
因而尚不能提交 CI 构建，也没有新 run ID。此限制与源码尚缺 ADT/早期
日志、内存归属及 MTK 控制器移植是不同的未完成事项。

内存清单补充：同一真机 FDT 有 51 个保留区节点，其中 3 个仅给动态
分配要求，2 个没有 `alloc-ranges`。因此不能仅凭某个高地址窗口没有
固定 `reg` 重叠，就把它交给 XNU。旧 Android 日志记录了两个 CMA 池的
实际分配位置，但它们只是那次 Android 启动的结果，不构成下一次原生
启动的内存所有权保证。目前仍未选定可部署的 XNU RAM 默认地址。
私有清单及日志来源哈希保存在同一证据目录。

最新阶段见 [Ace pmsg 与 Cortex-A55 编译目标](ACE-XNU-PMSG.zh-CN.md)：
已增加正常 KPRINTF 阶段的日志后端，并通过真机 CPU0 的准确 PC SIGILL
查明隐含 M1 编译目标造成的 STLUR 问题，ACE 已显式指定 Cortex-A55。
新后端尚未真机执行，第一条 XNU 指令到 MMU 切换之前的日志仍未覆盖。

## 接下来的实质工作

ACE 全内核已成功链接。下一步采用真机观察的
13MHz/PPI27、GIC 地址及 CPU affinity；从实际 FDT 和完整保留区构造
有明确内存归属的 ADT/BootArgs，并接通 XNU 日志、16K 映射和异常处理。
这些条件满足后才能提交具体真机启动镜像和回滚方案。存储、DSI 显示与
触摸控制器仍需移植和真机验证，不能以协议编解码测试代替。
