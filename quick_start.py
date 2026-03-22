#!/usr/bin/env python3
"""
Quick Start Script for AI Media Workspace

This script helps you get started quickly once you have API credentials.
It will guide you through configuration and run initial tests.
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("AI Media Workspace - Quick Start")
    print("=" * 70)
    print()

def check_environment():
    """Check if required libraries are installed"""
    print("Checking environment...")

    missing_libs = []

    # Check for required libraries
    try:
        import requests
        print("  ✓ requests installed")
    except ImportError:
        missing_libs.append("requests")
        print("  ✗ requests not found")

    try:
        import cv2
        print("  ✓ opencv-python installed")
    except ImportError:
        print("  ⚠ opencv-python not installed (optional for video editing)")

    try:
        import moviepy
        print("  ✓ moviepy installed")
    except ImportError:
        print("  ⚠ moviepy not installed (optional for video editing)")

    if missing_libs:
        print(f"\n✗ Missing required libraries: {', '.join(missing_libs)}")
        print("Install with: pip install " + " ".join(missing_libs))
        return False

    print()
    return True

def setup_config():
    """Create configuration file"""
    print("Setting up configuration...")

    config_path = Path(".env")

    if config_path.exists():
        print(f"  ⚠ Configuration file already exists: {config_path}")
        overwrite = input("  Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("  Skipping configuration setup")
            return

    print()
    print("Choose your API provider:")
    print("  1. APIYI ($0.045/image + SLA)")
    print("  2. LaoZhang.ai ($0.05/image)")
    print("  3. xais1.dchai.cn (Web automation mode)")
    print("  4. Custom endpoint")

    choice = input("Select (1/2/3/4): ").strip()

    if choice == "1":
        base_url = "https://api.apiyi.com"  # Replace with actual APIYI endpoint
        provider = "APIYI"
        mode = "api"
    elif choice == "2":
        base_url = "https://api.laozhang.ai"  # Replace with actual LaoZhang endpoint
        provider = "LaoZhang"
        mode = "api"
    elif choice == "3":
        base_url = "https://xais1.dchai.cn"
        provider = "XAIS Web"
        mode = "web"
    elif choice == "4":
        base_url = input("Enter base URL: ").strip()
        provider = "Custom"
        mode = "api"
    else:
        print("Invalid choice")
        return

    api_key = input("Enter your API key: ").strip()

    config_content = f"""# AI Media API Configuration
# Provider: {provider}

# Banana Pro Settings
BANANA_PRO_API_KEY={api_key}
BANANA_PRO_BASE_URL={base_url}
BANANA_PRO_MODE={mode}

# Seedance 2.0 Settings (add when ready)
# SEEDANCE_API_KEY=your-key-here
# SEEDANCE_BASE_URL=https://api.provider.com

# Output Settings
OUTPUT_DIR=./outputs
"""

    with open(config_path, "w") as f:
        f.write(config_content)

    print(f"  ✓ Configuration saved to {config_path}")
    print()

def create_output_directory():
    """Create output directory for generated media"""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    print(f"  ✓ Output directory ready: {output_dir.absolute()}")
    print()

def run_basic_test():
    """Run a basic connectivity test"""
    print("Running basic connectivity test...")

    try:
        # Load config
        config_path = Path(".env")
        if not config_path.exists():
            print("  ✗ No configuration file found. Run setup first.")
            return False

        # Read API key and base URL from config
        config = {}
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key] = value

        api_key = config.get("BANANA_PRO_API_KEY")
        base_url = config.get("BANANA_PRO_BASE_URL")
        mode = config.get("BANANA_PRO_MODE", "api").lower()

        if not api_key or not base_url:
            print("  ✗ API key or base URL not found in config")
            return False

        # Test connection
        if mode == "web" or "xais1.dchai.cn" in base_url:
            from banana_pro_web_client import BananaProWebClient
            client = BananaProWebClient(api_key=api_key, base_url=base_url)
        else:
            from banana_pro_gemini import BananaProGeminiClient
            client = BananaProGeminiClient(api_key=api_key, base_url=base_url)

        print("  Testing API connection...")
        try:
            models = client.list_models()
            print(f"  ✓ API connection successful!")
            print(f"  ✓ Found {len(models.get('data', []))} models")
        except Exception as e:
            print(f"  ✗ API connection failed: {e}")
            return False

        # Generate test image
        print("\n  Generating test image...")
        print("  (This will use ~$0.05 of credits)")
        proceed = input("  Continue? (y/n): ").strip().lower()

        if proceed == 'y':
            try:
                result = client.generate_image(
                    prompt="A simple red circle on white background, minimal, clean",
                    route="2K_2",
                    aspect_ratio="1:1",
                    save_path="outputs/test_image.png"
                )
                print(f"  ✓ Test image generated successfully!")
                print(f"  ✓ Saved to: {result['saved_to']}")
                return True
            except Exception as e:
                print(f"  ✗ Image generation failed: {e}")
                return False
        else:
            print("  Skipping image generation test")
            return True

    except ImportError:
        print("  ✗ Required Banana Pro client module not found")
        return False
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print()
    print("=" * 70)
    print("Quick Start Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Review the generated test image in outputs/")
    print("  2. Check example_usage.py for more advanced examples")
    print("  3. Review TESTING_CHECKLIST.md for comprehensive testing")
    print("  4. Read BOARD_SUMMARY.md for full feature overview")
    print()
    print("Generate your first image:")
    print("  python3 -c \"from banana_pro_gemini import BananaProGeminiClient; \\")
    print("    client = BananaProGeminiClient(api_key='YOUR_KEY'); \\")
    print("    client.generate_image('Your prompt here', route='2K_2')\"")
    print()
    print("Or run the full example suite:")
    print("  python3 example_usage.py")
    print()
    print("=" * 70)

def main():
    """Main quick start flow"""
    print_banner()

    # Step 1: Check environment
    if not check_environment():
        print("Please install missing dependencies and run again.")
        sys.exit(1)

    # Step 2: Setup configuration
    setup_config()

    # Step 3: Create output directory
    create_output_directory()

    # Step 4: Run basic test
    print("Would you like to run a basic connectivity test?")
    test = input("This will test API access and optionally generate a test image (y/n): ").strip().lower()

    if test == 'y':
        success = run_basic_test()
        if success:
            show_next_steps()
        else:
            print("\n⚠ Some tests failed. Please check your configuration.")
            print("Review BOARD_SUMMARY.md for troubleshooting tips.")
    else:
        print("\nConfiguration complete!")
        print("Run this script again to test your API connection.")
        show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
