---
name: code-formatter
description: Applies Ruff lint fixes, import sorting, and formatting and runs pre-commit hooks for code quality
---

## What I do
- Format Python code with Ruff
- Sort imports and remove unused imports with Ruff lint fixes
- Run pre-commit hooks for quality checks
- Validate code style compliance

## When to use me
Use this when formatting code, checking formatting, or running linting checks. This includes before commits, after major changes, or when setting up the development environment.

## Procedure
1. Activate conda environment: `conda activate softball-stats`
2. Apply lint fixes and sort imports: `ruff check --fix src/ tests/`
3. Format code: `ruff format src/ tests/`
4. Verify lint and formatting: `make check-format`
5. Run pre-commit checks: `pre-commit run --all-files`
6. Fix any remaining issues identified

## Related Guidelines
- Follow code style guidelines from AGENTS.md
- Use Ruff with the configured 88-character line length
- Keep Ruff import sorting enabled through the `I` lint rules
- Ensure mandatory pre-commit checks pass
