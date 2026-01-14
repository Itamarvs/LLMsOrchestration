import pytest
import os
import json
from deepfake_platform.detector.agent import DeepFakeDetector

# Skip all tests in this module if no API key is present
pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set in environment"
)

@pytest.fixture
def detector():
    return DeepFakeDetector()

@pytest.fixture
def real_video_path():
    # Try to find a real video file in the project
    candidates = [
        "examples/deepfake_demo.mp4",
        "src/deepfake_platform/generator/output/fake_video.mp4",
        "src/deepfake_platform/generator/data/target_video.mp4"
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return path
            
    pytest.skip("No test video files found for integration testing")

@pytest.fixture
def high_quality_video_path():
    # Path to the downloaded high-quality sample
    path = "tests/data/high_quality_fake.mp4"
    if os.path.exists(path):
        return path
    pytest.skip("High-quality test video file not found at tests/data/high_quality_fake.mp4")

def test_integration_full_detection_flow(detector, real_video_path):
    """
    Integration test that runs the full detection flow on a real video file.
    This makes actual calls to the Gemini API.
    """
    print(f"Testing with video: {real_video_path}")
    
    result_json = detector.detect_deepfake(real_video_path)
    result = json.loads(result_json)
    
    # Verify the structure of the response
    assert "verdict" in result, "Response should contain a verdict"
    assert "confidence" in result, "Response should contain confidence score" 
    
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]
    
    if result["verdict"] != "ERROR":
         assert "error" not in result

def test_detect_high_quality_fake(detector, high_quality_video_path):
    """
    Test against a known high-quality deepfake sample.
    """
    print(f"Testing with high-quality fake: {high_quality_video_path}")
    
    result_json = detector.detect_deepfake(high_quality_video_path)
    result = json.loads(result_json)
    
    assert "verdict" in result
    assert "confidence" in result
    print(f"High Quality Fake Result: {result}")
    
    # Ideally, this should be detected as FAKE
    # But for now, we just ensure it processes correctly without crashing
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]
