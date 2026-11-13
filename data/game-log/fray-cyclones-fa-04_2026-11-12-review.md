# Fray Cyclones — Fall 2026, game 04 — November 12, 2026

Source: `fray-cyclones-fa-04_2026-11-12.jpeg` in this directory.
Extraction: visual reading of the original photograph and enlarged local crops;
no OCR engine or external image upload. Metadata comes from the filename, not
visible inning headings. The photo is a co-ed roster board with seven men on
the left and three women on the right. No opponent score is supplied.

## Confirmations and scoring decisions

- The team scored six runs in the first inning and none afterward. The initial
  wording “scoreless after the first” means no subsequent scoring.
- Scorers, confirmed by the user: Garroway, Alex, Cory, Paul, Kyla, Chance.
- Kap singled, then was tagged out at home on Chance's first single. Preserve
  both singles; Kap receives no run and Chance receives no RBI for that out.
- RBI dots: Garroway's HR (1), Kap's single (1), Cory's double (1), and
  Paul's HR (3). On follow-up, the user identified the dot above Kap's first
  at-bat, which visual reinspection confirms. Kap's single is corrected to
  `1B*`; his later tag-out does not erase that RBI.
- Correction history: the initial transcription missed Kap's RBI and treated
  “Yes, Cory most likely got an RBI on that double” as an additional RBI for
  Cory. That interpretation is superseded by the source dot above Kap's
  single. Cory's double returns to `2B*+`, matching its one visible RBI dot.
- The user confirmed Tyler was forced out on Garroway's second result, `5-4`,
  then Garroway and Kyla were retired on Kyla's `6-4-3` double play.
- The user corrected Tyler's second result from the visual candidate `6-4` to
  `5-4` and confirmed Mayra was the runner forced out to end the fourth.
- No generic `O` fallback is used. Kyla's final `FO` and Chance's final `4`
  preserve the source labels without inventing a specific outfield position.
- The small dark mark below Garroway's final `1-3` is not used as an inning
  slash: the fifth ends on Chance's visible `4/` with the third out.

## Source-backed appearance ledger

All rows reference the source above. L1–L7 identify the men's top-to-bottom
rows; R1–R3 identify the women's rows. A1–A3 are each player's left-to-right
appearances, not innings. RBI and run columns are independent reads. Confidence
is high following the Kap RBI reinspection and the user correction of Tyler's
label. Order follows the independent guy-guy-girl rotation.

| Order | Inning | Player | Physical cell | Raw result | RBI | Run | Final token | Evidence / later event |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Garroway | L1 A1 | HR | 1 | 1 | HR*+ | One dot, plus; solo home run |
| 2 | 1 | Alex | L2 A1 | 1B | 0 | 1 | 1B+ | Plus; eventual run |
| 3 | 1 | Kyla | R1 A1 | 1B | 0 | 1 | 1B+ | Plus; eventual run |
| 4 | 1 | Kap | L3 A1 | 1B | 1 | 0 | 1B* | One RBI dot above single; later tagged out at home on Chance's single, out 1 |
| 5 | 1 | Cory | L4 A1 | 2B | 1 | 1 | 2B*+ | One visible RBI dot; plus |
| 6 | 1 | Chance | R2 A1 | 1B | 0 | 1 | 1B+ | Plus; Kap out at home on this play |
| 7 | 1 | Bryce | L5 A1 | 5-3 | 0 | 0 | 5-3 | Out 2 |
| 8 | 1 | Paul | L6 A1 | HR | 3 | 1 | HR***+ | Three dots, plus; scores Cory, Chance, Paul |
| 9 | 1 | Mayra | R3 A1 | 5-3/ | 0 | 0 | 5-3 | Out 3; visible inning slash |
| 10 | 2 | Tyler | L7 A1 | 1B | 0 | 0 | 1B | Forced at second on Garroway's 5-4, out 1 |
| 11 | 2 | Garroway | L1 A2 | 5-4 | 0 | 0 | 5-4 | Reached on force; later out 2 on Kyla's double play |
| 12 | 2 | Kyla | R1 A2 | 6-4-3 | 0 | 0 | 6-4-3 | User confirms double play: Garroway out 2, Kyla out 3 |
| 13 | 3 | Alex | L2 A2 | 2B | 0 | 0 | 2B | Literal double; no run mark |
| 14 | 3 | Kap | L3 A2 | F4 | 0 | 0 | F4 | Out 1 |
| 15 | 3 | Chance | R2 A2 | 5-3 | 0 | 0 | 5-3 | Out 2 |
| 16 | 3 | Cory | L4 A2 | 1-3/ | 0 | 0 | 1-3 | Out 3; visible inning slash |
| 17 | 4 | Bryce | L5 A2 | F8 | 0 | 0 | F8 | Out 1 |
| 18 | 4 | Mayra | R3 A2 | 1B | 0 | 0 | 1B | Forced on Tyler's 5-4, out 3 |
| 19 | 4 | Paul | L6 A2 | F1 | 0 | 0 | F1 | Out 2 |
| 20 | 4 | Tyler | L7 A2 | 6-4 candidate | 0 | 0 | 5-4 | User correction; Mayra forced for out 3; Tyler reached |
| 21 | 5 | Kyla | R1 A3 | FO | 0 | 0 | FO | Out 1; source does not specify position |
| 22 | 5 | Garroway | L1 A3 | 1-3 | 0 | 0 | 1-3 | Out 2 |
| 23 | 5 | Alex | L2 A3 | 1B | 0 | 0 | 1B | Literal single; no run mark |
| 24 | 5 | Chance | R2 A3 | 4/ | 0 | 0 | 4 | Out 3; visible inning slash |

Every hit was checked against the written outcome independently of run/RBI
modifiers: Garroway HR; Alex 1B, 2B, 1B; Kap 1B; Cory 2B;
Paul HR; Tyler 1B; Kyla 1B; Chance 1B; Mayra 1B. Total: 11 hits,
including seven singles, two doubles, and two home runs. No walks are marked.

## Inning-by-inning text game log

Runner-out annotations can repeat an out number because both rows describe the
same event. The `+` on a reaching result means the batter eventually scored.
Innings two and four have no clear ending slash; their confirmed runner outs
and double play establish the boundaries. There are 15 unique out events.

```text
--- 1st inning [6 runs]
Garroway,HR*+
Alex,1B+
Kyla,1B+
Kap,1B*,1,Tagged out at home on Chance's single
Cory,2B*+
Chance,1B+,1,Kap tagged out at home; Chance reached and later scored
Bryce,5-3,2
Paul,HR***+
Mayra,5-3,3
--- 2nd inning [0 runs]
Tyler,1B,1,Forced at second on Garroway's 5-4
Garroway,5-4,2,Tyler forced for out 1; Garroway reached then forced on Kyla's double play for out 2
Kyla,6-4-3,3,Garroway out 2; Kyla out 3 on double play
--- 3rd inning [0 runs]
Alex,2B
Kap,F4,1
Chance,5-3,2
Cory,1-3,3
--- 4th inning [0 runs]
Bryce,F8,1
Mayra,1B,3,Forced at second on Tyler's 5-4
Paul,F1,2
Tyler,5-4,3,Mayra forced at second; Tyler reached
--- 5th inning [0 runs]
Kyla,FO,1
Garroway,1-3,2
Alex,1B
Chance,4,3
---
```

## Reconciliation and delivery status

| Player | Appearances | RBI | Runs |
| --- | --- | --- | --- |
| Garroway | 3 | 1 | 1 |
| Alex | 3 | 0 | 1 |
| Kap | 2 | 1 | 0 |
| Cory | 2 | 1 | 1 |
| Bryce | 2 | 0 | 0 |
| Paul | 2 | 3 | 1 |
| Tyler | 2 | 0 | 0 |
| Kyla | 3 | 0 | 1 |
| Chance | 3 | 0 | 1 |
| Mayra | 2 | 0 | 0 |
| Total | 24 | 6 | 6 |

Inning runs: 6, 0, 0, 0, 0. Scoring plays: Garroway's solo HR (1),
Kap's single (1), Cory's double (1), Paul's HR (3). Six independent source plus
signs match the six user-confirmed scorers. RBI/run totals now balance using
the six visible RBI dots. No sacrifice-fly interpretation or generic-out
fallback is needed. The sheet ends after the fifth; the reason for the game
ending and the opponent's score are not supplied.

Validated the session-created draft with `parse_csv_file`, moved it to
`data/input/fray-cyclones-fa-04_2026-11-12.csv`, and parsed the final path again.
Both parses agree exactly: correct filename metadata, 10 players, 24 appearances,
exact outcomes and per-player order/counts, 11 hits, 19 total bases, six RBIs,
six runs, and zero warnings. Hit bases and modifiers were asserted separately.
No application code was changed. No game import, database operation, or
spreadsheet generation was performed.

After the Kap RBI correction, a fresh direct parse of the final CSV confirmed
Kap's `1B*`, Cory's `2B*+`, 24 appearances, six RBIs, six runs, and zero
warnings. The corrected inning log matches every parsed appearance; local
UTF-8, final-newline, and trailing-whitespace checks passed again.

Configured file checks were attempted with `pre-commit run --files` against the
CSV, review, source photo, and inspection crops. The hooks could not initialize:
GitHub DNS resolution failed while fetching `pre-commit-hooks`. This is an
unavailable configured check, not a passing hook run. Basic local checks cover
UTF-8 text, trailing whitespace, final newlines, consistent CSV width, and the
chronological log matching every parsed appearance exactly once. The full test
suite was not run for this data-only transcription; no commit was requested.

### Verification for the requested commit

The user subsequently requested a local commit of the game log and recap skill.
The configured pinned hooks were reused from existing local environments without
installing packages. The first full lint attempt hit sandbox write restrictions
and reformatted an unrelated historical report script. With the required project
access, `make lint && make test` completed successfully: all six lint hooks
passed and all 236 tests passed. The unrelated report formatting was restored
to its original content and excluded from this commit. This full lint result
therefore includes that temporary formatting repair; it does not establish that
the unchanged historical report passes Ruff formatting. The source photograph
is staged as a Git LFS pointer. Inspection crops and cache files are excluded.

### Pre-push verification and cleanup

The user requested branch publication, a PR, and removal of temporary
transcription files. The seven session-created PNG inspection crops were
removed; the original JPEG, final CSV, and this review were preserved.
To make the complete publication candidate pass required repository checks,
the historical report builder's existing Ruff formatting issue is included as
a separate formatting commit. Its parsed Python AST is identical before and
after formatting. With that change retained, `make lint && make test` passed
all configured lint hooks and all 236 tests. No typecheck, integration, E2E, or
build check is configured in the Makefile or project configuration, and no CI
configuration is present. No package, application, or publishing configuration
was changed.
