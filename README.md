# LLMs Orchestration Project

## Overview
This project implements a Multi-Agent System for orchestrating LLM workflows, built as part of the Advanced Agentic Coding course. It is designed to be modular, extensible, and fully automated.

## Structure
The project follows a standard Python package structure:
- `src/`: Source code
    - `agents/`: Agent implementations
    - `utils/`: Helper functions
    - `config/`: Configuration logic
- `tests/`: Unit and integration tests
- `docs/`: Documentation
- `data/`: Input datasets
- `results/`: Experiment outputs
- `notebooks/`: Analysis notebooks

## 🎥 Output Example
We included a sample generated Deepfake in `examples/`.
<video src="examples/deepfake_demo.mp4" controls title="Deepfake Demo"></video>

## Installation

### Prerequisites
- Python 3.9+
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd LLMsOrchestration
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Usage

### Running the Orchestrator
```bash
python -m llms_orchestration.main
```

### Running Tests
```bash
pytest tests/
```

## Configuration
Copy the `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
See `config/` for more advanced settings.

## Troubleshooting
- **ModuleNotFoundError**: Ensure you have installed the package in editable mode (`pip install -e .`).
- **API Errors**: Check that your `.env` file contains valid keys.

## Credits
Course Instructions by Dr. Yoram Segal.
