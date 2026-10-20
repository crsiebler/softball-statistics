---
name: season-recap
description: Draft WhatsApp-ready softball season wrap-ups for Cyclones or Don't Cha Know with season awards, playoff standouts, team shoutouts, final totals, and optional next-season reminders. Use for end-of-season recaps rather than routine post-game updates.
---

# Season recap

Create a finished, copyable team message in the style of the post-game recap,
centered on the completed season and its ending.

Identify the team, league, and season from the request or labeled sources. Read
the shared team context for [Cyclones](../post-game-recap/references/cyclones.md)
or [Don't Cha Know](../post-game-recap/references/dont-cha-know.md). Ask if the
team or season cannot be resolved. Use current roster data, not names or results
from a style example.

## Establish the facts

- Use supplied season totals, game logs, application-generated workbooks, and
  user narrative. Read spreadsheets through an available matching skill/tool.
  Do not regenerate application outputs unless needed and authorized; activate
  `softball-stats` before running the application.
- Establish whether season totals and awards include playoffs or only the regular
  season. Follow the user's scope or labeled source scope; do not silently mix
  them. If ambiguous and it changes an award or total, ask while drafting the
  unaffected sections. Distinguish playoff-game highlights from season totals.
- Verify the final result, opponent, score, placement, and championship status
  separately. A semifinal loss alone does not establish third place. Use the
  user's account for game context, including disputed calls, without inventing
  mistakes, motives, or explanations for a loss.
- Resolve conflicting counts or omit the affected claim. Calculate aggregate
  rates from summed underlying counts using the application's definitions,
  never by averaging player percentages. Display AVG and OBP as `.572` and OPS
  as `1.298`, to three decimals; preserve the leading digit for rates of 1 or more.

## Season awards and recognition

Use the award categories in the template when supported. Include all tied
leaders with `&` and make clear the count is per player. Omit categories with no
positive or qualifying leader. Do not declare a batting or OPS champion from
an unqualified maximum: use the supplied or established season AB minimum and
show it on both rate-award lines. If no criterion is established, ask for one
or omit those awards pending clarification; do not invent a threshold.

Select roughly 4–8 playoff standouts when playoff data is available. Keep each
player on one line with compact contributions such as `3-for-3, 2 RBI`,
`2-for-2, 2 RBI, 2 runs`, or `double, walk, 2 RBI, 2 runs`. Use `HR`, `RBI`,
`double`, `triple`, and singular `run`/`walk` for one. Omit zero-value stats.
When covering multiple playoff games, label combined totals or use game
subheads so each highlight and result has an unambiguous scope.

For Cyclones, include the women shoutout when the user or roster evidence
identifies the players and supports their contributions. Do not infer gender
from names. Combine meaningful season stats, playoff contributions, and
user-supplied roster support or attendance notes. Label season versus playoff
stats where needed. Check claims such as "team-high" against the full team;
use "among the women" only when that narrower comparison is verified. Do not
fabricate praise or attendance to fill every roster slot. Omit the section
when unsupported or inapplicable; use a general team shoutout if requested.

## Stats link and publishing handoff

Read and follow only the **Publish the season stats** and **Manual publishing
handoff** sections of the shared [post-game recap skill](../post-game-recap/SKILL.md)
for registry lookup, any authorized new-season import, and manual replacement
instructions. Use this skill's season template and award criteria for drafting.

Match `league`, `season`, and `team` in `data/season_links.json`. Reuse established
destinations; a wrap-up does not itself authorize a new upload or replacement.
Never copy a URL from a style example or another season. Omit the link section
if no destination is established. A saved link does not prove the shared sheet
is current. Keep publishing status, a local XLSX link, and any manual update
reminder outside the copyable team message. Do not send or post the recap unless
the user explicitly authorizes that action.

## Message template

Use single asterisks for WhatsApp bold, literal `•` bullets, and blank lines
between sections. This requested format uses the team emoji at the start and
end, plus section and award emojis. Honor an emoji-free request by removing
them; keep surrounding explanations free of emojis. Substitute the braces and
omit unsupported sections rather than returning empty placeholders.

```text
{emoji} *{team} Season Wrap-Up* {emoji}

{One or two result-led sentences about the season ending, with the final score and placement when established.}

{Brief, candid reflection on the final game or season using supplied context.}

🏆 *Season Awards*

🎯 Batting Champion (min. {N} AB): {player(s)} — *{.AVG}*
🏆 RBI Leader: {player(s)} — *{count}*
🏃 Runs Leader: {player(s)} — *{count}*
💥 OPS Leader (min. {N} AB): {player(s)} — *{OPS}*
🚀 Home Run Leader(s): {player(s)} — *{count}*
👀 Walk Leader: {player(s)} — *{count}*

🔥 *Playoff Standouts*
• {player}: *{compact, verified playoff contributions}*
• {player}: {compact, verified playoff contributions}

🌟 *{team} Women Shoutout*
• {player}: {verified season achievement}
• {player}: {verified playoff contribution}
• {player}: {user-supplied contribution or roster support}

We scored *{runs} runs* this season and finished with a *{.AVG} team batting average*. {Brief perspective appropriate to the result.}

📊 *Full stats:*
{established stats URL(s) for this team and season}

⚠️ *Reminder:* {user-supplied next-season action, deadline, and discount details, if applicable}

{Brief appreciative, competitive close.} {emoji}🥎
```

Adapt singular/plural award labels for ties. Mention the season name or award
scope when needed for clarity. Other supported team totals may replace or
supplement runs and AVG, but keep the summary short.

Include a next-season reminder only when supplied or verified for the current
recap. Never reuse "before Monday" or a discount from an example. Resolve a
relative deadline to the intended date when context permits; ask or omit it if
ambiguous. Keep the reminder after the stats link and before the closing.

## Voice and final check

Write as a teammate: candid, appreciative, competitive, and concise. Acknowledge
a painful ending without dwelling on blame; celebrate a confirmed championship
when appropriate. Recognize supported contributions beyond the award winners.
Do not reuse the example's score, third-place finish, disputed play, player
stats, registration offer, or closing promise as facts about another season.

Before returning the message, check that award winners and ties match the chosen
season scope and qualification rule, playoff highlights match the stated games,
shoutout superlatives are accurate, and every total, destination, and deadline
is supported. Deliver the recap in one copyable text block, with any missing-data
or publishing notes separately and briefly.
