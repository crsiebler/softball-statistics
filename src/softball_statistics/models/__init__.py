from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class League:
    """Represents a softball league."""

    id: Optional[int]
    name: str
    season: str

    def __post_init__(self):
        if not self.name or not self.season:
            raise ValueError("League name and season are required")


@dataclass
class Team:
    """Represents a team within a league."""

    id: Optional[int]
    league_id: Optional[int]
    name: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Team name is required")
        if self.league_id is not None and self.league_id < 1:
            raise ValueError("league_id must be positive if provided")


@dataclass
class Player:
    """Represents a player on a team."""

    id: Optional[int]
    team_id: Optional[int]
    name: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Player name is required")
        if self.team_id is not None and self.team_id < 1:
            raise ValueError("team_id must be positive if provided")


@dataclass
class Week:
    """Represents a week within a league season."""

    id: Optional[int]
    league_id: Optional[int]
    week_number: int
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.week_number < 1:
            raise ValueError("Week number must be positive")
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before or equal to end date")
        if self.league_id is not None and self.league_id < 1:
            raise ValueError("league_id must be positive if provided")


@dataclass
class Game:
    """Represents a game within a week."""

    id: Optional[int]
    week_id: Optional[int]
    team_id: Optional[int]
    date: date
    opponent_team_id: Optional[int] = None

    def __post_init__(self):
        if self.week_id is not None and self.week_id < 1:
            raise ValueError("week_id must be positive if provided")
        if self.team_id is not None and self.team_id < 1:
            raise ValueError("team_id must be positive if provided")


@dataclass
class AtBatAttempt:
    """Represents a single at-bat attempt."""

    id: Optional[int]
    player_id: Optional[int]
    game_id: Optional[int]
    outcome: str  # The raw attempt string (e.g., "2B*", "K", "F4")
    bases: int = 0  # 0=out, 1=single, 2=double, 3=triple, 4=home_run
    rbis: int = 0  # Runs batted in for this attempt
    runs_scored: int = 0  # Runs scored on this attempt

    def __post_init__(self):
        if not self.outcome:
            raise ValueError("Outcome is required")
        if self.player_id is not None and self.player_id < 1:
            raise ValueError("player_id must be positive if provided")
        if self.game_id is not None and self.game_id < 1:
            raise ValueError("game_id must be positive if provided")
        if self.bases < 0 or self.bases > 4:
            raise ValueError("Bases must be between 0 and 4")
        if self.rbis < 0 or self.runs_scored < 0:
            raise ValueError("RBIs and runs scored cannot be negative")


@dataclass
class PlayerStats:
    """Calculated statistics for a player."""

    player_id: int
    at_bats: int = 0
    hits: int = 0
    singles: int = 0
    doubles: int = 0
    triples: int = 0
    home_runs: int = 0
    rbis: int = 0
    runs_scored: int = 0
    batting_average: float = 0.0
    on_base_percentage: float = 0.0
    slugging_percentage: float = 0.0
    ops: float = 0.0

    def __post_init__(self):
        if self.player_id < 1:
            raise ValueError("Valid player_id is required")
        for field in [
            "at_bats",
            "hits",
            "singles",
            "doubles",
            "triples",
            "home_runs",
            "rbis",
            "runs_scored",
        ]:
            if getattr(self, field) < 0:
                raise ValueError(f"{field} cannot be negative")
