import os
import tempfile

import pytest

from softball_statistics.parsers.csv_parser import (
    CSVParseError,
    create_database_objects,
    parse_csv_file,
)


class TestCSVParser:
    def test_parse_valid_csv(self):
        """Test parsing a valid CSV file."""
        csv_content = """Player Name,Attempt,Attempt,Attempt
Anthony,1B,2B*,K
Bryce,F4,BB,1B+
"""

        # Create temp directory and file with proper name
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test-team-season-01.csv")

            with open(file_path, "w") as f:
                f.write(csv_content)

            result = parse_csv_file(file_path)

            assert result["metadata"]["league"] == "test"
            assert result["metadata"]["team"] == "team"
            assert result["metadata"]["season"] == "season"
            assert result["metadata"]["game"] == "01"

            assert len(result["player_names"]) == 2
            assert "Anthony" in result["player_names"]
            assert "Bryce" in result["player_names"]

            assert len(result["attempts"]) == 6  # 2 players × 3 attempts each

            # Check first attempt
            attempt1 = result["attempts"][0]
            assert attempt1["player_name"] == "Anthony"
            assert attempt1["hit_type"] == "single"
            assert attempt1["bases"] == 1
            assert attempt1["rbis"] == 0
            assert attempt1["runs_scored"] == 0

            # Check warnings (should be empty for this test)
            assert result["warnings"] == []

    def test_parse_csv_with_complex_attempts(self):
        """Test parsing CSV with complex attempt combinations."""
        csv_content = """Player Name,Attempt,Attempt
Player1,3B*+,HR**,2B
Player2,K+,F8*,BB
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                result = parse_csv_file(f.name)

                assert len(result["attempts"]) == 6

                # Check complex attempts
                hr_attempt = next(
                    a for a in result["attempts"] if a["attempt_raw"] == "HR**"
                )
                assert hr_attempt["hit_type"] == "home_run"
                assert hr_attempt["bases"] == 4
                assert hr_attempt["rbis"] == 2
                assert hr_attempt["runs_scored"] == 0

                triple_attempt = next(
                    a for a in result["attempts"] if a["attempt_raw"] == "3B*+"
                )
                assert triple_attempt["hit_type"] == "triple"
                assert triple_attempt["bases"] == 3
                assert triple_attempt["rbis"] == 1
                assert triple_attempt["runs_scored"] == 1

                # Check warnings (should be empty for this test)
                assert result["warnings"] == []

            finally:
                os.unlink(f.name)

    def test_parse_csv_invalid_filename(self):
        """Test that invalid filename raises error."""
        csv_content = """Player Name,Attempt
Player1,1B
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            try:
                with pytest.raises(CSVParseError, match="Invalid filename format"):
                    parse_csv_file(f.name)
            finally:
                os.unlink(f.name)

    def test_parse_csv_missing_file(self):
        """Test that missing file raises error."""
        with pytest.raises(CSVParseError, match="File not found"):
            parse_csv_file("nonexistent.csv")

    def test_parse_csv_invalid_header(self):
        """Test CSV with invalid header."""
        csv_content = """Name,Attempt
Player1,1B
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                with pytest.raises(
                    CSVParseError, match="First column must be 'Player Name'"
                ):
                    parse_csv_file(f.name)
            finally:
                os.unlink(f.name)

    def test_parse_csv_invalid_attempt(self):
        """Test CSV with invalid attempt notation."""
        csv_content = """Player Name,Attempt
Player1,INVALID
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                with pytest.raises(CSVParseError, match="Unknown attempt notation"):
                    parse_csv_file(f.name)
            finally:
                os.unlink(f.name)

    def test_parse_empty_csv(self):
        """Test CSV with no data."""
        csv_content = """Player Name,Attempt
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                with pytest.raises(CSVParseError, match="No valid attempts found"):
                    parse_csv_file(f.name)
            finally:
                os.unlink(f.name)

    def test_create_database_objects(self):
        """Test creating database objects from parsed data."""
        parsed_data = {
            "metadata": {
                "league": "TestLeague",
                "team": "TestTeam",
                "season": "Winter",
                "game": "01",
            },
            "player_names": ["Player1", "Player2"],
            "attempts": [
                {
                    "player_name": "Player1",
                    "attempt_raw": "1B",
                    "hit_type": "single",
                    "bases": 1,
                    "rbis": 0,
                    "runs_scored": 0,
                },
                {
                    "player_name": "Player2",
                    "attempt_raw": "2B*",
                    "hit_type": "double",
                    "bases": 2,
                    "rbis": 1,
                    "runs_scored": 0,
                },
            ],
        }

        objects = create_database_objects(parsed_data)

        # Check that objects are created with None IDs (to be set by repository)
        assert objects["league"].name == "TestLeague"
        assert objects["league"].id is None
        assert objects["team"].name == "TestTeam"
        assert objects["team"].id is None
        assert objects["team"].league_id is None  # Will be set after league save
        assert len(objects["players"]) == 2
        assert len(objects["attempts"]) == 2

        # Check player names
        player_names = [p.name for p in objects["players"]]
        assert "Player1" in player_names
        assert "Player2" in player_names

    def test_parse_csv_hr_warnings_collection(self):
        """Test that HR parsing warnings are collected from CSV."""
        csv_content = """Player Name,Attempt,Attempt
Player1,HR,HR*
Player2,1B,HR**
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix="_test-team-season-01.csv", delete=False
        ) as f:
            f.write(csv_content)
            f.flush()

            try:
                result = parse_csv_file(f.name)

                # Should have 2 warnings: one for bare HR, one for HR*
                assert len(result["warnings"]) == 2

                # Check first warning (bare HR)
                warning1 = result["warnings"][0]
                assert warning1["player_name"] == "Player1"
                assert warning1["row_num"] == 2
                assert warning1["col_num"] == 2
                assert "test-team-season-01.csv" in warning1["filename"]
                assert warning1["original_attempt"] == "hr"
                assert "HR solo" in warning1["assumption"]

                # Check second warning (HR*)
                warning2 = result["warnings"][1]
                assert warning2["player_name"] == "Player1"
                assert warning2["row_num"] == 2
                assert warning2["col_num"] == 3
                assert warning2["original_attempt"] == "hr*"
                assert "HR solo" in warning2["assumption"]

                # Check that HR** has no warning (explicit RBIs)
                hr_double_star = next(
                    a for a in result["attempts"] if a["attempt_raw"] == "HR**"
                )
                assert hr_double_star["rbis"] == 2

            finally:
                os.unlink(f.name)
