# 一加 Ace：电脑端准备与接机验证

目标设备为 PGKM10／MT6895。本机已完成可以独立验证的工具、固件、用户空间、参考内核仿真和诊断代码准备。
真机的启动入口、最终内存布局及 MTK 外设驱动仍未验证，**目前没有可以直接部署到 Ace 的 iOS 启动镜像**。

## 2026-10-19 无线接机结果

重启后，已有配对通过 mDNS 自动连接。已验证无线 ADB 和 `su` UID 0，Android 正常启动、当前 B 槽、SELinux Enforcing；无需重新刷入 Magisk。

- 8 项只读采集全部成功：live DT、内存、中断、实际显示/触摸绑定、分区及启动控制信息。
- 实机内存 8 GiB，8 核在线，4×A55＋4×A78；显示输出 1080×2412，面板实际绑定 BOE NT37701A，触摸驱动 Synaptics S3910。
- 19 项分区备份全部通过设备读取前后 SHA-256、主机重新读取 SHA-256 和长度核对，共 578,781,184 字节。包括两槽 boot/vendor_boot/dtbo/vbmeta 系列及选定校准分区。备份不包含完整 userdata/super。
- 私有证据位于 `research/ace-live-20261019-wireless/`；有效备份位于 `research/ace-backup-20261019-wireless-v2/`。第一次尝试受远端 dd 统计输出污染，已保留为失败记录；工具已修复，不能使用第一次的 partial 文件。

当前 boot_b 是手机现有 Magisk 镜像，vendor_boot_b 与已保存原厂素材一致；A/B 启动镜像不同，恢复时必须按槽位匹配。
最初备份阶段没有上传或加载模块；后续寄存器模块验证见下文。整个阶段没有重启、切槽、修改属性或刷写手机启动/原始分区。

已取得精确 live kheaders 和原厂模块，重建正常 Kbuild/modpost/LTO 流程后，最小寄存器模块先在原厂内核 QEMU 中通过加载/卸载验证，再在真机成功运行。逐核限制到 CPU 0..7，8 核 MMFR0 均为 `0x101122`，TGran16=1，CNTFRQ=13MHz，确认 A55/A78 都提供 16KB 页能力。模块已卸载、手机临时文件已删除，Android 正常；尚未运行 16KB 页表或 XNU。

REA 又核对了与 live 固件一致的 LK 和 ATF，定位到条件选择 EL2h/EL1h 的交接路径，并据此修复诊断探针。新版 EL1/EL2 共 8 项实际 QEMU 测试通过。详细函数证据、实验边界及剩余工作见 [ACE-BOOT-ENTRY.zh-CN.md](ACE-BOOT-ENTRY.zh-CN.md)。

## 已完成的电脑端工作

| 内容 | 结果 |
| --- | --- |
| iPhone X iOS 16.7.16／20H392 | 完整 IPSW 校验、三个系统卷提取、16 GiB HFS+ 根镜像和 sparse 镜像已完成，详见 `IOS-LOCAL-PREP.zh-CN.md` |
| 工具链 | AArch64 GCC 13.3、Clang/LLVM/LLD 18.1.3、QEMU 8.2.2、GDB、DTC、Ninja、GitHub CLI、APFS/HFS+/sparse 工具均可用 |
| 原厂回退素材 | boot、vendor_boot 重新核对 SHA-256；解析 v4 头、ramdisk/DTB 和 AVB footer 边界通过 |
| 固件硬件配置 | `profiles/ace-mt6895.json` 与原厂 DTB 一致；报告明确区分固件配置与真机行为 |
| XNU 参考基线 | 已获取 CI 39158169212 的 0081 内核及构建树，按 GitHub artifact digest 与内核 SHA256SUMS 校验 |
| CPU 诊断探针 | 独立 PIC ARM64 探针编译通过，EL1/EL2 共 8 个 QEMU 执行用例通过；不访问未知 MMIO/存储，不是 Android boot 镜像 |
| 接机工具 | 只读信息采集器、白名单原始分区备份器、离线主机准备检查器及测试已完成 |

参考内核 SHA-256：

```text
d9cb893bd2baf841e94cd2001f0ec70c0fea42f045f87f14ae807e4ebc50e1e5
```

这是 **SWEET/QEMU 参考内核**，不是 MT6895 移植内核。原始 100 秒仿真运行到测试 PID 1、输出 10 次心跳后，触发中断耗时断言。
另一次增加内核已有的 `interrupt-masked-debug-mode=1`（TRACE）后，100 秒内观察到 PID 1 和 13 次心跳，最终快照无 panic。
该模式改变超时诊断响应，不能据此宣称原始配置稳定。运行的是小型 mockfs 测试 init，不是苹果 launchd 或完整 iOS。

原始失败证据与复测结果均保存在 `research/ci-0081/qemu-baseline/`。
QEMU 的 GDB 接口已改为只监听 `127.0.0.1`。本次两轮 XNU 基线未启用 GDB。

## 固件事实与待验证项

| 项目 | 原厂固件中的配置 | 真机仍需确认 |
| --- | --- | --- |
| CPU | 4×A55＋4×A78，affinity 0x000..0x700 | 实际裸机入口 EL、16K 页表执行；8 核 16K 能力位已实测 |
| GICv3 | GICD 0x0c000000，GICR 0x0c040000 | 非安全组配置和真实中断递送 |
| 定时器 | 13 MHz，虚拟 timer INTID 27 | CNTFRQ 和实际 IRQ 行为 |
| PSCI | SMC | 运行时版本、可用功能及 CPU_ON |
| 内存 | 基础 DTB 仅包含部分内存和动态 carve-out 请求 | live FDT、iomem、所有实际保留区，XNU 安全装载窗口 |
| UFS | HCI 0x112b0000，SPI 137／INTID 169 | LUN、分区、时钟/电源/复位、MTK 初始化路径 |
| 显示/触摸 | 板级源码含 command-mode 面板候选与 SPI 触摸配置 | 实际绑定器件、framebuffer、DSI/CMDQ/TE 刷新路径 |

基础 DTB 的 `/memory` 不能当作完整 RAM 地图；`reg` 报告保留父总线地址语义，不臆造缺失的地址转换。
原厂内核的嵌入配置已提取并校验：KEXEC、KEXEC_FILE、DEVMEM 均未启用。
这意味着不能直接依赖标准 kexec 或 `/dev/mem` 路径；Android 的 4K 内核配置不代表 CPU 不支持 16K。

已有 Fastboot 记录也没有建立标准临时 `fastboot boot` 在 Ace 上可用的证据。
原项目的 Qualcomm 内存、显示、UFS、USB 和重启寄存器不能直接用于这台手机。

## 本机检查与复现

在 `/home/xu/Desktop/IOS-Sweet` 执行：

```bash
python3 -m unittest discover -s tests -v
./probe/build.sh
python3 probe/verify.py
python3 tools/ace-prepare.py --output research/ace-offline/readiness-NEW.json
```

输出文件必须使用新名字。`ace-prepare.py` 不执行 ADB、Fastboot、挂载或任何手机操作。
它检查工具、原厂镜像和 AVB 边界、固件 profile、CPU 探针及参考内核；大型 iOS 根镜像引用此前验证的哈希，当前调用只检查几何和记录，不重新读取全部 28 GiB 数据。

```bash
python3 tools/ace-prepare.py --require-ios-deployable
```

当前预期返回 **2**：电脑端准备通过，但 Ace 的 iOS 部署条件未满足。普通准备检查则返回 0。
返回 1 表示本机素材、构建或工具缺失，应先修复。

CPU 探针验证包括 EL1/EL2 各自的采集、有效身份映射下的 MMU-on 拒绝、重定位运行和 BRK 异常记录，共 8 项。
这些是 QEMU 事实。探针没有刷机包装和硬件日志通道，不能把 `probe.Image` 直接当手机启动镜像。
每次重跑会先使旧成功记录失效，并绑定源码哈希；详情见 `probe/README.md`。

GitHub CLI 已安装，但本机尚未登录。现有参考产物通过已连接的 GitHub 工具取得；没有触发新 CI。
CLI 日志获取被登录状态阻止，连接器日志调用则出现 transport closed，完整 CI 编译日志未取得。
完整新 XNU 构建仍使用项目的 macOS Actions 流程；本机 Linux 工具提供探针、测试 init 和单文件检查能力。
`tools/xnu-cc.py` 可通过 `XNU_CLANG`／`XNU_CLANGXX` 指定编译器，`XNU_CC_JOBS` 默认最多 4，避免无界并行。
本次只验证了显式 Clang 能输出 ARM64 Mach-O C/C++ 对象，未将其表述为完整 XNU 本地编译通过。

## 手机接入后的顺序

### 1. 恢复稳定连接，只读采集

先正常启动 Android，连接并授权 ADB。本轮无线连接已验证；USB 过流问题未在本轮复测。
无需先重复刷 Magisk 或调整 adbd。工具可以使用已授权的 `su`，不要求普通 adbd 本身为 UID 0。

```bash
python3 tools/ace-collect.py --output research/ace-connected-NEW --dry-run
python3 tools/ace-collect.py --output research/ace-connected-NEW
```

工具要求唯一已授权设备，或显式 `--serial` 选择；不会将 transport serial 写入 manifest。
它只读取白名单身份信息、UID/root 能力、live FDT、iomem、interrupts、保留内存、显示/触摸绑定、block 布局和 32 字节 boot-control。
不可读项与超时会记录为缺失，不会自动重启、修改 USB 配置、SELinux、属性或槽位。
返回 2 表示存在未读取成功的项，需查看 manifest。

原始 FDT 可能含设备自身的 serial 属性，校准分区也含设备私有数据。
这些文件只保存在 Git 忽略的私有目录，不能提交或发布。

随后比较 live 配置：

```bash
python3 tools/ace-dt-audit.py research/ace-connected-NEW/live-fdt.dtb \
  --source-kind live-dtb --profile profiles/ace-mt6895.json \
  --output research/ace-connected-NEW/live-dt-audit.json
```

### 2. 按实际分区名读取备份

先查看计划，不访问手机：

```bash
python3 tools/ace-backup.py --plan
```

根据采集结果确认实际存在的名称后，再显式选择，例如：

```bash
python3 tools/ace-backup.py \
  --partitions boot_a,boot_b,vendor_boot_a,vendor_boot_b,dtbo_a,dtbo_b,vbmeta_a,vbmeta_b \
  --output research/ace-backup-NEW
```

校准分区从白名单中按实际存在的名称另行选择。
每分区上限 1 GiB，总量上限 4 GiB；不包含 userdata、super、LK 或 preloader。
备份前后设备 SHA-256、主机落盘文件 SHA-256 和长度全部匹配才标记 verified。
失败留下私有 partial 文件；活跃 Android 数据变化不会被误报为稳定备份。
工具没有自动恢复或写分区功能。原厂固件副本不等同于已取得该手机的两槽启动镜像及校准备份。

### 3. 建立自定义代码启动与日志路径

先补齐可恢复启动路径、实际装载地址、内存 carve-out 和诊断记录读取方法。
只有这些条件确定后，才能给 CPU 探针设计 Ace 的实际启动包装并验证，再推进独立 XNU 平台与驱动。
原厂 boot/vendor_boot 副本和回退步骤应根据当时真机身份、槽位及备份结果重新核对。

### 4. 分阶段完成 Ace 移植并部署

顺序为：CPU/16K/异常日志 → GIC/timer → XNU 平台/安全内存窗口 → 只读存储 → 根文件系统 → 显示输入。
接机并不代表已经能直接部署完整 iOS。任何后续具体分区写入仍按 `AGENTS.md` 逐项确认；保留 bootloader、recovery、modem、persist 和校准备份，不改变 GPT。

目前没有后台监听器、自动刷机或待执行的手机命令。

## 交接位置

- `research/ace-offline/`：主机检查、原厂 DT/内核配置报告、CPU 探针和验证记录。
- `research/ci-0081/` 与 `xnu/out-0081/`：已校验参考内核、构建树和 QEMU 结果。
- `research/ipsw-x/`：苹果固件、系统卷和已校验 iOS 根镜像。
- `NOTES.md`：最新状态、提交号、精确哈希、成功/失败记录和下一步。

设备产物、苹果下载文件和本地构建树均保持 Git 忽略。
