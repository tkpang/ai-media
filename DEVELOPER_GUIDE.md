# Developer Guide - AI Media Workspace

**For:** Developers working on the AI Media integration
**Last Updated:** 2026-03-22

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Media Workspace                       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │ Banana  │        │Seedance │        │  Video  │
   │   Pro   │        │   2.0   │        │ Editing │
   │ (Image) │        │ (Video) │        │ (Post)  │
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                   │
        └──────────────────┴───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Storage   │
                    │  (outputs/) │
                    └─────────────┘
```

---

## Code Structure

### Core Components

#### 1. Banana Pro Client (`banana_pro_gemini.py`)

**Purpose:** Image generation using Google's Gemini API format

**Key Class:**
```python
class BananaProGeminiClient:
    def __init__(self, api_key: str, base_url: str)
    def generate_image(prompt, route, aspect_ratio, save_path) -> dict
    def list_models() -> dict
```

**Routes Available:**
- 2K: `2K_1` through `2K_7` (cost-optimized: 2, 5)
- 4K: `4K_1` through `4K_7` (cost-optimized: 2, 5)

**Aspect Ratios:**
- `1:1`, `16:9`, `9:16`, `4:3`, `3:2`, `4:5`, `21:9`

**Example:**
```python
client = BananaProGeminiClient(api_key="sk-xxx", base_url="https://api.provider.com")
result = client.generate_image(
    prompt="A red apple",
    route="2K_2",
    aspect_ratio="1:1"
)
# Returns: {"saved_to": "path/to/image.png", "candidates": [...]}
```

#### 2. Configuration Management

**Environment Variables (.env):**
```bash
BANANA_PRO_API_KEY=sk-xxx
BANANA_PRO_BASE_URL=https://api.provider.com
SEEDANCE_API_KEY=sk-yyy
SEEDANCE_BASE_URL=https://api.seedance.com
OUTPUT_DIR=./outputs
```

**Loading Config:**
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BANANA_PRO_API_KEY")
base_url = os.getenv("BANANA_PRO_BASE_URL")
```

#### 3. Error Handling

**Common Errors:**

```python
# Authentication Error
try:
    client.generate_image(...)
except requests.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")

# Network Error
except requests.Timeout:
    print("Request timed out")
except requests.ConnectionError:
    print("Connection failed")

# Validation Error
except ValueError as e:
    print(f"Invalid parameters: {e}")
```

---

## Development Workflow

### 1. Local Development Setup

```bash
# Clone or navigate to workspace
cd /home/pangtiankai/paperclip/ai-media

# Install dependencies
pip install requests python-dotenv

# Optional: Video editing libraries
pip install opencv-python moviepy ffmpeg-python

# Create .env file
cp .env.example .env  # (create .env.example if needed)
# Edit .env with your API credentials

# Run quick start
python3 quick_start.py
```

### 2. Testing Your Changes

```bash
# Unit test individual function
python3 -c "from banana_pro_gemini import BananaProGeminiClient; \
    client = BananaProGeminiClient(api_key='xxx', base_url='https://api.provider.com'); \
    print(client.list_models())"

# Integration test
python3 example_usage.py

# Full test suite (when API configured)
python3 TESTING_CHECKLIST.md  # Use as checklist, not executable
```

### 3. Adding New Features

**Example: Add a new image filter**

```python
# In banana_pro_gemini.py

def generate_image_with_filter(
    self,
    prompt: str,
    filter_type: str = "none",
    **kwargs
) -> dict:
    """
    Generate image with post-processing filter

    Args:
        prompt: Image description
        filter_type: Filter to apply (none, sepia, grayscale, blur)
        **kwargs: Other generate_image parameters
    """
    # Generate base image
    result = self.generate_image(prompt, **kwargs)

    # Apply filter if needed
    if filter_type != "none":
        image_path = result['saved_to']
        filtered_path = self._apply_filter(image_path, filter_type)
        result['saved_to'] = filtered_path

    return result

def _apply_filter(self, image_path: str, filter_type: str) -> str:
    """Apply filter using OpenCV"""
    import cv2

    img = cv2.imread(image_path)

    if filter_type == "grayscale":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif filter_type == "sepia":
        # Sepia filter transformation
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        img = cv2.transform(img, kernel)
    # ... more filters

    output_path = image_path.replace('.png', f'_{filter_type}.png')
    cv2.imwrite(output_path, img)
    return output_path
```

---

## API Integration Guide

### Switching API Providers

**Current:** Blocked (xais1.dchai.cn is web UI)
**Target:** APIYI or LaoZhang.ai

**Changes needed:**

1. Update `.env`:
```bash
BANANA_PRO_BASE_URL=https://api.apiyi.com  # or LaoZhang endpoint
BANANA_PRO_API_KEY=sk-new-key-here
```

2. Test connection:
```bash
python3 test_banana_pro.py
```

3. Verify endpoint format:
```python
# Endpoint should be:
# POST {base_url}/v1beta/models/{model_id}:generateContent

# If provider uses different format, update client:
def generate_image(self, ...):
    url = f"{self.base_url}/v1beta/models/{model_id}:generateContent"
    # Adjust URL format based on provider's API spec
```

### Adding Seedance 2.0

**Create:** `seedance_client.py`

```python
#!/usr/bin/env python3
"""
Seedance 2.0 Video Generation Client
"""

import requests
import time
from pathlib import Path

class SeedanceClient:
    def __init__(self, api_key: str, base_url: str = "https://api.provider.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_video(
        self,
        prompt: str,
        duration: int = 10,
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        save_path: str = None
    ) -> dict:
        """
        Generate video from text prompt

        Args:
            prompt: Video description
            duration: Length in seconds (max 20)
            resolution: "720p" or "1080p"
            aspect_ratio: Video aspect ratio
            save_path: Where to save video

        Returns:
            dict with video_url, cost, generation_time
        """
        url = f"{self.base_url}/v1/video/generate"

        payload = {
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio
        }

        response = requests.post(url, headers=self.headers, json=payload, timeout=300)
        response.raise_for_status()

        result = response.json()

        # Download video
        video_url = result['video_url']
        if save_path is None:
            save_path = f"outputs/video_{int(time.time())}.mp4"

        self._download_video(video_url, save_path)
        result['saved_to'] = save_path

        return result

    def _download_video(self, url: str, save_path: str):
        """Download video from URL"""
        response = requests.get(url, stream=True)
        response.raise_for_status()

        Path(save_path).parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
```

---

## Common Development Tasks

### 1. Debug API Calls

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Add to client
class BananaProGeminiClient:
    def generate_image(self, ...):
        logging.debug(f"Request URL: {url}")
        logging.debug(f"Payload: {payload}")

        response = requests.post(...)

        logging.debug(f"Response status: {response.status_code}")
        logging.debug(f"Response body: {response.text[:500]}")
```

### 2. Add Retry Logic

```python
from functools import wraps
import time

def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

# Usage
@retry_on_failure(max_retries=3)
def generate_image(self, ...):
    # ... existing code
```

### 3. Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.total_cost = 0
        self.generations = 0

    def track(self, cost: float):
        self.total_cost += cost
        self.generations += 1

    def report(self):
        avg = self.total_cost / self.generations if self.generations > 0 else 0
        return {
            "total": self.total_cost,
            "count": self.generations,
            "average": avg
        }

# In client
class BananaProGeminiClient:
    def __init__(self, ...):
        # ... existing code
        self.cost_tracker = CostTracker()

    def generate_image(self, ...):
        result = # ... generate image
        cost = 0.045  # or calculate based on route/resolution
        self.cost_tracker.track(cost)
        result['cost'] = cost
        return result
```

### 4. Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_generate(client, prompts, max_workers=5):
    """Generate multiple images concurrently"""
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                client.generate_image,
                prompt=prompt,
                route="2K_2"
            ): prompt
            for prompt in prompts
        }

        for future in as_completed(futures):
            prompt = futures[future]
            try:
                result = future.result()
                results.append((prompt, result))
                print(f"✓ Completed: {prompt}")
            except Exception as e:
                print(f"✗ Failed: {prompt} - {e}")

    return results
```

---

## Performance Optimization

### 1. Caching Responses

```python
import hashlib
import json
from pathlib import Path

class CachedClient:
    def __init__(self, client, cache_dir="./cache"):
        self.client = client
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def generate_image(self, prompt, **kwargs):
        # Create cache key from parameters
        cache_key = hashlib.md5(
            json.dumps({"prompt": prompt, **kwargs}, sort_keys=True).encode()
        ).hexdigest()

        cache_file = self.cache_dir / f"{cache_key}.json"

        # Check cache
        if cache_file.exists():
            print("Using cached result")
            with open(cache_file) as f:
                return json.load(f)

        # Generate new
        result = self.client.generate_image(prompt, **kwargs)

        # Save to cache
        with open(cache_file, 'w') as f:
            json.dump(result, f)

        return result
```

### 2. Async Generation

```python
import asyncio
import aiohttp

class AsyncBananaProClient:
    async def generate_image_async(self, prompt, **kwargs):
        """Async version of generate_image"""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                result = await response.json()
                # ... process result
                return result

# Usage
async def main():
    client = AsyncBananaProClient(...)
    results = await asyncio.gather(
        client.generate_image_async("prompt 1"),
        client.generate_image_async("prompt 2"),
        client.generate_image_async("prompt 3"),
    )
```

---

## Contributing Guidelines

### Code Style

- Follow PEP 8
- Use type hints where possible
- Document all public methods
- Keep functions under 50 lines

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/add-filters

# Make changes
# ... edit files

# Test changes
python3 test_banana_pro.py

# Commit
git add .
git commit -m "Add image filter support"

# Push
git push origin feature/add-filters
```

### Documentation

- Update README.md for user-facing changes
- Update this DEVELOPER_GUIDE.md for code changes
- Add examples to example_usage.py
- Update TESTING_CHECKLIST.md with new test cases

---

## Troubleshooting

### Issue: "API returns HTML instead of JSON"

**Solution:** Wrong endpoint. Check provider documentation for correct base URL.

### Issue: "401 Unauthorized"

**Solution:** Invalid API key. Check `.env` file and provider dashboard.

### Issue: "Timeout errors"

**Solution:** Increase timeout in requests:
```python
response = requests.post(url, json=payload, timeout=300)  # 5 minutes
```

### Issue: "Out of memory during video processing"

**Solution:** Process videos in chunks:
```python
# For large videos, use streaming
cap = cv2.VideoCapture('large_video.mp4')
# Process frame by frame, release each frame after processing
```

---

## Contact & Support

**For technical issues:**
- Check `TESTING_CHECKLIST.md` for diagnostics
- Review `BOARD_SUMMARY.md` for known issues
- Contact Development Agent #2 (开发二号)

**For API issues:**
- Check provider's documentation
- Verify API key and base URL
- Test with `test_banana_pro.py`

---

**Last Updated:** 2026-03-22
**Maintainer:** Development Agent #2 (开发二号)
