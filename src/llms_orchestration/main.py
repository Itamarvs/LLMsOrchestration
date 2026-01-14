import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from llms_orchestration.agents.developer import DeveloperAgent
from llms_orchestration.agents.architect import ArchitectAgent
from llms_orchestration.agents.code_quality import CodeQualityAgent
from llms_orchestration.agents.qa import QAAgent
from llms_orchestration.agents.research import ResearchAgent
from llms_orchestration.agents.self_assessment import SelfAssessmentAgent
from llms_orchestration.config import settings
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("--- Starting Multi-Agent Orchestration System ---")
    
    # Initialize Core Agents
    architect = ArchitectAgent()
    dev = DeveloperAgent()
    quality = CodeQualityAgent()
    qa = QAAgent()
    research = ResearchAgent()
    grader = SelfAssessmentAgent()

    logger.info("[Orchestrator] Initializing Project...")
    architect.perform_task("Scaffold project structure")

    logger.info("[Orchestrator] Starting Development Cycle...")
    # Step 1: Develop
    code = dev.perform_task("Generate Hello World feature with UI considerations")
    
    # Simulate writing file
    # Ensure directory exists or write to a specific location if needed
    # For now, keeping original logic but noting potential issue if running from elsewhere
    try:
        with open("generated_hello.py", "w") as f:
            f.write(code)
    except IOError as e:
        logger.error(f"Failed to write generated_hello.py: {e}")

    # Step 2: Quality Check
    quality.perform_task("Check generated_hello.py for secrets and standards")

    # Step 3: Test
    qa.perform_task("Run unit tests for Hello World")

    # Step 4: Research/Optimization
    research.perform_task("Analyze performance sensitivity")

    logger.info("[Orchestrator] Finalizing Submission...")
    # Step 5: Assessment
    report = grader.perform_task("Assess project against Dr. Segal's criteria")
    
    logger.info("--- Final Assessment Report ---")
    logger.info("\n" + report)
    logger.info("[Orchestrator] System Run Complete.")

if __name__ == "__main__":
    main()
