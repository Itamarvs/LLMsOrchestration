# Deep Fake Detection with LLM Orchestration

## Project Overview
This project is part of the "LLMs Orchestration" course within the Computer Science MSc program. The primary goal is to leverage Large Language Models (LLMs) to detect whether a given video of a person/face is a deep fake or authentic.

## Objectives

### 1. Deep Fake Detection
The core mission is to design and implement a system that uses LLMs to classify videos. This involves:
-   **Video Processing**: Extracting relevant information from video inputs.
-   **Prompt Engineering**: Sending specific, sophisticated, and well-designed prompts to an LLM to analyze the visual or audio cues.
-   **Classification**: Determining if the content is real or fake based on the LLM's reasoning.

### 2. Data Generation (Self-Testing)
To rigorously test the detection system, we will generate a dataset of deep fake videos.
-   **Method**: Using tools such as OpenCV or dedicated Google tools.
-   **Input**: Real static images of people/faces serve as the "seed" for generation.
-   **Output**: A variety of deep fake videos to benchmark our detector.

---

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

---

## Course Context
-   **Course**: LLMs Orchestration
-   **Program**: MSc in Computer Science
-   **Focus**: Practical application of LLM orchestration in security and media forensics.
