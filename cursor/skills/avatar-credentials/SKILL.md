---
name: avatar-credentials
description: >-
  获取、验证并写入讯飞虚拟人平台凭据，包括 appId、apiKey、apiSecret 和 sceneId。用于创建接口服务、自动登录控制台、检查资源授权或为项目生成环境变量时。
---

# avatar-credentials: 凭据获取和验证

## 运行位置

从本文件反推 `<plugin-root>`，并在插件根目录执行 `tools/xfyun_*.py`。Cookie 默认保存到 `<plugin-root>/.runtime/xfyun_cookies.json`；用 `XFYUN_AVATAR_COOKIE_FILE` 可覆盖。不要依赖用户名、当前工作目录或安装缓存路径。

## 必需数据

| 配置 | 用途 |
|---|---|
| `appId` | 应用标识 |
| `apiKey` / `apiSecret` | WebSocket 鉴权 |
| `sceneId` | 已发布的接口服务标识 |
| `avatarId` | 已授权形象 |
| `vcn` | 已授权发音人 |

首次接入默认使用：

- 形象 ID：`111310001`
- 发音人：`x4_lingxiaoqi_oral`

保持默认值以减少接入变量。仅在平台明确返回未授权或用户要求更换时，查询当前 `appId` 的可用资产。

## 自动流程

1. 在 `<plugin-root>` 运行 `python tools/xfyun_common.py cookie-path`。
2. 登录态缺失或过期时运行 `python tools/xfyun_common.py login`；需要重登时加 `--force`。
3. 运行 `python tools/xfyun_query_services.py` 查询应用、场景和脱敏密钥。
4. 从查询结果选择准确的 `appId` 与 `sceneId`。
5. 运行 `python tools/write_env_safe.py <appId> <sceneId> <outputPath>`，直接把完整密钥写入目标环境文件。
6. 进行格式检查、资源授权检查和在线连接验证。

## 场景解析与自动修复（HARD-GATE）

对用户提供的 `sceneId`，先运行场景列表查询并按精确 ID 匹配，再确认：`scene.appId == appId`、场景是接口类型、具备对话能力且发布成功。不能仅凭 `query <sceneId>` 能返回草稿 NLP 配置就判定场景有效。

若场景缺失、未发布、归属不匹配、没有对话能力，或最小连接返回 `10114`，按以下顺序执行：

```text
1. 保留已验证的 appId，不继续写入旧 sceneId。
2. python tools/xfyun_interface.py create <appId> <sceneName> --desc <description>
3. 从工具输出读取新 sceneId，并重新执行 scenes/check/publish/在线连接验证。
4. 只有全部通过后，使用新 sceneId 覆盖目标 credentials.json 或环境文件。
```

创建命令已包含 NLP、交互和发布；发布或验证失败时，查询新场景的实际状态并修复。不得把无效场景写成“草稿可配置”，也不得把“创建新场景”留作用户后续操作或交付文档中的待办项。

完整控制台流程见 `references/console-setup-guide.md`；自动工具不可用时再用 `references/interactive-guide.md`。

## 缺凭据时的强制脚本顺序

当上游任务说“有账号但没配好”、未给完整 6 项凭据、或项目里没有有效 `credentials.json` 时，必须先尝试自动获取，不得直接生成占位配置：

```text
1. python tools/xfyun_common.py cookie-path
2. python tools/xfyun_common.py login        # 无有效 Cookie 时；允许打开浏览器
3. python tools/xfyun_query_services.py      # 查询应用、场景、脱敏密钥
4. python tools/xfyun_model_manage.py scenes # 需要确认场景时
5. python tools/write_env_safe.py <appId> <sceneId> <outputPath>
```

若任务还包含外部模型或知识库，凭据写入后继续运行对应平台脚本，而不是把配置工作留给用户：

```text
python tools/xfyun_model_manage.py list|create|bind|publish
python tools/xfyun_knowledge.py labels|create-label|create-kb|upload|enable|status
```

仅在以下情况下允许降级为“配置后即可运行”：

- 用户拒绝登录或无法完成扫码/授权；
- 账号没有接口服务或对话/文档能力，且需要人工开通；
- 脚本连续失败并给出明确平台错误、网络错误或权限错误；
- 用户明确要求离线生成工程，不进行平台写操作。

降级输出必须列出已运行的脚本、成功项、失败项和恢复命令。

## 执行分工

- Cursor Agent 负责运行命令、设置工作目录、打开浏览器、查询平台和写入配置。
- 用户只处理扫码、账号登录、订阅确认等必须由人完成的浏览器操作。
- 登录、查询、创建接口服务、写入配置和发布是快速接入常规步骤，不增加统一确认门禁。
- 凭据不要经过对话文本；优先让脚本从平台响应直接写入目标文件。

## 决策分支

| 情况 | 处理 |
|---|---|
| 已有有效 Cookie | 直接查询服务，不重复打开浏览器 |
| Cookie 缺失或过期 | 执行 `login`，等待用户完成浏览器登录 |
| 账号无可用应用 | 读取 `references/app-authorization-check.md`，打开订阅页面 |
| 应用授权不匹配 | 报告缺失能力并引导补授权 |
| 能查询但缺接口场景 | 按控制台指南创建并发布接口服务 |
| 自动工具失败 | 转交互式流程，不要求用户代跑终端命令 |
| 格式通过但连接失败 | 读 `references/error-codes.md`，再转 `avatar-network-debug` |

## HARD-GATE

- 接口服务必须发布；未发布的 `sceneId` 不可交付。
- `sceneId` 只有通过精确归属、发布状态、对话能力和最小连接四项验证后才能交付；任一项失败必须自动创建替换场景或明确阻断，不能继续配置无效场景。
- `apiSecret` 和自有模型 API Key 不打印完整值，不进入命令行参数或聊天记录。
- `.env`、`credentials.json` 和其他凭据文件必须加入目标项目 `.gitignore`。
- `avatarId` 与 `vcn` 必须属于当前应用授权范围。
- 所有应用和场景匹配使用精确 ID，不用模糊匹配或列表第一项。
- Windows 下自动化交互式密钥输入时，遵循 `references/windows-secret-input.md`，不使用 PowerShell 对象管道喂给 `getpass`。

## 格式与在线验证

格式规则只能发现明显输入错误，不能替代在线验证。具体正则和 WebSocket 验证见 `references/validation.md`。

验证顺序：

1. 检查必需字段非空和基本格式。
2. 查询应用授权，确认形象、发音人和场景属于当前应用。
3. 确认接口服务已发布。
4. 建立最小连接并等待成功事件或明确错误码。
5. 仅在在线验证成功后向下游交付凭据文件路径。

## References

- `references/app-authorization-check.md`：应用类型和能力授权检查
- `references/console-setup-guide.md`：控制台申请、创建、授权和发布
- `references/interactive-guide.md`：自动工具不可用时的交互式流程
- `references/validation.md`：格式与在线连接验证
- `references/config-templates.md`：环境变量和各端配置模板
- `references/error-codes.md`：常见凭据错误码
- `references/windows-secret-input.md`：Windows 交互式密钥输入自动化

## 验证清单

- [ ] 6 项配置齐全
- [ ] `appId`、场景和授权属于同一应用
- [ ] 接口服务已发布
- [ ] 默认或指定的形象与发音人已授权
- [ ] 在线连接验证成功
- [ ] 凭据文件已写入且被 Git 忽略
- [ ] 回复和日志未泄露完整密钥

## 交接

- 上游：`avatar-preflight`
- 下游：`avatar-artifact-download` 或具体构建流程
- 连接失败：`avatar-network-debug`
