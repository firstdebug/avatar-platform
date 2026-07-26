#!/usr/bin/env python3
"""
UserPromptSubmit hook: 检测虚拟人相关需求，注入路由提示让模型先走 avatar-workflow-entry
"""
import sys
import os
from datetime import datetime

# 虚拟人相关关键词（中英文）
AVATAR_KEYWORDS = [
    # 中文
    "虚拟人", "数字人", "讯飞", "xfyun", "avatar", "智能客服", "直播",
    "语音交互", "文本驱动", "音频驱动", "动作控制", "形象", "发音人",
    "场景", "模型配置", "知识库", "appId", "appSecret", "anchorId", "vcn",
    "Web对话", "H5通话", "大屏交互", "透明背景", "字幕", "全双工",
    # 英文/拼音
    "virtual human", "digital human", "avatar sdk", "web template",
    "live streaming", "voice interact", "text driver", "audio driver",
]

def main():
    # 从 stdin 读取用户输入
    user_prompt = sys.stdin.read().strip()

    # 调试日志
    log_file = os.path.join(os.environ.get('TEMP', '/tmp'), 'avatar_hook_debug.log')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.now()}] Hook triggered\n")
        f.write(f"Input: {user_prompt[:100]}\n")

    # 检测是否包含虚拟人关键词
    prompt_lower = user_prompt.lower()
    is_avatar_related = any(kw.lower() in prompt_lower for kw in AVATAR_KEYWORDS)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Avatar related: {is_avatar_related}\n")

    if is_avatar_related:
        # 注入路由提示到 additionalContext（hook 输出到 stdout 会被注入）
        hint = """
<avatar-routing-hint>
检测到虚拟人/数字人相关需求。请优先使用 avatar-workflow-entry 技能进行智能路由，
而不是直接调用子技能（avatar-web-template / avatar-credentials 等）。
avatar-workflow-entry 会根据意图分析、置信度评估，引导到最合适的执行路径。
</avatar-routing-hint>
""".strip()
        print(hint, file=sys.stdout)
        sys.stdout.flush()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("Output: routing hint sent\n")

    sys.exit(0)

if __name__ == "__main__":
    main()
