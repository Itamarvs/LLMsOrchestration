
import pytest
from unittest.mock import MagicMock, patch
import os
import cv2
import numpy as np
from deepfake_platform.detector.video_utils import extract_frames

@pytest.fixture
def mock_video_capture():
    with patch("cv2.VideoCapture") as mock_cap:
        # Configure the mock to simulate a valid video
        cap_instance = mock_cap.return_value
        cap_instance.get.side_effect = lambda prop: 100 if prop == cv2.CAP_PROP_FRAME_COUNT else 0
        cap_instance.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))
        yield cap_instance

def test_extract_frames_success(mock_video_capture):
    with patch("cv2.imwrite") as mock_write, \
         patch("os.makedirs") as mock_makedirs, \
         patch("os.path.exists", return_value=True):
         
        output_dir = "test_frames"
        frames = extract_frames("dummy.mp4", output_dir, max_frames=5)
        
        assert len(frames) == 5
        assert mock_makedirs.called
        assert mock_write.call_count == 5

def test_extract_frames_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            extract_frames("nonexistent.mp4", "out")

def test_extract_frames_zero_frames(mock_video_capture):
    mock_video_capture.get.side_effect = lambda prop: 0 if prop == cv2.CAP_PROP_FRAME_COUNT else 0
    
    with patch("os.path.exists", return_value=True), \
         patch("os.makedirs"):
        with pytest.raises(ValueError, match="Video has 0 frames"):
            extract_frames("empty.mp4", "out")
