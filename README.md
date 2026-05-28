# Divition — 手势控制塔罗占卜

基于 **MediaPipe HandLandmarker** 的手势识别塔罗牌占卜应用。通过摄像头实时追踪手部 21 个关键点，识别捏合、握拳、张开手掌等手势来控制牌的选择与 AI 解读。

## 演示

https://tuteng3.site/hand-gesture/gesture-demo.html

## 功能特性

- **实时手势识别** — 6 种手势（捏合选中、握拳清空、张开提交、悬停自动选、左右挥手翻页）
- **36 张塔罗牌** — 22 张大阿尔卡纳 + 14 张小阿尔卡纳，古汉字×神秘学视觉风格
- **AI 命理解读** — MiniMax M2.7 模型生成个性化占卜解读（约 6-10 秒）
- **PC/移动端双支持** — 手势 + 键盘快捷键 + 鼠标 + 触摸
- **调试面板** — 实时显示关键点坐标、手指状态、手势识别计数器
- **卡牌洗牌/排序** — 一键随机打乱或按序排列

## 架构

```
Layer 0: <video>          — 摄像头原始画面
Layer 1: <canvas>         — 手部骨骼/关节点叠加绘制
Layer 2: #dim-overlay     — 半透明遮罩
Layer 3: #cards-layer     — 卡片交互区
  ├── #available-area     — 上半区：待选牌（横向滚动）
  └── #selected-area      — 下半区：已选牌
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 手势识别 | MediaPipe HandLandmarker (`@mediapipe/tasks-vision@0.10.17`) |
| 模型文件 | `hand_landmarker.task` (7.8MB, WASM) |
| 前端 | 纯 HTML/CSS/JS (ES Module)，无框架依赖 |
| AI 解读 | MiniMax M2.7 API，通过 PHP 代理调用 |
| 摄像头 | `navigator.mediaDevices.getUserMedia` |

## 手势识别

### 手势对照表

| 手势 | 触发条件 | 动作 |
|------|---------|------|
| 🤏 **捏合** | 拇指+食指指尖靠近 (< 0.3×手掌宽度)，其余 3 指伸展 | 选中当前指向的牌 |
| ☝ **悬停 3 秒** | 食指指尖指向同一张卡持续 180 帧 | 自动选中该牌 |
| ✊ **握拳** | 5 指指尖全部在 PIP 关节下方，持续 90 帧 (0.5s) | 清空所有已选牌 |
| 🖐 **张开手掌** | 5 指指尖全部在 PIP 关节上方，持续 120 帧 (0.6s) | 提交并显示 AI 解读 |
| 👈 **手左挥** | 手 X 坐标连续左移 (>5px/frame, 6 帧) | 待选区向右翻页 |
| 👉 **手右挥** | 手 X 坐标连续右移 (>5px/frame, 6 帧) | 待选区向左翻页 |

### 识别流程

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
  ├── 悬停计时器: 指向同一张卡 180帧(3秒) → 自动选中
  └── handleGesture() → 分发动作
```

> 左下角调试面板实时显示 pinchDist、5 指 Y 偏移 (tip.y - pip.y)、手势及计数器。
> **Y 偏移解读**: 负值 = 指尖在上方(伸展)，正值 = 指尖在下方(弯曲)。握拳时 5 个值应全正，张开时全负。

## 键盘快捷键 (PC)

| 按键 | 动作 |
|------|------|
| `←` `→` | 翻动待选牌 |
| `Enter` / `Space` | 选中当前高亮牌 |
| `Delete` / `Backspace` | 移除最后一张已选牌 |
| `Escape` | 清空已选 / 关闭弹窗 |
| `S` | 提交解读 |
| `?` | 显示/隐藏快捷键帮助 |
| 鼠标点击牌 | 选中/取消选中 |

## 本地运行

### 前置条件

- 现代浏览器 (Chrome/Edge/Safari/Firefox)
- 摄像头设备
- **必须通过 HTTP 服务器访问**（摄像头 API 要求安全上下文：localhost 或 HTTPS）

### 启动方式

```bash
# 方式 1: Python (仅手势展示，无 AI 解读)
python3 -m http.server 8080
# 访问 http://localhost:8080/gesture-demo.html

# 方式 2: Node.js
npx serve .
# 访问 http://localhost:3000/gesture-demo.html

# 方式 3: PHP 内置服务器 (支持 AI 解读)
php -S localhost:8888
# 访问 http://localhost:8888/gesture-demo.html
```

> **注意**: 直接用 `file://` 协议打开会导致摄像头权限被拒绝。AI 解读功能依赖 `proxy.php`，需要 PHP 环境并设置 `MINIMAX_API_KEY` 环境变量。

## 部署

### 服务器要求

- Nginx (或其他 HTTP 服务器)
- PHP-FPM 8.0+ (AI 解读代理)
- **必须启用 HTTPS**（摄像头 API 要求安全上下文）

### 上传文件

```bash
scp gesture-demo.html hand_landmarker.task proxy.php user@your-server:/var/www/hand-gesture/
scp cards/*.png user@your-server:/var/www/hand-gesture/cards/
```

### Nginx 配置

```nginx
# 静态文件
location ^~ /hand-gesture/ {
    alias /var/www/hand-gesture/;
    index gesture-demo.html;

    location ~ \.task$ {
        types { application/octet-stream task; }
        add_header Cache-Control "public, max-age=86400";
    }

    location ~ \.(png|jpg|webp)$ {
        add_header Cache-Control "public, max-age=604800";
    }
}

# PHP AI 代理
location = /hand-gesture/proxy.php {
    alias /var/www/hand-gesture/proxy.php;
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME /var/www/hand-gesture/proxy.php;
    include fastcgi_params;
    fastcgi_read_timeout 60s;
}
```

### 环境变量

在 PHP-FPM 池配置或 `.env` 中设置：

```ini
MINIMAX_API_KEY=sk-your-minimax-key-here
```

### 验证部署

```bash
# 主页
curl -sI https://your-domain/hand-gesture/gesture-demo.html | head -1
# HTTP/1.1 200 OK

# AI 代理
curl -s -X POST https://your-domain/hand-gesture/proxy.php \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"你好"}]}'
# 应返回 JSON 格式的 AI 回复
```

## 项目结构

```
hand-gesture/
├── gesture-demo.html        # 主应用 (~64KB，单文件)
├── hand_landmarker.task     # MediaPipe 手部关键点模型 (7.8MB)
├── proxy.php                # MiniMax AI API 代理
├── assets/                  # 演示视频和背景音乐
│   ├── card_reveal_pc.mp4
│   ├── card_reveal_web.mp4
│   └── harry_potter_style_bgm.mp3
├── cards/                   # 卡牌图片
│   ├── gen_cards.py         # 卡牌生成脚本（智谱 CogView-4）
│   ├── faces/               # 卡牌正面设计稿
│   ├── back_selected/       # 已选卡牌背面
│   └── back_unselected/     # 未选卡牌背面
└── README.md
```

## 卡牌数据

36 张塔罗牌，包含 22 张大阿尔卡纳（愚者 → 世界）和 14 张小阿尔卡纳（权杖/圣杯/宝剑/星币各若干）。每张牌都有中文名、罗马/数字符号和寓意关键词。

牌面图片通过智谱 CogView-4 模型生成，以古汉字为视觉主题，融合神秘学塔罗风格。

## 兼容性

| 平台 | 手势控制 | 键盘/鼠标 | 触摸 |
|------|---------|----------|------|
| 桌面浏览器 | ✅ | ✅ | — |
| 移动端浏览器 | ✅ | — | ✅ 滑动 + 点击 |
| 平板 | ✅ | — | ✅ |
