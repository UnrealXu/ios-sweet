# Ace entry 诊断镜像的电脑端封装

`tools/ace-entry-boot.py` 只在电脑上验证、压缩和封装文件，不访问手机。
载荷为 **ACEENTRY → ACEPROBE**，不是 XNU，也不能启动 iOS。

先完成当前源码对应的原 probe 八项测试、entry 默认测试及 pmsg 普通 RAM
实验测试；以各验证脚本的最终报告为准。开始重新构建会使旧 PASS 失效。
封装器会核对完整 entry 源码集合、原 probe 源码和 Image、每项实际记录及
日志哈希，并独立检查默认 entry 的 EL1 结果和 MMU 拒绝时的页表不变性。
缺失、过期、重复或失败用例均拒绝；`pass: true` 本身不能替代产物验证。

默认只生成确定性 gzip 和 manifest：

```sh
python3 tools/ace-entry-boot.py \
  --output-dir research/ace-entry-wrapper-20261019/default
```

只有显式参数才另生成 `UNTESTED-unsigned-entry-boot.img`，供后续审核：

```sh
python3 tools/ace-entry-boot.py \
  --output-dir research/ace-entry-wrapper-20261019/unsigned-review \
  --emit-unsigned-boot
```

输出目录必须是新的、被 Git 忽略的 `research/` 子目录。文件权限为 0600，
目录为 0700。原厂 boot/vendor_boot 的 SHA256 固定；候选仅改变 boot v4
头部的 `kernel_size` 并替换 kernel，保留原 ramdisk，检查 gzip 解包结果。
不复制旧 AVB 元数据或 footer，不声称原厂 vbmeta 能认证修改后的 kernel。

默认封装 **未启用 pmsg** 的 entry Image。只有显式 `--experimental-ace-pmsg`
才选择第二组矩阵已验证的 enabled Image，固定地址 `0x48160000`、长度
`65536`；仍强制默认四项、两组各十四项和原 probe 八项全部通过。
可同时加 `--emit-unsigned-boot`，在新的输出目录生成带日志的审阅候选。
这是 QEMU 普通 RAM 实验：地址值与手机预留区相同不能证明物理内存
所有权、跨重启持久化、缓存一致性或手机日志取回能力。

所有 manifest 都明确记录 `ios_deployable=false`、
`hardware_execution_verified=false`、`hardware_test_recommended=false`。
候选未验证 Ace 加载、启动认证、物理内存所有权及故障恢复，不是可部署的
iOS 镜像。LK 的标准临时启动命令已实测不支持；本文不提供设备执行步骤。

测试仅使用合成电脑端格式／证据 fixture：

```sh
python3 -m unittest discover -s tests -p test_ace_entry_boot.py -v
```
