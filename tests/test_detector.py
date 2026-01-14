
import pytest
from unittest.mock import patch, MagicMock
import os
import json
from detector.agent import DeepFakeDetector

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
    with patch("detector.agent.extract_frames") as mock_extract:
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

def test_analyze_gemini_fallback(detector):
    """Test fallback when Gemini returns invalid JSON"""
    with patch("google.generativeai.GenerativeModel") as MockModel:
        mock_instance = MockModel.return_value
        # Mock a response that isn't JSON
        mock_instance.generate_content.return_value.text = "I think it is fake."
        
        with patch("PIL.Image.open"):
            with patch("detector.agent.DETECTOR_SYSTEM_PROMPT", "prompt", create=True):
                 result = detector._analyze_with_gemini(["path/to/img.jpg"])
                 assert result["verdict"] == "UNKNOWN"
                 assert "invalid JSON" in result["reasoning"]
