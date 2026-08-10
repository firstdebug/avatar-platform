---
name: avatar-verification
description: 项目交付前的完整验证流程。自动检测并修复常见问题，确保项目开箱即用。
tags:
  - verification
  - validation
  - quality-assurance
priority: critical
optional_tools:
  - name: query-scene-config
    when: Layer 2 凭据验证——确认 sceneId 真的已发布且具备对话能力
    fallback: 仅做本地格式校验，提醒用户手动确认控制台已发布
---

# avatar-verification: 交付前验证

## 定位

在项目交付给用户前，自动执行完整的验证流程，检测并修复常见问题，确保用户拿到的是**开箱即用**的项目。

**调用时机**:
- 项目代码生成完成后
- 凭据配置完成后
- SDK 下载完成后
- 启动服务器之前（HARD-GATE）

---

## 关键约束

- **HARD-GATE**: 启动服务器之前必须通过验证，只有验证通过（`ready_to_deliver: true`）才交付给用户。
- Critical 问题未修复 → 禁止交付。
- 能自动修复的问题优先自动修复；无法自动修复的问题必须列入 `remaining_issues` 并回退到 `avatar-troubleshoot`。

### Red Flags（最常见的交付前问题）

- `bitrate < 200` → SDK 报错 `value must be larger or equal than 200`，修复为 2000
- SDK 路径错误 → SDK 加载失败，需匹配实际下载目录
- 凭据未用 `import.meta.env.VITE_*` 加载
- 缺少关键事件监听（connected / error / disconnected）
- SDK 未下载 / node_modules 未安装

---

## 核心工作流概览

按顺序执行 7 层验证，每层失败记录 issue，最后统一汇总并尝试自动修复。

| Layer | 名称 | 检查内容 |
|-------|------|----------|
| 1 | 文件完整性 | 所有必需文件存在且内容完整 |
| 2 | 凭据验证 | `.env` 存在、格式正确、值非空 |
| 3 | SDK 验证 | SDK 已下载、路径正确、关键文件存在 |
| 4 | 依赖验证 | `node_modules` 存在、`package.json` 正确 |
| 5 | 配置参数验证（关键） | 检查并修复已知错误配置 |
| 6 | 编译验证 | 代码语法正确、无明显错误 |
| 7 | 运行时验证 | 启动开发服务器、检查报错 |

---

## 工具增强（Layer 2 发布状态确认）

`.env` 格式正确≠凭据可用——**sceneId 未发布**是头号交付后连接失败原因（10121 /
`authentication failed`）。本地校验查不出，但若用户提供了 `xfyun-tools`，可主动确认：

```bash
if [ -f tools/xfyun_model_manage.py ]; then
    # 查询场景真实配置：是否已发布、是否具备对话能力
    python tools/xfyun_model_manage.py query <sceneId>
    # → 未发布则 Layer 2 记为 Critical issue，交接 avatar-model-config publish 修复
fi
```

**Fallback**: 无工具时，Layer 2 只做本地格式校验，并在报告中**明确提醒**用户手动确认
控制台已点击"发布"。

---

## 决策分支（场景 → 应读哪个 reference）

- **Layer 5 配置参数验证 / 已知配置陷阱（bitrate、SDK 路径、凭据加载、事件监听）的检测与自动修复代码** → 详见 `references/config-checks.md`
- **完整验证流程实现（`verifyProject()` 全量代码，含 7 层逻辑与自动修复汇总）** → 详见 `references/verify-workflow.md`
- **集成到 avatar-executing 工作流、验证报告格式、输出结构（passed / failed）** → 详见 `references/integration-output.md`

---

## references/ 索引

| 文件 | 内容 |
|------|------|
| `references/config-checks.md` | Layer 5 已知配置陷阱：bitrate、SDK 路径、凭据加载、事件监听的检测函数与自动修复函数 |
| `references/verify-workflow.md` | `verifyProject()` 完整实现：7 层验证流程、问题分级、自动修复汇总 |
| `references/integration-output.md` | 集成到 avatar-executing（Step 8-10）、验证报告格式、输出 YAML 结构 |

---

## 验证清单 / 交接协议

交付前必须确认:
- [ ] Layer 1-7 全部通过（或已自动修复）
- [ ] 无未修复的 Critical 问题
- [ ] `ready_to_deliver: true`

交接:
- 验证通过 → 交付给用户（开箱即用）
- 验证失败且无法自动修复 → 调用 `avatar-troubleshoot` 处理 `remaining_issues`

---

## 相关技能

- `avatar-executing`: 执行后调用本技能
- `avatar-troubleshoot`: 如果验证失败，调用故障排查
- `avatar-code-reviewer` (agent): 代码审查后验证配置
