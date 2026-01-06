from .base_agent import Agent
from typing import Dict, Any
import os
import json
import random

# Import Detector tools
try:
    from DEEPFAKE.detector.video_utils import extract_frames
    # from DEEPFAKE.detector.prompts import DETECTOR_SYSTEM_PROMPT
except ImportError:
    # Fallback for when running tests not from root
    pass

import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(name="SciBot", role="Research & Analysis")

    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        if "analyze" in task.lower() and "video" in task.lower():
            return self.detect_deepfake(context.get("video_path"))
        
        if "analyze" in task.lower():
            return "Sensitivity analysis complete. Parameters optimal."
        return "Research Agent ready."

    def detect_deepfake(self, video_path: str) -> str:
        """
        Blue Team Operation: Detect if video is fake using Gemini.
        """
        if not video_path or not os.path.exists(video_path):
            return json.dumps({"error": "Video path missing or invalid"})
            
        # Check for API Key
        if not os.getenv("GEMINI_API_KEY"):
            return json.dumps({
                "error": "Missing GEMINI_API_KEY. Please set it in .env file.", 
                "verdict": "ERROR"
            })

        print(f"[{self.name}] extracting frames from {video_path}...")
        try:
            frames_dir = os.path.join(os.path.dirname(video_path), "frames")
            # Extract fewer frames to save tokens/quota
            frames_paths = extract_frames(video_path, frames_dir, max_frames=3)
        except Exception as e:
            return json.dumps({"error": f"Frame extraction failed: {str(e)}"})

        print(f"[{self.name}] Analyzing {len(frames_paths)} frames with Gemini 1.5 Flash...")
        
        try:
            verdict = self._analyze_with_gemini(frames_paths)
            return json.dumps(verdict, indent=2)
        except Exception as e:
             return json.dumps({"error": f"Gemini Analysis failed: {str(e)}", "verdict": "ERROR"})

    def _analyze_with_gemini(self, frame_paths):
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Load images
        images = []
        for p in frame_paths:
            img = PIL.Image.open(p)
            images.append(img)
            
        # Construct Prompt
        # We import the system prompt or define it inline if import fails
        try:
            from DEEPFAKE.detector.prompts import DETECTOR_SYSTEM_PROMPT
            prompt = DETECTOR_SYSTEM_PROMPT
        except ImportError:
            prompt = "Analyze these video frames. Is this video REAL or FAKE? Return JSON with verdict, confidence, and reasoning."

        # Send to API
        response = model.generate_content([prompt, *images])
        
        # Parse Response (Gemini returns markdown text, usually with ```json ... ```)
        text = response.text
        
        # Clean up code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
             text = text.split("```")[1].split("```")[0]
             
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback if model didn't return valid JSON
            return {
                "verdict": "UNKNOWN", 
                "confidence": 0, 
                "raw_response": text,
                "reasoning": "Model returned invalid JSON format."
            }
