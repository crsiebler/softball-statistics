"""
Pure functions for calculating baseball/softball statistics.
"""

from typing import Dict


def calculate_batting_average(hits: int, at_bats: int) -> float:
    """
    Calculate batting average: H / AB

    Args:
        hits: Number of hits
        at_bats: Number of at-bats

    Returns:
        Batting average as a decimal (e.g., 0.300)
    """
    if at_bats == 0:
        return 0.000
    return round(hits / at_bats, 3)


def calculate_obp(hits: int, walks: int, hbp: int, at_bats: int, sf: int) -> float:
    """
    Calculate on-base percentage: (H + BB + HBP) / (AB + BB + HBP + SF)

    Args:
        hits: Number of hits
        walks: Number of walks
        hbp: Number of hit-by-pitches
        at_bats: Number of at-bats
        sf: Number of sacrifice flies

    Returns:
        OBP as a decimal (e.g., 0.350)
    """
    numerator = hits + walks + hbp
    denominator = at_bats + walks + hbp + sf

    if denominator == 0:
        return 0.000
    return round(numerator / denominator, 3)


def calculate_slg(
    singles: int, doubles: int, triples: int, home_runs: int, at_bats: int
) -> float:
    """
    Calculate slugging percentage: Total Bases / AB

    Total Bases = 1B×1 + 2B×2 + 3B×3 + HR×4

    Args:
        singles: Number of singles
        doubles: Number of doubles
        triples: Number of triples
        home_runs: Number of home runs
        at_bats: Number of at-bats

    Returns:
        SLG as a decimal (e.g., 0.450)
    """
    total_bases = (singles * 1) + (doubles * 2) + (triples * 3) + (home_runs * 4)

    if at_bats == 0:
        return 0.000
    return round(total_bases / at_bats, 3)


def calculate_ops(obp: float, slg: float) -> float:
    """
    Calculate on-base plus slugging: OBP + SLG

    Args:
        obp: On-base percentage
        slg: Slugging percentage

    Returns:
        OPS as a decimal (e.g., 0.800)
    """
    return round(obp + slg, 3)


def calculate_batting_stats(
    at_bats: int,
    hits: int,
    singles: int,
    doubles: int,
    triples: int,
    home_runs: int,
    walks: int,
    strikeouts: int,
    rbis: int,
    runs_scored: int,
    hbp: int = 0,
    sf: int = 0,
) -> Dict[str, float]:
    """
    Calculate all batting statistics for a player.

    Args:
        at_bats: Number of at-bats
        hits: Number of hits
        singles: Number of singles
        doubles: Number of doubles
        triples: Number of triples
        home_runs: Number of home runs
        walks: Number of walks
        strikeouts: Number of strikeouts
        rbis: Number of RBIs
        runs_scored: Number of runs scored
        hbp: Number of hit-by-pitches (default 0)
        sf: Number of sacrifice flies (default 0)

    Returns:
        Dictionary with all calculated statistics
    """
    ba = calculate_batting_average(hits, at_bats)
    obp = calculate_obp(hits, walks, hbp, at_bats, sf)
    slg = calculate_slg(singles, doubles, triples, home_runs, at_bats)
    ops = calculate_ops(obp, slg)

    return {
        "at_bats": at_bats,
        "hits": hits,
        "singles": singles,
        "doubles": doubles,
        "triples": triples,
        "home_runs": home_runs,
        "walks": walks,
        "strikeouts": strikeouts,
        "rbis": rbis,
        "runs_scored": runs_scored,
        "batting_average": ba,
        "on_base_percentage": obp,
        "slugging_percentage": slg,
        "ops": ops,
    }
