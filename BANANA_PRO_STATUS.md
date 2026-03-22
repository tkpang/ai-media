# Banana Pro Integration Status

## API Discovery Results

### Endpoint: https://xais1.dchai.cn
### API Key: `sk-Pi5Sc2cZfD7M9bkCHU2ly0OroaFoYirtteqIu1HwkssCsKL8`

## Available Models

The API supports 18 models across multiple routes (accessible via `/v1/models`):

### 2K Resolution (Cost-optimized routes: **2** and **5**)
- `Nano_Banana_Pro_2K_1` through `Nano_Banana_Pro_2K_7`
- Additional: `xitu_2K`

### 4K Resolution
- `Nano_Banana_Pro_4K_1` through `Nano_Banana_Pro_4K_7`
- Additional: `xitu_4K`, `mjx_4K`

### Other
- `c3f`

## API Testing Results

### ✓ Working Endpoints
- `GET /v1/models` - Lists available models

### ✗ Tested but Failed
- `POST /v1/images/generations` - Returns 404
- `POST /v1/chat/completions` - Returns error: "文生图服务调用失败!" (Text-to-image service call failed)
- `POST /v1/completions` - Returns error: "文生图服务调用失败!"

## Web Automation Solution (Implemented)

`xais1.dchai.cn` is a web app, but its internal `/xais/*` endpoints are stable and can be automated.

Working flow implemented on **2026-03-22**:
1. `POST /xais/xtokenLogin` with `text/plain` xtoken body
2. `GET /xais/confGet` for model/ratio metadata
3. `POST /xais/workerTaskStart` to create image task
4. `GET /xais/workerTaskWait?id=...` via `text/event-stream` until `result`
5. `GET /xais/attUrls?att=...` to resolve downloadable image URL

Code delivered:
- `banana_pro_web_client.py` - end-to-end web automation client
- `banana_pro_web_with_tracking.py` - same flow with cost tracking
- `ai_media_cli.py` - auto-selects web mode for xais1 or `BANANA_PRO_MODE=web`
- `quick_start.py` - setup option for xais1 web mode

## Alternative Approach

If the xais1.dchai.cn API is not programmatically accessible, we can:
1. Use the web UI manually for image generation
2. Find alternative Banana Pro API providers (e.g., apiyi.com, laozhang.ai, kie.ai)
3. Use Google's official Gemini API directly

## Cost Information (from research)

Based on third-party providers:
- 2K images: ~$0.05 - $0.134 per image
- 4K images: ~$0.24 per image
- Routes 2 and 5 recommended for cost optimization

## Video Editing Requirements

For Ubuntu platform video editing, recommend:
- **FFmpeg** - Command-line video processing
- **kdenlive** - GUI video editor (if desktop available)
- **OpenCV** - Programmatic video editing via Python

Awaiting board decision on whether video editing should be automated or manual workflow.
