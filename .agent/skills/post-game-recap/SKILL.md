---
name: post-game-recap
description: Draft WhatsApp-ready softball game recaps and season updates for Cyclones or Don't Cha Know using a shared message template, compact player highlights, and season leaders.
---

# Post-game recap

Identify the team from the prompt or labeled logs, then read its short context:
[Cyclones](references/cyclones.md) or [Don't Cha Know](references/dont-cha-know.md).
If unclear, ask which team. Use that team's name and emoji in the shared template below.

## Publish the season stats

When the recap uses an application-generated workbook, check whether publishing
the updated stats is already authorized and whether the destination is known.
Ask early while preparing the recap; do not block independent drafting.

- New season: ask whether to upload the workbook and where to create the shared
  spreadsheet (destination folder, if relevant). Do not create one without approval.
- Existing season: ask whether to update the published stats and request the exact
  Google Sheets or Drive file URL to replace if it is not already established.
  Reuse authorization and destinations supplied for this task; do not ask again.
- Make direction explicit: publish the local XLSX to the shared destination.
  Never replace application-generated local output with a downloaded copy as
  part of the recap workflow.
- Inspect the destination's identity, file type, team, season, and tabs first.
  If it includes other seasons or user-maintained tabs absent from the workbook,
  clarify whether to preserve them or replace the entire workbook before removal.
- Use available Google Drive/Sheets tools and their matching skills. A raw XLSX
  stored in Drive can be replaced in place with a supported file-update action.
  A native Google Sheet requires a supported in-place Sheets update or import
  workflow; do not assume a new-file import replaces an existing spreadsheet.
  Preserve the established file ID, URL, and sharing unless otherwise requested.
- After an authorized upload/update, read back the destination and compare tab
  coverage, latest-game results, season totals, and representative formatting
  with the local source. Report any publishing or verification limitation honestly.
  Do not claim an upload succeeded merely because the local workbook is current.
- Use the verified destination link in the recap. If publishing is declined or
  unavailable, finish the recap from the supplied workbook and report publishing
  status separately; never invent a link or imply the shared copy is updated.

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
