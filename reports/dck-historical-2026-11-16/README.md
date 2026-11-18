# Don't Cha Know historical backfill

Input: data/input/scottsdale-dont_cha_know-historical-01_2026-08-31.csv.
League/team: Scottsdale / Dont Cha Know. Season: Historical 2026.
August 31 is an authorized placeholder date. Both PDFs are aggregate summaries;
Week 7 is a whole subsequent season, added exactly once. The synthetic game is
an import container, not reconstructed game history.

Sources: page 1 of 2026 lifetime stats.pdf and week 7 season totals.pdf in Downloads.
source-totals.json preserves extracted counts, printed rates and SHA-256 hashes.
week7-review.png records the visual check. January–February CSVs are already
included; do not import data/dont_cha_know/ alongside this backfill.

## Source discrepancies and decisions

Lifetime player sums match its printed counts: 324 runs / 325 RBIs.
Week 7 prints 124 runs / 124 RBIs, but its 15 named-player rows sum to 115 runs /
119 RBIs. Its printed counts also exceed named-player sums by 27 PA, 2 BB, 17 H,
12 singles, 4 doubles and 1 triple. Visual inspection confirms this discrepancy.

The user requested removal of Unattributed Historical. Only named-player counts
contribute. The previously authorized one extra run remains assigned to Paul,
randomly selected from the top five historical hitters (Nick, Mike, Paul, Cory,
Jason). No other residual counts are assigned to players.

Generated totals: 1,409 PA, 93 BB, 692 H, 498 singles, 111 doubles, 54 triples,
29 HR, 22 SF, 440 runs, 444 RBIs, and 1,294 AB. Paul has 42 historical runs.
Historical seasons now preserve unequal RBI/run counts with a warning; regular
games still reject discrepancies. No further balancing counts are invented.

Event order, fielding notation and per-appearance run/RBI assignments are synthetic.
SF uses F8 with an RBI; HR entries explicitly include a run and at least one RBI.
Strikeouts are unknown and represented by generic outs (displayed zero does not
establish historical zero strikeouts). Rates are recalculated from counts.

Only the Historical workbook has the synthetic Game tab; Fall retains 13 actual
Game tabs. One synthetic game contributes to game counts. Zack in Fall games 7
and 8 is normalized to Zach. validation.json records counts and verification.

The user confirmed that the prior scorer did not record substitutes, explaining
the gap between named-player counts and printed team totals. Unidentified
substitute statistics are omitted at the user's request.
