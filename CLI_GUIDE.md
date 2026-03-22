# AI Media CLI - User Guide

Quick command-line access to all AI Media features.

## Installation

No installation needed! Just ensure you have:
1. Python 3.8+
2. Required dependencies: `pip install requests`
3. Configuration file: `.env` (run `quick_start.py` to create)

## Quick Start

```bash
# Check system status
python3 ai_media_cli.py status

# Generate a single image
python3 ai_media_cli.py generate "a beautiful sunset"

# Process a batch from file
python3 ai_media_cli.py batch prompts.txt

# Check costs
python3 ai_media_cli.py cost --budget 150
```

---

## Commands

### 1. `status` - System Status

Check configuration, dependencies, and usage statistics.

```bash
python3 ai_media_cli.py status
```

**Output:**
- Configuration status
- Installed dependencies
- Usage statistics (total calls, cost)
- Output directory info

---

### 2. `generate` - Single Image

Generate a single image from a text prompt.

```bash
python3 ai_media_cli.py generate "PROMPT" [OPTIONS]
```

**Options:**
- `--route ROUTE` - Model route (default: 2K_2)
- `--aspect-ratio RATIO` - Aspect ratio (default: 1:1)
- `--cost COST` - Cost per image (default: 0.045)

**Examples:**

```bash
# Basic generation
python3 ai_media_cli.py generate "a mountain landscape"

# Wide format
python3 ai_media_cli.py generate "cityscape" --aspect-ratio 16:9

# Custom route
python3 ai_media_cli.py generate "portrait" --route 4K_2
```

**Aspect Ratios:**
- `1:1` - Square (Instagram)
- `16:9` - Wide (YouTube, presentations)
- `9:16` - Vertical (Stories, Reels)
- `4:3` - Standard
- `3:2` - Photography
- `4:5` - Portrait
- `21:9` - Ultra-wide

---

### 3. `batch` - Batch Processing

Process multiple prompts from a file.

```bash
python3 ai_media_cli.py batch PROMPTS_FILE [OPTIONS]
```

**Options:**
- `--route ROUTE` - Model route (default: 2K_2)
- `--aspect-ratio RATIO` - Aspect ratio (default: 1:1)
- `--workers N` - Parallel workers (default: 3)
- `--max-cost COST` - Maximum cost limit (default: 100)
- `--output DIR` - Output directory (default: outputs/batch)
- `--save-results` - Save results to JSON

**Prompts File Format:**
```text
a beautiful sunset over mountains
a futuristic cityscape
a cozy coffee shop interior
a tropical beach
```

**Examples:**

```bash
# Basic batch
python3 ai_media_cli.py batch prompts.txt

# High-volume batch with limits
python3 ai_media_cli.py batch prompts.txt \
  --workers 5 \
  --max-cost 10.0 \
  --save-results

# Custom settings
python3 ai_media_cli.py batch marketing_prompts.txt \
  --route 2K_2 \
  --aspect-ratio 16:9 \
  --workers 3 \
  --output outputs/marketing
```

**Progress Output:**
```
[████████████████████████░░░░░░░░] 60.0% | ✓45 ✗3 / 80
```

**Summary:**
```
Batch Processing Summary
======================================================================
Total Jobs: 50
Completed: 48 (✓)
Failed: 2 (✗)
Success Rate: 96.0%
Total Cost: $2.16
Duration: 245.3s
Avg Time/Job: 4.9s
```

---

### 4. `cost` - Cost Management

View cost statistics and budget status.

```bash
python3 ai_media_cli.py cost [OPTIONS]
```

**Options:**
- `--budget AMOUNT` - Monthly budget for comparison
- `--days N` - Days to include (default: 30)
- `--export FILE` - Export to CSV

**Examples:**

```bash
# Basic cost summary
python3 ai_media_cli.py cost

# Check budget status
python3 ai_media_cli.py cost --budget 150

# Last 7 days
python3 ai_media_cli.py cost --days 7

# Export to CSV
python3 ai_media_cli.py cost --export costs.csv
```

**Budget Status Output:**
```
Budget Status:
==================================================
Monthly Budget: $150.00
Current Spend: $67.50
Remaining: $82.50
Percent Used: 45.0%

Days Elapsed: 15
Avg Daily Spend: $4.50
Projected Monthly: $135.00

✓ Budget on track
```

**Alert Levels:**
- ✓ `ok` - On track
- ⚠️ `warning` - Spending faster than expected
- ⚠️ `high` - Approaching budget limit (>90%)
- ⚠️ `critical` - Budget exceeded

---

## Common Workflows

### Daily Content Generation

```bash
# 1. Create prompts file
cat > daily_prompts.txt << EOF
product showcase - professional lighting
lifestyle shot - morning coffee
brand story - behind the scenes
EOF

# 2. Generate images
python3 ai_media_cli.py batch daily_prompts.txt \
  --aspect-ratio 1:1 \
  --output outputs/daily

# 3. Check costs
python3 ai_media_cli.py cost --budget 150
```

### Marketing Campaign

```bash
# 1. Prepare prompts (50 variations)
# prompts.txt contains 50 lines

# 2. Process with cost limit
python3 ai_media_cli.py batch prompts.txt \
  --workers 5 \
  --max-cost 5.0 \
  --aspect-ratio 16:9 \
  --output outputs/campaign_2024_03 \
  --save-results

# 3. Export cost report
python3 ai_media_cli.py cost --export campaign_costs.csv
```

### A/B Testing

```bash
# Test different prompts
cat > test_prompts.txt << EOF
product - minimalist style
product - vibrant colors
product - natural lighting
product - studio setup
EOF

# Generate variations (5 each = 20 total)
for i in {1..5}; do
  cat test_prompts.txt >> all_tests.txt
done

python3 ai_media_cli.py batch all_tests.txt \
  --aspect-ratio 1:1 \
  --output outputs/ab_test
```

### Weekly Report

```bash
# Generate weekly cost report
python3 ai_media_cli.py cost --days 7 > weekly_report.txt

# Export detailed data
python3 ai_media_cli.py cost --export weekly_costs.csv

# Check status
python3 ai_media_cli.py status >> weekly_report.txt
```

---

## Tips & Best Practices

### Performance

1. **Parallel Workers:**
   - Use 3 workers for normal operations
   - Use 5+ workers for high-volume batches
   - Reduce to 1-2 if experiencing rate limits

2. **Batch Size:**
   - Small batches: 10-50 images
   - Medium batches: 50-200 images
   - Large batches: 200+ images (use `--max-cost` limit)

3. **Route Selection:**
   - `2K_2` or `2K_5` for most use cases
   - `4K_2` or `4K_5` for higher quality

### Cost Management

1. **Always set `--max-cost` for large batches:**
   ```bash
   python3 ai_media_cli.py batch large.txt --max-cost 10.0
   ```

2. **Monitor budget weekly:**
   ```bash
   python3 ai_media_cli.py cost --budget 150
   ```

3. **Export costs for accounting:**
   ```bash
   python3 ai_media_cli.py cost --export monthly_$(date +%Y_%m).csv
   ```

### Error Handling

1. **Save results for debugging:**
   ```bash
   python3 ai_media_cli.py batch prompts.txt --save-results
   # Creates: batch_results_prompts.json
   ```

2. **Check logs for failures:**
   ```bash
   grep "failed" batch_results_prompts.json
   ```

3. **Reprocess failed jobs:**
   - Extract failed prompts from JSON
   - Create new prompts file
   - Rerun batch

---

## Troubleshooting

### "Configuration not found"

```bash
# Run setup wizard
python3 quick_start.py
```

### "API credentials not found"

Check your `.env` file contains:
```
BANANA_PRO_API_KEY=your-key-here
BANANA_PRO_BASE_URL=https://api.provider.com
```

### "Missing dependencies"

```bash
# Install required
pip install requests

# Install optional (for video)
pip install opencv-python moviepy ffmpeg-python
```

### Rate Limiting

Reduce workers:
```bash
python3 ai_media_cli.py batch prompts.txt --workers 1
```

### Cost Exceeded

Lower max cost or process in chunks:
```bash
python3 ai_media_cli.py batch prompts.txt --max-cost 5.0
```

---

## Advanced Usage

### Automation with Cron

```bash
# Daily generation at 2 AM
crontab -e

# Add:
0 2 * * * cd /path/to/ai-media && python3 ai_media_cli.py batch daily.txt --max-cost 5
```

### Shell Scripts

```bash
#!/bin/bash
# generate_marketing.sh

DATE=$(date +%Y_%m_%d)
OUTPUT="outputs/marketing_$DATE"

python3 ai_media_cli.py batch marketing.txt \
  --aspect-ratio 16:9 \
  --output "$OUTPUT" \
  --max-cost 10.0 \
  --save-results

python3 ai_media_cli.py cost --export "costs_$DATE.csv"
```

### Piping and Filtering

```bash
# Generate from stdin
echo "a sunset" | python3 -c "
import sys
from banana_pro_with_tracking import BananaProWithTracking
client = BananaProWithTracking(...)
for line in sys.stdin:
    client.generate_image(line.strip())
"
```

---

## Integration with Other Tools

### FFmpeg (Video Creation)

```bash
# Generate images, then create video
python3 ai_media_cli.py batch scenes.txt --output outputs/video_frames

# Create video from images
ffmpeg -framerate 1 -pattern_type glob -i 'outputs/video_frames/*.png' \
  -c:v libx264 -pix_fmt yuv420p output.mp4
```

### ImageMagick (Batch Processing)

```bash
# Generate images
python3 ai_media_cli.py batch prompts.txt --output outputs/raw

# Add watermark to all
for img in outputs/raw/*.png; do
  convert "$img" -pointsize 30 -fill white \
    -annotate +10+30 'Your Brand' "outputs/final/$(basename $img)"
done
```

---

## Reference

### Exit Codes

- `0` - Success
- `1` - Error (configuration, API, etc.)
- `130` - Interrupted by user (Ctrl+C)

### Environment Variables

```bash
# Override .env file
export BANANA_PRO_API_KEY="key"
export BANANA_PRO_BASE_URL="https://api.provider.com"

python3 ai_media_cli.py generate "sunset"
```

### File Locations

- Config: `.env`
- Cost data: `cost_data.json`
- Outputs: `outputs/` (configurable)
- Batch results: `batch_results_*.json`

---

**For more information:**
- `PRODUCTION_FEATURES.md` - Feature overview
- `DEVELOPER_GUIDE.md` - API documentation
- `example_usage.py` - Python code examples

**Support:** 开发一号 (Development Agent #1)
