"""
Use cases for softball statistics application.
"""

from __future__ import annotations

from typing import Any, Dict

from softball_statistics.calculators.stats_calculator import (
    calculate_batting_average,
    calculate_ops,
    calculate_slg,
)
from softball_statistics.interfaces import CommandRepository, Parser, QueryRepository
from softball_statistics.models import League, Team


class ValidationError(Exception):
    """Raised when game data validation fails."""


class ProcessGameUseCase:
    """Use case for processing a game file."""

    def __init__(
        self,
        parser: Parser,
        command_repo: CommandRepository,
        query_repo: QueryRepository,
    ):
        self.parser = parser
        self.command_repo = command_repo
        self.query_repo = query_repo

    def execute(self, file_path: str, replace_existing: bool = False) -> Dict[str, Any]:
        """Process a game file and save to repository.

        Returns parsed data with metadata.
        """
        # Parse the file
        parsed_data = self.parser.parse(file_path)

        # Validate RBI total equals run total
        total_rbis = sum(pa["rbis"] for pa in parsed_data["plate_appearances"])
        total_runs = sum(pa["runs_scored"] for pa in parsed_data["plate_appearances"])

        if total_rbis != total_runs:
            raise ValidationError(
                f"RBI total ({total_rbis}) does not equal run total ({total_runs}). "
                f"File rejected."
            )

        # Create database objects
        # Note: This assumes create_database_objects is moved to domain or injected
        # For now, keep as is, but ideally refactor
        from softball_statistics.parsers.csv_parser import create_database_objects

        objects = create_database_objects(parsed_data)

        # Check if game exists
        metadata = parsed_data["metadata"]
        game_exists = self.query_repo.game_exists(
            metadata["league"], metadata["team"], metadata["season"], metadata["game"]
        )

        if game_exists and not replace_existing:
            raise ValueError("Game already exists")

        if game_exists and replace_existing:
            self.command_repo.delete_game_data(
                metadata["league"],
                metadata["team"],
                metadata["season"],
                metadata["game"],
            )

        # Save to repository
        self.command_repo.save_game_data(objects)

        # Save warnings
        warnings = parsed_data.get("warnings", [])
        if warnings:
            self.command_repo.save_parsing_warnings(warnings)

        return parsed_data


class CalculateStatsUseCase:
    """Use case for calculating and retrieving statistics."""

    def __init__(self, query_repo: QueryRepository):
        self.query_repo = query_repo

    def execute(self, league_name: str, team_name: str, season: str) -> Dict[str, Any]:
        """Calculate stats for a team.

        Returns stats data ready for export.
        """
        # Find league
        leagues = self.query_repo.list_leagues()
        league = next(
            (l for l in leagues if l.name == league_name and l.season == season), None
        )
        if not league or not league.id:
            raise ValueError(f"League '{league_name}' season '{season}' not found")

        # Find team
        teams = self.query_repo.list_teams_by_league(league.id)
        team = next((t for t in teams if t.name == team_name), None)
        if not team or not team.id:
            raise ValueError(f"Team '{team_name}' not found in league")

        # Get players and stats
        # Note: This uses raw SQL access, should be abstracted
        players_data = []
        # For now, keep similar logic, but ideally repository should provide this
        from softball_statistics.repository.sqlite import SQLiteQueryRepository

        if isinstance(self.query_repo, SQLiteQueryRepository):
            with self.query_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name FROM players WHERE team_id = ?", (team.id,)
                )
                players = cursor.fetchall()

            for player_id, player_name in players:
                stats = self.query_repo.get_player_stats(player_id)
                if stats:
                    player_stats_dict = {
                        "player_id": player_id,
                        "player_name": player_name,
                        "at_bats": stats.at_bats,
                        "hits": stats.hits,
                        "singles": stats.singles,
                        "doubles": stats.doubles,
                        "triples": stats.triples,
                        "home_runs": stats.home_runs,
                        "rbis": stats.rbis,
                        "runs_scored": stats.runs_scored,
                        "batting_average": stats.batting_average,
                        "on_base_percentage": stats.on_base_percentage,
                        "slugging_percentage": stats.slugging_percentage,
                        "ops": stats.ops,
                        "plate_appearances": stats.plate_appearances,
                        "walks": stats.walks,
                        "sacrifice_flies": stats.sacrifice_flies,
                    }
                    players_data.append(player_stats_dict)

        # Calculate team-level statistics
        team_totals = self._calculate_team_totals(players_data)

        # Calculate actual games played
        games_played = self._calculate_games_played(team.id)

        team_stats = {
            team_name: {
                "players": players_data,
                "games_played": games_played,
                **team_totals,  # Include team totals
            }
        }

        return {
            "league_name": league_name,
            "season": season,
            "team_stats": team_stats,
        }

    def _calculate_team_totals(
        self, players_data: list[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate team-level statistics by aggregating player data."""
        if not players_data:
            return {
                "team_batting_average": 0.000,
                "team_on_base_percentage": 0.000,
                "team_slugging_percentage": 0.000,
                "team_ops": 0.000,
            }

        # Sum all player statistics
        total_at_bats = sum(player.get("at_bats", 0) for player in players_data)
        total_hits = sum(player.get("hits", 0) for player in players_data)
        total_singles = sum(player.get("singles", 0) for player in players_data)
        total_doubles = sum(player.get("doubles", 0) for player in players_data)
        total_triples = sum(player.get("triples", 0) for player in players_data)
        total_home_runs = sum(player.get("home_runs", 0) for player in players_data)
        total_walks = sum(player.get("walks", 0) for player in players_data)
        total_sacrifice_flies = sum(
            player.get("sacrifice_flies", 0) for player in players_data
        )

        # Calculate team batting average
        team_batting_average = calculate_batting_average(total_hits, total_at_bats)

        # Calculate accurate OBP: (H + BB) / (AB + BB + SF)
        obp_denominator = total_at_bats + total_walks + total_sacrifice_flies
        team_on_base_percentage = (
            (total_hits + total_walks) / obp_denominator if obp_denominator > 0 else 0.0
        )

        # Calculate SLG from available data
        team_slugging_percentage = calculate_slg(
            total_singles, total_doubles, total_triples, total_home_runs, total_at_bats
        )

        team_ops = calculate_ops(team_on_base_percentage, team_slugging_percentage)

        return {
            "team_batting_average": round(team_batting_average, 3),
            "team_on_base_percentage": round(team_on_base_percentage, 3),
            "team_slugging_percentage": round(team_slugging_percentage, 3),
            "team_ops": round(team_ops, 3),
        }

    def _calculate_games_played(self, team_id: int) -> int:
        """Calculate actual number of games played by the team."""
        from softball_statistics.repository.sqlite import SQLiteQueryRepository

        if isinstance(self.query_repo, SQLiteQueryRepository):
            with self.query_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(DISTINCT g.id) FROM games g WHERE g.team_id = ?",
                    (team_id,),
                )
                result = cursor.fetchone()
                return result[0] if result else 0

        return 0

    def get_cumulative_team_stats(self, team_name: str) -> Dict[str, Any]:
        """Get cumulative stats for a team across all seasons."""
        from softball_statistics.repository.sqlite import SQLiteQueryRepository

        if not isinstance(self.query_repo, SQLiteQueryRepository):
            raise ValueError("Cumulative stats require SQLite repository")

        aggregated_players = {}
        all_team_ids = []

        with self.query_repo._get_connection() as conn:
            cursor = conn.cursor()
            # Find all teams with this name
            cursor.execute("SELECT id FROM teams WHERE name = ?", (team_name,))
            team_ids = [row[0] for row in cursor.fetchall()]
            all_team_ids.extend(team_ids)

        if not all_team_ids:
            return {"players": [], "team_totals": self._calculate_team_totals([])}

        # Get all players for these teams and aggregate by player_name
        for team_id in all_team_ids:
            with self.query_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name FROM players WHERE team_id = ?", (team_id,)
                )
                players = cursor.fetchall()

            for player_id, player_name in players:
                stats = self.query_repo.get_player_stats(player_id)
                if stats:
                    if player_name not in aggregated_players:
                        aggregated_players[player_name] = {
                            "player_id": player_id,
                            "player_name": player_name,
                            "at_bats": stats.at_bats,
                            "hits": stats.hits,
                            "singles": stats.singles,
                            "doubles": stats.doubles,
                            "triples": stats.triples,
                            "home_runs": stats.home_runs,
                            "rbis": stats.rbis,
                            "runs_scored": stats.runs_scored,
                            "batting_average": stats.batting_average,
                            "on_base_percentage": stats.on_base_percentage,
                            "slugging_percentage": stats.slugging_percentage,
                            "ops": stats.ops,
                            "plate_appearances": stats.plate_appearances,
                            "walks": stats.walks,
                            "sacrifice_flies": stats.sacrifice_flies,
                        }
                    else:
                        # Sum the stats
                        aggregated_players[player_name]["at_bats"] += stats.at_bats
                        aggregated_players[player_name]["hits"] += stats.hits
                        aggregated_players[player_name]["singles"] += stats.singles
                        aggregated_players[player_name]["doubles"] += stats.doubles
                        aggregated_players[player_name]["triples"] += stats.triples
                        aggregated_players[player_name]["home_runs"] += stats.home_runs
                        aggregated_players[player_name]["rbis"] += stats.rbis
                        aggregated_players[player_name][
                            "runs_scored"
                        ] += stats.runs_scored
                        aggregated_players[player_name][
                            "plate_appearances"
                        ] += stats.plate_appearances
                        aggregated_players[player_name]["walks"] += stats.walks
                        aggregated_players[player_name][
                            "sacrifice_flies"
                        ] += stats.sacrifice_flies

        # Recalculate derived stats after aggregation
        players_data = []
        for player in aggregated_players.values():
            ab = player["at_bats"]
            hits = player["hits"]
            singles = player["singles"]
            doubles = player["doubles"]
            triples = player["triples"]
            hr = player["home_runs"]
            player["walks"]
            player["sacrifice_flies"]
            player["plate_appearances"]

            # Recalculate averages
            player["batting_average"] = (
                calculate_batting_average(hits, ab) if ab > 0 else 0.0
            )
            # Simplified OBP (BA approximation, as before)
            player["on_base_percentage"] = player["batting_average"]
            player["slugging_percentage"] = (
                calculate_slg(singles, doubles, triples, hr, ab) if ab > 0 else 0.0
            )
            player["ops"] = calculate_ops(
                player["on_base_percentage"], player["slugging_percentage"]
            )

            players_data.append(player)

        team_totals = self._calculate_team_totals(players_data)

        # Calculate total games played across all seasons
        total_games = sum(
            self._calculate_games_played(team_id) for team_id in all_team_ids
        )

        return {
            "players": players_data,
            "team_totals": team_totals,
            "games_played": total_games,
        }

    def get_team_games_stats(self, team_id: int) -> list[Dict[str, Any]]:
        """Get stats for each game played by the team."""
        from softball_statistics.repository.sqlite import SQLiteQueryRepository

        if not isinstance(self.query_repo, SQLiteQueryRepository):
            return []

        games_stats = []

        with self.query_repo._get_connection() as conn:
            cursor = conn.cursor()
            # Get all games for the team, ordered by date
            cursor.execute(
                """
                SELECT g.id, g.game_number, g.date, w.week_number, l.name as league_name, l.season
                FROM games g
                JOIN weeks w ON g.week_id = w.id
                JOIN leagues l ON w.league_id = l.id
                WHERE g.team_id = ?
                ORDER BY g.date
                """,
                (team_id,),
            )
            games = cursor.fetchall()

        for game_id, game_number, date, week_number, league_name, season in games:
            # Get all plate appearances for this game
            with self.query_repo._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT outcome, bases, rbis, runs_scored FROM plate_appearances WHERE game_id = ?",
                    (game_id,),
                )
                attempts = cursor.fetchall()

            # Aggregate game stats
            total_attempts = len(attempts)
            hits = 0
            singles = 0
            doubles = 0
            triples = 0
            home_runs = 0
            walks = 0
            rbis = 0
            runs_scored = 0
            sacrifice_flies = 0

            for outcome, bases, attempt_rbis, attempt_runs in attempts:
                outcome_lower = outcome.lower()
                rbis += attempt_rbis
                runs_scored += attempt_runs

                if outcome_lower.startswith("bb"):
                    walks += 1
                elif bases > 0:
                    hits += 1
                    if bases == 1:
                        singles += 1
                    elif bases == 2:
                        doubles += 1
                    elif bases == 3:
                        triples += 1
                    elif bases == 4:
                        home_runs += 1
                elif attempt_rbis > 0 and outcome.startswith("F"):
                    sacrifice_flies += 1

            at_bats = total_attempts - walks - sacrifice_flies

            # Calculate team stats for the game
            game_stats = {
                "game_id": game_id,
                "game_number": game_number,
                "date": date,
                "week_number": week_number,
                "league_name": league_name,
                "season": season,
                "plate_appearances": total_attempts,
                "at_bats": at_bats,
                "hits": hits,
                "singles": singles,
                "doubles": doubles,
                "triples": triples,
                "home_runs": home_runs,
                "walks": walks,
                "sacrifice_flies": sacrifice_flies,
                "rbis": rbis,
                "runs_scored": runs_scored,
                "batting_average": calculate_batting_average(hits, at_bats)
                if at_bats > 0
                else 0.0,
                "on_base_percentage": calculate_batting_average(hits, at_bats)
                if at_bats > 0
                else 0.0,  # Simplified
                "slugging_percentage": calculate_slg(
                    singles, doubles, triples, home_runs, at_bats
                )
                if at_bats > 0
                else 0.0,
                "ops": calculate_ops(
                    calculate_batting_average(hits, at_bats) if at_bats > 0 else 0.0,
                    calculate_slg(singles, doubles, triples, home_runs, at_bats)
                    if at_bats > 0
                    else 0.0,
                ),
            }
            games_stats.append(game_stats)

        return games_stats

    def get_game_player_stats(self, game_id: int) -> list[Dict[str, Any]]:
        """Get individual player stats for a specific game."""
        from softball_statistics.repository.sqlite import SQLiteQueryRepository

        if not isinstance(self.query_repo, SQLiteQueryRepository):
            return []

        player_stats = {}

        with self.query_repo._get_connection() as conn:
            cursor = conn.cursor()
            # Get all plate appearances for this game with player info
            cursor.execute(
                """
                SELECT pa.outcome, pa.bases, pa.rbis, pa.runs_scored, p.id, p.name
                FROM plate_appearances pa
                JOIN players p ON pa.player_id = p.id
                WHERE pa.game_id = ?
                ORDER BY p.name
                """,
                (game_id,),
            )
            attempts = cursor.fetchall()

        # Group by player
        for outcome, bases, rbis, runs_scored, player_id, player_name in attempts:
            if player_id not in player_stats:
                player_stats[player_id] = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "plate_appearances": 0,
                    "at_bats": 0,
                    "hits": 0,
                    "singles": 0,
                    "doubles": 0,
                    "triples": 0,
                    "home_runs": 0,
                    "walks": 0,
                    "sacrifice_flies": 0,
                    "rbis": 0,
                    "runs_scored": 0,
                }

            player = player_stats[player_id]
            player["plate_appearances"] += 1
            player["rbis"] += rbis
            player["runs_scored"] += runs_scored

            outcome_lower = outcome.lower()
            if outcome_lower.startswith("bb"):
                player["walks"] += 1
            elif bases > 0:
                player["hits"] += 1
                if bases == 1:
                    player["singles"] += 1
                elif bases == 2:
                    player["doubles"] += 1
                elif bases == 3:
                    player["triples"] += 1
                elif bases == 4:
                    player["home_runs"] += 1
            elif rbis > 0 and outcome.startswith("F"):
                player["sacrifice_flies"] += 1

        # Calculate derived stats for each player
        result = []
        for player in player_stats.values():
            pa = player["plate_appearances"]
            walks = player["walks"]
            sf = player["sacrifice_flies"]
            ab = pa - walks - sf
            player["at_bats"] = ab
            hits = player["hits"]
            singles = player["singles"]
            doubles = player["doubles"]
            triples = player["triples"]
            hr = player["home_runs"]

            # Calculate averages
            player["batting_average"] = (
                calculate_batting_average(hits, ab) if ab > 0 else 0.0
            )
            # Simplified OBP (BA approximation)
            player["on_base_percentage"] = player["batting_average"]
            player["slugging_percentage"] = (
                calculate_slg(singles, doubles, triples, hr, ab) if ab > 0 else 0.0
            )
            player["ops"] = calculate_ops(
                player["on_base_percentage"], player["slugging_percentage"]
            )

            result.append(player)

        return result


class ListLeaguesUseCase:
    """Use case for listing leagues."""

    def __init__(self, query_repo: QueryRepository):
        self.query_repo = query_repo

    def execute(self) -> list[League]:
        """List all leagues."""
        return self.query_repo.list_leagues()


class ListTeamsUseCase:
    """Use case for listing teams in a league."""

    def __init__(self, query_repo: QueryRepository):
        self.query_repo = query_repo

    def execute(self, league_name: str) -> list[Team]:
        """List teams in a league."""
        leagues = self.query_repo.list_leagues()
        league = next((l for l in leagues if l.name == league_name), None)
        if not league or not league.id:
            raise ValueError(f"League '{league_name}' not found")
        return self.query_repo.list_teams_by_league(league.id)
