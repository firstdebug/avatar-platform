---
name: avatar-workflow-entry
description: >-
  【讯飞虚拟人/数字人任务的必经入口 — 任何虚拟人相关请求都必须先调用本 skill 再响应】处理一切与讯飞虚拟人/数字人（xfyun
  avatar）有关的需求：构建/搭建/做一个虚拟人项目或应用、从零创建/接入虚拟人、把虚拟人集成到
  web/android/ios、Web对话模板、数字人直播、WebAPI报文接入、语音/文本/音频驱动、配置调整、故障排查，以及"你能做什么/有哪些功能"这类能力询问。本
  skill 负责意图识别与智能路由，分发到对应子技能。触发词：构建虚拟人、搭建虚拟人、虚拟人项目、创建虚拟人、数字人、虚拟人集成、avatar、avatar
  SDK、讯飞虚拟人、xfyun、virtual-man、数字人直播、虚拟主播、你能做什么、有哪些功能、功能清单。收到上述任一信号时不要用通用知识直接回答或抛技术选型问题（如
  Unity/Three.js/2D-3D），必须先走本入口路由。
tags:
  - entry
  - routing
  - dispatcher
  - avatar
  - virtual-human
  - capabilities
priority: critical
---

# avatar-workflow-entry: 智能路由入口

## ⚙️ 技能库位置（路由前必读）

本入口是 avatar-platform 技能包的总入口。整个技能库在固定位置：

**根目录：`${CLAUDE_PLUGIN_ROOT}`**（插件安装目录，Claude Code 自动解析为真实路径）
- 全部 26 个业务子技能：`skills/<name>/skill.md`（本入口及 credentials/model-config/knowledge-base
  为 `SKILL.md`，其余为小写 `skill.md`）；另有 `skills/shared/` 下 2 个跨领域方法论 skill（执行时应用，不在路由表内）
- 平台脚本：`tools/xfyun_*.py`｜工具注册表：`config/tools.yaml`｜平台能力矩阵：`config/platform-registry.yaml`

**重要**：下方路由表的目标（avatar-brainstorming / avatar-preflight / avatar-troubleshoot /
avatar-config-authoring 等）中，仅 credentials/model-config/knowledge-base 已注册为可发现 skill；
**其余目标未单独注册**。路由到它们时，直接 `Read` 对应文件
`${CLAUDE_PLUGIN_ROOT}/skills/<目标名>/skill.md` 作为 playbook 执行，
而非期待系统自动加载。

## 定位

虚拟人集成任务的**统一入口**，负责快速识别任务类型并路由到对应技能。

## 调用时机

- 用户提出虚拟人相关需求
- 明确的问题场景（故障排查、配置调整）
- 模糊的需求场景（需要澄清）

---

## 核心工作流概览

三步完成路由决策：

1. **快速扫描工程** — 检测 SDK 集成状态（未集成 / 部分 / 完整）与平台（web / android / ios / unknown）
2. **意图识别** — 结合关键词、指标、工程扫描结果输出意图类型与置信度
3. **路由决策** — 按置信度阈值决定直接路由、询问确认或回退完整流程

完整代码实现见 `references/routing-flow.md`。

---

## 决策分支（场景 → 路由目标）

| 场景 | 典型信号 | 路由目标 | 优先级 |
|------|----------|----------|--------|
| 故障排查 | 失败/报错/黑屏、错误码、日志 | avatar-troubleshoot | highest |
| 权限问题 | 权限拒绝、麦克风/摄像头 | avatar-permissions-setup | high |
| 网络问题 | 连接/超时/断开、10200/10201 | avatar-network-debug | high |
| 配置调整 | 调整/修改、分辨率/码率/形象 | avatar-config-authoring | high |
| Web 对话模板 | 智能客服/H5/大屏、用模板快速生成对话页 | avatar-web-template | high |
| 数字人直播 | 直播间/虚拟主播/带货/分镜 | avatar-live-streaming | high |
| WebAPI 报文接入 | WebAPI/web api/报文/协议/不用SDK/直连WebSocket/请求响应/ctrl/event_type | avatar-webapi-protocol | high |
| 知识库管理 | 知识库/docqa/RAG/上传文档/知识问答/文档检索 | avatar-knowledge-base | high |
| 首次接入 | 集成/接入/从零、SDK 未集成 | avatar-brainstorming | medium |
| 功能扩展 | 添加/新增、语音交互/动作控制 | avatar-brainstorming | medium |
| 文档查询 | 如何/怎么、无实施意图 | provide_docs | low |

- 完整关键词 / 指标映射：见 `references/routing-rules.md`
- 各路由目标的输入 / 输出说明：见 `references/route-targets.md`
- 各置信度下的完整示例：见 `references/examples.md`

---

## 外部LLM + 讯飞知识库集成（路由增强：识别后按原生链路处理）

**触发条件**：用户需求中**同时**出现以下信号：
- 外部LLM关键词：DeepSeek / GPT / Claude / ChatGPT / 通义千问 / 文心一言 / 外部模型 / 第三方模型
- 讯飞能力关键词：讯飞知识库 / docqa / NLP / 星火 / 虚拟人对话 / 大模型对话

**关键事实（不是冲突）**：讯飞平台支持把外部 LLM（DeepSeek/GPT 等）注册为**自有模型**
（`create-custom-model`，modelType=2，`nlpType=openai`，走 OpenAI 兼容端点）。知识库（docqa）
的检索结果可以通过调用链 `docqa,<自有模型>` 灌给这个外部模型生成答案——**并非只能对接星火**。
调用链 `nlpAssistantInfo` 是**原样可配置字符串**，`docqa,openai` 与 `docqa,xinghuo` 同等有效。

**原生集成链路（DeepSeek + 健身知识库为例）**：
1. `create-custom-model` 注册 DeepSeek（apiUrl=OpenAI 兼容端点，apiKey 交互输入）→ nlpType 识别为 `openai`
2. `bind-model` 把 DeepSeek 绑到场景（写入 nlpExtra 的 apiKey/baseUrl/model）
3. `create-knowledge-base` + `upload-kb-document` 建库并上传健身文档（平台自动切块+向量化）
4. `enable-kb-for-scene ... --chain docqa,openai`（**必须显式指定 openai**，默认 `docqa,xinghuo` 会指向星火）
5. `publish-kb-scene` 发布生效

**处理流程**：
- 识别到该组合 → **不中断路由**，直接路由到 `avatar-brainstorming`（首次接入/建项目）或
  `avatar-knowledge-base`（已有场景只需配知识库），并在规划中标注"DeepSeek 走自有模型 + `docqa,openai` 链路"
- 仅当用户明确表示"不想把密钥托管到讯飞平台/要完全自建 RAG"时，才改走 App/后端自建 RAG 方案

**HARD-GATE**：给外部 LLM 挂知识库时，`enable`/`chain` 的调用链第二段**必须**是绑定模型的
nlpType（自有模型=`openai`），写成 `docqa,openai`。沿用默认 `docqa,xinghuo` 会导致知识库检索
结果被喂给星火而非 DeepSeek。

**示例**：
```
用户："构建基于健身知识库的虚拟人对话安卓项目，用DeepSeek模型"
检测到：DeepSeek(外部LLM) + 知识库(讯飞能力) → 原生可集成，无需自建RAG
输出：路由到 avatar-brainstorming，标注"DeepSeek 注册为自有模型(openai) + docqa,openai 链路挂健身知识库"
```

---

## 交付形态澄清（HARD-GATE：宽泛"构建对话项目"需求）

当用户表达的是**宽泛的"构建 / 搭建 / 做一个 虚拟人对话项目 / 应用"**，且**未指明交付形态**时，
**不要**默认跳进 SDK 自建（avatar-brainstorming）访谈。先用 `AskUserQuestion` 澄清路径，再路由：

| 路径 | 交付物 | 路由目标 | 适合 |
|------|--------|----------|------|
| 官方模板 | 零代码、开箱即用的可访问链接 | avatar-web-template | 智能客服 / H5 / 大屏，想快速拿链接 |
| 数字人直播 | 营销带货直播间（商品 / 分镜 / 脚本） | avatar-live-streaming | 虚拟主播、带货直播场景 |
| 接 SDK 自建 | 真正的前端 / 客户端工程项目 | avatar-brainstorming → avatar-executing | 需要定制 UI、深度集成、控制交互细节 |

判定规则：
- 用户信号明确偏向某一路径（如"用模板""要个链接" / "直播""带货""虚拟主播" / "接 SDK""自己写前端""要个工程"）→ 直接路由，不必再问
- 信号不明确（如仅"构建一个虚拟人对话项目"）→ 先 `AskUserQuestion` 让用户在上述路径中选择，再路由
- **不要**在澄清中列出尚未支持的交付形态，只呈现当前可交付的路径

---

## 方法论增强（横切能力，非意图路由目标）

上表是"用户意图 → 业务 skill"的路由。另有一类跨领域方法论 skill（`skills/shared/`），
不是用户开口要的东西，而是**在执行编码/多任务时自动应用**。路由到实施类目标
（brainstorming/executing 等）时，若命中以下场景，一并提示应用对应方法论：

| 场景信号 | 应用方法论（skills/shared/） | 落地位置 |
|----------|------------------------------|----------|
| 要写可单测的业务逻辑/函数/模块、或修逻辑 bug | test-driven-development（先写失败测试再实现） | avatar-executing Step 3 |
| 手头有多个**互不依赖、不写同一文件**的任务 | dispatching-parallel-agents（并行分发子 agent） | avatar-planning 标注 + avatar-executing Step 3 |

说明：这两个是**增强**不是门禁——SDK 真机交互无法单测的部分不套 TDD（走
avatar-verification 运行时验证）；有依赖的任务不并行（仍串行）。

---

## 关键约束

### 优先级规则（HARD-GATE）

故障排查 > 权限/网络问题 > 配置调整 > 首次接入/功能扩展

多个信号命中时，**必须**按上述优先级选择路由目标。

### 置信度阈值（HARD-GATE）

- **> 0.8**：直接路由
- **0.5 - 0.8**：询问用户确认
- **< 0.5**：回退到 avatar-brainstorming 完整流程

### Red Flags

- 工程扫描结果与用户描述矛盾（如称"已集成"但扫描无 SDK）→ 以扫描结果为准并提示用户
- 同时命中故障排查与配置调整 → 优先故障排查
- 需求模糊且平台未知 → 不要猜测，回退完整流程澄清

### 其他注意事项

- **工程扫描**：利用缓存避免重复扫描，扫描结果作为路由决策依据
- **用户体验**：明确问题快速路由，模糊需求走完整流程，避免过度询问

### 执行原则（HARD-GATE：路由到实施类目标后适用）

- **第一条消息就走 skill**：avatar 相关需求一进来就调用本入口做路由，**不要**先用通用知识
  抛技术选型问题（如 Unity / Three.js / 2D-3D）。本平台走讯飞官方能力，通用选型问答是跑偏。
- **主动执行，最小化用户手动操作**：涉及命令行工具的步骤由 Claude 直接用 Bash/PowerShell 执行，
  **不要**让用户在输入框自己输命令（`! ...`）。跑命令、切目录、打开浏览器都是 Claude 的工作。
- **浏览器交互分工**：需要浏览器的命令（登录、create、publish）直接执行且**默认不加 `--no-browser`**，
  让浏览器自动弹出；用户只负责浏览器里的人类动作（扫码、测试对话）。**切勿**只贴链接让用户自己打开。
- **HARD-GATE 前置校验要提前**：如模板路径要求 appType=2，应在 create **之前**用 `list-apps` 校验，
  别等到 create 被门禁拦下才发现。
- **阻塞时给明确选项**：遇到无法自动解决的阻塞（如需用户订阅新应用），立刻给出"路径 A / 路径 B"
  式的可选方案 + 各自 trade-off + 相关链接，而不是只报告问题。
- **⚠️ SDK 自建工程强制三阶段流程（Android/Web）**：
  - 当目标是 `avatar-brainstorming` 且涉及 Android/Web SDK 自建工程时，**必须**完整走完三阶段：
    1. `avatar-brainstorming` → design-spec.md
    2. `avatar-planning` → implementation-plan.md（计划中必须引用 playbook）
    3. `avatar-executing` → 按 playbook 严格执行（**不允许主 agent 绕过 avatar-executing 直接手写代码**）
  - **违规后果**：主 agent 手写代码会用错 API（Android: createStreamPlayer/sendText 等不存在，Web: bitrate 陷阱、前端硬编码 apiSecret），导致编译失败、黑屏、构建 20+ 分钟。
  - **执行检测**：在 brainstorming/planning 完成后，系统会检查主 agent 是否调用了 `avatar-executing` skill，如未调用则报错并提示正确流程。

---

## references/ 索引

| 文件 | 内容 |
|------|------|
| `references/routing-rules.md` | 完整路由规则表（关键词 / 指标 / 目标 / 优先级） |
| `references/routing-flow.md` | 三步路由流程的完整 JavaScript 实现 |
| `references/route-targets.md` | 6 个路由目标的适用场景、输入、输出 |
| `references/examples.md` | 4 个置信度场景的完整路由示例 |

---

## 输出格式

### 成功路由
```yaml
status: "routed"
target: "avatar-troubleshoot"
confidence: 0.95
reason: "明确的错误码和异常行为"
```

### 需要确认
```yaml
status: "needs_confirmation"
suggested_target: "avatar-config-authoring"
confidence: 0.75
question: "检测到您想调整虚拟人分辨率，是否需要我帮您修改配置？"
```

### 回退到完整流程
```yaml
status: "fallback_to_full_workflow"
target: "avatar-brainstorming"
reason: "需求不明确，需要完整的澄清流程"
```

---

## 相关技能

- `avatar-brainstorming`: 完整工作流入口
- `avatar-troubleshoot`: 故障排查
- `avatar-config-authoring`: 配置调整
- `avatar-permissions-setup`: 权限配置
- `avatar-network-debug`: 网络诊断
