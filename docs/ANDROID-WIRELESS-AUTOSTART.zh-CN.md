# Android 重启后恢复无线调试

按用户要求，在现有 Magisk 的 late_start 阶段安装一个开机脚本：

`/data/adb/service.d/90-ace-wireless-debugging.sh`

项目源码为 `tools/android-wireless-adb-autostart.sh`。它等待 Android 完成启动、wlan0 连接获得地址，然后通过 Android settings 恢复 `adb_wifi_enabled=1`，等待系统给出 TLS 调试端口。沿用已有配对和 Android 的 Wi-Fi 授权机制，不清除密钥、不修改认证或 SELinux、不重启 adbd，也不启用 legacy TCP 模式。

每次启动只进行一次有界恢复，成功就退出；手动关闭后不会在同一次启动中持续强制开启。开机等待最多240秒，网络/TLS重试最多90轮，每轮2秒，settings 调用各限10秒。框架和网络暂未可用时可能超过纯睡眠时间；脚本不会阻塞 Magisk/Android 的 late_start 启动阶段。

手机状态记录在 `/data/adb/ace-wireless-debugging/status.txt`，权限由 umask077限制。它保存当前 boot ID、最后一次验证的 setting/port，不记录配对码、ADB 私钥、SSID 或设备序列号。

前提是 Magisk仍启用、Wi-Fi能够连接、电脑保留原配对并可发现 mDNS。新网络可能仍需 Android 的信任确认。恢复无线调试不等于手机运行 iOS；这是后续真机验证的连接准备。

## 当前验证结果

已实际安装并手动运行成功。第一次重启自动出现网络信任框；用户随后勾选“始终允许通过此网络进行调试”并允许。

保存网络授权后，再次执行正常 Android 重启：boot ID 确实改变；开机脚本状态中的 boot ID 与当前启动一致，`state=tls-ready`、`wireless_setting=1`，脚本记录端口与系统当前有效 TLS 端口一致。现有配对电脑成功重新连接，Android 启动完成、B槽、root、SELinux Enforcing、`ro.adb.secure=1` 以及安装脚本 SHA256 均核对通过。此次验证未要求用户解锁、开关无线调试或再次点击允许。

**当前 Wi-Fi 和现有配对电脑的重启自动恢复验证通过。** 证据为忽略目录中的 `trusted-reboot-verification.json` 及哈希绑定的原始快照。换到未信任的网络或删除配对后，Android 仍可能要求新的授权；脚本保留这一系统机制。

## 停用与移除

在已授权 root shell 中执行以下任一种：

```sh
# 保留脚本，停止后续恢复；脚本尚在等待时也会在下一轮退出。
touch /data/adb/ace-wireless-debugging/disable

# 或只删除本项目安装的开机脚本。
rm /data/adb/service.d/90-ace-wireless-debugging.sh
```

重新允许开机恢复时移除该 disable 文件。上述操作不会删除无线调试配对；如需关闭当前无线调试，可直接使用手机设置。

实现依据：[Magisk 官方 Boot Scripts](https://topjohnwu.github.io/Magisk/guides.html#boot-scripts)。实际安装与重启验证记录保存在忽略的 `research/ace-wireless-autostart-20261019/`。
