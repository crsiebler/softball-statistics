# Game 3 transcription review — September 21, 2026

## Source and contract

- Source: `scottsdale-dont_cha_know-fa-03_2026-09-21.jpeg`.
- Extraction: visual inspection, followed by a focused fielding-notation pass;
  no OCR engine or external image upload. Source photograph preserved.
- Detail: `scottsdale-dont_cha_know-fa-03_2026-09-21-detail-pat-jack.png`
  is a session-created crop of physical column 6, Blake/Pat/Jack rows.
- Metadata comes from the supplied filename: Scottsdale / Dont Cha Know /
  Fall 2026 / game 03 / 2026-09-21. The sheet identifies the home team;
  its handwritten date is indistinct and is not the metadata authority.
- Confirmed name spellings: Marques, Paul, Cory, Jakob. Lineup order preserved.
  Logan is listed on the sheet but user-confirmed DNP; omitted from the CSV.
- `*` = one RBI; `+` = batter scored; `O` = approved unspecified non-hit.
  Attempt columns are chronological appearances, not innings.
- Inspected filename, CSV, and attempt parsers and import validation contract.
  Explicit HR RBI/run modifiers avoid parser assumptions.

## Confirmations

The user confirmed seven innings, with a scoreless fourth inning omitted from
the bottom totals; Rafael's first-inning 6-4-3 double play retired Marques and
Rafael; Cory's final double drove in Mike and Josh; Blake's fourth appearance
was a hit and Pat's subsequent fielder's choice retired Blake; Jack's third
appearance was an out, not a walk; Logan DNP. The user explicitly confirmed
Jack's second-inning RBI out as an F7 sacrifice fly and authorized generic outs
where exact notation cannot be determined from the photograph or context.

The detail crop resolves Pat's final play as 6-4 and Jack's final out as F10.
Blake's fourth appearance remains a double despite the runner-out circle.

## Chronological inning ledger

Physical columns C1–C6 are counted left to right. Blue C1 entries are inning 1;
pencil C1 entries below Paul are inning 2. C2 is inning 3; C3 is inning 4;
C4 is inning 5; C5 is inning 6; C6 is inning 7. An inning wraps through the
lineup within its physical column where necessary. Blank cells and boundary
slashes are not appearances. Every token below represents one appearance.

| Inning | Column | Batting sequence and outcomes | Outs in order |
| --- | --- | --- | --- |
| 1 | C1, blue | Marques `1B`; Rafael `6-4-3`; Mike `1B`; Paul `O` | Marques and Rafael on DP; Paul 3 |
| 2 | C1, pencil | Josh `2B+`; Cory `1B*+`; Blake `1B`; Pat `F7`; Jack `F7*`; Jakob `O` | Pat 1; Jack 2; Jakob 3 |
| 3 | C2 | Marques `HR*+`; Rafael `O`; Mike `O`; Paul `1B+`; Josh `2B*`; Cory `O` | Rafael 1; Mike 2; Cory 3 |
| 4 | C3 | Blake `O`; Pat `O`; Jack `O` | Blake 1; Pat 2; Jack 3 |
| 5 | C4 | Jakob `1B+`; Marques `HR**+`; Rafael `O`; Mike `1B+`; Paul `O`; Josh `1B`; Cory `1B*`; Blake `1B`; Pat `F7` | Rafael 1; Paul 2; Pat 3 |
| 6 | C5 | Jack `O`; Jakob `O`; Marques `1B`; Rafael `O` | Jack 1; Jakob 2; Rafael 3 |
| 7 | C6 | Mike `1B+`; Paul `O`; Josh `2B+`; Cory `2B**`; Blake `2B`; Pat `6-4`; Jack `F10` | Paul 1; Blake forced out on Pat's FC 2; Jack 3 |

## Literal evidence and confidence

Hit labels are circled in their cells, with corresponding basepaths; fully
shaded diamonds identify the nine scored runs below. Hit and run readings are
high confidence, except Mike's C4 label has overlapping marks; the single is
the retained reading from the user-reviewed plan. Pat's C1/C4 F7 labels are
visible inside the diamonds; Jack C1 F7 is user-confirmed. Rafael C1 has blue
DP/out markings, with 6-4-3 supplied by the user. Pat C6 shows 6-4 beside the
out circle; Jack C6 shows F10, with out 3 overlapping the printed BB area.
The focused crop resolves both labels with high confidence. No walk is recorded.

RBI evidence: Cory C1 one dot; Jack C1 one dot; Marques C2 solo-HR mark;
Josh C2 one dot; Marques C4 two dots; Cory C4 one dot; Cory C6 two RBIs
explicitly confirmed by the user. User confirmation controls where marks overlap.

### Generic-out audit

The full boxes were visually reinspected, including above/left of the diamond
and around each out circle. The entries below show circled out numbers without
recoverable fielding labels. Confidence is high for an out and low for its
fielding sequence. All use the user's explicit fallback authorization.

| Player | Inning / physical cell | Raw evidence and selected token |
| --- | --- | --- |
| Paul | 1 / C1 | Blue out 3; `O` |
| Jakob | 2 / C1 | Out 3 and inning boundary; `O` |
| Rafael | 3 / C2 | Out 1; `O` |
| Mike | 3 / C2 | Out 2; `O` |
| Cory | 3 / C2 | Out 3 and boundary; `O` |
| Blake | 4 / C3 | Out 1; `O` |
| Pat | 4 / C3 | Out 2; `O` |
| Jack | 4 / C3 | Out 3 and boundary; `O` |
| Rafael | 5 / C4 | Out 1; `O` |
| Paul | 5 / C4 | Out 2; `O` |
| Jack | 6 / C5 | Out 1; user corrects earlier walk reading; `O` |
| Jakob | 6 / C5 | Out 2; `O` |
| Rafael | 6 / C5 | Out 3 and boundary; `O` |
| Paul | 7 / C6 | Out 1; `O` |

There are 14 generic outs. FC token `6-4` is a non-hit in this parser, but
Pat reached and Blake was retired; it does not mean Pat was the runner out.
Marques's first single and Blake's final double retain their original results.

## Independent scoring reconciliation

| Inning | Scored runners (shaded diamonds) | RBI credits | Runs | RBIs | Cumulative runs |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | None | None | 0 | 0 | 0 |
| 2 | Josh, Cory | Cory 1 (Josh); Jack 1 (Cory) | 2 | 2 | 2 |
| 3 | Marques, Paul | Marques 1 (self); Josh 1 (Paul) | 2 | 2 | 4 |
| 4 | None | None | 0 | 0 | 4 |
| 5 | Jakob, Marques, Mike | Marques 2 (Jakob, self); Cory 1 (Mike) | 3 | 3 | 7 |
| 6 | None | None | 0 | 0 | 7 |
| 7 | Mike, Josh | Cory 2 (Mike, Josh), user-confirmed | 2 | 2 | 9 |
| Total | | | 9 | 9 | 9 |

The sheet's written totals are 0, 2/2, 2/4, 3/7, 0/7, 2/9. Inserting the
confirmed omitted scoreless fourth inning reconciles all cumulative totals.
No runs or RBIs were added merely to balance totals.

| Player | Appearances | Hit bases | RBIs | Runs |
| --- | ---: | ---: | ---: | ---: |
| Marques | 4 | 10 | 3 | 2 |
| Rafael | 4 | 0 | 0 | 0 |
| Mike | 4 | 3 | 0 | 2 |
| Paul | 4 | 1 | 0 | 1 |
| Josh | 4 | 7 | 1 | 2 |
| Cory | 4 | 4 | 4 | 1 |
| Blake | 4 | 4 | 0 | 0 |
| Pat | 4 | 0 | 0 | 0 |
| Jack | 4 | 0 | 1 | 0 |
| Jakob | 3 | 1 | 0 | 1 |
| Total | 39 | 30 | 9 | 9 |

## Validation

Validated with `python -B` and `parse_csv_file` after activating the
`softball-stats` conda environment. Both the session draft and final file
`data/input/scottsdale-dont_cha_know-fa-03_2026-09-21.csv` passed: 39 appearances,
30 hit bases, 9 RBIs, 9 runs, one sacrifice fly, and zero parser warnings.
Checked metadata, exact outcomes, lineup order, per-player chronological
appearance counts/numbers, and per-player bases/RBIs/runs against this ledger.
Separately verified cyclic batting order and runs/RBIs in each of seven innings.
CSV padding is trailing only. All 14 generic outs are enumerated above.

Scoped pre-commit file checks passed on the draft artifacts. Ruff does not apply
to these CSV/Markdown/image files. The initial validation command used a Python
feature unavailable in this environment (`zip(strict=True)`); the compatible
rerun passed with explicit sequence-length assertions. No application code was
changed. No database import or spreadsheet generation was performed.
