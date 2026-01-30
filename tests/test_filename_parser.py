import pytest

from softball_statistics.parsers.filename_parser import (
    FilenameParseError,
    parse_filename,
)


class TestFilenameParser:
    def test_valid_filename(self):
        """Test parsing a valid filename."""
        result = parse_filename("fray-cyclones-winter-01.csv")
        expected = {
            "league": "fray",
            "team": "cyclones",
            "season": "winter",
            "game": "01",
        }
        assert result == expected

    def test_filename_with_numbers_in_names(self):
        """Test parsing filename with numbers in league/team names."""
        result = parse_filename("league1-team2-fall-03.csv")
        expected = {
            "league": "league1",
            "team": "team2",
            "season": "fall",
            "game": "03",
        }
        assert result == expected

    def test_filename_with_underscores(self):
        """Test parsing filename with underscores in names."""
        result = parse_filename("big_league-super_team-spring-15.csv")
        expected = {
            "league": "big_league",
            "team": "super_team",
            "season": "spring",
            "game": "15",
        }
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_filename",
        [
            "fray-cyclones-winter.csv",  # Missing game number
            "fray-cyclones-01.csv",  # Missing season
            "fray-winter-01.csv",  # Missing team
            "cyclones-winter-01.csv",  # Missing league
            "fray-cyclones-winter-01.txt",  # Wrong extension
            "fray-cyclones-winter-01",  # No extension
            "",  # Empty string
            "invalid-format.csv",  # Wrong number of parts
            "a-b-c-d-e.csv",  # Too many parts
        ],
    )
    def test_invalid_filenames(self, invalid_filename):
        """Test that invalid filenames raise FilenameParseError."""
        with pytest.raises(FilenameParseError):
            parse_filename(invalid_filename)

    def test_filename_with_special_characters(self):
        """Test parsing filename with special characters."""
        result = parse_filename("test_league-test_team-2024_season-01.csv")
        expected = {
            "league": "test_league",
            "team": "test_team",
            "season": "2024_season",
            "game": "01",
        }
        assert result == expected

    def test_game_number_with_leading_zero(self):
        """Test that game numbers keep leading zeros."""
        result = parse_filename("league-team-season-001.csv")
        assert result["game"] == "001"

    def test_case_sensitivity(self):
        """Test that parsing is case-sensitive (preserves original case)."""
        result = parse_filename("FRAY-Cyclones-WINTER-01.csv")
        expected = {
            "league": "FRAY",
            "team": "Cyclones",
            "season": "WINTER",
            "game": "01",
        }
        assert result == expected
