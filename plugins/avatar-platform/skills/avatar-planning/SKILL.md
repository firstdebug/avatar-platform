---
name: avatar-planning
description: 将已确认的讯飞虚拟人设计规格转换为可执行实施计划。仅用于用户选择严格三阶段、需要完整计划文档和 plan-reviewer 的场景；快速交付模式直接跳过本 Skill。
---

# avatar-planning: 严格模式计划

## 模式门禁

先读 `../avatar-shared/delivery-modes.md`。

- `workflow_mode=quick`：不要读取计划模板，不创建计划文档，不调用 plan-writer/plan-reviewer；把实施摘要直接交给 `avatar-executing`。
- `workflow_mode=strict`：继续本流程。

## 输入与输出

输入：已确认设计规格、平台、实施类型和 `workflow_mode=strict`。  
输出：`implementation-plan.md` 和 `avatar-executing` 所需上下文。

## 严格流程

1. 按 `references/design-parsing.md` 提取实施范围和依赖。
2. 调用 `plan-writer`，按 `references/plan-document-template.md` 生成计划。
3. 按 `references/review-and-output.md` 执行一次 `plan-reviewer` 阻塞性评审；只有发现阻塞问题时再修订，最多 2 轮。
4. 展示简短摘要并取得用户确认，进入 `avatar-executing`。

计划按范围控制长度：首次接入 6-10 步、功能扩展 3-5 步、配置调整 1-2 步。每步只保留目标、文件、验证和必要回滚，不在计划中复制平台 Playbook 或大段代码。

## 共同门禁

- apiSecret 不进入计划、源码或版本库。
- avatarId/vcn/sceneId 已验证，不使用示例值代替平台结果。
- 只有目标功能需要录音时才规划麦克风权限。
- 平台真实 API 由 `avatar-executing` Playbook 提供，计划只引用路径。

## References

- `../avatar-shared/delivery-modes.md`：模式门禁
- `references/design-parsing.md`：设计信息提取和范围识别
- `references/plan-document-template.md`：严格模式计划模板
- `references/review-and-output.md`：严格模式评审和确认

## 交接

```yaml
status: completed
workflow_mode: strict
plan_path: ./avatar-implementation-plan.md
next_step: avatar-executing
```

必须调用 `avatar-executing` 读取真实 Playbook；这里的“跳过 planning”仅指快速模式不生成计划文档，不允许跳过实际实现门禁。
