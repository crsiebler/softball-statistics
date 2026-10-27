# Game 10 transcription review

Status: finalized; draft and final CSV parser validation passed. No database import.

Source: `scottsdale-dont_cha_know-fa-10_2026-10-26.jpeg`.
Filename metadata: Scottsdale; Don't Cha Know; Fall 2026; game 10; 2026-10-26.
The sheet labels the team as home, shows 10/26 and 9:30, and contains five
marked inning columns. Written inning runs: 0, 2, 0, 0; cumulative: 0, 2, 2, 2.
The fifth-inning total is blank, although the column records three outs and
an inning-ending slash. No fifth-inning diamond is filled. The user confirmed
a run-rule loss in response to the five-inning/two-run ending question. Opponent and final opposing score are not recorded.
Later blank columns are not counted as zero-run innings.

Extraction: visual reading of original and locally enlarged crops, no OCR.
Inspection artifacts: matching `-inspection-top.png`, `-inspection-bottom.png`,
and `-notation-detail.png`. Source photograph unchanged. The initial sips crop
attempt produced black images; the session-owned crops were regenerated from
the source with existing Pillow in the base conda runtime and visually checked.

## Appearance ledger

Columns C1-C5 are physical inning columns, not CSV attempt numbers. PA is the
player's chronological appearance. RBI values count lower-left dots; runs
count filled diamonds. `?` remains review-only. H = high visual confidence;
M = medium initial reading; user resolutions are recorded below. Hit circles were audited independently
of subsequent basepath advancement. All rows refer to the source above.

| Inning/cell | Player / PA | Raw evidence | Initial result / final token | RBI | Run | Confidence / issue |
| --- | --- | --- | --- | --- | --- | --- |
| 1/C1 | Cory / 1 | F1, circled out 1 | F1 | 0 | 0 | Visual reading retained; no correction in user's reply |
| 1/C1 | Jason / 1 | F8, circled out 2 | F8 | 0 | 0 | Visual reading retained; no correction in user's reply |
| 1/C1 | Blake / 1 | 5-3, circled out 3, inning slash | 5-3 | 0 | 0 | H |
| 2/C2 | Skip / 1 | Circled 2B, filled diamond | 2B+ | 0 | 1 | H |
| 2/C2 | Jack / 1 | Circled 2B, one dot, filled diamond | 2B*+ | 1 | 1 | H |
| 2/C2 | Jakob / 1 | Circled out 1; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 2/C2 | Marques / 1 | Circled 2B, one lower-left RBI mark, paths to second | 2B* | 1 | 0 | H |
| 2/C2 | Rafael / 1 | Circled out 2; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 2/C2 | Josh / 1 | Circled out 3; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 3/C3 | Mike / 1 | Circled out 1, small scribble above; no recoverable label | O | 0 | 0 | H out; exact type absent; user-approved O |
| 3/C3 | Cory / 2 | Circled 1B, path to first | 1B | 0 | 0 | H |
| 3/C3 | Jason / 2 | Circled out 2; dot at upper left, no play label | O | 0 | 0 | User: dot shows out location, not RBI; O approved |
| 3/C3 | Blake / 2 | Circled 1B, path to first | 1B | 0 | 0 | H |
| 3/C3 | Skip / 2 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 4/C4 | Jack / 2 | Circled 1B, paths to second | 1B | 0 | 0 | H; later advance is not a double |
| 4/C4 | Jakob / 2 | Circled out 1; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 4/C4 | Marques / 2 | Circled out 2; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 4/C4 | Rafael / 2 | Circled 1B, path to first | 1B | 0 | 0 | H |
| 4/C4 | Josh / 2 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Mike / 2 | Circled out 1; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Cory / 3 | Circled 1B, paths to second | 1B | 0 | 0 | H; later advance is not a double |
| 5/C5 | Jason / 3 | Circled 1B, path to first | 1B | 0 | 0 | H |
| 5/C5 | Blake / 3 | Circled out 2; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Skip / 3 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |

## Reconciliation

| Inning | PA | Filled diamonds | RBI marks | Written runs | Written cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 0 | 0 | 0 |
| 2 | 6 | 2 | 2 | 2 | 2 |
| 3 | 5 | 0 | 0 | 0 | 2 |
| 4 | 5 | 0 | 0 | 0 | 2 |
| 5 | 5 | 0 | 0 | Blank | Blank |
| Total | 24 | 2 | 2 | 2 through inning 4 | 2 through inning 4 |

Runs: Skip and Jack one each. RBIs: Jack 1, Marques 1. User clarified that
Jason's inning-3 upper dot shows where the out occurred; it is not an RBI.
The new scorekeeper was unfamiliar with the usual marking convention. Inning 5
has zero runs from the complete appearance/run ledger; the written total stays
documented as blank.
Initial hit audit: six singles, three doubles (Skip, Jack, Marques), no triples
or homers: nine hits, 12 total bases. No walks visible.
Cory/Jason/Blake/Skip have three appearances each; the remaining six players
have two each. Preserve that roster order and pack actual appearances only.

## User confirmations and representation limits

- User confirmed a run-rule loss. Five offensive innings are recorded; no
  unplayed inning is represented as a zero-run inning.
- Cory F1, Jason F8, and Blake 5-3 opening plays were presented for correction
  and retained from visual evidence; the reply supplied no changes to them.
- Jason's inning-3 dot denotes out location, not RBI. His token is O with
  zero RBIs and zero runs.
- Twelve generic O tokens are explicitly authorized: Jakob innings 2/4,
  Rafael 2, Josh 2/4, Mike 3/5, Jason 3, Skip 3/5, Marques 4, Blake 5.
  Marques inning 4 received separate explicit approval. Enlarged full-cell
  inspection found no recoverable fielding labels for these cells.
- No unresolved scoring questions. Opposing score is unavailable.
- Prior draft checks: scoped pre-commit whitespace, end-of-file, and
  added-large-file checks passed; YAML/Ruff skipped as inapplicable.

## Final validation

Activated conda environment softball-stats and called parse_csv_file directly
with python -B on the draft, then moved the session-created draft to data/input
and parsed the final path. Both parses matched exactly, with no warnings or
dropped appearances. Checked metadata/date, roster order, all 24 appearances,
per-player attempt order/count, exact tokens, per-appearance bases/RBIs/runs,
hit distribution, total bases, and approved generic-out counts against the
source-backed ledger and user corrections. Run and RBI totals agree; no
known import-total blocker. Fielding sequences represent non-hits in the
parser and do not establish batter retirement. No import, repository,
exporter, CLI, or database operation was executed.
