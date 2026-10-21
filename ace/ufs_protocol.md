# UFS 只读协议层

`ufs_protocol.c/.h` 是原创 MIT 许可的纯内存编码/检查代码，提供经典 UFSHCI 2.x/3.x UTRD、COMMAND UPIU、最多 16 个 PRDT 项，READ(10/16)、TUR、INQUIRY、READ CAPACITY(10/16)、REPORT LUNS 和有界响应解析。它不提交请求，不访问 MMIO、系统寄存器或设备，不生成 WRITE、UNMAP、FORMAT、cache-flush 或 crypto 命令。

代码没有接入现有 Qualcomm shim 或 XNU 路径。**这不是已完成的 MT6895 UFS 驱动。**

调用方必须建立真正的设备 DMA 地址映射、连续缓冲区、描述符生命周期、缓存一致性和屏障，并先证明 host/link/clock/power 状态可用。传入的 DMA 地址不是自动等同于 CPU 物理地址。单次数据上限 4 MiB，PRDT 每项最多 256 KiB；UCD 地址需 128 字节对齐，数据地址/长度需 4 字节对齐。库检查地址溢出、32/64-bit 地址能力和数据/UCD 重叠，但无法证明这些地址实际上可供控制器访问。输出对象由调用者独立分配；这只是 wire layout，C 类型本身不保证物理地址对齐。

支持普通 LUN0–7，另外仅允许 REPORT LUNS 发往其标准 WLUN `0x81`。READ CAPACITY(10) 返回最大值时要求改用 READ CAPACITY(16)；不会把 `0xffffffff` 当作准确容量。REPORT LUNS 解析器只接受简单普通 LUN0–7，拒绝重复、分级或未知地址，不能将 Linux 磁盘字母猜成 LUN。当前真机证据已经独立确认 Ace 的 `sdc` 为 SCSI LUN2，userdata 在 `sdc80`；该值没有硬编码进协议层。

返回响应时校验 OCS、transaction、tag、LUN、response code、EHS、残差/溢出/下溢及 sense 长度。CHECK CONDITION 返回有界的借用 sense 视图；调用者必须保留底层响应缓冲区。代码不执行重试、错误恢复、复位或功能协商；也未实现 Query/NOP、UIC/link startup、interrupt、PM、IOMMU、crypto、HPB 或 MCQ。

验证命令：

```sh
python3 -m unittest discover -s tests -p test_ace_ufs_protocol.py -v
```

15 项测试实际编译并调用 C 代码，覆盖手工固定的标准 wire 向量、PRDT 分段、容量/LUN 识别、截断响应、sense 越界、整数和 DMA 边界、伪造写命令拒绝；另用 ASAN/UBSAN 对 12,000 组有界响应/识别数据运行，并用 AArch64 freestanding / general-registers-only 编译确认没有未定义符号。

协议字段依据公开 UFSHCI/UPIU/SCSI 格式；交叉核对 [OnePlusOSS `ufs.h`](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/drivers/scsi/ufs/ufs.h) 与 [`ufshci.h`](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/drivers/scsi/ufs/ufshci.h)。这些参考文件受 GPL-2.0 许可；本实现没有复制 Linux 驱动函数体，原始源码与 SHA/URL 证据保留在忽略的 research 目录。
