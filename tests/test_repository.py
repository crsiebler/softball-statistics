import pytest

from softball_statistics.models import League
from softball_statistics.repository.sqlite import SQLiteRepository


@pytest.fixture
def repo(tmp_path):
    """Fixture providing a test repository with temp database."""
    db_path = tmp_path / "test.db"
    return SQLiteRepository(str(db_path))


class TestSQLiteRepository:
    def test_init_creates_database(self, repo):
        """Test that repository initializes and creates database tables."""
        # Check that tables exist by trying to query them
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            expected_tables = [
                "leagues",
                "teams",
                "players",
                "weeks",
                "games",
                "plate_appearances",
                "parsing_warnings",
            ]
            for table in expected_tables:
                assert table in tables

    def test_save_and_get_league(self, repo):
        """Test saving and retrieving a league."""
        # Test saving
        league = League(id=None, name="Test League", season="Winter 2024")
        # Since save_league doesn't exist, use the combined repo method
        # Actually, the repo has save_game_data, but for testing, let's use direct SQL or create test data
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                (league.name, league.season),
            )
            cursor.lastrowid

        # Test getting - but get_league doesn't exist, list_leagues does
        leagues = repo.list_leagues()
        retrieved = next((l for l in leagues if l.name == "Test League"), None)
        assert retrieved is not None
        assert retrieved.name == "Test League"
        assert retrieved.season == "Winter 2024"

    def test_get_league_not_found(self, repo):
        """Test getting a league that doesn't exist."""
        leagues = repo.list_leagues()
        assert len(leagues) == 0

    def test_save_and_get_team(self, repo):
        """Test saving and retrieving a team."""
        # First create a league
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("Test League", "Winter 2024"),
            )
            league_id = cursor.lastrowid

            # Save team
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Cyclones"),
            )
            cursor.lastrowid

        # Test listing teams
        teams = repo.list_teams_by_league(league_id)
        assert len(teams) == 1
        assert teams[0].name == "Cyclones"
        assert teams[0].league_id == league_id

    def test_save_and_get_player(self, repo):
        """Test saving and retrieving a player."""
        # Create league and team first
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("Test League", "Winter 2024"),
            )
            league_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Cyclones"),
            )
            team_id = cursor.lastrowid

            # Save player
            cursor.execute(
                "INSERT INTO players (team_id, name) VALUES (?, ?)",
                (team_id, "Anthony"),
            )
            player_id = cursor.lastrowid

        # Test getting player stats (which queries players)
        stats = repo.get_player_stats(player_id)
        # Since no at-bats, stats should be None or zero
        assert stats is None or stats.at_bats == 0

    def test_game_exists_true(self, repo):
        """Test checking if a game exists (returns True)."""
        # Create a game
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("Fray", "Winter 2026"),
            )
            league_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Cyclones"),
            )
            team_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO weeks (league_id, week_number, start_date, end_date) VALUES (?, ?, date('now'), date('now'))",
                (league_id, 1),
            )
            week_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO games (week_id, team_id, game_number, date) VALUES (?, ?, ?, date('now'))",
                (week_id, team_id, 1),
            )

        exists = repo.game_exists("Fray", "Cyclones", "Winter 2026", "01")
        assert exists is True

    def test_game_exists_false(self, repo):
        """Test checking if a game exists (returns False)."""
        exists = repo.game_exists("Fray", "Cyclones", "Winter 2026", "01")
        assert exists is False

    def test_list_leagues(self, repo):
        """Test listing all leagues."""
        # Create some leagues
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("League A", "Winter 2024"),
            )
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("League B", "Spring 2024"),
            )

        leagues = repo.list_leagues()

        assert len(leagues) == 2
        league_names = [l.name for l in leagues]
        assert "League A" in league_names
        assert "League B" in league_names

    def test_list_teams_by_league(self, repo):
        """Test listing teams for a specific league."""
        # Create league and teams
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("Test League", "Winter 2024"),
            )
            league_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Team A"),
            )
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Team B"),
            )

        teams = repo.list_teams_by_league(league_id)

        assert len(teams) == 2
        team_names = [t.name for t in teams]
        assert "Team A" in team_names
        assert "Team B" in team_names

    def test_save_parsing_warnings(self, repo):
        """Test saving parsing warnings to the database."""
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

        # Verify warnings were saved
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM parsing_warnings")
            count = cursor.fetchone()[0]
            assert count == 2

    def test_home_run_outs_counting(self, repo):
        """Test that HRO outcomes are counted correctly in player stats."""
        # Create league, team, player, week, and game
        with repo._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leagues (name, season) VALUES (?, ?)",
                ("Test League", "Winter 2024"),
            )
            league_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO teams (league_id, name) VALUES (?, ?)",
                (league_id, "Test Team"),
            )
            team_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO players (team_id, name) VALUES (?, ?)",
                (team_id, "Test Player"),
            )
            player_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO weeks (league_id, week_number, start_date, end_date) VALUES (?, ?, date('now'), date('now'))",
                (league_id, 1),
            )
            week_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO games (week_id, team_id, game_number, date) VALUES (?, ?, ?, date('now'))",
                (week_id, team_id, 1),
            )
            game_id = cursor.lastrowid

            # Insert plate appearances: 1 hit, 1 walk, 1 HRO, 1 strikeout
            cursor.execute(
                "INSERT INTO plate_appearances (player_id, game_id, outcome, bases, rbis, runs_scored) VALUES (?, ?, ?, ?, ?, ?)",
                (player_id, game_id, "1B", 1, 0, 0),  # Single
            )
            cursor.execute(
                "INSERT INTO plate_appearances (player_id, game_id, outcome, bases, rbis, runs_scored) VALUES (?, ?, ?, ?, ?, ?)",
                (player_id, game_id, "BB", 0, 0, 0),  # Walk
            )
            cursor.execute(
                "INSERT INTO plate_appearances (player_id, game_id, outcome, bases, rbis, runs_scored) VALUES (?, ?, ?, ?, ?, ?)",
                (player_id, game_id, "HRO", 0, 0, 0),  # Home Run Out
            )
            cursor.execute(
                "INSERT INTO plate_appearances (player_id, game_id, outcome, bases, rbis, runs_scored) VALUES (?, ?, ?, ?, ?, ?)",
                (player_id, game_id, "K", 0, 0, 0),  # Strikeout
            )

        # Get player stats
        stats = repo.get_player_stats(player_id)

        # Verify stats
        assert stats is not None
        assert stats.plate_appearances == 4
        assert stats.at_bats == 3  # 4 PA - 1 BB = 3 AB
        assert stats.hits == 1
        assert stats.walks == 1
        assert stats.home_run_outs == 1  # HRO should be counted
