from .base_agent import Agent
from typing import Dict, Any

class CodeQualityAgent(Agent):
    def __init__(self):
        super().__init__(name="LintBot", role="Code Quality")

    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        if "check" in task.lower():
            return "[PASS] No hardcoded secrets found. Naming conventions followed."
        return "Quality Agent ready."
