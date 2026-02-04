import pytest

from softball_statistics.parsers.attempt_parser import (
    AttemptParseError,
    _is_fly_ball,
    _is_ground_ball,
    _is_other_out,
    _is_simple_fielding,
    parse_attempt,
)


class TestAttemptParser:
    def test_single_hit(self):
        """Test parsing a single (1B)."""
        result = parse_attempt("1B")
        assert result == {
            "hit_type": "single",
            "bases": 1,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }


class TestIsOutNotation:
    @pytest.mark.parametrize("attempt", ["F1", "F9", "F10", "f1", "f10"])
    def test_is_fly_ball_valid(self, attempt):
        assert _is_fly_ball(attempt) is True

    @pytest.mark.parametrize("attempt", ["F11", "F0", "F", "f11", "G1"])
    def test_is_fly_ball_invalid(self, attempt):
        assert _is_fly_ball(attempt) is False

    @pytest.mark.parametrize("attempt", ["5-1", "4-6-3", "10-10", "1-2-3-4"])
    def test_is_ground_ball_valid(self, attempt):
        assert _is_ground_ball(attempt) is True

    @pytest.mark.parametrize(
        "attempt", ["11-1", "1-11", "4-6-11", "5", "1-2-3-11", "a-1"]
    )
    def test_is_ground_ball_invalid(self, attempt):
        assert _is_ground_ball(attempt) is False

    @pytest.mark.parametrize("attempt", ["1", "5", "9"])
    def test_is_simple_fielding_valid(self, attempt):
        assert _is_simple_fielding(attempt) is True

    @pytest.mark.parametrize("attempt", ["11", "0", "5-1", "F5"])
    def test_is_simple_fielding_invalid(self, attempt):
        assert _is_simple_fielding(attempt) is False

    @pytest.mark.parametrize("attempt", ["A1", "P3", "P10"])
    def test_is_other_out_valid(self, attempt):
        assert _is_other_out(attempt) is True

    @pytest.mark.parametrize("attempt", ["A11", "A0", "A123", "A", "11", "B11"])
    def test_is_other_out_invalid(self, attempt):
        assert _is_other_out(attempt) is False

    def test_triple_hit(self):
        """Test parsing a triple (3B)."""
        result = parse_attempt("3B")
        assert result == {
            "hit_type": "triple",
            "bases": 3,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_home_run_hit(self):
        """Test parsing a home run (HR)."""
        result = parse_attempt("HR")
        expected = {
            "hit_type": "home_run",
            "bases": 4,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [
                {
                    "player_name": "",
                    "row_num": 0,
                    "col_num": 0,
                    "filename": "",
                    "original_attempt": "hr",
                    "assumption": "HR solo (assumed 1 RBI, 1 run scored)",
                }
            ],
        }
        assert result == expected

    def test_strikeout(self):
        """Test parsing a strikeout (K)."""
        result = parse_attempt("K")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_simple_out(self):
        """Test parsing a simple out (O)."""
        result = parse_attempt("O")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_walk(self):
        """Test parsing a walk (BB)."""
        result = parse_attempt("BB")
        assert result == {
            "hit_type": "walk",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_out_with_fly_ball(self):
        """Test parsing an out (F4)."""
        result = parse_attempt("F4")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_out_with_ground_ball(self):
        """Test parsing an out (5-1)."""
        result = parse_attempt("5-1")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_single_with_rbi(self):
        """Test parsing a single with RBI (1B*)."""
        result = parse_attempt("1B*")
        assert result == {
            "hit_type": "single",
            "bases": 1,
            "rbis": 1,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_double_with_runs_scored(self):
        """Test parsing a double with runs scored (2B+)."""
        result = parse_attempt("2B+")
        assert result == {
            "hit_type": "double",
            "bases": 2,
            "rbis": 0,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_triple_with_multiple_modifiers(self):
        """Test parsing a triple with both RBI and runs scored (3B*+)."""
        result = parse_attempt("3B*+")
        assert result == {
            "hit_type": "triple",
            "bases": 3,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_home_run_with_multiple_rbis(self):
        """Test parsing a home run with multiple RBIs (HR**)."""
        result = parse_attempt("HR**")
        assert result == {
            "hit_type": "home_run",
            "bases": 4,
            "rbis": 2,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_walk_with_runs_scored(self):
        """Test parsing a walk with runs scored (BB+)."""
        result = parse_attempt("BB+")
        assert result == {
            "hit_type": "walk",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_strikeout_with_runs_scored(self):
        """Test parsing a strikeout with runs scored (K+)."""
        result = parse_attempt("K+")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_simple_out_with_rbi(self):
        """Test parsing a simple out with RBI (O*)."""
        result = parse_attempt("O*")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 1,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_simple_out_with_runs_scored(self):
        """Test parsing a simple out with runs scored (O+)."""
        result = parse_attempt("O+")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_simple_out_with_multiple_modifiers(self):
        """Test parsing a simple out with both RBI and runs scored (O*+)."""
        result = parse_attempt("O*+")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [],
        }

    def test_out_with_fly_ball_f10(self):
        """Test parsing an out with F10 (right fielder in softball)."""
        result = parse_attempt("F10")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_out_with_fly_ball_f10_rbi(self):
        """Test parsing an out with F10 and RBI (F10*)."""
        result = parse_attempt("F10*")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 1,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_ground_ball_10_1(self):
        """Test parsing a ground ball to position 10 throwing to 1."""
        result = parse_attempt("10-1")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_special_out_hpo(self):
        """Test parsing hit to pitcher out (HPO)."""
        result = parse_attempt("HPO")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_special_out_fo(self):
        """Test parsing foul out (FO)."""
        result = parse_attempt("FO")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_special_out_hro(self):
        """Test parsing home run out (HRO)."""
        result = parse_attempt("HRO")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    @pytest.mark.parametrize(
        "invalid_attempt",
        [
            "",  # Empty string
            "*",  # Just modifiers
            "+",  # Just modifiers
            "1C",  # Invalid hit type
            "4B",  # Invalid bases
            "1B++",  # Too many + modifiers
            "HR*****",  # Too many * modifiers for HR (should fail)
            "1B!*",  # Invalid modifier
            "AB",  # Looks like walk but invalid
            "F11",  # Invalid fly ball position (>10)
            "11-1",  # Invalid ground ball position (>10)
            "A11",  # Invalid other notation position (>10)
            "11",  # Invalid simple fielding position (>10)
        ],
    )
    def test_invalid_attempts(self, invalid_attempt):
        """Test that invalid attempts raise AttemptParseError."""
        with pytest.raises(AttemptParseError):
            parse_attempt(invalid_attempt)

    def test_hr_too_many_rbis(self):
        """Test that HR with 5+ RBIs raises error."""
        # HR**** has 4 RBIs, should be ok
        result = parse_attempt("HR****")
        assert result["rbis"] == 4

        # But HR***** has 5 RBIs, should fail
        with pytest.raises(
            AttemptParseError, match="Home runs cannot have more than 4 RBIs"
        ):
            parse_attempt("HR*****")

    def test_hr_solo_with_star(self):
        """Test HR* generates warning about solo assumption."""
        result = parse_attempt(
            "HR*", player_name="John", row_num=2, col_num=3, filename="test.csv"
        )
        expected = {
            "hit_type": "home_run",
            "bases": 4,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [
                {
                    "player_name": "John",
                    "row_num": 2,
                    "col_num": 3,
                    "filename": "test.csv",
                    "original_attempt": "hr*",
                    "assumption": "HR solo (assumed 1 RBI, 1 run scored)",
                }
            ],
        }
        assert result == expected

    def test_ground_ball_multi_position(self):
        """Test parsing a multi-position ground ball (4-6-3)."""
        result = parse_attempt("4-6-3")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

    def test_case_insensitive(self):
        """Test that parsing is case insensitive."""
        result = parse_attempt("HR*+")
        expected = {
            "hit_type": "home_run",
            "bases": 4,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [],
        }
        assert result == expected

    def test_whitespace_handling(self):
        """Test that whitespace is handled properly."""
        result = parse_attempt(" 1B * + ")
        assert result == {
            "hit_type": "single",
            "bases": 1,
            "rbis": 1,
            "runs_scored": 1,
            "warnings": [],
        }
