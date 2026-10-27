# Game 09 transcription review

Status: finalized; draft and final CSV parser validation passed. No database import.

Source: `scottsdale-dont_cha_know-fa-09_2026-10-26.jpeg`.
Filename metadata: Scottsdale; Don't Cha Know; Fall 2026; game 09; 2026-10-26.
The sheet labels the team as home, shows 10/26, and has five marked inning
columns. Written inning runs: 4, 0, 0, 0, 0; cumulative: 4, 4, 4, 4, 4.
Opponent and final opposing score are not recorded. User confirmed the game ended
after inning 5; later blank columns are not counted as zero-run innings.

Extraction: visual reading of original and locally enlarged crops, no OCR.
Inspection artifacts: matching `-inspection-top.png`, `-inspection-bottom.png`,
and `-notation-detail.png`. Source photograph unchanged. The initial sips crop
attempt produced black images; the session-owned crops were regenerated from
the source with existing Pillow in the base conda runtime and visually checked.

## Appearance ledger

Columns C1-C5 are physical inning columns, not CSV attempt numbers. PA is the
player's chronological appearance. RBI values below count lower-left dots;
runs count filled diamonds. `?` remains review-only. H = high visual confidence;
M = medium initial reading; user resolutions are recorded below. Outcome circles were audited separately
from later basepath advancement. All rows refer to the source above.

| Inning/cell | Player / PA | Raw evidence | Initial result / final token | RBI | Run | Confidence / issue |
| --- | --- | --- | --- | --- | --- | --- |
| 1/C1 | Marques / 1 | Circled 1B, filled diamond | 1B+ | 0 | 1 | H |
| 1/C1 | Rafael / 1 | Circled 3B, one dot, filled diamond | 3B*+ | 1 | 1 | H |
| 1/C1 | Josh / 1 | Circled 2B, one dot, filled diamond | 2B*+ | 1 | 1 | H |
| 1/C1 | Mike / 1 | Circled HR, two dots, filled diamond | HR**+ | 2 | 1 | H |
| 1/C1 | Cory / 1 | Circled 1B, basepath, circled out 2 | 1B | 0 | 0 | H hit; runner later retired |
| 1/C1 | Jason / 1 | Initially read F9-4? above circled out 1 | F7-4 | 0 | 0 | User corrected to F7-4 double play; Cory retired running bases |
| 1/C1 | Blake / 1 | Circled 1B, basepath | 1B | 0 | 0 | H |
| 1/C1 | Skip / 1 | 5-4, circled out 3, inning slash | 5-4 | 0 | 0 | H notation; likely force of Blake, retain Blake's single |
| 2/C2 | Jack / 1 | Circled 1B, basepath, circled out 1 | 1B | 0 | 0 | H hit; runner later retired |
| 2/C2 | Jakob / 1 | FC, basepath, circled out 2 | 6-4 | 0 | 0 | User confirmed 6-4 fielder's choice |
| 2/C2 | Marques / 2 | FC, basepath | 6-4 | 0 | 0 | User confirmed 6-4 fielder's choice |
| 2/C2 | Rafael / 2 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 3/C3 | Josh / 2 | Circled out 1; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 3/C3 | Mike / 2 | Circled 1B, basepath | 1B | 0 | 0 | H |
| 3/C3 | Cory / 2 | K, circled out 2 | K | 0 | 0 | H |
| 3/C3 | Jason / 2 | FO, circled out 3, inning slash | FO | 0 | 0 | User confirmed foul out; FO |
| 4/C4 | Blake / 2 | Circled 1B, paths to second | 1B | 0 | 0 | H; later advance is not a double |
| 4/C4 | Skip / 2 | F4, circled out 1 | F4 | 0 | 0 | User confirmed F4 |
| 4/C4 | Jack / 2 | Circled 1B, circled out 2 | 1B | 0 | 0 | H hit; runner later retired |
| 4/C4 | Jakob / 2 | 5-4, path to first | 5-4 | 0 | 0 | H notation; consistent with forcing Jack |
| 4/C4 | Marques / 3 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Rafael / 3 | Circled out 1; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Josh / 3 | Circled out 2; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |
| 5/C5 | Mike / 3 | Circled out 3, inning slash; no play label found | O | 0 | 0 | H out; exact type absent; user-approved O |

## Reconciliation

| Inning | PA | Filled diamonds | RBI dots | Written runs | Written cumulative |
| --- | --- | --- | --- | --- | --- |
| 1 | 8 | 4 | 4 | 4 | 4 |
| 2 | 4 | 0 | 0 | 0 | 4 |
| 3 | 4 | 0 | 0 | 0 | 4 |
| 4 | 5 | 0 | 0 | 0 | 4 |
| 5 | 3 | 0 | 0 | 0 | 4 |
| Total | 24 | 4 | 4 | 4 | 4 |

Runs: Marques, Rafael, Josh, Mike one each. RBIs: Rafael 1, Josh 1, Mike 2.
Initial hit audit: seven singles, one double (Josh), one triple (Rafael),
one home run (Mike): 10 hits, 16 total bases. No walks visible.
Marques/Rafael/Josh/Mike have three appearances each; remaining six players
have two each. Pack actual appearances in that batting order with trailing
padding only. Circled runner outs do not replace Cory's or Jack's singles.
Inning 2 is consistent with successive forces of Jack and Jakob; the user
confirmed both FC sequences as 6-4. Parser acceptance cannot establish who
was retired on a force play.

## User confirmations and representation limits

- Jason's first appearance is F7-4, a double play with Cory out running the
  bases; Cory retains his single. Jason's second appearance is FO (foul out).
- Skip's second appearance is F4.
- Jakob and Marques each have a 6-4 fielder's choice in inning 2. Preserve
  Jack's earlier single and each batter's actual appearance. The parser
  classifies 6-4 as a non-hit/out; that classification does not mean the batter
  was the runner retired.
- Six generic O tokens are explicitly authorized: Rafael innings 2/5,
  Josh 3/5, Marques 4, Mike 5. Enlarged full-cell inspection found no exact
  fielding label for these cells. No partially readable label was replaced.
- User confirmed the five-inning ending. No unresolved scoring questions.
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
