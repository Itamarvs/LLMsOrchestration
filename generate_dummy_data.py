
import cv2
import numpy as np
import os

def generate_dummy_face(path):
    # Draw a simple face on a white background
    img = np.zeros((500, 500, 3), dtype=np.uint8) + 255
    # Yellow Face
    cv2.circle(img, (250, 250), 100, (0, 255, 255), -1)
    # Eyes
    cv2.circle(img, (220, 230), 10, (0, 0, 0), -1)
    cv2.circle(img, (280, 230), 10, (0, 0, 0), -1)
    # Smile
    cv2.ellipse(img, (250, 280), (40, 20), 0, 0, 180, (0, 0, 0), 3)
    
    cv2.imwrite(path, img)
    print(f"Generated dummy face at {path}")

def generate_dummy_video(path):
    width, height = 640, 480
    fps = 30
    seconds = 3
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    for i in range(fps * seconds):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Moving Blue circle (Head)
        cx = 320 + int(50 * np.sin(i * 0.1))
        cy = 240
        cv2.circle(frame, (cx, cy), 80, (255, 0, 0), -1)
        # Eyes (to be detected as face)
        cv2.circle(frame, (cx-20, cy-20), 8, (255, 255, 255), -1)
        cv2.circle(frame, (cx+20, cy-20), 8, (255, 255, 255), -1)
        # Mouth
        cv2.line(frame, (cx-20, cy+30), (cx+20, cy+30), (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"Generated dummy video at {path}")

if __name__ == "__main__":
    os.makedirs("DEEPFAKE/generator/data", exist_ok=True)
    generate_dummy_face("DEEPFAKE/generator/data/source_face.jpg")
    generate_dummy_video("DEEPFAKE/generator/data/target_video.mp4")
