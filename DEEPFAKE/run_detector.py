
import sys
import os

# Add root to python path
sys.path.append(os.getcwd())

from src.agents.research import ResearchAgent

def run_blue_team_operation(video_path):
    agent = ResearchAgent()
    print("--- Blue Team Operation Initiated ---")
    result = agent.perform_task(f"Analyze video {video_path} for signs of Deepfake", {"video_path": video_path})
    print("\n--- Mission Report ---")
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_detector.py <video_path>")
        # Default to the generated fake
        video = "DEEPFAKE/generator/output/fake_video.mp4"
    else:
        video = sys.argv[1]
    
    run_blue_team_operation(video)
