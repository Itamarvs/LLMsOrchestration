# System Architecture

## Context Diagram

```mermaid
graph TD
    User((User))
    Orchestrator[LLM Orchestrator System]
    LLM[LLM Provider API]
    
    User -->|Initiates Task| Orchestrator
    Orchestrator -->|Sends Prompts| LLM
    LLM -->|Returns Completions| Orchestrator
    Orchestrator -->|Generates Artifacts| FileSystem[(File System)]
```

## Container Diagram

```mermaid
graph TD
    subgraph "Orchestration Layer"
        Main[Main Entrypoint] -->|Initializes| Agents
    end
    
    subgraph "Agent Layer"
        Agents --> Architect[ArchitectAgent]
        Agents --> Developer[DeveloperAgent]
        Agents --> QA[QAAgent]
        Agents --> Quality[CodeQualityAgent]
        Agents --> Research[ResearchAgent]
        Agents --> Assessor[SelfAssessmentAgent]
    end
    
    subgraph "Infrastructure Layer"
        Utils[Utilities]
        Config[Configuration]
    end
    
    Agents -.->|Uses| Utils
    Agents -.->|Uses| Config
```

## Class Hierarchy

### `Agent` (Base Class)
- **Role**: Abstract base for all specialized agents.
- **Methods**:
  - `perform_task(task: str) -> str`: Public interface.
  - `_execute(task: str, context: Dict) -> str`: Abstract implementation.
  - `_log(message: str)`: Internal logging.

### Specialized Agents
- **`ArchitectAgent`**: Scaffolds project structure.
- **`DeveloperAgent`**: Generates implementation code.
- **`CodeQualityAgent`**: runs static analysis (Ruff/Bandit).
- **`QAAgent`**: Runs unit tests (Pytest).
- **`ResearchAgent`**: Optimizes and analyzes performance.
- **`SelfAssessmentAgent`**: Grades the final output.

## API Documentation
The system currently exposes a CLI entry point:
```bash
python -m llms_orchestration.main
```
This triggers the sequential execution of all agents defined in the `main()` function.
