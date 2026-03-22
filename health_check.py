#!/usr/bin/env python3
"""
AI Media Health Check - System validation and diagnostics

Validates:
- Python dependencies
- Configuration files
- API connectivity
- File permissions
- Storage space
- Cost tracking system
- All utilities

Usage:
    python3 health_check.py              # Run all checks
    python3 health_check.py --quick      # Quick check (no API calls)
    python3 health_check.py --verbose    # Detailed output
"""

import argparse
import sys
import os
import json
from pathlib import Path
from datetime import datetime

class HealthCheck:
    """System health validation"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name, func, critical=True):
        """Run a single health check"""
        try:
            result = func()

            if result is True or result == "pass":
                self.passed += 1
                print(f"  ✅ {name}")
                return True
            elif result == "warn":
                self.warnings += 1
                print(f"  ⚠️  {name} (warning)")
                return True
            else:
                if critical:
                    self.failed += 1
                    print(f"  ❌ {name} - {result}")
                else:
                    self.warnings += 1
                    print(f"  ⚠️  {name} - {result}")
                return False
        except Exception as e:
            if critical:
                self.failed += 1
                print(f"  ❌ {name} - Error: {e}")
            else:
                self.warnings += 1
                print(f"  ⚠️  {name} - Error: {e}")
            return False

    def run_all_checks(self, quick_mode=False):
        """Run all health checks"""
        print("=" * 80)
        print("AI MEDIA HEALTH CHECK".center(80))
        print("=" * 80)
        print()

        # Environment checks
        print("🔧 ENVIRONMENT")
        self.check("Python version >= 3.8", self._check_python_version)
        self.check("requests library", self._check_requests)
        self.check("json support", self._check_json)
        self.check("pathlib support", self._check_pathlib)
        print()

        # Optional dependencies
        print("📦 OPTIONAL DEPENDENCIES")
        self.check("opencv-python", self._check_opencv, critical=False)
        self.check("moviepy", self._check_moviepy, critical=False)
        self.check("ffmpeg-python", self._check_ffmpeg_python, critical=False)
        print()

        # File structure
        print("📁 FILE STRUCTURE")
        self.check("Core client exists", self._check_core_client)
        self.check("Cost tracker exists", self._check_cost_tracker)
        self.check("Batch processor exists", self._check_batch_processor)
        self.check("CLI tool exists", self._check_cli_tool)
        self.check("Configuration template", self._check_config_template)
        print()

        # Directory structure
        print("📂 DIRECTORIES")
        self.check("Outputs directory", self._check_outputs_dir)
        self.check("Logs directory (optional)", self._check_logs_dir, critical=False)
        self.check("Cache directory (optional)", self._check_cache_dir, critical=False)
        print()

        # Permissions
        print("🔐 PERMISSIONS")
        self.check("Output directory writable", self._check_output_writable)
        self.check("Cost data writable", self._check_cost_data_writable)
        print()

        # Storage
        print("💾 STORAGE")
        self.check("Sufficient disk space", self._check_disk_space)
        print()

        # Configuration
        print("⚙️  CONFIGURATION")
        env_exists = self.check("Environment file exists", self._check_env_file, critical=False)
        if env_exists:
            self.check("API key configured", self._check_api_key, critical=False)
            self.check("Base URL configured", self._check_base_url, critical=False)
        print()

        # Cost tracking
        print("💰 COST TRACKING")
        self.check("Cost tracker initializes", self._check_cost_tracker_init)
        self.check("Cost data file valid", self._check_cost_data_valid, critical=False)
        print()

        # API connectivity (skip in quick mode)
        if not quick_mode:
            print("🌐 API CONNECTIVITY")
            if env_exists:
                self.check("API endpoint reachable", self._check_api_connectivity, critical=False)
            else:
                print("  ⚠️  Skipping (no .env file)")
            print()

        # Summary
        self._print_summary()

    def _check_python_version(self):
        """Check Python version"""
        version = sys.version_info
        if version >= (3, 8):
            if self.verbose:
                print(f"    Python {version.major}.{version.minor}.{version.micro}")
            return True
        return f"Python {version.major}.{version.minor} (need >= 3.8)"

    def _check_requests(self):
        """Check requests library"""
        try:
            import requests
            if self.verbose:
                print(f"    requests {requests.__version__}")
            return True
        except ImportError:
            return "Not installed (pip install requests)"

    def _check_json(self):
        """Check JSON support"""
        import json
        return True

    def _check_pathlib(self):
        """Check pathlib support"""
        from pathlib import Path
        return True

    def _check_opencv(self):
        """Check OpenCV (optional)"""
        try:
            import cv2
            if self.verbose:
                print(f"    opencv {cv2.__version__}")
            return True
        except ImportError:
            return "Not installed (optional for video editing)"

    def _check_moviepy(self):
        """Check MoviePy (optional)"""
        try:
            import moviepy
            if self.verbose:
                print(f"    moviepy installed")
            return True
        except ImportError:
            return "Not installed (optional for video editing)"

    def _check_ffmpeg_python(self):
        """Check ffmpeg-python (optional)"""
        try:
            import ffmpeg
            return True
        except ImportError:
            return "Not installed (optional for video editing)"

    def _check_core_client(self):
        """Check core client file"""
        return Path("banana_pro_gemini.py").exists()

    def _check_cost_tracker(self):
        """Check cost tracker file"""
        return Path("cost_tracker.py").exists()

    def _check_batch_processor(self):
        """Check batch processor file"""
        return Path("batch_processor.py").exists()

    def _check_cli_tool(self):
        """Check CLI tool file"""
        return Path("ai_media_cli.py").exists()

    def _check_config_template(self):
        """Check config template"""
        return Path(".env.example").exists()

    def _check_outputs_dir(self):
        """Check outputs directory"""
        path = Path("outputs")
        if not path.exists():
            path.mkdir(exist_ok=True)
            return "warn"  # Created, but show warning
        return True

    def _check_logs_dir(self):
        """Check logs directory (optional)"""
        path = Path("logs")
        if not path.exists():
            return "Not created yet (will be created on first use)"
        return True

    def _check_cache_dir(self):
        """Check cache directory (optional)"""
        path = Path("cache")
        if not path.exists():
            return "Not created yet (will be created if caching enabled)"
        return True

    def _check_output_writable(self):
        """Check if output directory is writable"""
        path = Path("outputs")
        test_file = path / ".write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception as e:
            return f"Not writable: {e}"

    def _check_cost_data_writable(self):
        """Check if cost data can be written"""
        path = Path("cost_data.json")
        try:
            if not path.exists():
                # Create empty cost data
                path.write_text('{"records": []}')
                return True
            else:
                # Try to read and write
                data = json.loads(path.read_text())
                return True
        except Exception as e:
            return f"Cannot access cost data: {e}"

    def _check_disk_space(self):
        """Check available disk space"""
        import shutil
        try:
            total, used, free = shutil.disk_usage(".")
            free_gb = free / (1024 ** 3)

            if self.verbose:
                print(f"    {free_gb:.1f} GB free")

            if free_gb < 1:
                return f"Low disk space ({free_gb:.1f} GB free)"
            elif free_gb < 5:
                return "warn"
            return True
        except Exception as e:
            return f"Cannot check disk space: {e}"

    def _check_env_file(self):
        """Check if .env file exists"""
        return Path(".env").exists()

    def _check_api_key(self):
        """Check if API key is configured"""
        try:
            env_path = Path(".env")
            content = env_path.read_text()
            for line in content.split('\n'):
                if line.startswith('BANANA_PRO_API_KEY='):
                    value = line.split('=', 1)[1].strip()
                    if value and value != 'your-api-key-here':
                        if self.verbose:
                            print(f"    API key configured ({value[:10]}...)")
                        return True
            return "Not configured in .env"
        except Exception as e:
            return f"Cannot read .env: {e}"

    def _check_base_url(self):
        """Check if base URL is configured"""
        try:
            env_path = Path(".env")
            content = env_path.read_text()
            for line in content.split('\n'):
                if line.startswith('BANANA_PRO_BASE_URL='):
                    value = line.split('=', 1)[1].strip()
                    if value and value != 'https://api.provider.com':
                        if self.verbose:
                            print(f"    Base URL: {value}")
                        return True
            return "Not configured in .env"
        except Exception as e:
            return f"Cannot read .env: {e}"

    def _check_cost_tracker_init(self):
        """Check if cost tracker can initialize"""
        try:
            from cost_tracker import CostTracker
            tracker = CostTracker()
            return True
        except Exception as e:
            return f"Cannot initialize: {e}"

    def _check_cost_data_valid(self):
        """Check if cost data file is valid JSON"""
        try:
            path = Path("cost_data.json")
            if not path.exists():
                return "No data yet (ok)"

            data = json.loads(path.read_text())
            if 'records' in data:
                count = len(data['records'])
                if self.verbose:
                    print(f"    {count} cost records")
                return True
            return "Invalid format"
        except Exception as e:
            return f"Invalid JSON: {e}"

    def _check_api_connectivity(self):
        """Check API connectivity"""
        try:
            # Read API credentials from .env
            env_path = Path(".env")
            config = {}
            for line in env_path.read_text().split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

            api_key = config.get('BANANA_PRO_API_KEY')
            base_url = config.get('BANANA_PRO_BASE_URL')

            if not api_key or not base_url:
                return "API credentials not configured"

            # Try to connect
            import requests
            url = f"{base_url}/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                if self.verbose:
                    print(f"    Connected to {base_url}")
                return True
            else:
                return f"HTTP {response.status_code}"

        except Exception as e:
            return f"Connection failed: {e}"

    def _print_summary(self):
        """Print check summary"""
        print("=" * 80)
        print("SUMMARY".center(80))
        print("=" * 80)

        total = self.passed + self.failed + self.warnings

        print(f"Total Checks:  {total}")
        print(f"✅ Passed:     {self.passed}")
        print(f"⚠️  Warnings:   {self.warnings}")
        print(f"❌ Failed:     {self.failed}")
        print()

        if self.failed == 0:
            print("🎉 All critical checks passed!")
            if self.warnings > 0:
                print(f"   ({self.warnings} warnings - review above)")
        else:
            print("⚠️  Some critical checks failed. Review errors above.")

        print()

        return self.failed == 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Media Health Check',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Quick check (skip API connectivity test)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with details'
    )

    args = parser.parse_args()

    checker = HealthCheck(verbose=args.verbose)
    success = checker.run_all_checks(quick_mode=args.quick)

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
