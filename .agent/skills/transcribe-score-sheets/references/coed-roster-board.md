# Co-ed Roster Board

Use for the handwritten two-column board described by the user on October 1,
2026. Follow the shared CSV contract and validation in [SKILL.md](../SKILL.md).

## Layout and rotation

- Men are listed top-to-bottom on the left; women top-to-bottom on the right.
- Outcomes belong to the name immediately above them and run left-to-right in
  chronological plate-appearance order. Horizontal positions are not innings.
- Batting rotates guy, guy, girl. Advance the men's and women's lists
  independently, wrapping each list when exhausted. Preserve the next group
  slot across innings. Unequal group sizes mean there is no fixed interleaved
  lineup that repeats after every player has batted once.
- Serialize each player once, men in left-column order followed by women in
  right-column order. Record the interleaved chronological sequence separately;
  the CSV stores player appearances, not a global batting-order schedule.
- Confirm starting offsets or skipped/substituted players if evidence conflicts
  with a rotation starting at the top of each column. Do not add appearances to
  make the two groups' counts match.

## Marks and exact results

| Visible mark | Meaning | CSV |
| --- | --- | --- |
| Outcome below the name | That player's plate appearance | Preserve exact result |
| One dot above an outcome | One RBI credited to that batter | Append `*` |
| Multiple dots above an outcome | One RBI per dot | Append one `*` per dot |
| Plus below an outcome | That batter subsequently scored | Append `+` |
| Forward slash next to an outcome | Last batter of the inning; not necessarily the retired runner | Ledger only; omit slash from CSV |
| `HPO` | Hit Pitcher Out: automatic out for hitting the pitcher | `HPO` |
| `HRO` | Home Run Out: home run beyond the team's allowed limit | `HRO` |

For example, a double with two dots above and a plus below becomes `2B**+`.
Read RBI dots and run plus signs independently. A plus on a fielding sequence
can describe a batter who reached on a fielder's choice and later scored;
do not remove it just because the parser classifies the sequence as a non-hit.
`HPO` and `HRO` are supported outs with zero bases, not hits or home runs.
Do not turn `HRO` into `HR` or award automatic HR runs/RBIs. Do not invent these
labels when the photograph shows an ordinary fielding result.

## Inning endings and run limits

The user confirms that a forward slash marks the last plate appearance of an
inning. Resume at the next guy-guy-girl slot, preserving both roster offsets.
The inning can end on a baserunner being tagged out during a hit. Preserve the
batter's hit and the runner's earlier reaching result; record the runner out
separately and do not award a run to a runner retired at home.

Initial innings have a seven-run limit. A home run can carry the inning beyond
seven when the runners scoring on that home run exceed the remaining allowance;
retain the actual runs and RBIs rather than truncating them. The final inning
has unlimited runs. Confirm which inning was declared final when it affects
reconstruction. Do not assume every inning must end with three outs: a capped
inning may end upon reaching the limit. An HRO remains an out and does not
qualify for the scoring-home-run exception.

Use slashes, runner outs, and confirmed run-limit endings together. Missing
slashes or inconsistent marks should be documented rather than silently fixed.

## Inspection and reconciliation

1. Inventory both name columns and record each appearance, dot count, and plus
   independently. Distinguish marker dots from scratches, printed lines, and
   strokes belonging to nearby names. Review questionable marks at full detail.
2. Reinspect every out label. Preserve `L6`, `F1`, `F8`, `F7`, `1-3`, `5-4`,
   `5-3`, `6-3`, `6-4`, and `K` when actually supported by the source; these are
   examples, not default interpretations of unclear writing.
3. Construct the independent-list rotation and compare counts with the photo.
   Use forward slashes as inning endpoints, including hits during which a
   runner makes the final out. Reconcile run-limit endings separately from outs.
4. Sum visible run plus signs and RBI dots separately. Compare with any supplied
   final score. If totals differ, revisit ambiguous marks without adding credits
   solely to balance. Ask a focused question and retain a draft when unresolved.
5. Record missing inning headings/totals or game-ending information explicitly.
   A supported per-player log is still useful even when innings cannot be
   reconstructed. Keep unresolved scoring in `data/game-log/` until confirmed.

## Source example and checks

`data/game-log/fray-cyclones-lsu-05_2026_10_01.jpeg` demonstrates seven men and
three women. Its companion review records this game's readings and unresolved
marks; those readings are not blanket confirmation for other games.

Check that seven men and three women cycle independently, dots above results
become RBIs, plus signs below become runs, fielding-result runs survive, and
HPO/HRO remain outs. A dark scratch near an outcome must not become an RBI just
because it would balance the totals. Parser acceptance alone cannot resolve it.

For this source, the user confirmed Alex was thrown out at home during Kyla's
third appearance (the third result in her row, `1B`, not necessarily her third
successful hit). Preserve Alex's preceding double and Kyla's single, record
Alex's runner out separately, and give Alex no run for that appearance.
