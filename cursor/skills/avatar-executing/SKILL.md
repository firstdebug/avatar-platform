---
name: avatar-executing
description: 按快速实施摘要或严格设计与计划构建讯飞虚拟人 Web、Android 或 iOS 工程。快速模式由主 agent 直接实现并验证，不生成过程文档或运行 writer-reviewer 循环；严格模式保留完整分阶段评审。
---

# avatar-executing: 执行实现

## 输入

- `workflow_mode: quick | strict`
- `quick`：不超过 12 行的内存实施摘要
- `strict`：设计规格与实施计划路径
- 平台、任务类型、项目路径和 preflight/资源验证结果

先读 `../avatar-shared/delivery-modes.md`。模式不明确时返回上游询问用户，不能默认 quick，也不能边实现边补模式。

## 共同前置门禁

- 需求边界、启用与排除能力明确。
- 首次自建或多能力扩展已有用户选择的 `workflow_mode`；没有选择时停止。
- 新增语音、麦克风权限或录音代码前，已有用户对语音能力和交互形态的明确确认。
- 凭据、sceneId 发布状态、资源授权、SDK、网络和工具链已验证。
- 目标路径和现有用户改动已识别。
- Android/Web 首次接入全文读取对应真实 Playbook。

Quick 不要求设计或计划文件存在；Strict 要求两者存在且已确认。

## 权威来源

| 场景 | 资料 |
|---|---|
| 交付模式 | `../avatar-shared/delivery-modes.md` |
| Web SDK | `references/web-sdk-build-playbook.md` |
| Android SDK | `references/android-sdk-build-playbook.md` |
| Android MainActivity | `references/android-mainactivity-template.java` |
| Android Gradle | `templates/android-build-template/` + `../avatar-shared/android-gradle-stability.md` |
| 严格执行循环 | `references/execution-loop.md` |
| 验证 | `references/verification.md` |
| 严格报告格式 | `references/output-formats.md` |

快速模式不读取 writer/reviewer 或完整报告 reference。严格模式需要时读取 `references/avatar-code-writer.md` 和 `references/avatar-code-reviewer.md`。

## 快速模式

由主 agent 直接完成：

1. 解析实施摘要和验收条件。
2. 检查/下载 SDK 产物。
3. 对可单测逻辑先写针对性测试，然后实现最小变更。
4. 按平台 Playbook 和模板直接编辑工程，不派发 writer。
5. 运行真实 API 黑名单、密钥、权限、生命周期和配置扫描，不派发 reviewer。
6. 构建、启动并验证首帧、目标交互、错误路径和资源释放。
7. 用简短最终结果交付；只列变更、验证和剩余风险，不创建过程报告文件。

出现 Playbook/SDK 签名冲突、关键静态扫描命中、同一阻塞修复两次仍失败，或用户明确要求时，才调用一次针对性 reviewer。不要因此补生成 spec/plan 或启动 writer-reviewer 循环。

## 严格模式

1. 解析设计与计划。
2. 按 `references/execution-loop.md` 使用 writer/reviewer 实现每个高风险 SDK 步骤。
3. writer 和 reviewer 必须各自读取同一平台 Playbook。
4. Critical/High 问题修复后重新评审；最多保留必要轮次。
5. 生成完整验证报告并交付审计材料。

## Web HARD-GATE

- 使用 Playbook 的后端签名架构，前端不保存完整 `apiSecret`。
- 先运行 `python "<plugin-root>/tools/sdk_artifact.py" ensure --platform web --project "<project>"`；非零退出时停止编码后的交付结论，状态保持 `blocked_missing_sdk`。
- 读取实际 SDK 的 `index.d.ts`，确认 `module.default`、`setApiInfo`、`setGlobalParams`、`start` 和目标驱动方法；不得凭记忆补 API。
- 获取凭据使用 `tools/_fetch_creds.py` 或 `avatar-credentials` 的安全写入流程；脱敏输出不能写入 `.env`，不得输出完整值。
- 签名实现逐项对照 `../avatar-network-debug/references/auth-verification.md`，必须包含 `GET <path> HTTP/1.1` 和 `headers="host date request-line"`。
- 显式配置 stream、bitrate、framerate、protocol、avatar、TTS、scene 和 dispatch。
- 扫描密钥泄漏，验证连接、首帧、自动播放和断线处理。浏览器验证必须由 Playwright/浏览器测试产生 `.runtime/web-runtime-evidence.json`，不得手写通过结论。
- 最后运行 `python "<plugin-root>/tools/web_sdk_gate.py" check --project "<project>" --interaction "<text|voice|audio>"`。退出码 2 是静态失败，3 是 `needs_runtime_verification`，都不得交付或调用完成上报；只有退出码 0 才是 `ready_to_deliver`。

Quick 与 Strict 都执行以上命令。Quick 只省略过程文档和常规 reviewer，不降低 SDK、凭据、签名、构建或浏览器验证。

## Android HARD-GATE

- 以当前 AAR 和 `android-sdk-build-playbook.md` 为准，不凭记忆拼 API。
- 使用三参数初始化、`IAvatarListener`、`createPlayer` 和 `setRenderArea`。
- `.so` 由 AAR 提供，不重复复制 WebRTC 原生库。
- 按 `android-gradle-stability.md` 串行构建、在线预热并离线复验。
- 扫描失真调用：`createStreamPlayer`、`sendText`、`onNlpResult`、`onAsrResult`、`onAvatarReady`、`writeAudioFrame`、`startAudioInteract`、`setApiKey` 和两参数初始化。

## 共同 Red Flags

- 未发布/未授权资源进入运行配置
- 用户未选择语音却加入麦克风权限或录音代码
- 用户未选择交付模式却开始首次自建或多能力扩展
- 播放器未挂载渲染容器
- 未监听错误/断线或未正确释放资源
- 用过程文档代替构建和运行验证
- 快速模式仍生成 spec/plan 或派发常规 writer/reviewer

## 验证与交接

- 编译/构建、初始化、连接、首帧和目标功能通过。
- 客观扫描无 Critical/High 命中。
- 凭据未进入源码、日志或版本库。
- 无设备或外部阻塞时明确标记未验证项。

快速模式交付代码、运行方式、验证结论和剩余风险。严格模式额外交付设计、计划、评审和完整验证报告。
