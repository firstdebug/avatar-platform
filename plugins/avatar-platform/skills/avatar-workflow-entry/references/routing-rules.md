# 路由规则

本文件是完整路由规则的唯一来源。`SKILL.md` 只保留快速索引。

## 优先级

按以下顺序处理同时出现的信号：

1. 明确故障、错误码或异常行为
2. 权限或纯网络问题
3. 已有项目的配置修改
4. 用户明确指定的交付形态或平台能力
5. 首次接入和宽泛构建需求
6. 纯概念或文档查询

## 意图映射

| 意图 | 信号 | 路由 |
|---|---|---|
| 故障排查 | 报错、失败、黑屏、无声音、日志、错误码 | `avatar-troubleshoot` |
| 权限问题 | 权限拒绝、麦克风、摄像头、录音失败 | `avatar-permissions-setup` |
| 网络问题 | WebSocket、连接、超时、断开、10200、10201 | `avatar-network-debug` |
| 配置修改 | 分辨率、码率、帧率、形象、发音人、TTS、背景 | `avatar-config-authoring` |
| 凭据 | appId、apiKey、apiSecret、sceneId、接口服务 | `avatar-credentials` |
| 官方模板 | 模板、H5、客服页、大屏、快速链接 | `avatar-web-template` |
| 直播 | 直播间、虚拟主播、带货、商品、分镜、脚本 | `avatar-live-streaming` |
| WebAPI | 不用 SDK、报文、协议、ctrl、event_type、直连 WebSocket | `avatar-webapi-protocol` |
| 知识库 | 知识库、docqa、RAG、上传文档、文档检索 | `avatar-knowledge-base` |
| 模型配置 | 绑定模型、自有模型、OpenAI 兼容模型、发布 NLP | `avatar-model-config` |
| 首次 SDK 接入 | 从零、接 SDK、新工程、完整项目 | `avatar-brainstorming` |
| 单一功能扩展 | 已有工程且只增加文本、动作、字幕或透明背景 | 对应能力 Skill |
| 语音能力扩展 | 已有工程且要增加语音识别、语音问答、录音或麦克风权限 | 先问语音确认，再用 `avatar-voice-interact`/`avatar-permissions-setup` |
| 概念了解 | 只问 SDK 结构、无实施意图 | `avatar-integration-guides` |

## 边界规则

- “调高分辨率”是明确配置修改，直接处理，不需要再问是否要修改。
- “黑屏后想换形象”先排查黑屏，再修改形象。
- “做一个虚拟客服”缺少交付形态，只询问模板、直播或 SDK 自建三选一。
- “用 Android SDK 做虚拟客服”已经明确 SDK 自建，直接进入 `avatar-brainstorming`。
- “给现有项目加语音交互”即使工程和目标明确，也先确认是否加入语音能力和交互形态；确认后用 `avatar-voice-interact`。涉及多项能力或架构调整时还要进入 `avatar-brainstorming` 并选择快速或严格模式。
- `avatar-integration-guides` 仅解释结构，不作为 Android 或 Web 生产代码来源。
- 工程扫描结果与用户描述冲突时，说明证据并以实际工程状态规划后续操作。
