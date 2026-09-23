# Game 4 transcription review — September 21, 2026

## Source and contract

- Source: `scottsdale-dont_cha_know-fa-04_2026-09-21.jpeg`.
- Extraction: visual inspection, followed by a focused fielding-notation pass;
  no OCR engine or external image upload. Source photograph preserved.
- Detail: `scottsdale-dont_cha_know-fa-04_2026-09-21-detail-marques.png`
  is a session-created crop of Marques's fourth-inning cell with column headings.
- Metadata comes from the supplied filename: Scottsdale / Dont Cha Know /
  Fall 2026 / game 04 / 2026-09-21. Sheet identifies the visitor team and
  labels innings 1–7. Printed scoring-example column excluded.
- Confirmed name spellings: Marques, Paul, Cory, Jakob. Lineup order preserved.
- `*` = one RBI; `+` = batter scored; `O` = approved unspecified non-hit.
  Attempt columns are chronological appearances, not innings.
- Inspected filename, CSV, and attempt parsers and import validation contract.

## Confirmations

The user confirmed Mike's first appearance as a sacrifice fly; his seventh-
inning appearance as a fielder's choice retiring Logan; Cory's sixth-inning
appearance as a single; and Blake's sixth-inning appearance as a fielder's
choice retiring Cory, not a hit. The user authorized generic outs where exact
notation cannot be determined from the photograph or context. The revised
plan uses FO* for the confirmed sacrifice fly with unspecified fielding position,
and O/O+ for fielder's choices with unreadable fielding sequences.

The detail crop resolves Marques's fourth-inning out as F7, rather than a
generic out. No home run is recorded for Mike's seventh-inning appearance.

## Chronological inning ledger

Physical columns C1–C7 correspond to the labeled logical innings. An inning
wraps through the lineup within its column where necessary. Every token below
represents one appearance; blank cells and boundary slashes are not appearances.

| Inning | Column | Batting sequence and outcomes | Outs in order |
| --- | --- | --- | --- |
| 1 | C1 | Marques `3B+`; Mike `FO*`; Paul `O`; Josh `O` | Mike 1; Paul 2; Josh 3 |
| 2 | C2 | Cory `O`; Blake `1B+`; Pat `1B`; Jack `1B*`; Jakob `O`; Logan `O` | Cory 1; Jakob 2; Logan 3 |
| 3 | C3 | Marques `O`; Mike `O`; Paul `O` | Marques 1; Mike 2; Paul 3 |
| 4 | C4 | Josh `1B+`; Cory `O`; Blake `1B*+`; Pat `1B+`; Jack `1B*`; Jakob `O`; Logan `1B*`; Marques `F7` | Cory 1; Jakob 2; Marques 3 |
| 5 | C5 | Mike `O`; Paul `O`; Josh `O` | Mike 1; Paul 2; Josh 3 |
| 6 | C6 | Cory `1B`; Blake `O+`; Pat `2B*`; Jack `O`; Jakob `O` | Cory forced out on Blake's FC 1; Jack 2; Jakob 3 |
| 7 | C7 | Logan `1B`; Marques `O`; Mike `O`; Paul `1B`; Josh `O` | Marques 1; Logan forced out on Mike's FC 2; Josh 3 |

## Literal evidence and confidence

Marques C1 has circled 3B and a filled diamond; Blake C2 and Josh/Blake/Pat C4
have circled 1B and filled diamonds. Blake C6 has a filled diamond and a marked
1B area, but the user's correction establishes FC, not a single. Other retained
hits have circled hit labels and/or corresponding basepaths. Cory C6 and Logan
C7 have reaching paths plus out circles: user-confirmed singles followed by
runner outs. Hit/run readings are high confidence with these corrections.

RBI dots are visible at Mike C1, Jack C2, Blake C4, Jack C4, Logan C4, and
Pat C6. All six are one-RBI credits. Mike's sacrifice-fly type is user-confirmed;
its fielding position is not legible. Marques C4 shows F7 above/overlapping
out 3; the focused crop establishes the fielding label with high confidence.

### Generic-out and fielder's-choice audit

The full boxes were visually reinspected, including above/left of the diamond
and around each out circle. Unless noted below, only the out ordinal is
recoverable; confidence is high for an out, low for the fielding sequence.
The user's explicit fallback authorization applies to each listed token.

| Player | Inning / physical cell | Raw evidence and selected token |
| --- | --- | --- |
| Paul | 1 / C1 | Out 2; `O` |
| Josh | 1 / C1 | Out 3 and boundary; `O` |
| Cory | 2 / C2 | Out 1; `O` |
| Jakob | 2 / C2 | Out 2; `O` |
| Logan | 2 / C2 | Out 3; `O` |
| Marques | 3 / C3 | Out 1; `O` |
| Mike | 3 / C3 | Out 2; `O` |
| Paul | 3 / C3 | Out 3 and boundary; `O` |
| Cory | 4 / C4 | Out 1; `O` |
| Jakob | 4 / C4 | Out 2; `O` |
| Mike | 5 / C5 | Out 1; `O` |
| Paul | 5 / C5 | Out 2; `O` |
| Josh | 5 / C5 | Out 3 and boundary; `O` |
| Blake | 6 / C6 | Filled diamond, 1B-area mark; user corrects to FC retiring Cory; `O+` |
| Jack | 6 / C6 | Out 2; `O` |
| Jakob | 6 / C6 | Out 3; `O` |
| Marques | 7 / C7 | Out 1; `O` |
| Mike | 7 / C7 | Ambiguous marks near HR; user confirms FC retiring Logan; `O` |
| Josh | 7 / C7 | Out 3; `O` |

There are 19 generic non-hit tokens, including two fielder's choices. Neither
FC means the batter was retired. Blake scored after reaching on his FC, so O+
retains the run without incorrectly crediting a hit. The CSV cannot independently
encode the retired runner or distinguish these generic FC tokens from batter
outs; this ledger preserves that information. Cory's and Logan's earlier hits
remain singles. FO* preserves Mike's sacrifice-fly treatment without inventing
a fielding position; it is separate from the 19 generic O tokens.

## Independent scoring reconciliation

| Inning | Scored runners (shaded diamonds) | RBI credits | Runs | RBIs | Cumulative runs |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | Marques | Mike 1 (Marques), confirmed sacrifice fly | 1 | 1 | 1 |
| 2 | Blake | Jack 1 (Blake) | 1 | 1 | 2 |
| 3 | None | None | 0 | 0 | 2 |
| 4 | Josh, Blake, Pat | Blake 1 (Josh); Jack 1 (Blake); Logan 1 (Pat) | 3 | 3 | 5 |
| 5 | None | None | 0 | 0 | 5 |
| 6 | Blake | Pat 1 (Blake) | 1 | 1 | 6 |
| 7 | None | None | 0 | 0 | 6 |
| Total | | | 6 | 6 | 6 |

Written inning totals 1, 1, 0, 3, 0, 1, 0 and cumulative totals 1, 2, 2, 5,
5, 6, 6 match independently counted scored diamonds and RBI credits.

| Player | Appearances | Hit bases | RBIs | Runs |
| --- | ---: | ---: | ---: | ---: |
| Marques | 4 | 3 | 0 | 1 |
| Mike | 4 | 0 | 1 | 0 |
| Paul | 4 | 1 | 0 | 0 |
| Josh | 4 | 1 | 0 | 1 |
| Cory | 3 | 1 | 0 | 0 |
| Blake | 3 | 2 | 1 | 3 |
| Pat | 3 | 4 | 1 | 1 |
| Jack | 3 | 2 | 2 | 0 |
| Jakob | 3 | 0 | 0 | 0 |
| Logan | 3 | 2 | 1 | 0 |
| Total | 34 | 16 | 6 | 6 |

## Validation

Validated with `python -B` and `parse_csv_file` after activating the
`softball-stats` conda environment. Both the session draft and final file
`data/input/scottsdale-dont_cha_know-fa-04_2026-09-21.csv` passed: 34 appearances,
16 hit bases, 6 RBIs, 6 runs, one sacrifice fly, and zero parser warnings.
Checked metadata, exact outcomes, lineup order, per-player chronological
appearance counts/numbers, and per-player bases/RBIs/runs against this ledger.
Separately verified cyclic batting order and runs/RBIs in each of seven innings.
CSV padding is trailing only. All 19 generic non-hit tokens are enumerated above.

Scoped pre-commit file checks passed on the draft artifacts. Ruff does not apply
to these CSV/Markdown/image files. The initial validation command used a Python
feature unavailable in this environment (`zip(strict=True)`); the compatible
rerun passed with explicit sequence-length assertions. No application code was
changed. No database import or spreadsheet generation was performed.
