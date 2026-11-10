"""Reproduce the Cyclones roster history report from the collected source."""

import json
import re
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT / "source.json").read_text())
assumptions = json.loads((ROOT / "revenue_assumptions.json").read_text())
fee = assumptions["fee_per_registration"]
core = set(assumptions["core_players"])
acquisitions = set(assumptions["long_term_acquisitions"])
assert len(core) == 8 and len(acquisitions) == 12 and not core & acquisitions


def player_group(name):
    if name in core:
        return "Core players"
    if name in acquisitions:
        return "Long-term acquisitions"
    return "Other players"


def revenue(registrations):
    return None if fee is None else round(registrations * fee, 2)


def money(amount):
    return "Fee needed" if amount is None else f"${amount:,.2f}"


canonical = json.dumps(source["records"], separators=(",", ":"), ensure_ascii=False)
fingerprint = 2166136261
for character in canonical:
    fingerprint = ((fingerprint ^ ord(character)) * 16777619) & 0xFFFFFFFF
assert (len(canonical), fingerprint) == (8499, 924760690), "Browser export mismatch"

labels = {
    "WT": "Winter", "SP": "Spring", "LSP": "Late Spring", "SU": "Summer",
    "LSU": "Late Summer", "FA": "Fall", "LFA": "Late Fall",
}
seasons = []
for row in source["records"]:
    season = dict(zip(source["columns"], row))
    code, year = re.search(r"- ([A-Z]+)'(\d{2})", season["league_name"]).groups()
    season.update(
        year=2000 + int(year),
        season=labels[code],
        status="Current" if season["season_id"] == source["current_season_id"] else "Past",
        overview_url=f'https://commi.sh/seasons/{season["season_id"]}/overviews',
        roster_url=f'https://commi.sh/seasons/{season["season_id"]}/new_teams_page',
    )
    assert season["listed_player_count"] == len(season["players"])
    assert len(season["players"]) == len(set(season["players"]))
    assert int(season["start_date"][:4]) == season["year"]
    season["estimated_gross_revenue"] = revenue(season["listed_player_count"])
    seasons.append(season)
assert len({season["season_id"] for season in seasons}) == 29
assert [season["start_date"] for season in seasons] == sorted(
    season["start_date"] for season in seasons
)
all_counts = Counter(player for season in seasons for player in season["players"])
past_counts = Counter(
    player for season in seasons if season["status"] == "Past"
    for player in season["players"]
)
players = []
for name, count in sorted(all_counts.items(), key=lambda item: (-item[1], item[0])):
    memberships = [season for season in seasons if name in season["players"]]
    players.append({
        "player": name,
        "group": player_group(name),
        "past_seasons": past_counts[name],
        "current_seasons": count - past_counts[name],
        "total_seasons": count,
        "estimated_gross_revenue": revenue(count),
        "first_season_start": memberships[0]["start_date"],
        "last_season_start": memberships[-1]["start_date"],
        "season_ids": [season["season_id"] for season in memberships],
    })
assert len(players) == 65 and len(past_counts) == 62
assert sum(all_counts.values()) == 398 and sum(past_counts.values()) == 386
assert core | acquisitions <= all_counts.keys()
group_totals = []
for group in ("Core players", "Long-term acquisitions", "Other players"):
    members = [player for player in players if player["group"] == group]
    past = sum(player["past_seasons"] for player in members)
    current = sum(player["current_seasons"] for player in members)
    group_totals.append({
        "group": group,
        "unique_players": len(members),
        "past_registrations": past,
        "current_registrations": current,
        "total_registrations": past + current,
        "past_estimated_revenue": revenue(past),
        "current_estimated_revenue": revenue(current),
        "total_estimated_revenue": revenue(past + current),
    })
assert sum(group["total_registrations"] for group in group_totals) == 398
assert sum(group["past_registrations"] for group in group_totals) == 386
report = {
    "collected_on": source["collected_on"],
    "method": source["method"],
    "revenue_assumptions": assumptions,
    "group_totals": group_totals,
    "summary": {
        "total_seasons": 29, "past_seasons": 28, "current_seasons": 1,
        "unique_listed_players": 65, "unique_past_players": 62,
        "player_season_registrations": 398, "past_player_season_registrations": 386,
        "count_mismatches": 0,
        "past_estimated_gross_revenue": revenue(386),
        "current_estimated_gross_revenue": revenue(12),
        "total_estimated_gross_revenue": revenue(398),
    },
    "seasons": seasons,
    "players": players,
}
(ROOT / "history.json").write_text(json.dumps(report, indent=2) + "\n")


def table(headers, rows):
    """Build a compact HTML table; row cells are already escaped markup."""
    return (
        '<div class="scroll"><table><thead><tr>'
        + "".join(f"<th>{escape(header)}</th>" for header in headers)
        + "</tr></thead><tbody>"
        + "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
        + "</tbody></table></div>"
    )


season_rows = []
for season in seasons:
    season_rows.append([
        str(season["year"]), season["season"], season["start_date"],
        str(season["listed_player_count"]), season["status"],
        money(season["estimated_gross_revenue"]),
        f'<a href="{season["overview_url"]}">{escape(season["league_name"])}</a>',
        '<details><summary>Roster</summary><p>'
        + ", ".join(escape(name) for name in season["players"])
        + f'</p><a href="{season["roster_url"]}">Source roster</a></details>',
    ])
player_rows = []
for player in players:
    memberships = [season for season in seasons if season["season_id"] in player["season_ids"]]
    season_links = "; ".join(
        f'<a href="{season["roster_url"]}">{season["year"]} {season["season"]}</a>'
        for season in memberships
    )
    player_rows.append([
        escape(player["player"]), player["group"], str(player["past_seasons"]),
        str(player["current_seasons"]), str(player["total_seasons"]),
        money(player["estimated_gross_revenue"]),
        player["first_season_start"], player["last_season_start"],
        f'<details><summary>Seasons</summary><p>{season_links}</p></details>',
    ])
html = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cyclones season and player history</title>
<style>
body{font:16px/1.5 system-ui,sans-serif;color:#172b3a;margin:0;background:#f5f7fa}
main{max-width:1440px;margin:auto;padding:32px}h1{margin-bottom:8px}
h2{margin-top:40px}a{color:#165c9b}p{max-width:100ch}.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;background:white;font-size:14px}
th,td{padding:11px 13px;text-align:left;border-bottom:1px solid #dce3e9;vertical-align:top}
th{background:#193b53;color:white;white-space:nowrap}tr:nth-child(even){background:#f0f4f7}
summary{cursor:pointer;white-space:nowrap}details p{min-width:260px;max-width:480px}
nav{display:flex;gap:24px}.facts{font-size:20px;font-weight:600}
@media(max-width:700px){main{padding:16px}}
</style><main>
<h1>Cyclones season and player history</h1>
<p>Collected October 30, 2026 from the signed-in
<a href="https://commi.sh/users/seasons?type=leagues">commi.sh leagues page</a>.</p>
<p class="facts">29 seasons · 65 distinct listed names · 398 player-season registrations</p>
<p>Past seasons: 28, with 62 distinct names and 386 registrations. Current Fall 2026:
12 players, beginning October 22, 2026. Coverage: July 13, 2021–October 22, 2026.</p>
<p>Counts represent registered roster membership, not verified game attendance.
Start dates are the site's listed season start dates. Year and season are decoded from the
league name; LFA means Late Fall. Names retain the site's spelling and capitalization;
possible aliases have not been merged (for example, Bruce Johnson and Bryce Johnson).
Every extracted roster count matches its displayed team total. No duplicate names were
found within any roster.</p>
<nav><a href="#revenue">Registration revenue</a><a href="#seasons">Season history</a><a href="#players">Player tally</a>
<a href="history.json">Structured data</a></nav>
'''
html += '<h2 id="revenue">Estimated PHX Fray registration revenue</h2>'
html += f'<p>Assumed fee per player per season: <strong>{money(fee)}</strong>. '
html += escape(assumptions["scope"]) + ". " + escape(assumptions["revenue_basis"]) + "</p>"
html += '<p>Player groups supplied by the user. ' + escape(assumptions["normalization_note"]) + "</p>"
html += table(
    ["Player group", "Unique players", "Past registrations", "Current registrations", "Total registrations", "Past revenue", "Current revenue", "Total revenue"],
    [[group["group"], str(group["unique_players"]), str(group["past_registrations"]),
      str(group["current_registrations"]), str(group["total_registrations"]),
      money(group["past_estimated_revenue"]), money(group["current_estimated_revenue"]),
      money(group["total_estimated_revenue"])] for group in group_totals]
    + [["All players", "65", "386", "12", "398", money(revenue(386)), money(revenue(12)), money(revenue(398))]],
)
html += '<h2 id="seasons">Season history</h2>'
html += table(["Year", "Season", "Start date", "Players", "Status", "Est. revenue", "League / source", "Roster"], season_rows)
html += '<h2 id="players">Player seasons</h2><p>Ordered by total seasons, then name. Expand a player to see every season.</p>'
html += table(["Player", "Group", "Past", "Current", "Total", "Est. revenue", "First start", "Latest start", "Memberships"], player_rows)
html += "</main></html>\n"
(ROOT / "history.html").write_text(html)
print(json.dumps(report["summary"]))
print(json.dumps(group_totals))
print(f"Source matches browser fingerprint: {fingerprint}")
print("Created history.json and history.html")
