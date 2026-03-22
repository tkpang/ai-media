# Banana Pro 图片生成操作指南

## 概述

本文档记录了使用 Banana Pro (xais1.dchai.cn) 成功生成 AI 图片的完整方法。

**核心结论：** xais1.dchai.cn 是一个 Web 应用，不是标准 REST API。需要模拟浏览器的请求流程才能正常生成图片。标准的 OpenAI/Gemini 格式 API 调用（`/v1/images/generations`、`/v1/chat/completions`）均无法使用。

## 成功案例

| 时间 | 提示词 | 路由 | 分辨率 | 文件大小 | 文件名 |
|------|--------|------|--------|----------|--------|
| 2026-03-22 20:54 | "a simple red apple icon on white background" | 2K_5 | 2048x2048 | 3.9 MB | banana_pro_web_2K_5_20260322_205359.png |
| 2026-03-22 20:52 | 集成测试 | 2K_5 | 2048x2048 | 2.9 MB | outputs/web_integration_smoke.png |
| 2026-03-22 21:14 | "CEO test: professional headshot of a business leader" | 2K_5 | 2048x2048 | 5.7 MB | banana_pro_web_2K_5_20260322_211442.png |

**单次生成成本：** ~$0.045（约 ¥0.33）

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install requests python-dotenv

# 配置环境变量（复制 .env.example 并填入你的 API Key）
cp .env.example .env
# 编辑 .env，填入以下内容：
# BANANA_PRO_API_KEY=sk-你的密钥
# BANANA_PRO_BASE_URL=https://xais1.dchai.cn
# BANANA_PRO_MODE=web
```

### 2. 生成一张图片

```bash
python generate_image.py "一只可爱的猫咪在阳光下睡觉"
```

或者在 Python 中调用：

```python
from banana_pro_web_client import BananaProWebClient

client = BananaProWebClient(
    api_key="sk-你的密钥",
    base_url="https://xais1.dchai.cn"
)
client.login()

result = client.generate_image(
    prompt="一只可爱的猫咪在阳光下睡觉",
    route="2K_2",          # 推荐路由
    aspect_ratio="1:1",    # 正方形
)
print(f"图片已保存: {result['saved_to']}")
```

### 3. 带费用追踪的生成

```python
from banana_pro_web_with_tracking import BananaProWebWithTracking

client = BananaProWebWithTracking(
    api_key="sk-你的密钥",
    base_url="https://xais1.dchai.cn"
)
client.login()

result = client.generate_image(
    prompt="专业商务人像照",
    route="2K_2",
    aspect_ratio="1:1",
)
print(f"图片: {result['saved_to']}, 费用: ${result['cost']}")
```

## 技术原理

### 请求流程（6 步）

```
1. POST /xais/xtokenLogin    → 用 API Key 登录，获取会话
2. GET  /xais/confGet         → 获取可用模型配置
3. POST /xais/workerTaskStart → 提交生图任务
4. GET  /xais/workerTaskWait  → SSE 流等待任务完成
5. GET  /xais/attUrls         → 获取图片下载地址
6. GET  {image_url}           → 下载图片到本地
```

### 可用模型

| 模型名称 | 分辨率 | 推荐度 |
|----------|--------|--------|
| Nano_Banana_Pro_2K_2 | 2048x2048 | ★★★ 推荐（性价比最高） |
| Nano_Banana_Pro_2K_5 | 2048x2048 | ★★★ 推荐 |
| Nano_Banana_Pro_2K_1 | 2048x2048 | ★★ |
| Nano_Banana_Pro_2K_3~7 | 2048x2048 | ★★ |
| Nano_Banana_Pro_4K_2 | 4096x4096 | ★★ 高清但更贵 |
| Nano_Banana_Pro_4K_5 | 4096x4096 | ★★ 高清但更贵 |

### 支持的宽高比

- `1:1` — 正方形（默认）
- `16:9` — 横屏宽幅
- `9:16` — 竖屏（手机竖屏/短视频封面）
- `4:3` — 标准横幅
- `3:2` — 专业摄影比例
- `4:5` — Instagram 竖幅
- `21:9` — 超宽屏

## 文件清单

### 核心脚本（运行必需）

| 文件 | 说明 |
|------|------|
| `generate_image.py` | 命令行一键生图脚本 |
| `banana_pro_web_client.py` | Web 自动化核心客户端 |
| `banana_pro_web_with_tracking.py` | 带费用追踪的客户端 |
| `cost_tracker.py` | 费用追踪模块 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `.env.example` | 环境变量模板 |
| `.env` | 实际配置（不要提交到 git） |

### 辅助脚本（可选）

| 文件 | 说明 |
|------|------|
| `banana_pro_gemini.py` | Gemini 格式客户端（备用方案） |
| `banana_pro_client.py` | OpenAI 格式客户端（备用方案） |
| `batch_processor.py` | 批量生图处理器 |
| `ai_media_cli.py` | 完整 CLI 工具 |
| `integration_test.py` | 集成测试套件 |
| `health_check.py` | 系统健康检查 |
| `monitor.py` | 实时监控面板 |

## 常见问题

### Q: 为什么不能用标准 REST API？

xais1.dchai.cn 是一个 Web 应用界面，它的后端使用了自定义的 `/xais/*` 路由，不兼容 OpenAI 或 Gemini 的标准 API 格式。虽然 `/v1/models` 能返回模型列表，但 `/v1/images/generations` 返回 404，`/v1/chat/completions` 返回服务错误。

### Q: 生成一张图大约要多久？

根据测试，从提交任务到图片下载完成大约需要 30-120 秒，取决于服务器负载。脚本内置了 240 秒超时。

### Q: 如何控制费用？

使用 `BananaProWebWithTracking` 客户端会自动记录每次生成的费用到 `cost_data.json`。每张 2K 图片约 $0.045，月预算 $150 可以生成约 3300 张图。

### Q: 路由 2 和 5 有什么区别？

两者生成质量相近，都是经过验证的稳定路由。客户端内置了自动 fallback 机制，如果首选路由失败会自动尝试备选路由。

## 验证状态

- 集成测试通过率: 93% (27/29)
- 健康检查通过率: 71% (15/21，所有关键项通过)
- 生产图片生成: 3 张验证成功
- 费用追踪: 正常运行
- 总花费: $7.04 / $150 预算
