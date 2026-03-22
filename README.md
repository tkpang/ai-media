# AI Media - Paperclip Agent Workspace

## Project Overview

AI media generation and editing workspace for the Paperclip agent system.

## Current Tools

### 1. Banana Pro (Image Generation)

**Status:** ✅ WORKING - Supports both API mode and xais1 web automation mode

**xais1 Endpoint:** https://xais1.dchai.cn
**Implementation:** Uses stable web-task endpoints (`/xais/xtokenLogin`, `/xais/workerTaskStart`, `/xais/workerTaskWait`, `/xais/attUrls`)

**✅ Code Ready:**
- `banana_pro_gemini.py` - Production-ready client (Gemini API format)
- `banana_pro_web_client.py` - Production-ready web automation client for xais1
- `banana_pro_web_with_tracking.py` - Web client with automatic cost tracking
- `example_usage.py` - Comprehensive usage examples
- All aspect ratios supported: 1:1, 16:9, 9:16, 4:3, 3:2, 4:5, 21:9
- Cost-optimized routes pre-configured

**Mode Selection:**
1. **`BANANA_PRO_MODE=web`** with `BANANA_PRO_BASE_URL=https://xais1.dchai.cn`
2. **`BANANA_PRO_MODE=api`** for APIYI/LaoZhang/custom Gemini-compatible providers

**Files:**
- `banana_pro_gemini.py` - Ready-to-use client
- `example_usage.py` - Production examples
- `BANANA_PRO_STATUS.md` - Technical investigation
- `ALTERNATIVES.md` - ⭐ Provider comparison & recommendations
- `test_banana_pro.py` - Diagnostic tool

### 2. Seedance 2.0 (Video Generation)

**Status:** 📋 Pending - Not yet configured

To be implemented after Banana Pro is working.

### 3. Video Editing (Ubuntu)

**Status:** 📋 Pending - Awaiting requirements

**Recommended Tools:**
- **FFmpeg** - Command-line video processing (automated workflows)
- **kdenlive** - GUI video editor (manual editing, requires desktop)
- **Python Libraries:**
  - `opencv-python` - Video processing and manipulation
  - `moviepy` - High-level video editing
  - `ffmpeg-python` - Python wrapper for FFmpeg

**Installation:**
```bash
# FFmpeg
sudo apt update && sudo apt install ffmpeg

# Python libraries
pip install opencv-python moviepy ffmpeg-python

# kdenlive (if GUI needed)
sudo apt install kdenlive
```

## Documentation

### 📋 Current Status & Planning
- **[Board Summary](./BOARD_SUMMARY.md)** - ⭐ **START HERE** - Executive summary for decision makers
- [Banana Pro Status](./BANANA_PRO_STATUS.md) - Technical investigation and blockers
- [Alternatives Research](./ALTERNATIVES.md) - API provider comparison and recommendations

### ✅ Implementation Ready
- [Example Usage](./example_usage.py) - Production-ready usage examples
- [Banana Pro Client](./banana_pro_gemini.py) - Ready-to-use Python client
- [Testing Checklist](./TESTING_CHECKLIST.md) - Comprehensive QA procedures

### 🔮 Future Planning
- [Seedance 2.0 Plan](./SEEDANCE_PLAN.md) - Video generation integration roadmap
- [Video Editing Guide](./VIDEO_EDITING_GUIDE.md) - Tools and workflows for video processing

### 🔧 Utilities
- **[AI Media CLI](./ai_media_cli.py)** - ⭐ **NEW** Command-line interface for all features ([guide](./CLI_GUIDE.md))
- [Quick Start](./quick_start.py) - Interactive setup wizard
- [Cost Tracker](./cost_tracker.py) - Budget monitoring and analytics
- [Batch Processor](./batch_processor.py) - Parallel bulk processing
- [Banana Pro + Tracking](./banana_pro_with_tracking.py) - Auto-tracking client
- [Test Script](./test_banana_pro.py) - API endpoint diagnostic tool

### 📖 Additional Guides
- **[Quick Reference](./QUICK_REFERENCE.md)** - ⭐⭐ **START HERE** - Commands cheat sheet
- **[Workspace Status](./WORKSPACE_STATUS.md)** - ⭐ Complete system status report
- **[CLI Guide](./CLI_GUIDE.md)** - Complete command-line reference
- **[Production Features](./PRODUCTION_FEATURES.md)** - Enterprise features overview
- [Developer Guide](./DEVELOPER_GUIDE.md) - Technical documentation for developers
- [Development Log](./DEVELOPMENT_LOG.md) - Complete development history

## Research Sources

- [Atlas Cloud - Nano Banana Pro Guide](https://www.atlascloud.ai/blog/guides/how-to-use-nano-banana-pro-api-the-complete-guide-in-2026)
- [APIYI - OpenClaw Integration Tutorial](https://help.apiyi.com/en/openclaw-nano-banana-pro-image-api-tutorial-en.html)
- [Kie.ai - Nano Banana Pro](https://kie.ai/nano-banana-pro)
- [LaoZhang AI Blog](https://blog.laozhang.ai/en/posts/how-to-get-nano-banana-pro-api-key)

## Quick Start

### Option 1: Command Line (Recommended for most users)

```bash
# 1. Setup (first time only)
python3 quick_start.py

# 2. Generate a single image
python3 ai_media_cli.py generate "a beautiful sunset"

# 3. Process a batch
python3 ai_media_cli.py batch prompts.txt

# 4. Check costs
python3 ai_media_cli.py cost --budget 150

# See full CLI guide: CLI_GUIDE.md
```

### Option 2: Interactive Setup

```bash
# Run the interactive setup wizard
python3 quick_start.py
```

This will guide you through:
1. Environment check (dependencies)
2. API configuration setup
3. Connectivity testing
4. First test image generation

**Or manual setup:**

```python
# Basic client (no cost tracking)
from banana_pro_gemini import BananaProGeminiClient

client = BananaProGeminiClient(
    api_key="your-api-key-here",
    base_url="https://api.provider.com"
)

result = client.generate_image(
    prompt="A beautiful sunset over mountains",
    route="2K_2",  # Cost-optimized
    aspect_ratio="16:9"
)
```

**With automatic cost tracking:**

```python
from banana_pro_with_tracking import BananaProWithTracking

client = BananaProWithTracking(
    api_key="your-api-key-here",
    base_url="https://api.provider.com",
    cost_per_image=0.045  # APIYI pricing
)

result = client.generate_image("A beautiful sunset over mountains")
# Cost is automatically tracked!

# View budget status
status = client.tracker.get_budget_status(monthly_budget=150.0)
print(f"Spent: ${status['current_spend']:.2f} / ${status['monthly_budget']:.2f}")
```

**Batch processing:**

```python
from batch_processor import BatchProcessor

processor = BatchProcessor(
    client=client,
    max_workers=3,  # Parallel processing
    max_cost=10.0   # Stop at $10
)

prompts = ["sunset", "mountain", "ocean"]
summary = processor.process_image_batch(prompts, route="2K_2")

print(f"Generated {summary['completed']} images")
print(f"Total cost: ${summary['total_cost']:.2f}")
```

## Next Steps

### Immediate Actions Required

**Decision Needed:** Choose API provider for Banana Pro
- See `ALTERNATIVES.md` for detailed comparison
- Recommended: APIYI ($0.045/image + SLA) or LaoZhang ($0.05/image)
- Code is ready - just need credentials

### Then

1. Run `quick_start.py` to configure and test
2. Set up Seedance 2.0 for video generation
3. Define video editing workflow requirements (FFmpeg/OpenCV)
