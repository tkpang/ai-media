#!/usr/bin/env python3
"""
Banana Pro Image Generation Client
OpenAI-compatible API for Nano Banana Pro via xais1.dchai.cn
"""

import requests
import base64
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

class BananaProClient:
    """Client for Banana Pro image generation API"""

    def __init__(self, api_key: str, base_url: str = "https://xais1.dchai.cn/v1"):
        """
        Initialize the Banana Pro client

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (default: https://xais1.dchai.cn/v1)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def list_models(self) -> dict:
        """List available models"""
        url = f"{self.base_url}/models"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def generate_image(
        self,
        prompt: str,
        model: str = "Nano_Banana_Pro_2K_2",  # Route 2 (cheaper)
        n: int = 1,
        size: str = "1024x1024",
        response_format: Literal["url", "b64_json"] = "b64_json",
        save_path: Optional[str] = None
    ) -> dict:
        """
        Generate an image using Banana Pro

        Args:
            prompt: Text description of the image to generate
            model: Model ID to use. Available routes:
                   - Nano_Banana_Pro_2K_1 through Nano_Banana_Pro_2K_7 (2K resolution)
                   - Nano_Banana_Pro_4K_1 through Nano_Banana_Pro_4K_7 (4K resolution)
                   Routes 2 and 5 are recommended for cost optimization
            n: Number of images to generate (default: 1)
            size: Image size (default: "1024x1024")
            response_format: "url" or "b64_json" (default: "b64_json")
            save_path: Optional path to save the image. Auto-generated if None

        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/images/generations"

        payload = {
            "prompt": prompt,
            "model": model,
            "n": n,
            "size": size,
            "response_format": response_format
        }

        print(f"Generating image with model: {model}")
        print(f"Prompt: {prompt}")

        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Handle image saving
        if response_format == "b64_json" and "data" in result:
            for idx, item in enumerate(result["data"]):
                if "b64_json" in item:
                    # Generate filename if not provided
                    if save_path is None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        save_path = f"banana_pro_{timestamp}_{idx}.png"

                    # Save image
                    with open(save_path, "wb") as f:
                        f.write(base64.b64decode(item["b64_json"]))
                    print(f"✓ Image saved: {save_path}")
                    item["saved_to"] = save_path

        return result

    def get_cost_optimized_model(self, resolution: Literal["2K", "4K"] = "2K") -> str:
        """
        Get the cost-optimized model for the specified resolution

        Args:
            resolution: "2K" or "4K"

        Returns:
            Model ID for route 2 (recommended for cost optimization)
        """
        return f"Nano_Banana_Pro_{resolution}_2"


def main():
    """Example usage"""
    # Initialize client
    API_KEY = "sk-Pi5Sc2cZfD7M9bkCHU2ly0OroaFoYirtteqIu1HwkssCsKL8"
    client = BananaProClient(api_key=API_KEY)

    print("=" * 60)
    print("Banana Pro Image Generation Test")
    print("=" * 60)

    # List available models
    print("\n1. Listing available models...")
    models = client.list_models()
    print(f"Found {len(models['data'])} models:")
    for model in models['data']:
        print(f"  - {model['id']}")

    # Test image generation with cost-optimized route
    print("\n2. Testing image generation (Route 2 - Cost Optimized)...")
    result = client.generate_image(
        prompt="A red apple on a white background, photorealistic",
        model=client.get_cost_optimized_model("2K"),
        n=1,
        size="1024x1024"
    )

    print("\n" + "=" * 60)
    print("✓ Test completed successfully!")
    print("=" * 60)

    return result


if __name__ == "__main__":
    main()
