import os
import tempfile
from unittest.mock import Mock

import pytest

from softball_statistics.parsers.csv_parser import CSVParser
from softball_statistics.use_cases import ProcessGameUseCase, ValidationError


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
        # Create CSV with unbalanced RBIs and runs
        # Player1: 1B (0 RBI, 0 runs), 2B* (1 RBI, 0 runs) = 1 RBI, 0 runs
        # Player2: HR* (1 RBI, 1 run from HR assumption), F4+ (0 RBI, 1 run) = 1 RBI, 2 runs
        # Total: 2 RBI, 2 runs - wait, need to make them unequal
        csv_content = """Player Name,Attempt1,Attempt2
Player1,2B*,1B+
Player2,HR*,F4
"""
        # Player1: 2B* (1 RBI, 0 runs), 1B+ (0 RBI, 1 run) = 1 RBI, 1 run
        # Player2: HR* (1 RBI, 1 run), F4 (0 RBI, 0 run) = 1 RBI, 1 run
        # Total: 2 RBI, 2 runs - still equal

        # To make unequal: add more RBIs without runs
        csv_content = """Player Name,Attempt1,Attempt2
Player1,2B*,1B
Player2,HR*,F4+
"""
        # Player1: 2B* (1 RBI, 0 runs), 1B (0 RBI, 0 runs) = 1 RBI, 0 runs
        # Player2: HR* (1 RBI, 1 run), F4+ (0 RBI, 1 run) = 1 RBI, 2 runs
        # Total: 2 RBI, 2 runs - still equal!

        # Let's make HR without * to trigger assumption
        csv_content = """Player Name,Attempt1,Attempt2
Player1,2B*,1B
Player2,HR,F4+
"""
        # Player1: 2B* (1 RBI, 0 runs), 1B (0 RBI, 0 runs) = 1 RBI, 0 runs
        # Player2: HR (assumed 1 RBI, 1 run), F4+ (0 RBI, 1 run) = 1 RBI, 2 runs
        # Total: 2 RBI, 2 runs - still equal!

        # Need to add more
        csv_content = """Player Name,Attempt1,Attempt2,Attempt3
Player1,2B*,1B,3B
Player2,HR,F4+,K
"""
        # Player1: 2B* (1 RBI, 0 runs), 1B (0 RBI, 0 runs), 3B (0 RBI, 0 runs) = 1 RBI, 0 runs
        # Player2: HR (1 RBI, 1 run), F4+ (0 RBI, 1 run), K (0 RBI, 0 runs) = 1 RBI, 2 runs
        # Total: 2 RBI, 2 runs - still equal!

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
