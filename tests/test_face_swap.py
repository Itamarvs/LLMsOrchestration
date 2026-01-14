
import pytest
from unittest.mock import MagicMock, patch
import numpy as np
import cv2
from deepfake_platform.generator.face_swap import get_face_transform, process_face_swap

@pytest.fixture
def mock_cv2():
    with patch("cv2.CascadeClassifier") as mock_cascade, \
         patch("cv2.cvtColor") as mock_cvt, \
         patch("cv2.imread") as mock_read, \
         patch("cv2.VideoCapture") as mock_cap, \
         patch("cv2.VideoWriter") as mock_writer:
         
        # Setup mock behavior
        mock_cascade.return_value.empty.return_value = False
        mock_cascade.return_value.detectMultiScale.return_value = [(10, 10, 50, 50)]
        mock_read.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap.return_value.isOpened.side_effect = [True, False] # Run loop once
        mock_cap.return_value.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))
        
        yield

def test_get_face_transform(mock_cv2):
    src_img = np.zeros((100, 100, 3), dtype=np.uint8)
    cascade = MagicMock()
    cascade.detectMultiScale.return_value = [(10, 10, 50, 50)]
    
    face_roi, rect = get_face_transform(src_img, cascade, None)
    
    assert face_roi is not None
    assert rect == (10, 10, 50, 50)

def test_get_face_transform_no_face(mock_cv2):
    src_img = np.zeros((100, 100, 3), dtype=np.uint8)
    cascade = MagicMock()
    cascade.detectMultiScale.return_value = []
    
    result = get_face_transform(src_img, cascade, None)
    assert result is None

def test_process_face_swap_flow(mock_cv2):
    # This test ensures the function runs end-to-end without error given valid mocks
    with patch("os.makedirs"):
        process_face_swap("source.jpg", "target.mp4", "output.mp4")
