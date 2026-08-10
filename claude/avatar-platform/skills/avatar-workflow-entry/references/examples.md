# 示例场景

路由决策在不同置信度下的完整示例。

## 示例 1: 故障排查（高置信度）

**用户输入**:
```
"Android 虚拟人黑屏，日志显示错误码 20002"
```

**识别结果**:
```yaml
type: troubleshooting
confidence: 0.95
evidence:
  - "黑屏" → 异常行为
  - "错误码 20002" → 明确错误码
  - "Android" → 平台明确
suggested_route: avatar-troubleshoot
```

**路由**:
```
✓ 高置信度，直接路由到 avatar-troubleshoot

执行: avatar-troubleshoot
  - 错误码 20002: 播放器创建失败
  - 原因: XRTC SDK 未引入或 ABI 不匹配
  - 修复: 检查 app/libs/ 下是否有 xrtcsdk-*.aar
```

---

## 示例 2: 配置调整（中置信度）

**用户输入**:
```
"想把虚拟人分辨率调高一点"
```

**识别结果**:
```yaml
type: config_adjustment
confidence: 0.75
evidence:
  - "分辨率调高" → 参数修改
  - 工程扫描: SDK 已集成
suggested_route: avatar-config-authoring
```

**路由**:
```
中置信度，询问确认:
  "检测到您想调整虚拟人分辨率，是否需要我帮您修改配置？"
  - 是 → avatar-config-authoring
  - 否 → 提供文档链接

用户选择: 是
执行: avatar-config-authoring
  - 当前分辨率: 720x1280
  - 建议选项: 1080x1920 / 540x960
  - 修改参数并说明影响
```

---

## 示例 3: 首次接入（低置信度）

**用户输入**:
```
"我想做一个虚拟客服"
```

**识别结果**:
```yaml
type: first_integration
confidence: 0.45
evidence:
  - 需求模糊，未明确平台
  - 工程扫描: SDK 未集成
suggested_route: avatar-brainstorming
```

**路由**:
```
低置信度，使用完整工作流:

执行: avatar-brainstorming
  Phase 1: 扫描工程（未检测到 SDK）
  Phase 2: 环境门禁（preflight）
  Phase 3: 意图分类 → 首次接入
  Phase 4: 访谈
    - 平台？Web / Android / iOS
    - 功能？文本驱动 / 语音交互
    - 效果？透明背景 / 动作控制
  Phase 5: 生成设计文档
  ...
```

---

## 示例 4: 权限问题（高置信度）

**用户输入**:
```
"iOS 麦克风录音失败，提示权限拒绝"
```

**识别结果**:
```yaml
type: permission_issue
confidence: 0.9
evidence:
  - "麦克风录音失败" → 权限相关
  - "权限拒绝" → 明确问题
  - "iOS" → 平台明确
suggested_route: avatar-permissions-setup
```

**路由**:
```
✓ 高置信度，直接路由到 avatar-permissions-setup

执行: avatar-permissions-setup
  平台: iOS
  权限类型: 麦克风
  
  检查:
    1. Info.plist 是否有 NSMicrophoneUsageDescription ❌
    2. 运行时是否申请权限 ✓
  
  修复:
    在 Info.plist 添加:
    <key>NSMicrophoneUsageDescription</key>
    <string>用于虚拟人语音交互</string>
```
