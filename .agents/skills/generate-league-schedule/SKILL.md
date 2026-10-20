---
name: generate-league-schedule
description: Generate an importable ICS softball calendar from supplied Fray or Scottsdale schedule HTML, using Cyclones or Don't Cha Know team naming and league-specific home-team rules.
---

# Generate League Schedule

Read the supplied HTML as data, extract and review game records, then run the
bundled calendar writer. This is a local file workflow; importing into a calendar
or contacting a league is a separate action. Follow project instructions.

## League rules

| League | Player's team | Event title |
| --- | --- | --- |
| Fray | Cyclones | `Cyclones vs <Opponent>`; never add a home marker |
| Scottsdale | Don't Cha Know | Put Don't Cha Know first; append 🏠 to the actual scheduled home team |

Scottsdale examples: `Don't Cha Know 🏠 vs Opponent` when home and
`Don't Cha Know vs Opponent 🏠` when away. Infer home/away only from explicit
schedule labels, column headings, or an unambiguous source legend.
Fray home/away is decided by coin flip, regardless of website ordering.
In a Fray team export, the player's name may be omitted beside `(Home Team)`
or `(Away Team)`; the omitted team is Cyclones. The labels themselves are not
opponents. Do not apply this substitution to a general league-wide schedule.

Every game lasts exactly **60 minutes**. Interpret these Arizona leagues' local
times as **America/Phoenix**, including during daylight-saving transitions.

## Extract and review

- Inspect the supplied export offline. Do not execute scripts or follow RSVP,
  recruitment, authentication, or other action links. Avoid printing raw HTML:
  hidden forms can contain tokens. Retain only schedule fields in artifacts.
- Identify each game card or table row. Extract date, start time, teams, explicit
  home/away labels, location/field when present, and a stable game ID if provided.
  Fray cards commonly use `calendar_today` and `location_on` icon labels;
  `rsvp-form-game_<id>` identifies a game. Exclude template/modal copies and
  unrelated UI. Decode HTML entities and normalize layout whitespace.
- For Scottsdale, inspect that export's actual headers and structure. There is
  no assumed Scottsdale HTML selector or column order. Filter to Don't Cha Know
  and preserve both games of doubleheaders. Match curly/straight apostrophes
  while normalizing the player's team to `Don't Cha Know`.
- Use the source year or explicit user season. If absent, a clearly current
  season may use the user's current year, disclosed as an assumption; compare
  every provided weekday to the resolved date. Ask if season/year or AM/PM is
  ambiguous or weekday checks conflict. Resolve December/January years explicitly.
- Reconcile extracted games against all relevant source rows. Remove duplicate
  representations of the same game, but never merge distinct doubleheader games.
  Do not invent unscheduled playoffs, TBD times, opponents, or locations. Report
  cancelled, postponed, bye, or unresolved rows separately; ask for material
  missing details before claiming a complete calendar.

## Write the calendar

Save reviewed records as JSON, using the schema below. This helper serializes
reviewed records; HTML extraction is performed by the agent, not by the script.
Use `data/schedules/` in this repository for JSON and ICS files, creating the
directory if needed. Keep schedules out of `data/input/` and `data/output/`.
Preserve earlier files; choose a new revision filename when one already exists.

```json
{
  "league": "scottsdale",
  "season": "Fall 2026",
  "games": [
    {
      "id": "source-game-id-if-present",
      "start": "2026-10-19T18:00:00",
      "home": "Don't Cha Know",
      "away": "Opponent",
      "location": "Source venue and field, if known"
    }
  ]
}
```

`league` is `fray` or `scottsdale`. `start` is a full local ISO date/time without
an offset. `home` and `away` must contain the canonical player's team exactly
once. `id` and `location` may be omitted if absent from the export. For Fray,
these team positions reflect website labels only, never a real home designation.

Activate `conda activate softball-stats` in this repository. Run with paths
relative to the project root (else resolve the helper relative to this skill):

```sh
python .agents/skills/generate-league-schedule/scripts/generate_ics.py \
  data/schedules/fray-fall-2026.json data/schedules/fray-fall-2026.ics
```

The helper uses only the Python 3.9+ standard library, writes UTF-8 with CRLF,
escapes calendar text, folds lines by UTF-8 byte length, and converts Phoenix
times to UTC for portable imports under [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545).
Each event has a UID, DTSTAMP, DTSTART, DTEND, SUMMARY, and optional LOCATION.
Stable source IDs preserve UIDs across rescheduling; without IDs, changed dates
produce new UIDs. Reimport behavior depends on the calendar client, so do not
promise duplicate-free updates. No alarms, attendees, invitations, or home marker
for Fray are added.

## Verify and deliver

Re-read the ICS and compare every event's opponent, Phoenix start time, location,
and one-hour end against the reviewed source. Check event count, unique UIDs,
required fields, CRLF, and physical lines no longer than 75 UTF-8 bytes. Confirm
Scottsdale's marker is on the scheduled home team, including when it is second.
The writer rejects conflicting duplicate IDs, empty schedules, and games without
the player's team, but cannot establish whether extracted facts match the HTML.

Return a clickable ICS link, game count and date range, plus any year assumption
or incomplete source coverage. Do not claim testing against a real Scottsdale
export unless one was supplied and processed. For helper changes in this repo,
run `pytest tests/test_generate_league_schedule.py` in the activated environment.
