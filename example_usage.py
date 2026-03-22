#!/usr/bin/env python3
"""
Banana Pro - Example Usage Script
Demonstrates how to use the BananaProGeminiClient once API is working
"""

from banana_pro_gemini import BananaProGeminiClient
from pathlib import Path

def main():
    """Example workflows for common image generation tasks"""

    # Initialize client (replace with actual working API endpoint)
    API_KEY = "sk-Pi5Sc2cZfD7M9bkCHU2ly0OroaFoYirtteqIu1HwkssCsKL8"
    BASE_URL = "https://xais1.dchai.cn"  # Replace when working endpoint is provided

    client = BananaProGeminiClient(api_key=API_KEY, base_url=BASE_URL)

    print("=" * 70)
    print("Banana Pro - Image Generation Examples")
    print("=" * 70)

    # Example 1: Simple 2K image with cost optimization
    print("\n[Example 1] Cost-optimized 2K portrait")
    print("-" * 70)
    try:
        result = client.generate_image(
            prompt="Professional portrait of a business executive, confident smile, office background, natural lighting, high quality",
            route="2K_2",  # Cost-optimized route
            aspect_ratio="4:5",  # Portrait format
            save_path="outputs/portrait_executive.png"
        )
        print(f"✓ Saved to: {result['saved_to']}")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Example 2: Landscape 4K image
    print("\n[Example 2] 4K landscape wallpaper")
    print("-" * 70)
    try:
        result = client.generate_image(
            prompt="Stunning mountain landscape at sunset, golden hour, dramatic clouds, crystal clear lake reflection, 8K wallpaper quality",
            route="4K_5",  # 4K cost-optimized
            aspect_ratio="21:9",  # Ultrawide
            save_path="outputs/landscape_mountains.png"
        )
        print(f"✓ Saved to: {result['saved_to']}")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Example 3: Social media content
    print("\n[Example 3] Instagram post (1:1)")
    print("-" * 70)
    try:
        result = client.generate_image(
            prompt="Minimalist product photography, modern smartphone on marble surface, soft shadows, premium aesthetic, instagram worthy",
            route="2K_2",
            aspect_ratio="1:1",
            save_path="outputs/social_product.png"
        )
        print(f"✓ Saved to: {result['saved_to']}")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Example 4: YouTube thumbnail
    print("\n[Example 4] YouTube thumbnail (16:9)")
    print("-" * 70)
    try:
        result = client.generate_image(
            prompt="Tech review thumbnail, excited person pointing at laptop, vibrant colors, bold composition, YouTube style",
            route="2K_5",
            aspect_ratio="16:9",
            save_path="outputs/youtube_thumbnail.png"
        )
        print(f"✓ Saved to: {result['saved_to']}")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Example 5: Batch generation with different routes
    print("\n[Example 5] Batch generation - testing route quality")
    print("-" * 70)
    base_prompt = "Photorealistic red apple on white background, studio lighting"
    test_routes = ["2K_1", "2K_2", "2K_5"]

    for route in test_routes:
        try:
            print(f"  Testing route {route}...")
            result = client.generate_image(
                prompt=base_prompt,
                route=route,
                aspect_ratio="1:1",
                save_path=f"outputs/apple_{route}.png"
            )
            print(f"  ✓ {route} completed")
        except Exception as e:
            print(f"  ✗ {route} failed: {e}")

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nRecommended routes for cost optimization:")
    print("  • 2K images: Use routes 2K_2 or 2K_5")
    print("  • 4K images: Use routes 4K_2 or 4K_5")
    print("\nAspect ratios available:")
    print("  • 1:1   - Square (Instagram posts)")
    print("  • 16:9  - Landscape (YouTube, presentations)")
    print("  • 9:16  - Portrait (Stories, TikTok)")
    print("  • 4:3   - Classic (presentations)")
    print("  • 3:2   - Photography")
    print("  • 4:5   - Portrait")
    print("  • 21:9  - Ultrawide (wallpapers)")


if __name__ == "__main__":
    # Create outputs directory
    Path("outputs").mkdir(exist_ok=True)
    main()
