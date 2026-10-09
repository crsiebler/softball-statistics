# Softball Statistics Tracker

A comprehensive Python application to process softball game results and calculate batting statistics for multiple leagues and teams.

## Features

- Process CSV files with structured naming: `<league>-<team>-<season>-<game>[_<YYYY-MM-DD>].csv`
- Calculate comprehensive batting statistics (BA, OBP, SLG, OPS, etc.)
- Multi-league and multi-team support
- Separate formatted Excel workbooks for each league and season, with historical summaries
- SQLite database for data persistence (`data/output/stats.db`)
- Duplicate upload prevention with user confirmation

## Installation

### Development Setup

```bash
# Clone repository
git clone https://github.com/crsiebler/softball-statistics.git
cd softball-statistics

# Create conda environment
make setup
conda activate softball-stats

# Install in development mode
make install
```

Package metadata, runtime dependencies, and development dependencies are
declared in `pyproject.toml`. The Conda environment installs the project with
its `dev` extra in editable mode.

### Production Installation

```bash
pip install softball-statistics
```

## Usage

```bash
# Process a game file
softball-stats --file data/input/fray-cyclones-wt-01_2026-01-29.csv --output data/output/stats.xlsx

# List available leagues
softball-stats --list-leagues

# List teams in a league
softball-stats --list-teams --league "fray"
```

### League and season workbooks

The CLI stores its database at `data/output/stats.db` by default, creating the
parent directory when needed. Use `--db PATH` to select another location.
Existing root-level databases are not moved or deleted automatically.

`--output` supplies the directory and filename prefix. For example,
`--output data/output/stats.xlsx` generates files such as:

```text
data/output/stats-fray-winter_2026.xlsx
data/output/stats-fray-spring_2026.xlsx
data/output/stats-fray-late_summer_2026.xlsx
data/output/stats-scottsdale-fall_2026.xlsx
```

All games remain in the same SQLite database. Each workbook contains:

- **Legend**: statistic definitions.
- **League Summary**: cumulative team statistics for that league through the
  season's latest recorded game date, shown in the **Through Date** column.
- **Player Summary**: cumulative player statistics for that league through the
  same date, combining matching player names across teams/seasons.
- **Team Total** tabs: cumulative statistics for each team playing that season.
- **Season Total** tabs: statistics from that season only.
- **Game** tabs: one tab per team/game from that season, ordered by date and
  game number, including separate tabs for doubleheaders.

For example, a Spring workbook includes earlier Winter games in cumulative
summaries, but does not include later Summer games or another league's games.
Cutoffs use actual game dates rather than season labels or import order. If
seasons overlap, only games on or before the cutoff contribute to summaries.
An active season's cutoff advances as new games are recorded.

Each export refreshes all league/season workbooks in the database, so backfilled
games are reflected in later cumulative summaries. Existing consolidated
`stats.xlsx` files are not deleted or refreshed. Seasons without games produce
no workbook. Filenames are sanitized; colliding league/season names receive an
ID suffix. Worksheet names are shortened and disambiguated when necessary.

### Season share links

`data/season_links.json` is the tracked registry for Google Sheet share URLs.
Each record has `league`, `season`, `team`, and a nonempty `urls` list. Use the
same names as the application (for example, `Fray`, `Late Summer 2026`, and
`Cyclones`). Name-based records survive database rebuilds; no SQLite IDs or
database migration are involved. Add or update records directly in the JSON file.
Multiple URLs are supported when a season intentionally has several destinations.

```bash
softball-stats --list-season-links --league "Fray" --season "Late Summer 2026" --team "Cyclones"
```

Omit filters to list all saved destinations. Run from the repository root or
pass `--season-links-file /path/to/season_links.json`. Lookup validates the
registry and rejects duplicate identities and invalid Google Sheet URLs.

The post-game recap skill reads this registry and records confirmed links there.
It can upload the complete workbook for a new season with authorization. For
existing seasons, open the recap link and manually replace the shared file from
the generated XLSX. For newly uploaded seasons, manually enable **Anyone with
the link → Viewer**. Saving a URL does not verify freshness or sharing permissions.
The application does not upload files or change Google Drive permissions.

## Development

### Running Tests

```bash
make test
```

### Code Quality

```bash
# Format code
make format

# Check formatting
make check-format

# Run all linting and checks (includes formatting)
make lint

# Install pre-commit hooks (runs automatically on commits)
make pre-commit-install
```

### Running the Application

```bash
# Via console script
make run

# Via python module
make run-module
```

## Project Structure

```
softball-statistics/
├── scripts/                   # Utility scripts
│   ├── generate_test_data.py  # Generate fake test data
│   └── process_test_data.py   # Process test data and export
├── src/softball_statistics/
│   ├── cli.py                 # Command-line interface
│   ├── models/                # Data models
│   ├── repository/            # Data persistence layer
│   ├── parsers/               # CSV and filename parsers
│   ├── calculators/           # Statistics calculations
│   └── exporters/             # Export functionality
├── tests/                     # Test suite
├── data/                      # Actual gameplay data
│   ├── input/                 # Input data directory
│   │   └── fray-cyclones-wt-01_2026-01-29.csv
│   └── output/                # Generated workbooks and stats.db (ignored)
├── environment.yml            # Conda environment
├── pyproject.toml             # Package and dependency configuration
├── .gitignore                 # Git ignore rules
└── Makefile                   # Automation scripts
```

## License

MIT License
