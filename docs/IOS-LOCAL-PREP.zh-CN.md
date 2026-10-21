# 本机 iOS 镜像准备

本项目使用 iPhone X（iPhone10,3／D22AP）的 iOS 16.7.16（20H392）用户空间。
苹果 IPSW 提供系统文件；移植后的 XNU、启动层和设备驱动由项目另外构建。
原项目支持红米 Note 10 Pro（sweet／SM7150）。本机连接过的一加 Ace
PGKM10／MT6895 尚无可启动的对应移植内核，不能直接使用 sweet 启动镜像。

以下操作仅创建电脑上的文件。手机 userdata 写入另需逐项确认。

## 固件来源与校验

苹果 CDN：

<https://updates.cdn-apple.com/2025FallFCS/fullrestores/122-77006/1158E502-D76D-4226-AA06-ED5E30CD1111/iPhone10,3,iPhone10,6_16.7.16_20H392_Restore.ipsw>

文件长度为 6,171,035,648 字节。IPSW.me 固件索引提供的 SHA-256：

```text
ece1194f7e233e9109c5790a8d23a4564a10a254e15ec5b09978a343265568fb
```

该哈希用于完整性比对；它不是独立验证的苹果签名。
下载后还要读取包内 BuildManifest.plist，确认版本、构建号和设备类型，
并通过 ZIP CRC 校验提取出的每个组件。

## 本地文件

目录：`research/ipsw-x/`（已被 Git 忽略）。

| 文件 | 用途 |
| --- | --- |
| `*.ipsw` | 完整苹果恢复固件；`.part` 只代表下载中 |
| `firmware-api.json`、`URL.txt` | 来源、长度及固件索引中的校验信息 |
| `IPSW-SHA256SUMS` | 完整下载校验成功后生成 |
| `extracted/BuildManifest.plist` | 苹果固件组件清单 |
| `extracted/087-86698-044.dmg` | OS 根文件系统 |
| `extracted/087-86593-047.dmg` | SystemOS cryptex，包含 dyld 共享缓存 |
| `extracted/087-86715-047.dmg` | AppOS cryptex |
| `d22ap.adt` | 解包、解压后的苹果设备树 |
| `extraction-report.json`、`EXTRACTED-SHA256SUMS` | 提取结果、组件 CRC 和本地 SHA-256 |
| `ios16-root.img` | 按项目脚本生成的 HFS+ 根镜像 |
| `ios16-root.simg` | Android sparse 格式根镜像 |

是否已完成制作，以 `NOTES.md` 最新记录和实际文件为准，文件存在本身不代表已通过校验。

## 依赖

系统已有 Python、Make、CMake、ARM64 GCC、mkbootimg、rsync 和 hfsprogs。
另外安装 `libfuse3-dev libbz2-dev zlib1g-dev libattr1-dev android-sdk-libsparse-utils`。

APFS 读取工具来源为 <https://github.com/sgan81/apfs-fuse>，本次使用提交
`66b86bd525e8cb90f9012543be89b1f092b75cf3`；LZFSE 子模块提交为
`e634ca58b4821d9f3d560cdc6df5dec02ffc93fd`。
本地源码和构建日志在 `research/` 下，工具副本在 `research/ios-toolchain/bin/`。

## 制作步骤

在项目根目录执行。完整固件和三个 DMG 就绪后：

```bash
export PATH="$PWD/research/ios-toolchain/bin:$PATH"
python3 tools/adt.py unwrap \
  research/ipsw-x/extracted/Firmware/all_flash/DeviceTree.d22ap.im4p \
  research/ipsw-x/d22ap.adt

sudo env PATH="$PATH" bash tools/mkiosroot.sh \
  research/ipsw-x/extracted/087-86698-044.dmg \
  research/ipsw-x/extracted/087-86593-047.dmg \
  research/ipsw-x/extracted/087-86715-047.dmg \
  research/ipsw-x/ios16-root.img 16G

sudo fsck.hfsplus -fy research/ipsw-x/ios16-root.img
```

随后挂载这个镜像文件，应用项目配置并卸载：

```bash
(
  set -e
  mnt=$(mktemp -d)
  cleanup() {
    if mountpoint -q "$mnt"; then sudo umount "$mnt" || return; fi
    rmdir "$mnt"
  }
  trap cleanup EXIT
  sudo mount -t hfsplus -o loop,force research/ipsw-x/ios16-root.img "$mnt"
  sudo python3 tools/sweet-root-tweaks.py "$mnt"
)
sudo fsck.hfsplus -fn research/ipsw-x/ios16-root.img
```

核对 `/sbin/launchd`、`/usr/lib/dyld`、SpringBoard、共享缓存、文件属主和关键符号链接。
所有挂载必须在制作结束后释放。最后执行：

```bash
img2simg research/ipsw-x/ios16-root.img research/ipsw-x/ios16-root.simg
sha256sum research/ipsw-x/ios16-root.{img,simg}
```

`sweet-root-tweaks.py` 使用原项目的实验配置。完成根镜像说明用户空间准备就绪，
不代表一加 Ace 的启动、显示、触摸、UFS 或其他驱动已实现。
本步骤不包含 `fastboot flash` 或任何手机分区写入。

## 2026-10-19 本机制作结果

- 完整 IPSW：长度、SHA-256、SHA-1 均与固件索引匹配。
- 15 个提取组件：ZIP CRC 校验通过，并保存逐文件 SHA-256。
- 原始根镜像：17,179,869,184 字节（16 GiB），应用 SWEET 实验配置。
- Sparse 根镜像：12,145,303,892 字节，格式 1.0，4096 字节块。
- 49 项文件检查通过：系统版本、核心程序的 root 属主及可执行权限、共享缓存硬链接等。
- 配置修改后 `fsck.hfsplus -fn` 报告 `The volume iOSRoot appears to be OK.`。
- Sparse 镜像还原为 16 GiB 后，与原始镜像逐字节比较一致；临时还原文件已删除。

本地证据位于 `research/ipsw-x/`：`root-build.log`、
`root-content-verification.json`、`image-format-verification.json`、
`ROOT-SHA256SUMS`。这些大文件和提取资料不进入 Git。
未进行手机刷写或启动测试；一加 Ace 的专用 XNU／启动层／驱动仍待实现。
