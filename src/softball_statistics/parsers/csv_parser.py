"""
CSV parser for softball game data.
"""

import csv
import logging
from pathlib import Path
from typing import Any, Dict, List

from softball_statistics.models import AtBatAttempt, Game, League, Player, Team, Week
from softball_statistics.models.factories import (
    LeagueFactory,
    PlayerFactory,
    TeamFactory,
)
from softball_statistics.parsers.attempt_parser import AttemptParseError, parse_attempt
from softball_statistics.parsers.base import Parser
from softball_statistics.parsers.filename_parser import (
    FilenameParseError,
    parse_filename,
)

logger = logging.getLogger(__name__)


class CSVParseError(Exception):
    """Raised when CSV parsing fails."""

    pass


class CSVParser(Parser):
    """CSV parser implementing Parser interface."""

    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse a CSV file."""
        return parse_csv_file(file_path)


def parse_csv_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a CSV file and extract all game data.

    Args:
        file_path: Path to the CSV file

    Returns:
        Dictionary containing parsed metadata and attempts

    Raises:
        CSVParseError: If parsing fails
        FilenameParseError: If filename is invalid
    """
    path = Path(file_path)
    if not path.exists():
        raise CSVParseError(f"File not found: {file_path}")

    # Parse filename for metadata
    try:
        metadata = parse_filename(path.name)
    except FilenameParseError as e:
        raise CSVParseError(f"Invalid filename format: {e}")

    # Parse CSV content
    attempts = []
    player_names = set()
    all_warnings = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)

            if not headers or len(headers) < 2:
                raise CSVParseError(
                    "CSV must have at least 2 columns (Player Name + attempts)"
                )

            if headers[0].strip().lower() != "player name":
                raise CSVParseError("First column must be 'Player Name'")

            # Process each row
            for row_num, row in enumerate(reader, start=2):
                if not row or not row[0].strip():
                    continue  # Skip empty rows

                player_name = row[0].strip()
                player_names.add(player_name)

                # Process each attempt column
                for col_num, attempt_str in enumerate(row[1:], start=2):
                    attempt_str = attempt_str.strip()
                    if not attempt_str:
                        continue  # Skip empty attempts

                    try:
                        parsed_attempt = parse_attempt(
                            attempt_str,
                            player_name=player_name,
                            row_num=row_num,
                            col_num=col_num,
                            filename=path.name,
                        )
                        attempts.append(
                            {
                                "player_name": player_name,
                                "outcome": attempt_str,
                                "bases": parsed_attempt["bases"],
                                "rbis": parsed_attempt["rbis"],
                                "runs_scored": parsed_attempt["runs_scored"],
                                "attempt_number": col_num
                                - 1,  # Column index starting from 0
                                "row_num": row_num,
                                "col_num": col_num,
                            }
                        )
                        # Collect warnings
                        all_warnings.extend(parsed_attempt["warnings"])
                    except AttemptParseError as e:
                        raise CSVParseError(
                            f"Invalid attempt '{attempt_str}' for {player_name} "
                            f"at row {row_num}, column {col_num}: {e}"
                        )

    except (IOError, UnicodeDecodeError) as e:
        raise CSVParseError(f"Error reading file: {e}")

    if not attempts:
        raise CSVParseError("No valid attempts found in CSV")

    return {
        "metadata": metadata,
        "player_names": sorted(list(player_names)),
        "attempts": attempts,
        "total_attempts": len(attempts),
        "warnings": all_warnings,
    }


def create_database_objects(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create database model objects from parsed CSV data.

    Args:
        parsed_data: Result from parse_csv_file()

    Returns:
        Dictionary with lists of objects to save
    """
    metadata = parsed_data["metadata"]
    attempts = parsed_data["attempts"]

    # Create league
    league = LeagueFactory.create_league(
        {
            "name": metadata["league"],
            "season": metadata["season"],
        }
    )

    # Create team
    team = TeamFactory.create_team(
        {
            "league_id": None,  # Will be set after league is saved
            "name": metadata["team"],
        }
    )

    # Create week (simplified - just create one week for now)
    # In a real implementation, you'd want proper week management
    from datetime import date

    week = Week(
        id=None,
        league_id=None,  # Will be set after league is saved
        week_number=int(
            metadata["game"]
        ),  # Use game number as week number for simplicity
        start_date=date.today(),  # Placeholder
        end_date=date.today(),  # Placeholder
    )

    # Create game
    game_date = date.today()
    if metadata.get("date"):
        try:
            game_date = date.fromisoformat(metadata["date"])
        except ValueError:
            # If date parsing fails, fall back to today
            game_date = date.today()

    game = Game(
        id=None,
        week_id=None,  # Will be set after week is saved
        team_id=None,  # Will be set after team is saved
        date=game_date,
        opponent_team_id=None,
        game_number=int(metadata["game"]),
    )

    # Create players (we'll create them as we encounter them)
    players = {}
    at_bat_attempts = []

    for attempt_data in attempts:
        player_name = attempt_data["player_name"]

        if player_name not in players:
            players[player_name] = PlayerFactory.create_player(
                {
                    "team_id": None,  # Will be set after team is saved
                    "name": player_name,
                }
            )

        # Create at-bat attempt
        at_bat = {
            "player_name": player_name,
            "outcome": attempt_data["outcome"],
            "bases": attempt_data["bases"],
            "rbis": attempt_data["rbis"],
            "runs_scored": attempt_data["runs_scored"],
            "attempt_number": attempt_data["attempt_number"],
        }
        at_bat_attempts.append(at_bat)

    return {
        "league": league,
        "team": team,
        "week": week,
        "game": game,
        "players": list(players.values()),
        "attempts": at_bat_attempts,
    }
