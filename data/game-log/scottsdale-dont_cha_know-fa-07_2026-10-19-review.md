# Game 07 transcription review

Status: user corrections received; final ledger below supersedes the preserved initial draft. No import.
Source: `scottsdale-dont_cha_know-fa-07_2026-10-19.jpeg`.
Filename metadata: Scottsdale, Don't Cha Know, Fall 2026, game 07, 2026-10-19.
Visible sheet: visitor team; five occupied inning columns; written runs 1, 0, 0, 1, 1 (total 3).
Extraction: visual inspection, no OCR. An attempted sips enlargement produced black inspection images and supplied no usable additional evidence. Source is unchanged.

## Appearance ledger

Entries are listed by physical inning column, preserving the batting order. `out ?` means a circled out number without a readable fielding label; it is not an approved CSV token. No generic-out fallback is authorized. Blank cells, including inning-ending slashes crossing the next row's printed BB, are not appearances.

| Player | First appearance | Second appearance | Third appearance | Confidence / unresolved evidence |
| --- | --- | --- | --- | --- |
| Josh | I1: out 1 | I3: FC, circled 2 | I5: out 1 | FC visible; fielding sequence and runner interpretation unresolved |
| Marques | I1: 1B, filled diamond | I3: FC, circled 3 | I5: 1B, lower-left RBI dot candidate | Run high; fifth-inning RBI medium |
| Mike | I1: out 2 | I3: FC, inning-ending slash | I5: 1B | FC visible, no supported numeric sequence |
| Cory | I1: 1B, one lower-left RBI dot | I4: out 1 | I5: out 2 | First RBI high; unlabeled outs unresolved |
| Jason | I1: out 3 | I4: 1B with circled 2 | I5: out 3 | Preserve fourth-inning single despite runner out |
| Blake | I2: out 1 | I4: 1B, filled diamond | I5: possible BB | Final BB circle versus adjacent slash requires confirmation |
| Pat | I2: 2B | I4: 1B | — | No clear RBI dot on fourth-inning single |
| Skip | I2: out 2 | I4: 1B, one lower-left RBI dot | — | Fourth-inning RBI medium/high |
| Zack | I2: 1B | I4: out 3 | — | Name reads Zack; spelling unconfirmed |
| Jack | I2: out 3 | I5: 1B with run-mark candidate | — | Fifth-inning run appears outlined rather than filled; written total supports one run but is not attribution proof |
| Logan | I3: BB, circled 1 | I5: 1B | — | Preserve walk despite runner out |

All cells without stated RBI dots or filled diamonds have no observed RBI/run credit; uncertain marks above remain pending.

## Chronological reconstruction

1. Josh, Marques, Mike, Cory, Jason: one run, Marques; Cory RBI.
2. Blake, Pat, Skip, Zack, Jack: zero runs.
3. Logan BB; Josh FC; Marques FC; Mike FC. The circled outs on Logan/Josh/Marques suggest successive runner retirements. Confirm this sequence and approved fielding notation for all three FC results.
4. Cory, Jason, Blake, Pat, Skip, Zack: one run, Blake; Skip RBI candidate. Jason's circled 2 is a runner out after a single.
5. Jack, Logan, Josh, Marques, Mike, Cory, Jason, possible Blake BB. Jack run and Marques RBI are candidates. A Blake appearance after Jason's third out would conflict with the apparent inning ending; do not serialize it without clarification.

Provisional reconciliation: three runs (Marques, Blake, Jack) and three RBIs (Cory, Skip, Marques), subject to the specific marks above. Written cumulative runs: 1, 1, 1, 2, 3. Unplayed later innings are not recorded as zeros.

## Required confirmations

- Is the final Blake BB a real appearance, or just the preceding inning-ending slash? If real, clarify the fifth-inning ending/order.
- Confirm third-inning BB/FC sequence, who was retired, and fielding sequences or an explicit supported representation for FC.
- Confirm Jack scored in the fifth, and Marques drove him in.
- Confirm Zack spelling and that the game ended after five innings.
- Unlabeled batter outs needing exact notation or permission for O: Josh I1/I5; Mike I1; Cory I4/I5; Jason I1/I5; Blake I2; Skip I2; Zack I4; Jack I2.

## Validation

Input contract inspected in filename_parser.py, csv_parser.py, attempt_parser.py, and use_cases/__init__.py. FC is not a supported literal token. The importer requires equal RBI/run totals, independently of parser acceptance. Parser validation withheld because no settled draft CSV exists. No database operations performed.

## Final ledger after user corrections

The preceding sections preserve the initial visual reading and its questions. The user's replies authorize O for unlabeled plays, correct the fifth-inning RBI to Mike (bases loaded, one run), and confirm names and five-inning endings. Game 07's three FC cells use O under the user's answer to the specific FC-notation question; no fielding sequence is invented. These non-hit outcomes do not mean the batter was the retired runner.

| Player | Attempt 1 | Attempt 2 | Attempt 3 | RBI | Runs |
| --- | --- | --- | --- | --- | --- |
| Josh | O | O | O | 0 | 0 |
| Marques | 1B+ | O | 1B | 0 | 1 |
| Mike | O | O | 1B* | 1 | 0 |
| Cory | 1B* | O | O | 1 | 0 |
| Jason | O | 1B | O | 0 | 0 |
| Blake | O | O+ | — | 0 | 1 |
| Pat | 1B | 1B | — | 0 | 0 |
| Skip | O | 1B* | — | 1 | 0 |
| Zack | 1B | O | — | 0 | 0 |
| Jack | O | 1B+ | — | 0 | 1 |
| Logan | BB | 1B | — | 0 | 0 |

Final reconciliation: 27 appearances, 11 hits, 11 total bases, one walk, three RBIs, three runs. Innings: 1, 0, 0, 1, 1. Scorers: Marques, Blake, Jack. RBI credits: Cory, Skip, Mike. Jack's run occurs on Mike's fifth-inning hit, not Marques's. Blake has no third appearance: the apparent BB is treated as the inning-ending slash following Jason's third out, consistent with the confirmed five-inning ending.

Generic O audit: 15 O-based outcomes (14 O and one O+), comprising the 11 unlabeled batter-out cells enumerated above, the three third-inning FC cells (Josh, Marques, Mike), and Blake’s fourth-inning FC/run. The latest user correction confirms Blake reached on a fielder’s choice, not a single; O+ retains his run without crediting a hit. Jason’s earlier single remains unchanged; his runner out is separate from that hit. Full-sheet inspection found no supported numeric fielding sequences. The user authorized the fallback. Logan's walk and Jason's single remain reaching outcomes despite later runner outs. Exact retirement sequences are not encoded by these CSVs.

## Previous verification, before Blake correction

Final CSV parser verification: 27 appearances, 11 players, 12 hits, 13 total bases, 3 RBIs, 3 runs, 14 authorized generic O tokens, zero warnings. Draft and final paths were parsed before the later Cory correction; final path was parsed again after that correction. Scoped pre-commit file checks passed (trailing whitespace, final newline, large-file checks; YAML/Ruff skipped as inapplicable). No import or database operations performed.

## Verification after Blake correction

Final CSV parsed successfully: 27 appearances, 11 players, 11 hits, 12 total bases, 3 RBIs, 3 runs, zero warnings. Blake’s appearances are O and O+; his fourth-inning fielder’s choice retains the scored run. No import performed.

## Hit-value audit after latest user correction

Earlier verification totals are historical and superseded by this audit. Reinspected both original photographs and new PIL crops (*-hit-audit-top.png and *-hit-audit-bottom.png). These crops rendered successfully, unlike the earlier sips inspection images. Read the circled printed 1B/2B/3B/HR result separately from drawn basepaths, scored-run shading, and circled out numbers inside the diamond. Later advances do not add hit bases.

Found an additional error: Pat, inning 2, has circled 1B with later advancement; corrected 2B to 1B. Blake’s fourth-inning FC remains O+ per the earlier correction; Logan’s third-inning circled BB remains a walk despite his runner out.

Every hit checked against the source:

| Player | Inning | Player appearance | Circled initial hit | Final token |
| --- | --- | --- | --- | --- |
| Marques | 1 | 1 | 1B | 1B+ |
| Cory | 1 | 1 | 1B | 1B* |
| Pat | 2 | 1 | 1B | 1B |
| Zack | 2 | 1 | 1B | 1B |
| Jason | 4 | 2 | 1B | 1B |
| Pat | 4 | 2 | 1B | 1B |
| Skip | 4 | 2 | 1B | 1B* |
| Jack | 5 | 2 | 1B | 1B+ |
| Logan | 5 | 2 | 1B | 1B |
| Marques | 5 | 3 | 1B | 1B |
| Mike | 5 | 3 | 1B | 1B* |

All 11 hit values in this game now match the circled singles. No additional hit-value discrepancies found in the supplied two-game scope. Final parser validation: 27 appearances, 11 hits, 11 total bases, 3 RBIs, 3 runs, no warnings. Exact player appearance sequences and all modifiers checked against the corrected ledger. Game 07 inning runs remain 1, 0, 0, 1, 1; Game 08 remains 0, 0, 2, 0, 1. No import performed.
