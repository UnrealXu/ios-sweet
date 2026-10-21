# Ace pmsg 原始头部只读诊断

本组件已在同一原厂内核的 QEMU 和真实 Ace 上正常加载、卸载。它只观察
`0x48160000` 的 pmsg 签名、start 和 size，不是裸机启动代码或 iOS 驱动。

## 已得到的实际结果

真机候选148,184字节，SHA256：

```
c15323b76d08c75921ee31601cf85de9788402e707e8517ad698c83fffeea5b4
```

- 真机原始头：sig=`43474244`（DBGC）、start=288、size=288，ECC0容量65524。
  两次读取一致，第一次尝试完成；双读一致不等于 writer lock 或原子快照。
- 普通 insmod/rmmod 均返回0。前后 boot ID、kernel taint 不变，Android 启动
  完成、root及SELinux Enforcing仍正常。模块无残留，暂存文件已删除。
- 原 pstore 文件已先保存，不 unlink、不清空；当前 pmsg payload 未读取或改写。
  printk及正常 MMIO tracing 可以写普通内核日志/trace buffer，printk也可进入
  ramoops console。因此只读承诺针对 **pmsg 目标区**，不声称内核完全零 RAM 写入。
- 原厂内核 QEMU14.967秒正常退出：普通加载/卸载各两次，初始头start=size=0；
  PID1通过正常 pmsg字符设备写入27字节后，再读得到start=size=27；签名、容量
  均符合预期，无panic/CFI failure。QEMU内的普通写入只是测试夹具，真机未写pmsg。

证据在忽略的 `research/ace-pmsg-header-20261019/`：
`module-live/build-result.json`、`qemu-live-candidate/result.json`、
`live-run1/result-verified.json`。最初 live 验收解析未处理 Android dmesg 在 tag
与冒号之间插入的 ANSI 颜色控制码；原失败结果和完整原日志保留。修复后离线复核
同一次采样通过，没有为修复解析重复加载模块。新增4项解析回归测试。

## 映射与 ABI 边界

执行前必须核对真实设备/内核/boot状态、`/proc/iomem` 精确 pmsg resource、
ramoops 参数 mem_type=0、ecc=0。`ioremap_wc(...,12)` 会按页建立临时4KiB映射，
其范围全部位于实际64KiB pmsg区；源码只读取偏移0/4/8，无初始化、zap或payload访问。
读取后立即 iounmap，仅撤销自己的alias，不申请/释放原驱动resource。

原厂 ramoops使用同一WC类型；保留`readl_relaxed`的MMIO tracing和原有严格CFI、LTO、
SCS、PAC/BTI等配置。不提供force-load、trace关闭、cacheable alias或映射失败后
直接读物理地址的退路。如果内核拒绝映射，模块返回失败。

9项import CRC全部直接解码自固定SHA的实际OEM `mediatek-drm.ko` __versions；
并与其他原厂模块交叉核对。EXPORT_SYMBOL与4项GPL导出class来自同一固定公开
OnePlus源码；namespace/class应用到exact OEM仍属于部分重建metadata，正常
QEMU/真机加载提供这个候选的运行佐证，不声称取得完整原版Module.symvers。
原 prepared tree 的 Module.symvers 在构建后恢复。

imports的固定来源、CRC记录偏移及公开声明：
`imports/imports-manifest.json` SHA256
`9d67d90f91dcbe1eb711270e3be4e41b258c9950a1aa93be8481c73e4be84e05`。

REA审查首个候选的初始化函数，Evidence
`ev_6b8a4e5b4bcefd640fad18caf71d566beec48b186651b27bf64662c78062ad2e`。
其源码读取逻辑及最终候选的.text/.init.text/.exit.text/__versions/__jump_table
逐字节一致；差异是调试路径、说明字符串等。此静态佐证不替代上述真实运行记录。
REA会话已关闭并保存snapshot。

## 重放

```sh
# 只检查固定私有输入，不构建或访问设备。
python3 diagnostics/ace-pmsg-header/rebuild.py --check-only

# 选择新的私有输出目录；不覆盖已验证候选。
python3 diagnostics/ace-pmsg-header/rebuild.py --output research/ace-pmsg-header-20261019/module-new
python3 diagnostics/ace-pmsg-header/qemu.py research/ace-pmsg-header-20261019/module-new/ace_pmsg_header.ko --output research/ace-pmsg-header-20261019/qemu-new
```

`live.py`默认只读preflight，需要module与绑定相同hash/当前源码的QEMU结果；显式
`--load-readonly-module`才执行普通加载/卸载。原始证据只能保存到忽略目录。多个
ADB transport时须明确选择目标；脚本不修改配对、SELinux、分区或启动属性。
`--verify-existing`仅离线复核既有采样，不执行设备命令。设备检查拒绝Python `-O`。

这个结果补齐了真实pmsg头部/映射验证，仍未验证裸机writer、cache/ownership交接、
LK在所有reset原因下的保留行为、PSCI/watchdog或自定义镜像执行。

参考：[原厂 ram_core.c](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/fs/pstore/ram_core.c)、
[原厂 ARM64 ioremap.c](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/arch/arm64/mm/ioremap.c)、
[Linux ramoops文档](https://www.kernel.org/doc/html/latest/admin-guide/ramoops.html)。
