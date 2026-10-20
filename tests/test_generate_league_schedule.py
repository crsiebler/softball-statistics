"""Calendar behavior independent of league HTML presentation."""

import runpy
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents/skills/generate-league-schedule/scripts/generate_ics.py"
)
generate_calendar = runpy.run_path(str(SCRIPT))["generate_calendar"]


@pytest.fixture
def schedule():
    return {
        "league": "fray",
        "season": "Fall 2026",
        "games": [
            {
                "id": "294641",
                "start": "2026-10-22T20:00:00",
                "home": "Cyclones",
                "away": "Enrichment Time",
                "location": "350 E Oak St, Phoenix, AZ 85004",
            }
        ],
    }


def properties(document):
    return document.decode().replace("\r\n ", "").split("\r\n")


@pytest.mark.parametrize("reverse", [False, True])
def test_fray_team_first_and_one_hour_in_phoenix(schedule, reverse):
    game = schedule["games"][0]
    if reverse:
        game["home"], game["away"] = game["away"], game["home"]
    lines = properties(generate_calendar(schedule))
    assert "SUMMARY:Cyclones vs Enrichment Time" in lines
    assert "DTSTART:20261023T030000Z" in lines
    assert "DTEND:20261023T040000Z" in lines
    assert "LOCATION:350 E Oak St\\, Phoenix\\, AZ 85004" in lines
    assert not any("🏠" in line for line in lines)


@pytest.mark.parametrize("home", [True, False])
def test_scottsdale_marks_actual_home_team(schedule, home):
    schedule["league"] = "scottsdale"
    game = schedule["games"][0]
    game["home"], game["away"] = (
        ("Don't Cha Know", "Opponents") if home else ("Opponents", "Don't Cha Know")
    )
    expected = (
        "Don't Cha Know 🏠 vs Opponents" if home else "Don't Cha Know vs Opponents 🏠"
    )
    assert f"SUMMARY:{expected}" in properties(generate_calendar(schedule))


def test_escaping_utf8_folding_and_crlf(schedule):
    opponent = "Équipe 🏠; " * 20 + "A,B\\C\nSecond line"
    schedule["games"][0]["away"] = opponent
    document = generate_calendar(schedule)
    assert document.endswith(b"\r\n")
    assert b"\n" not in document.replace(b"\r\n", b"")
    assert all(len(line) <= 75 for line in document.split(b"\r\n"))
    assert all(line.decode("utf-8") is not None for line in document.split(b"\r\n"))
    unfolded = document.decode().replace("\r\n ", "")
    assert "\\;" in unfolded
    assert "A\\,B\\\\C\\nSecond line" in unfolded


def test_deduplication_and_stable_source_identity(schedule):
    first = properties(generate_calendar(schedule))
    schedule["games"].append(dict(schedule["games"][0]))
    assert properties(generate_calendar(schedule)).count("BEGIN:VEVENT") == 1
    schedule["games"].pop()
    schedule["games"][0]["start"] = "2026-10-29T18:00:00"
    updated = properties(generate_calendar(schedule))
    assert [v for v in first if v.startswith("UID:")] == [
        v for v in updated if v.startswith("UID:")
    ]


@pytest.mark.parametrize(
    "change",
    [
        {"home": "Another team"},
        {"start": "TBD"},
        {"start": "2026-10-22T20:00:00+00:00"},
        {"away": ""},
    ],
)
def test_invalid_games_are_rejected(schedule, change):
    schedule["games"][0].update(change)
    with pytest.raises(ValueError):
        generate_calendar(schedule)


def test_conflicting_source_ids_are_rejected(schedule):
    schedule["games"].append({**schedule["games"][0], "away": "Different team"})
    with pytest.raises(ValueError, match="Conflicting"):
        generate_calendar(schedule)


def test_empty_schedule_is_rejected(schedule):
    schedule["games"] = []
    with pytest.raises(ValueError):
        generate_calendar(schedule)
