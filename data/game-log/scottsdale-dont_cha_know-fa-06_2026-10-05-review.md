# Game 06 confirmed transcription

Source: `scottsdale-dont_cha_know-fa-06_2026-10-05.jpeg`. Extraction: direct visual reading, no OCR.
Filename metadata: Scottsdale, Dont Cha Know, Fall 2026, 2026-10-05.
Final CSV: `data/input/scottsdale-dont_cha_know-fa-06_2026-10-05.csv`. Both games ended after five innings under run rules, confirmed by user. Raf is Rafael.

## Confirmed appearance ledger

Attempts are packed chronologically; blank source cells are not appearances.
Tokens preserve hit results, RBI stars, and scored-run plus signs.

| Player | Attempt 1 | Attempt 2 |
| --- | --- | --- |
| Josh | 6-3 | 2B+ |
| Paul | 1-3 | 3B* |
| Mike | F6 | 1B |
| Marques | O | O |
| Jason | 1B+ | O |
| Blake | O | O |
| Rafael | 2B* | O |
| Cory | BB | F7 |
| Jack | O | 1B |
| Logan | O | 6-4 |
| Skip | O |  |
| Jakob | O |  |

## Source reconciliation and confirmations

Inning sequence: I1 Josh, Paul, Mike; I2 Marques through Jack; I3 Logan, Skip, Jakob; I4 Josh through Blake; I5 Rafael, Cory, Jack, Logan.

Confirmed inning runs: 0,1,0,1,0; cumulative 0,1,1,2,2. Jason scores in inning 2 on Rafaels double; Josh scores in inning 4 on Pauls triple. Rafael and Paul each receive one RBI.

User confirmed Josh 6-3, Paul 1-3, Mike F6 in inning 1; Cory F7 in inning 5; Joshs fourth-inning double. Logan reaches on FC in inning 5, retiring Jack after Jacks single. User supplied tentative sequence 6-4 and indicated exact sequence was unimportant; retained 6-4 as the approved representation. Jack remains 1B, with no batter out added.

## Approved notation fallback

Whole-cell visual inspection found only circled out numbers or no recoverable fielding label for the generic outs. User approved the fallback (typed 0); the parsers supported token is capital O. No partially readable fielding labels were replaced.

Marques attempt 1: O; Marques attempt 2: O; Jason attempt 2: O; Blake attempt 1: O; Blake attempt 2: O; Rafael attempt 2: O; Jack attempt 1: O; Logan attempt 1: O; Skip attempt 1: O; Jakob attempt 1: O.

## Validation

Direct parse_csv_file validation in activated softball-stats conda environment passed on the draft and final paths. 22 appearances, 12 players, 2 runs.
RBI/run totals: 2/2. No parser warnings. Metadata and full parsed results matched after moving drafts to final input paths. CSV rows have matching field counts, trailing padding only, and no question-mark tokens. No database import or application execution performed.
