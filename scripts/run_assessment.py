
import os
import json
import sys
# Add root to python path
sys.path.append(os.getcwd())

from detector.agent import DeepFakeDetector

def run_assessment():
    print("--- Self-Assessment Agent: Deepfake Project Evaluation ---")
    score = 0
    max_score = 3
    
    # Criteria 1: Generator Output Exists
    fake_video = "generator/output/fake_video.mp4"
    if os.path.exists(fake_video):
        print(f"[PASS] Generator created video: {fake_video}")
        score += 1
    else:
        print(f"[FAIL] Missing generator output: {fake_video}")

    # Criteria 2: Detector Agent exists and is runnable
    try:
        agent = DeepFakeDetector()
        print(f"[PASS] Detector Agent initialized.")
        score += 1
    except Exception as e:
        print(f"[FAIL] Detector Agent init failed: {e}")

    # Criteria 3: Detector produces verdict
    try:
        if os.path.exists(fake_video):
            res_json = agent.detect_deepfake(fake_video)
            res = json.loads(res_json)
            if "verdict" in res and "confidence" in res:
                print(f"[PASS] Detector produced valid verdict: {res['verdict']}")
                score += 1
            else:
                print(f"[FAIL] Detector output format invalid: {res_json}")
        else:
            print("[SKIP] Cannot test detector without video.")
    except Exception as e:
        print(f"[FAIL] Detector execution failed: {e}")
        
    print(f"\nFinal Score: {score}/{max_score}")
    if score == max_score:
        print("SUCCESS: Project meets all Deepfake technical criteria.")
    else:
        print("WARNING: Project is incomplete.")

if __name__ == "__main__":
    run_assessment()
