# Ace 移植进度：启动桥接与驱动协议（2026-10-19）

**当前没有启动成功的 Ace iOS 镜像。** 本轮实现了独立启动桥接、诊断包装和存储/触摸协议代码，补足真实硬件参数；完整 XNU 平台与 MTK 外设驱动尚未完成。没有将未验证镜像刷入手机，也没有覆盖 userdata。

## 本轮代码与执行结果

| 组件 | 已实现并验证 | 尚缺 |
| --- | --- | --- |
| `ace/entry/` | 单核 EL2→EL1 ERET、EL1 直达、位置无关跳转；默认4项加可选RAM日志双矩阵28项真实 QEMU 测试通过；默认Image字节保持不变 | Mach-O/XNU 加载、ADT/BootArgs、MTK GIC/PSCI/SMP、硬件可观测入口 |
| `tools/ace-probe-boot.py` | 确定性 gzip、hash/源码/8 用例证据绑定、可选未签名 v4 诊断候选；7 项测试，AOSP 独立解包及实际提取 payload 的 EL1/EL2 仿真通过 | LK/ATF/AVB 实际接受、裸机日志取回；它打包的是寄存器探针，不是 iOS |
| `ace/ufs_protocol.c` | READ10/16、INQUIRY/容量/LUN、UPIU/UTRD/PRDT 与响应解析；拒绝写指令；15 项测试、ASAN/UBSAN 12,000 组有界输入、ARM64 freestanding 编译通过 | 时钟/电源/PHY/SMC、DMA 映射与队列提交、UIC/错误恢复、XNU BSD 磁盘后端 |
| `ace/tcm_protocol.py` | TCM 帧/continuation 校验和 LSB bitfield；11 项测试及与官方 C helper 10,000 组差分通过 | SPI 控制器、固件启动、实际动态 report descriptor、EINT/IRQ 与 XNU HID |
| `diagnostics/ace-pmsg-header/` | 原厂内核 QEMU 与真机正常加载/卸载，读取真实 DBGC/start/size 头，保持 pmsg 目标只读；签名、容量、ECC0核对通过 | 裸机 writer、cache/ownership交接与reset后保留 |
| `ace/pstore_ring.c` | caller-owned RAM 的 DBGC/12B 环形缓冲读写；10 项测试、UBSan、1,600 轮完整字节差分、ARM64 freestanding 无未定义符号 | 真实物理 RAM 头、ownership/cache/reset 保留验证及启动桥接集成 |
| 显示 | 官方源码与原厂模块核对，取得实际 DRM 模式/格式/行跨度 | DSI/DSC/CMDQ/TE、电源时钟、IOMMU/DMA 与 XNU framebuffer/刷新 |

完整单元测试111项通过；默认桥接及两组日志矩阵共32项不同 QEMU 用例通过，281个产物哈希复算稳定。诊断 boot 候选 1,667,072 字节，SHA256 `0fe98860a5e3a63ce70cf797e65d3b9f0fbefff4664e0b479d5e28e45a1369fb`；它明确标记 **UNTESTED、unsigned、ios_deployable=false、hardware_test_recommended=false**。旧 boot legacy signature 区全零；替换内核后不保留或声称原 RSA AVB 有效。原 ramdisk 和除 kernel_size 外头字段保持不变。

## REA 与真实二进制

原厂 vendor_boot 与已备份 B 槽逐字节一致；重新 LZ4 解码的 ramdisk CPIO 与原解码结果逐字节相同。只提取相关 `.ko` 到忽略的私有目录，未加载这些 OEM 驱动副本，也未操作其硬件。

- UFS：`ufs-mediatek-mod.ko` SHA256 `f064758906893c1e112fde167f5ee3c0b627e62ae6e4b064c0912bf27c7a9a03`。REA 核对 HCE reset 顺序、setup_clocks、DME link startup、SMC `0xc2000276` device reset。它需要 MTK 专用电源/时钟/安全固件协作；不是更换 Qualcomm 控制器基址即可。
- 触摸：`oplus_bsp_tp_tcm_S3910.ko` SHA256 `8afe864c48e9a02c0a28f0c9069eb9a6517feb63b112c3a57f09ac59520e93b2`。REA 核对填 `0xff` 的 SPI read、A5/LE16 长度、continuation 及末字节 padding，以及 LSB-first 标量字段抽取。源码和实际模块都需要动态 report 配置；不能把固定坐标偏移当作驱动。
- 显示：`mediatek-drm.ko` SHA256 `5ae1377b473bb753bed0c6825612c29cde0650a4448d899ebaef7b4e60d67ca3`。对 `mtk_fb_get_dma` 的精确 36 字节函数切片做 REA，并保留父 ELF 的文件偏移和双重 hash。函数从私有 fb+200 取 GEM，再 GEM+360 取 DMA。此切片仅证明该 getter 的静态字段访问，不能证明对象 lifetime 或 DMA→物理地址映射。

REA Evidence：UFS HCE `ev_3a8f675c1c4b01b7493ebccc6f79a87c1d3c1ffc8ed65b1e5ed10438cbb52a2a`；clock `ev_bb0a39ccf031e7bf2f8e384792e8d4dcbdbc4de3d8f525478315b8190ec218ca`；reset `ev_b18726c20592cbc7617b65e018e937f229dbecbe61d5bbe3bbf31d0e7c48b909`；touch bitfield `ev_328045fecc6c358f5325d1eb8a7e41667a1cd38d7840cc89e5f1486ceb60561f`；touch read `ev_f2daa6a3799807001dcc2948d910b47badcfe1a1db81e06b55189eb9cc5fc626`；DRM getter `ev_8f8584e3eec00ac816a111ae554c75f2fe09cf6eced3e9109ad9df49c473c783`。完整快照保存在 `research/ace-driver-port-20261019/vendor-modules/`，所有 REA 会话已关闭。

## 真机补充事实

### UFS 与 userdata

Android OEM 驱动的 sysfs 路径明确给出 SCSI 地址 `0:0:0:0/1/2`，分别对应 sda/sdb/sdc。sda、sdb 各 4MiB；sdc 包含 userdata，逻辑块均为 4096 字节。读取 sdc 开头 64KiB 后，GPT 头与 128 项表 CRC 全部通过：userdata 为 LUN2 第80分区，4096-byte LBA `3514368..62476279`，241,507,991,552 字节，与 Linux 512-sector 单位的 sysfs start/size 完全一致。

这些结果不证明裸机 DMA 已可用；协议编码器不硬编码 LUN0、LUN2 或 userdata 起点。后续首次裸机读取须先取得实际 handoff 的 HCE/HCS/UTRL 状态和独立 DMA ownership，避免抢占 Android 活跃存储队列。

### 显示与触摸

临时挂载 debugfs，只读 DRM state/framebuffer 后已卸载。实际 crtc0 为 1080×2412@120Hz，主 plane 为 XB24 little-endian、linear modifier0、pitch **4352** 字节；不是 width×4=4320。其他 overlay 存在 MTK modifier，不能按线性 buffer 解释。对象字段 null 不代表没有 GEM：原厂驱动用私有 GEM 字段。当前 DMA/PA 尚未取得。

BOE NT37701A 是 4-lane command-mode DSI，活动 DSC 配置为 10bpc、10bpp、540×12 slice、675-byte chunk；参考源码及实际 panel `.ko` 数据均支持此配置。Linux 桌面 scanout 不等于 LK 留下的 framebuffer，不能直接继承旧 DT 的 PA 当作当前缓冲。

S3910 是 SPI mode0/8-bit、最高5MHz，TCM MTK chunk2048。实际 report descriptor 仍需取得；未向已由 Android 驱动绑定的 SPI 设备并发发命令。

## 持久日志取回验证

本机实际 backend 为 ramoops：mem_address=`0x48090000`、mem_size=`0xe0000`、record_size=`0x1000`、console_size=`0x40000`、ftrace_size=`0x1000`、pmsg_size=`0x10000`、ecc=0、mem_type=0。它不是仅由 reserved-memory 节点推测的配置。

已先保存原 console/pmsg 文件，再通过 Android 正常 `/dev/pmsg0` 写入唯一短标记并正常重启。重启后 boot ID 改变、Android B 槽正常完成启动、root 可用；读取新的 pmsg-ramoops-0（522字节）确实包含该标记。完整证据位于 `research/ace-driver-port-20261019/pstore-retention/status.json`。没有清空 pstore、调用 log_store 的 eMMC/PMIC 接口或刷写原始分区。

依 ramoops 实际参数和官方 pstore/ram 源码，pmsg 区预计为 `0x48160000..0x4816ffff`，12字节 DBGC/start/size 头及 `0xfff4` 字节环形数据。随后在自动恢复无线连接后的真机上读取 `/proc/iomem`，实际注册了153个连续、不重叠的 ramoops resource，完整覆盖 `0x48090000..0x4816ffff`；其中 `ramoops:pmsg` 确实为 `0x48160000..0x4816ffff`。因此该物理范围已有运行内核 resource 记录佐证。随后新增受限诊断模块，用与原厂相同 WC 类型建立临时 alias，只读12字节头后立即 unmap；真机得到签名 `0x43474244`、start=size=288、ECC0容量65524。普通加载/卸载均成功、boot ID与taint不变、模块和暂存文件均清理。原始头部已实际核对，不再仅靠推导。该模块保留 tracing/CFI，普通 printk可进入console日志，但不改 pmsg 目标。详见 [头部诊断](../diagnostics/ace-pmsg-header/README.md)。正常 Android reboot 的保留证据不能替代裸机 RAM 写入、任意 watchdog/PSCI reset 路径或 LK 处理后的结果；后续必须逐步验证，不能因此直接启动无日志镜像。

## 联网资料与边界

按固定 commit 获取官方来源并保存 URL、SHA256 与获取失败记录：

- [OnePlus MT6895 kernel](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/tree/8baa5a377e2776402de745579cc3835d08ee1cca) 的 UFS、时钟、电源、显示/PHY/IOMMU 和面板代码。
- [OnePlus MT6895 vendor modules](https://github.com/OnePlusOSS/android_vendor_mediatek_kernel_modules_mt6895/tree/0c04020c19a68356afd49ce24f2ff95ee56c37e0) 的 S3910 与 touch common 接口。
- [Linux ARM64 booting](https://www.kernel.org/doc/html/latest/arch/arm64/booting.html) 与 [Linux v5.10 head.S](https://github.com/torvalds/linux/blob/v5.10/arch/arm64/kernel/head.S) 的入口约定。

这些公开源 commit **不是已证明的运行内核 g6973d81cd2ac 完整源码**；实际模块的 REA 和 Android runtime evidence 用来限定哪些行为已交叉核对。纯协议测试、QEMU、静态反编译和真机执行证据分别记录，不相互替代。

## 下一阶段

当前 Bootloader 的真实 `fastboot boot` 测试返回 `unknown command`：现有B槽镜像下载成功，但临时启动命令不受支持。已普通重启回Android，boot/vendor_boot哈希不变；见 [Fastboot实测](ACE-FASTBOOT-RESULT.zh-CN.md)。REA已进一步核对 `continue`：它通知存储Linux启动线程，而非跳转到下载RAM；原厂标准kexec关闭，标准AOSP fastbootd也无boot/continue后端。详见 [入口边界](ACE-ENTRY-OPTIONS.zh-CN.md)。必须先确定实际可用的自定义代码入口，不能继续假定可用临时RAM启动，也不因此自动改用分区刷写。随后建立可取回的裸机日志和安全 RAM/DMA 区，验证 EL2→EL1 真机入口及 GIC/timer，再完成 XNU loader/ADT/BootArgs 与 MTK 控制器驱动。在得到实际 LUN2 只读容量/GPT结果及显示/触摸执行证据前，不把诊断包装文件命名为可用的 iOS 镜像。每一项破坏性分区写入仍需具体镜像、验证和恢复方案，并按项目要求单独确认。

## 可选日志与审阅封装

`ace/entry/build.sh --pmsg-ram ADDRESS BYTES` 显式启用普通RAM实验日志，默认关闭。程序只在接受的MMU/cache状态下向已有规范DBGC环追加阶段文本，未知头、非规范cursor或镜像重叠则拒绝；无SMC、reset、存储或MMIO操作。QEMU包含数值匹配真机pmsg范围的矩阵，但不能替代裸机ownership/cache/reset取回验证。

新增 [证据绑定封装器](ACE-ENTRY-WRAPPER.zh-CN.md) 独立核对全部源码、原probe记录、entry原始记录、环形数据和页表不变性，默认仅gzip，显式参数可生成未签名v4审阅文件及实验日志版本。所有结果仍为 `ios_deployable=false`、`hardware_test_recommended=false`，未刷写手机；这是带日志诊断基础，不是iOS。

## XNU 加载与参数交接基础（2026-10-19）

新增 [Ace 加载组件](../ace/xnu-loader/README.md) 可在显式 RAM 范围内验证并复制已重定位的段、清零 BSS、放置 ADT 与 XNU8796 BootArgs。拒绝旧 SWEETXNU 目标标记、越界、溢出、源/保留区/目标重叠及落在 BSS 或空洞中的入口；没有 Ace 物理地址默认值，视频字段保持关闭。

5 项实际 QEMU 用例通过：EL1、EL2→EL1、重定位进入合成接收程序，错误入口与段重叠在目标写入前拒绝；每项比较完整256KiB目标 RAM。10 项新增主机测试包括5000组 ASan/UBSan 畸形载荷及与实际缓存 XNU 头的全部 BootArgs 字段偏移核对；全项目127项通过。

这是可复用的加载/交接代码，**没有执行真正的 XNU 或 iOS**。仍缺已验证的 Ace 裸机入口、RAM ownership、Ace ADT 与 XNU 平台实现、16KiB 映射及 MTK 控制器驱动。本轮没有连接或改动手机，没有生成可刷入的 iOS 镜像。
