# avatar-platform — Cursor 包

由 acplugin 从 Claude Code 源插件转换而来。

## 内容
- `.cursor-plugin/plugin.json` — 清单（`skills` → `./.agents/skills/`，`agents` → `./agents/`）
- `.agents/skills/` — 30 个 SKILL.md + references
- `agents/` — 7 个 Cursor 格式 agent

## 投放
将本目录内容放入 Cursor 项目对应位置（`.agents/skills/` 为 skill 发现目录）。

## 已知降级
- **无自动路由**：源插件的 UserPromptSubmit 钩子在 Cursor 无对应机制，转换时已跳过。
  处理虚拟人任务需手动调用入口 skill `avatar-workflow-entry`，或把关键词路由规则写进 Cursor rules。
- **Python 工具**：源插件的 `tools/` 未包含在本转换产物内。若需要，从 Claude 包获取并
  `pip install -r tools/requirements.txt && playwright install chromium`。

## 注意
`.cursor-plugin/plugin.json` 由人工补齐（acplugin 本版禁用了 Cursor 清单生成）。
若 Cursor 实际识别的清单字段名不同，以 Cursor 官方规范为准调整。
