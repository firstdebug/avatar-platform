# 路由示例

## 明确故障

“Android 虚拟人黑屏，日志有 20002”直接使用 `avatar-troubleshoot`，传入 Android、黑屏现象和日志。不要先进入需求访谈。

## 明确配置

“把现有项目分辨率调成 1080x1920”直接使用 `avatar-config-authoring` 并修改配置。不要再询问用户是否确定要修改。

## 宽泛项目

“做一个虚拟客服”只询问交付形态：官方 Web 模板、数字人直播或 SDK 自建。选择后立即路由。

## 明确 SDK 自建

“用 Android SDK 做一个支持语音交互的虚拟客服”先提供一次交付模式选择，并单独确认语音交互形态（按住说话、点击开始/停止或全双工）。两项都确认后，选快速时由 `avatar-brainstorming` 形成实施摘要后直接进入 `avatar-executing`；选严格时依次进入 `avatar-planning` 和 `avatar-executing`。

## 已有项目增加单一能力

“给这个 Web 项目加文本驱动”扫描确认已有 SDK 后使用 `avatar-text-driver`。若同时要求重构交互、知识库和 UI，则进入 `avatar-brainstorming` 并提供快速或严格模式选择。

## 外部模型与知识库

“用 DeepSeek 和讯飞知识库做 Android 虚拟人”读取 `external-llm-knowledge-base.md`，再从 `avatar-brainstorming` 开始；必须先问快速或严格。用户选快速时不生成设计/计划文档或调用 writer-reviewer，但资源验证、Playbook 和真机验证仍执行。未确认语音时不加入麦克风权限或录音代码。
