import re
from typing import Dict


class FilenameParseError(Exception):
    """Raised when a filename cannot be parsed."""

    pass


def parse_filename(filename: str) -> Dict[str, str]:
    """
    Parse a CSV filename with format: <league>-<team>-<season>-<game>.csv

    Args:
        filename: The filename to parse (e.g., "fray-cyclones-winter-01.csv")

    Returns:
        Dictionary with keys: 'league', 'team', 'season', 'game'

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

    if len(parts) != 4:
        raise FilenameParseError(
            f"Filename must have exactly 4 parts separated by hyphens: "
            f"<league>-<team>-<season>-<game>. Found {len(parts)} parts in '{filename}'"
        )

    league, team, season, game = parts

    # Validate that all parts are non-empty
    if not all([league, team, season, game]):
        raise FilenameParseError(
            "All filename parts (league, team, season, game) must be non-empty"
        )

    # Validate game number format (should be numeric, can have leading zeros)
    if not game.isdigit():
        raise FilenameParseError(f"Game number must be numeric, found '{game}'")

    return {"league": league, "team": team, "season": season, "game": game}
