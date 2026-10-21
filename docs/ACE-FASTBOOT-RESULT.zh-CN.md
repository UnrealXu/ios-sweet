# Ace 临时启动命令实测（2026-10-19）

**当前安装的 Bootloader 不接受标准 `fastboot boot` 命令。** 这阻断了原计划的临时
RAM镜像启动路径；不能据此改用未验证镜像刷写分区。

## 实际执行

用户接入USB后，手机从DISCONNECTED/online0变为CONFIGURED/online1，USB ADB已
授权。先核对PGKM10/MT6895、B槽、启动完成、root/Enforcing，实际 boot_b 和
vendor_boot_b 哈希仍与已验证备份一致，再正常重启到Bootloader。

只读getvar结果：product=`k6895v1_64`、current-slot=`b`、unlocked=`yes`、
is-userspace=`no`、max-download-size=`0x4000000`（64MiB）。

用当前正在使用的B槽boot完整备份测试RAM下载与临时启动：

- boot_b镜像67,108,864字节，SHA256
  `ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10`。
- `Sending 'boot.img' (65536 KB) OKAY [1.381s]`。
- `Booting FAILED (remote: 'unknown command')`，host返回1。
- 随后 `fastboot reboot` 成功；Android正常启动回B槽，boot ID改变、root与
  SELinux Enforcing仍正常，无线调试脚本再次自动达到tls-ready。
- 恢复后实际boot_b/vendor_boot_b SHA256与测试前相同。没有执行flash、erase、
  set_active或任何OEM命令，没有执行自定义入口或iOS。

该测试确认当前固件的标准boot命令未实现；下载成功本身不是镜像执行成功，更不证明
LK已接受自定义诊断payload。它不排除尚未查明的其他启动入口。

完整原始命令结果与hash绑定恢复记录位于忽略的
`research/ace-fastboot-baseline-20261019/verification.json`。

## REA静态交叉核对及限制

使用已与真机B槽前缀匹配的LK首组件，SHA256
`9e3f9fd53316fe7d64a5ed70eea5374489f9aed3e33b20511437f21e269e8511`，
raw ARM64分析基址0。恢复原handoff snapshot，继续核对：

- 注册helper `0x5b58`创建0x28字节链表记录，含命令名、长度、flags及handler。
  Evidence `ev_fbbac844bc9ff1454a40c95d30ab562543808a740390a9620ab81d7be23d0873`。
- `0x8558`注册download:/flash:/erase:及ultraflash系列；此函数无标准boot注册。
  Evidence `ev_ff5a9d8772a1638f6577b6bd26eb3d55464a4efa03b2276525ec52cc64746df4`。
- 存在`unknown command`字符串，Evidence
  `ev_191aecc76fd341827e28bbc6410180d5bc50e22523a754d0d8a228a6017ac606`。

`0x6754`是注册代码的内部块，不是Ghidra识别的函数入口，直接分析请求被拒绝。
此次Ghidra对unknown-command字符串没有给出xref；这只限定当前分析覆盖，不能作为
全二进制不存在引用的证明。完整注册/dispatch与OEM替代入口仍未解决。当前boot命令
不受支持的决定性证据是上面的真机响应，不是有限静态搜索的阴性结果。

REA会话已关闭，新snapshot保存在同一私有目录。

## 后续边界

先研究当前LK真正可用的自定义代码入口及恢复方案。现有协议代码和CPU/日志诊断
不组成可启动的iOS镜像。若后续方案必须写boot等分区，按项目AGENTS要求，应先完成
具体镜像、验证与恢复准备，再针对该破坏性步骤单独确认；本次没有此类写入。
