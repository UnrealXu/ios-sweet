# Ace 初始 XNU 设备树与时钟交接

`tools/ace-mkadt.py` 根据有界 FDT 生成单 CPU Ace ADT。它只在电脑上生成
元数据，不连接手机、不写物理内存，也不生成可刷写的 iOS 镜像。

## 已实现的交接约束

输入必须明确给出管理 RAM 的基址和长度、传入 FDT 的物理地址、加载器
及栈/源镜像的排除区间、启动 CPU affinity，以及 `--cold-native` 阶段。
工具拒绝缺失、溢出、未按 32MiB 对齐或不在声明 RAM 内的区间，并排除
FDT、initrd、固定保留区和有界动态分配域。未知无界动态保留区会拒绝。

仅两个名称、大小、对齐和属性均匹配的 SSMR/SSHEAP Linux CMA 池可以
在显式的 Linux 启动前方案中保持未实例化。依据是固定提交的 OnePlus
[保留内存分配代码](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/drivers/of/of_reserved_mem.c)
与 [CMA 初始化代码](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/kernel/dma/contiguous.c)。
公开源码不能证明当前 ROM 或安全固件的全部运行状态；这条规则不能用于
覆盖正在运行的 Android 内存，最终加载器仍须验证实际硬件内存归属。

ADT 描述 PGKM10/MT6895、唯一 CPU0、13MHz 时基、GICv3、PPI27 和已确认
的 pmsg 保留区。未确认的总线、内存和外设时钟被省略，不复制 Android
序列号、启动参数或其他机型身份。CPU 的 1701MHz 来自固件声明，不能
当作实时 DVFS 测量。

`0085-ace-clock-without-invented-bus.patch` 修复 XNU 在缺失总线频率时的
除零路径：ACE 检查设备树时基和 `CNTFRQ_EL0` 都是 13MHz，未知总线的
派生比率保持 0/1。提供有效总线频率时原比率计算仍保留；其他平台流程
不变。没有凭空填写一个总线时钟来绕过问题。

## 验证结果（2026-10-20）

实际手机 FDT 的 SHA256 为
`68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b`。
由它生成的主机候选 ADT 为 2652 字节，规划 5–8GiB 的物理窗口并排除
52 个区间。只读 Android `/proc/iomem` 表明该窗口属于一个 System RAM
区间；这不能证明它空闲或已经由 XNU 独占。候选清单明确记录
`hardware_ram_ownership_verified=false` 和 `ios_deployable=false`。

与原生加载器衔接的主机打包工具及其验证边界见
[ACE-XNU-PAYLOAD.zh-CN.md](ACE-XNU-PAYLOAD.zh-CN.md)。

验证使用实际缓存 XNU 的 `SecureDT` 解析器、时钟结构与补丁后的识别
函数，在主机上仅适配内核分配、panic 和寄存器读取。实际生成的 ADT
能被这些消费者读取，返回正确的 GIC、pmsg、13MHz 时基及未知总线值。
错误或缺失时基会被拒绝。

同一 ADT 通过实际 `ace/xnu_handoff.c` 的规划检查，64 位地址及 BootArgs
在 1GiB 和 3GiB 窗口下保持一致。测试内核只是四字节 NOP 数据，未跳转、
未拷贝到手机，因此不构成 XNU 启动验证。三个真实 arm64 Mach-O 时钟
编译案例成功；最终完整主机测试 163 项通过，69.249 秒。

私有证据保存在 `research/ace-adt-20261019/`，包括候选、源哈希、实际
消费者与加载器规划结果、编译目标、测试日志和 `verification.json`。

## 完整构建与下一步

最新结果：补丁 0086 修复 BearSSL 参数门控后，个人 fork 的第三轮
[CI 39288876908](https://github.com/UnrealXu/ios-sweet/actions/runs/39288876908)
已成功链接实际 Ace 内核；产物哈希、最终指令扫描与加载器主机写入验证
见 [ACE-XNU-PAYLOAD.zh-CN.md](ACE-XNU-PAYLOAD.zh-CN.md)。下文为最初提交
时的排队记录，不能再将它当作当前阻塞。原生内存归属与真机启动仍未解决。

已在用户账号下建立 `UnrealXu/ios-sweet` fork。Ace 最小构建分支
`codex/ace-initial-platform` 的提交为
`03be91534408e3fe39687841d602b6a79176925b`，仅包含补丁 0082–0085 和三个
依赖准备脚本，没有上传手机原始数据、Apple 下载物或本地交接记录。
已手动提交 `MACHINE_CONFIG=ACE` 的完整
[CI run 39283161766](https://github.com/UnrealXu/ios-sweet/actions/runs/39283161766)。
提交时状态为排队，不能据此声称已链接成功。

截至本轮结束仍在排队。GitHub [官方 runner 公告](https://github.com/actions/runner-images/issues/13518)
列出的 macOS 14 暂停时段涵盖本次提交时间（北京时间 10 月 19 日
22:00 至 20 日 08:00），可能影响启动或导致基础设施失败。该工作流为
旧 XNU 的 IORPC 生成接口选择 Xcode 15；迁移新 runner 时须解决实际
工具链兼容性，不能仅增加结构字段强行编译。

接下来需检查完整构建和最终指令集，补齐原生加载器的实时归属检查及
最早启动日志，然后准备可审查的真机临时启动方案。MTK UFS、显示、
触摸驱动和 iOS 用户空间均未完成；当前没有新的 iOS 镜像可刷。
