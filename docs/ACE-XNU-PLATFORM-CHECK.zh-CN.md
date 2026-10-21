# Ace 启动前的 FDT 与 ADT 一致性检查

`ace/xnu_platform.c/.h` 核对实时 FDT 的初始平台描述与传入 Ace ADT。
`ace_xnu_prepare_platform` / `ace_xnu_materialize_platform` 将它接到已有
CPU 检查和有界加载器：配置拒绝时不修改计划或目标内存。这些调用已接入
[原生 EL1 Image](ACE-XNU-NATIVE-ENTRY.zh-CN.md)，尚未在手机执行。
当前没有 XNU/iOS 真机启动结果。

## 初始平台契约

FDT 必须描述八个不同的完整 CPU affinity（0、0x100…0x700），前四个
为 Cortex-A55，后四个为 Cortex-A78，均使用 PSCI。每核的 phandle 必须
唯一且别名一致。CPU0 的固件声明时钟须存在，并与 ADT 一致；它不能当作
当前 DVFS 测量。实际启动核及 CPU 状态仍须单独由特权采样确认。

GIC 必须是唯一启用的根级 GICv3，分配器为 `0x0c000000+0x40000`、
redistributor 为 `0x0c040000+0x200000`，具有四单元中断格式和明确的
interrupt-controller 属性。实际手机带两个 PPI 分区；检查它们的 CPU
引用和四核分组，未知子节点拒绝。不能按“GIC 必须无子节点”这一猜测
拒绝真实 FDT。

四个架构定时器描述必须与当前 FDT 的完整四单元编码一致，时基为
13MHz，虚拟定时器 INTID 为 27，提供者必须解析到上述唯一 GIC。当前
只接受第四单元为零的这组定时器描述；不能把非零 PPI 分区引用当成填充
忽略。[Linux GIC 绑定变更](https://cos.googlesource.com/third_party/kernel/+/f61a657fdf221403d99e6f0d4c6d24762920d4a9%5E2..f61a657fdf221403d99e6f0d4c6d24762920d4a9/)
说明该单元的分区引用含义。PSCI 必须声明 1.0 与 SMC 方法；这与
[Linux PSCI 绑定](https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/arm/psci.yaml)
交叉核对。检查不发出 PSCI 调用，也不测量定时器或读取 GIC 寄存器。

## ADT 比较与加载接口

根据这些已检查的 FDT 值和请求 RAM，在固定 3072 字节工作缓冲中构造
当前 `ace-mkadt.py` 的规范九节点表示。输入 ADT 必须逐字节一致，包括
节点数、属性、标志、phandle、GIC ranges、CPU0、pmsg 元数据、RAM 和
全部边界；唯独 64 字节 random-seed 的内容保持不透明。它不验证种子
熵，也不是支持任意 ADT 变体的通用解析器。主机生成器改变格式时必须
同时审查这份原生契约，不能静默放宽比较。

输入 RAM 仍须经过实时 FDT 内存策略检查，CPU 仍须为新鲜 EL1 采样。
新接口拒绝上下文/输入与计划或目标映射的别名，随后才进入同一个精确
段复制器。所有缓冲和策略必须保持稳定；声明一致不能证明固件或 DMA
已释放 RAM、其他 CPU 静止、缓存一致性或 pmsg 的实际跨重启可靠性。

## 已取得的证据（2026-10-20）

- 真实 FDT 与实际 2652 字节 Ace 候选 ADT 通过同一 C 检查。初版因错误
  假定 GIC 无子节点而拒绝；核对真实 PPI 分区后加入明确检查。测试路径
  也由错误的 CPU 节点名改为正确夹具路径，判断核心始终使用 reg。
- 9 项新增回归覆盖 CPU/GIC/timer/PSCI 错误、重复提供者、PPI 分区、
  ADT 改动/额外属性/截断、上下文别名，以及拒绝前整个目标映射和计划
  不变。ASan+UBSan 检查 2000 次 FDT/ADT 变异及截断，输入未改变。
- 最终完整 193 项主机回归通过，42.540 秒。
- Cortex-A55 freestanding 部分链接无运行库导入。单帧 stack-usage：规范
  ADT 比较 3248 字节，
  平台检查 352 字节，prepare 1872 字节，materialize 1888 字节；尚非
  整个手机启动调用链的最大栈占用证明。
- 手机 CPU0 / shell UID2000 执行普通静态进程退出 0：配置比较返回 0，
  ADT 截断与损坏均返回 -45，Android 阶段仍拒绝内存加载策略。程序没有
  执行特权采样、materializer 或 XNU，也没有操作控制器。执行前后 boot ID
  相同，临时文件已清理，Android 已启动，SELinux Enforcing。
- 实际内核载荷在主机串联 FDT 内存策略、CPU 状态夹具、平台检查和真实
  materializer 成功：10 段、966656 字节 BSS、ADT、BootArgs、53 个排除区
  均已核对；目标为主机映射，没有跳转内核。

原生目标文件审查另发现两个本地字符串指针数组生成了 15 条绝对数据
重定位。它们适用于已验证的固定地址 Android ELF；未经处理不能用于
重定位的原生 Image。已改为直接字符串引用，目标链和新增回归检查均无
ABS64/ABS32/ABS16 或绝对 MOVW 重定位。它不等于整幅原生 Image 已通过
运行时重定位测试；该测试仍须随入口整合执行。

修正后的手机程序已重新执行成功，23840 字节，SHA256：
`c7f813f6511d69c2f970e2a2670202a473251a1e47e4264caf1164455fc8d830`。
真实 FDT、ADT、程序和源码哈希、完整 stdout、清理及主机验证保存在
私有 `research/ace-platform-20261020/`。下一步为原生入口整合与最早
XNU 启动日志；存储、显示和触摸运行验证仍未完成。
