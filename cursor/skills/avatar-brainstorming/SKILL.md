---
name: avatar-brainstorming
description: 为讯飞虚拟人首次 SDK 接入、从零构建或大型功能扩展确认需求边界，并按用户选择输出快速实施摘要或完整设计规格。快速模式不生成过程文档或调用 spec-reviewer；严格模式进入完整三阶段。
---

# avatar-brainstorming: 需求边界

## 定位

确认会改变实现路径的最小信息，并按 `workflow_mode` 交接实现。先读 `../avatar-shared/delivery-modes.md`。

## 输入

- 用户目标、项目路径和已知资源
- 平台或待选择的交付形态
- `workflow_mode: quick | strict`

首次 SDK 自建未指定模式时只询问一次并推荐 `quick`。已有项目单一修改不应进入本 Skill。

## 共同流程

1. 扫描现有工程和 SDK 状态，复用已知信息。
2. 调用 `avatar-preflight` 做与目标平台相关的检查，不生成额外过程文档。
3. 分类任务并确认最小需求边界。
4. 使用 `avatar-credentials` 验证待复用资源；缺失或无效资源按平台流程创建、发布并重新验证。
5. 按交付模式输出实施摘要或设计规格。

## 最小访谈

一次最多 4 个紧凑问题，只问用户尚未说明且会改变实现的内容：

| 主题 | 内容 | 未回答时默认 |
|---|---|---|
| 功能 | 文本交互、播报、短语音、全双工、字幕、动作、透明背景 | 文本交互 + 字幕 |
| 平台 | Web/Android/iOS 和最低版本 | Android 12+（仅已选 Android 时） |
| 视频 | XRTC/WebRTC/RTMP、默认/自定义/透明背景 | XRTC + 默认背景 |
| 资源 | 是否复用 appId/sceneId；无效时是否自动创建 | 复用 appId；无效 sceneId 自动替换 |

凭据和外部模型密钥作为待验证输入处理，不在对话或文档中显示完整值。不得根据“虚拟人对话”自行加入麦克风、语音或动作。

## 快速模式

不读取 `design-doc-template.md` 或 `review-and-output.md`，不创建 `design-spec.md`，不调用 `spec-reviewer`，不增加单独的用户文档确认回合。

在当前上下文维护 `delivery-modes.md` 定义的不超过 12 行实施摘要。资源验证和需求边界完成后直接调用 `avatar-executing`：

```yaml
status: ready_to_execute
workflow_mode: quick
implementation_brief: <in-memory>
next_step: avatar-executing
```

## 严格模式

按现有完整流程执行：

1. 读取 `references/project-scanning.md` 和 `references/intent-classification.md`。
2. 按 `references/interview-templates.md` 完成访谈。
3. 按 `references/design-doc-template.md` 生成设计规格。
4. 按 `references/review-and-output.md` 调用一次 `spec-reviewer`；只修复阻塞问题。
5. 用户确认后进入 `avatar-planning`。

```yaml
status: completed
workflow_mode: strict
design_spec_path: ./avatar-integration-spec.md
next_step: avatar-planning
```

## 共同 HARD-GATE

- 平台和启用/排除功能已明确。
- sceneId 在线验证为已发布、归属正确且具备接口能力；否则已创建并验证替代场景。
- 外部模型 + 知识库已明确 `docqa,<nlpType>` 链路。
- apiSecret 不进入源码、对话、日志或版本库。
- 环境阻塞不能用占位工程掩盖。

## References

快速模式只读：

- `../avatar-shared/delivery-modes.md`
- `references/project-scanning.md` 中与目标平台相关的扫描段落
- `references/intent-classification.md`（仅意图不明确时）
- `references/interview-templates.md`（仅需要具体问题措辞时）

严格模式额外读取：

- `references/design-doc-template.md`
- `references/review-and-output.md`

## 交接检查

快速模式：模式已确认、实施摘要完整、资源已验证，直接进入 `avatar-executing`。  
严格模式：设计规格已生成并通过一次阻塞性评审，用户确认后进入 `avatar-planning`。
