# avatar-platform — Codex 包

由 acplugin 从 Claude Code 源插件转换而来。

## 内容
- `.codex-plugin/plugin.json` — 清单（`skills` → `./.agents/skills/`）
- `.agents/skills/` — 30 个 SKILL.md + references（Codex 复用此目录）
- `.codex/agents/` — 7 个 `.toml` agent

## 投放
将本目录内容放入 Codex 项目对应位置，清单的 `skills` 指针解析到 `.agents/skills/`。

## 已知降级
- **无自动路由**：源插件的 UserPromptSubmit 钩子在 Codex 不可移植，转换时已跳过。
  处理虚拟人任务需手动调用入口 skill `avatar-workflow-entry`，或把关键词路由规则写进 Codex 配置。
- **Python 工具**：源插件的 `tools/` 未包含在本转换产物内。若需要，从 Claude 包获取并
  `pip install -r tools/requirements.txt && playwright install chromium`。
