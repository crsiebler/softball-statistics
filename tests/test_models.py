from datetime import date

import pytest

from softball_statistics.models import (
    AtBatAttempt,
    Game,
    League,
    Player,
    PlayerStats,
    Team,
    Week,
)


class TestLeague:
    def test_valid_league(self):
        league = League(id=1, name="Fray League", season="Winter 2024")
        assert league.id == 1
        assert league.name == "Fray League"
        assert league.season == "Winter 2024"

    def test_league_without_id(self):
        league = League(id=None, name="Fray League", season="Winter 2024")
        assert league.id is None

    def test_league_missing_name(self):
        with pytest.raises(ValueError, match="League name and season are required"):
            League(id=1, name="", season="Winter 2024")

    def test_league_missing_season(self):
        with pytest.raises(ValueError, match="League name and season are required"):
            League(id=1, name="Fray League", season="")


class TestTeam:
    def test_valid_team(self):
        team = Team(id=1, league_id=1, name="Cyclones")
        assert team.id == 1
        assert team.league_id == 1
        assert team.name == "Cyclones"

    def test_team_missing_name(self):
        with pytest.raises(ValueError, match="Team name is required"):
            Team(id=1, league_id=1, name="")

    def test_team_invalid_league_id(self):
        # Team can now have None league_id initially (set later)
        team = Team(id=1, league_id=None, name="Cyclones")
        assert team.league_id is None
        assert team.name == "Cyclones"


class TestPlayer:
    def test_valid_player(self):
        player = Player(id=1, team_id=1, name="Anthony")
        assert player.id == 1
        assert player.team_id == 1
        assert player.name == "Anthony"

    def test_player_missing_name(self):
        with pytest.raises(ValueError, match="Player name is required"):
            Player(id=1, team_id=1, name="")

    def test_player_invalid_team_id(self):
        # Player can now have None team_id initially (set later)
        player = Player(id=1, team_id=None, name="Anthony")
        assert player.team_id is None
        assert player.name == "Anthony"


class TestWeek:
    def test_valid_week(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 7)
        week = Week(id=1, league_id=1, week_number=1, start_date=start, end_date=end)
        assert week.id == 1
        assert week.league_id == 1
        assert week.week_number == 1
        assert week.start_date == start
        assert week.end_date == end

    def test_week_invalid_week_number(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 7)
        with pytest.raises(ValueError, match="Week number must be positive"):
            Week(id=1, league_id=1, week_number=0, start_date=start, end_date=end)

    def test_week_start_after_end(self):
        start = date(2024, 1, 7)
        end = date(2024, 1, 1)
        with pytest.raises(
            ValueError, match="Start date must be before or equal to end date"
        ):
            Week(id=1, league_id=1, week_number=1, start_date=start, end_date=end)


class TestGame:
    def test_valid_game(self):
        game_date = date(2024, 1, 5)
        game = Game(id=1, week_id=1, team_id=1, date=game_date, opponent_team_id=2)
        assert game.id == 1
        assert game.week_id == 1
        assert game.team_id == 1
        assert game.date == game_date
        assert game.opponent_team_id == 2

    def test_game_without_opponent(self):
        game_date = date(2024, 1, 5)
        game = Game(id=1, week_id=1, team_id=1, date=game_date)
        assert game.opponent_team_id is None

    def test_game_invalid_week_id(self):
        game_date = date(2024, 1, 5)
        with pytest.raises(ValueError, match="week_id must be positive if provided"):
            Game(id=1, week_id=0, team_id=1, date=game_date)


class TestAtBatAttempt:
    def test_valid_attempt(self):
        attempt = AtBatAttempt(
            id=1, player_id=1, game_id=1, outcome="2B*", bases=2, rbis=1, runs_scored=0
        )
        assert attempt.id == 1
        assert attempt.player_id == 1
        assert attempt.game_id == 1
        assert attempt.outcome == "2B*"
        assert attempt.bases == 2
        assert attempt.rbis == 1
        assert attempt.runs_scored == 0

    def test_attempt_missing_outcome(self):
        with pytest.raises(ValueError, match="Outcome is required"):
            AtBatAttempt(id=1, player_id=1, game_id=1, outcome="")

    def test_attempt_invalid_bases(self):
        with pytest.raises(ValueError, match="Bases must be between 0 and 4"):
            AtBatAttempt(id=1, player_id=1, game_id=1, outcome="HR", bases=5)

    def test_attempt_negative_rbis(self):
        with pytest.raises(ValueError, match="RBIs and runs scored cannot be negative"):
            AtBatAttempt(id=1, player_id=1, game_id=1, outcome="1B", rbis=-1)


class TestPlayerStats:
    def test_valid_stats(self):
        stats = PlayerStats(
            player_id=1,
            at_bats=10,
            hits=3,
            singles=2,
            doubles=1,
            triples=0,
            home_runs=0,
            rbis=2,
            runs_scored=1,
            batting_average=0.300,
            on_base_percentage=0.400,
            slugging_percentage=0.350,
            ops=0.750,
        )
        assert stats.player_id == 1
        assert stats.at_bats == 10
        assert stats.hits == 3
        assert stats.batting_average == 0.300

    def test_stats_invalid_player_id(self):
        with pytest.raises(ValueError, match="Valid player_id is required"):
            PlayerStats(player_id=0)

    def test_stats_negative_values(self):
        with pytest.raises(ValueError, match="at_bats cannot be negative"):
            PlayerStats(player_id=1, at_bats=-1)
