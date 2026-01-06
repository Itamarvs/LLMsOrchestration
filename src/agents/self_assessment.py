from .base_agent import Agent
from typing import Dict, Any
import os

class SelfAssessmentAgent(Agent):
    """
    Agent responsible for grading the project based on the course guide.
    """
    def __init__(self):
        super().__init__(name="Grader", role="Self-Assessment")

    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        if "assess" in task.lower():
            return self._perform_assessment()
        return "Grader waiting for assessment task."

    def _perform_assessment(self) -> str:
        score = 0
        report = []

        # Criteria 3.2, 4.2: Project Structure (15%)
        if os.path.exists("src") and os.path.exists("tests"):
             score += 15
             report.append("[x] Project Structure (15/15)")
        else:
             report.append("[ ] Project Structure (0/15) - Missing src/ or tests/")

        # Criteria 4.1: Documentation (20%)
        if os.path.exists("README.md"):
            score += 20
            report.append("[x] Documentation (20/20) - README exists")
        else:
            report.append("[ ] Documentation (0/20)")

        # Simplified Logic for other criteria
        report.append(f"Total Score: {score}/35 (Partial Check)")
        
        return "\n".join(report)
