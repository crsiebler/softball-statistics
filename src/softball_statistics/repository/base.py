"""
Abstract repository interface for data persistence.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from softball_statistics.models import League, Team, Player, Week, Game, AtBatAttempt, PlayerStats


class Repository(ABC):
    """Abstract base class for data repositories."""

    @abstractmethod
    def save_league(self, league: League) -> int:
        """Save a league and return its ID."""
        pass

    @abstractmethod
    def get_league(self, league_id: int) -> Optional[League]:
        """Get a league by ID."""
        pass

    @abstractmethod
    def list_leagues(self) -> List[League]:
        """List all leagues."""
        pass

    @abstractmethod
    def save_team(self, team: Team) -> int:
        """Save a team and return its ID."""
        pass

    @abstractmethod
    def get_team(self, team_id: int) -> Optional[Team]:
        """Get a team by ID."""
        pass

    @abstractmethod
    def list_teams_by_league(self, league_id: int) -> List[Team]:
        """List all teams in a league."""
        pass

    @abstractmethod
    def save_player(self, player: Player) -> int:
        """Save a player and return their ID."""
        pass

    @abstractmethod
    def get_player(self, player_id: int) -> Optional[Player]:
        """Get a player by ID."""
        pass

    @abstractmethod
    def save_week(self, week: Week) -> int:
        """Save a week and return its ID."""
        pass

    @abstractmethod
    def get_week(self, week_id: int) -> Optional[Week]:
        """Get a week by ID."""
        pass

    @abstractmethod
    def save_game(self, game: Game) -> int:
        """Save a game and return its ID."""
        pass

    @abstractmethod
    def get_game(self, game_id: int) -> Optional[Game]:
        """Get a game by ID."""
        pass

    @abstractmethod
    def game_exists(self, league: str, team: str, season: str, game: str) -> bool:
        """Check if a game already exists."""
        pass

    @abstractmethod
    def delete_game_data(self, league: str, team: str, season: str, game: str) -> None:
        """Delete all data for a specific game."""
        pass

    @abstractmethod
    def save_at_bat(self, attempt: AtBatAttempt) -> int:
        """Save an at-bat attempt and return its ID."""
        pass

    @abstractmethod
    def get_player_stats(self, player_id: int, week_id: Optional[int] = None) -> Optional[PlayerStats]:
        """Get calculated stats for a player, optionally for a specific week."""
        pass

    @abstractmethod
    def save_game_data(self, objects: Dict[str, List]) -> None:
        """Save all game data objects in the correct order."""
        pass