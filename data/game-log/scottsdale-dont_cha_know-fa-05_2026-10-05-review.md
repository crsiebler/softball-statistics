# Game 05 confirmed transcription

Source: `scottsdale-dont_cha_know-fa-05_2026-10-05.jpeg`. Extraction: direct visual reading, no OCR.
Filename metadata: Scottsdale, Dont Cha Know, Fall 2026, 2026-10-05.
Final CSV: `data/input/scottsdale-dont_cha_know-fa-05_2026-10-05.csv`. Both games ended after five innings under run rules, confirmed by user. Raf is Rafael.

## Confirmed appearance ledger

Attempts are packed chronologically; blank source cells are not appearances.
Tokens preserve hit results, RBI stars, and scored-run plus signs.

| Player | Attempt 1 | Attempt 2 |
| --- | --- | --- |
| Josh | O | 2B+ |
| Paul | O | 3B*+ |
| Mike | 1B | 1B |
| Marques | 1B | O |
| Jason | O | O* |
| Blake | O | O |
| Rafael | 1B | 1B+ |
| Cory | O | O |
| Jack | O | 1B+ |
| Logan | O | 2B* |
| Skip | O | 6-4-3* |
| Jakob | O | O |

## Source reconciliation and corrections

Inning sequence: I1 Josh through Jason; I2 Blake, Rafael, Cory (Rafael retired after his single); I3 Jack, Logan, Skip; I4 Jakob through Blake; I5 Rafael through Jakob.

Confirmed inning runs: 0,0,0,2,2; cumulative 0,0,0,2,4. User corrections supersede ambiguous handwritten fifth-inning totals.

Runs: Josh and Paul in inning 4; Rafael and Jack in inning 5. RBIs: Paul and Jason in inning 4; Logan and Skip in inning 5. Mike has no RBI. Jason has a second appearance in inning 4 with an RBI, represented as O*.

Skip hit to shortstop, who threw to second and then first. There was no force at second; only one out occurred. Preserve 6-4-3* without treating it as a double play. Rafael retains his first-inning-column-2 single despite a later runner out.

## Approved notation fallback

Whole-cell visual inspection found only circled out numbers or no recoverable fielding label for the generic outs. User approved the fallback (typed 0); the parsers supported token is capital O. No partially readable fielding labels were replaced.

Josh attempt 1: O; Paul attempt 1: O; Marques attempt 2: O; Jason attempt 1: O; Jason attempt 2: O*; Blake attempt 1: O; Blake attempt 2: O; Cory attempt 1: O; Cory attempt 2: O; Jack attempt 1: O; Logan attempt 1: O; Skip attempt 1: O; Jakob attempt 1: O; Jakob attempt 2: O.

## Validation

Direct parse_csv_file validation in activated softball-stats conda environment passed on the draft and final paths. 24 appearances, 12 players, 4 runs.
RBI/run totals: 4/4. No parser warnings. Metadata and full parsed results matched after moving drafts to final input paths. CSV rows have matching field counts, trailing padding only, and no question-mark tokens. No database import or application execution performed.
