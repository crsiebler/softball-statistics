# October 29 game: rules-based reassessment

This is a diagnostic reconstruction, **not an accepted 17-run game log**.
It produces a coherent five-inning game with 18 runs and 18 RBIs. It respects
the supplied scoring rules and the six latest confirmed facts, but conflicts
with the previously confirmed final total of 17. No exact 17-run reconstruction
has been established. This is not proof that every other reconstruction is
impossible, or that the actual score was 18.

The latest correction is David's first appearance = F3, superseding F5.
The source photograph was reinspected visually; no OCR was used. The input
CSV and earlier review are unchanged. All new or moved events below are
assumptions for analysis, not newly confirmed statistics.

## Full diagnostic game log

`+` means the batter subsequently scored; `*` means one RBI. References
in the fourth field point to the appendices below. Repeated out numbers on a
runner's reaching row and the later force play describe the same out.

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
David,F3,1,Latest user correction [A]
Nicole,K,2
Bryce,1B+
Garroway,1B*+
Kyla,1B*+
Alex,HR***+
Cory,1B
Erica,2B,3,Forced at third on Kap's 6-5 [A]
Paul,1B
Kap,6-5,3,Erica forced at third [A]
--- 3rd inning [0 runs]
Nicole,K,1
David,1B,3,Doubled off on Bryce's L5-3 [A]
Bryce,L5-3,2
--- 4th inning [6 runs]
Kyla,1B+
Garroway,1B+
Alex,1B*+,,Kyla scores [B]
Erica,1B,2,Assumed runner forced on Paul's 5-4 [B]
Cory,F2,1
Paul,5-4**+,2,Erica forced; throwing error scores Garroway and Alex [B]
Kyla,3B*+,,Assumed earlier turn; Paul scores [B]
Kap,2B*+,,Kyla scores [B]
David,2B*,,Kap scores; David remains aboard [B]
Nicole,K,3,Assumed delayed third appearance; David stranded [B]
--- 5th inning [6 runs]
Bryce,1B+,,Run confirmed; scoring play assumed below [C]
Garroway,F7,1
Erica,2B*+,,Bryce scores [C]
Alex,2B*+,,Erica scores [C]
Cory,1B,2,Alex advances to third; Cory later forced by next batter [C]
Kyla,6-4*+,2,HYPOTHETICAL missing appearance; Cory forced; Alex scores [C]
Paul,1B+,,Kyla advances to second [C]
Kap,HR***+,,Kyla and Paul score with Kap [C]
David,2B,,Confirmed out-of-order turn; stranded [D]
Nicole,2-3,3,Confirmed fourth appearance and final out
---
```

## Appendix A — supported early innings and current facts

The first three innings retain the earlier reconstruction: 1, 5, and 0 runs.
The board's endpoint slashes and the supplied rotation support those boundaries.
Erica as the runner retired on Kap's 6-5 and David as the runner doubled off
come from the user's supplied game-log example. Detailed advances below are
possible basepaths, not independently observed movements.

- First: Garroway scores on Kyla's sacrifice fly. Alex and Cory remain aboard.
- Second: Kap scores on Garroway's single; Bryce scores on Kyla's single;
  Garroway, Kyla, and Alex score on Alex's homer. After the homer, Cory can
  remain at third, Erica at second, and Paul at first before Kap's grounder.
  Erica's force at third ends the inning; no run is counted on that force.
- Third: Nicole strikes out, then Bryce's line-drive double play retires
  Bryce and David. No run scores.

The latest facts applied here are Bryce's final run, Cory's final force at
second, Paul scoring on Kap's three-run homer, David's first result F3,
David's three-men-in-a-row exception, and Nicole's game-ending 2-3. Prior
confirmations also retained include Cory's F2 being an out, Paul's 5-4 making
a force at second before a throwing error, and Nicole having four appearances.

## Appendix B — fourth-inning hypothesis and runner accounting

Under the original projected order, Cory F2, Paul's force, and Nicole K would
end the inning before Paul could score. Kap cannot then lead off with an RBI
double. That sequence is rejected.

This candidate instead moves Kyla's fourth recorded appearance ahead of
Nicole's third. The women's turns become Kyla, Erica, Kyla, Nicole in the
fourth. That preserves the sex pattern but is an **additional change to the
women's roster order**, beyond David's known exception. It is unconfirmed.

| Scoring play | Runner(s) scoring | Relevant base state |
| --- | --- | --- |
| Alex 1B* | Kyla | Kyla reached before Garroway and Alex |
| Paul 5-4** | Garroway, Alex | Bases loaded after Erica's single; Erica forced at second; Paul reaches on the play |
| Kyla 3B* | Paul | Paul aboard after the force/error |
| Kap 2B* | Kyla | Kyla at third after her triple |
| David 2B* | Kap | Kap aboard after his double |

Nicole then makes the third out and strands David. This explains a six-run
fourth without a seven-run ending, an empty-base RBI, or a run by the final
batter. It also changes the earlier disputed recollection: Kyla's triple
scores **Paul**, not David, in this hypothesis. Its RBI remains an assumption.

## Appendix C — fifth-inning hypothesis and the extra run

Preserving the recorded men's order, the pair Alex/Cory needs a woman's turn
before Paul/Kap/David. Cory's immediate next batter must make the force at
second. Assigning a missing fifth Kyla appearance to that slot is one possible
explanation; neither her identity nor that appearance is confirmed.

The candidate explicitly retains Paul's final recorded single. It does not
change that hit to a fielder's choice without evidence.

| Scoring play | Runner(s) scoring | Relevant base state |
| --- | --- | --- |
| Erica 2B* | Bryce | Bryce aboard from his final single |
| Alex 2B* | Erica | Erica aboard from her double |
| Hypothetical Kyla 6-4* | Alex | Alex advances to third on Cory's single; Cory forced at second; Kyla reaches |
| Kap HR*** | Kyla, Paul, Kap | Kyla remains aboard and Paul singles before the homer |

Alex scoring on the force is a modeling choice, not a recollection. He could
instead score on Paul's single, moving that assumed RBI to Paul. Either way,
this candidate still produces six runs in the fifth. The missing reaching
woman cannot simply vanish: she is not one of the confirmed three outs and
must score before or on the homer. If Alex also remained aboard, the homer
would instead be a four-run homer, contradicting its three-RBI mark.

Under this candidate the women's late order is also altered: the extra Kyla
turn occurs before Nicole's final turn. Satisfying boy-boy-girl does not prove
that the original women's roster order was followed.

## Appendix D — batting pattern and final out

From the third-inning endpoint, the candidate's groups are:

```text
David / Bryce / Kyla
Garroway / Alex / Erica
Cory / Paul / Kyla       <- women's order hypothesis
Kap / David / Nicole
Bryce / Garroway / Erica
Alex / Cory / Kyla       <- missing-appearance hypothesis
Paul / Kap / David / Nicole  <- known three-men exception
```

Groups continue across inning breaks. The candidate has 27 men's and 13
women's appearances: the 39 written appearances plus one hypothetical woman.
With a game starting with a man and ending with a woman, strict boy-boy-girl
with exactly one three-man group requires 27 = 2(13) + 1. This conditional
count establishes a missing turn or some other recording/order discrepancy;
it does not establish an actual extra appearance by Kyla.

David's final double follows the homer here. If his no-run mark is correct,
he cannot have been aboard for the homer, and the three confirmed final-inning
outs leave no earlier runner out available for him. Nicole makes the third
out and strands him.

## Appendix E — why this is not yet the 17-run game

| Inning | Runs | RBIs | Outs |
| --- | ---: | ---: | ---: |
| 1 | 1 | 1 | 3 |
| 2 | 5 | 5 | 3 |
| 3 | 0 | 0 | 3 |
| 4 | 6 | 6 | 3 |
| 5 | 6 | 6 | 3 |
| Total | 18 | 18 | 15 |

Every non-homer RBI has an eligible runner, no runner crosses an inning break,
no final batter scores, and neither late inning reaches the seven-run limit.
The requested RBI/run equality uses the team's convention crediting Paul's
two error-related runs as RBIs.

The board has 16 visible runs; Bryce's confirmed final run makes 17. The
hypothetical additional Kyla run makes 18 even with **no David runs**. Thus
removing David's disputed run does not resolve this particular reconstruction.
The candidate adds two RBIs to the board's 16: Kyla's triple scoring Paul and
the hypothetical force play scoring Alex.

To reach a defensible 17, at least one premise of this candidate must change:
an existing run credit, the missing woman's placement/outcome, the reconstructed
order, or another source entry. No specific run should be deleted just to
balance the total. This analysis has not exhaustively ruled out alternative
chronologies or source corrections. The uncertain 11-run start to the fifth
would require a 1/5/0/5/6 line score; the candidate instead starts the fifth
with 12 and does not validate that memory.

Most useful unresolved facts:

1. Who immediately followed Cory's final single and forced him at second?
2. Did Kyla's triple precede Kap's RBI double and score Paul?
3. Did Nicole's third strikeout follow David's RBI double, stranding David?
4. Which other runner, besides Paul, scored on Kap's homer?

## Verification

The diagnostic sequence is checked separately from the application CSV. Its
validation checks appearance counts, unique outs, run/RBI totals by inning,
the sex pattern with the one final triple, and a possible explicit base-state
trace. Such checks demonstrate internal consistency of the assumptions, not
that the assumed events happened. No game import or application data change
is part of this reassessment.
