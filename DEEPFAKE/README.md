# Deepfake Generator & Detector Project

## Project Overview
This project demonstrates Generative AI Security concepts using a Red Team / Blue Team approach:
1.  **Red Team (Generator)**: Uses OpenCV and computer vision to swap faces onto target videos.
2.  **Blue Team (Detector)**: Uses **Gemini 2.0 Flash** (Vision LLM) to analyze frames and detect manipulation artifacts.

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- A Google Cloud API Key for Gemini.

### 2. Install Dependencies
Run from the root of the repository:
```bash
pip install -r requirements.txt
# OR manually:
pip install opencv-python numpy google-generativeai python-dotenv
```

### 3. API Key Configuration (CRITICAL)
The **Detector Agent** requires a valid Gemini API key to function.

1.  Create a `.env` file in the root directory (copy from example):
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and add your key:
    ```bash
    GEMINI_API_KEY=AIzaSy...YourKeyHere
    ```
    *(Note: This file is ignored by Git to keep your secrets safe!)*

---

## 🛠️ Usage

### 🎭 1. Red Team: Generator
Creates deepfakes by swapping source faces onto target people.
*   **Logic**: Automatically matches gender (Man->Man, Woman->Woman) for realism.
*   **Inputs**: Images in `DEEPFAKE/generator/data/`
*   **Command**:
    ```bash
    python3 DEEPFAKE/generator/face_swap.py
    ```
*   **Output**: Videos saved in `DEEPFAKE/generator/output/`.

### 🛡️ 2. Blue Team: Detector
Analyzes a video file to detect if it is REAL or FAKE.
*   **Command**:
    ```bash
    python3 DEEPFAKE/run_detector.py <path_to_video>
    ```
*   **Example**:
    ```bash
    python3 DEEPFAKE/run_detector.py DEEPFAKE/generator/output/fake_real_face_man.mp4
    ```

---

## 📂 Examples
See `DEEPFAKE/examples/` for sample outputs.

### Deepfake Demo
> **Note**: This video was generated using our "Red Team" script.
<video src="examples/deepfake_demo.mp4" controls></video>
