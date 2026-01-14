import pytest
from llms_orchestration.agents.developer import DeveloperAgent
from llms_orchestration.agents.architect import ArchitectAgent
from llms_orchestration.agents.code_quality import CodeQualityAgent
from llms_orchestration.agents.qa import QAAgent
from llms_orchestration.agents.self_assessment import SelfAssessmentAgent
from llms_orchestration.main import main
import os

@pytest.fixture
def developer_agent():
    return DeveloperAgent()

@pytest.fixture
def architect_agent():
    return ArchitectAgent()

def test_developer_hello_world(developer_agent):
    """Test that developer agent generates expected hello world code."""
    task = "Generate Hello World feature"
    result = developer_agent.perform_task(task)
    assert "def hello_world():" in result
    assert "print(\"Hello, World!\")" in result

def test_architect_scaffold(architect_agent):
    """Test that architect agent acknowledges scaffold task."""
    task = "Scaffold project structure"
    result = architect_agent.perform_task(task)
    assert "scaffolded" in result or "Simulated" in result

def test_full_flow_dry_run(capsys):
    """Test the main entry point runs without error."""
    # We allow it to run. It writes to 'generated_hello.py'.
    # We should clean it up after.
    try:
        main()
    except SystemExit:
        pass
    
    # Check output
    captured = capsys.readouterr()
    # Note: We switched to logging, so standard output might be empty or contain logs if configured to stream to stdout.
    # But logging usually goes to stderr by default or configured stream. 
    # Our settings.py configures basicConfig, which defaults to stderr.
    # capsys captures stdout and stderr.
    
    # Check if generated file exists
    assert os.path.exists("generated_hello.py")
    
    # Clean up
    if os.path.exists("generated_hello.py"):
        os.remove("generated_hello.py")

def test_code_quality_agent():
    agent = CodeQualityAgent()
    result = agent.perform_task("Check generated code")
    assert "[PASS]" in result

def test_qa_agent():
    agent = QAAgent()
    result = agent.perform_task("Run unit tests")
    assert "10/10 tests passed" in result

def test_self_assessment():
    agent = SelfAssessmentAgent()
    # Mocking os.path.exists to ensure it finds src and tests
    # But since we are running in the repo, they should exist.
    result = agent.perform_task("Assess project")
    assert "Project Structure" in result
    assert "Total Score" in result

from unittest.mock import patch, MagicMock
from llms_orchestration.agents.research import ResearchAgent

def test_research_agent_deepfake_mock():
    agent = ResearchAgent()
    
    # Mock extract_frames and _analyze_with_gemini
    with patch("llms_orchestration.agents.research.extract_frames") as mock_extract:
        with patch.object(agent, "_analyze_with_gemini") as mock_analyze:
            with patch("os.path.exists") as mock_exists:
                with patch("os.getenv") as mock_getenv:
                    # Setup mocks
                    mock_exists.return_value = True
                    mock_getenv.return_value = "fake_key"
                    mock_extract.return_value = ["frame1.jpg"]
                    mock_analyze.return_value = {"verdict": "FAKE", "confidence": 0.9}
                    
                    # Test
                    context = {"video_path": "dummy.mp4"}
                    result = agent.perform_task("Analyze video for deepfake", context)
                    
                    assert "FAKE" in result
                    assert "0.9" in result

def test_research_agent_missing_video():
    agent = ResearchAgent()
    context = {}
    result = agent.perform_task("Analyze video", context)
    assert "Error" in result
