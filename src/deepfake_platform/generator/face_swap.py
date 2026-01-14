"""Face swap generator for creating deepfake test videos."""

import os
import sys

import cv2
import numpy as np


def get_face_transform(src_img, face_cascade, eye_cascade):
    """Extract face region and bounding box from source image."""
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face_roi_color = src_img[y:y+h, x:x+w]

    # Simple approach: Return the face ROI and its center relative to image
    return face_roi_color, (x, y, w, h)

def process_face_swap(source_path, target_path, output_path):
    """Swap face from source image onto faces in target video."""
    print("Starting Face Swap (OpenCV Haar Mode)...")

    # Load Cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    if face_cascade.empty():
        print("Error: Could not load Haar classifier.")
        return

    # Process Source
    img_src = cv2.imread(source_path)
    res = get_face_transform(img_src, face_cascade, None)

    if res:
        src_face_img, src_rect = res
    else:
        print("Warning: No face found in source image. Using full image.")
        src_face_img = img_src
        h, w = img_src.shape[:2]
        h, w = img_src.shape[:2]
        # src_rect = (0, 0, w, h)

    # Create an oval mask for the source face (simple feathering)
    src_h, src_w = src_face_img.shape[:2]
    mask = np.zeros((src_h, src_w, 3), dtype=np.uint8)
    cv2.ellipse(mask, (src_w//2, src_h//2), (src_w//2, src_h//2), 0, 0, 360, (255, 255, 255), -1)
    mask = cv2.GaussianBlur(mask, (21, 21), 11)

    # Process Target Video
    cap = cv2.VideoCapture(target_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # Resize source face to match target face rect
            try:
                resized_src = cv2.resize(src_face_img, (w, h))
                resized_mask = cv2.resize(mask, (w, h))

                # Region of Interest in Target
                roi = frame[y:y+h, x:x+w]

                # Blend: ROI = ROI*(1-mask) + Source*mask
                # Convert mask to float 0-1
                mask_norm = resized_mask / 255.0

                # Perform blending
                roi_float = roi.astype(float)
                src_float = resized_src.astype(float)

                blended = roi_float * (1.0 - mask_norm) + src_float * mask_norm

                # Place back
                frame[y:y+h, x:x+w] = blended.astype(np.uint8)

                # Debug: Draw rectangle
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            except Exception as e:
                print(f"Error blending frame {frame_count}: {e}")

        out.write(frame)
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames")

    cap.release()
    out.release()
    print(f"Done. Output: {output_path}")

if __name__ == "__main__":
    import glob

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    target_video = os.path.join(data_dir, "target_video.mp4")

    # Find all source images (jpg, png)
    sources = glob.glob(os.path.join(data_dir, "*.png")) + glob.glob(os.path.join(data_dir, "*.jpg"))
    # Exclude frame files and dummy source
    sources = [s for s in sources if "frame_" not in s and "source_face.jpg" not in s]

    if not sources:
        print("No source images found in data/.")
        sys.exit(1)

    for source in sources:
        base_name = os.path.splitext(os.path.basename(source))[0]

        # Determine demographic match
        if "man" in base_name and "woman" not in base_name:
            target_video = os.path.join(data_dir, "target_video_man.mp4")
        elif "woman" in base_name:
             target_video = os.path.join(data_dir, "target_video_woman.mp4")
        else:
             target_video = os.path.join(data_dir, "target_video.mp4") # Fallback

        output = os.path.join(output_dir, f"fake_{base_name}.mp4")

        if os.path.exists(target_video):
            print(f"Processing {base_name} -> {os.path.basename(target_video)}...")
            process_face_swap(source, target_video, output)
        else:
            print(f"Skipping {base_name}: Missing target ({target_video})")
