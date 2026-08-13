# Android SDK 五分钟速览

本页只帮助快速理解 Android 接入结构。构建可交付工程时，必须读取
`skills/avatar-executing/references/android-sdk-build-playbook.md`，并以实际 AAR 的签名为最终依据。

## 接入前提

- Android SDK 产物：`avatar-core-*.aar` 与 `xrtcsdk-*.aar`
- 凭据：`appId`、`apiKey`、`apiSecret`、已发布的 `sceneId`
- 默认形象：`111310001`
- 默认发音人：`x4_lingxiaoqi_oral`
- 最低系统版本、JDK、AGP 和 Gradle 组合以 Android Playbook 的版本矩阵为准

SDK 缺失时使用 `avatar-artifact-download`；凭据缺失时使用 `avatar-credentials`。

## 最小结构

Android 接入由五部分组成：

1. 用 `AvatarPlatformConfig.Builder` 配置凭据、服务地址和日志。
2. 用三参数 `AvatarPlatform.initialize(context, config, listener)` 初始化。
3. 从 `AvatarPlatform.getController()` 获取 `AvatarPlayController`。
4. 创建 XRTC 播放器、设置渲染容器，并交给 controller。
5. 设置全局参数、注册 `IAvatarListener`，然后启动并发送交互指令。

## 真实 API 主链

下面只保留签名级速览，不作为完整工程模板：

```java
AvatarPlatform.initialize(getApplicationContext(), config, (code, msg) -> {
    if ("0".equals(code)) {
        controller = AvatarPlatform.getController();
    }
});
```

```java
IStreamPlayer player = StreamPlayerFactory.createPlayer(this, AvatarConstant.STREAM_XRTC);
player.setRenderArea(videoContainer);
controller.setStreamPlayer(player);
```

全局参数至少包含：

- `AvatarParams.Avatar`：形象、尺寸，并通过 `avatar.setStream(stream)` 绑定流参数
- `AvatarParams.Stream`：`xrtc`、帧率、码率、透明背景标记
- `AvatarParams.TTS`：发音人、语速、音调、音量
- `AvatarParams.Scene`：已发布的 `sceneId`
- `AvatarParams.Dispatch`：追加或打断模式

首次接入先使用默认形象和发音人。只有平台明确返回未授权，或用户要求更换时，才探测当前应用可用资产。

## 常用入口

| 能力 | 真实入口 |
|---|---|
| 纯文本播报 | `controller.writeText(text)` |
| 文本 NLP 交互 | `controller.writeText(text, textParams)`，且 `textParams.setNlp(true)` |
| 语音交互 | `controller.setAudioRecorder(recorder, audioParams)` |
| 事件结果 | `IAvatarListener.onResult/onEvent/onError` |
| 渲染挂载 | `player.setRenderArea(videoContainer)` |
| 释放资源 | 先停录音和播放，再 `controller.stop()`、`controller.destroy()` |

NLP 和 ASR 文本从 `IAvatarListener.onResult` 的 `extra` JSON 中解析，不假设存在额外的简化回调。

## 基础权限

`AndroidManifest.xml` 至少声明：

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
```

`RECORD_AUDIO` 和 Android 12+ 的 `BLUETOOTH_CONNECT` 需要运行时申请。只做文本播报时，可按实际功能裁剪麦克风相关权限。

## 快速检查

- 初始化回调成功码为字符串 `"0"`
- 播放器已调用 `setRenderArea`，且容器可见并有尺寸
- `avatar.stream`、TTS、scene 和 dispatch 均已设置
- `sceneId` 已发布，形象和发音人已授权
- 生命周期结束时先停止录音，再释放 controller 和播放器

## 权威边界

本页不维护以下内容，避免与构建 Playbook 漂移：

- 完整 API 表与 MainActivity 模板
- Gradle、AGP、JDK 版本矩阵和性能参数
- AAR、`.so` 冲突与打包规则
- 六步构建流程和真机验收
- 历史错误 API 黑名单

这些内容统一读取 `skills/avatar-executing/references/android-sdk-build-playbook.md`。若指南、模型记忆与 AAR 不一致，以当前项目实际 SDK 产物为准。

## 相关 Skill

- `avatar-executing`：构建完整 Android 工程
- `avatar-artifact-download`：获取并校验 AAR
- `avatar-permissions-setup`：处理录音和相机权限
- `avatar-troubleshoot`：排查黑屏、连接和错误码
