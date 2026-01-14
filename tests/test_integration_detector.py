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
    
    # We don't assert the specific verdict (REAL/FAKE) as ML models can be non-deterministic
    # and we want to test the plumbing, not the accuracy here.
    assert result["verdict"] in ["REAL", "FAKE", "UNKNOWN", "ERROR"]
    
    # If successful, there shouldn't be a top-level error (unless it's a model error)
    if result["verdict"] != "ERROR":
         assert "error" not in result
