"""Read manually maintained season share links without relying on database IDs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DEFAULT_SEASON_LINKS = Path("data/season_links.json")


@dataclass(frozen=True)
class SeasonLinks:
    """Published destinations; presence does not establish public visibility."""

    league: str
    season: str
    team: str
    urls: tuple[str, ...]


def load_season_links(path: Path = DEFAULT_SEASON_LINKS) -> list[SeasonLinks]:
    """Validate the whole registry so ambiguous destinations cannot be selected."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError(f"Unsupported season links format: {path}")
    if not isinstance(data.get("seasons"), list):
        raise ValueError(f"Season links must contain a seasons list: {path}")
    result = []
    identities = set()
    for item in data["seasons"]:
        if not isinstance(item, dict) or any(
            not isinstance(item.get(key), str) or not item[key].strip()
            for key in ("league", "season", "team")
        ):
            raise ValueError("Each season link record needs league, season, and team")
        identity = tuple(
            item[key].strip().casefold() for key in ("league", "season", "team")
        )
        if identity in identities:
            raise ValueError("Duplicate league/season/team in season links")
        identities.add(identity)
        urls = item.get("urls")
        if (
            not isinstance(urls, list)
            or not urls
            or any(
                not isinstance(url, str)
                or not re.fullmatch(
                    r"https://docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]+(?:/[^\s]*)?",
                    url,
                )
                for url in urls
            )
        ):
            raise ValueError(
                "Season urls must be a nonempty list of Google Sheet HTTPS links"
            )
        result.append(
            SeasonLinks(
                item["league"].strip(),
                item["season"].strip(),
                item["team"].strip(),
                tuple(urls),
            )
        )
    return result


def find_season_links(
    path: Path = DEFAULT_SEASON_LINKS,
    *,
    league: Optional[str] = None,
    season: Optional[str] = None,
    team: Optional[str] = None,
) -> list[SeasonLinks]:
    """Match names case-insensitively; never fall back to another season."""
    filters = {"league": league, "season": season, "team": team}
    return [
        record
        for record in load_season_links(path)
        if all(
            value is None or getattr(record, key).casefold() == value.strip().casefold()
            for key, value in filters.items()
        )
    ]
