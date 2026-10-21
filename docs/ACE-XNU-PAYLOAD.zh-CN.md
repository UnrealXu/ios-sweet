# Ace 原生内核载荷打包

`tools/ace-mkpayload.py` 将链接后的普通 arm64 Mach-O 与 Ace ADT 打包为
`ACEXNU01/v1`，交给 `ace/xnu_handoff.c`。它不会生成 Android boot.img，
不会连接手机或写分区；输出清单明确标记 iOS 不可部署及平台来源尚待验证。

## 输入与校验

```sh
python3 tools/ace-mkpayload.py KERNEL ACE_ADT_DIRECTORY NEW_OUTPUT_DIRECTORY
```

设备树目录必须包含 `ace-mkadt.py` 生成的 `ace.adt` 和 `manifest.json`。
打包器核对 ADT 哈希、Ace 身份、物理内存范围及排除区间；既有输出目录
会被拒绝。命令行超过 607 个 ASCII 字节或含 NUL 会拒绝，不静默截断。

Mach-O 必须是薄的、小端、普通 arm64 `MH_EXECUTE`，声明无未定义符号。
程序有界检查命令、段、节、文件范围、重叠、溢出及权限。入口必须位于
可执行段中，且至少有四个实际文件字节。内核头、数据尾和 BSS 大小分别
保留，ADT 和 BootArgs 的最终位置须完全放得进管理 RAM。

当前支持保持链接时虚拟地址不变的加载方式。旧内核产物中的本地
`ARM64_RELOC_UNSIGNED` 表已经指向普通链接地址，零虚拟偏移时无需再加
物理地址差。打包器逐条检查这些记录及目标，保留指针、加载命令和
`__LINKEDIT` 原始字节。加载到不同物理地址不等于改变链接虚拟地址。

外部重定位、未定义符号、chained/dyld 编码、非空 threaded starts、
arm64e、IMG4、加密格式和 fileset 目前会拒绝，不能把尚未解析的编码
指针当作普通指针。后续实际 Ace 构建若使用不同格式，需要按该产物
补齐并验证解析器，不能直接关闭这些检查。

## 已验证与尚未验证

七项打包回归覆盖输入损坏、段及重定位越界、错误入口、ADT/清单不一致、
输出覆盖拒绝、优化 Python 下仍启用校验，以及真实 C 加载器的交接。

另外读取缓存成功构建 `39158169212` 的 **SWEET 对照内核**：检查其
77,056 条已链接本地指针，比较每个打包段的全部实际文件字节，并将
生成的载荷交给真正的 `ace_xnu_prepare`。规划成功，入口、ADT、BootArgs
及 `topOfKernelData` 与打包清单一致。没有修改指针、执行内核或向手机
拷贝数据。这个对照仅验证文件格式和加载计划，绝不能用于 Ace 刷机。

证据位于私有 `research/ace-payload-20261020/`，对照文件名明确包含
`SWEET-format-control-NOT-DEPLOYABLE`。手机没有本轮写入或重启。

## 实际 Ace 内核（2026-10-20）

个人 fork 的 [CI 39288876908](https://github.com/UnrealXu/ios-sweet/actions/runs/39288876908)
已成功，job `118183995118`，源码提交
`5ea487d7f403efb8739115550098bd568c7069b3`。kernel artifact `12205216685`
包含实际 `kernel.development.ace`，17,519,656 字节，SHA256：
`e3772e867b64b1777488b9e2cf3ca1d5a431a4c7f543b106354d8fe05d98652a`。
ZIP 哈希与连接器返回值、内核哈希与包内 `SHA256SUMS` 均已核对。

实际内核通过格式检查，10 个加载段、75,766 条已链接本地指针保持不变。
入口 `0xfffffe000749e488` 的实际指令跳到 `start_first_cpu`，后者保留 x0
并从其 BootArgs 读取虚拟基址、物理基址和内存长度；早期固定 Redmi
帧缓冲写入未出现在所检查的入口序列中。

对四个指令节共 9,082,624 字节比较默认与 Cortex-A55 解码：20 处分歧
均为嵌入数据，未识别出实际执行代码中的 STLUR/LDAPUR 或 PAC 指令。
仍存在四条 Apple watchdog 特有寄存器访问，其源代码由设备树
`awl-scratch-supported` 属性保护；静态扫描不能证明所有运行路径兼容。

该内核与实际手机 FDT 派生的候选 ADT 已生成 16,933,500 字节主机载荷，
SHA256 `31ff937e6e3d416dc001d15e151b23a0c9d9ecd9f447e9f9f5f90e78450bb405`。
实际 C `ace_xnu_materialize` 返回 0：全部 10 段文件字节相等，966,656
字节 BSS 从非零初值清零，52 个保留区通过规划排除，ADT、736 字节
BootArgs 和其页尾清零正确。它只写入主机匿名映射，没有执行 XNU 指令。

证据在私有 `research/ace-linked-20261020/`。这些结果不证明 5–8GiB
窗口可由原生启动独占，也不证明手机运行成功。原生加载器的运行时归属、
CPU 状态检查、最早日志和 16K 页表仍待真机验证；当前 QEMU 加载器使用
模拟固定地址，不能部署到手机。仍无可刷写的 Ace iOS 镜像或已运行的
MTK 存储、显示、触摸驱动。
