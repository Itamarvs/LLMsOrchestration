from .base_agent import Agent
from typing import Dict, Any

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(name="SciBot", role="Research & Analysis")

    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        if "analyze" in task.lower():
            return "Sensitivity analysis complete. Parameters optimal."
        return "Research Agent ready."
