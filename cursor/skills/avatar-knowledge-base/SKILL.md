---
name: avatar-knowledge-base
description: >-
  管理讯飞知识库、docqa 和 RAG，包括建库、上传文档、分类、关联场景、配置检索链路与发布。用于用户已明确要操作知识库或为已有虚拟人场景增加知识问答时。
---

# avatar-knowledge-base: 知识库管理

## 运行位置

从本文件反推 `<plugin-root>`，并在插件根目录执行 `tools/xfyun_knowledge.py`。不要依赖用户名、当前工作目录或固定安装路径。首次登录见 `avatar-credentials`。

## 前置条件

- 场景经 `avatar-credentials` 精确验证存在、归属目标 appId、具备对话能力且已发布；不接受只能查询到草稿配置的 sceneId。
- 场景已绑定 NLP 模型；模型配置见 `avatar-model-config`。
- 已明确目标场景、文档来源和期望的回答策略。
- 自有模型的 `nlpType` 为 `openai`，官方星火为 `xinghuo`。

## 核心工作流

1. 用 `labels`/`create-label` 准备标签，再用 `create-kb` 建库。
2. 用 `upload ... --wait` 上传文档并等待拆分、向量化完成。
3. 用 `docs <libId>` 确认每个文档 `status=1` 且段落数大于 0。
4. 用 `enable <sceneId> <libId> --chain <chain>` 关联场景。
5. 用 `publish <sceneId>` 发布配置。
6. 用 `status <sceneId>` 和真实问答验证检索命中。

完整命令、参数、分类、删除和更新示例见 `references/operations.md`。

## 调用链决策

| 场景 | 推荐链路 |
|---|---|
| 严格基于文档回答 | `docqa` |
| 知识库优先，官方星火生成 | `docqa,xinghuo` |
| 知识库优先，自有模型生成 | `docqa,openai` |
| LLM 优先，再补充知识库 | `xinghuo,docqa` 或 `openai,docqa` |
| 暂时只用模型 | `xinghuo` 或 `openai` |

链路中的模型段必须与场景当前 `nlpType` 一致。DeepSeek、GPT 等 OpenAI 兼容模型不能沿用 `docqa,xinghuo`。

## 文档策略

- 普通文章和说明书默认使用智能拆分。
- 有稳定章节结构的文档可用目录拆分。
- Q&A 表格使用问答对类型，确保问题和答案列符合工具约定。
- 上传时显式分类前，先确认分类 ID 属于当前知识库。
- 批量上传后逐项检查状态，不因部分成功而把整批标为完成。

## HARD-GATE

- `check`、`enable` 或 `publish` 返回场景不存在、未发布或无能力时，立即停止本技能，回到 `avatar-credentials` 创建并验证替换接口场景；不得继续上传关联到无效 ID，或把失败留在报告中。
- 文档处理完成前不进入场景联调。
- `enable` 或 `chain` 后必须 `publish`。
- 换模型后重新检查知识库链路；`bind` 可能覆盖 `docqa` 配置。
- 不把文档内容或平台密钥粘贴到对话中，直接用工具上传。
- 所有 `sceneId`、`libId`、`docId` 和分类 ID 来自运行时查询，不使用示例值。
- 删除文档或知识库沿用脚本内置的不可逆操作确认，不新增针对常规创建、上传、关联和发布的统一门禁。

## 执行原则

- Cursor Agent 直接执行登录、建库、上传、关联和发布命令。
- 用户只处理浏览器登录、授权或文档内容选择等人工步骤。
- 平台写操作失败时读取响应并查询当前状态，避免重复创建同名资源。
- 上传新文档通常形成新版本；只有关联或链路发生变化时才需要重新发布场景。

## 常见问题

| 现象 | 优先检查 |
|---|---|
| 文档一直处理中且段落为 0 | 分类 ID、拆分策略、文件格式和文件完整性 |
| 对话不引用知识库 | 链路是否包含 `docqa`，配置是否已发布 |
| 换模型后知识库失效 | `bind` 是否覆盖调用链，模型段是否随 `nlpType` 更新 |
| DeepSeek 回答异常 | 是否错误使用 `docqa,xinghuo` |
| `domain can not be blank` | 重新执行 `enable` 或模型绑定，补齐 NLP domain |
| `enable` 被拒绝 | 场景是否具备对话能力 |

## References

- `references/operations.md`：全部命令、上传参数、分类、删除和典型工作流
- `skills/avatar-model-config/references/operations.md`：自有模型创建、绑定和发布

## 验证清单

- [ ] 有有效 `libId`
- [ ] 文档处理成功且段落数大于 0
- [ ] 场景具备对话能力并已绑定模型
- [ ] 调用链包含预期的 `docqa` 与模型段
- [ ] 配置已发布
- [ ] `status` 返回预期知识库和链路
- [ ] 真实问答能引用文档内容

## 相关 Skill

- `avatar-model-config`：准备 NLP 模型
- `avatar-credentials`：准备场景凭据
- `avatar-text-interact`：进行文本问答验证
- `avatar-troubleshoot`：排查运行时问题
