from .base_agent import Agent
from typing import Dict, Any

class DeveloperAgent(Agent):
    """
    Agent responsible for writing code and implementing features.
    """
    def __init__(self):
        super().__init__(name="DevBot", role="Developer")

    def _execute(self, task: str, context: Dict[str, Any]) -> str:
        # Mocking the LLM generation for the "Hello World" scenario
        if "hello world" in task.lower():
            return self._generate_hello_world()
        
        return f"Developer Agent received task: {task}. (LLM logic not connected yet)"

    def _generate_hello_world(self) -> str:
        code = """
def hello_world():
    print("Hello, World!")
    return "Hello, World!"

if __name__ == "__main__":
    hello_world()
"""
        return code
