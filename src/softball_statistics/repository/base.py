"""
Abstract repository interface for data persistence.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from softball_statistics.models import (
    AtBatAttempt,
    Game,
    League,
    Player,
    PlayerStats,
    Team,
    Week,
)


class Repository(ABC):
    """Abstract base class for data repositories."""

    @abstractmethod
    def save_league(self, league: League) -> int:
        """Save a league and return its ID."""

    @abstractmethod
    def get_league(self, league_id: int) -> Optional[League]:
        """Get a league by ID."""

    @abstractmethod
    def list_leagues(self) -> List[League]:
        """List all leagues."""

    @abstractmethod
    def save_team(self, team: Team) -> int:
        """Save a team and return its ID."""

    @abstractmethod
    def get_team(self, team_id: int) -> Optional[Team]:
        """Get a team by ID."""

    @abstractmethod
    def list_teams_by_league(self, league_id: int) -> List[Team]:
        """List all teams in a league."""

    @abstractmethod
    def save_player(self, player: Player) -> int:
        """Save a player and return their ID."""

    @abstractmethod
    def get_player(self, player_id: int) -> Optional[Player]:
        """Get a player by ID."""

    @abstractmethod
    def save_week(self, week: Week) -> int:
        """Save a week and return its ID."""

    @abstractmethod
    def get_week(self, week_id: int) -> Optional[Week]:
        """Get a week by ID."""

    @abstractmethod
    def save_game(self, game: Game) -> int:
        """Save a game and return its ID."""

    @abstractmethod
    def get_game(self, game_id: int) -> Optional[Game]:
        """Get a game by ID."""

    @abstractmethod
    def game_exists(self, league: str, team: str, season: str, game: str) -> bool:
        """Check if a game already exists."""

    @abstractmethod
    def delete_game_data(self, league: str, team: str, season: str, game: str) -> None:
        """Delete all data for a specific game."""

    @abstractmethod
    def save_at_bat(self, attempt: AtBatAttempt) -> int:
        """Save an at-bat attempt and return its ID."""

    @abstractmethod
    def get_player_stats(
        self, player_id: int, week_id: Optional[int] = None
    ) -> Optional[PlayerStats]:
        """Get calculated stats for a player, optionally for a specific week."""

    @abstractmethod
    def save_game_data(self, objects: Dict[str, List]) -> None:
        """Save all game data objects in the correct order."""
