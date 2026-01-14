from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from llms_orchestration.config.prompts import AGENT_PROMPTS
import logging

logger = logging.getLogger(__name__)

class Agent(ABC):
    """
    Abstract base class for all agents in the orchestration system,
    following the 'Building Block' pattern.
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.system_prompt = AGENT_PROMPTS.get(role, "You are a helpful assistant.")
        self.memory: List[Dict[str, Any]] = []
        self.add_memory(self.system_prompt)

    def perform_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Main entry point for an agent to perform a specific task.
        """
        logger.info(f"[{self.name}] ({self.role}) Starting task: {task}")
        result = self._execute(task, context or {})
        logger.info(f"[{self.name}] Task completed.")
        return result

    @abstractmethod
    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        """
        Internal implementation of the task logic.
        Must be implemented by subclasses.
        """
        pass

    def add_memory(self, content: str):
        self.memory.append({"role": "system", "content": content})
