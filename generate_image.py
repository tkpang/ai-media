#!/usr/bin/env python3
"""
Banana Pro 图片生成 — 一键运行脚本

用法:
    python generate_image.py "你的提示词"
    python generate_image.py "提示词" --route 2K_5 --ratio 16:9 --output my_image.png

环境变量（通过 .env 文件配置）:
    BANANA_PRO_API_KEY     — API 密钥（必需）
    BANANA_PRO_BASE_URL    — 服务地址，默认 https://xais1.dchai.cn
    BANANA_PRO_DEFAULT_ROUTE — 默认路由，默认 2K_2
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# 尝试从 .env 文件加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv 不是必须的，可以直接设置环境变量

from banana_pro_web_client import BananaProWebClient
from cost_tracker import CostTracker


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Banana Pro 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python generate_image.py "一只可爱的猫咪"
    python generate_image.py "sunset over mountains" --route 2K_5 --ratio 16:9
    python generate_image.py "商务人像" --output portrait.png --no-tracking
        """,
    )
    parser.add_argument("prompt", help="图片生成提示词")
    parser.add_argument(
        "--route",
        default=os.getenv("BANANA_PRO_DEFAULT_ROUTE", "2K_2"),
        help="模型路由 (默认: 2K_2，推荐: 2K_2 或 2K_5)",
    )
    parser.add_argument(
        "--ratio",
        default=os.getenv("BANANA_PRO_DEFAULT_ASPECT_RATIO", "1:1"),
        choices=["1:1", "16:9", "9:16", "4:3", "3:2", "4:5", "21:9"],
        help="宽高比 (默认: 1:1)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出文件路径（不指定则自动命名）",
    )
    parser.add_argument(
        "--no-tracking",
        action="store_true",
        help="禁用费用追踪",
    )

    args = parser.parse_args()

    # 获取 API 配置
    api_key = os.getenv("BANANA_PRO_API_KEY")
    if not api_key:
        print("错误: 未设置 BANANA_PRO_API_KEY 环境变量")
        print("请复制 .env.example 为 .env 并填入你的 API Key")
        sys.exit(1)

    base_url = os.getenv("BANANA_PRO_BASE_URL", "https://xais1.dchai.cn")

    # 创建客户端
    client = BananaProWebClient(api_key=api_key, base_url=base_url)
    tracker = CostTracker() if not args.no_tracking else None

    print(f"提示词: {args.prompt}")
    print(f"路由: {args.route}")
    print(f"宽高比: {args.ratio}")
    print(f"服务地址: {base_url}")
    print()

    # 登录
    print("正在登录...")
    profile = client.login()
    print(f"登录成功 (用户ID: {profile.get('id', 'unknown')})")
    print()

    # 生成图片
    print("正在生成图片，请耐心等待...")
    result = client.generate_image(
        prompt=args.prompt,
        route=args.route,
        aspect_ratio=args.ratio,
        save_path=args.output,
    )

    saved_to = result["saved_to"]
    file_size = Path(saved_to).stat().st_size
    size_mb = file_size / (1024 * 1024)

    print()
    print(f"生成成功!")
    print(f"  文件: {saved_to}")
    print(f"  大小: {size_mb:.1f} MB")
    print(f"  模型: {result['model']}")
    print(f"  路由: {result['route']}")
    print(f"  宽高比: {result['aspect_ratio']}")

    # 记录费用
    if tracker:
        cost = 0.045
        tracker.add_record(
            service="banana_pro_web",
            operation="image_generation",
            cost=cost,
            metadata={
                "prompt": args.prompt[:100],
                "route": args.route,
                "aspect_ratio": args.ratio,
                "model": result.get("model", ""),
                "task_id": result.get("task_id", ""),
                "saved_to": saved_to,
            },
        )
        print(f"  费用: ${cost:.3f} (已记录)")


if __name__ == "__main__":
    main()
