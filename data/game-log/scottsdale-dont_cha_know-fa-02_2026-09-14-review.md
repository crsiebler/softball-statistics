# Don't Cha Know — September 14, 2026 — Game 2

## Sources and transcription decisions

- League: Scottsdale; season: Fall 2026; date: Monday, September 14, 2026.
- Source: `data/game-log/scottsdale-dont_cha_know-fa_02_2026-09-14.jpeg`.
- Input: `data/input/scottsdale-dont_cha_know-fa-02_2026-09-14.csv`.
- Extraction: visual reading of the supplied photograph; no standalone OCR
  engine was run. Scoring corrections were supplied by the user.
- The CSV filename normalizes the source's `fa_02` to parser-compatible
  `fa-02`. The team slug parses as `Dont Cha Know`.
- Player spelling is Marques, as confirmed by the user. Rows retain this
  photograph's lineup order.
- `*` records one RBI; `+` records one scored run. Attempt columns are packed
  chronologically for each player, not aligned to innings.
- Every generic `O` below is an unreadable out subtype using the user's approved
  fallback. It is not an invented appearance or an assertion of a particular
  fielding play. Readable/confirmed notation is retained.

## Game 2 — visitor, four innings, ended by run rule

| Inning / photo column | Chronological appearances | Runs | RBIs | Cumulative runs |
| --- | --- | --- | --- | --- |
| 1 | Paul 1-3; Jason 1B; Skip F8; Cory 1B; Blake 1-3 | 0 | 0 | 0 |
| 2 | Jack 1B; Jakob 5-4; Logan F4; Marques 1B; Rafael F7 | 0 | 0 | 0 |
| 3 | Mike O; Paul O; Jason 1B; Skip O | 0 | 0 | 0 |
| 4 | Cory 1B+; Blake F8; Jack 3B*+; Jakob 1B*; Logan BB; Marques F8; Rafael F8 | 2 | 2 | 2 |
| Total | 21 appearances | 2 | 2 | 2 |

Confirmed corrections:

- User-confirmed exact plays replace the original generic notation: Paul and
  Blake `1-3` in inning 1, Logan `F4` in inning 2, and Marques and Rafael `F8`
  in inning 4. Paul, Blake, and Logan were already corrected in the input CSV
  when this revision began; those edits were preserved.
- Rafael's inning-2 `F7` was also already present in the CSV and is preserved
  here. This revision did not independently re-read it from the photograph.
- Remaining generic outs are Mike, Paul, and Skip in inning 3. Their original
  visual readings established outs but left the fielding labels unresolved;
  the user approved generic `O`. No enlarged/cropped reread was performed in
  this correction, so exact labels remain unavailable rather than verified
  illegible under the skill's new focused-pass requirements.
- Jakob reached on a 5–4 fielder's choice in the second. Jack was forced out
  at second; Jack's earlier single stays `1B`. The user approved `5-4` for
  Jakob. The parser groups this as an out/non-hit; the CSV does not separately
  encode the retired runner or Jakob reaching base. This ledger preserves it.
- Jack's fourth-inning triple drove in Cory; Jakob's single then drove in Jack.
  Both Cory and Jack scored, matching the two filled diamonds and bottom total.
- The game ended after four innings by run rule. Later blank columns are
  unplayed innings, not zero-run innings.

## Per-player cross-check

| Player | Appearances | R | RBI |
| --- | --- | --- | --- |
| Paul | 2 | 0 | 0 |
| Jason | 2 | 0 | 0 |
| Skip | 2 | 0 | 0 |
| Cory | 2 | 1 | 0 |
| Blake | 2 | 0 | 0 |
| Jack | 2 | 1 | 1 |
| Jakob | 2 | 0 | 1 |
| Logan | 2 | 0 | 0 |
| Marques | 2 | 0 | 0 |
| Rafael | 2 | 0 | 0 |
| Mike | 1 | 0 | 0 |
| Total | 21 | 2 | 2 |

## Validation

Status: parser-validated. No games have been imported.

- Activated `softball-stats` and called `parse_csv_file` directly using
  `python -B`; the CSV parsed with no warnings before relocation.
- Verified exact metadata, calendar date/day, CSV headers and row widths,
  photographed lineup order, per-player appearance counts/order, exact outcomes,
  bases, RBI/run modifiers, and agreement with the chronological inning ledger.
- Game 2: 21 appearances, 2 runs, 2 RBIs; inning totals 0, 0, 0, 2.
- Revalidated the final `data/input/` path with no parser warnings. Exact
  appearances, metadata, bases, runs, and RBIs match this split inning ledger
  and per-player table. The former staged CSV path no longer exists.
- No Markdown/CSV formatter is configured. The configured pre-commit hook
  package was unavailable in the active environment, so whitespace/newline
  checks were performed directly instead. No tools were installed.
- Application code was unchanged; no database, application import, or full
  application test suite was run for these documentation/input artifacts.
