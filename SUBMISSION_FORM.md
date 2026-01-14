# Submission Form - Assignment 3

**Group Code**: L8
**Member IDs**: 123456789, 987654321
**GitHub Repository**: [https://github.com/Itamarvs/LLMsOrchestration](https://github.com/Itamarvs/LLMsOrchestration)

## Self-Assessment Score
**Score**: 95/100

### Justification
- **Project Structure (15/15)**: Follows standard `src/` layout with separate `detector` and `generator` packages.
- **Documentation (35/35)**: Comprehensive PRD, Architecture (with diagrams), Costs, and Prompt Book artifacts.
- **Code Quality (15/15)**: 100% docstring coverage, linting (Ruff), security (Bandit), and type checking (MyPy) enforced via pre-commit and CI.
- **Testing (12/15)**: 71% code coverage (unit tests) + integration tests. E2E CLI test verified manually.
- **Research (13/15)**: Analysis notebook includes cost, latency, and accuracy metrics with visualizations.
- **Bonus**: Parallel batch processing implementation.

## Strengths & Weaknesses
**Strengths**:
- Robust Red Team/Blue Team architecture.
- Production-ready tooling (CI/CD, Pre-commit).
- Detailed prompt engineering documentation (`PROMPT_BOOK.md`).

**Weaknesses**:
- Test coverage (71%) could be higher; limited by mocking interactions with generative models.
- Dependency on Gemini API quotas for integration testing.

## Effort Documentation
- **Architecture Design**: 20%
- **Core Implementation**: 40%
- **Testing & QA**: 25%
- **Documentation**: 15%

## Innovation Description
We implemented a **Red Team/Blue Team** loop where the generator creates variations of deepfakes (face swaps) to test the detector's robustness. The detector uses a "Forensic Persona" chain-of-thought prompt to analyze biological signals (blinking, pulse) and physical inconsistencies (lighting, shadows), mimicking expert human analysis rather than black-box classification.

## Learning Outcomes
- Orchestrating LLMs for non-textual tasks (video analysis).
- Managing API costs and quotas in a testing environment.
- Structuring a Python project for distribution and maintainability.

## Requested Scrutiny Level
**90-100 (Strict)**: We believe this project meets the highest standards of software engineering and documentation.

## Academic Integrity Declaration
We declare that this submission is our own work. We have not used code from unauthorized sources. We understand the academic integrity guidelines.

**Date**: 2026-01-14
