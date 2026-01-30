# Softball Statistics Generator

## Architecture Core
- **Dependency Injection**: Decouple components via interfaces (e.g., repository injection in CLI)
- **Repository Pattern**: Abstract data access (SQLiteRepository implements base interfaces)
  - Domain Logic: Business logic isolated in `calculators/`, data access in `repository/`

## System Structure
- **Clean Architecture**: Entities → Use Cases → Adapters → Frameworks
  - Hexagonal: Core domain independent of external concerns (parsers, exporters)

## Design Patterns
- **Strategy Pattern**: Interchangeable logic (e.g., parser implementations)
  - When: Multiple algorithms for same interface
  - Code: `class Parser(ABC): @abstractmethod def parse(self, data): pass`
- **CQRS**: Separate read/write operations (query stats vs. save games)
  - When: Different read/write requirements
  - Code: `class Repository: def get_stats(self): pass; def save_game(self): pass`
- **Factory Pattern**: Object creation (e.g., model factories)
  - When: Complex object instantiation
  - Code: `@staticmethod def create_player(data): return Player(**data)`

## Agentic Workflow
- **Plan-Then-Execute**: State intent before changes (e.g., "Planning to add new calculator method")
- **ReAct Loop**: Reason current state → Act with changes → Repeat
  - Generic examples: Debug failing test → Analyze error → Fix implementation → Re-run

## Technical Constraints - Boundaries
- **Never Touch**: `data/` folder (only Python app writes to `data/output`)
- **Preferred Tools**: conda, pytest
- **Mandatory Pre-commit**: `make lint && make test`

## Testing Standards
- No mocking - use fixtures for test data
- Repository Pattern, TDD, high coverage (`pytest --cov`)
- Short methods, dependency injection for DB/services
  - Domain Logic: Tests in `tests/`, fixtures for repository setup

## Git Workflow
- Branches: `<type>/<description>` (feat/, fix/, refactor/, chore/, docs/)
- Commits: Conventional format (`feat: add login button`)
- PRs: Create for human review, don't merge

## Build/Lint/Test Commands
- Test all: `make test` (pytest with coverage)
- Test single: `pytest tests/test_file.py::TestClass::test_method -v`
- Format: `make format` (Black + isort)
- Lint: `make lint` (pre-commit)

## Code Style Guidelines
- Black (88 chars), isort (black profile)
- Type hints, dataclasses, docstrings
- Snake_case naming, custom exceptions
