---
name: avatar-verification
description: 对讯飞虚拟人项目执行交付前验证，覆盖配置、构建、运行、首帧、音视频、交互和常见修复。快速模式只返回简短验证结论，不生成过程报告；严格模式生成完整验证报告。
---

# avatar-verification: 交付前验证

## 输入与模式

先读 `../avatar-shared/delivery-modes.md`，接收上游 `workflow_mode: quick | strict`，不要重复询问。

- `quick`：执行完整验证，但只在上下文和最终回复中保留简短结果，不创建 `verification-report.md`。
- `strict`：执行完整验证并按 `references/integration-output.md` 生成审计报告。

模式只改变报告形态，不降低验证覆盖。

## HARD-GATE

- Critical 问题未修复时禁止标记 `ready_to_deliver: true`。
- 能安全自动修复的问题先修复并复验；其余交给 `avatar-troubleshoot`。
- sceneId 必须在线确认已发布并具备目标能力。
- 无设备或无法执行人工视觉/听觉检查时，明确标记 pending，不声称运行时通过。
- Web SDK 项目必须运行 `python "<plugin-root>/tools/web_sdk_gate.py" check --project "<project>" --interaction "<target>"`；只有退出码 0 才能进入交付。

## 七层验证

| Layer | Web | Android/iOS |
|---|---|---|
| 1 文件 | 入口、源码、配置 | 工程、Manifest/Info.plist、源码、资源 |
| 2 凭据/资源 | 环境变量、sceneId | 构建类型隔离、sceneId、授权资源 |
| 3 SDK | SDK 目录和入口 | AAR/Framework 与原生库 |
| 4 依赖 | package lock/node_modules | Gradle/CocoaPods 依赖 |
| 5 配置 | stream、bitrate、事件 | ABI、权限、播放器、事件、生命周期 |
| 6 构建 | 生产构建 | 测试、APK/Archive 构建 |
| 7 运行 | 首帧和目标交互 | 安装、初始化、首帧、目标交互和释放 |

只验证用户选择的能力。未选择语音时，不把麦克风权限、录音或 ASR 当作必检项。

## 平台分支

- 配置陷阱和自动修复：按需读取 `references/config-checks.md`。
- Web/Android 七层细节：按需读取 `references/verify-workflow.md`，不要把 Web 的 `.env`/`node_modules` 检查套到 Android。
- Android 构建：必须读取 `../avatar-shared/android-gradle-stability.md`，串行完成在线预热与 `--offline` 复验。
- 严格模式报告：读取 `references/integration-output.md`。

## 快速输出

不创建报告文件，最终仅保留高信号字段：

```yaml
status: passed | failed | pending_device_verification
workflow_mode: quick
build: passed | failed
runtime: passed | pending | failed
critical_issues: 0
ready_to_deliver: true | false
```

再列 APK/URL、测试数量和剩余阻塞；不要复述每条内部检查。

Web 的状态由 `web_sdk_gate.py` 落盘到 `.runtime/verification-result.json`：

- `failed` / 退出码 2：静态门禁失败，修复后复验。
- `needs_runtime_verification` / 退出码 3：缺少新鲜的 `connected`、`stream_start`、首帧或目标交互浏览器证据；保持 workflow 进行中。
- `ready_to_deliver` / 退出码 0：静态和浏览器门禁均通过，才允许 Reporter 标记 SDK workflow 完成。

不要由模型手写 `ready_to_deliver: true`。`.runtime/web-runtime-evidence.json` 必须来自 Playwright/浏览器验证过程，并晚于本轮工程与 SDK 变更。

## 严格输出

按 `references/integration-output.md` 输出 Layer 1-7、自动修复、证据、构建产物、运行结果和 `ready_to_deliver`。只有严格模式默认创建 `verification-report.md`。

## Red Flags

- bitrate 低于平台要求
- SDK/AAR/Framework 路径错误
- 缺少目标能力所需事件监听
- 凭据进入源码、日志或 Release 客户端
- Android 存在重叠 Gradle、慢源优先、缓存锁或激进内存配置
- 快速模式为了“审计”补生成完整过程报告

## 交接

- 通过：交付运行方式和验证结论。
- 无设备：`ready_to_install: true`、`ready_to_deliver: false`，列出真机恢复步骤。
- 失败：交给 `avatar-troubleshoot` 修复剩余 Critical/High 问题后重新验证。
