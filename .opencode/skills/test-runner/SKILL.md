---
name: test-runner
description: Executes tests, analyzes coverage, and debugs test failures in the softball-statistics repository
---

## What I do
- Run test suites with coverage analysis
- Debug failing tests and analyze error messages
- Generate coverage reports for code quality assessment

## When to use me
Use this when you need to execute tests, check coverage, or troubleshoot test failures. This includes running all tests, single test methods, or debugging specific test issues.

## Procedure
1. Activate conda environment: `conda activate softball-stats`
2. Run tests with coverage: `pytest tests/ -v --cov=src --cov-report=html`
3. Analyze coverage report in htmlcov/ directory
4. Debug failures by examining error messages and test fixtures
5. Fix implementation issues identified by tests

## Related Guidelines
- Follow testing standards from AGENTS.md
- Use fixtures for test data setup
- Ensure pre-commit checks pass before commits
