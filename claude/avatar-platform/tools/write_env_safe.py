#!/usr/bin/env python3
"""
安全写入 .env 文件工具
从平台 API 获取完整凭据并写入指定路径的 .env，密钥不打印到控制台
"""
import sys
import json
from pathlib import Path
from xfyun_common import get_session

def write_env(app_id, scene_id, output_path):
    """获取完整凭据并写入 .env"""
    print(f"[查询] 应用 {app_id} 的完整凭据...")

    # 获取已登录的会话
    session = get_session()
    if not session:
        print("[错误] 无法获取登录会话")
        return False

    payload = {"current": 1, "size": 100, "appId": app_id}
    resp = session.post(
        "https://virtual-man.xfyun.cn/zs_web/app/query",
        json=payload,
        timeout=30
    )

    if resp.status_code != 200:
        print(f"[错误] HTTP {resp.status_code}")
        return False

    data = resp.json()
    if not data.get("flag") or not data.get("data", {}).get("records"):
        print("[错误] 查询失败或无应用记录")
        return False

    record = data["data"]["records"][0]
    api_key = record["apiKey"]
    api_secret = record["apiSecret"]

    # 脱敏显示确认
    print(f"[OK] API Key:    {api_key[:4]}{'*'*8}{api_key[-4:]}")
    print(f"[OK] API Secret: {api_secret[:4]}{'*'*8}{api_secret[-4:]}")

    # 写入 .env
    output_file = Path(output_path)
    env_content = f"""# 讯飞虚拟人 WebAPI 凭据
# 自动生成，请勿提交到版本库

XF_APP_ID={app_id}
XF_API_KEY={api_key}
XF_API_SECRET={api_secret}
XF_SCENE_ID={scene_id}
XF_AVATAR_ID=111310001
XF_VCN=x4_lingxiaoqi_oral
"""

    output_file.write_text(env_content, encoding='utf-8')
    print(f"\n[完成] 凭据已写入: {output_file}")
    print(f"[安全] 密钥未打印到控制台，仅存储在本地文件")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python write_env_safe.py <app_id> <scene_id> <output_path>")
        print("示例: python write_env_safe.py YOUR_APP_ID 336130030977552384 ~/.env")
        sys.exit(1)

    app_id = sys.argv[1]
    scene_id = sys.argv[2]
    output_path = sys.argv[3]

    if write_env(app_id, scene_id, output_path):
        sys.exit(0)
    else:
        sys.exit(1)
