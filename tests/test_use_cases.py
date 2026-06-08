import os
import tempfile
from datetime import date
from unittest.mock import Mock

import pytest

from softball_statistics.models import Game, League, PlateAppearance, Player, Team, Week
from softball_statistics.parsers.csv_parser import CSVParser
from softball_statistics.repository.sqlite import SQLiteRepository
from softball_statistics.use_cases import (
    CalculateStatsUseCase,
    ProcessGameUseCase,
    ValidationError,
)


class TestProcessGameUseCase:
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_command_repo = Mock()
        self.mock_query_repo = Mock()
        self.parser = CSVParser()
        self.use_case = ProcessGameUseCase(
            self.parser, self.mock_command_repo, self.mock_query_repo
        )

    def test_process_game_valid_data(self):
        """Test processing a game with valid RBI/run totals."""
        # Create CSV with balanced RBIs and runs
        csv_content = """Player Name,Attempt1,Attempt2
Player1,1B,2B*
Player2,HR*,F4+
"""
        # Player1: 1B (0 RBI, 0 runs), 2B* (1 RBI, 0 runs) = 1 RBI, 0 runs
        # Player2: HR* (1 RBI, 1 run), F4+ (0 RBI, 1 run) = 1 RBI, 2 runs
        # Total: 2 RBI, 2 runs - balanced!

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                # Mock repo methods
                self.mock_query_repo.game_exists.return_value = False
                self.mock_command_repo.save_game_data.return_value = None
                self.mock_command_repo.save_parsing_warnings.return_value = None

                # Should succeed
                result = self.use_case.execute(f.name)

                # Verify parsing worked
                assert len(result["plate_appearances"]) == 4
                total_rbis = sum(pa["rbis"] for pa in result["plate_appearances"])
                total_runs = sum(
                    pa["runs_scored"] for pa in result["plate_appearances"]
                )
                assert total_rbis == total_runs == 2

            finally:
                os.unlink(f.name)

    def test_process_game_rbi_run_mismatch_validation(self):
        """Test that mismatched RBI/run totals raise ValidationError."""
        # To make unequal, need more RBIs
        csv_content = """Player Name,Attempt1,Attempt2
Player1,2B**,1B
Player2,HR,F4+
"""
        # Player1: 2B** (2 RBI, 0 runs), 1B (0 RBI, 0 runs) = 2 RBI, 0 runs
        # Player2: HR (1 RBI, 1 run), F4+ (0 RBI, 1 run) = 1 RBI, 2 runs
        # Total: 3 RBI, 2 runs - perfect, unequal!

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                # Should raise ValidationError
                with pytest.raises(
                    ValidationError,
                    match=r"RBI total \(3\) does not equal run total \(2\)\. File rejected\.",
                ):
                    self.use_case.execute(f.name)

            finally:
                os.unlink(f.name)


class TestCalculateStatsUseCase:
    def test_league_summary_combines_same_league_team_across_seasons(self, tmp_path):
        """Same league/team in multiple seasons should produce one summary row."""
        repo = SQLiteRepository(str(tmp_path / "test.db"))
        self._save_game(repo, "Fray", "Spring 2025", "Cyclones", 1)
        self._save_game(repo, "Fray", "Summer 2025", "Cyclones", 2)
        self._save_game(repo, "Other League", "Spring 2025", "Cyclones", 3)

        summary = CalculateStatsUseCase(repo).get_league_summary_data()

        fray_rows = [
            row
            for row in summary
            if row["League"] == "Fray" and row["Team"] == "Cyclones"
        ]
        other_rows = [
            row
            for row in summary
            if row["League"] == "Other League" and row["Team"] == "Cyclones"
        ]
        assert len(fray_rows) == 1
        assert fray_rows[0]["Games Played"] == 2
        assert len(other_rows) == 1
        assert other_rows[0]["Games Played"] == 1

    def _save_game(
        self,
        repo: SQLiteRepository,
        league_name: str,
        season: str,
        team_name: str,
        week_number: int,
    ) -> None:
        league_id = repo.save_league(League(None, league_name, season))
        team_id = repo.save_team(Team(None, league_id, team_name))
        player_id = repo.save_player(Player(None, team_id, "Player One"))
        week_id = repo.save_week(
            Week(
                None,
                league_id,
                week_number,
                date(2025, 1, week_number),
                date(2025, 1, week_number),
            )
        )
        game_id = repo.save_game(
            Game(None, week_id, team_id, date(2025, 1, week_number), 1)
        )
        repo.save_plate_appearance(
            PlateAppearance(None, player_id, game_id, "1B", bases=1)
        )
