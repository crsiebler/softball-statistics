from typing import Dict, Optional


class FilenameParseError(Exception):
    """Raised when a filename cannot be parsed."""

    pass


def parse_filename(filename: str) -> Dict[str, Optional[str]]:
    """
    Parse a CSV filename with format: <league>-<team>-<season>-<game>[_<date>].csv

    Supports both formats for backward compatibility:
    - Old: league-team-season-game.csv
    - New: league-team-season-game_YYYY-MM-DD.csv

    Args:
        filename: The filename to parse

    Returns:
        Dictionary with keys: 'league', 'team', 'season', 'game', 'date'
        (date will be None for old format or invalid dates)

    Raises:
        FilenameParseError: If filename doesn't match expected format
    """
    if not filename:
        raise FilenameParseError("Filename cannot be empty")

    # Remove .csv extension if present
    if filename.endswith(".csv"):
        filename = filename[:-4]
    else:
        raise FilenameParseError("Filename must have .csv extension")

    # Split by hyphens
    parts = filename.split("-")

    if len(parts) < 4:
        raise FilenameParseError(
            f"Filename must have at least 4 parts separated by hyphens. Found {len(parts)} parts in '{filename}'"
        )

    league, team, season = parts[0], parts[1], parts[2]

    # The remaining parts after season could be "game" or "game_YYYY-MM-DD"
    remaining = "-".join(parts[3:])

    game = remaining
    date = None

    # Check if the remaining part contains an underscore (new format)
    if "_" in remaining:
        game_date_parts = remaining.split("_", 1)
        if len(game_date_parts) == 2:
            game = game_date_parts[0]
            date_candidate = game_date_parts[1]
            # Basic validation of date format (YYYY-MM-DD)
            if len(date_candidate) == 10 and date_candidate.count("-") == 2:
                date = date_candidate
            else:
                raise FilenameParseError(
                    f"Invalid date format '{date_candidate}'. Expected YYYY-MM-DD"
                )
        else:
            raise FilenameParseError(f"Invalid game_date format in '{remaining}'")

    # Validate that required parts are non-empty
    if not all([league, team, season, game]):
        raise FilenameParseError(
            "All filename parts (league, team, season, game) must be non-empty"
        )

    # Validate game number format (should be numeric, can have leading zeros)
    if not game.isdigit():
        raise FilenameParseError(f"Game number must be numeric, found '{game}'")

    return {
        "league": league,
        "team": team,
        "season": season,
        "game": game,
        "date": date,
    }
