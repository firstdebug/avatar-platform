---
name: avatar-model-config
description: >-
  管理讯飞虚拟人场景的大模型和 NLP 配置，包括列出、创建、绑定、切换并发布星火或 OpenAI 兼容自有模型。用于用户已明确要操作模型配置时。
---

# avatar-model-config: 模型配置和管理

## 运行位置

从本文件反推 `<plugin-root>`，并在插件根目录执行 `tools/xfyun_model_manage.py`。不要依赖用户名、当前工作目录或固定安装路径。首次使用的登录流程见 `avatar-credentials`。

## 输入

- 要执行的动作：查询、检查能力、创建、更新、绑定或发布
- 已发布或待配置的 `sceneId`
- 模型名称；创建自有模型时还需模型标识、说明和 OpenAI 兼容端点

## 核心工作流

| 任务 | 顺序 |
|---|---|
| 查看模型 | `list` |
| 给场景绑定模型 | `check` → `bind` → `publish` → `query` |
| 创建自有模型 | `create` → `bind` → `publish` → 实际对话验证 |
| 更新密钥 | `update` → 必要时重新发布 → 实际对话验证 |
| 排查配置 | `query`，再根据结果检查授权、类型和发布状态 |

完整命令、参数和示例见 `references/operations.md`。

## 模型类型决策

| 模型 | `nlpType` | 知识库推荐链路 |
|---|---|---|
| 讯飞官方星火 | `xinghuo` | `docqa,xinghuo` |
| DeepSeek、GPT 等 OpenAI 兼容自有模型 | `openai` | `docqa,openai` |

绑定模型会重写场景 NLP 配置。若场景原来已挂知识库，绑定后重新调用 `avatar-knowledge-base` 的 `enable` 或 `chain`，把 `docqa` 加回，并确保第二段与当前 `nlpType` 一致。

## HARD-GATE

- 在 `check`、`bind`、`publish` 前确认 sceneId 已由 `avatar-credentials` 验证为存在、归属当前 appId、具备对话能力且已发布；任何“场景不存在”响应都必须转回自动创建替换场景流程，不能向旧 ID 继续写入 NLP 或 interact 草稿。
- 绑定前运行 `check <sceneId>`；场景无对话授权时不要继续。
- `bind` 后必须执行 `publish`，随后用 `query` 核对生效配置。
- 自有模型 API Key 不通过命令行参数传入；使用脚本的交互输入。
- 不在日志、回复、命令历史或示例中写真实 API Key。
- OpenAI 兼容端点填写到 `/v1` 层级，模型标识必须与提供方一致。
- 使用知识库时，调用链模型段必须匹配当前 `nlpType`。

## 执行原则

- 登录、查询、创建、绑定和发布命令由 Codex 直接执行。
- 创建和发布属于快速接入的常规平台写操作，不增加统一确认门禁。
- 用户只处理浏览器登录、授权或无法自动完成的账号操作。
- 所有标识从用户输入或平台查询结果取得，不使用示例 ID。
- 配置失败先读取平台响应和 `query` 结果，不用重复创建资源碰运气。

## 常见问题

| 现象 | 优先检查 |
|---|---|
| `bind` 被拒绝 | `check` 是否显示场景具备对话能力 |
| 配置不生效 | 是否执行 `publish`，`query` 是否返回新模型 |
| 自有模型调用失败 | API Key、`apiUrl`、模型标识和兼容格式 |
| 换模型后知识库失效 | `bind` 是否覆盖了原调用链 |
| DeepSeek 检索结果未进入目标模型 | 链路是否误用了 `docqa,xinghuo` |

## References

- `references/operations.md`：命令表、创建/绑定/发布示例和验证步骤
- `skills/avatar-knowledge-base/references/operations.md`：知识库链路的详细配置

## 验证清单

- [ ] 场景具备对话能力
- [ ] 模型已创建或可查询
- [ ] `nlpType` 与模型类型一致
- [ ] 模型已绑定并发布
- [ ] `query` 返回预期配置
- [ ] 实际对话成功
- [ ] 使用知识库时链路已恢复且类型正确

## 相关 Skill

- `avatar-credentials`：获取 `sceneId` 并完成登录
- `avatar-knowledge-base`：配置 `docqa` 链路
- `avatar-text-interact`：验证 NLP 对话
- `avatar-troubleshoot`：排查运行时错误
