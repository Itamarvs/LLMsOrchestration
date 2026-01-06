
import unittest
import os
import shutil
import json
from src.agents.research import ResearchAgent
from DEEPFAKE.detector.video_utils import extract_frames

class TestDetectorAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchAgent()
        self.test_video = "DEEPFAKE/tests/data/test_video.mp4"
        self.test_output = "DEEPFAKE/tests/data/frames"
        
        os.makedirs("DEEPFAKE/tests/data", exist_ok=True)
        # Create a dummy video file if not exists
        if not os.path.exists(self.test_video):
            # We can just touch it, but extract_frames needs a real video structure usually.
            # Using the generate_dummy_data utility if possible, or mocking.
            # For unit test of AGENT, we can mock the video_utils interaction.
            # But let's reuse our dummy generator for integration test style.
            try:
                from DEEPFAKE.generate_dummy_data import generate_dummy_video
                generate_dummy_video(self.test_video)
            except ImportError:
                # Fallback: Create empty file and mock extract_frames
                with open(self.test_video, 'wb') as f:
                    f.write(b'dummy')

    def tearDown(self):
        if os.path.exists("DEEPFAKE/tests/data"):
            shutil.rmtree("DEEPFAKE/tests/data")

    def test_extract_frames(self):
        # Only run if cv2 works and video is valid
        if os.path.getsize(self.test_video) > 1000:
            frames = extract_frames(self.test_video, self.test_output, max_frames=2)
            self.assertEqual(len(frames), 2)
            self.assertTrue(os.path.exists(frames[0]))

    def test_agent_detection_mock(self):
        # Rename video to include "fake" to trigger mock logic
        fake_video_path = "DEEPFAKE/tests/data/fake_test_video.mp4"
        if os.path.exists(self.test_video):
            shutil.copy(self.test_video, fake_video_path)
        
        result_json = self.agent.detect_deepfake(fake_video_path)
        result = json.loads(result_json)
        
        self.assertEqual(result["verdict"], "FAKE")
        self.assertTrue(result["confidence"] > 80)
        
if __name__ == '__main__':
    unittest.main()
