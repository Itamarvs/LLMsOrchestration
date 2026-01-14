# Product Requirements Document (PRD)

## Problem Statement
The proliferation of deepfake technology poses a significant threat to information integrity. Identifying manipulated media is becoming increasingly difficult for humans. There is a need for an automated system that can analyze video content and determine its authenticity using advanced reasoning capabilities of Large Language Models (LLMs).

## User Requirements

### Functional Requirements
- **Deepfake Detection (Blue Team)**:
    - Users must be able to input a video file.
    - The system must extract frames from the video.
    - The system must use an LLM (Gemini) to analyze visual artifacts (lighting, shadows, blinking, lip-sync).
    - The system must output a verdict (REAL/FAKE) with a confidence score and reasoning.
- **Data Generation (Red Team)**:
    - Users must be able to generate deepfake videos for testing purposes.
    - The system should support face swapping functionality.

### Non-Functional Requirements
- **Accuracy**: The system should account for rate limits and potential API errors.
- **Traceability**: All analysis steps should be logged.
- **Usability**: The system should be runnable via a simple CLI command.

## Key Performance Indicators (KPIs)
- **Detection Accuracy**: Percentage of correctly classified videos (Real vs Fake).
- **False Positive Rate**: Percentage of real videos incorrectly flagged as fake.
- **Analysis Latency**: Time taken to return a verdict.

## Timeline / Milestones
- **Milestone 1**: Core Detector Logic (Completed).
- **Milestone 2**: Red Team Generator (Completed).
- **Milestone 3**: Orchestrated Verification System (Current).
