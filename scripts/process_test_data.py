#!/usr/bin/env python3
"""
Process test data CSVs and generate comprehensive Excel export.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from softball_statistics.exporters.excel_exporter import ExcelExporter
from softball_statistics.repository.sqlite import SQLiteRepository
from softball_statistics.use_cases import CalculateStatsUseCase, ProcessGameUseCase


def main():
    # Setup repository
    repo = SQLiteRepository("data/test/test.db")  # File-based for testing

    # Setup use case
    calculator = CalculateStatsUseCase(repo)
    exporter = ExcelExporter(repo)

    # Setup process game use case
    from softball_statistics.parsers.csv_parser import CSVParser

    parser = CSVParser()
    process_use_case = ProcessGameUseCase(parser, repo, repo)

    # Process all CSV files
    input_dir = Path("data/test/input")
    csv_files = sorted(input_dir.glob("*.csv"))

    print(f"Found {len(csv_files)} CSV files to process")

    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        try:
            # Process the game file
            process_use_case.execute(str(csv_file))

            print(f"✓ Processed {csv_file.name}")
        except Exception as e:
            print(f"✗ Error processing {csv_file.name}: {e}")
            continue

    # Generate comprehensive export
    output_path = "data/test/test.xlsx"
    print(f"Generating Excel export to {output_path}...")

    try:
        # Get all teams
        leagues = repo.list_leagues()
        all_teams = []
        for league in leagues:
            teams = repo.list_teams_by_league(league.id)
            all_teams.extend(teams)

        team_stats = {}

        for team in all_teams:
            # Get cumulative stats for each team
            cumulative_stats = calculator.get_cumulative_team_stats(team.name)
            team_stats[team.name] = cumulative_stats

        stats_data = {"team_stats": team_stats}

        # Export to Excel
        exporter.export(stats_data, output_path, use_case=calculator)
        print(f"✓ Export completed: {output_path}")

    except Exception as e:
        print(f"✗ Error during export: {e}")
        import traceback

        traceback.print_exc()

    return 0


if __name__ == "__main__":
    sys.exit(main())
