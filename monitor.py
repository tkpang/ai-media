#!/usr/bin/env python3
"""
AI Media Monitor - Real-time dashboard for tracking usage and costs

Usage:
    python3 monitor.py              # Show current status
    python3 monitor.py --watch      # Live monitoring mode
    python3 monitor.py --report     # Generate detailed report
    python3 monitor.py --export     # Export data to CSV
"""

import argparse
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from cost_tracker import CostTracker

class Monitor:
    """Real-time monitoring dashboard for AI Media services"""

    def __init__(self):
        self.tracker = CostTracker()
        self.clear_screen = lambda: os.system('clear' if os.name != 'nt' else 'cls')

    def show_dashboard(self, watch=False, interval=5):
        """Display real-time dashboard"""
        try:
            while True:
                if watch:
                    self.clear_screen()

                print("=" * 80)
                print("AI MEDIA MONITORING DASHBOARD".center(80))
                print("=" * 80)
                print()

                # Current status
                self._show_status()
                print()

                # Today's activity
                self._show_today()
                print()

                # Budget status
                self._show_budget()
                print()

                # Recent activity
                self._show_recent()
                print()

                if watch:
                    print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Refreshing in {interval} seconds... (Ctrl+C to stop)")
                    time.sleep(interval)
                else:
                    break

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")

    def _show_status(self):
        """Show overall status"""
        print("📊 OVERALL STATUS")
        print("-" * 80)

        total_cost = self.tracker.get_total_cost()
        total_count = len(self.tracker.records)

        print(f"Total API Calls:     {total_count:,}")
        print(f"Total Cost:          ${total_cost:.2f}")

        if total_count > 0:
            avg_cost = total_cost / total_count
            print(f"Average per Call:    ${avg_cost:.4f}")

        # Service breakdown
        service_costs = {}
        for record in self.tracker.records:
            service = record.get('service', 'unknown')
            service_costs[service] = service_costs.get(service, 0) + record['cost']

        if service_costs:
            print("\nBy Service:")
            for service, cost in sorted(service_costs.items(), key=lambda x: -x[1]):
                print(f"  • {service:<20} ${cost:.2f}")

    def _show_today(self):
        """Show today's activity"""
        print("📅 TODAY'S ACTIVITY")
        print("-" * 80)

        today = datetime.now().date()
        summary = self.tracker.get_daily_summary(str(today))

        print(f"Date:                {today}")
        print(f"API Calls:           {summary['count']:,}")
        print(f"Total Cost:          ${summary['total_cost']:.2f}")

        if summary['count'] > 0:
            print(f"Average per Call:    ${summary['average_cost']:.4f}")
            print(f"Services Used:       {', '.join(summary['services'])}")

    def _show_budget(self, monthly_budget=150.0):
        """Show budget status"""
        print("💰 BUDGET STATUS")
        print("-" * 80)

        status = self.tracker.get_budget_status(monthly_budget=monthly_budget)

        print(f"Monthly Budget:      ${status['monthly_budget']:.2f}")
        print(f"Current Spend:       ${status['current_spend']:.2f}")
        print(f"Remaining:           ${status['remaining']:.2f}")
        print(f"Usage:               {status['percent_used']:.1f}%")

        # Progress bar
        bar_width = 50
        filled = int(bar_width * status['percent_used'] / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        alert_colors = {
            'ok': '\033[92m',      # Green
            'warning': '\033[93m',  # Yellow
            'high': '\033[91m',     # Red
            'critical': '\033[95m'  # Magenta
        }
        reset_color = '\033[0m'

        color = alert_colors.get(status['alert_level'], '')
        print(f"Progress:            {color}[{bar}]{reset_color} {status['alert_level'].upper()}")

        if status['days_until_reset'] > 0:
            print(f"Days until Reset:    {status['days_until_reset']}")

        # Projection
        if status['current_spend'] > 0:
            days_passed = 30 - status['days_until_reset']
            if days_passed > 0:
                daily_avg = status['current_spend'] / days_passed
                projected = daily_avg * 30
                print(f"Projected Monthly:   ${projected:.2f}")

                if projected > monthly_budget:
                    over = projected - monthly_budget
                    print(f"⚠️  Projected Overage: ${over:.2f}")

    def _show_recent(self, limit=10):
        """Show recent activity"""
        print(f"📝 RECENT ACTIVITY (Last {limit})")
        print("-" * 80)

        if not self.tracker.records:
            print("No activity recorded yet.")
            return

        recent = sorted(
            self.tracker.records,
            key=lambda x: x['timestamp'],
            reverse=True
        )[:limit]

        print(f"{'Time':<20} {'Service':<15} {'Description':<30} {'Cost':>10}")
        print("-" * 80)

        for record in recent:
            timestamp = datetime.fromisoformat(record['timestamp'])
            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            service = record.get('service', 'unknown')[:14]
            description = record.get('description', 'N/A')[:29]
            cost = f"${record['cost']:.4f}"

            print(f"{time_str:<20} {service:<15} {description:<30} {cost:>10}")

    def generate_report(self, days=30):
        """Generate detailed report"""
        print("=" * 80)
        print("AI MEDIA DETAILED REPORT".center(80))
        print("=" * 80)
        print()

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        print(f"Report Period: {start_date} to {end_date}")
        print()

        # Overall summary
        self._show_status()
        print()

        # Daily breakdown
        print(f"📊 DAILY BREAKDOWN (Last {days} days)")
        print("-" * 80)
        print(f"{'Date':<15} {'Calls':>8} {'Total Cost':>12} {'Avg Cost':>12}")
        print("-" * 80)

        for i in range(days):
            date = start_date + timedelta(days=i)
            summary = self.tracker.get_daily_summary(str(date))

            if summary['count'] > 0:
                print(
                    f"{date!s:<15} "
                    f"{summary['count']:>8} "
                    f"${summary['total_cost']:>11.2f} "
                    f"${summary['average_cost']:>11.4f}"
                )

        print()

        # Weekly summary
        print("📈 WEEKLY SUMMARY")
        print("-" * 80)

        weeks = []
        for i in range(0, days, 7):
            week_start = start_date + timedelta(days=i)
            week_end = min(week_start + timedelta(days=6), end_date)

            week_cost = 0
            week_count = 0

            for record in self.tracker.records:
                record_date = datetime.fromisoformat(record['timestamp']).date()
                if week_start <= record_date <= week_end:
                    week_cost += record['cost']
                    week_count += 1

            if week_count > 0:
                weeks.append({
                    'start': week_start,
                    'end': week_end,
                    'cost': week_cost,
                    'count': week_count
                })

        for week in weeks:
            avg = week['cost'] / week['count'] if week['count'] > 0 else 0
            print(
                f"{week['start']} to {week['end']}: "
                f"{week['count']} calls, "
                f"${week['cost']:.2f} total, "
                f"${avg:.4f} avg"
            )

        print()

        # Cost trends
        if len(weeks) >= 2:
            print("📉 TRENDS")
            print("-" * 80)

            current_week = weeks[-1]['cost'] if weeks else 0
            previous_week = weeks[-2]['cost'] if len(weeks) >= 2 else 0

            if previous_week > 0:
                change = ((current_week - previous_week) / previous_week) * 100
                direction = "↑" if change > 0 else "↓"
                print(f"Week-over-week change: {direction} {abs(change):.1f}%")

            # Busiest day
            daily_costs = {}
            for record in self.tracker.records:
                date = datetime.fromisoformat(record['timestamp']).date()
                daily_costs[date] = daily_costs.get(date, 0) + record['cost']

            if daily_costs:
                busiest_day = max(daily_costs.items(), key=lambda x: x[1])
                print(f"Busiest day: {busiest_day[0]} (${busiest_day[1]:.2f})")

    def export_data(self, output_file=None):
        """Export cost data to CSV"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"cost_report_{timestamp}.csv"

        self.tracker.export_to_csv(output_file)

        # Also create a summary JSON
        summary_file = output_file.replace('.csv', '_summary.json')

        summary = {
            'generated_at': datetime.now().isoformat(),
            'total_records': len(self.tracker.records),
            'total_cost': self.tracker.get_total_cost(),
            'date_range': {
                'start': min(r['timestamp'] for r in self.tracker.records) if self.tracker.records else None,
                'end': max(r['timestamp'] for r in self.tracker.records) if self.tracker.records else None
            }
        }

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"✅ Data exported:")
        print(f"   • CSV: {output_file}")
        print(f"   • Summary: {summary_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Media Monitoring Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--watch', '-w',
        action='store_true',
        help='Live monitoring mode (auto-refresh)'
    )

    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=5,
        help='Refresh interval in seconds (default: 5)'
    )

    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help='Generate detailed report'
    )

    parser.add_argument(
        '--export', '-e',
        action='store_true',
        help='Export data to CSV'
    )

    parser.add_argument(
        '--days', '-d',
        type=int,
        default=30,
        help='Number of days for report (default: 30)'
    )

    parser.add_argument(
        '--budget', '-b',
        type=float,
        default=150.0,
        help='Monthly budget in USD (default: 150.00)'
    )

    args = parser.parse_args()

    monitor = Monitor()

    try:
        if args.export:
            monitor.export_data()
        elif args.report:
            monitor.generate_report(days=args.days)
        else:
            monitor.show_dashboard(watch=args.watch, interval=args.interval)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
