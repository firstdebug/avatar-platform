# avatar-platform

讯飞虚拟人交互平台接入插件，覆盖 Web 对话模板、数字人直播、Web/Android/iOS SDK、WebAPI、模型配置、知识库、凭据获取和故障排查。

本仓库同时发布 Claude Code、Codex 和 Cursor 版本。Claude Code 与 Codex 使用独立插件包和独立 manifest，不会加载对方的 Skills 或 agents。

## 安装

### Claude Code

```bash
claude plugin marketplace add https://github.com/firstdebug/avatar-platform.git
claude plugin install avatar-platform@avatar-platform-marketplace
```

验证：

```bash
claude plugin list
```

### Codex

```bash
codex plugin marketplace add firstdebug/avatar-platform --ref main
codex plugin add avatar-platform@avatar-platform-codex
```

验证：

```bash
codex plugin list
```

安装或更新后，请新建一个 Codex 任务，使新的 Skills 和 agents 生效。

### Cursor

Cursor 适配包位于 `cursor/`，可按项目需要复制其中的 `.cursor-plugin`、`.agents` 和 `agents` 目录。

## 使用

统一入口为 `avatar-workflow-entry`。也可以直接描述需求，例如：

- 创建 Web 智能客服虚拟人
- 在 Android 应用中接入虚拟人 SDK
- 通过 WebAPI 从后端驱动虚拟人
- 配置大模型或知识库
- 排查鉴权、黑屏、无声音或网络问题

## 仓库结构

```text
avatar-platform/
├─ .claude-plugin/marketplace.json
├─ .agents/plugins/marketplace.json
├─ claude/avatar-platform/          # Claude Code 自包含插件
├─ plugins/avatar-platform/         # Codex 自包含插件
├─ cursor/                          # Cursor 适配包
└─ README.md
```

Marketplace 会拉取同一个 GitHub 仓库，但安装时只注册对应平台的子目录：

- Claude Code：`claude/avatar-platform/`
- Codex：`plugins/avatar-platform/`

## 运行依赖

Python 工具需要 Python 3.8+：

```bash
pip install -r tools/requirements.txt
playwright install chromium
```

在 Claude Code 包中从 `claude/avatar-platform/` 执行，在 Codex 包中从 `plugins/avatar-platform/` 执行。

## 安全

- 不要提交 `.runtime/`、Cookie、`.env`、API Key 或 API Secret。
- Cookie 默认写入插件自身的 `.runtime/xfyun_cookies.json`。
- 可通过 `XFYUN_AVATAR_COOKIE_FILE` 覆盖 Cookie 路径。
- Web 生产接入应在服务端签名，不要把 `apiSecret` 写入前端代码。

## 版本

当前版本：`1.0.0`

许可证：MIT
