---
name: yearly-recap
description: Draft WhatsApp-ready annual softball statistics recaps for Cyclones or Don't Cha Know, combining the requested year's seasons and historical records with team totals and standout players. Use for yearly recaps rather than individual games or single-season wrap-ups.
---

# Yearly recap

Create one finished, copyable WhatsApp message highlighting a team's recorded
statistics across the requested calendar year. For an ongoing year, say
"year to date" or give the latest included date; do not imply the year is over.

Read the relevant shared team context:
[Cyclones](../post-game-recap/references/cyclones.md) or
[Don't Cha Know](../post-game-recap/references/dont-cha-know.md).
Use that team's emoji and branding, current records, and the requested year.

## Establish the annual scope

- Read the application-generated workbook or underlying records using an
  available spreadsheet-reading skill/tool. Do not regenerate outputs unless
  needed and authorized. Activate `softball-stats` before running the application.
- A cumulative Team Total tab may include earlier years. Establish the year
  boundaries and included leagues, teams, seasons and playoff games before
  using it as an annual total. Do not add overlapping cumulative snapshots.
- Add each historical aggregate once. A PDF titled Week 7 Season Totals is a
  cumulative season summary, not just the seventh week's games. Check source
  scope rather than assuming every dated document is a separate game.
- Check whether historical totals already include individual logs. Synthetic
  historical games are import containers; omit game counts and per-game averages
  unless actual historical game counts are known.
- Respect confirmed player aliases in the current inputs (for example, Zack and
  Zach may be one player). Do not merge people based only on similar names.
- Distinguish printed team totals from the sum of named players. Use the user's
  chosen reconciliation and report incomplete coverage briefly. Do not invent
  substitute identities, distribute residuals, or adjust counts while drafting.
- Calculate team rates from summed underlying counts using application definitions,
  not averages of player percentages. Preserve documented unequal runs/RBIs;
  neither number should be silently changed to make them match.

## Choose standout players

Rank players by recorded at-bats for the requested year, highest first. Aim to
include the top 13–15 players, in that order, and show each player's AB alongside
their highlights. Select the cutoff from the actual AB distribution rather than
padding the list to reach a target count.

Inspect adjacent AB counts around the cutoff and compare the gap with nearby
gaps and the main group's workload. Stop before a substantial drop into a
lower-volume group; omit that player and the players below them. Include fewer
than 13 when a clear drop occurs earlier, and do not extend to 14 or 15 when
doing so crosses that drop. Do not impose an arbitrary universal AB minimum or
percentage threshold. For example, a boundary of 79, 67, 43, 37, 26 AB supports
stopping at 67 rather than adding the much lower-volume players to fill slots.
Honor any explicit user-supplied roster or cutoff instead.

Within each selected player's line, highlight full-year production: hits, RBI,
runs, extra-base hits and walks, including verified category-leading counts.
Do not replace a selected player with a lower-AB player merely for a higher
average or a category lead. Do not hardcode names or copy older recap stats.

Check each "team-high" claim and include ties. A high batting average over fewer
at-bats need not displace a player with substantially more annual production.
Rate highlights can supplement counting stats; state the sample when useful.
Declare batting/OPS champions only with an established qualification threshold;
otherwise omit those awards rather than inventing a minimum.

Use measured descriptions such as "walks leader." Walk totals alone do not
establish patience, and batting records do not establish defense, attendance,
effort, wins or championships. Avoid unsupported narrative claims.

## WhatsApp formatting

Return the message in one fenced `text` block. Use single asterisks for bold,
literal `•` bullets for individual highlights, and an emoji on each team-total
and player line. Keep every player on one compact line with **no blank lines
between player bullets**. Separate sections with one blank line. Honor a user's
request for fewer/no emojis. Display AVG/OBP/SLG as `.516` when below one, and
OPS as `1.270`, consistently to three decimals.

Use this structure, adapting or omitting unsupported details:

1. Team emoji, team name, year and "Stats Update" or "Yearly Recap" heading.
2. A short opening stating the included annual/historical scope.
3. Team totals: hits and AVG; runs and RBI; doubles, triples and HR; walks and PA.
4. Top Players by At-Bats: adjacent `• {emoji} *Name:* ...` lines, ordered by AB,
   with each player's AB, verified highlights and clear category-leading claims.
   If the heading states a player count, use the actual selected count.
5. Say "recorded totals" rather than claiming complete coverage. Omit historical
   substitute and missing-record commentary from the WhatsApp message; keep any
   necessary coverage explanation outside it unless the user requests inclusion.
6. Established stats link, when applicable, followed by a short teammate-style
   appreciative close using the team's emoji.

## Stats link and publishing

Read only **Publish the season stats** and **Manual publishing handoff** in the
[post-game recap skill](../post-game-recap/SKILL.md) when a stats link or publishing
handoff is needed. Match the team/league/season in `data/season_links.json`;
an annual recap may point to the latest season workbook when its cumulative tab
contains the requested year's history. Explain which tab has the annual totals.
Ignore punctuation differences only when the same team is established by context.
Never reuse another team's destination or imply that a saved link was refreshed.
Keep manual-upload reminders outside the copyable message. A draft request does
not authorize sending the message or modifying an external spreadsheet.

Before returning, verify totals, player names, AB ranking and cutoff, leaders/ties,
annual boundaries, historical coverage and link scope against the chosen sources.
Check that no low-volume player was added just to reach 13–15. Keep provenance
and publishing notes outside the WhatsApp block. Do not add historical substitute
or missing-record commentary to the team message unless the user requests it.
