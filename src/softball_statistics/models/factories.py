"""
Factories for creating model instances.
"""

from typing import Any, Dict

from softball_statistics.models import League, Player, Team


class LeagueFactory:
    """Factory for creating League instances."""

    @staticmethod
    def create_league(data: Dict[str, Any]) -> League:
        """Create a League from data dictionary."""
        return League(
            id=data.get("id"),
            name=data["name"],
            season=data["season"],
        )


class TeamFactory:
    """Factory for creating Team instances."""

    @staticmethod
    def create_team(data: Dict[str, Any]) -> Team:
        """Create a Team from data dictionary."""
        return Team(
            id=data.get("id"),
            league_id=data["league_id"],
            name=data["name"],
        )


class PlayerFactory:
    """Factory for creating Player instances."""

    @staticmethod
    def create_player(data: Dict[str, Any]) -> Player:
        """Create a Player from data dictionary."""
        return Player(
            id=data.get("id"),
            team_id=data["team_id"],
            name=data["name"],
        )
