---
name: avatar-shared
description: >-
  讯飞虚拟人 Skills 的共享材料索引，包含快速/严格交付模式、测试驱动开发、并行任务分发、Android Gradle 稳定构建和分区存储适配。仅供其他 avatar-* Skill 按需引用，不作为用户任务入口。
---

# avatar-shared: 共享材料容器

## 定位

本 skill 收纳被多个其他 skill 复用的通用材料，避免重复。它不是任务入口——由 `avatar-executing`
等 skill 在需要时引用，而不是用户直接触发。

## 内容索引

| 材料 | 路径 | 用途 |
|------|------|------|
| 快速/严格交付模式 | `delivery-modes.md` | 选择少文档直做或完整三阶段评审流程 |
| 测试驱动开发 | `avatar-test-driven-development/SKILL.md` | 通用 TDD 工作方法（先写测试再实现） |
| 并行分发子 agent | `avatar-dispatching-parallel-agents/SKILL.md` | 把多个独立任务并行派发给子 agent 缩短耗时 |
| Android Gradle 稳定构建 | `android-gradle-stability.md` | 处理镜像、冷/热缓存、daemon、缓存锁、内存和超时 |
| Android 分区存储适配 | `android-scoped-storage.md` | Android 11+ (API 30) 分区存储下的日志路径配置 |

## 使用建议

- 需要并行处理多个独立任务 → 参考 `avatar-dispatching-parallel-agents`
- 首次自建或大型扩展需要控制文档、评审和 token 成本 → 参考 `delivery-modes.md`
- 涉及测试策略 → 参考 `avatar-test-driven-development`
- Android 构建、Gradle 下载或卡住 → 参考 `android-gradle-stability.md`
- Android 工程遇到 `/sdcard/` 写入受限 → 参考 `android-scoped-storage.md`
