# Cyclones — October 22, 2026 — transcription review

Status: scoring and notation resolved. Final CSV:
`data/input/fray-cyclones-fa-01_2026-10-22.csv`. No import performed by the agent.
Final parser and file-check verification is recorded below.

Source: `fray-cyclones-fa-01_2026-10-22.jpeg`, inspected visually at default and
original detail. No OCR, external upload, or image modification was used.
All locations below refer to that photograph. Appearance numbers count visible
results left-to-right beneath each name, not innings.

Filename metadata: Fray / Cyclones / Fall 2026 / game 01 / 2026-10-22.
User-confirmed result: Cyclones won 15–14. This score is not written on the board.
The source ledger retains board labels for traceability. User-confirmed identity
mapping: board `Dad` is existing player **Bryce**; board `Bryce` is **Garroway**.
The CSV uses these confirmed names. `Kap` remains the board label.

## User confirmations and current reconciliation

- Guy–guy–girl rotation confirmed; no substitutions.
- The opening inning ended at the seven-run limit. In response to the proposed
  final play, the user confirmed the board's Bryce drove in the last run. With
  the identity correction, record **Garroway appearance 1: `1B*`**, scoring Bryce
  (board Dad). This supplies one missing RBI; Bryce already has a run mark.
- **Kap's third single was the walk-off, scoring Cory and then Paul.** Preserve
  Kap's two visible RBI dots and Cory's already marked third-appearance run.
- Paul walked in his final appearance and scored on Kap's walk-off: add `BB+`
  as Paul's third appearance, independently of his earlier single and home run.
- Bryce (board Dad) lined out to shortstop in his final appearance: add `L6`
  as his third appearance. Kyla's fourth single preceded that lineout.
- Chance was on deck after Kap and never batted again. Exclude the apparent
  fourth `F6` from the CSV; retain its original visual reading below for history.
- Alex had a third appearance ending the inning before the final inning.
  The user first described it as `6`, then recalled "two 5" results, explaining
  that third base fielded the ball and forced a runner at third. On follow-up,
  the user initially confirmed both outs were by the third baseman. That earlier
  correction was superseded for appearance 2: Alex did not get out in the second
  inning and instead had a hit scoring Stephen. Appearance 3 remains `5`.
  A force at third does not establish that Alex was the retired runner. Preserve
  the earlier reaching result of whichever baserunner was forced out.

- Stephen scored after his second hit: change appearance 2 from `1B` to `1B+`.
  The user also recalled Kyla being thrown out at home, a baserunning out.
  In the context of the second-hit sequence this is recorded against Kyla's
  second appearance; preserve her `1B` with no run. The exact play on which she
  was retired remains unspecified. The latest correction attributes Stephen's
  run to Alex's second-appearance hit. The user explicitly directed a double:
  serialize Alex's second appearance as `2B*`, with one RBI and no run.
- Cory led off the third inning with his second-appearance single. This places
  Chance's second-appearance F6 at the end of the second inning. Second-inning
  outs are David F6, Kyla out at home, and Chance F6. The slash near Alex's
  second result is not an inning boundary under the corrected reconstruction.

Accounted-for scoring: all 15 runs (13 marks plus Paul's final run and Stephen's
second-appearance run), and 15 RBIs (13 dots plus Garroway's first-inning RBI
and Alex's second-appearance RBI). Alex's double is user-directed, superseding
the photographed notation and earlier recollections.

The completed CSV has 32 appearances, 15 runs and 15 RBIs. Alex's row is
`Alex,1B*+,2B*,5,`. The existing input CSV was inspected before correction;
only his second-appearance token was changed in this final edit.

Adding the three user-recalled men's appearances and excluding Chance's unplayed
fourth entry resolves the rotation/count discrepancy: 22 men's appearances and
10 women's appearances, ending at Kap in global slot 32.

## Independent source passes

The board has eight names on the left and three on the right. Separate outcome,
RBI-dot, run-plus, and out-notation passes produced the ledger below. `0` means
no visible mark, not confirmation that no credit occurred. Missing scoring marks
were subsequently resolved through the user corrections above. Alex's second
result was visually read as `5` followed by a slash; the latest user correction
supersedes that reading with `2B*`. No generic `O` fallback is used.

| Player / physical row | Visible appearance | Raw result | RBI dots | Run plus | Notes |
| --- | --- | --- | --- | --- | --- |
| Stephen / left 1 | 1 | 2B | 0 | 1 | Double |
| Stephen / left 1 | 2 | 1B | 0 | 0 | Single |
| Stephen / left 1 | 3 | HRO | 0 | 0 | Home run out, not HR |
| Alex / left 2 | 1 | 1B | 1 | 1 | Single |
| Alex / left 2 | 2 | 5 | 0 | 0 | Forward slash after result; no visible second fielding number |
| Cory / left 3 | 1 | HR | 3 | 1 | Three separate dots above HR |
| Cory / left 3 | 2 | 1B | 0 | 1 | Single |
| Cory / left 3 | 3 | 1B | 1 | 1 | Single |
| Paul / left 4 | 1 | 1B | 0 | 1 | Single |
| Paul / left 4 | 2 | HR | 2 | 1 | Two dots above HR |
| Dad / left 5 | 1 | 1B | 0 | 1 | Single |
| Dad / left 5 | 2 | 1B | 0 | 0 | Single |
| Kap / left 6 | 1 | 1B | 1 | 0 | Single |
| Kap / left 6 | 2 | 1B | 1 | 1 | Single |
| Kap / left 6 | 3 | 1B | 2 | 0 | Two diagonally separated dots |
| Bryce / left 7 | 1 | 1B | 0 | 0 | Forward slash after result |
| Bryce / left 7 | 2 | K | 0 | 0 | Strikeout |
| David / left 8 | 1 | F6 | 0 | 0 | Fly out |
| David / left 8 | 2 | 1B | 1 | 0 | Single; no clear plus below |
| Kyla / right 1 | 1 | BB | 0 | 1 | Walk |
| Kyla / right 1 | 2 | 1B | 0 | 0 | Single |
| Kyla / right 1 | 3 | 1B | 0 | 0 | Single |
| Kyla / right 1 | 4 | 1B | 0 | 0 | Single |
| Chance / right 2 | 1 | 1B | 0 | 1 | Single |
| Chance / right 2 | 2 | F6 | 0 | 0 | Narrow F and descending 6 between singles |
| Chance / right 2 | 3 | 1B | 0 | 0 | Single |
| Chance / right 2 | 4 | F6 | 0 | 0 | Fly out |
| Erica / right 3 | 1 | BB | 1 | 0 | Walk; one blue dot above |
| Erica / right 3 | 2 | 1B | 0 | 1 | Single |
| Erica / right 3 | 3 | 2B | 0 | 1 | Double |

## Visible totals

| Player | Appearances | RBI marks | Run marks |
| --- | --- | --- | --- |
| Stephen | 3 | 0 | 1 |
| Alex | 2 | 1 | 1 |
| Cory | 3 | 4 | 3 |
| Paul | 2 | 2 | 2 |
| Dad | 2 | 0 | 1 |
| Kap | 3 | 4 | 1 |
| Bryce | 2 | 0 | 0 |
| David | 2 | 1 | 0 |
| Kyla | 4 | 0 | 1 |
| Chance | 4 | 0 | 1 |
| Erica | 3 | 1 | 2 |
| Total | 30 | 13 | 13 |

There are two fewer run marks than the user-confirmed score. RBI marks also total
13; whether the other two runs earned RBIs must be established independently.
Equal visible totals do not resolve missing credits or attribution.

## Chronological ledger with user corrections

The following sequence uses the confirmed guy–guy–girl rotation and source
column order, starting Stephen / Alex / Kyla. Board aliases below retain the
original physical locations: Dad = Bryce; board Bryce = Garroway. Missing
appearances are added only from user recollection; Alex's notation is confirmed.

| Global slot | Player appearance | Source result | Boundary / issue |
| --- | --- | --- | --- |
| 1 | Stephen 1 | 2B | |
| 2 | Alex 1 | 1B | |
| 3 | Kyla 1 | BB | |
| 4 | Cory 1 | HR | |
| 5 | Paul 1 | 1B | |
| 6 | Chance 1 | 1B | |
| 7 | Dad 1 | 1B | |
| 8 | Kap 1 | 1B | |
| 9 | Erica 1 | BB | |
| 10 | Bryce 1 | 1B | Confirmed first-inning endpoint, seven-run cap; add RBI |
| 11 | David 1 | F6 | |
| 12 | Kyla 2 | 1B | Later thrown out at home per user; preserve hit, no run |
| 13 | Stephen 2 | 1B | User confirms he scored on Alex's hit |
| 14 | Alex 2 | 2B | User-directed double; one RBI scoring Stephen; no run |
| 15 | Chance 2 | F6 | Second-inning third out under confirmed Cory leadoff |
| 16 | Cory 2 | 1B | User-confirmed third-inning leadoff |
| 17 | Paul 2 | HR | |
| 18 | Erica 2 | 1B | |
| 19 | Dad 2 | 1B | |
| 20 | Kap 2 | 1B | |
| 21 | Kyla 3 | 1B | |
| 22 | Bryce 2 | K | |
| 23 | David 2 | 1B | |
| 24 | Chance 3 | 1B | |
| 25 | Stephen 3 | HRO | |
| 26 | Alex 3 | 5 | User-confirmed third-baseman out and endpoint before final inning |
| 27 | Erica 3 | 2B | Final inning; marked run |
| 28 | Cory 3 | 1B | Marked RBI and run |
| 29 | Paul 3 | BB | User-confirmed walk and run |
| 30 | Kyla 4 | 1B | User-confirmed before Bryce's L6 |
| 31 | Dad 3 | L6 | User-confirmed lineout |
| 32 | Kap 3 | 1B | Confirmed walk-off, scoring Cory and Paul |

Chance's apparent fourth F6 is excluded because the user confirmed she did not
bat after the walk-off. The raw source ledger intentionally preserves the mark.

Prior reconstruction, superseded by the new baserunning-out evidence: a candidate
second inning spanning slots 11–15
(David F6, Alex force at third, Chance F6 = three outs) and a candidate third
inning spanning slots 16–26 (Garroway K, Stephen HRO, Alex force = three outs).
This would explain why Alex's third appearance ended the inning before the final,
but conflicts with the photographed slash after his second result. Inning 2/3
boundaries remain a reconstruction, not user-confirmed facts.

The subsequent user correction adds Kyla's out at home and Stephen's run.
Withdraw the previously presented estimate of 7–0–5–3: the zero-run second
segment and the proposed extra third-inning scorer were unsupported. If the
second inning ends at the photographed Alex slash, David's F6, Kyla's runner
out, and Alex's `5` account for three outs. However, the exact timing of Kyla's
retirement and Stephen's scoring play is needed, and the later outs/boundaries
must still be reconciled with the confirmed endpoint at Alex's third appearance.
Do not infer that a run counted on a third-out force play.

The user explicitly confirmed the inning scoring breakdown as **7–1–4–3** after
final CSV validation. This confirmation supersedes the prior estimates above;
the table below records the confirmed inning run totals alongside the
reconciled appearance sequence and RBI totals.

| Inning | Global slots | Runs | RBIs | Ending / outs |
| --- | --- | --- | --- | --- |
| 1 | 1–10 | 7 | 7 | Seven-run cap on Garroway's single |
| 2 | 11–15 | 1 | 1 | David F6, Kyla runner out at home, Chance F6 |
| 3 | 16–26 | 4 | 4 | Garroway K, Stephen HRO, Alex 5 |
| 4 | 27–32 | 3 | 3 | Bryce L6; Kap walk-off single |
| Total | 32 appearances | 15 | 15 | Alex's RBI double resolved by user |

Scorers: inning 1 Stephen, Alex, Kyla, Cory, Paul, Chance, Bryce; inning 2
Stephen; inning 3 Cory, Paul, Erica, Kap; inning 4 Erica, Cory, Paul. No extra
run is assigned to Bryce's second single. Kyla's second single is preserved
despite her baserunning out. The inning structure now reconciles the out counts.

## Initial inning and scoring questions (retained history)

1. Confirm rotation, starting offsets, and missing/skipped appearances.
2. Opening sequence: Alex's RBI single plausibly scored Stephen, and Cory's
   three-run HR then scored Alex, Kyla, and Cory. Paul, Chance, and Dad also have
   run marks. Kap's RBI single and Erica's RBI walk account for two of those
   three RBIs; Bryce's single has no dot and an inning-ending slash. Did Bryce
   drive in Dad for the seventh run, reaching the run limit? This is a proposed
   reconstruction, not an added credit.
3. What ended the segment at Alex's second result? The label reads `5/`.
   David's F6 and this result alone do not establish three outs. Was there a
   double play or another baserunner out? Preserve the reaching hits regardless.
4. Confirm final inning, final batter, scorers, and whether the win was a walk-off.
   Cory's third single has one RBI and a run; Kap's third single has two RBIs;
   Erica's double has a run. Final sequence is uncertain because of missing slots.
5. Confirm any non-RBI runs and any scoring credits missing from the photograph.

The user subsequently confirmed seven runs in the first inning and Garroway's
missing RBI, then confirmed the complete inning scoring breakdown as 7–1–4–3.
The final play is confirmed as Kap's walk-off single scoring Cory and Paul.

All serialization questions are resolved: the user directed a double for Alex's
second-appearance RBI hit. His third result remains `5`; the prior second-result
`5` is superseded. Paul's BB+, Bryce's L6, Kyla's final single, and Chance's
unplayed fourth entry are resolved. Detailed baserunner movements beyond these
credits are not fully recorded and are not inferred in the CSV.

Rejected scoring lead, retained history: in the segment after
Paul's two-run HR, Erica singles, Bryce singles, Kap hits an RBI single, and Kyla
hits her third-appearance single. Bryce has no run mark on his second single;
Kyla has no RBI dot on her third single. This was proposed as a missing run/RBI
pair, but the user instead identified Stephen's second-appearance run. No extra
run for Bryce or RBI for Kyla has been added.

## Final CSV and validation history

Final validation passed by calling `parse_csv_file` directly on the input path,
with `conda activate softball-stats` and `python -B`. Verified metadata, all
11 player names and roster order, all 32 exact tokens, per-player appearance
order/counts, bases, RBIs, and runs. No warnings or dropped appearances.

Final totals: 15 runs, 15 RBIs, 32 hit bases. Hit audit: 18 singles, 3 doubles
(Stephen 1, Alex 2, Erica 3), and 2 home runs (Cory 1, Paul 2). Other results:
3 walks, 2 F6, 1 K, 1 HRO, 1 L6, 1 `5`. The photo's hit labels were inspected
independently of scoring modifiers; Alex's second result is explicitly corrected
by the user, not inferred from basepath advancement or balanced totals.

The independent-list chronological reconstruction was checked against all
32 appearances; per-inning run/RBI totals both match 7, 1, 4, 3. No generic outs
or notation fallbacks remain. Kyla's baserunning out is retained in this review;
the CSV preserves her single and does not encode runner outs or inning numbers.
Detailed runner movement and fielding sequences beyond the recorded results are
unavailable. The equal-total import blocker is resolved; no import was run.

`data/input/fray-cyclones-fa-01_2026-10-22.csv` records 32 appearances,
with user-confirmed names, Garroway's first RBI, Paul's BB+, Bryce's L6, and
Chance's unplayed fourth entry excluded, Alex's third result confirmed as `5`,
Stephen's second single marked with his confirmed run, and Alex's second
appearance corrected to the user-directed `2B*`.
At finalization the draft was no longer in `data/game-log/`; an otherwise matching
CSV was already present in `data/input/`. The agent updated only Alex's second
token there under the user's correction request, preserving all other contents.

The following validation entries are historical intermediate drafts; their
incomplete totals are retained as evidence, not the final result.

Initial source-only draft validation passed via direct `parse_csv_file` with
`conda activate softball-stats` and `python -B`: 11 players, 30 appearances,
13 runs, 13 RBIs, 30 hit bases, correct metadata, and no warnings. Exact tokens,
per-player order/counts, bases, and modifiers were checked against the visual
ledger. Outcomes: 18 singles, 2 doubles, 2 HR, 2 BB, 3 F6, 1 K, 1 HRO, 1 `5`.
Scoped pre-commit checks passed (whitespace, EOF, large-file check; YAML and Ruff
not applicable). The first Python attempt did not execute because the shell
could not create a heredoc temporary file; rerunning with `python -B -c` passed.
Validation after the confirmed-name/RBI correction also passed: 11 players,
30 appearances, 13 serialized runs, 14 RBIs, 30 hit bases, no warnings, and
confirmed names plus exact outcomes/order. Paul's additional confirmed run is
documented above but remains unserialized pending his reaching result.
No import, repository operation, or exporter run.
Latest correction validation passed via direct parser: 31 serialized appearances,
14 runs, 14 RBIs, 30 hit bases, and no warnings. Verified corrected player outcomes
and appearance order; Alex's third result remains deliberately unserialized.
Subsequent validation after Alex's confirmation passed: 32 appearances, 14 runs,
14 RBIs, no warnings. Alex's outcomes `1B*+`, `5`, `5`, appearance numbers,
bases, and scoring modifiers were verified. The prior 31-appearance result above
is retained as verification history, not the current draft state.
Validation after Stephen's run correction passed: 32 appearances, 15 runs,
14 RBIs, 30 hit bases, and no warnings. Verified Stephen's `2B+`, `1B+`, `HRO`
and Kyla's unchanged `BB+`, `1B`, `1B`, `1B`, including appearance order.
The importer requires equal RBI/run totals; legitimate non-RBI scoring would
remain an import blocker even after a parser-valid and accurate CSV is produced.

## Session ownership

Created this session: this review and the original draft CSV. At finalization,
the CSV was found in `data/input/` and corrected in place; the agent did not
perform that relocation. This review is session-owned and remains alongside
the source photograph.
Source photograph predates this work and remains unchanged.
