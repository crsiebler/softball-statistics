"""Write bounded league/season workbooks using prepared historical snapshots."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from softball_statistics.exporters.excel_exporter import (
    ExcelExportError,
    _abbreviate_team_name,
    _create_cumulative_team_sheet,
    _create_legend_sheet,
    _create_per_game_sheet,
    _create_season_total_sheet,
)
from softball_statistics.interfaces import QueryRepository
from softball_statistics.use_cases import CalculateStatsUseCase
from softball_statistics.use_cases.season_exports import SeasonExportUseCase


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "unnamed"


def _sheet_name(label: str, writer: pd.ExcelWriter) -> str:
    """Keep game tabs distinct even with long seasons or colliding team initials."""
    label = re.sub(r"[\\/*?:\[\]]", "_", label).strip("'") or "Sheet"
    existing = {name.casefold() for name in writer.sheets}
    candidate = label[:31]
    index = 2
    while candidate.casefold() in existing:
        suffix = f" ({index})"
        candidate = label[: 31 - len(suffix)] + suffix
        index += 1
    return candidate


def _write_snapshot(snapshot: dict[str, Any], path: Path) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for team_name in snapshot["team_stats"]:
            short_name = _abbreviate_team_name(team_name)
            cumulative = snapshot["cumulative_team_stats"][team_name]
            _create_cumulative_team_sheet(
                team_name,
                {**cumulative, "team_totals": cumulative},
                writer,
                sheet_name=_sheet_name(f"{short_name} Total", writer),
            )
            _create_season_total_sheet(
                team_name,
                snapshot["season"],
                snapshot,
                writer,
                sheet_name=_sheet_name(
                    f"{short_name} {snapshot['season']} Total", writer
                ),
            )

        # Show the most recent game first, preserving doubleheader order in reverse.
        for game in reversed(snapshot["games"]):
            label = (
                f"{_abbreviate_team_name(game['team_name'])} "
                f"{snapshot['season']} Game {game['game_number']}"
            )
            _create_per_game_sheet(
                game["team_name"],
                game,
                game["players"],
                writer,
                sheet_name=_sheet_name(label, writer),
            )

        _create_legend_sheet(writer)


def export_season_workbooks(
    query_repo: QueryRepository, stats: CalculateStatsUseCase, output_path: str
) -> list[str]:
    """Treat output_path as a filename prefix, e.g. stats-fray-winter_2026.xlsx."""
    try:
        base = Path(output_path)
        snapshots = SeasonExportUseCase(query_repo, stats).execute()
        slugs = [f"{_slug(s['league_name'])}-{_slug(s['season'])}" for s in snapshots]
        counts = Counter(slugs)
        if snapshots:
            base.parent.mkdir(parents=True, exist_ok=True)
        paths = []
        for snapshot, slug in zip(snapshots, slugs):
            # Keep distinct league/season identities even if sanitizing collides.
            if counts[slug] > 1:
                slug += f"-{snapshot['league_id']}"
            path = base.with_name(f"{base.stem}-{slug}.xlsx")
            _write_snapshot(snapshot, path)
            paths.append(str(path))
        return paths
    except Exception as exc:
        raise ExcelExportError(f"Failed to export season workbooks: {exc}") from exc
