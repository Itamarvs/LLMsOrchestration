
import pytest
from unittest.mock import patch, MagicMock
import os
import json
from deepfake_platform.detector.agent import DeepFakeDetector

@pytest.fixture
def detector():
    return DeepFakeDetector()

def test_detector_initialization(detector):
    assert detector.name == "BlueTeam-Detector"

def test_detector_missing_video(detector):
    result = detector.detect_deepfake("non_existent_video.mp4")
    data = json.loads(result)
    assert "error" in data
    assert "missing or invalid" in data["error"]

def test_detector_deepfake_mock(detector):
    # Mock extract_frames and _analyze_with_gemini
    with patch("deepfake_platform.detector.agent.extract_frames") as mock_extract:
        with patch.object(detector, "_analyze_with_gemini") as mock_analyze:
            with patch("os.path.exists") as mock_exists:
                with patch("os.getenv") as mock_getenv:
                    # Setup mocks
                    mock_exists.return_value = True
                    mock_getenv.return_value = "fake_key"
                    mock_extract.return_value = ["frame1.jpg"]
                    mock_analyze.return_value = {"verdict": "FAKE", "confidence": 0.9}
                    
                    # Test
                    result = detector.detect_deepfake("dummy.mp4")
                    data = json.loads(result)
                    
                    assert data["verdict"] == "FAKE"
                    assert data["confidence"] == 0.9

    """Test fallback when Gemini returns invalid JSON"""
    with patch("google.generativeai.GenerativeModel") as MockModel:
        mock_instance = MockModel.return_value
        # Mock a response that isn't JSON
        mock_instance.generate_content.return_value.text = "I think it is fake."
        
        with patch("PIL.Image.open"):
            with patch("deepfake_platform.detector.agent.DETECTOR_SYSTEM_PROMPT", "prompt", create=True):
                 result = detector._analyze_with_gemini(["path/to/img.jpg"])
                 # The result is parsed from the response object, so we check the result of _analyze_with_gemini
                 # which calls _retry_with_backoff, which calls _parse_gemini_response
                 assert result["verdict"] == "UNKNOWN"
                 assert "invalid JSON" in result["reasoning"]

def test_retry_on_quota_error(detector):
    """Test that the detector retries on 429 errors."""
    mock_func = MagicMock()
    # Side effects: Fail twice with 429, then succeed
    mock_func.side_effect = [
        Exception("429 Resource exhausted"),
        Exception("Quota exceeded"),
        MagicMock(text='{"verdict": "REAL", "confidence": 0.95, "reasoning": "Looks real"}')
    ]
    
    # We need to mock time.sleep to avoid waiting during tests
    with patch("time.sleep") as mock_sleep:
        result = detector._retry_with_backoff(mock_func, max_retries=3)
        
        # Should have called the function 3 times (2 fails + 1 success)
        assert mock_func.call_count == 3
        # Should have slept twice
        assert mock_sleep.call_count == 2
        # Result should be parsed correctly
        assert result["verdict"] == "REAL"
        assert result["confidence"] == 0.95
