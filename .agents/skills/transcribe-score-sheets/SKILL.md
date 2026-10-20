---
name: transcribe-score-sheets
description: Transcribes photographed softball diamond score sheets and co-ed roster-board game logs into CSVs with source-backed RBI/run reconciliation.
---

# Transcribe Score Sheets

## Goal

Produce evidence-backed input CSVs from supplied game-log photographs. Resolve
scoring ambiguities with the user before finalizing affected appearances.
Preserve batting order, reaching results, RBI credits, and scored runs.

Follow AGENTS.md and runtime permissions. Read explicitly supplied photographs;
do not browse unrelated game data. Use `data/game-log/` for transcription drafts
and game-specific review notes. Generate confirmed, parser-validated player
statistics CSVs in `data/input/`; that directory contains only CSV game logs.
Reserve `data/output/` for application-generated SQLite databases and Excel
spreadsheets. Do not import games or run database operations.
In plan mode, provide a draft and questions only. Do not install OCR software or
upload photographs externally without authorization.

Track which `data/game-log/` files were created in this working session. Modify
only those files; never overwrite, rename, or delete files from earlier sessions.
For an existing review path, create a uniquely named revision instead. Check
destination paths before writing and preserve existing input CSVs unless their
replacement is explicitly authorized.

Save each review Markdown in `data/game-log/` alongside its source photograph,
not in `data/input/` or a separate transcription directory. Name it after its
game CSV:
`data/game-log/<league>-<team>-<season>-<game>_<YYYY-MM-DD>-review.md`.
Keep separate reviews for doubleheader games. Use a unique revision suffix if
that review already exists from an earlier session; leave source photos intact.

## Establish the input contract

Inspect these sources before serializing; application changes may affect tokens:

- `src/softball_statistics/parsers/filename_parser.py`
- `src/softball_statistics/parsers/csv_parser.py`
- `src/softball_statistics/parsers/attempt_parser.py`
- `src/softball_statistics/use_cases/__init__.py`

Current format:

```text
<league>-<team>-<season>-<game>_<YYYY-MM-DD>.csv
Player Name,Attempt,Attempt,Attempt
```

- Use a numeric game number and a real calendar date. For example,
  `scottsdale-dont_cha_know-fa-02_2026-09-14.csv`.
- League/team underscores become spaces and names are title-cased; `fa` becomes
  Fall with the date's year appended. Preserve the approved team slug.
- UTF-8 CSV, one row per player in the format-specific roster order. Use confirmed
  spelling, distinguishing similar names such as Jack and Jakob.
- Pack each player's actual appearances chronologically. Attempt columns are
  appearances, not innings. Use only trailing padding for unused CSV cells.
- Hits: `1B`, `2B`, `3B`, `HR`; walk: `BB`; strikeout: `K`.
- Preserve exact supported out notation, such as `1-3`, `F4`, `F8`, or `6-3`.
  Generic `O` is a last resort after the focused notation pass below and user
  approval. Blanket fallback approval does not make partially read plays `O`.
- Append `*` per RBI and `+` if that batter scored: `1B*`, `2B+`, `3B**+`.
- There is no literal `SF` token. A confirmed sacrifice fly can be `F8*`;
  downstream statistics use fly-out notation with RBI to identify sacrifices.
- A confirmed fielder's choice may use the approved fielding sequence, such as
  `5-4`. Preserve who reached and who was retired in the ledger. This parser
  groups the result as an out/non-hit; that does not establish the batter was
  the runner retired. Do not infer every `5-4` is a fielder's choice without
  context. Keep the retired runner's earlier single or walk unchanged.
- Do not invent mappings for unsupported results. The parser is permissive;
  acceptance alone is not proof of correct scoring semantics.
- Home-run parsing can assume missing RBI/run modifiers. Resolve them from
  evidence rather than accepting automatic assumptions as scoring evidence.

## Select the scorekeeping format

Read the supplied photo visually and identify its layout before interpreting
marks. Report visual extraction versus actual OCR use accurately. Read only
the matching reference:

- [Diamond score sheet](references/diamond-score-sheet.md): formal inning
  columns, infield diamonds, lower-left RBI dots, filled diamonds for runs,
  out numbers, and inning reconstruction.
- [Co-ed roster board](references/coed-roster-board.md): men on the left,
  women on the right, guy-guy-girl rotation, outcomes below each name,
  RBI dots above outcomes, and run plus signs below outcomes.

Do not transfer dot placement, diamond conventions, or column meanings between
formats. Record filename-derived metadata separately from visible evidence.

## Read and reconcile

Use separate passes for outcomes, RBI marks, and run marks. Preserve each
player's left-to-right appearance order. Reinspect fielding notation separately
from modifiers; compare handwriting within the source and retain exact labels.
A fielding sequence does not prove the batter was the runner retired. A runner
out does not replace that runner's earlier hit or walk.

Record source, player, physical location/appearance, raw outcome, RBI count,
run mark, confidence, and unresolved questions. Use `?` only in review notes.
Blank space is not an out. Any proposed generic `O` requires a documented
inspection attempt, unresolved exact notation, and user fallback authorization;
do not replace a partially readable label silently.

Build a chronological ledger using the selected format. Reconstruct innings
only where supported by evidence; explicitly report unavailable inning totals.
Reconcile player/game runs and RBIs independently. Equal totals cannot prove
correct attribution. Never invent credits to balance totals. Confirm legitimate
non-RBI runs and report the import blocker: the importer requires equal RBI/run
totals even though the CSV parser does not.

## Resolve questions and serialize

Batch focused questions by game, inning, player, and physical cell. State the
visible candidate and scoring impact. Ask whether a fly out with an RBI is a
sacrifice fly rather than silently selecting that interpretation.

Retain user corrections in the ledger. Once scoring ambiguities, names, ending,
and approved notation fallbacks are resolved, generate the CSVs under the
existing write authorization; do not request repeated approval for settled
items. Keep remaining uncertainties explicit in `data/game-log/` drafts and
withhold affected final logs from `data/input/`.

## Validate and deliver

Activate `conda activate softball-stats` before executing Python. Use
`python -B` and call `parse_csv_file` directly on draft CSVs in `data/game-log/`.
After validation, move session-created CSV drafts into `data/input/` and check
the final paths through the parser. Do not call the
CLI, import use case, repositories, exporters, `make run`, or reparse commands.

Compare parsed metadata, exact outcomes, per-player appearance order/counts,
bases, RBIs, and runs with the ledger. Verify no unexpected warnings or dropped
appearances. Reconcile supported innings separately because CSV attempt columns do not
encode innings; do not fabricate missing inning evidence. Parser success is not proof an import was performed.

Check exact tokens against the source/user-confirmed notation, not only a ledger
copied from the CSV. Enumerate any remaining generic outs and their evidence.
When correcting an existing CSV, preserve other user edits and update only
session-owned review files (or create a new uniquely named review revision).

Run configured file checks scoped to changed artifacts. Report unavailable
tools rather than installing them. Deliver:

- CSV paths and extraction method.
- A source-backed appearance ledger, supported innings, confirmations, and fallbacks.
- Game run/RBI totals, available inning totals, and actual validation results.
- Remaining limitations, including any representation or import blockers.
