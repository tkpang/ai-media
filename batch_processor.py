#!/usr/bin/env python3
"""
Batch Processor for AI Media Generation

Process multiple prompts efficiently with:
- Parallel processing
- Progress tracking
- Error handling and retry logic
- Cost estimation and limits
- Result organization

Usage:
    from batch_processor import BatchProcessor

    processor = BatchProcessor(client, max_workers=3)
    results = processor.process_image_batch(prompts)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BatchJob:
    """Single job in a batch"""
    job_id: str
    prompt: str
    params: Dict  # Additional parameters (route, aspect_ratio, etc.)
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[Dict] = None
    error: Optional[str] = None
    attempts: int = 0
    created_at: str = ""
    completed_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class BatchProcessor:
    """Process multiple AI generation jobs efficiently"""

    def __init__(
        self,
        client,  # BananaProClient or SeedanceClient
        max_workers: int = 3,
        max_retries: int = 3,
        retry_delay: int = 5,
        max_cost: Optional[float] = None
    ):
        """
        Initialize batch processor

        Args:
            client: API client instance
            max_workers: Maximum parallel workers (default: 3)
            max_retries: Maximum retry attempts per job (default: 3)
            retry_delay: Seconds to wait between retries (default: 5)
            max_cost: Maximum total cost limit (optional)
        """
        self.client = client
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_cost = max_cost
        self.total_cost = 0.0

    def process_image_batch(
        self,
        prompts: List[str],
        route: str = "2K_2",
        aspect_ratio: str = "1:1",
        output_dir: str = "outputs/batch",
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Process a batch of image generation prompts

        Args:
            prompts: List of text prompts
            route: Model route to use
            aspect_ratio: Image aspect ratio
            output_dir: Directory for output images
            progress_callback: Optional callback(current, total, job)

        Returns:
            dict with results summary
        """
        # Create jobs
        jobs = []
        for i, prompt in enumerate(prompts):
            job = BatchJob(
                job_id=f"img_{i:04d}",
                prompt=prompt,
                params={
                    "route": route,
                    "aspect_ratio": aspect_ratio,
                    "output_dir": output_dir
                }
            )
            jobs.append(job)

        # Process jobs
        return self._process_jobs(
            jobs,
            self._process_image_job,
            progress_callback
        )

    def process_video_batch(
        self,
        prompts: List[str],
        duration: int = 10,
        resolution: str = "1080p",
        output_dir: str = "outputs/batch",
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Process a batch of video generation prompts

        Args:
            prompts: List of text prompts
            duration: Video duration in seconds
            resolution: Video resolution
            output_dir: Directory for output videos
            progress_callback: Optional callback(current, total, job)

        Returns:
            dict with results summary
        """
        # Create jobs
        jobs = []
        for i, prompt in enumerate(prompts):
            job = BatchJob(
                job_id=f"vid_{i:04d}",
                prompt=prompt,
                params={
                    "duration": duration,
                    "resolution": resolution,
                    "output_dir": output_dir
                }
            )
            jobs.append(job)

        # Process jobs
        return self._process_jobs(
            jobs,
            self._process_video_job,
            progress_callback
        )

    def _process_jobs(
        self,
        jobs: List[BatchJob],
        job_handler: Callable,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Process jobs with parallel execution

        Args:
            jobs: List of BatchJob instances
            job_handler: Function to process each job
            progress_callback: Optional progress callback

        Returns:
            dict with summary statistics
        """
        total_jobs = len(jobs)
        completed = 0
        failed = 0
        results = []

        print(f"Starting batch processing: {total_jobs} jobs")
        print(f"Max parallel workers: {self.max_workers}")
        print()

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(job_handler, job): job
                for job in jobs
            }

            # Process completed jobs
            for future in as_completed(future_to_job):
                job = future_to_job[future]

                try:
                    result = future.result()
                    job.status = "completed"
                    job.result = result
                    job.completed_at = datetime.now().isoformat()
                    completed += 1

                    # Update cost
                    if result and 'cost' in result:
                        self.total_cost += result['cost']

                except Exception as e:
                    job.status = "failed"
                    job.error = str(e)
                    failed += 1
                    print(f"✗ Job {job.job_id} failed: {e}")

                results.append(job)

                # Progress callback
                if progress_callback:
                    progress_callback(completed + failed, total_jobs, job)

                # Print progress
                self._print_progress(completed, failed, total_jobs)

                # Check cost limit
                if self.max_cost and self.total_cost >= self.max_cost:
                    print(f"\n⚠ Cost limit reached (${self.max_cost:.2f})")
                    print("Cancelling remaining jobs...")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

        end_time = time.time()
        duration = end_time - start_time

        # Summary
        summary = {
            "total_jobs": total_jobs,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total_jobs * 100) if total_jobs > 0 else 0,
            "total_cost": self.total_cost,
            "duration_seconds": duration,
            "avg_time_per_job": duration / total_jobs if total_jobs > 0 else 0,
            "jobs": [asdict(job) for job in results]
        }

        return summary

    def _process_image_job(self, job: BatchJob) -> Dict:
        """Process single image generation job with retries"""
        attempts = 0

        while attempts < self.max_retries:
            try:
                job.status = "processing"
                job.attempts = attempts + 1

                # Create output path
                output_dir = Path(job.params.get("output_dir", "outputs/batch"))
                output_dir.mkdir(parents=True, exist_ok=True)
                save_path = output_dir / f"{job.job_id}.png"

                # Generate image
                result = self.client.generate_image(
                    prompt=job.prompt,
                    route=job.params.get("route", "2K_2"),
                    aspect_ratio=job.params.get("aspect_ratio", "1:1"),
                    save_path=str(save_path)
                )

                print(f"✓ Job {job.job_id} completed")
                return result

            except Exception as e:
                attempts += 1
                if attempts >= self.max_retries:
                    raise e

                print(f"⚠ Job {job.job_id} failed (attempt {attempts}/{self.max_retries}), retrying...")
                time.sleep(self.retry_delay)

    def _process_video_job(self, job: BatchJob) -> Dict:
        """Process single video generation job with retries"""
        attempts = 0

        while attempts < self.max_retries:
            try:
                job.status = "processing"
                job.attempts = attempts + 1

                # Create output path
                output_dir = Path(job.params.get("output_dir", "outputs/batch"))
                output_dir.mkdir(parents=True, exist_ok=True)
                save_path = output_dir / f"{job.job_id}.mp4"

                # Generate video
                result = self.client.generate_video(
                    prompt=job.prompt,
                    duration=job.params.get("duration", 10),
                    resolution=job.params.get("resolution", "1080p"),
                    save_path=str(save_path)
                )

                print(f"✓ Job {job.job_id} completed")
                return result

            except Exception as e:
                attempts += 1
                if attempts >= self.max_retries:
                    raise e

                print(f"⚠ Job {job.job_id} failed (attempt {attempts}/{self.max_retries}), retrying...")
                time.sleep(self.retry_delay)

    def _print_progress(self, completed: int, failed: int, total: int):
        """Print progress bar"""
        processed = completed + failed
        percent = (processed / total * 100) if total > 0 else 0

        bar_length = 40
        filled = int(bar_length * processed / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        status = f"[{bar}] {percent:5.1f}% | ✓{completed} ✗{failed} / {total}"
        print(f"\r{status}", end="", flush=True)

        if processed >= total:
            print()  # New line when complete

    def save_results(self, summary: Dict, output_file: str = "batch_results.json"):
        """Save batch processing results"""
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\nResults saved to {output_file}")

    def print_summary(self, summary: Dict):
        """Print formatted summary"""
        print()
        print("=" * 70)
        print("Batch Processing Summary")
        print("=" * 70)
        print(f"Total Jobs: {summary['total_jobs']}")
        print(f"Completed: {summary['completed']} (✓)")
        print(f"Failed: {summary['failed']} (✗)")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Cost: ${summary['total_cost']:.2f}")
        print(f"Duration: {summary['duration_seconds']:.1f}s")
        print(f"Avg Time/Job: {summary['avg_time_per_job']:.1f}s")
        print("=" * 70)


def example_usage():
    """Example batch processing"""
    print("Batch Processor Example")
    print()

    # Example prompts
    prompts = [
        "A serene mountain landscape at sunset",
        "A futuristic cityscape with flying cars",
        "A cozy coffee shop interior",
        "A tropical beach with palm trees",
        "A snowy forest in winter"
    ]

    print(f"Processing {len(prompts)} image generation jobs...")
    print()

    # Note: This requires a working client
    # Uncomment when you have API credentials
    """
    from banana_pro_with_tracking import BananaProWithTracking

    client = BananaProWithTracking(
        api_key="your-key",
        cost_per_image=0.045
    )

    processor = BatchProcessor(
        client=client,
        max_workers=3,
        max_cost=1.0  # Stop after $1
    )

    summary = processor.process_image_batch(
        prompts=prompts,
        route="2K_2",
        aspect_ratio="16:9"
    )

    processor.print_summary(summary)
    processor.save_results(summary)
    """

    print("Batch processor ready to use!")
    print("Configure with your API client to start processing.")


if __name__ == "__main__":
    example_usage()
