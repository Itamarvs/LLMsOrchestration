
import subprocess
import os
import sys

def test_cli_help():
    """Verify that the CLI help command runs successfully."""
    result = subprocess.run(
        [sys.executable, "run_detector.py"],
        capture_output=True,
        text=True
    )
    # No args should print usage and exit 0 or 1 depending on implementation
    # Current implementation exits 1 if no args
    assert "Usage:" in result.stdout or "Usage:" in result.stderr

def test_cli_mock_run():
    """Verify that we can run the detector in a way that doesn't crash."""
    # We use a non-existent file to trigger the 'error' path which is fast and safe
    # Or checking if a real file exists to run against.
    
    video_path = "tests/data/fake/low_quality/fake_video.mp4"
    if os.path.exists(video_path):
        # We assume GEMINI_API_KEY is present or it will fail gracefully/mock
        # But for E2E speed, we might want to just check the error handling if key missing
        pass
    
    result = subprocess.run(
        [sys.executable, "run_detector.py", "non_existent_video.mp4"],
        capture_output=True,
        text=True
    )
    # Should output error about file not found
    assert "error" in result.stdout.lower() or "missing" in result.stdout.lower()

if __name__ == "__main__":
    try:
        test_cli_help()
        test_cli_mock_run()
        print("✅ E2E CLI verified successfully")
    except AssertionError as e:
        print(f"❌ E2E CLI verification failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)
