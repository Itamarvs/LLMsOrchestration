#!/usr/bin/env python3
"""CLI entry point for the Deepfake Detector.

This script demonstrates:
1. Single video analysis
2. Batch parallel processing using concurrent.futures
"""

import sys
from concurrent.futures import ThreadPoolExecutor

from deepfake_platform.detector.agent import DeepFakeDetector


def run_single_analysis(video_path: str) -> str:
    """Analyze a single video for deepfake detection."""
    agent = DeepFakeDetector()
    print("--- Blue Team Operation Initiated ---")
    result = agent.detect_deepfake(video_path)
    print("\n--- Mission Report ---")
    print(result)
    return result


def run_batch_analysis(video_paths: list[str], max_workers: int = 4) -> list[str]:
    """Analyze multiple videos in parallel using ThreadPoolExecutor.

    Args:
        video_paths: List of paths to video files.
        max_workers: Maximum number of parallel threads.

    Returns:
        List of JSON result strings for each video.
    """
    agent = DeepFakeDetector()
    print(f"--- Batch Analysis: {len(video_paths)} videos, {max_workers} workers ---")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(agent.detect_deepfake, video_paths))

    print(f"\n--- Batch Complete: {len(results)} results ---")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_detector.py <video_path> [video_path2 ...]")
        print("       Single video: python run_detector.py video.mp4")
        print("       Batch mode:   python run_detector.py vid1.mp4 vid2.mp4 vid3.mp4")
        sys.exit(1)

    if len(sys.argv) == 2:
        # Single video mode
        run_single_analysis(sys.argv[1])
    else:
        # Batch parallel mode
        videos = sys.argv[1:]
        results = run_batch_analysis(videos)
        for i, res in enumerate(results):
            print(f"\n=== Video {i+1}: {videos[i]} ===")
            print(res)
