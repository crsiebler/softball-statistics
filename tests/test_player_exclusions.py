"""Player exclusions affect summary workbooks without changing stored games."""

import json
from datetime import date

import pytest
from openpyxl import load_workbook

from softball_statistics.cli import CLI
from softball_statistics.exporters.excel_exporter import ExcelExporter, ExcelExportError
from softball_statistics.models import Game, League, PlateAppearance, Player, Team, Week
from softball_statistics.parsers.csv_parser import CSVParser
from softball_statistics.repository.sqlite import SQLiteRepository


@pytest.fixture
def export_setup(tmp_path):
    repo = SQLiteRepository(str(tmp_path / "stats.db"))
    for league, team, season, month in [
        ("Fray", "Cyclones", "Winter 2026", 2),
        ("Fray", "Cyclones", "Spring 2026", 4),
        ("Fray", "Storm", "Spring 2026", 4),
        ("Scottsdale", "Cyclones", "Spring 2026", 4),
    ]:
        league_id = repo.save_league(League(None, league, season))
        team_id = repo.save_team(Team(None, league_id, team))
        day = date(2026, month, 1)
        week_id = repo.save_week(Week(None, league_id, 1, day, day))
        game_id = repo.save_game(Game(None, week_id, team_id, day, 1))
        for name, outcome, bases in [("Alex", "1B", 1), ("Guest", "HR", 4)]:
            player_id = repo.save_player(Player(None, team_id, name))
            repo.save_plate_appearance(
                PlateAppearance(None, player_id, game_id, outcome, bases=bases)
            )
    config = tmp_path / "exclusions.json"
    config.write_text(json.dumps({"version": 1, "players": []}))
    return repo, config


def records(workbook, name):
    rows = workbook[name].iter_rows(values_only=True)
    headers = next(rows)
    return [dict(zip(headers, row)) for row in rows if row[0] is not None]


def run_export(repo, config, tmp_path):
    CLI(repo, repo, CSVParser(), ExcelExporter(repo, config)).run(
        ["--export-only", "--output", str(tmp_path / "stats.xlsx")]
    )


def test_exclude_and_restore_summary_players(export_setup, tmp_path):
    repo, config = export_setup
    config.write_text(
        json.dumps(
            {
                "version": 1,
                "players": [
                    {"league": " fray ", "team": "CYCLONES", "player": "guest"}
                ],
            }
        )
    )
    with repo._get_connection() as conn:
        before = list(conn.iterdump())
    run_export(repo, config, tmp_path)
    with repo._get_connection() as conn:
        assert list(conn.iterdump()) == before
    workbook = load_workbook(tmp_path / "stats-fray-spring_2026.xlsx")
    try:
        for tab, pa in [("Cyclo Total", 2), ("Cyclo Spring 2026 Total", 1)]:
            rows = records(workbook, tab)
            assert [row["Player"] for row in rows] == ["Alex", "TEAM TOTALS"]
            assert (rows[-1]["PA"], rows[-1]["H"], rows[-1]["HR"]) == (pa, pa, 0)
            assert rows[-1]["SLG"] == "1.000"
            assert rows[-1]["OPS"] == "2.000"
        assert [r["Player"] for r in records(workbook, "Cyclo Spring 2026 Game 1")] == [
            "Alex",
            "Guest",
            "TEAM TOTALS",
        ]
        assert records(workbook, "Storm Total")[-1]["HR"] == 1
    finally:
        workbook.close()
    other = load_workbook(tmp_path / "stats-scottsdale-spring_2026.xlsx")
    try:
        assert records(other, "Cyclo Total")[-1]["HR"] == 1
    finally:
        other.close()
    config.write_text(json.dumps({"version": 1, "players": []}))
    run_export(repo, config, tmp_path)
    restored = load_workbook(tmp_path / "stats-fray-spring_2026.xlsx")
    try:
        assert records(restored, "Cyclo Total")[-1]["HR"] == 2
        assert records(restored, "Cyclo Total")[-1]["SLG"] == "2.500"
    finally:
        restored.close()


def test_all_players_hidden_keeps_zero_total_tabs(export_setup, tmp_path):
    repo, config = export_setup
    config.write_text(
        json.dumps(
            {
                "version": 1,
                "players": [
                    {"league": "Fray", "team": "Cyclones", "player": name}
                    for name in ("Alex", "Guest")
                ],
            }
        )
    )
    run_export(repo, config, tmp_path)
    workbook = load_workbook(tmp_path / "stats-fray-spring_2026.xlsx")
    try:
        for tab in ("Cyclo Total", "Cyclo Spring 2026 Total"):
            rows = records(workbook, tab)
            assert len(rows) == 1
            assert rows[0]["Player"] == "TEAM TOTALS"
            assert rows[0]["PA"] == 0
            assert rows[0]["OPS"] == "0.000"
        assert len(records(workbook, "Cyclo Spring 2026 Game 1")) == 3
    finally:
        workbook.close()


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"version": 2, "players": []},
        {"version": 1, "players": "Guest"},
        {"version": 1, "players": [{"league": "Fray", "team": "", "player": "Guest"}]},
        {"version": 1, "players": ["Guest"]},
        {
            "version": 1,
            "players": [
                {"league": "Fray", "team": "Cyclones", "player": "Guest"},
                {"league": "fray", "team": "Cyclones", "player": " Guest "},
            ],
        },
        {
            "version": 1,
            "players": [
                {
                    "league": "Fray",
                    "team": "Cyclones",
                    "player": "Guest",
                    "season": "Winter",
                }
            ],
        },
    ],
)
def test_invalid_exclusions_fail_before_writing_workbooks(export_setup, tmp_path, data):
    repo, config = export_setup
    config.write_text(json.dumps(data))
    with pytest.raises(ExcelExportError, match="exclusion"):
        ExcelExporter(repo, config).export({}, str(tmp_path / "stats.xlsx"))
    assert not list(tmp_path.glob("*.xlsx"))


def test_missing_explicit_exclusions_file_is_an_error(export_setup, tmp_path):
    repo, _ = export_setup
    with pytest.raises(ExcelExportError):
        ExcelExporter(repo, tmp_path / "missing.json").export(
            {}, str(tmp_path / "stats.xlsx")
        )


def test_malformed_json_does_not_overwrite_existing_workbooks(export_setup, tmp_path):
    repo, config = export_setup
    run_export(repo, config, tmp_path)
    before = {path.name: path.read_bytes() for path in tmp_path.glob("*.xlsx")}
    config.write_text("{invalid")
    with pytest.raises(ExcelExportError, match="exclusions"):
        ExcelExporter(repo, config).export({}, str(tmp_path / "stats.xlsx"))
    assert {path.name: path.read_bytes() for path in tmp_path.glob("*.xlsx")} == before


def test_export_only_rejects_import_options_before_writing(export_setup, tmp_path):
    repo, config = export_setup
    cli = CLI(repo, repo, CSVParser(), ExcelExporter(repo, config))
    for options in (["--file", "missing.csv"], ["--reparse-all"]):
        with pytest.raises(SystemExit) as exc:
            cli.run(["--export-only", *options])
        assert exc.value.code == 2
    assert not list(tmp_path.glob("*.xlsx"))
