#!/usr/bin/env python3
"""
Banana Pro (xais1.dchai.cn) - Gemini API Format Client
Uses Gemini generateContent format for NanoBanana Pro image generation
"""

import requests
import base64
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

class BananaProGeminiClient:
    """Client for Banana Pro using Gemini API format"""

    # Model name mapping for routes
    ROUTES = {
        "2K_1": "Nano_Banana_Pro_2K_1",
        "2K_2": "Nano_Banana_Pro_2K_2",  # Cost-optimized
        "2K_3": "Nano_Banana_Pro_2K_3",
        "2K_4": "Nano_Banana_Pro_2K_4",
        "2K_5": "Nano_Banana_Pro_2K_5",  # Cost-optimized
        "2K_6": "Nano_Banana_Pro_2K_6",
        "2K_7": "Nano_Banana_Pro_2K_7",
        "4K_1": "Nano_Banana_Pro_4K_1",
        "4K_2": "Nano_Banana_Pro_4K_2",  # Cost-optimized
        "4K_3": "Nano_Banana_Pro_4K_3",
        "4K_4": "Nano_Banana_Pro_4K_4",
        "4K_5": "Nano_Banana_Pro_4K_5",  # Cost-optimized
        "4K_6": "Nano_Banana_Pro_4K_6",
        "4K_7": "Nano_Banana_Pro_4K_7",
    }

    def __init__(self, api_key: str, base_url: str = "https://xais1.dchai.cn"):
        """
        Initialize the Banana Pro Gemini client

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (default: https://xais1.dchai.cn)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        route: str = "2K_2",  # Default to cost-optimized route 2
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:2", "4:5", "21:9"] = "1:1",
        save_path: Optional[str] = None
    ) -> dict:
        """
        Generate an image using Banana Pro via Gemini API format

        Args:
            prompt: Text description of the image to generate
            route: Route ID (e.g., "2K_2", "2K_5", "4K_2", "4K_5")
                   Routes 2 and 5 are recommended for cost optimization
            aspect_ratio: Image aspect ratio
            save_path: Optional path to save the image. Auto-generated if None

        Returns:
            API response dictionary with image data

        Raises:
            ValueError: If route is invalid
            requests.HTTPError: If API request fails
        """
        if route not in self.ROUTES:
            raise ValueError(f"Invalid route: {route}. Must be one of {list(self.ROUTES.keys())}")

        model_id = self.ROUTES[route]
        resolution = "2K" if "2K" in route else "4K"

        # Gemini API endpoint format
        url = f"{self.base_url}/v1beta/models/{model_id}:generateContent"

        # Gemini API request format
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageSize": resolution
                }
            }
        }

        print(f"Generating image...")
        print(f"  Model: {model_id}")
        print(f"  Route: {route}")
        print(f"  Resolution: {resolution}")
        print(f"  Aspect Ratio: {aspect_ratio}")
        print(f"  Prompt: {prompt}")

        response = requests.post(url, headers=self.headers, json=payload, timeout=120)

        # Check for errors
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()

        result = response.json()

        # Extract and save image
        try:
            img_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

            # Generate filename if not provided
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"banana_pro_{route}_{timestamp}.png"

            # Save image
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(img_data))
            print(f"✓ Image saved: {save_path}")

            result["saved_to"] = save_path
        except (KeyError, IndexError) as e:
            print(f"✗ Failed to extract image data: {e}")
            print(f"Response structure: {json.dumps(result, indent=2)}")
            raise

        return result

    def list_models(self) -> dict:
        """List available models"""
        url = f"{self.base_url}/v1/models"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


def main():
    """Example usage with cost-optimized routes"""
    # Initialize client
    API_KEY = "sk-Pi5Sc2cZfD7M9bkCHU2ly0OroaFoYirtteqIu1HwkssCsKL8"
    client = BananaProGeminiClient(api_key=API_KEY)

    print("=" * 60)
    print("Banana Pro (xais1.dchai.cn) - Gemini API Test")
    print("=" * 60)

    # Test with cost-optimized route 2
    print("\n1. Testing Route 2K_2 (Cost-optimized)...")
    try:
        result = client.generate_image(
            prompt="A red apple on a white background, photorealistic, 4K quality",
            route="2K_2",
            aspect_ratio="1:1"
        )
        print("✓ Route 2K_2 successful!")
    except Exception as e:
        print(f"✗ Route 2K_2 failed: {e}")

    # Test with cost-optimized route 5
    print("\n2. Testing Route 2K_5 (Cost-optimized)...")
    try:
        result = client.generate_image(
            prompt="A cute kitten playing with yarn, studio lighting",
            route="2K_5",
            aspect_ratio="16:9"
        )
        print("✓ Route 2K_5 successful!")
    except Exception as e:
        print(f"✗ Route 2K_5 failed: {e}")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
