"""Build league/season export snapshots without leaking future games."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from softball_statistics.calculators.stats_calculator import (
    calculate_batting_average,
    calculate_obp,
    calculate_ops,
    calculate_slg,
)
from softball_statistics.interfaces import QueryRepository
from softball_statistics.use_cases import CalculateStatsUseCase

COUNT_FIELDS = (
    "plate_appearances",
    "at_bats",
    "hits",
    "singles",
    "doubles",
    "triples",
    "home_runs",
    "walks",
    "sacrifice_flies",
    "hit_pitcher_outs",
    "home_run_outs",
    "rbis",
    "runs_scored",
)


def _rates(counts: dict[str, Any]) -> dict[str, float]:
    """Calculate rates from counts, never averages of per-game rates."""
    ba = calculate_batting_average(counts["hits"], counts["at_bats"])
    obp = calculate_obp(
        counts["hits"], counts["walks"], 0, counts["at_bats"], counts["sacrifice_flies"]
    )
    slg = calculate_slg(
        counts["singles"],
        counts["doubles"],
        counts["triples"],
        counts["home_runs"],
        counts["at_bats"],
    )
    return {
        "batting_average": ba,
        "on_base_percentage": obp,
        "slugging_percentage": slg,
        "ops": calculate_ops(obp, slg),
    }


def _aggregate_players(games: list[dict[str, Any]]) -> list[dict[str, Any]]:
    players: dict[str, dict[str, Any]] = {}
    for game in games:
        for player in game["players"]:
            name = player["player_name"]
            if name not in players:
                players[name] = {
                    "player_name": name,
                    **dict.fromkeys(COUNT_FIELDS, 0),
                }
            for field in COUNT_FIELDS:
                players[name][field] += player.get(field, 0)
    for player in players.values():
        player.update(_rates(player))
    return sorted(players.values(), key=lambda player: player["player_name"].casefold())


def _team_stats(games: list[dict[str, Any]]) -> dict[str, Any]:
    players = _aggregate_players(games)
    totals = {field: sum(p[field] for p in players) for field in COUNT_FIELDS}
    return {
        "players": players,
        "games_played": len(games),
        **{f"team_{key}": value for key, value in _rates(totals).items()},
    }


class SeasonExportUseCase:
    """Prepare all season snapshots from the same read-only repository."""

    def __init__(self, query_repo: QueryRepository, stats: CalculateStatsUseCase):
        self.query_repo = query_repo
        self.stats = stats

    def execute(self) -> list[dict[str, Any]]:
        """Include only same-league games dated through each season's last game.

        Season names are labels, not chronological sort keys. A backfilled or
        overlapping season is handled by individual game dates. Empty seasons
        have no cutoff and do not produce a workbook.
        """
        by_league: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for league in self.query_repo.list_leagues():
            if league.id is None:
                continue
            for team in self.query_repo.list_teams_by_league(league.id):
                if team.id is None:
                    continue
                for game in self.stats.get_team_games_stats(team.id):
                    by_league[league.name].append(
                        {
                            **game,
                            "date": str(game["date"]),
                            "league_id": league.id,
                            "season": league.season,
                            "team_name": team.name,
                            "players": self.stats.get_game_player_stats(
                                game["game_id"]
                            ),
                        }
                    )

        snapshots = []
        for league_name, games in sorted(by_league.items()):
            games.sort(
                key=lambda g: (
                    g["date"],
                    g["game_number"],
                    g["team_name"],
                    g["game_id"],
                )
            )
            seasons: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for game in games:
                seasons[game["season"]].append(game)
            for season, season_games in seasons.items():
                cutoff = season_games[-1]["date"]
                history = [g for g in games if g["date"] <= cutoff]
                current_teams = sorted({g["team_name"] for g in season_games})
                historical_teams = sorted({g["team_name"] for g in history})
                snapshots.append(
                    {
                        "league_id": season_games[0]["league_id"],
                        "league_name": league_name,
                        "season": season,
                        "as_of": cutoff,
                        "games": season_games,
                        "team_stats": {
                            name: _team_stats(
                                [g for g in season_games if g["team_name"] == name]
                            )
                            for name in current_teams
                        },
                        "cumulative_team_stats": {
                            name: _team_stats(
                                [g for g in history if g["team_name"] == name]
                            )
                            for name in historical_teams
                        },
                        "players": _aggregate_players(history),
                    }
                )
        return snapshots
