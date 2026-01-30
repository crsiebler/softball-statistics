# Softball Statistics Tracker

A comprehensive Python application to process softball game results and calculate batting statistics for multiple leagues and teams.

## Features

- Process CSV files with structured naming: `<league>-<team>-<season>-<game>.csv`
- Calculate comprehensive batting statistics (BA, OBP, SLG, OPS, etc.)
- Multi-league and multi-team support
- Excel export with formatted reports
- SQLite database for data persistence (stats.db)
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

### Production Installation

```bash
pip install softball-statistics
```

## Usage

```bash
# Process a game file
softball-stats --file data/input/fray-cyclones-winter-01.csv --output stats.xlsx

# List available leagues
softball-stats --list-leagues

# List teams in a league
softball-stats --list-teams --league "fray"
```

## Development

### Running Tests

```bash
make test
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
├── src/softball_statistics/
│   ├── cli.py                 # Command-line interface
│   ├── models/                # Data models
│   ├── repository/            # Data persistence layer
│   ├── parsers/               # CSV and filename parsers
│   ├── calculators/           # Statistics calculations
│   └── exporters/             # Export functionality
├── tests/                     # Test suite
├── data/                      # Actual gameplay data
│   └── input/                 # Input data directory
│       ├── fray-cyclones-winter-01.csv
│       └── fray-cyclones-winter-01.txt
├── environment.yml            # Conda environment
├── setup.py                   # Package configuration
├── stats.db                   # SQLite database file
├── .gitignore                 # Git ignore rules
└── Makefile                   # Automation scripts
```

## License

MIT License