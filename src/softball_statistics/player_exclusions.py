"""Load summary-only player exclusions independently of database IDs."""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_PLAYER_EXCLUSIONS = Path("data/player_exclusions.json")
PlayerIdentity = tuple[str, str, str]


def player_identity(league: str, team: str, player: str) -> PlayerIdentity:
    """Match full names within a league/team, ignoring case and outer spaces."""
    return league.strip().casefold(), team.strip().casefold(), player.strip().casefold()


def load_player_exclusions(path: Path | None = None) -> frozenset[PlayerIdentity]:
    """Validate all exclusions before export; a missing default means no exclusions."""
    selected = DEFAULT_PLAYER_EXCLUSIONS if path is None else Path(path)
    try:
        data = json.loads(selected.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if path is None:
            return frozenset()
        raise
    if (
        not isinstance(data, dict)
        or set(data) != {"version", "players"}
        or type(data["version"]) is not int
        or data["version"] != 1
        or not isinstance(data["players"], list)
    ):
        raise ValueError(f"Invalid player exclusions format: {selected}")
    identities = set()
    for entry in data["players"]:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"league", "team", "player"}
            or any(
                not isinstance(value, str) or not value.strip()
                for value in entry.values()
            )
        ):
            raise ValueError(
                "Each player exclusion needs only league, team, and player names"
            )
        identity = player_identity(entry["league"], entry["team"], entry["player"])
        if identity in identities:
            raise ValueError("Duplicate player exclusion")
        identities.add(identity)
    return frozenset(identities)
