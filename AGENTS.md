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
- **Generated Output**: `data/output/` contains only application-generated SQLite databases and Excel spreadsheets. Only the Python application writes these outputs; do not hand-edit them or place source/review files there.
- **Game Inputs**: `data/input/` contains only CSV game logs with player statistics. The `transcribe-score-sheets` skill may generate confirmed, parser-validated CSV logs there. Keep photographs, review notes, and other work-in-progress artifacts out of this directory.
- **Game-Log Workspace**: `data/game-log/` is the work-in-progress area for source photographs, transcription drafts, and game-specific review notes. Existing files may be modified only if they were created within the current working session. Preserve files from earlier sessions; create a uniquely named new artifact instead of overwriting, renaming, or deleting them.
- **Preferred Tools**: conda, pytest
- **Environment Activation**: Always activate conda environment with `conda activate softball-stats` before testing or running the application
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
- Format: `make format` (Ruff lint fixes, import sorting, and formatting)
- Lint: `make lint` (pre-commit)

## Code Style Guidelines
- Ruff formatting with an 88-character line length and Ruff import sorting
- Type hints, dataclasses, docstrings
- Snake_case naming, custom exceptions
