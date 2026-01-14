import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
from typing import Dict, Any, List
import time
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Detector tools
try:
    from .video_utils import extract_frames
except ImportError:
    pass

class DeepFakeDetector:
    def __init__(self):
        self.name = "BlueTeam-Detector"
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            logger.warning("GEMINI_API_KEY not found in environment variables.")

    def detect_deepfake(self, video_path: str) -> str:
        """
        Blue Team Operation: Detect if video is fake using Gemini.

        Args:
            video_path (str): Path to the video file to analyze.

        Returns:
             str: JSON string containing the verdict and confidence.
        """
        if not video_path or not os.path.exists(video_path):
            return json.dumps({"error": "Video path missing or invalid"})
            
        # Check for API Key
        if not os.getenv("GEMINI_API_KEY"):
            return json.dumps({
                "error": "Missing GEMINI_API_KEY. Please set it in .env file.", 
                "verdict": "ERROR"
            })

        logger.info(f"[{self.name}] extracting frames from {video_path}...")
        try:
            frames_dir = os.path.join(os.path.dirname(video_path), "frames")
            # Extract fewer frames to save tokens/quota
            frames_paths = extract_frames(video_path, frames_dir, max_frames=3)
        except Exception as e:
            return json.dumps({"error": f"Frame extraction failed: {str(e)}"})

        logger.info(f"[{self.name}] Analyzing {len(frames_paths)} frames with Gemini 1.5 Flash...")
        
        try:
            verdict = self._analyze_with_gemini(frames_paths)
            return json.dumps(verdict, indent=2)
        except Exception as e:
             return json.dumps({"error": f"Gemini Analysis failed: {str(e)}", "verdict": "ERROR"})

    def _analyze_with_gemini(self, frame_paths: List[str]) -> Dict[str, Any]:
        """Internal method to call Gemini API."""
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Load images
        images = []
        for p in frame_paths:
            img = PIL.Image.open(p)
            images.append(img)
            
        # Construct Prompt
        try:
            from .prompts import DETECTOR_SYSTEM_PROMPT
            prompt = DETECTOR_SYSTEM_PROMPT
        except ImportError:
            prompt = "Analyze these video frames. Is this video REAL or FAKE? Return JSON with verdict ('REAL' or 'FAKE'), confidence (0-1), and reasoning."

        # Send to API with Retry Logic
        return self._retry_with_backoff(
            lambda: model.generate_content([prompt, *images]),
            max_retries=3
        )

    def _retry_with_backoff(self, func, max_retries=3):
        """Helper to retry a function on 429 errors with exponential backoff."""
        attempt = 0
        while attempt <= max_retries:
            try:
                response = func()
                return self._parse_gemini_response(response)
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "quota" in error_msg or "resource exhausted" in error_msg:
                    attempt += 1
                    if attempt > max_retries:
                        raise e
                    
                    # Exponential backoff: 2s, 4s, 8s... + jitter
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Quota exceeded. Retrying in {wait_time:.2f}s... (Attempt {attempt}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise e

    def _parse_gemini_response(self, response) -> Dict[str, Any]:
        """Parses the Gemini response object into a dictionary."""
        # Parse Response
        text = response.text
        
        # Clean up code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback parsing
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            
            return {
                "verdict": "UNKNOWN", 
                "confidence": 0, 
                "raw_response": text,
                "reasoning": "Model returned invalid JSON format."
            }
