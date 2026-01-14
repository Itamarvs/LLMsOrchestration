# LLM Orchestration System

A multi-agent system designed to orchestrate Large Language Models for software development tasks. This project demonstrates a pipeline where specialized agents (Architect, Developer, QA, etc.) collaborate to build, test, and assess software artifacts.

## Features
- **Multi-Agent Architecture**: Specialized roles for distinct phases of development.
- **Automated Workflow**: From scaffolding to implementation and verification.
- **Quality Gates**: Integrated security and linting checks.
- **Self-Assessment**: Built-in capability to grade its own output.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd LLMsOrchestration
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .[dev]
   ```

4. **Environment Configuration**:
   Copy `.env.example` to `.env` and configure your keys (if applicable):
   ```bash
   cp .env.example .env
   # Edit .env with your favorite editor
   ```

## Usage

Run the main orchestration script:

```bash
python -m llms_orchestration.main
```

### Components
- **Architect**: Sets up the folder structure.
- **Developer**: Writes the actual code (currently mocks a "Hello World").
- **Code Quality**: Checks for secrets and style violations.
- **QA**: Runs test suites.
- **Research**: Analyzes performance.
- **Self-Assessment**: Grades the final result.

## Troubleshooting

- **ModuleNotFoundError**: Ensure you have installed the package with `pip install -e .`.
- **API Limits**: If connecting to real LLMs, ensure your `.env` has valid keys and you are within rate limits.
- **Permission Errors**: Ensure the script has write access to the directory to generate files.

## Project Structure
```
src/
└── llms_orchestration/    # Main package
    ├── agents/            # Specialized agent implementations
    ├── config/            # Configuration settings
    ├── utils/             # Helper functions
    └── main.py            # Entry point
tests/                     # Test suite
docs/                      # Documentation
notebooks/                 # Analysis notebooks
```
