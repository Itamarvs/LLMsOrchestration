# Deep Fake Detection with LLM Orchestration

## Project Overview
This project is part of the "LLMs Orchestration" course within the Computer Science MSc program. The primary goal is to leverage Large Language Models (LLMs) to detect whether a given video of a person/face is a deep fake or authentic.

## Objectives

### 1. Deep Fake Detection
The core mission is to design and implement a system that uses LLMs to classify videos.

### 2. Data Generation (Self-Testing)
To rigorously test the detection system, we will generate a dataset of deep fake videos.

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- A Google Cloud API Key for Gemini.

### 2. Install Dependencies
Run from the root of the repository:
```bash
pip install -e .
```

### 3. API Key Configuration
Create a `.env` file:
```bash
GEMINI_API_KEY=AIzaSy...YourKeyHere
```

> [!NOTE]
> **For Graders / Testing without a Key:**
> If you do not have a Gemini API Key, the tool will automatically detect this and offer to run in **Mock Mode**.
> In Mock Mode, the system simulates the analysis process and returns a result based on heuristics, allowing you to verify the application flow and logic without an external dependency.

### 4. 🎥 Demo
Check out the system in action:

https://github.com/user-attachments/assets/deepfake_demo.mp4

*(A sample deepfake video is available in `examples/deepfake_demo.mp4`)*

## 🛠️ Usage

### 🎭 1. Red Team: Generator
Creates deepfakes by swapping source faces onto target people.
*   **Command**:
    ```bash
    python src/deepfake_platform/generator/face_swap.py
    ```
*   **Output**: Videos saved in `src/deepfake_platform/generator/output/`.

### 🛡️ 2. Blue Team: Detector
Analyzes a video file to detect if it is REAL or FAKE.

**Single Video:**
```bash
python run_detector.py <path_to_video>
```

**Batch Mode (Parallel):**
```bash
python run_detector.py video1.mp4 video2.mp4 video3.mp4
```

**Example:**
```bash
python run_detector.py src/deepfake_platform/generator/output/fake_real_face_man.mp4
```
