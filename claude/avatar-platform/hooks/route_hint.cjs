#!/usr/bin/env node
/**
 * UserPromptSubmit hook: 检测虚拟人相关需求，注入路由提示让模型先走 avatar-workflow-entry
 */
'use strict';

const fs = require('fs');
const path = require('path');

// 虚拟人相关关键词（中英文）
const AVATAR_KEYWORDS = [
  // 中文
  '虚拟人', '数字人', '讯飞', 'xfyun', 'avatar', '智能客服', '直播',
  '语音交互', '文本驱动', '音频驱动', '动作控制', '形象', '发音人',
  '场景', '模型配置', '知识库', 'appId', 'appSecret', 'anchorId', 'vcn',
  'Web对话', 'H5通话', '大屏交互', '透明背景', '字幕', '全双工',
  // 英文/拼音
  'virtual human', 'digital human', 'avatar sdk', 'web template',
  'live streaming', 'voice interact', 'text driver', 'audio driver',
];

// 从 stdin 读取输入
let inputData = '';
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(chunk) {
  inputData += chunk;
});

process.stdin.on('end', function() {
  const logFile = path.join(process.env.TEMP || '/tmp', 'avatar_hook_debug.log');
  try {
    const raw = inputData.trim();

    // UserPromptSubmit hook 传入的是 JSON payload，需解析出真正的 prompt 字段
    let userPrompt = raw;
    try {
      const payload = JSON.parse(raw);
      userPrompt = payload.prompt || payload.user_prompt || raw;
    } catch (e) {
      // 不是 JSON（如手动测试），直接用原文
    }

    fs.appendFileSync(logFile, '\n[' + new Date().toISOString() + '] Hook triggered\nPrompt: ' + userPrompt.slice(0, 120) + '\n', 'utf8');

    // 检测是否包含虚拟人关键词
    const promptLower = userPrompt.toLowerCase();
    const isAvatarRelated = AVATAR_KEYWORDS.some(function(kw) {
      return promptLower.includes(kw.toLowerCase());
    });

    fs.appendFileSync(logFile, 'Avatar related: ' + isAvatarRelated + '\n', 'utf8');

    if (isAvatarRelated) {
      // UserPromptSubmit hook 只能注入上下文（additionalContext），无法拦截/替代模型输出。
      // 通过官方 JSON 契约注入强路由提示，引导模型优先调用 avatar-workflow-entry。
      const context = '[avatar-platform 路由提示] 本次请求涉及讯飞虚拟人/数字人。'
        + '请在响应前先调用 Skill 工具（skill="avatar-workflow-entry"，来自 avatar-platform 插件）'
        + '进行意图识别与路由，由它分发到 avatar-web-template（Web对话模板）、avatar-executing（SDK自建工程）、'
        + 'avatar-live-streaming（直播）、avatar-troubleshoot（排障）等子技能。'
        + '不要跳过路由直接用通用知识抛技术选型问题（如 Unity/Three.js/2D-3D）。';

      const out = {
        hookSpecificOutput: {
          hookEventName: 'UserPromptSubmit',
          additionalContext: context
        }
      };

      process.stdout.write(JSON.stringify(out));
      fs.appendFileSync(logFile, 'Output: additionalContext injected\n', 'utf8');
    }

    process.exit(0);
  } catch (err) {
    fs.appendFileSync(logFile, 'Error: ' + err.message + '\n', 'utf8');
    process.exit(1);
  }
});
