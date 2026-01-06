---
description: Commit changes to Git on milestone completion
---

# Commit Workflow

This rule ensures that work is safely checkpointed after every major task or milestone.

1.  **Check Status**: Run `git status` to see what has changed.
2.  **Add Changes**: Run `git add .` (or specific files if needed).
3.  **Commit**: Run `git commit -m "type: Description of change"`
    - Use conventional commit types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.
4.  **Push**: Run `git push` to sync with the remote repository.
5.  **Verify**: Ensure the commit and push were successful.

**When to Run**:
- After completing a task in `task.md`.
- After a successful verification run.
- Before switching to a new major task.
