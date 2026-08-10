---
name: avatar-workflow-entry
description: >-
  讯飞虚拟人、数字人和 xfyun avatar 任务的统一入口。识别构建、SDK、模板、直播、WebAPI、知识库、模型、驱动、配置、排障或验证意图，并为 SDK 自建提供快速少文档或严格三阶段两种交付模式。
---

# Avatar workflow entry

## 目标

选择最具体的 `avatar-*` Skill 并继续执行。只询问会改变交付路径的信息，不重复收集用户已经提供的事实。

以本文件位置反推 `<plugin-root>`，从插件根目录解析 Skill、`tools/` 和 `config/`；不要依赖固定盘符、用户名或缓存版本。

## 路由流程

1. 判断咨询、创建、修改、排障或验证意图。
2. 仅在已有工程相关时扫描平台、SDK 和当前改动。
3. 按路由表选择最具体的 Skill。
4. SDK 首次自建或多能力扩展时，按 `../avatar-shared/delivery-modes.md` 选择一次 `workflow_mode: quick | strict`；用户未选择前停止，不默认 quick。
5. 把项目路径、平台、功能边界、资源状态、交付模式和已完成步骤传给目标 Skill，继续执行而不是只输出路由结果。

快速模式只需一句话说明路由和交付模式，之后仅在关键里程碑或阻塞时更新；严格模式可保留分阶段审计状态。

## 快速路由

| 用户意图 | 目标 Skill |
|---|---|
| 报错、黑屏、无声音、错误码、日志异常 | `avatar-troubleshoot` |
| Android Gradle、Wrapper、下载、缓存锁或构建卡住 | `avatar-troubleshoot` + `avatar-shared/android-gradle-stability.md` |
| 麦克风、相机或运行时权限 | `avatar-permissions-setup` |
| WebSocket、超时、断线、10200/10201 | `avatar-network-debug` |
| 修改分辨率、码率、形象、发音人、TTS 或背景 | `avatar-config-authoring` |
| 凭据、appId、apiKey、apiSecret、sceneId | `avatar-credentials` |
| 官方模板、H5、客服页、大屏、快速生成链接 | `avatar-web-template` |
| 虚拟主播、商品、分镜、直播间 | `avatar-live-streaming` |
| 不用 SDK、WebAPI、报文、直连 WebSocket | `avatar-webapi-protocol` |
| 知识库、docqa、RAG、上传文档 | `avatar-knowledge-base` |
| 创建、绑定、切换或发布大模型/NLP | `avatar-model-config` |
| 首次 SDK 接入、从零构建、多能力或架构扩展 | `avatar-brainstorming`，携带 `workflow_mode` |
| 已有项目增加单一能力 | 对应 driver/interact/action/subtitle/transparent Skill，默认 `quick` |
| 快速理解 SDK 结构 | `avatar-integration-guides` |
| 项目完成，需要交付验证 | `avatar-verification` |

故障类信号优先于创建/配置类信号。完整优先级见 `references/routing-rules.md`。

## SDK 自建模式

| 模式 | 流程 | 默认产物 |
|---|---|---|
| `quick`（推荐） | `avatar-brainstorming` 形成内存实施摘要 → `avatar-executing` 主 agent 直接实现 | 工程、构建/运行结果；不生成过程文档 |
| `strict` | `avatar-brainstorming` → `avatar-planning` → `avatar-executing`，含 spec/plan/code 评审 | 工程、设计、计划和完整验证报告 |

用户明确说快速、直接做、少文档或不要 reviewer 时直接选 `quick`。用户明确要求完整文档、审计或多人交接时选 `strict`。首次自建未表态时必须只问一次并推荐 `quick`，但不得在用户未回答时继续实现。

## 用户确认门禁

- **交付模式门禁**：首次 SDK 自建、从零构建或多能力扩展必须先问 `quick` 还是 `strict`。不能把“推荐 quick”当成用户选择。
- **语音门禁**：新增语音识别、语音问答、录音、麦克风权限或相关 UI 前，必须问用户是否确认加入语音能力，并确认交互形态。用户确认前不得修改 Manifest/Info.plist、申请麦克风权限或加入录音代码。
- **边界记录**：把用户选择写入实施摘要的 `features` 和 `excluded`；未确认的能力必须进入 `excluded`。

## SDK 自建不可跳过项

两种模式均执行：

1. 确认平台、功能范围、协议/背景和资源复用策略；未明确的能力不得自行扩展。
2. 使用 `avatar-credentials` 验证 appId/sceneId 的归属、接口能力和发布状态。
3. sceneId 无效、未发布或归属不匹配时，在已确认的 appId 下创建并发布替代场景，再写入运行配置。
4. 外部模型 + 知识库读取 `references/external-llm-knowledge-base.md`，验证 `docqa,<nlpType>` 调用链。
5. Android/Web 实现使用 `avatar-executing/references/` 下真实 Playbook，不使用快速概念指南生成代码。
6. Web SDK 自建先执行 `tools/sdk_artifact.py ensure`；返回 `blocked_missing_sdk` 时保持当前 workflow，不生成“手动下载后即可运行”的假交付。
7. Web 交付前执行 `tools/web_sdk_gate.py check`；只有退出码 0 / `ready_to_deliver` 才能标记完成，`needs_runtime_verification` 仍是同一 workflow。
8. 完成安全、构建、运行和目标交互验证；外部阻塞必须明确记录。

## 执行原则

- 直接运行可自动完成的命令，用户只处理扫码、授权或人工视觉/听觉确认。
- 遇到交付模式或语音门禁缺失时，先询问用户，不执行工程修改或平台写操作。
- 快速模式不加载或生成 spec/plan/writer/reviewer 内容。
- 只有独立任务确实能并行且不会共享写入时才考虑子 agent；快速模式默认由主 agent 完成。
- 遇到外部阻塞时给出恢复条件，不用长篇过程文档代替解决问题。

## References

- `../avatar-shared/delivery-modes.md`：快速/严格模式选择、门禁和 token 纪律
- `references/routing-rules.md`：意图优先级和边界
- `references/routing-flow.md`：路由步骤
- `references/route-targets.md`：目标输入输出
- `references/examples.md`：路由示例
- `references/external-llm-knowledge-base.md`：外部模型与 docqa 组合链路
