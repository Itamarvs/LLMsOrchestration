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

## Usage
The project is designed to be usable by others. It supports a workflow where a user can provide a video file, and the system processes it to output a determination: **Deep Fake** or **Authentic**.

## Course Context
-   **Course**: LLMs Orchestration
-   **Program**: MSc in Computer Science
-   **Focus**: Practical application of LLM orchestration in security and media forensics.
