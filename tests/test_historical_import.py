"""Historical summaries retain source discrepancies without inventing players."""

import pytest

from softball_statistics.parsers.csv_parser import CSVParser
from softball_statistics.repository.sqlite import SQLiteRepository
from softball_statistics.use_cases import ProcessGameUseCase, ValidationError


@pytest.mark.parametrize("season", ["historical", "fa"])
def test_score_discrepancy_is_allowed_only_for_historical_summary(tmp_path, season):
    path = tmp_path / f"scottsdale-dont_cha_know-{season}-01_2026-08-31.csv"
    path.write_text("Player Name,Attempt\nPaul,1B**+\n")
    repo = SQLiteRepository(str(tmp_path / "stats.db"))
    use_case = ProcessGameUseCase(CSVParser(), repo, repo)

    if season == "fa":
        with pytest.raises(ValidationError, match="does not equal run total"):
            use_case.execute(str(path))
        assert repo.list_leagues() == []
    else:
        use_case.execute(str(path))
        with repo._get_connection() as conn:
            assert conn.execute(
                "SELECT SUM(rbis), SUM(runs_scored) FROM plate_appearances"
            ).fetchone() == (2, 1)
