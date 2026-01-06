import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.agents.developer import DeveloperAgent
from src.agents.architect import ArchitectAgent
from src.agents.code_quality import CodeQualityAgent
from src.agents.qa import QAAgent
from src.agents.research import ResearchAgent
from src.agents.self_assessment import SelfAssessmentAgent

def main():
    print("--- Starting Multi-Agent Orchestration System ---")
    
    # Initialize Core Agents
    architect = ArchitectAgent()
    dev = DeveloperAgent()
    quality = CodeQualityAgent()
    qa = QAAgent()
    research = ResearchAgent()
    grader = SelfAssessmentAgent()

    print("\n[Orchestrator] Initializing Project...")
    architect.perform_task("Scaffold project structure")

    print("\n[Orchestrator] Starting Development Cycle...")
    # Step 1: Develop
    code = dev.perform_task("Generate Hello World feature with UI considerations")
    
    # Simulate writing file
    with open("src/hello.py", "w") as f:
        f.write(code)

    # Step 2: Quality Check
    quality.perform_task("Check src/hello.py for secrets and standards")

    # Step 3: Test
    qa.perform_task("Run unit tests for Hello World")

    # Step 4: Research/Optimization
    research.perform_task("Analyze performance sensitivity")

    print("\n[Orchestrator] Finalizing Submission...")
    # Step 5: Assessment
    report = grader.perform_task("Assess project against Dr. Segal's criteria")
    
    print("\n--- Final Assessment Report ---")
    print(report)
    print("\n[Orchestrator] System Run Complete.")

if __name__ == "__main__":
    main()
