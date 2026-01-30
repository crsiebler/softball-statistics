"""
Command-line interface for softball statistics.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from softball_statistics.exporters.excel_exporter import ExcelExporter, ExcelExportError
from softball_statistics.interfaces import (
    CommandRepository,
    Exporter,
    Parser,
    QueryRepository,
)
from softball_statistics.parsers.csv_parser import CSVParseError, CSVParser
from softball_statistics.use_cases import (
    CalculateStatsUseCase,
    ListLeaguesUseCase,
    ListTeamsUseCase,
    ProcessGameUseCase,
)


class CLI:
    """Command-line interface class."""

    def __init__(
        self,
        command_repo: CommandRepository,
        query_repo: QueryRepository,
        parser: Parser,
        exporter: Exporter,
    ):
        self.command_repo = command_repo
        self.query_repo = query_repo
        self.parser = parser
        self.exporter = exporter
        self.process_game_use_case = ProcessGameUseCase(
            parser, command_repo, query_repo
        )
        self.calculate_stats_use_case = CalculateStatsUseCase(query_repo)
        self.list_leagues_use_case = ListLeaguesUseCase(query_repo)
        self.list_teams_use_case = ListTeamsUseCase(query_repo)

    def run(self, args: Optional[list[str]] = None) -> None:
        """Run the CLI with given arguments."""
        parser = argparse.ArgumentParser(
            description="Softball Statistics Tracker",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  softball-stats --file fray-cyclones-winter-01.csv --output data/output/stats.xlsx
  softball-stats --list-leagues
  softball-stats --list-teams --league "fray"
            """,
        )

        parser.add_argument(
            "--file",
            type=str,
            help="CSV file to process (with format: league-team-season-game.csv)",
        )

        parser.add_argument(
            "--output",
            type=str,
            default="data/output/stats.xlsx",
            help="Output Excel file path (default: data/output/stats.xlsx)",
        )

        parser.add_argument(
            "--list-leagues",
            action="store_true",
            help="List all leagues in the database",
        )

        parser.add_argument(
            "--list-teams", action="store_true", help="List teams (requires --league)"
        )

        parser.add_argument("--league", type=str, help="League name for --list-teams")

        args_parsed = parser.parse_args(args)

        try:
            if args_parsed.list_leagues:
                self._list_leagues()
            elif args_parsed.list_teams:
                if not args_parsed.league:
                    print("Error: --league is required with --list-teams")
                    sys.exit(1)
                self._list_teams(args_parsed.league)
            elif args_parsed.file:
                self._process_file(args_parsed.file, args_parsed.output)
            else:
                parser.print_help()
                sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def _list_leagues(self) -> None:
        """List all leagues."""
        leagues = self.list_leagues_use_case.execute()
        if not leagues:
            print("No leagues found.")
            return

        print("Leagues:")
        for league in leagues:
            print(f"  - {league.name} ({league.season})")

    def _list_teams(self, league_name: str) -> None:
        """List teams in a league."""
        try:
            teams = self.list_teams_use_case.execute(league_name)
        except ValueError as e:
            print(f"Error: {e}")
            return

        if not teams:
            print(f"No teams found in league '{league_name}'.")
            return

        print(f"Teams in {league_name}:")
        for team in teams:
            print(f"  - {team.name}")

    def _process_file(self, file_path: str, output_path: str) -> None:
        """Process a CSV file."""
        try:
            # Process the file using use case
            print(f"Parsing {file_path}...")
            parsed_data = self.process_game_use_case.execute(
                file_path, replace_existing=False
            )

            # Calculate stats
            metadata = parsed_data["metadata"]
            stats_data = self.calculate_stats_use_case.execute(
                metadata["league"], metadata["team"], metadata["season"]
            )

            # Export to Excel
            print(f"Exporting to {output_path}...")
            self.exporter.export(stats_data, output_path)
            print(f"Success! Statistics exported to {output_path}")

            # Display parsing warnings if any
            warnings = parsed_data.get("warnings", [])
            if warnings:
                print(f"\n⚠️  Parsing Warnings ({len(warnings)}):")
                for warning in warnings:
                    location = ""
                    if (
                        warning["row_num"]
                        and warning["col_num"]
                        and warning["filename"]
                    ):
                        location = f" (row {warning['row_num']}, column {warning['col_num']} in {warning['filename']})"
                    elif warning["filename"]:
                        location = f" (in {warning['filename']})"

                    print(
                        f"  - Player '{warning['player_name']}': {warning['assumption']}{location}"
                    )
                    print(f"    Original: '{warning['original_attempt']}'")

        except ValueError as e:
            # Game exists, ask to replace
            if "already exists" in str(e):
                # Parse filename to get metadata for prompt
                from softball_statistics.parsers.filename_parser import parse_filename

                metadata = parse_filename(Path(file_path).name)
                response = input(
                    f"Game {metadata['league']}-{metadata['team']}-{metadata['season']}-{metadata['game']} already exists. Replace? (y/N): "
                )
                if response.lower() in ["y", "yes"]:
                    print("Replacing existing game data...")
                    parsed_data = self.process_game_use_case.execute(
                        file_path, replace_existing=True
                    )
                    # Continue with stats and export
                    stats_data = self.calculate_stats_use_case.execute(
                        metadata["league"], metadata["team"], metadata["season"]
                    )
                    print(f"Exporting to {output_path}...")
                    self.exporter.export(stats_data, output_path)
                    print(f"Success! Statistics exported to {output_path}")
                else:
                    print("Operation cancelled.")
            else:
                print(f"Processing failed: {e}")
                sys.exit(1)
        except (CSVParseError, ExcelExportError) as e:
            print(f"Processing failed: {e}")
            sys.exit(1)


def main():
    """Main CLI entry point."""
    # TODO: Use DI container or factory to inject dependencies
    # For now, hardcoded for transition
    from softball_statistics.repository.sqlite import (
        SQLiteCommandRepository,
        SQLiteQueryRepository,
    )

    db_path = "softball_stats.db"
    command_repo = SQLiteCommandRepository(db_path)
    query_repo = SQLiteQueryRepository(db_path)
    parser = CSVParser()
    exporter = ExcelExporter()

    cli = CLI(command_repo, query_repo, parser, exporter)
    cli.run()


if __name__ == "__main__":
    main()
