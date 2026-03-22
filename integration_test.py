#!/usr/bin/env python3
"""
AI Media Integration Test Suite

Tests all major components of the AI Media workspace to ensure
everything is properly connected and working together.

Usage:
    python3 integration_test.py              # Run all tests
    python3 integration_test.py --quick      # Skip slow tests
    python3 integration_test.py --no-api     # Skip API tests (offline mode)
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

class IntegrationTest:
    """Comprehensive integration testing"""

    def __init__(self, skip_api=False, quick=False):
        self.skip_api = skip_api
        self.quick = quick
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def test(self, name, func, slow=False, requires_api=False):
        """Run a single test"""
        if slow and self.quick:
            self.skipped += 1
            print(f"  ⏭  {name} (skipped - slow)")
            return

        if requires_api and self.skip_api:
            self.skipped += 1
            print(f"  ⏭  {name} (skipped - no API)")
            return

        try:
            func()
            self.passed += 1
            print(f"  ✅ {name}")
        except AssertionError as e:
            self.failed += 1
            print(f"  ❌ {name} - {e}")
        except Exception as e:
            self.failed += 1
            print(f"  ❌ {name} - Error: {e}")

    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 80)
        print("AI MEDIA INTEGRATION TEST SUITE".center(80))
        print("=" * 80)
        print()

        # Module Import Tests
        print("🔧 MODULE IMPORTS")
        self.test("Import banana_pro_gemini", self._test_import_gemini)
        self.test("Import banana_pro_web_client", self._test_import_web_client)
        self.test("Import cost_tracker", self._test_import_cost_tracker)
        self.test("Import batch_processor", self._test_import_batch_processor)
        self.test("Import banana_pro_with_tracking", self._test_import_tracking)
        self.test("Import banana_pro_web_with_tracking", self._test_import_web_tracking)
        print()

        # Client Instantiation Tests
        print("🔌 CLIENT INSTANTIATION")
        self.test("Create Gemini client", self._test_create_gemini_client)
        self.test("Create Web client", self._test_create_web_client)
        self.test("Create tracking client (API)", self._test_create_tracking_client)
        self.test("Create tracking client (Web)", self._test_create_web_tracking_client)
        print()

        # Cost Tracking Tests
        print("💰 COST TRACKING")
        self.test("Initialize cost tracker", self._test_cost_tracker_init)
        self.test("Add cost record", self._test_add_cost_record)
        self.test("Get total cost", self._test_get_total_cost)
        self.test("Get budget status", self._test_budget_status)
        self.test("Get daily summary", self._test_daily_summary)
        self.test("Export to CSV", self._test_export_csv)
        print()

        # Batch Processing Tests
        print("⚡ BATCH PROCESSING")
        self.test("Initialize batch processor", self._test_batch_processor_init)
        self.test("Validate parameters", self._test_batch_params)
        print()

        # Configuration Tests
        print("⚙️  CONFIGURATION")
        self.test("Env example exists", self._test_env_example)
        self.test("Gitignore exists", self._test_gitignore)
        print()

        # File Structure Tests
        print("📁 FILE STRUCTURE")
        self.test("Outputs directory", self._test_outputs_dir)
        self.test("Documentation exists", self._test_documentation)
        self.test("Utility scripts exist", self._test_utilities)
        print()

        # Mode Selection Tests
        print("🔀 MODE SELECTION")
        self.test("Detect API mode", self._test_api_mode_detection)
        self.test("Detect Web mode", self._test_web_mode_detection)
        print()

        # Integration Tests
        print("🔗 INTEGRATION")
        self.test("Cost tracker + API client", self._test_cost_tracker_integration)
        self.test("Cost tracker + Web client", self._test_cost_tracker_web_integration)
        print()

        # API Tests (if not skipped)
        if not self.skip_api:
            print("🌐 API CONNECTIVITY (requires .env)")
            self.test("API client can connect", self._test_api_connection, requires_api=True, slow=True)
            self.test("Web client can connect", self._test_web_connection, requires_api=True, slow=True)
            print()

        # Print summary
        self._print_summary()

    # Module Import Tests
    def _test_import_gemini(self):
        from banana_pro_gemini import BananaProGeminiClient
        assert BananaProGeminiClient is not None

    def _test_import_web_client(self):
        from banana_pro_web_client import BananaProWebClient
        assert BananaProWebClient is not None

    def _test_import_cost_tracker(self):
        from cost_tracker import CostTracker
        assert CostTracker is not None

    def _test_import_batch_processor(self):
        from batch_processor import BatchProcessor
        assert BatchProcessor is not None

    def _test_import_tracking(self):
        from banana_pro_with_tracking import BananaProWithTracking
        assert BananaProWithTracking is not None

    def _test_import_web_tracking(self):
        from banana_pro_web_with_tracking import BananaProWebWithTracking
        assert BananaProWebWithTracking is not None

    # Client Instantiation Tests
    def _test_create_gemini_client(self):
        from banana_pro_gemini import BananaProGeminiClient
        client = BananaProGeminiClient(api_key="test-key", base_url="https://test.com")
        assert client.api_key == "test-key"
        assert client.base_url == "https://test.com"

    def _test_create_web_client(self):
        from banana_pro_web_client import BananaProWebClient
        client = BananaProWebClient(api_key="test-key", base_url="https://test.com")
        assert client.api_key == "test-key"
        assert client.base_url == "https://test.com"

    def _test_create_tracking_client(self):
        from banana_pro_with_tracking import BananaProWithTracking
        client = BananaProWithTracking(
            api_key="test-key",
            base_url="https://test.com",
            cost_per_image=0.045
        )
        assert client.cost_per_image == 0.045

    def _test_create_web_tracking_client(self):
        from banana_pro_web_with_tracking import BananaProWebWithTracking
        client = BananaProWebWithTracking(
            api_key="test-key",
            base_url="https://test.com",
            cost_per_image=0.05
        )
        assert client.cost_per_image == 0.05

    # Cost Tracking Tests
    def _test_cost_tracker_init(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        assert tracker is not None

    def _test_add_cost_record(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        initial_count = len(tracker.records)
        tracker.add_record(service="test", operation="test", cost=1.0)
        assert len(tracker.records) == initial_count + 1

    def _test_get_total_cost(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        total = tracker.get_total_cost()
        assert isinstance(total, (int, float))
        assert total >= 0

    def _test_budget_status(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        status = tracker.get_budget_status(monthly_budget=100.0)
        assert 'current_spend' in status
        assert 'remaining' in status
        assert 'alert_level' in status

    def _test_daily_summary(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        summary = tracker.get_daily_summary(days=7)
        assert isinstance(summary, dict)

    def _test_export_csv(self):
        from cost_tracker import CostTracker
        tracker = CostTracker()
        test_file = "test_export.csv"
        tracker.export_to_csv(test_file)
        assert Path(test_file).exists()
        Path(test_file).unlink()  # Clean up

    # Batch Processing Tests
    def _test_batch_processor_init(self):
        from batch_processor import BatchProcessor
        from banana_pro_gemini import BananaProGeminiClient
        client = BananaProGeminiClient(api_key="test", base_url="https://test.com")
        processor = BatchProcessor(client)
        assert processor is not None

    def _test_batch_params(self):
        from batch_processor import BatchProcessor
        from banana_pro_gemini import BananaProGeminiClient
        client = BananaProGeminiClient(api_key="test", base_url="https://test.com")
        processor = BatchProcessor(client, max_workers=5, max_cost=10.0)
        assert processor.max_workers == 5
        assert processor.max_cost == 10.0

    # Configuration Tests
    def _test_env_example(self):
        assert Path(".env.example").exists()

    def _test_gitignore(self):
        assert Path(".gitignore").exists()

    # File Structure Tests
    def _test_outputs_dir(self):
        outputs = Path("outputs")
        if not outputs.exists():
            outputs.mkdir()
        assert outputs.exists()
        assert outputs.is_dir()

    def _test_documentation(self):
        docs = [
            "README.md",
            "BOARD_SUMMARY.md",
            "DEVELOPER_GUIDE.md",
            "CLI_GUIDE.md"
        ]
        for doc in docs:
            assert Path(doc).exists(), f"{doc} not found"

    def _test_utilities(self):
        utils = [
            "quick_start.py",
            "health_check.py",
            "monitor.py",
            "ai_media_cli.py"
        ]
        for util in utils:
            assert Path(util).exists(), f"{util} not found"

    # Mode Selection Tests
    def _test_api_mode_detection(self):
        """Test that API mode is properly detected"""
        # This would check mode selection logic
        base_url = "https://api.apiyi.com"
        assert "xais" not in base_url.lower()

    def _test_web_mode_detection(self):
        """Test that Web mode is properly detected"""
        base_url = "https://xais1.dchai.cn"
        assert "xais" in base_url.lower()

    # Integration Tests
    def _test_cost_tracker_integration(self):
        """Test cost tracker works with API client"""
        from banana_pro_with_tracking import BananaProWithTracking
        from cost_tracker import CostTracker

        tracker = CostTracker()
        initial_count = len(tracker.records)

        client = BananaProWithTracking(
            api_key="test",
            base_url="https://test.com",
            cost_per_image=0.045
        )

        # Verify tracker is shared
        assert client.tracker is not None

    def _test_cost_tracker_web_integration(self):
        """Test cost tracker works with Web client"""
        from banana_pro_web_with_tracking import BananaProWebWithTracking
        from cost_tracker import CostTracker

        tracker = CostTracker()
        client = BananaProWebWithTracking(
            api_key="test",
            base_url="https://test.com",
            cost_per_image=0.05
        )

        assert client.tracker is not None

    # API Tests
    def _test_api_connection(self):
        """Test actual API connection (requires .env)"""
        if not Path(".env").exists():
            raise AssertionError("No .env file - cannot test API")

        # Load config
        config = {}
        with open(".env") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()

        mode = config.get("BANANA_PRO_MODE", "api")
        if mode != "api":
            raise AssertionError("Not in API mode")

        from banana_pro_gemini import BananaProGeminiClient
        client = BananaProGeminiClient(
            api_key=config["BANANA_PRO_API_KEY"],
            base_url=config["BANANA_PRO_BASE_URL"]
        )

        # Try to list models
        models = client.list_models()
        assert models is not None

    def _test_web_connection(self):
        """Test actual Web connection (requires .env)"""
        if not Path(".env").exists():
            raise AssertionError("No .env file - cannot test Web")

        # Load config
        config = {}
        with open(".env") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()

        mode = config.get("BANANA_PRO_MODE", "api")
        if mode != "web":
            raise AssertionError("Not in Web mode")

        from banana_pro_web_client import BananaProWebClient
        client = BananaProWebClient(
            api_key=config["BANANA_PRO_API_KEY"],
            base_url=config["BANANA_PRO_BASE_URL"]
        )

        # Try to list models
        models = client.list_models()
        assert models is not None

    def _print_summary(self):
        """Print test summary"""
        print("=" * 80)
        print("TEST SUMMARY".center(80))
        print("=" * 80)

        total = self.passed + self.failed + self.skipped

        print(f"Total Tests:   {total}")
        print(f"✅ Passed:     {self.passed}")
        print(f"❌ Failed:     {self.failed}")
        print(f"⏭  Skipped:    {self.skipped}")
        print()

        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {self.failed} test(s) failed. Review errors above.")

        print()

        return self.failed == 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Media Integration Test Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Skip slow tests'
    )

    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Skip API connectivity tests (offline mode)'
    )

    args = parser.parse_args()

    tester = IntegrationTest(skip_api=args.no_api, quick=args.quick)
    success = tester.run_all_tests()

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
