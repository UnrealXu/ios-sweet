# Ace：现有内核与非刷写启动入口的边界

2026-10-19。**当前没有已经验证的“把自定义内核放进 RAM 并切换过去”的 Ace 入口。** 已证明诊断模块能在现有 Android 内核中运行，但这与启动新的内核不同。

入口调查读取本地配置、已有实测记录和联网取得的官方源码，并用 REA 继续分析原始 LK 字节；没有再次执行已失败的 `fastboot boot`，没有重启、模块加载、kexec/SMC、OEM 命令或分区写入。最后仅通过已授权 ADB 只读确认 Android 启动完成、B槽、root、Enforcing 与无线调试 tls-ready；原始健康检查保存在忽略目录。

## 可以排除的标准路径

| 路径 | 现有证据与结论 |
|---|---|
| 普通 `kexec_load` | 原厂配置明确 `CONFIG_KEXEC=n`，没有编入标准后端。获得 root 或安装 kexec-tools 不会补上内核功能。 |
| 文件式 `kexec_file_load` | `CONFIG_KEXEC_FILE=n`，同样缺少后端；换一种用户态参数不能解决。 |
| 标准 kdump/crash kernel | `CONFIG_CRASH_DUMP=n`，`CONFIG_KEXEC_CORE` 未定义。不能把 panic、SysRq 或崩溃转储当作已存在的新内核入口。 |
| 标准休眠恢复 | `CONFIG_HIBERNATION=n`，不是现成替代路径。 |
| LK 标准临时 `fastboot boot` | 已有真机记录：64 MiB 下载成功后，`boot` 返回 `unknown command`；Android 随后正常恢复且 boot/vendor_boot 哈希未变。本轮没有重试。 |
| AOSP 标准 fastbootd | Android 15 参考实现的命令表没有 `boot` 或 `continue`，未知命令直接失败。它提供下载、刷写、逻辑分区管理及重启等功能，不提供标准 RAM 新内核启动器。 |

配置依据是已固定 SHA 的原厂 Image 内嵌配置；其 **2,895 个启用配置项与实际取得的 live autoconf.h 全部相同**。KEXEC/FILE/CRASH_DUMP 是明确关闭项；KEXEC_CORE 是未定义项，不能误写成配置文件中有一条显式关闭记录。证据位于忽略目录 `research/ace-entry-options-20261019/verification.json`。

官方同代 ARM64 Kconfig 将 KEXEC/KEXEC_FILE 定义为 `bool`，并由它们选择 KEXEC_CORE；它们不是可直接补装的普通模块。Makefile 按这些选项决定是否链接后端，缺失系统调用有 ENOSYS fallback，`reboot(KEXEC)` 分支也受 KEXEC_CORE 控制。本轮没有在手机上调用这些系统调用；结论是标准构建路径缺失，不声称已测量每个 OEM syscall 返回值。[OnePlus ARM64 Kconfig](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/arch/arm64/Kconfig)、[kernel Makefile](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/kernel/Makefile)、[sys_ni.c](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/kernel/sys_ni.c)。该公开 commit 不是已证明的运行内核源码；配置本身来自实际原厂产物及 live headers。

## fastbootd、recovery 能做什么

AOSP fastbootd 已运行在 Linux 用户态。`download` 把数据接收到内存缓冲区，接下来仍需要设备端实现相应处理命令；下载成功不等于执行成功。电脑端 fastboot 工具具有 `Boot()` 分支，也不能证明设备端实现它。[AOSP fastbootd 命令表](https://android.googlesource.com/platform/system/core/+/android-15.0.0_r1/fastboot/device/fastboot_device.cpp)、[下载处理](https://android.googlesource.com/platform/system/core/+/android-15.0.0_r1/fastboot/device/commands.cpp)。

Recovery 不只是刷写程序：它也是维修、ADB、更新等功能的运行环境。但启动 recovery、切换 fastbootd 或 ADB sideload 并不会自动产生新的 kernel loader。官方设计允许 recovery 与 fastbootd 共享内核；进入 fastbootd 通过 recovery/BCB 流程完成，过程中可能写入或清理启动控制消息。因此切换模式也不能被当作完全无持久状态变化的 RAM 启动方案。[Android 官方 fastbootd 说明](https://source.android.com/docs/core/architecture/bootloader/fastbootd)、[Recovery 切换逻辑](https://android.googlesource.com/platform/bootable/recovery/+/android-15.0.0_r1/recovery_main.cpp)。

这些结论针对标准 AOSP 代码，**没有认定该手机的 OEM recovery/fastbootd 二进制与 AOSP 完全相同**。OEM HAL 可以扩展命令，仍需独立证据；本轮没有发送任何 OEM 命令。

## LK 分发器与 continue：新的静态证据

为解决 raw 基址0的自动函数识别缺口，先把原始字节的 `0x6620` 之后片段映射回同一地址，显式建立工作线程入口；随后使用 `tools/ace-lk-analysis-elf.py` 创建只供分析的 ELF 容器。ELF 的 `.image` 段与原始 LK 组件逐字节相同；完整父 SHA、段偏移及容器 SHA 均保存。原始固件文件没有修改。容器采用由真实指针表推导的 linker VA `0xffff000050f00000`，并为已独立解码的函数入口提供 `analyst_` 标签；这些不是原始符号，也不是物理地址。容器不可用于刷写或启动。

REA 原生 VA 视图补齐以下路径：

1. 工作线程 `0x6620` 完整注册7个基础命令、download/flash组及15项静态表；末尾分配64MiB缓冲，调用分发器，返回后释放该缓冲。Evidence `ev_5560f935af32505fcb507c1e2080f974bbe45a02161185108accea24d2590f65`。
2. 分发器 `0x5f50` 遍历链表匹配前缀。只有匹配后才检查security/lock flag并调用handler，传入参数、下载基址和长度。链表未匹配才返回 `unknown command`，与 `No support by security control`、`No support by lock control` 为不同路径。这解释了真实boot错误，不能把它当作签名验证失败。Evidence `ev_0a066ca1cce0fc11f8af4c886d0d0d4537d7d7e1cabc2641dd6e0d9bc36b1ed6`。
3. `continue` handler `0x6ea8` 只发送OKAY、把Fastboot状态置为退出、通知 `boot_linux` event；不读取传入下载缓冲。等待该event的线程随后调用 `0xde78`，该函数首先调用 `load_vfy_boot(0/1)` 从boot/recovery存储路径加载，再走既有Linux启动。没有在这条路径发现下载RAM镜像跳转。Evidence `ev_f3655184b2a8425b0fc76747516d886acbbc0f66f18156a4e23580f93b6ddabc`、`ev_744b0eb60ebd50c5edfac1c31eefb8580fc70374e7bce84a2da8f27493dd0d62`、`ev_3b07f7bcf3c9d2b8e0ae647a2a5cb9d05840f192c8864668184d1751e2c3573e`、`ev_2f43b2b61987fa4730812a51872284f12b0a0145c35174812d82c90f4e702b7b`。
4. 整个组件的独立4字节对齐opcode扫描得到13个直接BL和1个尾B指向注册helper，与 REA 的14个直接incoming call site吻合，归属工作线程和download/flash注册函数。此扫描不是对所有字节可执行性的证明，也不涵盖间接调用或内联修改链表；不能扩大成“所有私有入口均不存在”。

原始与原生VA视图的snapshot、父子hash及有界搜索记录在忽略目录 `research/ace-entry-options-20261019/`。静态分析不等于已在手机执行continue，本轮没有发送该命令。REA会话已关闭。

## 尚不能排除的入口

- **尚未验证的LK私有处理路径**：上文已核对 `continue` 的具体存储启动路径；其他私有逻辑、间接注册或其他固件组件仍需独立证据，不能由当前直接调用覆盖推断全部不存在。
- **OEM recovery/fastbootd 扩展或其他固件入口**：标准代码不支持不能证明所有厂商扩展不存在；目前没有已验证可调用的自定义 RAM 启动协议。
- **自研内核上下文 handoff/soft-reboot loader**：已验证的诊断模块说明可以运行有限的内核代码，但完整切换还需处理 CPU/中断、设备与 DMA、缓存/MMU、内存覆盖、异常级和返回/复位条件。这属于新实现，不能把函数跳转或现有模块成功等同于标准 kexec 已可用。
- **EFI 等其他前置环境**：`CONFIG_EFI_STUB=y` 只表明该内核能供合适的 EFI 引导环境使用；没有证明 Ace 存在可访问的 EFI shell/LoadImage 路径，或 Android 运行时能借此启动新内核。[Linux EFI stub 文档](https://docs.kernel.org/admin-guide/efi-stub.html)。

现阶段可执行的下一步仍是：完成 LK 已注册路径的有界分析，找出具体且可观测的临时入口；若转向自研 handoff，先在匹配原厂内核的 QEMU 中验证完整状态切换，而不在手机上直接试跳。若最终只能通过写入某个启动分区来进入新代码，那已经是另一类操作，需要具体镜像、回退方案和该破坏性写入步骤的确认，不能当作本轮非刷写调查的隐含授权。

本调查不改变 `ios_deployable=false`，也不说明 MT6895 XNU、UFS、显示或输入驱动已经完成。
