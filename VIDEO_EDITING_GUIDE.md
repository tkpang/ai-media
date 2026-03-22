# Video Editing Workflow - Ubuntu Platform

**Date:** 2026-03-22
**Platform:** Ubuntu Linux
**Status:** 📋 Planning - Awaiting requirements definition

---

## Overview

This guide covers video editing tools and workflows for the Paperclip AI media system running on Ubuntu.

Two main approaches are available:
1. **Programmatic/Automated** - For batch processing and scripted workflows
2. **Manual/GUI** - For detailed creative editing requiring human judgment

---

## Approach 1: Programmatic Video Editing (Recommended for Automation)

### Tools Stack

#### 1. FFmpeg (Core Tool) ⭐ PRIMARY RECOMMENDATION

**What it does:** Command-line video processing powerhouse
**Best for:** Format conversion, trimming, concatenation, filters, compression

**Installation:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Common Operations:**

```bash
# Convert format
ffmpeg -i input.mp4 output.webm

# Trim video (from 10s to 30s)
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:30 -c copy output.mp4

# Resize video
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Concatenate videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# Add audio to video
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -acodec mp3 audio.mp3

# Add watermark
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4

# Compress video
ffmpeg -i input.mp4 -vcodec h264 -crf 28 output.mp4
```

#### 2. Python Libraries

**a) opencv-python** - Computer vision and video processing

**Installation:**
```bash
pip install opencv-python opencv-contrib-python
```

**Use cases:**
- Frame-by-frame manipulation
- Object detection/tracking
- Color correction
- Stabilization
- Face detection/blurring

**Example:**
```python
import cv2

# Open video
cap = cv2.VideoCapture('input.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame (e.g., add filter)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    out.write(colored)

cap.release()
out.release()
```

**b) moviepy** - High-level video editing

**Installation:**
```bash
pip install moviepy
```

**Use cases:**
- Clip manipulation
- Text/title overlays
- Transitions
- Audio mixing
- GIF creation

**Example:**
```python
from moviepy.editor import *

# Load clips
clip1 = VideoFileClip("intro.mp4")
clip2 = VideoFileClip("main.mp4")
clip3 = VideoFileClip("outro.mp4")

# Concatenate
final = concatenate_videoclips([clip1, clip2, clip3])

# Add text
txt = TextClip("Subscribe!", fontsize=70, color='white')
txt = txt.set_pos('center').set_duration(3)
final = CompositeVideoClip([final, txt.set_start(5)])

# Export
final.write_videofile("output.mp4")
```

**c) ffmpeg-python** - Python wrapper for FFmpeg

**Installation:**
```bash
pip install ffmpeg-python
```

**Use cases:**
- Complex FFmpeg commands from Python
- Programmatic video pipelines
- Error handling for FFmpeg operations

**Example:**
```python
import ffmpeg

# Trim and resize
stream = ffmpeg.input('input.mp4')
stream = ffmpeg.trim(stream, start=10, end=30)
stream = ffmpeg.filter(stream, 'scale', 1280, 720)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)
```

---

## Approach 2: GUI-Based Manual Editing

### Tools

#### 1. Kdenlive (Recommended GUI Editor)

**What it is:** Professional-grade open-source video editor
**Best for:** Multi-track editing, effects, color grading, titles

**Installation:**
```bash
sudo apt install kdenlive
```

**Features:**
- Multi-track timeline
- Transitions and effects
- Keyframe animation
- Color grading
- Audio mixing
- Title/text overlays
- Green screen (chroma key)

**Note:** Requires desktop environment (GUI). Not suitable for headless servers.

#### 2. Shotcut (Alternative)

**Installation:**
```bash
sudo snap install shotcut --classic
```

**Features:** Similar to Kdenlive, slightly simpler interface

#### 3. OpenShot (Simple Option)

**Installation:**
```bash
sudo apt install openshot-qt
```

**Features:** Beginner-friendly, basic editing

---

## Recommended Workflow Architecture

### For Paperclip AI Media System

**Phase 1: AI Generation**
- Generate images with Banana Pro
- Generate videos with Seedance 2.0

**Phase 2: Automated Processing (Programmatic)**
```
FFmpeg + Python Scripts
├── Format conversion (ensure compatibility)
├── Trimming/cutting (remove unwanted sections)
├── Concatenation (combine multiple clips)
├── Basic filters (brightness, contrast, saturation)
├── Compression (optimize file size)
└── Watermarking (branding)
```

**Phase 3: Manual Refinement (if needed)**
```
Kdenlive (GUI)
├── Fine-tuning cuts
├── Advanced color grading
├── Complex transitions
├── Title animations
└── Audio mixing
```

---

## Workflow Templates

### Template 1: Social Media Video Creation (Automated)

**Goal:** Create Instagram/TikTok videos from AI-generated content

**Steps:**
1. Generate images with Banana Pro (9:16 aspect ratio)
2. Create slideshow with transitions (moviepy)
3. Add background music (FFmpeg)
4. Add text overlays (moviepy)
5. Export optimized for social media (FFmpeg compression)

**Script:** `workflows/social_media_video.py`

### Template 2: YouTube Content Pipeline (Semi-automated)

**Goal:** Create YouTube videos with intro/outro

**Steps:**
1. Generate B-roll with Seedance 2.0
2. Concatenate with intro/outro (FFmpeg)
3. Add background music (FFmpeg)
4. Add subscribe animation (moviepy)
5. Compress and optimize (FFmpeg)

**Script:** `workflows/youtube_pipeline.py`

### Template 3: Batch Video Processing (Automated)

**Goal:** Process 100s of videos consistently

**Steps:**
1. Watch input folder for new videos
2. Apply standard filters (brightness, contrast)
3. Add watermark
4. Compress to target file size
5. Move to output folder

**Script:** `workflows/batch_processor.py`

---

## System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Disk: 50GB free (for temporary video files)
- GPU: Not required (but speeds up encoding)

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 100GB+ SSD
- GPU: NVIDIA with CUDA (for hardware acceleration)

### Check Current System
```bash
# CPU info
lscpu | grep "Model name"
nproc  # Number of cores

# RAM
free -h

# Disk space
df -h

# GPU (if NVIDIA)
nvidia-smi
```

---

## Hardware Acceleration

### Enable NVIDIA GPU Acceleration (if available)

```bash
# Install NVIDIA drivers and CUDA
sudo apt install nvidia-driver-525 nvidia-cuda-toolkit

# FFmpeg with GPU support
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

**Speed improvement:** 5-10x faster encoding

---

## Python Workflow Skeleton

```python
#!/usr/bin/env python3
"""
Video editing workflow template
"""

import ffmpeg
from moviepy.editor import *
from pathlib import Path

class VideoProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def trim(self, start, end):
        """Trim video to specified time range"""
        stream = ffmpeg.input(self.input_path)
        stream = ffmpeg.trim(stream, start=start, end=end)
        stream = ffmpeg.output(stream, 'temp_trimmed.mp4')
        ffmpeg.run(stream)
        return 'temp_trimmed.mp4'

    def add_watermark(self, watermark_path, position='bottom-right'):
        """Add watermark to video"""
        # Implementation using FFmpeg overlay filter
        pass

    def compress(self, target_size_mb):
        """Compress video to target file size"""
        # Implementation using FFmpeg CRF
        pass

    def add_audio(self, audio_path):
        """Add background music"""
        # Implementation using FFmpeg audio mixing
        pass

    def export(self):
        """Export final video"""
        # Final export logic
        pass

# Example usage
processor = VideoProcessor('input.mp4', 'output.mp4')
processor.trim(10, 60)
processor.add_watermark('logo.png')
processor.compress(50)  # 50MB
processor.export()
```

---

## Cost Considerations

### Open Source = Free
All recommended tools (FFmpeg, OpenCV, MoviePy, Kdenlive) are **completely free** and open source.

### Compute Costs
- **Processing time:** Depends on video length and complexity
- **Storage:** Video files can be large (1GB+ for 10min 1080p)
- **Bandwidth:** If uploading/downloading videos

### Estimated Processing Time
- 1-minute 1080p video:
  - Basic trim/concat: ~5 seconds
  - Filters/effects: ~30 seconds
  - Full re-encode: ~2-5 minutes (CPU) or ~30 seconds (GPU)

---

## Deliverables (When Requirements Are Defined)

Once board specifies video editing requirements, we will create:

1. **Custom workflow scripts** for specific use cases
2. **Batch processing system** for automation
3. **Quality control tools** for validation
4. **Documentation** with examples
5. **Testing suite** for reliability

---

## Questions for Board

To build the right video editing workflow, we need to understand:

1. **What types of edits are most common?**
   - Simple concatenation?
   - Complex multi-track editing?
   - Effects and transitions?
   - Color grading?

2. **Volume expectations?**
   - How many videos per day/week?
   - Average video length?
   - Output quality requirements?

3. **Automation level?**
   - Fully automated (no human input)?
   - Semi-automated (human review/approval)?
   - Manual editing with tools provided?

4. **Output destinations?**
   - YouTube?
   - Instagram/TikTok?
   - Internal use?
   - Client deliverables?

5. **Integration requirements?**
   - Should video editing tie directly to Banana Pro/Seedance outputs?
   - Or standalone system?

---

## Recommended Next Step

**Option A:** Define specific use case
- Example: "Create 60-second Instagram reels from AI-generated images with music"
- We build custom automated workflow for this exact need

**Option B:** Start with general toolkit
- Install FFmpeg + Python libraries
- Create example scripts for common operations
- Board experiments and identifies needs
- We refine based on feedback

**Recommendation:** Start with Option B (general toolkit) to discover actual needs through experimentation.

---

## Installation Quick Start

```bash
# Install core tools
sudo apt update
sudo apt install ffmpeg

# Install Python libraries
pip install opencv-python moviepy ffmpeg-python pillow

# Optional: Install GUI editor
sudo apt install kdenlive

# Verify installations
ffmpeg -version
python3 -c "import cv2, moviepy; print('Libraries OK')"
```

**Time to setup:** ~10 minutes

---

**Status:** Ready to implement once requirements are defined.
