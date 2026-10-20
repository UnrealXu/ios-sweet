# XNU 构建加速

后续内核迭代默认选择 `build_mode=cached`；要完全绕过缓存核验，选择
`build_mode=full`。两条路径都重新应用当前补丁、生成头文件、运行 make 并链接
内核，保留 Ace 入口校验、精确产物哈希和真机试验前的检查。

快速路径复用两类内容：

- KDK 和依赖 Git 源码。每次恢复源码后，清除旧补丁和未跟踪的暂存提供者，
  再应用当前仓库补丁。缓存键包括 macOS 版本、固定构建脚本提交、Xcode/SDK
  标识及缓存实现版本。
- XNU Makefile 原生支持的 `CCACHE`。缓存键另区分架构、目标机型和配置；
  编译器缓存按源码、头文件、编译参数和编译器内容检查是否可以复用。
  不启用忽略时间宏、头文件或依赖变化的宽松选项。
  保留原始源码路径，不设置路径归一化，避免改变内核的 `__FILE__` 诊断字符串。

不缓存 `fakeroot`、生成的 XNU 头文件、make 的旧对象目录或已链接内核，
避免旧的“内核已构建”标记跳过本轮修改。这是编译器缓存加速，尚未引入直接
恢复旧 make 构建树的增量方案。

入口校验通过后立即上传 `xnu-kernel`，包含内核、SHA256、构建来源和
`build-metrics.json`。完整日志仍每轮保存。`diagnostic_artifacts=true` 可额外
上传本地编译树和 KDK 符号清单；`full` 模式也会保存这些资料。

第一次使用新缓存键仍需冷构建。实际收益必须比较相同源码、相同工具链的
完整构建、冷缓存及热缓存，记录 Build 时间、缓存命中率、内核哈希和上传时间；
不能仅凭缓存命中提示承诺固定分钟数。源码/编译缓存恢复或保存也有开销，
测量时要分别列出，不能从总耗时中隐去。

实现参考：[GitHub 缓存键与作用域](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)、
[ccache 的输入与编译器检查](https://ccache.dev/manual/4.10.html)。
