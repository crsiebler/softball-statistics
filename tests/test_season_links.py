"""Season link lookup uses durable names, independent of imported game IDs."""

import json

import pytest

from softball_statistics.cli import CLI
from softball_statistics.exporters.excel_exporter import ExcelExporter
from softball_statistics.parsers.csv_parser import CSVParser
from softball_statistics.repository.sqlite import SQLiteRepository

URL = "https://docs.google.com/spreadsheets/d/fray-season/edit?usp=sharing"
OTHER_URL = "https://docs.google.com/spreadsheets/d/other-season/edit"


@pytest.fixture
def link_cli(tmp_path):
    repo = SQLiteRepository(str(tmp_path / "stats.db"))
    return CLI(repo, repo, CSVParser(), ExcelExporter(repo))


def write_links(tmp_path, records):
    path = tmp_path / "season-links.json"
    path.write_text(json.dumps({"version": 1, "seasons": records}))
    return str(path)


def record(league="Fray", season="Late Summer 2026", team="Cyclones", urls=None):
    return dict(league=league, season=season, team=team, urls=urls or [URL])


def test_lookup_filters_season_team_and_league(link_cli, tmp_path, capsys):
    path = write_links(
        tmp_path,
        [
            record(urls=[URL, OTHER_URL]),
            record(
                season="Winter 2026",
                urls=["https://docs.google.com/spreadsheets/d/winter/edit"],
            ),
            record(
                league="Other",
                urls=["https://docs.google.com/spreadsheets/d/league/edit"],
            ),
            record(
                team="Other", urls=["https://docs.google.com/spreadsheets/d/team/edit"]
            ),
        ],
    )
    link_cli.run(
        [
            "--list-season-links",
            "--season-links-file",
            path,
            "--league",
            "fray",
            "--season",
            "Late Summer 2026",
            "--team",
            "Cyclones",
        ]
    )
    output = capsys.readouterr().out
    assert URL in output and OTHER_URL in output
    assert (
        "/winter/" not in output and "/league/" not in output and "/team/" not in output
    )


def test_no_matching_season_does_not_reuse_old_link(link_cli, tmp_path, capsys):
    path = write_links(tmp_path, [record()])
    link_cli.run(
        ["--list-season-links", "--season-links-file", path, "--season", "Winter 2027"]
    )
    assert "No season links found" in capsys.readouterr().out


@pytest.mark.parametrize(
    "records",
    [
        [record(), record(league="fray")],
        [record(urls=["javascript:alert(1)"])],
        [record(urls="https://docs.google.com/spreadsheets/d/example/edit")],
        [record(team="")],
    ],
)
def test_invalid_registry_fails_clearly(link_cli, tmp_path, capsys, records):
    path = write_links(tmp_path, records)
    with pytest.raises(SystemExit) as exc:
        link_cli.run(["--list-season-links", "--season-links-file", path])
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().out


def test_missing_registry_reports_path(link_cli, tmp_path, capsys):
    path = str(tmp_path / "missing.json")
    with pytest.raises(SystemExit) as exc:
        link_cli.run(["--list-season-links", "--season-links-file", path])
    assert exc.value.code == 1
    assert path in capsys.readouterr().out
