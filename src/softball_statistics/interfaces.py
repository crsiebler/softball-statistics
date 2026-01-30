"""
Interfaces for dependency injection.
"""

from typing import Any, Dict, Protocol

from softball_statistics.models import League, Team


class Parser(Protocol):
    """Protocol for data parsers."""

    def parse(self, file_path: str) -> Dict[str, Any]:
        ...


class Exporter(Protocol):
    """Protocol for data exporters."""

    def export(self, data: Dict[str, Any], output_path: str) -> None:
        ...


class Calculator(Protocol):
    """Protocol for statistics calculators."""

    def calculate_batting_stats(self, at_bats: list) -> Dict[str, Any]:
        ...


class CommandRepository(Protocol):
    """Protocol for command operations (writes)."""

    def save_game_data(self, objects: Dict[str, Any]) -> None:
        ...

    def save_parsing_warnings(self, warnings: list) -> None:
        ...

    def delete_game_data(self, league: str, team: str, season: str, game: str) -> None:
        ...


class QueryRepository(Protocol):
    """Protocol for query operations (reads)."""

    def game_exists(self, league: str, team: str, season: str, game: str) -> bool:
        ...

    def list_leagues(self) -> list[League]:
        ...

    def list_teams_by_league(self, league_id: int) -> list[Team]:
        ...

    def get_player_stats(self, player_id: int) -> Any:
        ...


class Repository(CommandRepository, QueryRepository, Protocol):
    """Combined repository protocol for backwards compatibility."""
