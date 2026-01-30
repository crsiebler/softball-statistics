import sqlite3
from unittest.mock import Mock, patch

import pytest

from softball_statistics.models import League, Player, Team
from softball_statistics.repository.sqlite import SQLiteRepository


class TestSQLiteRepository:
    def test_init_creates_database(self):
        """Test that repository initializes and creates database tables."""
        with patch("sqlite3.connect") as mock_connect, patch.object(
            SQLiteRepository, "_create_tables"
        ) as mock_create:
            mock_conn = Mock()
            mock_connect.return_value = mock_conn

            repo = SQLiteRepository(":memory:")

            mock_create.assert_called_once()

    def test_save_and_get_league(self):
        """Test saving and retrieving a league."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            # Mock the cursor to return league data
            mock_cursor.fetchone.return_value = (1, "Test League", "Winter 2024")
            mock_cursor.lastrowid = 1

            repo = SQLiteRepository(":memory:")

            # Test saving
            league = League(id=None, name="Test League", season="Winter 2024")
            saved_id = repo.save_league(league)
            assert saved_id == 1

            # Test getting
            retrieved = repo.get_league(1)
            assert retrieved.id == 1
            assert retrieved.name == "Test League"
            assert retrieved.season == "Winter 2024"

    def test_get_league_not_found(self):
        """Test getting a league that doesn't exist."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchone.return_value = None

            repo = SQLiteRepository(":memory:")
            result = repo.get_league(999)
            assert result is None

    def test_save_and_get_team(self):
        """Test saving and retrieving a team."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchone.return_value = (1, 1, "Cyclones")
            mock_cursor.lastrowid = 1

            repo = SQLiteRepository(":memory:")

            team = Team(id=None, league_id=1, name="Cyclones")
            saved_id = repo.save_team(team)
            assert saved_id == 1

            retrieved = repo.get_team(1)
            assert retrieved.id == 1
            assert retrieved.league_id == 1
            assert retrieved.name == "Cyclones"

    def test_save_and_get_player(self):
        """Test saving and retrieving a player."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchone.return_value = (1, 1, "Anthony")
            mock_cursor.lastrowid = 1

            repo = SQLiteRepository(":memory:")

            player = Player(id=None, team_id=1, name="Anthony")
            saved_id = repo.save_player(player)
            assert saved_id == 1

            retrieved = repo.get_player(1)
            assert retrieved.id == 1
            assert retrieved.team_id == 1
            assert retrieved.name == "Anthony"

    def test_game_exists_true(self):
        """Test checking if a game exists (returns True)."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchone.return_value = (1,)  # Game exists

            repo = SQLiteRepository(":memory:")
            exists = repo.game_exists("fray", "cyclones", "winter", "01")
            assert exists is True

    def test_game_exists_false(self):
        """Test checking if a game exists (returns False)."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchone.return_value = None  # Game doesn't exist

            repo = SQLiteRepository(":memory:")
            exists = repo.game_exists("fray", "cyclones", "winter", "01")
            assert exists is False

    def test_list_leagues(self):
        """Test listing all leagues."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchall.return_value = [
                (1, "League A", "Winter 2024"),
                (2, "League B", "Spring 2024"),
            ]

            repo = SQLiteRepository(":memory:")
            leagues = repo.list_leagues()

            assert len(leagues) == 2
            assert leagues[0].name == "League A"
            assert leagues[1].name == "League B"

    def test_list_teams_by_league(self):
        """Test listing teams for a specific league."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            mock_cursor.fetchall.return_value = [(1, 1, "Team A"), (2, 1, "Team B")]

            repo = SQLiteRepository(":memory:")
            teams = repo.list_teams_by_league(1)

            assert len(teams) == 2
            assert teams[0].name == "Team A"
            assert teams[1].name == "Team B"

    def test_save_parsing_warnings(self):
        """Test saving parsing warnings to the database."""
        with patch.object(SQLiteRepository, "_create_tables"), patch.object(
            SQLiteRepository, "_get_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__ = Mock(return_value=mock_conn)
            mock_get_conn.return_value.__exit__ = Mock(return_value=None)

            repo = SQLiteRepository(":memory:")

            warnings = [
                {
                    "player_name": "John",
                    "row_num": 2,
                    "col_num": 3,
                    "filename": "test.csv",
                    "original_attempt": "hr",
                    "assumption": "HR solo (assumed 1 RBI, 1 run scored)",
                },
                {
                    "player_name": "Jane",
                    "row_num": 3,
                    "col_num": 2,
                    "filename": "test.csv",
                    "original_attempt": "hr*",
                    "assumption": "HR solo (assumed 1 RBI, 1 run scored)",
                },
            ]

            # Test saving warnings
            repo.save_parsing_warnings(warnings)

            # Verify the cursor.execute was called twice (once for each warning)
            assert mock_cursor.execute.call_count == 2

            # Check the SQL and parameters for the first call
            first_call = mock_cursor.execute.call_args_list[0]
            sql = first_call[0][0]
            assert "INSERT INTO parsing_warnings" in sql
            assert (
                "player_name, row_num, col_num, filename, original_attempt, assumption"
                in sql
            )
            assert "VALUES (?, ?, ?, ?, ?, ?)" in sql
            assert first_call[0][1] == (
                "John",
                2,
                3,
                "test.csv",
                "hr",
                "HR solo (assumed 1 RBI, 1 run scored)",
            )

            # Test with empty warnings list
            repo.save_parsing_warnings([])
            # Should not have made additional calls
            assert mock_cursor.execute.call_count == 2
