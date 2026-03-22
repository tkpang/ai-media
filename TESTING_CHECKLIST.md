# AI Media Integration - Testing Checklist

**Purpose:** Comprehensive testing plan for Banana Pro, Seedance 2.0, and video editing tools
**Last Updated:** 2026-03-22

---

## Phase 1: Banana Pro Image Generation Testing

### 1.1 API Connectivity

- [ ] API endpoint is accessible (returns JSON, not HTML)
- [ ] Authentication successful with API key
- [ ] `/v1/models` endpoint returns model list
- [ ] Base URL is correct and working
- [ ] SSL/TLS certificate is valid
- [ ] Response times are acceptable (<5 seconds for metadata calls)

### 1.2 Model Availability

Test all cost-optimized routes:
- [ ] Route 2K_2 is available and working
- [ ] Route 2K_5 is available and working
- [ ] Route 4K_2 is available and working
- [ ] Route 4K_5 is available and working

Verify model names match expected format:
- [ ] `Nano_Banana_Pro_2K_2` endpoint exists
- [ ] Model returns proper generateContent responses

### 1.3 Image Generation - Basic Functionality

Simple prompt testing:
- [ ] Generate 1:1 square image (512x512 or similar)
- [ ] Generate 16:9 landscape image
- [ ] Generate 9:16 portrait image
- [ ] All images save successfully as PNG/JPEG
- [ ] File sizes are reasonable (not corrupted)
- [ ] Images match prompt description (visual quality check)

### 1.4 Aspect Ratio Testing

Test all supported ratios:
- [ ] 1:1 (Square - Instagram posts)
- [ ] 16:9 (Landscape - YouTube thumbnails)
- [ ] 9:16 (Portrait - Stories/TikTok)
- [ ] 4:3 (Classic presentation)
- [ ] 3:2 (Photography)
- [ ] 4:5 (Portrait - Instagram)
- [ ] 21:9 (Ultrawide wallpaper)

### 1.5 Resolution Testing

- [ ] 2K images are at expected resolution (~2048px width)
- [ ] 4K images are at expected resolution (~4096px width)
- [ ] Image quality is sharp and detailed
- [ ] No unexpected upscaling/downscaling artifacts

### 1.6 Prompt Complexity

Test varying prompt complexity:
- [ ] Simple prompt: "A red apple"
- [ ] Detailed prompt: "A photorealistic red apple on white marble surface, studio lighting, 4K, professional photography"
- [ ] Complex scene: "Sunset over mountains with lake reflection, dramatic clouds, golden hour, 8K wallpaper quality"
- [ ] Style modifiers work: "cyberpunk", "watercolor", "photorealistic"

### 1.7 Error Handling

- [ ] Invalid API key returns proper error message
- [ ] Invalid route name returns proper error message
- [ ] Network timeout is handled gracefully
- [ ] Malformed requests return useful error messages
- [ ] Content policy violations return clear error (if applicable)
- [ ] Rate limiting is detected and handled

### 1.8 Performance Testing

- [ ] Single image generation time is acceptable (<60 seconds)
- [ ] Batch generation (5 images) works without failures
- [ ] Concurrent requests don't cause errors
- [ ] Memory usage is reasonable during generation
- [ ] No memory leaks after multiple generations

### 1.9 Cost Tracking

- [ ] Cost per image matches expectations ($0.045 - $0.05)
- [ ] Billing increments are correct
- [ ] Cost tracking in logs is accurate
- [ ] Monthly spending can be monitored

### 1.10 File Management

- [ ] Images save to correct directory
- [ ] Filenames are unique (timestamp-based)
- [ ] Metadata is preserved (prompt, settings)
- [ ] Cleanup of temporary files works
- [ ] Storage space is monitored

---

## Phase 2: Seedance 2.0 Video Generation Testing

### 2.1 API Connectivity

- [ ] API endpoint is accessible
- [ ] Authentication successful with API key
- [ ] Provider-specific endpoints are working
- [ ] Response format matches documentation

### 2.2 Text-to-Video Generation

Basic tests:
- [ ] Generate 5-second video from simple prompt
- [ ] Generate 10-second video from detailed prompt
- [ ] Generate 20-second video (maximum length)
- [ ] Videos download successfully
- [ ] File format is playable (MP4/WebM)

### 2.3 Image-to-Video Generation

- [ ] Single image can be animated
- [ ] Motion is coherent and realistic
- [ ] Camera movements are smooth
- [ ] Physics simulation is believable

### 2.4 Multi-modal Generation

- [ ] Text + Image input works
- [ ] Text + Audio input works
- [ ] Multiple reference files (up to 12) are accepted
- [ ] Combined modalities produce coherent output

### 2.5 Resolution & Quality

- [ ] 720p output is available and acceptable quality
- [ ] 1080p output is available and high quality
- [ ] Frame rate is smooth (24/30/60fps)
- [ ] No compression artifacts
- [ ] Colors are accurate

### 2.6 Audio Testing

- [ ] Native audio generation works
- [ ] Audio matches video content
- [ ] Audio quality is clear (no distortion)
- [ ] Audio volume is appropriate
- [ ] Silent generation option works (if available)

### 2.7 Multi-shot Testing

- [ ] Scene cuts are coherent
- [ ] Transitions between shots are natural
- [ ] Story flow makes sense
- [ ] No jarring discontinuities

### 2.8 Performance & Timing

- [ ] 5-second video generation time is acceptable
- [ ] 10-second video generation time is acceptable
- [ ] 20-second video generation time is acceptable
- [ ] Queue position tracking works
- [ ] Progress updates are available

### 2.9 Error Handling

- [ ] Invalid prompts return clear errors
- [ ] Timeout errors are handled
- [ ] Content moderation rejections are clear
- [ ] Failed generations can be retried
- [ ] Partial failures are handled gracefully

### 2.10 Cost Tracking

- [ ] Cost per second matches expectations (~$0.14/sec)
- [ ] Total cost per video is calculated correctly
- [ ] Billing matches actual usage
- [ ] Budget alerts work (if implemented)

---

## Phase 3: Video Editing Tools Testing

### 3.1 FFmpeg Installation & Functionality

- [ ] FFmpeg is installed and accessible
- [ ] Version is up-to-date
- [ ] All required codecs are available
- [ ] Hardware acceleration works (if GPU available)

Basic operations:
- [ ] Format conversion (MP4 to WebM)
- [ ] Video trimming (cut 10-30 seconds)
- [ ] Video concatenation (join 3 clips)
- [ ] Audio extraction
- [ ] Resolution scaling

### 3.2 Python Libraries

**OpenCV:**
- [ ] opencv-python is installed
- [ ] Can read video files
- [ ] Can write video files
- [ ] Frame processing works
- [ ] Color space conversions work

**MoviePy:**
- [ ] moviepy is installed
- [ ] Can load video clips
- [ ] Can concatenate clips
- [ ] Text overlays work
- [ ] Audio mixing works
- [ ] Export to MP4 works

**ffmpeg-python:**
- [ ] ffmpeg-python is installed
- [ ] Can execute FFmpeg commands
- [ ] Error handling works
- [ ] Complex filters work

### 3.3 Common Workflows

**Workflow 1: Concatenate multiple videos**
- [ ] Load 3+ video files
- [ ] Concatenate in order
- [ ] Export single output file
- [ ] Audio remains synced
- [ ] No frame drops

**Workflow 2: Add watermark**
- [ ] Load watermark image (PNG with transparency)
- [ ] Position watermark (4 corners + center)
- [ ] Watermark is visible but not intrusive
- [ ] Export maintains video quality

**Workflow 3: Compress video**
- [ ] Target file size is achieved
- [ ] Quality is acceptable
- [ ] Aspect ratio is maintained
- [ ] Audio quality is preserved

**Workflow 4: Add background music**
- [ ] Load audio file (MP3/WAV)
- [ ] Mix with existing audio or replace
- [ ] Audio levels are balanced
- [ ] Fade in/out works

**Workflow 5: Create slideshow from images**
- [ ] Load 5+ images
- [ ] Set duration per image (3-5 seconds)
- [ ] Add transitions between images
- [ ] Add background music
- [ ] Export as video

### 3.4 Performance Testing

- [ ] 1-minute video processes in reasonable time
- [ ] 10-minute video doesn't run out of memory
- [ ] Batch processing 10 videos works
- [ ] CPU usage is efficient
- [ ] GPU acceleration works (if available)

### 3.5 Quality Assurance

- [ ] Output videos play correctly in VLC
- [ ] Output videos play correctly in web browsers
- [ ] Output videos are compatible with YouTube
- [ ] Output videos are compatible with Instagram
- [ ] No audio/video sync issues

---

## Phase 4: Integration Testing

### 4.1 Banana Pro → Video Editing

- [ ] Generate 10 images with Banana Pro
- [ ] Create slideshow video from images
- [ ] Add background music
- [ ] Export for social media
- [ ] End-to-end workflow completes successfully

### 4.2 Seedance → Video Editing

- [ ] Generate video with Seedance 2.0
- [ ] Trim to desired length
- [ ] Add watermark/branding
- [ ] Compress for web delivery
- [ ] Export final video

### 4.3 Combined Workflow

- [ ] Generate intro image (Banana Pro)
- [ ] Generate main video (Seedance 2.0)
- [ ] Generate outro image (Banana Pro)
- [ ] Concatenate intro + video + outro
- [ ] Add background music
- [ ] Add text overlays
- [ ] Export final production

### 4.4 Batch Processing

- [ ] Generate 10 images in batch (Banana Pro)
- [ ] Generate 5 videos in batch (Seedance)
- [ ] Process all through video editing pipeline
- [ ] Export all with consistent quality
- [ ] Monitor costs throughout

### 4.5 Error Recovery

- [ ] If Banana Pro fails, workflow continues with defaults
- [ ] If Seedance fails, retry logic works
- [ ] If video editing fails, error is logged and reported
- [ ] Partial failures don't corrupt other outputs

---

## Phase 5: Production Readiness

### 5.1 Documentation

- [ ] All API endpoints are documented
- [ ] Example scripts are provided
- [ ] Common errors and solutions are listed
- [ ] Cost estimates are documented
- [ ] Best practices are defined

### 5.2 Monitoring

- [ ] API usage is logged
- [ ] Costs are tracked daily
- [ ] Error rates are monitored
- [ ] Performance metrics are collected
- [ ] Alerts are configured for failures

### 5.3 Security

- [ ] API keys are stored securely (not in code)
- [ ] Output files have correct permissions
- [ ] No sensitive data in logs
- [ ] Rate limiting is respected
- [ ] Input validation prevents injection attacks

### 5.4 Scalability

- [ ] Can handle 100 requests/day
- [ ] Can handle concurrent requests
- [ ] Storage scales with usage
- [ ] Costs remain predictable
- [ ] Performance doesn't degrade with load

### 5.5 Maintenance

- [ ] Dependencies are documented
- [ ] Update process is defined
- [ ] Backup/restore procedures exist
- [ ] Debugging tools are available
- [ ] Support contact info is documented

---

## Testing Results Template

```markdown
## Test Run: [Date]
**Tester:** [Name]
**Environment:** [Production/Staging/Local]

### Banana Pro
- ✅ Basic generation: PASS
- ✅ All aspect ratios: PASS
- ⚠️ 4K generation slow (90s): WARN
- ❌ Route 4K_7 failed: FAIL

### Seedance 2.0
- ✅ Text-to-video: PASS
- ✅ Image-to-video: PASS
- ✅ Audio quality: PASS

### Video Editing
- ✅ FFmpeg operations: PASS
- ✅ Concatenation: PASS
- ✅ Watermarking: PASS

### Integration
- ✅ End-to-end workflow: PASS
- ✅ Cost tracking: PASS

### Issues Found
1. [Issue description and resolution]
2. [Issue description and resolution]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Automated Testing Script

```python
#!/usr/bin/env python3
"""
Automated testing suite for AI Media tools
"""

import sys
from banana_pro_gemini import BananaProGeminiClient
# from seedance_client import SeedanceClient  # When implemented

def test_banana_pro():
    """Test Banana Pro image generation"""
    print("Testing Banana Pro...")
    try:
        client = BananaProGeminiClient(api_key="YOUR_KEY")

        # Test basic generation
        result = client.generate_image(
            prompt="Test image: red circle on white background",
            route="2K_2",
            aspect_ratio="1:1"
        )

        # Verify file exists
        assert Path(result['saved_to']).exists(), "Image file not found"

        print("✅ Banana Pro: PASS")
        return True
    except Exception as e:
        print(f"❌ Banana Pro: FAIL - {e}")
        return False

def test_video_editing():
    """Test video editing tools"""
    print("Testing video editing...")
    try:
        import cv2
        import moviepy
        import ffmpeg

        print("✅ Video Editing Libraries: PASS")
        return True
    except Exception as e:
        print(f"❌ Video Editing: FAIL - {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Media Integration Testing")
    print("=" * 60)

    results = {
        "Banana Pro": test_banana_pro(),
        "Video Editing": test_video_editing(),
    }

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
```

---

**Status:** Checklist ready for use once APIs are configured.

**Next Steps:**
1. Configure API credentials
2. Run Phase 1 tests (Banana Pro)
3. Document results
4. Move to Phase 2 (Seedance) when ready
