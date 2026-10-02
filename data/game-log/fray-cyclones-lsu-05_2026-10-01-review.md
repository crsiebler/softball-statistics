# Fray Cyclones — Late Summer game 05 — October 1, 2026

## Status and provenance

Finalized: all scoring corrections confirmed. Source:
`fray-cyclones-lsu-05_2026_10_01.jpeg`. Extraction was visual, at standard and
original detail; no OCR engine was used. Game identity is from the filename,
with the date normalized to the parser's hyphenated form. No visible date,
opponent, inning headings, or final score appears on the board.

User-confirmed: men left, women right; guy-guy-girl rotation; outcomes below
names; dots above outcomes are RBIs; plus signs below are scored runs. HPO and
HRO are automatic outs; neither appears in this photograph. The user confirmed
16 Cyclones runs. Latest correction: Rafael's first homer earns two RBIs;
Paul's third-appearance double earns none. This supersedes the earlier proposed
RBI for Paul. Both confirmed RBI corrections are included in the draft.

## Appearance ledger

Locations are roster side/row, then appearance number from left to right.
`*` represents a visible dot above and `+` a visible plus below, except Rafael's
first-PA second `*`, which is user-corrected. All outcome labels were re-read separately
from modifiers. Baxter PA 2 and Maggie PA 3 plus signs were added by
user-confirmed reconstruction, not read from the image. Names are visual
readings. No generic `O` fallback was used.

| Location | Player | PA 1 | PA 2 | PA 3 | PA 4 | RBI | Runs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Left 1 | Kap | 1B | F1 | HR*+ | 1B* | 2 | 1 |
| Left 2 | Bryce | 5-4+ | 5-4 | 6-3 | 5-3 | 0 | 1 |
| Left 3 | Baxter | 3B*+ | 2B+ | HR**+ | F8 | 3 | 3 |
| Left 4 | Rafael | HR**+ | HR**+ | 1B | — | 4 | 2 |
| Left 5 | Paul | 1B+ | F8 | 2B+ | — | 0 | 2 |
| Left 6 | Cory | 2B*+ | 2B*+ | 2B*+ | — | 3 | 3 |
| Left 7 | Alex | F7 | 2B* | 1B* | — | 2 | 0 |
| Right 1 | Kyla | L6 | 1B* | 1B | 1B | 1 | 0 |
| Right 2 | Chance | 1-3 | 5-3 | BB+ | K | 0 | 1 |
| Right 3 | Maggie | 2B*+ | 2B+ | 6-4+ | F6 | 1 | 3 |

## Chronological rotation

Provisional start at the top of each list; men and women wrap independently.
Group numbers below are rotation groups, not innings. PA numbers refer to the
player's own appearances. This sequence fits all 36 visible appearances.

| Group | Man | Man | Woman |
| --- | --- | --- | --- |
| 1 | Kap PA 1: `1B` | Bryce PA 1: `5-4+` | Kyla PA 1: `L6` |
| 2 | Baxter PA 1: `3B*+` | Rafael PA 1: `HR**+` | Chance PA 1: `1-3` |
| 3 | Paul PA 1: `1B+` | Cory PA 1: `2B*+` | Maggie PA 1: `2B*+` |
| 4 | Alex PA 1: `F7` | Kap PA 2: `F1` | Kyla PA 2: `1B*` |
| 5 | Bryce PA 2: `5-4` | Baxter PA 2: `2B+` | Chance PA 2: `5-3` |
| 6 | Rafael PA 2: `HR**+` | Paul PA 2: `F8` | Maggie PA 2: `2B+` |
| 7 | Cory PA 2: `2B*+` | Alex PA 2: `2B*` | Kyla PA 3: `1B` |
| 8 | Kap PA 3: `HR*+` | Bryce PA 3: `6-3` | Chance PA 3: `BB+` |
| 9 | Baxter PA 3: `HR**+` | Rafael PA 3: `1B` | Maggie PA 3: `6-4+` |
| 10 | Paul PA 3: `2B+` | Cory PA 3: `2B*+` | Kyla PA 4: `1B` |
| 11 | Alex PA 3: `1B*` | Kap PA 4: `1B*` | Chance PA 4: `K` |
| 12 | Bryce PA 4: `5-3` | Baxter PA 4: `F8` | Maggie PA 4: `F6` |

## Updated reconstruction

Slashes mark inning-ending appearances. Alex's out at home on Kyla PA 3 is
user-confirmed; retain Alex's double and Kyla's single. The second-inning
endpoint on Bryce PA 2 is inferred from outs because no clear slash is visible.

| Candidate inning | Global PAs | Likely scorers | Reconstructed runs / RBIs |
| --- | --- | --- | --- |
| 1 | 1–6 | Bryce, Baxter, Rafael | 3 / 3 |
| 2 | 7–13 | Paul, Cory, Maggie | 3 / 3 |
| 3 | 14–21 | Baxter, Rafael, Maggie, Cory | 4 / 4 |
| 4 | 22–33 | Kap, Chance, Baxter, Maggie, Paul, Cory | 6 / 6 |
| 5 | 34–36 | None | 0 / 0 |

User-confirmed missing run credits: Baxter PA 2 `2B` → `2B+`, and Maggie PA 3
`6-4` → `6-4+`. The user accepted these reconstructed credits and authorized
applying them. Both are included in the final CSV; neither plus was visible
in the photograph.

Baxter's double precedes Rafael's two-RBI homer in inning 3. Baxter is the
natural second scorer. In inning 4, Maggie likely reaches on the force that
retires Rafael. Paul's double advances Maggie without scoring her. Cory's RBI
double scores Maggie while Paul advances to third. Kyla's non-RBI single
leaves Paul at third; Alex's RBI single scores Paul; Kap's RBI single scores
Cory. Kyla is left on base when Chance strikes out. Exact intermediate base
advancement is inferred, but this sequence fits all remaining RBI/run marks.

This produces 3 + 3 + 4 + 6 + 0 = 16. It removes the prior 17-run hypothesis
and the apparent seven-run-cap conflict: inning 4 ends with six runs and the
third out on Chance. No missing run for Kyla is needed.

## Final verification

With `softball-stats` activated, called `parse_csv_file` on the corrected draft,
then moved it to `data/input/fray-cyclones-lsu-05_2026-10-01.csv` and parsed the
final path again. Both results agree: 10 players, 36 appearances, 16 RBIs,
16 runs, zero warnings. Verified exact per-player tokens and appearance order,
and metadata Fray / Cyclones / Late Summer 2026 / game 05 / 2026-10-01.
No database import or workbook generation was performed.

History: the initial claim of 16 visible plus marks was incorrect; validation
found 14. The earlier added Paul RBI was based on the user's initial recollection
and is now explicitly superseded by the Rafael correction. Those errors are not
being counted as source evidence for the two proposed missing plus marks.
