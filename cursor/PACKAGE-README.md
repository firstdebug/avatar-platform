# avatar-platform - Cursor 插件包

这是基于 Codex `avatar-platform` 1.0.0 生成的 Cursor 适配包，包含 30 个 Agent Skills、配套 Python 工具、配置、规则和参考资料。

## 从 GitHub 导入

在 Cursor Dashboard 中打开：

`Plugins` -> `Team Marketplaces` -> `Add Marketplace` -> `Import from Repo`

填写仓库地址：

`https://github.com/firstdebug/avatar-platform`

仓库根目录的 `.cursor-plugin/plugin.json` 会把 Cursor 组件指向 `cursor/skills/` 和 `cursor/agents/`。导入后可在 Cursor 的 `Customize` -> `Plugins` 或 `Customize` -> `Skills` 中检查是否已启用。

## 直接使用包目录

如果不使用 Marketplace，也可以将本目录中的 `skills/` 复制到目标项目的 `.cursor/skills/`，或复制到用户目录 `~/.cursor/skills/`。入口 Skill 为 `avatar-workflow-entry`。

## 运行依赖

- Python 3.8 或更高版本
- `pip install -r tools/requirements.txt`
- 涉及网页登录时执行 `playwright install chromium`

工具运行时可能创建 `.runtime/`；该目录、Cookie 和凭据不得提交到 Git。

## 平台差异

Cursor 不执行 Claude Code 的 `UserPromptSubmit` 钩子，因此任务路由由 Cursor 根据 Skill 描述完成；也可以直接从 `avatar-workflow-entry` 开始。此包不依赖 `${CLAUDE_PLUGIN_ROOT}`，工具路径以当前包目录为基准。
