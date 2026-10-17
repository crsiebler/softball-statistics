"""Serialize reviewed league schedule records as an importable calendar."""

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from zoneinfo import ZoneInfo

TEAMS = {"fray": "Cyclones", "scottsdale": "Don't Cha Know"}
PHOENIX = ZoneInfo("America/Phoenix")


def required_text(record: dict, key: str) -> str:
    """Require nonempty text without silently coercing malformed fields."""
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid {key}")
    return value.strip()


def escape_text(value: str) -> str:
    """Escape iCalendar TEXT, including source-provided line breaks."""
    return (
        value.replace("\\", "\\\\")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def fold_line(line: str) -> str:
    """Fold at 75 UTF-8 octets without splitting a Unicode character."""
    parts = []
    current = ""
    size = 0
    for char in line:
        length = len(char.encode("utf-8"))
        if size + length > 75:
            parts.append(current)
            current, size = " ", 1
        current += char
        size += length
    parts.append(current)
    return "\r\n".join(parts)


def event_fields(game: dict, league: str, season: str) -> tuple:
    """Validate a reviewed game and build its stable identity and event data."""
    home = required_text(game, "home")
    away = required_text(game, "away")
    team = TEAMS[league]
    if [home, away].count(team) != 1:
        raise ValueError(f"Each game must contain {team} exactly once")
    start_text = required_text(game, "start")
    start = datetime.fromisoformat(start_text)
    if start.tzinfo is not None or "T" not in start_text:
        raise ValueError("start must be a local ISO date and time without an offset")
    start = start.replace(tzinfo=PHOENIX).astimezone(timezone.utc)
    opponent = away if home == team else home
    summary = f"{team} vs {opponent}"
    if league == "scottsdale":
        summary = (
            f"{team} 🏠 vs {opponent}" if home == team else f"{team} vs {opponent} 🏠"
        )
    location = game.get("location", "")
    if not isinstance(location, str):
        raise ValueError("location must be text")
    game_id = game.get("id")
    if game_id is not None:
        game_id = required_text(game, "id")
    identity = game_id or json.dumps([season, start_text, team, opponent])
    uid = str(uuid5(NAMESPACE_URL, f"softball-schedule:{league}:{identity}"))
    return uid, start, summary, location


def generate_calendar(schedule: dict) -> bytes:
    """Validate schedule records and return an iCalendar document."""
    league = required_text(schedule, "league")
    if league not in TEAMS:
        raise ValueError("league must be fray or scottsdale")
    season = required_text(schedule, "season")
    games = schedule.get("games")
    if not isinstance(games, list) or not games:
        raise ValueError("games must be a nonempty list")
    events = {}
    for game in games:
        if not isinstance(game, dict):
            raise ValueError("Each game must be an object")
        uid, start, summary, location = event_fields(game, league, season)
        event = (start, summary, location)
        if uid in events and events[uid] != event:
            raise ValueError("Conflicting records have the same game identity")
        events[uid] = event
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    title = f"{league.title()} {season} - {TEAMS[league]}"
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Softball Statistics//League Schedule//EN",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{escape_text(title)}",
        "X-WR-TIMEZONE:America/Phoenix",
    ]
    for uid, (start, summary, location) in sorted(
        events.items(), key=lambda item: (item[1][0], item[0])
    ):
        end = start + timedelta(hours=1)
        description = f"{league.title()} - {season}. Times: America/Phoenix."
        if league == "fray":
            description += " Home/away by coin flip."
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{stamp}",
                f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
                f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
                f"SUMMARY:{escape_text(summary)}",
                f"DESCRIPTION:{escape_text(description)}",
            ]
        )
        if location:
            lines.append(f"LOCATION:{escape_text(location)}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return ("\r\n".join(fold_line(line) for line in lines) + "\r\n").encode("utf-8")


def main() -> None:
    """Create a new calendar file without overwriting prior output."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Reviewed schedule JSON")
    parser.add_argument("output", type=Path, help="New .ics path")
    args = parser.parse_args()
    try:
        schedule = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(schedule, dict):
            raise ValueError("Schedule must be a JSON object")
        document = generate_calendar(schedule)
        with args.output.open("xb") as output:
            output.write(document)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Cannot generate calendar: {error}\n")
    count = document.count(b"BEGIN:VEVENT\r\n")
    print(f"Created {args.output} ({count} games; America/Phoenix; 60 minutes each)")


if __name__ == "__main__":
    main()
