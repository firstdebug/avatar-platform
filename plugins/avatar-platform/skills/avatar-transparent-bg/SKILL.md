---
name: avatar-transparent-bg
description: 配置讯飞虚拟人的透明背景、Alpha 渲染和自定义背景叠加。用于抠像、透明视频、Canvas 合成或解决透明区域显示异常时。
---

# avatar-transparent-bg: 透明背景配置

## 功能说明

虚拟人背景透明，可叠加到其他内容上，适用于直播、视频合成等场景。

**重要**: 仅 **XRTC 协议** + **标准虚拟人**支持透明背景，超拟人形象不支持。

---

## 快速配置

### Web
```javascript
// 1. 全局参数配置透明背景（完整结构）
avatar.setGlobalParams({
  stream: { 
    protocol: 'xrtc',  // 必须使用 XRTC
    fps: 25,
    bitrate: 2000,
    alpha: 1           // 1=透明背景, 0=普通背景
  },
  avatar: {
    avatar_id: 'your_avatar_id',
    width: 720,
    height: 1280,
    stream: {
      protocol: 'xrtc',  // 必填
      fps: 25,           // 必填
      bitrate: 2000,     // 必填
      alpha: 1           // 必填，透明背景
    }
  },
  tts: {
    vcn: 'your_vcn',
    speed: 50,
    pitch: 50,
    volume: 50
  }
});

// 2. 播放器配置透明
const player = avatar.player;
player.alpha = true;  // 启用透明渲染

// 3. 容器样式（可选）
// 如需叠加到其他内容上
const container = document.querySelector('.avatar-container');
container.style.backgroundColor = 'transparent';
```

### Android
```java
// 1. 全局参数配置
AvatarParams.Stream stream = new AvatarParams.Stream();
stream.setProtocol("xrtc");  // 必须 XRTC
stream.setAlpha(1);           // 透明背景

AvatarParams.Avatar avatar = new AvatarParams.Avatar();
avatar.setStream(stream);
// ... 其他配置

AvatarParams params = new AvatarParams();
params.setAvatar(avatar);
controller.setGlobalParams(params);

// 2. 播放器配置
StreamPlayerParams playerParams = new StreamPlayerParams();
playerParams.setBgAlpha(true);  // 启用透明
playerParams.setAlphaRenderMode(AlphaRenderMode.V2);  // 推荐 V2 模式
streamPlayer.setPlayerParams(playerParams);
```

### iOS
```objc
// 1. 全局参数配置
AvatarParamsStream *stream = [AvatarParamsStream new];
stream.protocol(@"xrtc").alpha(YES);  // 透明背景

AvatarParamsAvatar *avatar = [AvatarParamsAvatar new];
avatar.stream(stream);
// ... 其他配置

AvatarParams *params = [AvatarParams new];
params.avatar(avatar);
controller.globalParams = params;

// 2. 播放器配置
StreamPlayerParams *playerParams = [StreamPlayerParams new];
playerParams.alpha(YES);  // 启用透明
player.playerParams = playerParams;
```

---

## 注意事项

### 1. 协议要求

**必须使用 XRTC**:
```javascript
// ❌ 错误: WebRTC 不支持透明背景
stream.protocol = 'webrtc';
stream.alpha = 1;  // 无效

// ✓ 正确
stream.protocol = 'xrtc';
stream.alpha = 1;
```

### 2. 形象要求

**标准虚拟人支持，超拟人不支持**:
```javascript
// 检查形象类型
if (avatarId.startsWith('cnr')) {
  console.warn('超拟人形象不支持透明背景');
}
```

### 3. 双重配置

**必须同时配置 stream 和 player**:
```javascript
// ❌ 错误: 只配置了一处
stream.alpha = 1;
// 忘记配置 player.alpha

// ✓ 正确: 两处都配置
stream.alpha = 1;
player.alpha = true;
```

### 4. Android 渲染模式

推荐使用 `AlphaRenderMode.V2`:
```java
playerParams.setAlphaRenderMode(AlphaRenderMode.V2);  // 推荐
// V1 模式可能有兼容性问题
```

---

## 效果验证

### 检查方法

**Web**:
```javascript
// 检查视频元素背景
const videoEl = document.querySelector('video');
console.log('背景色:', window.getComputedStyle(videoEl).backgroundColor);
// 应为 transparent 或 rgba(0,0,0,0)
```

**Android**:
```java
// 检查播放器参数
if (playerParams.isBgAlpha()) {
    Log.d(TAG, "透明背景已启用");
}
```

**目视检查**:
- 虚拟人周围无绿幕或纯色背景
- 可以看到虚拟人后面的内容
- 边缘无明显色块

---

## 常见问题

### 1. 配置了透明背景但无效

**检查清单**:
- [ ] 协议是否为 `xrtc`
- [ ] `stream.alpha` 是否为 1
- [ ] `player.alpha` 是否为 true
- [ ] 形象是否为标准虚拟人（非超拟人）

### 2. 边缘有白边或黑边

**原因**: 渲染模式问题（Android）
**解决**: 使用 `AlphaRenderMode.V2`

### 3. 透明度不完全

**原因**: alpha 通道数据丢失
**解决**: 
- 检查网络质量
- 检查播放器参数
- 确认 SDK 版本是否支持

---

## 应用场景

### 1. 视频叠加

```html
<!-- Web: 叠加到视频上 -->
<div style="position: relative;">
  <video src="background.mp4"></video>
  <div class="avatar-container" style="position: absolute; top: 0; left: 0;"></div>
</div>
```

### 2. 直播推流

透明背景的虚拟人可以通过 OBS 等工具推流到直播平台。

### 3. 画中画效果

```css
.avatar-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 200px;
  height: 300px;
}
```

---

## 相关技能

- `avatar-brainstorming`: 在访谈时会询问是否需要透明背景
- `avatar-troubleshoot`: 透明背景问题排查
