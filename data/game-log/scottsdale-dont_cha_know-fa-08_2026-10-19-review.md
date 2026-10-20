# Game 08 transcription review

Status: user corrections received; final ledger below supersedes the preserved initial draft. No import.
Source: `scottsdale-dont_cha_know-fa-08_2026-10-19.jpeg`.
Filename metadata: Scottsdale, Don't Cha Know, Fall 2026, game 08, 2026-10-19.
Visible sheet: home team; Monday 10/19; Horizon, field 1, 9:30. Five innings show runs 0, 0, 2, 0, 1, cumulative 0, 0, 2, 2, 3.
Extraction: visual inspection, no OCR. An attempted sips enlargement produced black inspection images and supplied no usable additional evidence. Source is unchanged.

## Appearance ledger

Physical columns six continue inning five. `out ?` means circled out number without readable fielding notation, not an approved CSV token. No generic-out fallback is authorized. Blank cells and inning-ending slashes are not appearances.

| Player | First appearance | Second appearance | Third appearance | Confidence / unresolved evidence |
| --- | --- | --- | --- | --- |
| Blake | I1: out 1 | I3: 2B, lower-left RBI dot | I5 continuation: F9 candidate, out 1 | Double/RBI high; F9 label medium |
| Pat | I1: 1B, circled 2 | I3: 1B | I5 continuation: SAC, circled 2, lower-left RBI dot | Sacrifice type/fielding detail unresolved; preserve first single despite runner out |
| Skip | I1: 6-4 candidate | I3: SAC, circled 2 | I5 continuation: out 3 | SAC type and third-inning RBI attribution pending |
| Zack | I1: F1 candidate, out 3 | I3: out 3 | — | Name and F1 reading medium |
| Jack | I2: out 1 | I4: out 1 | — | Exact fielding labels absent/unresolved |
| Logan | I2: out 2 | I4: 1B | — | Exact first out label absent/unresolved |
| Josh | I2: 1B | I4: out 2 | — | Fourth-inning out label absent/unresolved |
| Marques | I2: out 3 | I4: 1B | — | Second-inning out label absent/unresolved |
| Mike | I3: 1B, filled diamond | I4: out 3 | — | Run high; out label absent/unresolved |
| Cory | I3: 2B, circled 1 | I5: 1B, filled diamond | — | Preserve double despite runner out; run high |
| Jason | I3: 1B, filled diamond | I5: 1B | — | Run high |

All cells without stated RBI dots or filled diamonds have no observed RBI/run credit. The possible RBI attached to Skip's SAC needs confirmation rather than being added to balance totals.

## Chronological reconstruction

1. Blake out; Pat single; Skip 6-4 (likely force retiring Pat for out 2); Zack F1 out 3. Zero runs.
2. Jack out, Logan out, Josh single, Marques out. Zero runs.
3. Mike single/run, Cory double/runner out 1, Jason single/run, Blake double/RBI, Pat single, Skip SAC/out 2, Zack out 3. Two runs. Candidate RBIs: Blake and Skip; clarify sacrifice and RBI marks independently.
4. Jack out, Logan single, Josh out, Marques single, Mike out. Zero runs.
5. Cory single/run, Jason single; continuation column: Blake F9/out 1, Pat SAC/RBI/out 2, Skip out 3. One run.

Filled diamonds support three runs: Mike, Jason, Cory. One RBI dot appears by Blake's initially misread hit and one by Pat's final sacrifice. A third RBI may belong to Skip's third-inning sacrifice, but it is not confirmed. Written total alone is not sufficient to assign it.

## Required confirmations

- Confirm Skip's third-inning SAC and Pat's fifth-inning SAC are sacrifice flies or bunts, and provide fielding positions/sequences. Literal SAC/SF are unsupported; a confirmed fly with RBI can use F<position>*.
- Confirm third-inning RBI credits: Blake and Skip, one each? Pat's fifth-inning RBI appears marked.
- Confirm first-inning Skip 6-4, Zack F1, and fifth-inning Blake F9 readings.
- Confirm Pat/Zack spellings and that the game ended after five innings.
- Unlabeled batter outs needing exact notation or permission for O: Blake I1; Zack I3; Jack I2/I4; Logan I2; Josh I4; Marques I2; Mike I4; Skip I5.

## Validation

Input contract inspected in filename_parser.py, csv_parser.py, attempt_parser.py, and use_cases/__init__.py. Literal SAC is unsupported. The importer requires equal RBI/run totals; legitimate non-RBI runs must be retained and reported as import blockers. Parser validation withheld because no settled draft CSV exists. No database operations performed.

## Final ledger after user corrections

The preceding sections preserve the initial visual reading and its questions. The user authorizes O for unlabeled outs; requests F8 for the two SAC plays despite uncertainty about the exact fielders; corrects Blake's last out to F8; confirms Skip 6-4 and Zack F1, names, and five-inning endings. F8 on SAC cells is a user-selected representation, not an independently verified fielding position.

The latest user correction confirms Cory singled, advanced to second, then was thrown out at home on Blake’s hit in inning three. His hit is 1B with no run; the earlier double reading is superseded; Blake's later single remains a hit with one RBI scoring Mike (latest user correction supersedes the double reading). Cory's runner out must not become an O appearance.

| Player | Attempt 1 | Attempt 2 | Attempt 3 | RBI | Runs |
| --- | --- | --- | --- | --- | --- |
| Blake | O | 1B* | F8 | 1 | 0 |
| Pat | 1B | 1B | F8* | 1 | 0 |
| Skip | 6-4 | F8* | O | 1 | 0 |
| Zack | F1 | O | — | 0 | 0 |
| Jack | O | O | — | 0 | 0 |
| Logan | O | 1B | — | 0 | 0 |
| Josh | 1B | O | — | 0 | 0 |
| Marques | O | 1B | — | 0 | 0 |
| Mike | 1B+ | O | — | 0 | 1 |
| Cory | 1B | 1B+ | — | 0 | 1 |
| Jason | 1B+ | 1B | — | 0 | 1 |

Final reconciliation: 25 appearances, 11 hits, 11 total bases, zero walks, three RBIs, three runs. Innings: 0, 0, 2, 0, 1. Scorers: Mike, Jason, Cory. RBI credits: Blake (Mike), Skip (Jason), Pat (Cory). User approval of the proposed credits and SAC representation resolves the draft's third-inning RBI question. F8* is interpreted downstream as a sacrifice fly; the source SAC marks and requested representation remain documented here.

Generic O audit: nine total at the unlabeled cells enumerated above. Full-sheet inspection found circled out numbers without recoverable fielding detail, and the user authorized O. Skip's 6-4 is preserved separately; Pat's earlier single remains a single despite his later force out. Cory's single and out at home are separate events. Runner retirements are not additional CSV appearances.

## Final verification

Final CSV parser verification: 25 appearances, 11 players, 11 hits, 12 total bases, 3 RBIs, 3 runs, 9 authorized generic O tokens, zero warnings. Draft and final paths were parsed before the later Cory correction; final path was parsed again after that correction. Scoped pre-commit file checks passed (trailing whitespace, final newline, large-file checks; YAML/Ruff skipped as inapplicable). No import or database operations performed.

## Hit-value audit after latest user correction

Earlier verification totals are historical and superseded by this audit. Reinspected both original photographs and new PIL crops (*-hit-audit-top.png and *-hit-audit-bottom.png). These crops rendered successfully, unlike the earlier sips inspection images. Read the circled printed 1B/2B/3B/HR result separately from drawn basepaths, scored-run shading, and circled out numbers inside the diamond. Later advances do not add hit bases.

Corrected Blake, inning 3, from 2B* to 1B*: circled 1B establishes the single; his later advance to second on Pat’s hit does not count toward total bases. His RBI scoring Mike is retained. Cory’s inning-3 single, advance to second, and out at home on Blake’s hit remain correctly represented as 1B with no run. This was the same initial-hit-versus-advance error, already corrected before this audit.

Every hit checked against the source:

| Player | Inning | Player appearance | Circled initial hit | Final token |
| --- | --- | --- | --- | --- |
| Pat | 1 | 1 | 1B | 1B |
| Josh | 2 | 1 | 1B | 1B |
| Mike | 3 | 1 | 1B | 1B+ |
| Cory | 3 | 1 | 1B | 1B |
| Jason | 3 | 1 | 1B | 1B+ |
| Blake | 3 | 2 | 1B | 1B* |
| Pat | 3 | 2 | 1B | 1B |
| Logan | 4 | 2 | 1B | 1B |
| Marques | 4 | 2 | 1B | 1B |
| Cory | 5 | 2 | 1B | 1B+ |
| Jason | 5 | 2 | 1B | 1B |

All 11 hit values in this game now match the circled singles. No additional hit-value discrepancies found in the supplied two-game scope. Final parser validation: 25 appearances, 11 hits, 11 total bases, 3 RBIs, 3 runs, no warnings. Exact player appearance sequences and all modifiers checked against the corrected ledger. Game 07 inning runs remain 1, 0, 0, 1, 1; Game 08 remains 0, 0, 2, 0, 1. No import performed.
