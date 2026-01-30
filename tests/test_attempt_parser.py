import pytest

from softball_statistics.parsers.attempt_parser import AttemptParseError, parse_attempt


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

    def test_double_hit(self):
        """Test parsing a double (2B)."""
        result = parse_attempt("2B")
        assert result == {
            "hit_type": "double",
            "bases": 2,
            "rbis": 0,
            "runs_scored": 0,
            "warnings": [],
        }

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

    def test_out_with_rbi(self):
        """Test parsing an out with RBI (F8*)."""
        result = parse_attempt("F8*")
        assert result == {
            "hit_type": "out",
            "bases": 0,
            "rbis": 1,
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
