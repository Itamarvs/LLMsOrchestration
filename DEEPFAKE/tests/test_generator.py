
import os
import unittest
import cv2
import numpy as np

class TestDeepfakeGenerator(unittest.TestCase):
    def setUp(self):
        self.output_path = "DEEPFAKE/generator/output/test_fake.mp4"
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_output_existence(self):
        # We assume the main script ran and produced "fake_video.mp4"
        # Or we can run the processing function here.
        # Ideally, we import the function.
        
        # Checking the file produced by the main run:
        default_output = "DEEPFAKE/generator/output/fake_video.mp4"
        self.assertTrue(os.path.exists(default_output), "Output video file created")
        
        # Check if video is valid
        cap = cv2.VideoCapture(default_output)
        self.assertTrue(cap.isOpened(), "Output video can be opened")
        ret, frame = cap.read()
        self.assertTrue(ret, "Output video has at least one frame")
        cap.release()

if __name__ == '__main__':
    unittest.main()
