# Don't Cha Know — September 14, 2026 — Game 1

## Sources and transcription decisions

- League: Scottsdale; season: Fall 2026; date: Monday, September 14, 2026.
- Game 1 source: `data/game-log/scottsdale-dont_cha_know-fa-01_2026-09-14.jpeg`.
- Input: `data/input/scottsdale-dont_cha_know-fa-01_2026-09-14.csv`.
- Extraction: visual reading of the supplied photographs; no standalone OCR
  engine was run. Scoring corrections were supplied by the user.
- The team slug parses as `Dont Cha Know`.
- Player spelling is Marques, as confirmed by the user. Rows retain this
  photograph's lineup order.
- `*` records one RBI; `+` records one scored run. Attempt columns are packed
  chronologically for each player, not aligned to innings.
- Every generic `O` below is an unreadable out subtype using the user's approved
  fallback. It is not an invented appearance or an assertion of a particular
  fielding play. Readable/confirmed notation is retained.

## Game 1 — home, seven innings

| Inning / photo column | Chronological appearances | Runs | RBIs | Cumulative runs |
| --- | --- | --- | --- | --- |
| 1 | Marques F7; Rafael F8; Mike 1B; Paul F9 | 0 | 0 | 0 |
| 2 | Jason F6; Skip 1B; Cory F8; Blake 1B; Jack F8 | 0 | 0 | 0 |
| 3 | Jakob O; Marques 2B+; Rafael 1B*+; Mike 2B+; Paul F8*; Jason 2B*; Skip F3 | 3 | 3 | 3 |
| 4 | Cory F7; Blake 1B; Jack 1B; Jakob K; Marques L4 | 0 | 0 | 3 |
| 5 | Rafael F8; Mike F6; Paul 3B; Jason F7 | 0 | 0 | 3 |
| 6 | Skip F5; Cory 2B+; Blake 6-3; Jack 1B*; Jakob K | 1 | 1 | 4 |
| 7 | Logan 1B; Marques F8; Rafael F9; Mike F7 | 0 | 0 | 4 |
| Total | 34 appearances | 4 | 4 | 4 |

Confirmed corrections:

- The user supplied the exact fielding/strikeout notation for 17 previously
  generic outs, now recorded in the inning table and CSV. This includes
  Marques's fourth-inning `L4`, Blake's sixth-inning `6-3`, and Jakob's
  fourth- and sixth-inning strikeouts (`K`). These corrections come from user
  confirmation, not a new OCR pass.
- Jakob's third-inning appearance is the only remaining generic `O`. Its
  original visual reading established an out but not its fielding label; the
  user's approved fallback remains in effect. No new close-up inspection was
  performed for that cell during this correction.
- Paul hit a sacrifice fly in the third: `F8*`.
- Jack's sixth-inning single drove in Cory: `1B*`.
- Logan arrived late and had only one at-bat. His earlier blank boxes are not
  missing appearances; his seventh-inning single is his first CSV attempt.
- The three third-inning filled diamonds belong to Marques, Rafael, and Mike.
  Cory's sixth-inning filled diamond supplies the fourth run.
- Rafael and Jason have visually read RBI dots in the third; Paul's confirmed
  sacrifice and Jack's confirmed single complete the four RBI credits.

## Per-player cross-check

| Player | Appearances | R | RBI |
| --- | --- | --- | --- |
| Marques | 4 | 1 | 0 |
| Rafael | 4 | 1 | 1 |
| Mike | 4 | 1 | 0 |
| Paul | 3 | 0 | 1 |
| Jason | 3 | 0 | 1 |
| Skip | 3 | 0 | 0 |
| Cory | 3 | 1 | 0 |
| Blake | 3 | 0 | 0 |
| Jack | 3 | 0 | 1 |
| Jakob | 3 | 0 | 0 |
| Logan | 1 | 0 | 0 |
| Total | 34 | 4 | 4 |

## Validation

Status: parser-validated. No games have been imported.

- Activated `softball-stats` and called `parse_csv_file` directly using
  `python -B`; the CSV parsed with no warnings before relocation.
- Verified exact metadata, calendar date/day, CSV headers and row widths,
  photographed lineup order, per-player appearance counts/order, exact outcomes,
  bases, RBI/run modifiers, and agreement with the chronological inning ledger.
- Game 1: 34 appearances, 4 runs, 4 RBIs; inning totals 0, 0, 3, 0, 0, 1, 0.
- Revalidated the final `data/input/` path with no parser warnings. Exact
  appearances, metadata, bases, runs, and RBIs match this split inning ledger
  and per-player table. The former staged CSV path no longer exists.
- No Markdown/CSV formatter is configured. The configured pre-commit hook
  package was unavailable in the active environment, so whitespace/newline
  checks were performed directly instead. No tools were installed.
- Application code was unchanged; no database, application import, or full
  application test suite was run for these documentation/input artifacts.
