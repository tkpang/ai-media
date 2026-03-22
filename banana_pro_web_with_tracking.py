#!/usr/bin/env python3
"""
Banana Pro Web Client with Integrated Cost Tracking.
"""

from __future__ import annotations

from typing import Literal, Optional

from banana_pro_web_client import BananaProWebClient
from cost_tracker import CostTracker


class BananaProWebWithTracking(BananaProWebClient):
    """Web automation client that records image generation cost."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://xais1.dchai.cn",
        cost_per_image: float = 0.045,
        cost_tracker: Optional[CostTracker] = None,
        timeout: int = 30,
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.cost_per_image = cost_per_image
        self.tracker = cost_tracker or CostTracker()

    def generate_image(
        self,
        prompt: str,
        route: str = "2K_2",
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:2", "4:5", "21:9"] = "1:1",
        save_path: Optional[str] = None,
        retries: int = 2,
        wait_timeout: int = 240,
    ):
        result = super().generate_image(
            prompt=prompt,
            route=route,
            aspect_ratio=aspect_ratio,
            save_path=save_path,
            retries=retries,
            wait_timeout=wait_timeout,
        )

        self.tracker.add_record(
            service="banana_pro_web",
            operation="image_generation",
            cost=self.cost_per_image,
            metadata={
                "prompt": prompt[:100],
                "route": route,
                "aspect_ratio": aspect_ratio,
                "model": result.get("model", ""),
                "task_id": result.get("task_id", ""),
                "saved_to": result.get("saved_to", ""),
            },
        )

        result["cost"] = self.cost_per_image
        result["cost_tracked"] = True
        return result
