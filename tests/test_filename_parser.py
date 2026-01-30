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
            "league": "Fray",
            "team": "Cyclones",
            "season": "Winter 2026",
            "game": "01",
            "date": None,
        }
        assert result == expected

    def test_filename_with_numbers_in_names(self):
        """Test parsing filename with numbers in league/team names."""
        result = parse_filename("league1-team2-fall-03.csv")
        expected = {
            "league": "League1",
            "team": "Team2",
            "season": "Fall 2026",
            "game": "03",
            "date": None,
        }
        assert result == expected

    def test_filename_with_underscores(self):
        """Test parsing filename with underscores in names."""
        result = parse_filename("big_league-super_team-spring-15.csv")
        expected = {
            "league": "Big League",
            "team": "Super Team",
            "season": "Spring 2026",
            "game": "15",
            "date": None,
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
            "league": "Test League",
            "team": "Test Team",
            "season": "2024 Season 2026",
            "game": "01",
            "date": None,
        }
        assert result == expected

    def test_game_number_with_leading_zero(self):
        """Test that game numbers keep leading zeros."""
        result = parse_filename("league-team-season-001.csv")
        assert result["game"] == "001"
        assert result["league"] == "League"
        assert result["team"] == "Team"
        assert result["season"] == "Season 2026"

    def test_filename_with_date(self):
        """Test parsing filename with date (season should use date year)."""
        result = parse_filename("fray-cyclones-winter-01_2025-03-15.csv")
        expected = {
            "league": "Fray",
            "team": "Cyclones",
            "season": "Winter 2025",
            "game": "01",
            "date": "2025-03-15",
        }
        assert result == expected

    def test_case_sensitivity(self):
        """Test that parsing applies title case transformation regardless of input case."""
        result = parse_filename("FRAY-Cyclones-WINTER-01.csv")
        expected = {
            "league": "Fray",
            "team": "Cyclones",
            "season": "Winter 2026",
            "game": "01",
            "date": None,
        }
        assert result == expected
