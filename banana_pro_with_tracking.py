#!/usr/bin/env python3
"""
Banana Pro Client with Integrated Cost Tracking

This is an enhanced version of banana_pro_gemini.py that automatically
tracks all API usage and costs.

Usage:
    from banana_pro_with_tracking import BananaProWithTracking

    client = BananaProWithTracking(
        api_key="your-key",
        base_url="https://api.provider.com",
        cost_per_image=0.045  # APIYI pricing
    )

    result = client.generate_image("A sunset")
    # Cost is automatically tracked!
"""

import sys
from pathlib import Path
from typing import Optional, Literal

# Import the base client
from banana_pro_gemini import BananaProGeminiClient

# Import cost tracker
from cost_tracker import CostTracker


class BananaProWithTracking(BananaProGeminiClient):
    """Banana Pro client with automatic cost tracking"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://xais1.dchai.cn",
        cost_per_image: float = 0.045,  # Default to APIYI pricing
        cost_tracker: Optional[CostTracker] = None
    ):
        """
        Initialize Banana Pro client with cost tracking

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
            cost_per_image: Cost per image generation (default: $0.045 for APIYI)
            cost_tracker: Optional CostTracker instance (creates new if None)
        """
        super().__init__(api_key=api_key, base_url=base_url)
        self.cost_per_image = cost_per_image
        self.tracker = cost_tracker or CostTracker()

    def generate_image(
        self,
        prompt: str,
        route: str = "2K_2",
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:2", "4:5", "21:9"] = "1:1",
        save_path: Optional[str] = None
    ):
        """
        Generate image with automatic cost tracking

        Args:
            prompt: Text description of the image
            route: Model route to use (default: 2K_2 for cost optimization)
            aspect_ratio: Image aspect ratio
            save_path: Optional path to save the image

        Returns:
            dict with generation result and cost info
        """
        # Call parent method
        result = super().generate_image(
            prompt=prompt,
            route=route,
            aspect_ratio=aspect_ratio,
            save_path=save_path
        )

        # Track the cost
        self.tracker.add_record(
            service="banana_pro",
            operation="image_generation",
            cost=self.cost_per_image,
            metadata={
                "prompt": prompt[:100],  # First 100 chars
                "route": route,
                "aspect_ratio": aspect_ratio,
                "model": self.ROUTES.get(route, "unknown"),
                "saved_to": result.get("saved_to", ""),
            }
        )

        # Add cost info to result
        result['cost'] = self.cost_per_image
        result['cost_tracked'] = True

        return result

    def get_session_cost(self) -> float:
        """Get total cost for current session"""
        # This would require session tracking - simplified for now
        return sum(r.cost for r in self.tracker.records if r.service == "banana_pro")

    def print_cost_summary(self):
        """Print cost summary for Banana Pro usage"""
        self.tracker.print_summary(days=30)


def example_usage():
    """Example usage with cost tracking"""
    print("Banana Pro with Cost Tracking - Example")
    print("=" * 70)
    print()

    # Create client with cost tracking
    # NOTE: Update these values when you have real credentials
    client = BananaProWithTracking(
        api_key="your-api-key-here",
        base_url="https://api.apiyi.com",  # or laozhang
        cost_per_image=0.045  # APIYI pricing
    )

    print("Client initialized with automatic cost tracking")
    print(f"Cost per image: ${client.cost_per_image}")
    print()

    # Example: Generate an image
    # (Commented out since we don't have real API access yet)
    """
    print("Generating image...")
    result = client.generate_image(
        prompt="A serene mountain landscape at sunset",
        route="2K_2",  # Cost-optimized
        aspect_ratio="16:9"
    )

    print(f"Image generated: {result['saved_to']}")
    print(f"Cost: ${result['cost']:.4f}")
    print()
    """

    # Show cost summary
    print("Cost Summary:")
    client.print_cost_summary()

    print()
    print("Cost tracking is automatic - every API call is logged!")
    print("Check cost_data.json for the full history")


if __name__ == "__main__":
    example_usage()
