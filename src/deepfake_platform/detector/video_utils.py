"""Video processing utilities for frame extraction."""

import os

import cv2
import numpy as np


def extract_frames(video_path, output_dir, max_frames=5):
    """Extract evenly spaced frames from a video.
    
    Building Block Specification:
        Input Data:
            - video_path (str): Path to the source MP4 video.
            - output_dir (str): Directory to save extracted frames.
            - max_frames (int): Number of frames to extract (default=5).
            
        Output Data:
            - List[str]: Paths to the extracted image files.
            
        Setup Data:
            - None. Uses standard OS and OpenCV libraries.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        raise ValueError("Video has 0 frames")

    # Calculate indices
    indices = np.linspace(0, total_frames-1, max_frames, dtype=int)

    extracted_paths = []

    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
            cv2.imwrite(frame_path, frame)
            extracted_paths.append(frame_path)

    cap.release()
    print(f"Extracted {len(extracted_paths)} frames to {output_dir}")
    return extracted_paths
