# Ace CPU 诊断探针（电脑端准备）

这是单 CPU、裸机 AArch64 寄存器探针，**不是 iOS 启动层、XNU、Android boot.img 或已验证的一加 Ace 启动镜像**。ARM64 Linux Image 头只方便 QEMU 装载。本目录不提供刷机、fastboot 或手机执行脚本。

```sh
./probe/build.sh
python3 probe/verify.py
```

依赖现有 `aarch64-linux-gnu-{gcc,ld,objcopy,nm,readelf,objdump}`、Python 3；执行验证另需 `qemu-system-aarch64` 和 `gdb-multiarch`。不自动安装、下载或调用 sudo。构建结果固定放在已忽略的 `research/ace-offline/probe/`，支持 `CROSS_COMPILE` 前缀。结果包含 `probe.Image`、带符号 ELF、反汇编、重定位列表、各用例的 QEMU/GDB 日志与 record 二进制、`verification.json`。

探针只改写镜像内的 record 和自有 4 KiB 栈；不访问 MMIO，不操作 UFS、GIC、显示、UART，不执行 SMC、HVC、PSCI 或复位，不访问任何存储。代码/数据使用 PC 相对地址，构建器拒绝绝对地址重定位和未定义符号。默认代码不包含 QEMU 专用设备地址。

入口首先保存 x0 和 CurrentEL；接受 EL1 和 EL2，EL3 直接记录 stage 2 并 WFE 停留，不设置 SPSel/VBAR，也不访问 EL1/EL2 控制状态。EL1 读取 SCTLR_EL1，EL2 读取 SCTLR_EL2；对应 M=1 时记录 stage 3 并停留，不更改 MMU/缓存/页表。仅在当前 EL 的 MMU off 时屏蔽 DAIF、设置 SPSel=1、自有栈和当前 EL 的 VBAR：EL1 使用 SP_EL1/VBAR_EL1，EL2 使用 SP_EL2/VBAR_EL2。C 采样函数按 CurrentEL 读取 TCR_EL1 或 TCR_EL2；MPIDR_EL1、ID_AA64MMFR0_EL1、CNTFRQ_EL0 在这两个 EL 均使用架构允许的公共读法。独立的 EL1/EL2 异常入口不依赖栈，分别保存当前 EL 的 ESR/FAR/ELR，记录 stage 6 后停留。探针从不关闭 MMU/缓存，不更改 SCTLR、TCR 或 TTBR，不切换异常级。

边界条件：需要引导器将整个镜像装入普通、可执行、可写 RAM，入口为 EL1/EL2/EL3，且仅一个 CPU 进入。MMU on 拒绝路径也要求镜像自己的数据仍有可写映射；对任意损坏页表、EL0、受上层虚拟化限制的特权寄存器访问、恶意入口或多核同时进入，不承诺可以留下记录。安装本地 VBAR 之前发生的异常仍由原环境处理。异常记录只覆盖当前 EL 的 VBAR 安装以后的路径。WFE 可被更高异常级配置截获；探针不尝试改变更高 EL 控制状态。没有硬件日志通道，手机上如何取得 RAM record 仍须先确定可用的调试/保留内存机制；不可据此直接打包部署。

## Record v2

记录符号是 `diagnostic_record`，共 120 字节，全部小端。v2 保留 v1 的字节布局，但控制/异常寄存器的银行由 CurrentEL 决定；解码器必须检查版本，不能把 EL2 记录当作 EL1 寄存器。地址为实际加载基址 + `nm probe.elf` 给出的符号偏移，不能把 QEMU 地址用作 Ace 地址。

| 字节偏移 | 字段 |
|---:|---|
| 0 | 8 字节 ASCII `ACEPROBE` |
| 8 | version = 2 |
| 16 | stage：1 入口，2 拒绝不支持的 EL（EL3），3 拒绝 MMU on，4 采集中，5 完成，6 异常 |
| 24 | 原始 entry x0；只记录数值，不解引用 DTB |
| 32 | CurrentEL 原值（EL1 = 4，EL2 = 8） |
| 40 | SCTLR_EL1 或 SCTLR_EL2，由 CurrentEL 指定；EL3 未读取 |
| 48 | MPIDR_EL1 |
| 56 | ID_AA64MMFR0_EL1 |
| 64 | CNTFRQ_EL0 |
| 72 | TCR_EL1 或 TCR_EL2，由 CurrentEL 指定 |
| 80 | MMFR0.TGran16 原始 4 位值 |
| 88 / 96 / 104 | 当前 EL 的 ESR / FAR / ELR（EL1 或 EL2），正常时 0 |
| 112 | supports_16k：已识别的 TGran16=1/2 为 1，其他值 0；保留原始字段供判断 |

被拒绝时未采集的字段保持 0，不能解读为硬件寄存器读数。首次运行依赖镜像的初始零数据；不提供返回入口或重复进入协议。record 未执行缓存清理；需要由调试机制考虑缓存一致性，不能假定设备重启后仍可读取。

## 已执行的离线验证

QEMU 8.2.2 / Cortex-A76 / virt / 128 MiB / 单 CPU，GDB 仅监听 `127.0.0.1`。测试通过 GDB 硬件断点停在 `probe_halt`，读取真实执行结果；每例具有 20 秒 GDB 超时并在退出时清理 QEMU。GDB 本地临时端口绑定存在短暂选端口竞态，端口被抢占会导致用例失败；不会暴露监听到外网。

- 实际 EL1、MMU off：stage 5；x0 = `0x44000000`；SCTLR = `0x30c50838`；MPIDR = `0x80000000`；MMFR0 = `0x101122`；CNTFRQ = 62,500,000 Hz；TCR = 0；TGran16 = 1。
- 开启 QEMU virtualization 的实际 EL2 入口：stage 5，CurrentEL = 8；SCTLR_EL2=0，TCR_EL2=0，采样 MPIDR=0x80000000、MMFR0=0x101122、CNTFRQ=62,500,000、TGran16=1。不再将这个架构允许的入口直接拒绝。
- EL1 和 EL2 各自在原始入口停止后，将同一完整镜像复制到 `0x40200000` 再执行：stage 5，保留原 x0，证明两种入口在第二个地址执行成功。
- EL1 和 EL2 各自用 GDB 在 `probe_main` 入口注入 BRK（仅测试进程内，不改构建产物）：stage 6；对应 ESR_EL1/ESR_EL2 = `0xf2000000`，ELR 为实际 `probe_main` 地址。成功与异常路径还检查实时 SP 为自有 stack_top，PSTATE.M 为 EL1h=5 或 EL2h=9，验证 SPSel=1 选中了当前 EL 的栈。
- EL1 MMU on 的真实拒绝：先在原入口断点停止，GDB 写入有效 L1 页表，再从独立测试 trampoline 执行 MSR/TLBI/DSB/ISB 启用身份映射后跳回未修改的 `probe.Image`。结果 stage 3、record 和停留时实时 SCTLR 均为 `0x30c50839`（M 仍为 1）；`probe_main` 处额外硬件断点未命中，采样字段仍为 0。页表执行前后逐字节一致。
- EL2 MMU on 的真实拒绝：独立 EL2 trampoline 配置有效身份页表，执行真实 MSR/TLBI/DSB/ISB 开启 EL2 MMU 后跳回探针。结果 stage 3，record 与实时 SCTLR_EL2 都为1；TCR_EL2=`0x80823019`、TTBR0_EL2=`0x41000000`、MAIR_EL2=`0x44`；C 采样入口断点未命中，采样字段为0，页表执行前后逐字节一致。
- ARM64 Image 头与镜像长度检查通过；没有 ABS64/绝对或动态重定位，没有 undefined symbol。裸机 ELF 的 RWX LOAD 段警告是本探针布局的结果，不代表启用了页表或 W^X 保护。

**16K 能力、计时器频率和寄存器值只证明本次 QEMU 模型的行为，不是 MT6895/Ace 的测量。** EL1 和 EL2 的成功、重定位、异常与 MMU on 拒绝共8例全部实测通过。MMU on 拒绝路径已分别用有效身份映射验证；EL3/EL0、真实 Ace 加载和 RAM 记录提取尚未实测。实际 Android 启动包装、装载位置/保留区、硬件入口状态和日志方式必须依据该手机证据另行设计。

## MMU on 测试边界与页表

`qemu-mmu-on.S` 和 `qemu-el2-mmu-on.S` **只由验证脚本构建，默认 `build.sh` 不编译、不链接它**，其固定地址仅用于 QEMU virt，不可作为手机代码。QEMU 8.2.2 的 GDB 接口虽然显示系统寄存器，但尝试写入 MAIR/TCR/TTBR/SCTLR 后读回仍为原值，因此改用这个独立 trampoline 执行真实架构指令；没有把未生效的 GDB 赋值作为 MMU 测试结果。

QEMU RAM 为 `0x40000000..0x47ffffff`（128 MiB）；probe 装入 `0x40080000`，测试 trampoline 位于 `0x41200000`，页表位于 `0x41000000`，三者互不重叠。页表为 4 KiB、512 项，只有 L1 index 1 为 `0x40000701`，其余清零：一个 1 GiB identity block，对应 VA=PA `0x40000000..0x7fffffff`，Valid=1、block 类型、AF=1、SH=Inner Shareable、EL1 读写、AttrIdx=0、可执行。映射涵盖全 RAM；测试只访问实际 RAM，未访问映射中 RAM 外的地址。

`TCR_EL1=0x200803019`：T0SZ=25（39-bit VA，从 L1 开始）、TG0=4 KiB、SH0=Inner、IRGN0/ORGN0=Non-cacheable、EPD1=1、IPS=40-bit。`MAIR_EL1=0x44` 为 AttrIdx 0 Normal Non-cacheable；`TTBR0_EL1=0x41000000`。trampoline 保留入口 x0、保留 SCTLR 其他位，只置 M=1；在控制寄存器更新前后执行 DSB/ISB 和 TLBI，真实执行 MMU on 下的取指和 record 写入。最终实时寄存器、页表描述符和范围均进入 `verification.json`，原始页表/执行后副本保存在输出目录。这证明探针对这个**有效且可写的身份映射**会拒绝运行，不代表支持任意已有页表。

## TGran16 编码依据

核对了 Linux 上游 v6.12 的 [arch/arm64/tools/sysreg](https://github.com/torvalds/linux/blob/v6.12/arch/arm64/tools/sysreg#L1552-L1556)：ID_AA64MMFR0_EL1[23:20] 的 0 表示 NI，1 表示 IMP，2 表示 52_BIT。因此本探针把已定义的 1/2 识别为支持 16 KiB，同时保留原始字段；2 额外表示 52-bit 地址支持，不能把它误判为不支持 16 KiB。其他编码保守保留为未识别，`supports_16k=0` 不代表对未来保留值做完整解码。


## EL2 修复依据和测试细节

本项目对 Ace 原厂 boot handler 的静态分析发现：读取 ID_AA64PFR0_EL1 的 EL2 字段，存在 EL2 时为 kernel 入口设置 SPSR=0x3c9（EL2h），否则设0x3c5（EL1h）。这个分支证据说明原来的“只接受 EL1”探针不覆盖合法入口；它不是对当前手机实际入口或可执行探针的验证。v2 因此支持 EL2，同时仍拒绝 EL3 和 MMU on。RAM、映射与单核前提仍须由装载环境保证，探针不检测这些前提。没有为了接受 EL2 执行 ERET、关闭 MMU 或发起 SMC/HVC。

EL2 测试专用 TCR_EL2=`0x80823019`：RES1 位31/23、PS=2（40位）、SH0=3、TG0=4 KiB、T0SZ=25，cache walk 为 Non-cacheable。RES1/PS 编码与已取得 Linux5.10 `arch/arm64/include/asm/kvm_arm.h` 一致。页表沿用 L1 index1 的 `0x40000701`，现在用于 EL2 stage-1；其余条目为0。`qemu-el2-mmu-on.S` 使用 MAIR_EL2、TTBR0_EL2、TCR_EL2、SCTLR_EL2 以及 `tlbi ALLE2`；它只在 QEMU 验证进程中装入，绝不链接进默认探针。

EL1/EL2 测试各自保存 `<case>-identity-l1.bin` 与 `<case>-identity-l1-after.bin`；verification.json 的 `control_register_bank` 指明银行，`record_version=2`，输入 SHA256 包含两个测试 trampoline。旧 v1 产物已单独保存在 ignored `research/ace-offline/probe-v1-before-el2/`，旧报告的“EL2 rejected”不再代表 v2。EL3 拒绝逻辑保留，但EL3/EL0、真实手机加载和 RAM record 获取均未实测。
