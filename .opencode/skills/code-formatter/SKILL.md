---
name: code-formatter
description: Applies Black and isort formatting, runs pre-commit hooks for code quality
---

## What I do
- Format Python code with Black formatter
- Sort imports with isort
- Run pre-commit hooks for quality checks
- Validate code style compliance

## When to use me
Use this when formatting code, checking formatting, or running linting checks. This includes before commits, after major changes, or when setting up the development environment.

## Procedure
1. Activate conda environment: `conda activate softball-stats`
2. Format code: `black src/ tests/ setup.py`
3. Sort imports: `isort src/ tests/ setup.py`
4. Run pre-commit checks: `pre-commit run --all-files`
5. Fix any linting issues identified

## Related Guidelines
- Follow code style guidelines from AGENTS.md
- Use Black with 88 character line length
- Apply isort with black profile
- Ensure mandatory pre-commit checks pass
