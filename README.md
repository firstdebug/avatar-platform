# avatar-platform

讯飞虚拟人交互平台全流程接入助手 - 从零代码快速搭建到 SDK/WebAPI 深度集成。

接入方式：
claude code：


## 功能概览

支持四种接入方式:

### 1. 创建标准应用(零代码)

- **Web 对话模板**: 智能客服、H5 对话页、大屏交互
- **数字人直播平台**: 虚拟主播带货、直播间互动

### 2. SDK 集成开发

- **Web SDK**: 浏览器端、H5 页面、桌面应用
- **Android SDK**: 原生 Android 应用
- **iOS SDK**: 原生 iOS 应用

### 3. WebAPI 报文接入

- 后端直连,无需 SDK
- 支持 Python/Java/Node.js
- 完整协议文档和 demo

### 4. 其他核心能力

- 登录获取凭据、检查应用授权
- 环境检查、配置调整
- 错误码定位、网络诊断
- 大模型配置、知识库管理

## 快速开始（目前仅支持claude code，codex与cursor的正在适配中）

方式 1：从 GitHub 直接安装（推荐）

```bash
# 从 GitHub 仓库安装
claude plugin add https://github.com/firstdebug/avatar-platform.git

# 或使用简写
claude plugin add firstdebug/avatar-platform
```

方式 2：本地开发模式

```bash
# 克隆仓库
git clone https://github.com/firstdebug/avatar-platform.git
cd avatar-platform

# 链接到 Claude Code
claude plugin link .
```

方式 3：添加为插件市场

```bash
# 添加市场源
claude plugin marketplace add https://github.com/firstdebug/avatar-platform.git

# 然后安装插件
claude plugin install avatar-platform
```

✅ 验证安装

```bash
# 查看已安装插件
claude plugin list

# 应该看到 avatar-platform 出现在列表中
```

🚀 快速开始

安装成功后，在 Claude Code 中使用：

```
/avatar-workflow-entry
```

或者直接告诉 Claude 你的需求：

- "我想做一个智能客服"
- "需要在 Android app 里集成虚拟人"
- "后端 Python 怎么对接 WebAPI"
- "你能做什么" / "有哪些功能"

## 目录结构

```
avatar-platform/
├── .claude-plugin/      # Plugin 元信息
├── skills/              # 28 个接入 skills
│   ├── avatar-credentials        # 登录获取凭据
│   ├── avatar-preflight          # 环境检查
│   ├── avatar-artifact-download  # SDK 下载
│   ├── avatar-web-template       # Web 对话模板
│   ├── avatar-live-streaming     # 数字人直播
│   ├── avatar-webapi-protocol    # WebAPI 接入
│   ├── text-driver               # 文本驱动
│   ├── voice-interact            # 语音交互
│   ├── full-duplex               # 全双工
│   └── ...                       # 其他 19 个 skills
├── tools/               # Python 工具脚本
│   ├── xfyun_common.py           # 登录、Cookie 管理
│   ├── xfyun_query_services.py   # 查询场景服务
│   ├── xfyun_template.py         # Web 模板创建
│   ├── xfyun_live.py             # 直播平台创建
│   ├── xfyun_model_manage.py     # 大模型配置
│   └── xfyun_knowledge.py        # 知识库管理
├── config/              # 配置文件
│   ├── agents.json               # Agent 定义
│   ├── tools.yaml                # 工具链配置
│   ├── error-codes.yaml          # 错误码映射
│   └── platform-registry.yaml    # 平台注册信息
└── docs/                # 文档
    ├── capabilities.md           # 功能清单
    ├── onboarding-flow.md        # 接入流程
    ├── authoring-guide.md        # Skill 编写指南
    ├── tool-integration-guide.md # 工具集成指南
    └── migration-codex-cursor.md # 迁移到 Codex/Cursor 说明
```

## Skills 列表(28 个)

### 接入准备与配置

- `avatar-workflow-entry` - 任务路由和工作流入口
- `avatar-credentials` - 登录平台、获取凭据、检查应用授权
- `avatar-preflight` - 环境门禁(Node/npm/防火墙/依赖)
- `avatar-artifact-download` - 自动下载 SDK 和资源
- `avatar-config-authoring` - 配置调整(分辨率/码率/形象/背景/音色)
- `toolchain` - 工具链检查(web/android/ios)

### 标准应用(零代码)

- `avatar-web-template` - Web 对话模板创建
- `avatar-live-streaming` - 数字人直播平台

### SDK 交互能力

- `text-driver` - 文本驱动
- `text-interact` - 文本交互(大模型对话)
- `audio-driver` - 音频驱动
- `voice-interact` - 语音交互(ASR+NLP+TTS)
- `full-duplex` - 全双工(实时打断)
- `action-control` - 动作控制
- `subtitle-setup` - 字幕配置
- `transparent-bg` - 透明背景

### WebAPI 报文接入

- `avatar-webapi-protocol` - WebAPI 协议和 demo

### 故障排查与调试

- `avatar-troubleshoot` - 错误码定位、常见问题排查
- `avatar-permissions-setup` - 浏览器权限配置(麦克风/摄像头)
- `avatar-network-debug` - 网络诊断(WSS 连通性/DNS)

### 平台管理

- `avatar-model-config` - 绑定/切换大模型(星火/GPT/Claude)
- `avatar-knowledge-base` - 创建/上传/管理知识库

### 开发辅助

- `avatar-brainstorming` - 需求澄清和方案设计
- `avatar-planning` - 集成任务计划生成(三阶段工作流第二阶段)
- `avatar-executing` - 执行器(调度其他 skills)
- `avatar-verification` - 交付前完整验证流程
- `integration-guides` - 三端集成指南索引(Web/Android/iOS 快速理解)
- `shared` - 跨 skill 复用的共享材料(TDD/并行分发/Android 分区存储)

## Tools 说明

所有 Python 工具位于 `tools/` 目录,通过 `config/tools.yaml` 配置调用:

- **xfyun_common.py**: 登录、Cookie 管理(所有工具的基础)
- **xfyun_query_services.py**: 查询场景服务(获取 sceneId/serviceId)
- **xfyun_template.py**: Web 模板创建(生成预览链接)
- **xfyun_live.py**: 直播平台创建(生成直播链接)
- **xfyun_model_manage.py**: 大模型配置(绑定/切换模型)
- **xfyun_knowledge.py**: 知识库管理(创建/上传文档)

## 使用方式

### 启动入口

本 plugin 的所有功能通过 **avatar-workflow-entry** skill 作为统一入口:

```
/avatar-workflow-entry
```

或者直接告诉我你的需求,我会自动识别并路由:

- "我想做一个智能客服"
- "需要在 Android app 里集成虚拟人"
- "后端 Python 怎么对接 WebAPI"
- "你能做什么" / "有哪些功能"

### 自动路由流程

当你提出需求后,系统会自动:

1. **识别意图**(通过 `avatar-workflow-entry` 智能路由)
2. 引导订阅产品(如果还没订阅)
3. 登录获取凭据(`avatar-credentials`)
4. 检查应用授权
5. 进入对应 skill 完成集成:
   - 零代码 → `avatar-web-template` / `avatar-live-streaming`
   - SDK 开发 → `text-driver` / `voice-interact` / `full-duplex` 等
   - WebAPI → `avatar-webapi-protocol`
   - 配置调整 → `avatar-config-authoring`
   - 故障排查 → `avatar-troubleshoot`

### 作为开发者

如果你要扩展或修改 skills:

1. 阅读 `docs/authoring-guide.md` 了解 skill 编写规范
2. 参考现有 skill 的 SKILL.md 和 references/
3. 新增工具参考 `docs/tool-integration-guide.md`
4. 更新 `config/tools.yaml` 注册新工具

## 依赖

- **Python 3.8+**: 运行 tools/ 下的工具脚本。依赖见 `tools/requirements.txt`：
  
  ```bash
  pip install -r tools/requirements.txt
  playwright install chromium
  ```
- **Node.js 16+**: Web SDK 开发环境(仅 SDK 接入需要)

## 跨平台支持

本插件原生为 **Claude Code** 开发，同时支持转换到 **Cursor** 和 **Codex**。

### 安装方式

#### Claude Code

```bash
# 方法1: 直接链接仓库根目录（推荐，开发模式）
cd /path/to/avatar-platform
claude plugins link .

# 方法2: 从插件市场安装
claude plugins install avatar-platform

# 验证
claude plugins list
```

#### Cursor

```bash
# 进入你的项目目录
cd /path/to/your-project

# 复制插件文件到项目
cp -r /path/to/avatar-platform/cursor/.cursor-plugin .cursor-plugin
cp -r /path/to/avatar-platform/cursor/.agents .agents
cp -r /path/to/avatar-platform/cursor/agents agents

# 或使用符号链接（开发模式）
ln -s /path/to/avatar-platform/cursor/.cursor-plugin .cursor-plugin
ln -s /path/to/avatar-platform/cursor/.agents .agents
ln -s /path/to/avatar-platform/cursor/agents agents

# 重启 Cursor
```

#### Codex

```bash
# 进入你的项目目录
cd /path/to/your-project

# 复制插件文件到项目
cp -r /path/to/avatar-platform/codex/.codex-plugin .codex-plugin
cp -r /path/to/avatar-platform/codex/.agents .agents
cp -r /path/to/avatar-platform/codex/.codex .codex

# 或使用符号链接（开发模式）
ln -s /path/to/avatar-platform/codex/.codex-plugin .codex-plugin
ln -s /path/to/avatar-platform/codex/.agents .agents
ln -s /path/to/avatar-platform/codex/.codex .codex

# 重启 Codex 客户端
```

### 重新生成 Cursor/Codex 包

如果你修改了源码，需要重新转换：

```bash
# 安装转换工具（首次）
npm install -g @disdjj/acplugin

# 重新生成 Cursor 和 Codex 包
acplugin -i . -o dist-convert

# 同步到根目录的 cursor/ 和 codex/
rsync -av --delete dist-convert/cursor/ cursor/
rsync -av --delete dist-convert/codex/ codex/
```

## 版本

当前版本: **1.0.0**

## 许可

MIT License

## 联系方式

- 讯飞虚拟人交互平台: https://virtual-man.xfyun.cn/
- 技术文档: https://doc.xfyun.cn/avatar/

---

> 本 plugin 包含 28 个 skills、6 个 Python 工具、4 个配置文件,覆盖讯飞虚拟人接入的全流程。
