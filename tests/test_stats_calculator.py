import pytest

from softball_statistics.calculators.stats_calculator import (
    calculate_batting_average,
    calculate_batting_stats,
    calculate_obp,
    calculate_ops,
    calculate_slg,
)


class TestStatsCalculator:
    def test_calculate_batting_average(self):
        """Test batting average calculation."""
        assert calculate_batting_average(hits=3, at_bats=10) == 0.300
        assert calculate_batting_average(hits=0, at_bats=5) == 0.000
        assert calculate_batting_average(hits=1, at_bats=1) == 1.000

    def test_calculate_batting_average_zero_at_bats(self):
        """Test batting average with zero at-bats (should return 0.000)."""
        assert calculate_batting_average(hits=0, at_bats=0) == 0.000

    def test_calculate_obp(self):
        """Test on-base percentage calculation."""
        # H=3, BB=2, HBP=0, AB=10, SF=0
        # OBP = (3 + 2 + 0) / (10 + 2 + 0 + 0) = 5/12 = 0.417
        assert calculate_obp(hits=3, walks=2, hbp=0, at_bats=10, sf=0) == 0.417

    def test_calculate_obp_with_hbp_and_sf(self):
        """Test OBP with hit-by-pitches and sacrifice flies."""
        # H=2, BB=1, HBP=1, AB=8, SF=1
        # OBP = (2 + 1 + 1) / (8 + 1 + 1 + 1) = 4/11 ≈ 0.364
        assert calculate_obp(hits=2, walks=1, hbp=1, at_bats=8, sf=1) == pytest.approx(
            0.364, rel=1e-3
        )

    def test_calculate_obp_zero_denominator(self):
        """Test OBP with zero denominator (should return 0.000)."""
        assert calculate_obp(hits=0, walks=0, hbp=0, at_bats=0, sf=0) == 0.000

    def test_calculate_slg(self):
        """Test slugging percentage calculation."""
        # 2 singles, 1 double, 1 triple, 0 HR, 4 AB
        # TB = 2*1 + 1*2 + 1*3 + 0*4 = 2 + 2 + 3 = 7
        # SLG = 7/4 = 1.750
        assert (
            calculate_slg(singles=2, doubles=1, triples=1, home_runs=0, at_bats=4)
            == 1.750
        )

    def test_calculate_slg_with_home_runs(self):
        """Test SLG with home runs."""
        # 1 single, 0 doubles, 0 triples, 2 HR, 4 AB
        # TB = 1*1 + 0*2 + 0*3 + 2*4 = 1 + 8 = 9
        # SLG = 9/4 = 2.250
        assert (
            calculate_slg(singles=1, doubles=0, triples=0, home_runs=2, at_bats=4)
            == 2.250
        )

    def test_calculate_slg_zero_at_bats(self):
        """Test SLG with zero at-bats (should return 0.000)."""
        assert (
            calculate_slg(singles=0, doubles=0, triples=0, home_runs=0, at_bats=0)
            == 0.000
        )

    def test_calculate_ops(self):
        """Test on-base plus slugging calculation."""
        obp = 0.350
        slg = 0.450
        assert calculate_ops(obp=obp, slg=slg) == 0.800

    def test_calculate_batting_stats_complete(self):
        """Test complete batting stats calculation."""
        stats = calculate_batting_stats(
            at_bats=10,
            hits=3,
            singles=2,
            doubles=1,
            triples=0,
            home_runs=0,
            walks=2,
            strikeouts=2,
            rbis=2,
            runs_scored=1,
            hbp=0,
            sf=0,
        )

        expected = {
            "at_bats": 10,
            "hits": 3,
            "singles": 2,
            "doubles": 1,
            "triples": 0,
            "home_runs": 0,
            "walks": 2,
            "strikeouts": 2,
            "rbis": 2,
            "runs_scored": 1,
            "batting_average": 0.300,
            "on_base_percentage": 0.417,  # (3+2+0)/(10+2+0+0) = 5/12
            "slugging_percentage": 0.400,  # (2*1 + 1*2 + 0*3 + 0*4)/10 = 4/10
            "ops": 0.817,  # 0.417 + 0.400
        }

        assert stats == expected

    def test_calculate_batting_stats_perfect_game(self):
        """Test stats for a perfect game scenario."""
        stats = calculate_batting_stats(
            at_bats=4,
            hits=4,
            singles=0,
            doubles=0,
            triples=0,
            home_runs=4,
            walks=0,
            strikeouts=0,
            rbis=8,
            runs_scored=4,
            hbp=0,
            sf=0,
        )

        assert stats["batting_average"] == 1.000
        assert stats["slugging_percentage"] == 4.000  # 4*4/4
        assert stats["ops"] == 5.000  # 1.000 + 4.000

    def test_calculate_batting_stats_zero_stats(self):
        """Test stats calculation with all zeros."""
        stats = calculate_batting_stats(
            at_bats=0,
            hits=0,
            singles=0,
            doubles=0,
            triples=0,
            home_runs=0,
            walks=0,
            strikeouts=0,
            rbis=0,
            runs_scored=0,
            hbp=0,
            sf=0,
        )

        assert stats["batting_average"] == 0.000
        assert stats["on_base_percentage"] == 0.000
        assert stats["slugging_percentage"] == 0.000
        assert stats["ops"] == 0.000
