---
name: avatar-integration-guides
description: >-
  提供讯飞虚拟人 Web、Android 和 iOS SDK 的概念索引与最小接入形态。仅用于快速理解平台结构；构建可交付工程时必须改用 avatar-executing 的真实 API playbook。
---

# avatar-integration-guides: 三端集成指南索引

## 定位

本 skill 是三端 SDK 集成的**快速理解入口**，提供每个平台的最小接入示例，帮助快速建立"这个平台大致怎么接"的认知。

> **⚠️ 生产/自建工程不以本指南为准**：真正构建可交付的 SDK 工程时，必须走
> `avatar-executing/references/*-sdk-build-playbook.md`（HARD-GATE）——那里规定了安全架构
> （后端签名、不在前端硬编码 apiSecret）、字段锁定表和关键陷阱（如 bitrate 会被 SDK /1024）。

## 分平台参考

| 平台 | 文件 | 状态 |
|------|------|------|
| Web | `web.md` | 五分钟最小示例，生产以 web-sdk-build-playbook 为准 |
| iOS | `ios.md` | 原生 iOS 集成快速指南 |
| Android | `android.md` | 已按 avatar-core-v3.2.7 真实 API 校正；完整构建流程仍以 Android playbook 为准 |

## 使用建议

- 只想快速了解某平台接入形态 → 读对应平台文件
- 要真正落地可交付工程 → 转 `avatar-executing`，按该平台的 build-playbook 执行
