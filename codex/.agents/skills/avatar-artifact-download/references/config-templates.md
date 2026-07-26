# SDK 下载配置

## OSS 固定链接（腾讯云，无过期时间）

```yaml
SDK_URLS:
  web:
    version: "3.2.3.1002"
    filename: "avatar-web-sdk.zip"
    url: "https://sdksave-1317537578.cos.ap-guangzhou.myqcloud.com/avatar-web-sdk.zip"
    size: "~5MB"
    verify_file: "index.js"
    
  android:
    version: "3.2.7"
    filename: "avatar-android-sdk.zip"
    url: "https://sdksave-1317537578.cos.ap-guangzhou.myqcloud.com/avatar-android-sdk.zip"
    size: "~15MB"
    verify_files: ["avatar-core-*.aar", "xrtcsdk-*.aar"]
    
  ios:
    version: "3.2.1"
    filename: "avatar-ios-sdk.zip"
    url: "https://sdksave-1317537578.cos.ap-guangzhou.myqcloud.com/avatar-ios-sdk.zip"
    size: "~20MB"
    verify_file: "AvatarSDK.framework"
```

✅ **所有链接均为固定 OSS 链接，无过期时间，无需定期更新**

---

## 官网手动下载文档（OSS 失败时提供）

```yaml
MANUAL_DOWNLOAD_DOCS:
  web:
    url: "https://www.yuque.com/xnrpt/bbc1du/ht4a2a2vstvb13se"
    title: "Web SDK 集成文档"
    
  android:
    url: "https://www.yuque.com/xnrpt/bbc1du/nvg8cabgl4ycqvtv"
    title: "Android SDK 集成文档"
    
  ios:
    url: "https://www.yuque.com/xnrpt/bbc1du/cwqfpgdg80wfdx3u"
    title: "iOS SDK 集成文档"
```

**说明**：
- OSS 链接优先使用，速度快且稳定
- OSS 下载失败时，**不自动解析文档页面**
- 而是引导用户打开文档链接，手动下载 SDK
- 文档页面包含最新 SDK 下载链接，需人工操作

---

## 目标路径规范

### Web SDK
```
项目根目录/
└── sdk/
    └── （解压后的 SDK 文件）
        ├── index.js
        ├── index.d.ts
        └── ...
```

### Android SDK
```
项目根目录/
└── app/
    └── libs/
        ├── avatar-core-v3.2.7.aar
        └── xrtcsdk-5.2024.3.0.aar
```

### iOS SDK
```
项目根目录/
└── Frameworks/
    ├── AvatarSDK.framework/
    └── XRTCSDK.framework/
```

---

## 验证文件规则

下载完成后，验证以下关键文件是否存在：

**Web**: 
- `**/index.js` 存在

**Android**:
- `**/avatar-core-*.aar` 存在
- `**/xrtcsdk-*.aar` 存在

**iOS**:
- `**/AvatarSDK.framework` 存在

验证失败视为下载不完整，需重新下载或手动下载。
