# Divition — 手势控制塔罗占卜游戏

基于 MediaPipe HandLandmarker 的手势识别塔罗牌占卜应用。通过摄像头实时追踪手部21个关键点，识别捏合、握拳、张开手掌等手势来控制牌的选择与解读。

## 架构概览

### 视觉层次（从底到顶）
```
Layer 0: <video>          — 摄像头原始画面
Layer 1: <canvas>         — 手部骨骼/关节点叠加绘制
Layer 2: #dim-overlay     — 半透明遮罩
Layer 3: #cards-layer     — 卡片交互区
  ├── #available-area     — 上半区：待选牌（横向滚动）
  └── #selected-area      — 下半区：已选牌
```

### 技术栈
- **手势识别**: MediaPipe HandLandmarker (CDN: `@mediapipe/tasks-vision@0.10.17`)
- **模型文件**: `hand_landmarker.task` (7.8MB, WASM)
- **前端**: 纯 HTML/CSS/JS (ES Module)，无框架依赖
- **摄像头**: `navigator.mediaDevices.getUserMedia`

### 手势识别流程
```
detectLoop() [每帧执行]
  ├── landmarker.detectForVideo() → 21个手部关键点
  ├── drawSkeleton() → 绘制骨骼叠加层
  ├── updatePointingFromLandmark() → 食指指尖(landmark[8])定位到卡片
  ├── recognizeGesture() → 分类手势
  │     ├── pinchDist < 0.28 → 'ok' (捏合)
  │     ├── avgOpen < 0.24 + allFingersClosed 90帧 → 'fist' (握拳)
  │     ├── avgOpen > 0.5 120帧 → 'submit' (张开手掌)
  │     └── else → 'none'
  ├── 悬停计时器: 指向同一张卡180帧(3秒) → 自动选中
  └── handleGesture() → 分发动作
```

### 手势对照表

| 手势 | 触发条件 | 动作 |
|------|---------|------|
| 🤏 捏合 | 拇指尖与食指尖距离 < 0.28×手掌大小 | 选中当前指向的牌 |
| ☝ 悬停3秒 | 食指指尖指向同一张卡持续3秒 | 自动选中该牌 |
| ✊ 握拳 | 五指向内弯曲1.5秒 | 清空所有已选牌 |
| 🖐 张开手掌 | 五指伸展2秒 | 提交并显示解读 |
| 👈 手左挥 | 手X坐标连续左移 | 待选区向右翻页 |
| 👉 手右挥 | 手X坐标连续右移 | 待选区向左翻页 |

### PC 键盘快捷键

| 按键 | 动作 |
|------|------|
| ← → | 翻动待选牌 |
| Enter / Space | 选中当前高亮牌 |
| Delete / Backspace | 移除最后一张已选牌 |
| Escape | 清空已选 / 关闭弹窗 |
| S | 提交解读 |
| ? | 显示/隐藏快捷键帮助 |
| 鼠标点击牌 | 选中/取消选中 |

## 本地运行

### 前置条件
- 现代浏览器 (Chrome/Edge/Safari/Firefox)
- 摄像头设备
- **必须通过 HTTP 服务器访问**（摄像头 API 需要安全上下文：localhost 或 HTTPS）

### 启动
```bash
cd /Users/easonlv/progs/hand-gesture
python3 -m http.server 8080
# 访问 http://localhost:8080/gesture-demo.html
```

或使用 Node.js:
```bash
npx serve .
# 访问 http://localhost:3000/gesture-demo.html
```

> **注意**: 直接用 `file://` 协议打开会导致摄像头权限被拒绝。

## 部署

### 服务器要求
- Nginx (或其他 HTTP 服务器)
- **必须启用 HTTPS**（摄像头 API 要求安全上下文）
- 静态文件服务，无需后端

### Nginx 配置示例
```nginx
location /hand-gesture/ {
    alias /var/www/hand-gesture/;
    index gesture-demo.html;
    # 确保 .task 文件以正确 MIME 类型提供
    location ~ \.task$ {
        types { application/octet-stream task; }
    }
}
```

### 部署步骤
```bash
# 上传文件
scp -r gesture-demo.html hand_landmarker.task cards/ root@SERVER_IP:/var/www/hand-gesture/

# 更新 Nginx 配置并重载
ssh root@SERVER_IP "nginx -t && systemctl reload nginx"
```

## 文件说明

```
hand-gesture/
├── gesture-demo.html        # 主应用（单文件）
├── hand_landmarker.task     # MediaPipe 手部关键点模型 (7.8MB)
├── cards/
│   ├── gen_cards.py         # 卡牌图片生成脚本（智谱 CogView-4）
│   ├── gen_cards.log        # 生成日志
│   ├── test_card.png        # 测试卡牌
│   ├── faces/               # 卡牌正面设计稿
│   ├── back_selected/       # 已选卡牌背面
│   └── back_unselected/     # 未选卡牌背面
└── README.md
```

## 卡牌数据

36张塔罗牌，包含22张大阿尔卡纳（愚者→世界）和14张小阿尔卡纳（权杖/圣杯/宝剑/星币各若干）。每张牌都有中文名、罗马/数字符号和寓意关键词。

牌面图片通过智谱 CogView-4 模型生成，以古汉字为视觉主题，融合神秘学塔罗风格。

## 兼容性

| 平台 | 手势控制 | 键盘/鼠标 | 触摸 |
|------|---------|----------|------|
| 桌面浏览器 | ✅ | ✅ | — |
| 移动端浏览器 | ✅ | — | ✅ 滑动+点击 |
| 平板 | ✅ | — | ✅ |
