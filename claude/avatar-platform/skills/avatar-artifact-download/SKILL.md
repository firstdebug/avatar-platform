---
name: avatar-artifact-download
description: 自动下载虚拟人 SDK（优先 OSS，失败时引导手动下载）
tags:
  - download
  - sdk
  - artifact
priority: high
---

# avatar-artifact-download: SDK 下载

## 定位

自动从腾讯云 OSS 下载虚拟人 SDK，失败时引导用户从官网手动下载。

**调用时机**:
- `avatar-preflight` Layer 1/3 检测到 SDK 缺失时（Tier 1 自动处理）
- 用户主动请求下载 SDK

---

## 核心工作流

下载分三个阶段：

| Phase | 步骤 | 说明 |
|-------|------|------|
| 1 | 检测 SDK 状态 | 检查目标目录是否已有 SDK 文件（.aar / .framework / index.js），存在则跳过 |
| 2 | OSS 自动下载 | 使用腾讯云 OSS 固定链接下载并解压，验证关键文件 |
| 3 | 失败时引导手动下载 | OSS 下载失败时，给用户官网文档链接，说明手动下载步骤 |

**不自动解析文档页面**：官网文档需要人工下载，无法自动获取链接。

---

## SDK 下载配置

### OSS 固定链接（腾讯云，无过期时间）

```yaml
SDK_URLS:
  web:
    version: "3.2.3.1002"
    filename: "avatar-web-sdk.zip"
    url: "https://sdksave-1317537578.cos.ap-guangzhou.myqcloud.com/avatar-web-sdk.zip"
    size: "~5MB"
    verify_file: "index.js"  # 验证文件存在
    
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

### 官网手动下载文档（OSS 失败时提供）

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

**说明**：这些文档页面包含 SDK 下载链接，需用户手动点击下载。

---

## Phase 1: 检测 SDK 状态

### Web SDK 检测

```python
def check_web_sdk(project_path):
    """检测 Web SDK 是否已存在"""
    # 检查常见位置
    search_paths = [
        f"{project_path}/sdk/**/index.js",
        f"{project_path}/node_modules/@xfyun/avatar-sdk/index.js",
        f"{project_path}/public/sdk/**/index.js"
    ]
    
    for pattern in search_paths:
        files = glob(pattern, recursive=True)
        if files:
            return {
                "exists": True,
                "path": os.path.dirname(files[0]),
                "version": extract_version_from_file(files[0])
            }
    
    return {"exists": False}
```

### Android SDK 检测

```python
def check_android_sdk(project_path):
    """检测 Android SDK 是否已存在"""
    libs_path = f"{project_path}/app/libs"
    
    # 检查必需的 aar 文件
    avatar_core = glob(f"{libs_path}/avatar-core-*.aar")
    xrtcsdk = glob(f"{libs_path}/xrtcsdk-*.aar")
    
    if avatar_core and xrtcsdk:
        return {
            "exists": True,
            "path": libs_path,
            "files": {
                "avatar_core": os.path.basename(avatar_core[0]),
                "xrtcsdk": os.path.basename(xrtcsdk[0])
            }
        }
    
    return {"exists": False}
```

### iOS SDK 检测

```python
def check_ios_sdk(project_path):
    """检测 iOS SDK 是否已存在"""
    search_paths = [
        f"{project_path}/Frameworks/AvatarSDK.framework",
        f"{project_path}/Pods/AvatarSDK/AvatarSDK.framework"
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return {
                "exists": True,
                "path": os.path.dirname(path)
            }
    
    return {"exists": False}
```

---

## Phase 2: OSS 自动下载

### 通用下载函数

```python
def download_sdk_from_oss(platform, target_dir):
    """
    从腾讯云 OSS 下载 SDK
    
    Args:
        platform: "web" / "android" / "ios"
        target_dir: 目标解压目录
    
    Returns:
        {"status": "success", "path": "...", "version": "..."}
        或
        {"status": "failed", "reason": "..."}
    """
    config = SDK_URLS[platform]
    temp_file = f"/tmp/{config['filename']}"
    
    print(f"📥 正在从 OSS 下载 {platform.upper()} SDK...")
    print(f"版本: {config['version']}")
    print(f"大小: {config['size']}")
    print("")
    
    # 下载
    try:
        response = requests.get(config['url'], stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        with open(temp_file, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                # 显示进度
                percent = int(downloaded / total_size * 100) if total_size else 0
                print(f"\r下载进度: {percent}%", end='', flush=True)
        
        print("\n✅ 下载完成\n")
    
    except requests.exceptions.RequestException as e:
        return {
            "status": "failed",
            "reason": f"OSS 下载失败: {str(e)}",
            "error_type": "network"
        }
    
    # 解压
    print("📦 正在解压 SDK...")
    try:
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print("✅ 解压完成\n")
    except Exception as e:
        return {
            "status": "failed",
            "reason": f"解压失败: {str(e)}",
            "error_type": "extraction"
        }
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # 验证
    print("🔍 验证 SDK 完整性...")
    verify_result = verify_sdk_files(platform, target_dir, config)
    
    if verify_result["valid"]:
        print("✅ SDK 验证通过\n")
        return {
            "status": "success",
            "path": verify_result["sdk_path"],
            "version": config["version"]
        }
    else:
        return {
            "status": "failed",
            "reason": f"SDK 验证失败: {verify_result['reason']}",
            "error_type": "verification"
        }
```

### SDK 文件验证

```python
def verify_sdk_files(platform, target_dir, config):
    """验证 SDK 关键文件是否存在"""
    
    if platform == "web":
        # 查找 index.js
        index_files = glob(f"{target_dir}/**/index.js", recursive=True)
        if index_files:
            return {"valid": True, "sdk_path": os.path.dirname(index_files[0])}
        return {"valid": False, "reason": "未找到 index.js"}
    
    elif platform == "android":
        # 查找 aar 文件
        avatar_core = glob(f"{target_dir}/**/avatar-core-*.aar", recursive=True)
        xrtcsdk = glob(f"{target_dir}/**/xrtcsdk-*.aar", recursive=True)
        
        if avatar_core and xrtcsdk:
            return {"valid": True, "sdk_path": target_dir}
        
        missing = []
        if not avatar_core:
            missing.append("avatar-core-*.aar")
        if not xrtcsdk:
            missing.append("xrtcsdk-*.aar")
        return {"valid": False, "reason": f"缺少文件: {', '.join(missing)}"}
    
    elif platform == "ios":
        # 查找 framework
        framework = glob(f"{target_dir}/**/AvatarSDK.framework", recursive=True)
        if framework:
            return {"valid": True, "sdk_path": os.path.dirname(framework[0])}
        return {"valid": False, "reason": "未找到 AvatarSDK.framework"}
    
    return {"valid": False, "reason": "未知平台"}
```

---

## Phase 3: 失败时引导手动下载

当 OSS 下载失败时，**不尝试自动解析文档页面**，而是给用户清晰的手动下载指引。

### 失败处理函数

```python
def handle_download_failure(platform, error_result):
    """OSS 下载失败时的处理"""
    
    print("❌ OSS 自动下载失败\n")
    print(f"失败原因: {error_result['reason']}\n")
    
    # 根据错误类型给诊断建议
    if error_result.get("error_type") == "network":
        print("💡 可能原因:")
        print("   - 网络连接问题")
        print("   - 防火墙或代理拦截腾讯云 OSS")
        print("   - DNS 解析失败\n")
        print("💡 排查步骤:")
        print("   1. 检查网络连接")
        print("   2. 尝试浏览器访问: https://sdksave-1317537578.cos.ap-guangzhou.myqcloud.com/")
        print("   3. 检查防火墙/代理设置\n")
    
    # 给手动下载指引
    doc_config = MANUAL_DOWNLOAD_DOCS[platform]
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  请手动下载 SDK                                           ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    print(f"📖 官方集成文档: {doc_config['title']}")
    print(f"🔗 链接: {doc_config['url']}\n")
    
    print("📝 手动下载步骤:")
    print("   1. 打开上面的文档链接")
    print("   2. 在文档中找到「SDK 下载」章节")
    print("   3. 点击下载链接，保存 SDK 压缩包")
    
    if platform == "web":
        print("   4. 解压到项目的 sdk/ 目录")
        print("   5. 确保 sdk/ 目录下有 index.js 文件\n")
    elif platform == "android":
        print("   4. 解压后，将 .aar 文件复制到 app/libs/ 目录")
        print("   5. 应该包含：avatar-core-*.aar 和 xrtcsdk-*.aar\n")
    elif platform == "ios":
        print("   4. 解压后，将 .framework 文件复制到 Frameworks/ 目录")
        print("   5. 在 Xcode 中添加 Framework 依赖\n")
    
    print("完成后，回来告诉我「SDK 已下载」，我会继续后续步骤。\n")
    
    return {
        "status": "manual_download_required",
        "doc_url": doc_config["url"],
        "instructions": "用户需手动从文档页面下载 SDK"
    }
```

---

## 完整执行流程

```python
def execute_sdk_download(platform, project_path):
    """
    执行 SDK 下载流程
    
    Args:
        platform: "web" / "android" / "ios"
        project_path: 项目根目录
    
    Returns:
        下载结果（成功、失败、需手动下载）
    """
    
    print(f"╔════════════════════════════════════════════════════════════╗")
    print(f"║  {platform.upper()} SDK 下载                                    ║")
    print(f"╚════════════════════════════════════════════════════════════╝\n")
    
    # Phase 1: 检测 SDK 是否已存在
    print("🔍 检测 SDK 状态...")
    
    if platform == "web":
        check_result = check_web_sdk(project_path)
        target_dir = f"{project_path}/sdk"
    elif platform == "android":
        check_result = check_android_sdk(project_path)
        target_dir = f"{project_path}/app/libs"
    elif platform == "ios":
        check_result = check_ios_sdk(project_path)
        target_dir = f"{project_path}/Frameworks"
    else:
        return {"status": "error", "reason": f"不支持的平台: {platform}"}
    
    if check_result["exists"]:
        print(f"✅ SDK 已存在")
        print(f"路径: {check_result['path']}\n")
        return {
            "status": "already_exists",
            "path": check_result["path"]
        }
    
    print("SDK 不存在，开始下载...\n")
    
    # Phase 2: 从 OSS 下载
    download_result = download_sdk_from_oss(platform, target_dir)
    
    if download_result["status"] == "success":
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  ✅ SDK 下载完成！                                        ║")
        print("╚════════════════════════════════════════════════════════════╝\n")
        print(f"SDK 路径: {download_result['path']}")
        print(f"版本: {download_result['version']}\n")
        return download_result
    
    # Phase 3: 失败时引导手动下载
    return handle_download_failure(platform, download_result)
```

---

## 输出格式

### 成功下载
```yaml
status: "success"
platform: "android"
path: "./app/libs"
version: "3.2.7"
source: "oss"
```

### 已存在，跳过
```yaml
status: "already_exists"
platform: "web"
path: "./sdk/avatar-sdk-web"
```

### 需要手动下载
```yaml
status: "manual_download_required"
platform: "ios"
doc_url: "https://www.yuque.com/xnrpt/bbc1du/cwqfpgdg80wfdx3u"
instructions: "用户需从文档页面手动下载 SDK"
reason: "OSS 下载失败: 网络超时"
```

---

## 验证清单

- [ ] Phase 1 检测 SDK 是否已存在（避免重复下载）
- [ ] Phase 2 从 OSS 下载并验证关键文件
- [ ] Phase 3 失败时给出清晰的手动下载指引（不自动解析文档）
- [ ] 支持 Web / Android / iOS 三个平台
- [ ] 网络错误时提供诊断建议

---

## 相关 Skills

- `avatar-preflight`: 在 Layer 1（Tier 1）调用本 skill 自动下载 SDK
- `avatar-credentials`: 凭据获取和验证
