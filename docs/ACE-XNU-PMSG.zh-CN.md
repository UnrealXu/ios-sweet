# Ace XNU pmsg 日志与 Cortex-A55 编译目标

本阶段实现并验证源码，尚未在手机执行新的 XNU 内核。真机验证的是
普通用户进程中的一条指令；不能把它算作 XNU 或 iOS 启动成功。

## 修复实际指令集不兼容

本地 clang18 对 Darwin 目标即使设置 `-march=armv8.2-a+crypto`，仍保留
`apple-m1` 默认 CPU。新日志核心的反汇编出现了 `STLUR`。该指令涉及
较新的 LRCPC2 扩展；不能仅凭“arm64 编译成功”认为它适合 Ace A55。
相关背景见 [Arm 的 RCPC 说明](https://developer.arm.com/community/arm-community-blogs/b/tools-software-ides-blog/posts/enabling-rcpc-in-gcc-and-llvm)
及 [Clang 的目标设置说明](https://clang.llvm.org/docs/CrossCompilation.html)。

真实 PGKM10 的只读 Linux 能力列表含 `atomics`、`lrcpc`，不含 `ilrcpc`。
随后使用 `diagnostics/ace-isa-probe/probe.S` 构建静态 Linux ELF，在配对
ADB shell 中以 `taskset 1` 固定 CPU0 执行。程序先验证 CPU 编号，再安装
SIGILL 处理器；只有内核正信号码与准确测试指令地址匹配才报告不支持。
测试指令只以自身 BSS 为目的地址。结果为准确 PC 的 SIGILL，退出3。

临时程序已移除，Android/Enforcing/启动 ID 与执行前一致；当前 ADB
shell UID2000 已复核。没有 reboot、模块、SMC、控制器 MMIO 或原始分区
写入。原 boot_b 诊断安装状态没有在本阶段改变。

0084 将 ACE 的编译 CPU 明确指定为 `-mcpu=cortex-a55`。修正后重新编译
22 个平台源文件，未发现此前那类 `STLUR`，新核心无需运行库原子函数。
这证明已检查目标文件的情况，不代表已审计最终链接的全部闭源库。
此前使用隐含 M1 CPU 的本地 ACE 对象不作为可部署产物。

## 0084 pmsg 串口后端

在 XNU 正常 `KPRINTF` 初始化调用 `serial_init` 时按需注册，只支持
输出。它仍不能记录 XNU 首条指令、MMU 开启及最终页表切换之前的故障。

需同时满足启动参数 `ace_pmsg=1` 和 ADT `/chosen/ace-pmsg` 节点：

| 属性 | 精确值 |
| --- | --- |
| compatible | `ace,ramoops-pmsg-v1`，含终止 NUL |
| reg | 小端两个 u64：`0x48160000`、`0x10000` |
| ecc-size | 小端 u32：0 |
| type-signature | 小端 u32：0 |

还检查 BootArgs Revision2/Version2、非空无溢出的 XNU 管理内存窗口与
pmsg 不重叠、EL1 和小端访问。源码通过 `ml_io_map_wcomb` 请求映射这段
16K 对齐的64KiB资源，不建立任意32MiB映射；尚未真机执行此映射。

日志核心要求已有 DBGC 签名和规范环形缓冲区状态，绑定时不改变旧日志，
不清零或初始化未知内存。输出逐字节保留最新内容；常规 RAM 上的非阻塞
锁在递归/争用时丢弃输出，串口 ready 始终返回可继续，避免等待日志锁。
每次写入重验头部，错误时不改记录。数据/元数据存储有顺序屏障，平台
成功写入后执行 `dsb sy`；不承诺中途复位的事务完整性或新 XNU 的复位
保留行为。前提仍是映射可访问、保留区由当前启动独占，无外部并发写者。

## 验证范围

- 实际缓存 XNU 参数重放10次相关编译，另有22个显式 A55 平台目标文件。
  原 SWEET 的两个相关目标文件与基线逐字节一致。
- A55 配置的真实 `genassym.c` 生成136个常量，全部匹配缓存汇编偏移；
  SWEET 对照也匹配。尚无完整 ACE 构建/链接或新 CI run。
- 回归测试执行补丁里的同一日志核心与前端控制逻辑，覆盖19种策略拒绝、
  映射/头部失败、旧记录保留、完整回卷、递归丢弃、400组头部变体。
  前端主机适配器替代了 ARM 寄存器、映射和屏障，只能证明控制逻辑。
- ASan/UBSan 加保护页执行同一核心，检查三次完整回卷及1024组状态。
  构建配置回归检查实际 `-target-cpu cortex-a55` 与无 STLUR/原子运行库导入。
- Linux raw signal ABI 的静态断言使用缓存的实际 Android UAPI 声明；
  初始 include 路径不完整，成功编译检查完成于上述真机运行之后。
  真机处理器中的精确故障地址匹配也成功，未重跑指令探针。

私有证据为 `research/ace-xnu-pmsg-20261019/verification.json`、
`isa-phone/` 原始结果和前后状态、显式 A55 目标文件、反汇编、测试日志。
GitHub 登录/仓库写入权限与原 boot_b 恢复确认仍是两个待处理事项。
接下来仍需完成 Ace ADT、启动内存归属、最早期日志与完整内核构建，
然后提交具体镜像和回滚方案进行新一轮真机启动验证。
