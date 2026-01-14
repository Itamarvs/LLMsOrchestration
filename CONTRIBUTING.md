# Contributing to Deepfake Detection System

Thank you for your interest in contributing to this project!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Itamarvs/LLMsOrchestration.git
   cd LLMsOrchestration
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .[dev]
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Code Style

We use the following tools to maintain code quality:

| Tool | Purpose |
|------|---------|
| **Ruff** | Linting and formatting |
| **MyPy** | Type checking |
| **Bandit** | Security scanning |

Run all checks locally:
```bash
ruff check src/ tests/
mypy src/ --ignore-missing-imports
bandit -r src/
```

## Testing

Run the test suite:
```bash
pytest tests/ --cov=src/deepfake_platform
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit with clear messages
3. Ensure all pre-commit hooks pass
4. Push and create a Pull Request
5. Wait for CI checks to pass

## Commit Message Format

Use clear, descriptive commit messages:
- `feat: Add new detection algorithm`
- `fix: Handle missing API key gracefully`
- `docs: Update README with new examples`
- `test: Add tests for retry logic`
