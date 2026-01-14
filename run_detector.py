import sys
import os

# Add root to python path
sys.path.append(os.getcwd())

from detector.agent import DeepFakeDetector

def run_blue_team_operation(video_path):
    agent = DeepFakeDetector()
    print("--- Blue Team Operation Initiated ---")
    result = agent.detect_deepfake(video_path)
    print("\n--- Mission Report ---")
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_detector.py <video_path>")
        # Default to the generated fake
        video = "generator/output/fake_video.mp4"
    else:
        video = sys.argv[1]
    
    run_blue_team_operation(video)
