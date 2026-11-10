# Inning-by-Inning Text Game Log

Read this reference when reconstructing, delivering, or discussing innings with
the transcribe-score-sheets skill. Include the log in each game's review Markdown
under `data/game-log/` and show it in a plain-text code block. It supplements the
per-player application CSV; inning headings, out tallies, and context do not
belong in that CSV.

## Format

```text
--- 1st inning [<runs-scored> run(s)]
<batter>,<plate-appearance>
<batter>,<plate-appearance>,<out-tally>
<batter>,<plate-appearance>,<out-tally>,<out-context>
--- 2nd inning [<runs-scored> run(s)]
<batter>,<plate-appearance>
--- 3rd inning [<runs-scored> run(s)]
...
---
```

- Use ordinal headings through the last inning actually played: `1st`, `2nd`,
  `3rd`, `4th`, and so on. Report runs in that inning, not the cumulative score:
  `[1 run]`, `[0 runs]`, or `[5 runs]`. End the complete log with `---`.
- Keep one row per actual plate appearance in chronological batting order.
  Preserve exact supported outcomes and modifiers: `1B`, `BB`, `F7*`,
  `5-4**+`, `L5-3`, and so on. A `+` means the batter eventually scored;
  it does not mean that run scored during this plate appearance.
- Omit unused trailing fields. A normal reaching result is `Batter,Outcome`;
  an out adds its inning out number; ambiguous outs add the fourth context field.
  Quote a context field containing commas using normal CSV quoting.
- The out tally identifies the inning's first, second, or third out. Reset
  numbering each inning. It can identify the batter being retired, that player
  being retired later as a runner, or a runner out caused by this batter's play.
  Use context to distinguish these cases.
- If context is needed without an out, leave the third field empty:
  `Batter,Outcome,,Seven-run limit reached`.

## Runner outs and double plays

Keep a runner's original reaching outcome. Annotate its row with the later out
number and the play that caused it. For example:

```text
Erica,2B,3,Out on Kap's 6-5
Paul,1B
Kap,6-5,3,Erica forced at third; Kap reached
```

Both `3` labels describe the same out. Erica's double remains a double, Kap's
fielding result does not establish that Kap was retired, and neither annotation
creates another plate appearance. The out numbers need not increase down the
rows because the runner's later out is annotated on an earlier reaching row.

For a confirmed double play, identify the individual outs on the relevant rows:

```text
Nicole,K,1
David,1B,3,Out on L5-3 double play not tagging
Bryce,L5-3,2
```

Bryce makes out two and David makes out three on the same play. Preserve David's
single and retain `L5-3` exactly. Do not invent the retired runner or order of
outs when those details are unknown; flag them in the draft.

A fielder's-choice row can carry a runner out while the batter reaches:

```text
Cory,1B,2,Forced at second on Paul's 6-4
Paul,6-4+,2,Cory forced at second; Paul reached and later scored
```

This is a conditional formatting example, not confirmation that Paul's disputed
final result in the October 29 game was `6-4+`. Never change a hit to a
fielder's choice without confirming which play retired the runner.

## Inning endings and incomplete evidence

- End an inning on a supported third out or a confirmed run-limit ending.
  A seven-run cap can end an inning with fewer than three outs; do not invent
  a third out. Apply the selected scorekeeping reference's final-inning and
  home-run exceptions. The cap does not undo a third out that occurred earlier.
- Distinguish the run driven in by a hit from the batter's later run. An RBI
  triple that scores run six does not reach the seven-run cap until a later
  play scores the seventh run.
- A first out does not establish the inning's first batter. Determine boundaries
  from the source and user-confirmed events, not from out numbers alone.
- Preserve confirmed substitutions, skipped turns, and out-of-order batting.
  Show the actual order; do not add appearances merely to satisfy a rotation.
- Use `[unknown runs]` for an unresolved inning total. Keep unknown results or
  tallies as `?` only in the review draft. Put appearances with unresolved inning
  assignments or order in a separate unresolved section outside the confirmed
  log. Label competing reconstructions as hypotheses.
- Count unique out events, not tally annotations. Check that each appearance
  occurs once, reaching runners do not cross inning breaks, and inning runs
  reconcile with confirmed player totals. Report unassigned appearances or
  unavailable inning totals without inventing them.

## Formatting example

This example illustrates the requested layout and runner-out annotations. It
does not resolve the disputed fourth/fifth-inning sequence of the source game.

```text
--- 1st inning [1 run]
Garroway,1B+
Alex,1B
Kyla,F7*,1
Cory,BB
Paul,F5,2
Erica,F7,3
--- 2nd inning [5 runs]
Kap,1B+
David,F5,1
Nicole,K,2
Bryce,1B+
Garroway,1B*+
Kyla,1B*+
Alex,HR***+
Cory,1B
Erica,2B,3,Out on Kap's 6-5
Paul,1B
Kap,6-5,3
--- 3rd inning [0 runs]
Nicole,K,1
David,1B,3,Out on L5-3 double play not tagging
Bryce,L5-3,2
---
```
