#!/usr/bin/env python3
"""
Banana Pro API Test Script
Tests the xais1.dchai.cn Banana Pro API with provided credentials
"""

import requests
import base64
import json
import os
from datetime import datetime

# API Configuration
API_BASE_URL = "https://xais1.dchai.cn"
API_KEY = "sk-Pi5Sc2cZfD7M9bkCHU2ly0OroaFoYirtteqIu1HwkssCsKL8"

def test_gemini_native_format():
    """Test with Gemini-native API format"""
    print("Testing Gemini-native format...")

    url = f"{API_BASE_URL}/v1beta/models/gemini-3-pro-image-preview:generateContent"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Test with 2K route (cheaper)
    payload = {
        "contents": [{
            "parts": [{"text": "A simple red apple on a white background"}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "1:1",
                "imageSize": "2K"
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code == 200:
            result = response.json()
            if "candidates" in result:
                img_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

                # Save image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_banana_pro_{timestamp}.png"
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(img_data))
                print(f"✓ Image saved: {filename}")
                return True

        return False
    except Exception as e:
        print(f"✗ Gemini format failed: {e}")
        return False


def test_openai_compatible_format():
    """Test with OpenAI-compatible API format (common for gateways)"""
    print("\nTesting OpenAI-compatible format...")

    url = f"{API_BASE_URL}/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "A simple red apple on a white background",
        "model": "nano-banana-pro-2k",
        "n": 1,
        "size": "1024x1024"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code == 200:
            result = response.json()
            if "data" in result:
                # Handle either URL or base64
                if "url" in result["data"][0]:
                    print(f"✓ Image URL: {result['data'][0]['url']}")
                elif "b64_json" in result["data"][0]:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"test_banana_pro_{timestamp}.png"
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(result["data"][0]["b64_json"]))
                    print(f"✓ Image saved: {filename}")
                return True

        return False
    except Exception as e:
        print(f"✗ OpenAI format failed: {e}")
        return False


def discover_api_endpoints():
    """Try to discover available API endpoints"""
    print("\nDiscovering API endpoints...")

    endpoints = [
        "/",
        "/v1/models",
        "/v1beta/models",
        "/api/v1/models",
        "/api/generate",
    ]

    for endpoint in endpoints:
        url = f"{API_BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=10)
            if response.status_code != 404:
                print(f"✓ {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"  Content preview: {response.text[:200]}")
        except:
            pass


if __name__ == "__main__":
    print("=" * 60)
    print("Banana Pro API Test")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 60)

    # Try both formats
    success = False

    if not success:
        success = test_gemini_native_format()

    if not success:
        success = test_openai_compatible_format()

    # Discovery mode
    if not success:
        discover_api_endpoints()

    print("\n" + "=" * 60)
    if success:
        print("✓ API Test SUCCESSFUL")
    else:
        print("✗ API Test FAILED - Check endpoint URL and documentation")
    print("=" * 60)
