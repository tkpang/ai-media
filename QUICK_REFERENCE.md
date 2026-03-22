# AI Media - Quick Reference Card

**Last Updated:** 2026-03-22

---

## 🚀 Getting Started (First Time)

```bash
# 1. Check system health
python3 health_check.py --quick

# 2. Configure API credentials
python3 quick_start.py

# 3. Generate test image
python3 ai_media_cli.py generate "test image"

# 4. Start monitoring
python3 monitor.py --watch
```

---

## 💡 Common Commands

### Generate Single Image
```bash
# Simple
python3 ai_media_cli.py generate "your prompt here"

# With options
python3 ai_media_cli.py generate "sunset over mountains" \
    --route 2K_5 \
    --aspect-ratio 16:9 \
    --output sunset.png
```

### Batch Processing
```bash
# From file
python3 ai_media_cli.py batch prompts.txt

# With cost limit
python3 ai_media_cli.py batch prompts.txt --max-cost 10.0

# Parallel workers
python3 ai_media_cli.py batch prompts.txt --workers 5
```

### Cost Monitoring
```bash
# Check current costs
python3 ai_media_cli.py cost

# With budget check
python3 ai_media_cli.py cost --budget 150

# Live monitoring
python3 monitor.py --watch

# Generate report
python3 monitor.py --report --days 30

# Export data
python3 monitor.py --export
```

### System Health
```bash
# Quick check
python3 health_check.py --quick

# Full check (with API)
python3 health_check.py

# Verbose output
python3 health_check.py --verbose
```

---

## 🐍 Python API Quick Start

### Basic Usage
```python
from banana_pro_gemini import BananaProGeminiClient

client = BananaProGeminiClient(
    api_key="your-key",
    base_url="https://api.provider.com"
)

result = client.generate_image(
    prompt="your prompt",
    route="2K_2",
    aspect_ratio="16:9"
)
```

### With Auto Cost Tracking
```python
from banana_pro_with_tracking import BananaProWithTracking

client = BananaProWithTracking(
    api_key="your-key",
    base_url="https://api.provider.com",
    cost_per_image=0.045
)

result = client.generate_image("your prompt")
# Cost automatically tracked!
```

### Batch Processing
```python
from batch_processor import BatchProcessor

processor = BatchProcessor(
    client=client,
    max_workers=3,
    max_cost=10.0
)

prompts = ["prompt 1", "prompt 2", "prompt 3"]
summary = processor.process_image_batch(
    prompts,
    route="2K_2"
)

print(f"Completed: {summary['completed']}")
print(f"Total cost: ${summary['total_cost']:.2f}")
```

### Cost Tracking
```python
from cost_tracker import CostTracker

tracker = CostTracker()

# Add record
tracker.add_record(
    service="banana_pro",
    cost=0.045,
    description="landscape image"
)

# Check budget
status = tracker.get_budget_status(monthly_budget=150.0)
print(f"Spent: ${status['current_spend']:.2f}")
print(f"Alert: {status['alert_level']}")

# Get summary
summary = tracker.get_daily_summary("2026-03-22")
print(f"Today's cost: ${summary['total_cost']:.2f}")
```

---

## 📊 Aspect Ratios

| Ratio | Use Case | Example |
|-------|----------|---------|
| 1:1 | Square | Instagram posts |
| 16:9 | Landscape | YouTube thumbnails |
| 9:16 | Portrait | Stories, TikTok |
| 4:3 | Classic | Presentations |
| 3:2 | Photography | Professional photos |
| 4:5 | Portrait | Instagram feed |
| 21:9 | Ultrawide | Desktop wallpapers |

---

## 🎯 Routes (Cost Optimization)

### Recommended Routes
- **2K_2** - Cost-optimized 2K ($0.045)
- **2K_5** - Alternative 2K ($0.045)
- **4K_2** - Cost-optimized 4K ($0.045)
- **4K_5** - Alternative 4K ($0.045)

### All Available
2K: `2K_1`, `2K_2`, `2K_3`, `2K_4`, `2K_5`, `2K_6`, `2K_7`
4K: `4K_1`, `4K_2`, `4K_3`, `4K_4`, `4K_5`, `4K_6`, `4K_7`

---

## 💰 Pricing (APIYI)

| Item | Cost |
|------|------|
| 2K Image | $0.045 |
| 4K Image | $0.045 |
| 100 images | $4.50 |
| 1,000 images | $45.00 |

**Budget Alerts:**
- ✅ OK: <50% of budget
- ⚠️ Warning: 50-75%
- 🔴 High: 75-90%
- 🚨 Critical: >90%

---

## 📁 File Locations

```
outputs/          # Generated images
logs/             # Application logs
cache/            # Cached responses (if enabled)
cost_data.json    # Cost tracking database
.env              # API configuration (CREATE THIS)
```

---

## 🔧 Configuration (.env)

```bash
# Required
BANANA_PRO_API_KEY=sk-your-key-here
BANANA_PRO_BASE_URL=https://api.provider.com

# Optional
OUTPUT_DIR=./outputs
ENABLE_COST_TRACKING=true
LOG_LEVEL=INFO
```

---

## 🆘 Troubleshooting

### "API returns HTML"
➜ Wrong endpoint. Use APIYI or LaoZhang.

### "401 Unauthorized"
➜ Check API key in .env file.

### "No module named 'requests'"
➜ Run: `pip install requests`

### "Permission denied"
➜ Run: `chmod 755 outputs/`

### "Cost tracking broken"
➜ Delete cost_data.json and restart.

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| README.md | Main overview |
| CLI_GUIDE.md | CLI reference |
| DEVELOPER_GUIDE.md | Code documentation |
| BOARD_SUMMARY.md | Executive summary |
| WORKSPACE_STATUS.md | Complete status |
| PRODUCTION_FEATURES.md | Feature list |
| TESTING_CHECKLIST.md | QA procedures |

---

## 🎨 Example Prompts

**Realistic:**
- "Professional headshot, business attire, studio lighting"
- "Modern office interior, natural light, minimalist design"

**Creative:**
- "Cyberpunk city at night, neon lights, rain"
- "Fantasy castle on mountain peak, dramatic sunset"

**Product:**
- "Product photography, white background, soft shadows"
- "Luxury watch on marble surface, professional lighting"

**Landscape:**
- "Mountain landscape, golden hour, lake reflection"
- "Beach sunset, calm ocean, palm trees"

---

## ⚡ Performance Tips

1. **Use cost-optimized routes** (2K_2, 2K_5)
2. **Batch similar requests** for efficiency
3. **Set max_cost limits** to prevent overruns
4. **Monitor with --watch** for real-time visibility
5. **Export reports** weekly for trend analysis

---

## 🔗 Quick Links

**Providers:**
- APIYI: https://apiyi.com (recommended)
- LaoZhang: https://laozhang.ai

**API Format:**
- Gemini API (Google format)
- Endpoint: `/v1beta/models/{model}:generateContent`

---

## ✅ Daily Workflow

```bash
# Morning: Check costs
python3 monitor.py

# Generate images as needed
python3 ai_media_cli.py generate "..."

# Batch processing
python3 ai_media_cli.py batch prompts.txt

# End of day: Export report
python3 monitor.py --export
```

---

**Need help?** Run `python3 health_check.py --verbose`
