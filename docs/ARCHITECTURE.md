# System Architecture

## Context Diagram

```mermaid
graph TD
    User((User))
    Detector[Deepfake Detector System]
    Generator[Deepfake Generator System]
    Gemini[Gemini API]
    
    User -->|Uploads Video| Detector
    User -->|Provides Images| Generator
    Generator -->|Creates Fakes| Detector
    Detector -->|Sends Frames| Gemini
    Gemini -->|Returns Analysis| Detector
    Detector -->|Outputs Verdict| User
```

## Container Diagram

```mermaid
graph TD
    subgraph "Deepfake Platform"
        Entry[run_detector.py]
        
        subgraph "Blue Team (Detector)"
            Agent[DeepFakeDetector Agent]
            Utils[Video Utils]
            Prompts[System Prompts]
        end
        
        subgraph "Red Team (Generator)"
            FaceSwap[Face Swap Script]
            Data[Source Images]
        end
    end
    
    Entry --> Agent
    Agent --> Utils
    Agent --> Prompts
    FaceSwap --> Data
```

## Component Details

### 1. Blue Team: Detector (`src/deepfake_platform/detector`)
- **`agent.py`**: The core orchestrator. Manages the flow of checking API keys, extracting frames, and calling the LLM.
- **`video_utils.py`**: Helper functions for OpenCV-based frame extraction.
- **`prompts.py`**: Contains the forensic persona prompt for Gemini.

### 2. Red Team: Generator (`src/deepfake_platform/generator`)
- **`face_swap.py`**: A standalone script using OpenCV Haar cascades to swap faces from source images onto target videos.

## Data Flow
1. **Input**: User provides a path to an MP4 video.
2. **Preprocessing**: `Video Utils` extracts N frames from the video.
3. **Analysis**: `DeepFakeDetector` constructs a prompt with these frames.
4. **Inference**: Prompt is sent to Gemini 1.5 Flash (via `google-generativeai`).
5. **Output**: JSON response containing `verdict`, `confidence`, and `reasoning`.

## Concurrency Considerations

This system supports **both synchronous and parallel execution**:

### Single Video Mode (Synchronous)
For individual video analysis, synchronous execution is used to keep the code simple and avoid unnecessary complexity.

### Batch Mode (Parallel)
For processing multiple videos, `run_detector.py` implements parallel execution using `concurrent.futures.ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor

def run_batch_analysis(video_paths: list[str], max_workers: int = 4) -> list[str]:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(agent.detect_deepfake, video_paths))
    return results
```

| Mode | Use Case | Implementation |
|------|----------|----------------|
| Single | `python run_detector.py video.mp4` | Synchronous |
| Batch | `python run_detector.py v1.mp4 v2.mp4 v3.mp4` | ThreadPoolExecutor (4 workers) |

**Rate Limiting**: When using batch mode, the Gemini API's rate limits still apply. The detector includes exponential backoff retry logic to handle `429 Resource Exhausted` errors gracefully.
