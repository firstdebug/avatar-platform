# 路由规则表（完整）

完整的关键词 / 指标 / 路由目标映射规则。

```yaml
故障排查:
  keywords:
    - "失败" / "报错" / "不工作" / "黑屏"
    - "错误码" / "error" / "异常"
    - "为什么..." / "怎么回事"
  indicators:
    - 提供了错误码
    - 提供了日志片段
    - 描述了异常行为
  route_to: avatar-troubleshoot
  priority: highest

配置调整:
  keywords:
    - "调整" / "修改" / "更换" / "优化"
    - "分辨率" / "码率" / "帧率"
    - "形象" / "声音" / "参数"
  indicators:
    - SDK 已集成
    - 基础功能已工作
    - 只涉及参数修改
  route_to: avatar-config-authoring
  priority: high

首次接入:
  keywords:
    - "集成" / "接入" / "从零" / "新项目"
    - "如何开始" / "怎么用"
  indicators:
    - SDK 未集成
    - 工程中无虚拟人相关代码
  route_to: avatar-brainstorming
  priority: medium

功能扩展:
  keywords:
    - "添加" / "新增" / "扩展"
    - "语音交互" / "动作控制" / "透明背景"
  indicators:
    - SDK 已集成
    - 部分功能已实现
    - 需要添加新功能
  route_to: avatar-brainstorming
  priority: medium

文档查询:
  keywords:
    - "如何..." / "怎么..." / "能不能"
    - "文档" / "教程" / "示例"
  indicators:
    - 无明确实施意图
    - 仅需信息不需实现
  route_to: provide_docs
  priority: low

权限问题:
  keywords:
    - "权限" / "拒绝" / "无法录音"
    - "麦克风" / "摄像头"
  indicators:
    - 权限相关错误
  route_to: avatar-permissions-setup
  priority: high

网络问题:
  keywords:
    - "连接" / "超时" / "断开"
    - "10200" / "10201" / "网络"
  indicators:
    - 网络相关错误码
  route_to: avatar-network-debug
  priority: high

知识库管理:
  keywords:
    - "知识库" / "docqa" / "RAG"
    - "上传文档" / "知识问答" / "文档检索"
    - "向量化" / "检索增强"
  indicators:
    - 明确提到操作知识库（创建/上传/关联）
    - 已有知识库需配置到场景
  route_to: avatar-knowledge-base
  priority: high
```
