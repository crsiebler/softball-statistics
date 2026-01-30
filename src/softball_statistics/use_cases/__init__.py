"""
Use cases for softball statistics application.
"""

from typing import Any, Dict

from softball_statistics.calculators.stats_calculator import (
    calculate_batting_average,
    calculate_ops,
    calculate_slg,
)
from softball_statistics.interfaces import CommandRepository, Parser, QueryRepository
from softball_statistics.models import League, Team


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

        # Calculate team batting average
        team_batting_average = calculate_batting_average(total_hits, total_at_bats)

        # For OBP and SLG, we need walks and HBP data, but these aren't tracked in PlayerStats
        # For now, calculate SLG from available data and set OBP to BA (simplified)
        team_slugging_percentage = calculate_slg(
            total_singles, total_doubles, total_triples, total_home_runs, total_at_bats
        )

        # Simplified OBP calculation - in a full implementation, we'd need walks/HBP data
        # For now, use batting average as approximation
        team_on_base_percentage = team_batting_average

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

        return 1  # Fallback to original behavior


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
