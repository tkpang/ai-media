#!/usr/bin/env python3
"""
Cost Tracker for AI Media Workspace

Tracks and analyzes API usage costs across all services:
- Banana Pro (image generation)
- Seedance 2.0 (video generation)
- Custom services

Features:
- Real-time cost tracking
- Daily/weekly/monthly summaries
- Budget alerts
- Usage analytics
- Export to CSV/JSON
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class UsageRecord:
    """Single API usage record"""
    timestamp: str
    service: str  # "banana_pro", "seedance", "custom"
    operation: str  # "image_generation", "video_generation", etc.
    cost: float
    metadata: Dict  # Additional info (resolution, duration, prompt, etc.)

    def to_dict(self) -> Dict:
        return asdict(self)


class CostTracker:
    """Track and analyze API usage costs"""

    def __init__(self, data_file: str = "cost_data.json"):
        self.data_file = Path(data_file)
        self.records: List[UsageRecord] = []
        self.load_records()

    def load_records(self):
        """Load existing records from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.records = [
                        UsageRecord(**record) for record in data
                    ]
                print(f"Loaded {len(self.records)} cost records")
            except Exception as e:
                print(f"Warning: Could not load cost data: {e}")
                self.records = []
        else:
            print("No existing cost data found. Starting fresh.")

    def save_records(self):
        """Save records to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(
                    [r.to_dict() for r in self.records],
                    f,
                    indent=2
                )
            print(f"Saved {len(self.records)} cost records")
        except Exception as e:
            print(f"Error saving cost data: {e}")

    def add_record(
        self,
        service: str,
        operation: str,
        cost: float,
        metadata: Optional[Dict] = None
    ):
        """Add a new usage record"""
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            service=service,
            operation=operation,
            cost=cost,
            metadata=metadata or {}
        )
        self.records.append(record)
        self.save_records()
        return record

    def get_records(
        self,
        service: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[UsageRecord]:
        """Filter records by criteria"""
        filtered = self.records

        if service:
            filtered = [r for r in filtered if r.service == service]

        if start_date:
            filtered = [
                r for r in filtered
                if datetime.fromisoformat(r.timestamp) >= start_date
            ]

        if end_date:
            filtered = [
                r for r in filtered
                if datetime.fromisoformat(r.timestamp) <= end_date
            ]

        return filtered

    def get_total_cost(
        self,
        service: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Calculate total cost for filtered records"""
        records = self.get_records(service, start_date, end_date)
        return sum(r.cost for r in records)

    def get_daily_summary(self, days: int = 7) -> Dict[str, Dict]:
        """Get daily cost summary for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        records = self.get_records(start_date=start_date)

        # Group by date and service
        daily_data = defaultdict(lambda: defaultdict(float))

        for record in records:
            date = datetime.fromisoformat(record.timestamp).date().isoformat()
            daily_data[date][record.service] += record.cost
            daily_data[date]['total'] += record.cost

        return dict(daily_data)

    def get_service_breakdown(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """Get cost breakdown by service"""
        records = self.get_records(start_date=start_date, end_date=end_date)

        breakdown = defaultdict(float)
        for record in records:
            breakdown[record.service] += record.cost

        return dict(breakdown)

    def get_budget_status(self, monthly_budget: float) -> Dict:
        """Check current month spending against budget"""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        current_spend = self.get_total_cost(start_date=start_of_month)
        remaining = monthly_budget - current_spend
        days_in_month = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)).day
        days_elapsed = now.day
        days_remaining = days_in_month - days_elapsed

        avg_daily = current_spend / days_elapsed if days_elapsed > 0 else 0
        projected_spend = avg_daily * days_in_month

        return {
            'monthly_budget': monthly_budget,
            'current_spend': current_spend,
            'remaining': remaining,
            'percent_used': (current_spend / monthly_budget * 100) if monthly_budget > 0 else 0,
            'days_elapsed': days_elapsed,
            'days_remaining': days_remaining,
            'avg_daily_spend': avg_daily,
            'projected_monthly_spend': projected_spend,
            'on_track': projected_spend <= monthly_budget,
            'alert_level': self._get_alert_level(current_spend, monthly_budget, days_elapsed, days_in_month)
        }

    def _get_alert_level(
        self,
        current_spend: float,
        budget: float,
        days_elapsed: int,
        days_in_month: int
    ) -> str:
        """Determine budget alert level"""
        percent_used = (current_spend / budget * 100) if budget > 0 else 0
        percent_time_elapsed = (days_elapsed / days_in_month * 100) if days_in_month > 0 else 0

        if percent_used >= 100:
            return "critical"  # Over budget
        elif percent_used >= 90:
            return "high"  # Near budget limit
        elif percent_used > percent_time_elapsed + 20:
            return "warning"  # Spending faster than expected
        else:
            return "ok"

    def export_to_csv(self, output_file: str = "cost_report.csv"):
        """Export records to CSV"""
        if not self.records:
            print("No records to export")
            return

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Timestamp', 'Service', 'Operation', 'Cost',
                'Metadata'
            ])

            # Data
            for record in self.records:
                writer.writerow([
                    record.timestamp,
                    record.service,
                    record.operation,
                    f"${record.cost:.4f}",
                    json.dumps(record.metadata)
                ])

        print(f"Exported {len(self.records)} records to {output_file}")

    def print_summary(self, days: int = 30):
        """Print a formatted summary report"""
        print("=" * 70)
        print(f"AI Media Cost Summary - Last {days} Days")
        print("=" * 70)
        print()

        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Total cost
        total = self.get_total_cost(start_date=start_date)
        print(f"Total Cost: ${total:.2f}")
        print()

        # Service breakdown
        breakdown = self.get_service_breakdown(start_date=start_date)
        if breakdown:
            print("Cost by Service:")
            for service, cost in sorted(breakdown.items(), key=lambda x: -x[1]):
                percent = (cost / total * 100) if total > 0 else 0
                print(f"  {service:20s}: ${cost:8.2f} ({percent:5.1f}%)")
            print()

        # Daily summary
        daily = self.get_daily_summary(days=min(days, 14))
        if daily:
            print(f"Daily Costs (Last {min(days, 14)} Days):")
            for date in sorted(daily.keys(), reverse=True):
                total_day = daily[date]['total']
                print(f"  {date}: ${total_day:8.2f}")
            print()

        # Record count
        records = self.get_records(start_date=start_date)
        print(f"Total Operations: {len(records)}")
        print()

        print("=" * 70)


def example_usage():
    """Example usage of the cost tracker"""
    tracker = CostTracker()

    # Add some example records
    print("Adding example records...")

    tracker.add_record(
        service="banana_pro",
        operation="image_generation",
        cost=0.045,
        metadata={
            "prompt": "Beautiful sunset",
            "resolution": "1024x1024",
            "route": "2K_2"
        }
    )

    tracker.add_record(
        service="seedance",
        operation="video_generation",
        cost=1.40,
        metadata={
            "prompt": "Timelapse of city",
            "duration": 10,
            "resolution": "1080p"
        }
    )

    # Print summary
    tracker.print_summary(days=30)

    # Check budget
    print("\nBudget Status:")
    status = tracker.get_budget_status(monthly_budget=150.0)
    print(f"  Monthly Budget: ${status['monthly_budget']:.2f}")
    print(f"  Current Spend: ${status['current_spend']:.2f}")
    print(f"  Remaining: ${status['remaining']:.2f}")
    print(f"  Percent Used: {status['percent_used']:.1f}%")
    print(f"  Projected Monthly: ${status['projected_monthly_spend']:.2f}")
    print(f"  Alert Level: {status['alert_level']}")

    # Export to CSV
    print("\nExporting to CSV...")
    tracker.export_to_csv()


if __name__ == "__main__":
    example_usage()
