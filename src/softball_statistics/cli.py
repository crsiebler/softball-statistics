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
    ValidationError,
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
  softball-stats --list-teams --league "Fray"
  softball-stats --reparse-all
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

        parser.add_argument(
            "--reparse-all",
            action="store_true",
            help="Wipe database and reparse all CSV files in data/input/",
        )

        parser.add_argument(
            "--replace-existing",
            action="store_true",
            help="Replace existing games without prompting",
        )

        parser.add_argument(
            "--force",
            action="store_true",
            help="Skip confirmation prompts",
        )

        args_parsed = parser.parse_args(args)

        try:
            if args_parsed.list_leagues:
                self._list_leagues()
            elif args_parsed.list_teams:
                if not args_parsed.league:
                    print("Error: --league is required with --list-teams")
                    sys.exit(1)
                self._list_teams(args_parsed.league)
            elif args_parsed.reparse_all:
                self._reparse_all(args_parsed)
            elif args_parsed.file:
                self._process_file(
                    args_parsed.file, args_parsed.output, args_parsed.replace_existing
                )
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

    def _reparse_all(self, args) -> None:
        """Wipe database and reparse all CSV files in data/input/."""
        from pathlib import Path

        print("⚠️  This will wipe the database and reparse all files in data/input/")
        if not args.force:
            response = input("Continue? (y/N): ")
            if response.lower() not in ["y", "yes"]:
                print("Operation cancelled.")
                return

        print("Wiping database...")
        # Clear all data

        sqlite_repo = self.command_repo  # type: ignore
        with sqlite_repo._get_connection() as conn:  # type: ignore
            cursor = conn.cursor()
            # Delete in reverse dependency order
            cursor.execute("DELETE FROM parsing_warnings")
            cursor.execute("DELETE FROM plate_appearances")
            cursor.execute("DELETE FROM games")
            cursor.execute("DELETE FROM players")
            cursor.execute("DELETE FROM weeks")
            cursor.execute("DELETE FROM teams")
            cursor.execute("DELETE FROM leagues")
            conn.commit()

        # Find all CSV files in data/input/
        input_dir = Path("data/input")
        if not input_dir.exists():
            print(f"Error: {input_dir} directory not found")
            return

        csv_files = list(input_dir.glob("*.csv"))
        if not csv_files:
            print(f"No CSV files found in {input_dir}")
            return

        print(f"Found {len(csv_files)} CSV files to process...")

        from softball_statistics.parsers.filename_parser import parse_filename

        success_count = 0
        error_count = 0

        for csv_file in csv_files:
            try:
                print(f"Processing {csv_file.name}...")
                self.process_game_use_case.execute(
                    str(csv_file), replace_existing=False
                )
                success_count += 1
            except Exception as e:
                print(f"Error processing {csv_file.name}: {e}")
                error_count += 1

        print(f"\nReparsing complete: {success_count} successful, {error_count} errors")
        if success_count > 0:
            print("Database has been rebuilt with formatted team/league names.")
            # Export stats if output path provided
            if hasattr(args, "output") and args.output:
                # Get metadata from the last processed file
                last_file = csv_files[-1]
                metadata = parse_filename(last_file.name)
                assert metadata["league"] is not None
                assert metadata["team"] is not None
                assert metadata["season"] is not None
                stats_data = self.calculate_stats_use_case.execute(
                    metadata["league"], metadata["team"], metadata["season"]
                )
                self.exporter.export(stats_data, args.output)
                print(f"Success! Statistics exported to {args.output}")

    def _process_file(
        self, file_path: str, output_path: str, replace_existing: bool
    ) -> None:
        """Process a CSV file."""
        try:
            # Process the file using use case
            print(f"Parsing {file_path}...")
            parsed_data = self.process_game_use_case.execute(
                file_path, replace_existing=replace_existing
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

        except ValidationError as e:
            print(f"Validation Error: {e}")
            sys.exit(1)
        except ValueError as e:
            # Game exists, ask to replace
            if "already exists" in str(e):
                if not replace_existing:
                    # Parse filename to get metadata for prompt
                    from softball_statistics.parsers.filename_parser import (
                        parse_filename,
                    )

                    metadata = parse_filename(Path(file_path).name)
                    assert metadata["league"] is not None
                    assert metadata["team"] is not None
                    assert metadata["season"] is not None
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
                    # Should not reach here if replace_existing=True
                    print(f"Processing failed: {e}")
                    sys.exit(1)
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
    from softball_statistics.repository.sqlite import SQLiteRepository

    db_path = "stats.db"
    repo = SQLiteRepository(db_path)  # type: ignore
    parser = CSVParser()
    exporter = ExcelExporter(repo)

    cli = CLI(repo, repo, parser, exporter)
    cli.run()


if __name__ == "__main__":
    main()
