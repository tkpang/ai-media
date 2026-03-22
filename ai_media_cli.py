#!/usr/bin/env python3
"""
AI Media CLI - Command Line Interface

Simple command-line tool for common operations:
- Generate single images
- Process batches
- Check costs and budget
- View usage statistics

Usage:
    python3 ai_media_cli.py generate "a sunset"
    python3 ai_media_cli.py batch prompts.txt
    python3 ai_media_cli.py cost --budget 150
    python3 ai_media_cli.py status
"""

import sys
import argparse
from pathlib import Path
from typing import List


def load_env():
    """Load API credentials from .env file"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Error: .env file not found")
        print("Run 'python3 quick_start.py' to set up configuration")
        sys.exit(1)

    config = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key] = value

    return config


def create_banana_client(config, cost_override=None):
    """Create Banana Pro client based on configuration mode."""
    api_key = config.get("BANANA_PRO_API_KEY")
    base_url = (config.get("BANANA_PRO_BASE_URL") or "").strip()
    mode = (config.get("BANANA_PRO_MODE") or "").strip().lower()
    cost_per_image = float(cost_override or 0.045)

    if not api_key or not base_url:
        print("Error: API credentials not found in .env")
        sys.exit(1)

    is_web_mode = mode == "web" or "xais1.dchai.cn" in base_url

    if is_web_mode:
        from banana_pro_web_with_tracking import BananaProWebWithTracking

        return BananaProWebWithTracking(
            api_key=api_key,
            base_url=base_url,
            cost_per_image=cost_per_image
        )

    from banana_pro_with_tracking import BananaProWithTracking
    return BananaProWithTracking(
        api_key=api_key,
        base_url=base_url,
        cost_per_image=cost_per_image
    )


def cmd_generate(args):
    """Generate a single image"""
    config = load_env()
    client = create_banana_client(config, cost_override=args.cost)

    print(f"Generating image: {args.prompt}")
    print(f"Route: {args.route}")
    print(f"Aspect ratio: {args.aspect_ratio}")
    print()

    try:
        result = client.generate_image(
            prompt=args.prompt,
            route=args.route,
            aspect_ratio=args.aspect_ratio
        )

        print(f"✓ Image generated successfully!")
        print(f"  Saved to: {result['saved_to']}")
        print(f"  Cost: ${result['cost']:.4f}")

    except Exception as e:
        print(f"✗ Generation failed: {e}")
        sys.exit(1)


def cmd_batch(args):
    """Process a batch of prompts"""
    from batch_processor import BatchProcessor

    # Load prompts
    prompts_file = Path(args.prompts_file)
    if not prompts_file.exists():
        print(f"Error: Prompts file not found: {prompts_file}")
        sys.exit(1)

    with open(prompts_file) as f:
        prompts = [line.strip() for line in f if line.strip()]

    if not prompts:
        print("Error: No prompts found in file")
        sys.exit(1)

    print(f"Loaded {len(prompts)} prompts from {prompts_file}")
    print()

    # Load config
    config = load_env()
    client = create_banana_client(config, cost_override=args.cost)

    # Create processor
    processor = BatchProcessor(
        client=client,
        max_workers=args.workers,
        max_cost=args.max_cost
    )

    print(f"Processing batch:")
    print(f"  Workers: {args.workers}")
    print(f"  Max cost: ${args.max_cost:.2f}")
    print()

    try:
        summary = processor.process_image_batch(
            prompts=prompts,
            route=args.route,
            aspect_ratio=args.aspect_ratio,
            output_dir=args.output
        )

        processor.print_summary(summary)

        # Save results
        if args.save_results:
            result_file = f"batch_results_{Path(prompts_file).stem}.json"
            processor.save_results(summary, result_file)

    except Exception as e:
        print(f"✗ Batch processing failed: {e}")
        sys.exit(1)


def cmd_cost(args):
    """View cost statistics"""
    from cost_tracker import CostTracker

    tracker = CostTracker()

    if args.export:
        tracker.export_to_csv(args.export)
        print(f"Exported costs to {args.export}")
        return

    if args.budget:
        print("Budget Status:")
        print("=" * 50)
        status = tracker.get_budget_status(monthly_budget=args.budget)

        print(f"Monthly Budget: ${status['monthly_budget']:.2f}")
        print(f"Current Spend: ${status['current_spend']:.2f}")
        print(f"Remaining: ${status['remaining']:.2f}")
        print(f"Percent Used: {status['percent_used']:.1f}%")
        print()
        print(f"Days Elapsed: {status['days_elapsed']}")
        print(f"Avg Daily Spend: ${status['avg_daily_spend']:.2f}")
        print(f"Projected Monthly: ${status['projected_monthly_spend']:.2f}")
        print()

        alert = status['alert_level']
        if alert == 'critical':
            print("⚠️  ALERT: Budget exceeded!")
        elif alert == 'high':
            print("⚠️  WARNING: Approaching budget limit")
        elif alert == 'warning':
            print("⚠️  CAUTION: Spending faster than expected")
        else:
            print("✓ Budget on track")

        print()

    # Show summary
    tracker.print_summary(days=args.days)


def cmd_status(args):
    """Show system status"""
    from cost_tracker import CostTracker

    print("AI Media Workspace - Status")
    print("=" * 70)
    print()

    # Check config
    env_file = Path(".env")
    if env_file.exists():
        print("✓ Configuration found (.env)")
        config = load_env()
        print(f"  API Key: {config.get('BANANA_PRO_API_KEY', 'Not set')[:20]}...")
        print(f"  Base URL: {config.get('BANANA_PRO_BASE_URL', 'Not set')}")
        mode = config.get("BANANA_PRO_MODE", "api")
        print(f"  Mode: {mode}")
    else:
        print("✗ Configuration not found")
        print("  Run 'python3 quick_start.py' to set up")

    print()

    # Check dependencies
    print("Dependencies:")
    try:
        import requests
        print("  ✓ requests")
    except ImportError:
        print("  ✗ requests (required)")

    try:
        import cv2
        print("  ✓ opencv-python")
    except ImportError:
        print("  ⚠ opencv-python (optional)")

    try:
        import moviepy
        print("  ✓ moviepy")
    except ImportError:
        print("  ⚠ moviepy (optional)")

    print()

    # Cost summary
    tracker = CostTracker()
    total = tracker.get_total_cost()
    records = len(tracker.records)

    print(f"Usage Statistics:")
    print(f"  Total API calls: {records}")
    print(f"  Total cost: ${total:.2f}")

    if records > 0:
        avg = total / records
        print(f"  Avg cost/call: ${avg:.4f}")

    print()

    # Output directory
    output_dir = Path("outputs")
    if output_dir.exists():
        files = list(output_dir.glob("**/*"))
        images = [f for f in files if f.suffix in ['.png', '.jpg', '.jpeg']]
        videos = [f for f in files if f.suffix in ['.mp4', '.mov', '.avi']]

        print(f"Output Directory:")
        print(f"  Path: {output_dir.absolute()}")
        print(f"  Images: {len(images)}")
        print(f"  Videos: {len(videos)}")
    else:
        print("Output directory: Not created")

    print()
    print("=" * 70)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AI Media CLI - Command line interface for AI media generation"
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a single image')
    gen_parser.add_argument('prompt', help='Text prompt for image generation')
    gen_parser.add_argument('--route', default='2K_2', help='Model route (default: 2K_2)')
    gen_parser.add_argument('--aspect-ratio', default='1:1', help='Aspect ratio (default: 1:1)')
    gen_parser.add_argument('--cost', type=float, help='Cost per image (default: 0.045)')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Process batch of prompts')
    batch_parser.add_argument('prompts_file', help='File with prompts (one per line)')
    batch_parser.add_argument('--route', default='2K_2', help='Model route (default: 2K_2)')
    batch_parser.add_argument('--aspect-ratio', default='1:1', help='Aspect ratio (default: 1:1)')
    batch_parser.add_argument('--workers', type=int, default=3, help='Parallel workers (default: 3)')
    batch_parser.add_argument('--max-cost', type=float, default=100.0, help='Max cost limit (default: 100)')
    batch_parser.add_argument('--cost', type=float, help='Cost per image (default: 0.045)')
    batch_parser.add_argument('--output', default='outputs/batch', help='Output directory')
    batch_parser.add_argument('--save-results', action='store_true', help='Save results to JSON')

    # Cost command
    cost_parser = subparsers.add_parser('cost', help='View cost statistics')
    cost_parser.add_argument('--budget', type=float, help='Monthly budget for comparison')
    cost_parser.add_argument('--days', type=int, default=30, help='Days to include (default: 30)')
    cost_parser.add_argument('--export', help='Export to CSV file')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Run command
    if args.command == 'generate':
        cmd_generate(args)
    elif args.command == 'batch':
        cmd_batch(args)
    elif args.command == 'cost':
        cmd_cost(args)
    elif args.command == 'status':
        cmd_status(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
