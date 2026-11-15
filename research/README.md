# Research line

Models here are aimed at a specific paper and have to pass the six points in [`GATE.md`](GATE.md). Everything else in the repository is the teaching Atlas (see [`../teach/`](../teach/README.md)). New ideas start in [`PUZZLE_LOG.md`](PUZZLE_LOG.md).

Each folder's README is generated from its result files. The one-line verdicts below were written on 14 November 2026; the folder README is the current source.

| Folder | Question | Verdict on 14 Nov 2026 | Feeds |
|---|---|---|---|
| [`shadow-education/`](shadow-education/README.md) | Can the three explanations of own-teacher tutoring be told apart? | **Not identified.** "Favour" is the same model as "thin" under a relabelling; "diversion" mostly behaves like "thin". The model needs a redesign before it can compare rivals. | Methods paper (as a case); a later shadow-education paper, after pupil-level data |
| [`credential-floor/`](credential-floor/README.md) | Can wealth profiles of completion separate four theories of the credential (human capital, positional, relational, Breen–Goldthorpe)? | **Not identified** on wealth profiles. The response of completion to a change in the graduate premium would separate them. | Massification paper with Nordtveit |
| [`china-forecast-ledger/`](china-forecast-ledger/README.md) | Do small models forecast China's youth unemployment better than "same month last year"? | **No model beats the naive rule** by a margin distinguishable from noise. Forecasts for Oct 2026 to Mar 2027 are frozen and waiting to be scored. | Methods paper; a public running scoreboard |
| [`marriage-gap/`](marriage-gap/README.md) | Is the gap in marriage wishes among unmarried Chinese men and women a preference gap or a selection effect? | **The chart cannot separate them.** The headline number rests on an opt-in online sample. Age-specific data would settle it. | Worked example of the gate; candidate microdata paper |
| [`methods-paper/`](methods-paper/OUTLINE_v2.md) | Revised outline, verified references, novelty assessment | Outline v2 engages analytical sociology and corrects the forecast claims. | The methods paper |

## Adding a month to the forecast ledger

Append the new NBS figure to `china-forecast-ledger/data/observed.csv` and run `python3 score.py` in that folder. Nothing is refitted.
