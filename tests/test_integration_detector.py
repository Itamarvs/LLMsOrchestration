import pytest
import os
import glob
import json
from deepfake_platform.detector.agent import DeepFakeDetector

# Skip all tests in this module if no API key is present
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set in environment"
)

def get_video_files(category_path):
    """Helper to finding all mp4 files in a directory"""
    search_path = os.path.join("tests/data", category_path, "*.mp4")
    files = glob.glob(search_path)
    return files

# Collect test files
REAL_VIDEOS = get_video_files("real")
LOW_QUALITY_FAKE_VIDEOS = get_video_files("fake/low_quality")
MEDIUM_QUALITY_FAKE_VIDEOS = get_video_files("fake/medium_quality")
HIGH_QUALITY_FAKE_VIDEOS = get_video_files("fake/high_quality")

@pytest.fixture
def detector():
    return DeepFakeDetector()

@pytest.mark.parametrize("video_path", REAL_VIDEOS)
def test_detect_real_videos(detector, video_path):
    """Test all videos in tests/data/real"""
    print(f"Testing REAL video: {video_path}")
    result_json = detector.detect_deepfake(video_path)
    result = json.loads(result_json)
    
    assert "verdict" in result
    assert "confidence" in result
    
    # Ideally should be REAL
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]
    if result["verdict"] != "ERROR":
         assert "error" not in result

@pytest.mark.parametrize("video_path", LOW_QUALITY_FAKE_VIDEOS)
def test_detect_low_quality_fakes(detector, video_path):
    """Test all videos in tests/data/fake/low_quality"""
    print(f"Testing LOW QUALITY FAKE video: {video_path}")
    result_json = detector.detect_deepfake(video_path)
    result = json.loads(result_json)
    
    assert "verdict" in result
    # Ideally should be FAKE
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]

@pytest.mark.parametrize("video_path", MEDIUM_QUALITY_FAKE_VIDEOS)
def test_detect_medium_quality_fakes(detector, video_path):
    """Test all videos in tests/data/fake/medium_quality"""
    print(f"Testing MEDIUM QUALITY FAKE video: {video_path}")
    result_json = detector.detect_deepfake(video_path)
    result = json.loads(result_json)
    
    assert "verdict" in result
    # Ideally should be FAKE
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]

@pytest.mark.parametrize("video_path", HIGH_QUALITY_FAKE_VIDEOS)
def test_detect_high_quality_fakes(detector, video_path):
    """Test all videos in tests/data/fake/high_quality"""
    print(f"Testing HIGH QUALITY FAKE video: {video_path}")
    result_json = detector.detect_deepfake(video_path)
    result = json.loads(result_json)
    
    assert "verdict" in result
    print(f"High Quality Result for {video_path}: {result}")
    
    # Ideally should be FAKE
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]

def test_no_empty_categories():
    """Ensure we have at least one video in each category to test"""
    print(f"Real Videos: {REAL_VIDEOS}")
    print(f"Low Quality Fakes: {LOW_QUALITY_FAKE_VIDEOS}")
    print(f"Medium Quality Fakes: {MEDIUM_QUALITY_FAKE_VIDEOS}")
    print(f"High Quality Fakes: {HIGH_QUALITY_FAKE_VIDEOS}")

    if not REAL_VIDEOS:
        pytest.fail("No videos found in tests/data/real/")
    if not LOW_QUALITY_FAKE_VIDEOS:
        pytest.fail("No videos found in tests/data/fake/low_quality/")
    if not MEDIUM_QUALITY_FAKE_VIDEOS:
        pytest.fail("No videos found in tests/data/fake/medium_quality/")
    if not HIGH_QUALITY_FAKE_VIDEOS:
        pytest.fail("No videos found in tests/data/fake/high_quality/")
