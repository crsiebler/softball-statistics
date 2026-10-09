---
name: post-game-recap
description: Draft WhatsApp-ready softball game recaps and season updates for Cyclones or Don't Cha Know using a shared message template, compact player highlights, and season leaders.
---

# Post-game recap

Identify the team from the prompt or labeled logs, then read its short context:
[Cyclones](references/cyclones.md) or [Don't Cha Know](references/dont-cha-know.md).
If unclear, ask which team. Use that team's name and emoji in the shared template below.

## Publish the season stats

Upload only for a new season that does not already have a published stats file.
Resolve the team and season from the current task. Read the application's
[season link registry](../../../data/season_links.json), matching `league`,
`season`, and `team` by name (case-insensitive). The `urls` list supports multiple
destinations. Never substitute another season's link. A missing record does not
prove the season is new: ask whether a sheet already exists before uploading.
Ask early without blocking independent drafting.

Record user-confirmed destinations and verified new imports in this JSON file.
Keep one record per league/season/team and preserve unrelated records. Use the
newly confirmed destination when correcting a mistaken link; keep multiple URLs
only when they are intentional destinations for that season. Do not copy URLs
into team references. From the repository root, validate and retrieve with:

```bash
conda activate softball-stats
softball-stats --list-season-links --league "Fray" --season "Late Summer 2026" --team "Cyclones"
```

- New season: ask whether to upload the application-generated local XLSX to
  Google Drive as a new native Google Sheet and where to place it. Reuse explicit
  authorization and destination details already supplied for this task.
- Use available Google Drive/Sheets tools and their matching skills to import
  the complete XLSX. Do not recreate the workbook by copying individual cells
  or duplicating an older game's tab. Never modify the local generated XLSX.
- Existing season: do not upload a replacement, create a duplicate, overwrite
  cells, duplicate tabs, or use browser automation to replace the spreadsheet
  as part of this skill. Reuse the established season link and remind the user
  to replace the shared spreadsheet manually from the updated local XLSX.
  Request the link only if it is unknown; do not imply the shared copy is current
  without readback verification or user confirmation.
- After a new-season upload, confirm it succeeded and verify the destination
  file's identity and URL before saving the link. Investigate conversion or
  formatting issues only if the upload reports a problem or a discrepancy is
  observed.
- If uploading is declined or unavailable, finish the recap from the supplied
  workbook and report publishing status separately. Never invent a link or
  treat local workbook freshness as evidence that shared stats were updated.

### Manual publishing handoff

Include the saved URL(s) as clickable links in the recap so the user can open
the sheet directly. Outside the copyable team message, identify the local XLSX
and remind the user of the applicable step: replace the shared file for an
existing season, or set Share → General access → Anyone with the link → Viewer
for a newly uploaded season. The user handles these steps; do not change sharing
permissions as part of this skill. A saved URL is a destination, not evidence
that its content is current or that public visibility has been enabled.

## Message template

Emojis are part of the requested recap format. Preserve the team emoji in the
heading and closing, plus the section and season-leader emojis shown below for
each included section or category. If the user requests an emoji-free message,
omit emojis while preserving the remaining format. This formatting requirement
applies to the finished team message, not surrounding explanations or tool updates.

Fill this template from the supplied game logs, season totals, and narrative. Braces are
substitution fields, not text to include in the final message. Omit unsupported sections
and unused highlight lines. Deliver a finished, copyable message.

```text
{emoji} *{team} Post-Game Recap* {emoji}

{Result-led opening with *score* and opponent if supplied. One or two conversational sentences about the night.}

{Brief positive or honest takeaway, emphasizing *team hits*, *runs*, or another meaningful stat when useful.}

🔥 *Game Highlights*
• {player}: *{H}-for-{AB}, HR, {count} doubles, {count} RBI, {count} runs*
• {player}: *{H}-for-{AB}, double, {count} RBI*
• {player}: *{H}-for-{AB}, triple, {count} runs*
• {player}: *{H}-for-{AB}, walk, {count} runs*
• {player}: Hit, walk, {count} runs

📈 *Season Leaders*
🎯 Batting Average (min. {N} AB): {player} — *{.AVG}*
🏆 RBI: {player} — *{count}*
🏃 Runs: {player(s)} — *{count}*
🚀 Home Runs: {player} — *{count}*
💥 OPS (min. {N} AB): {player} — *{OPS}*
👀 Walks: {player(s)} — *{count}*

Through {number} games, we’re hitting *{.AVG} as a team* with *{hits} hits, {runs} runs, {doubles} doubles, and {home runs} home runs*. {Short takeaway.}

📊 *Full stats:*
{verified publishing link or user-supplied link established for this team and season}

{Brief encouraging close.} {emoji}💪
```

## Highlight syntax and variations

- Use literal `•` player bullets and single asterisks for WhatsApp bold. Leave blank
  lines between sections; keep each player's highlight on one line.
- Select standout and supporting contributions, usually 4–8 players. Each line includes
  only that player's actual achievements; the template's stats are optional examples.
- Preserve the examples' compact syntax: `4-for-4, HR, 3 doubles, 3 RBI, 3 runs`,
  `3-for-3, double, 2 RBI`, `Hit, walk, 2 runs`, or `2 walks, RBI, run`.
  Use `HR`, `RBI`, `double`, `triple`, and singular `run`/`walk` for one.
  Omit zero-value stats.
- Bold the whole standout stat line, or just its key contribution:
  `• {player}: 2-for-3, *HR, 2 RBI*`. An occasional `— monster night` fits an
  exceptional performance.
- For doubleheaders, either combine the night's highlights (make that clear) or use
  `*Game 1:*` and `*Game 2:*` beneath the highlights heading. Keep each score tied
  to its game. For playoffs, use `🔥 *Playoff Night Highlights* 🔥` with game subheads.
- Use `{emoji} *{team} Season Update* {emoji}` for season-focused messages.
  For a confirmed championship, the examples' celebratory heading fits:
  `{emoji}🏆 *{SEASON} CHAMPIONS — {TEAM} ARE ON TOP!* 🏆{emoji}`.
- Retain the separate season-leader lines when season totals are available. Show ties
  with `&`, and state the AB minimum for batting average and OPS. Use a supplied
  minimum; otherwise choose a sensible 5 or 10 AB threshold for the sample and apply
  it consistently. Omit categories with no qualifying or positive leader.
- Keep the team summary concise; select meaningful totals such as triples when relevant.
  Place the stats link before the closing, as in the supplied examples.

## Voice and accuracy

Write as a teammate: upbeat, candid, competitive, and concise. Match the result:
“Big bounce-back win,” “Still plenty of positives,” “the bats showed up,” or
“let’s get back after it” when supported. Losses deserve an honest acknowledgment
and a practical, encouraging close. Use supplied anecdotes for light humor; avoid
inventing effort, defensive mistakes, or reasons for the result.

Use current logs for players and stats, and supplied season totals for leaders.
Keep the two teams' data separate. Calculate combined rates from summed counts,
not averaged percentages; display rates to three decimals. If data conflicts,
omit the affected claim or clarify it rather than silently copying a suspect total.
An uncertain score stays uncertain: “run-ruled in Game 2” is enough.
Use the verified publishing link or the user-supplied destination established for
this team and season in the current task. Prefer a newly confirmed destination
over earlier links. Omit the link section if no destination is established.
Do not reuse old opponents, schedules, championships, or stats from style examples.
