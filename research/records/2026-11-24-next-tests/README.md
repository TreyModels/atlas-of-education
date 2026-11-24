# Next tests: scripts, parameters and results for the five open questions (24 Nov 2026)

Companion to `research/records/2026-11-24-assessment-and-next-experiments/`. Start with `LETTER_FOR_DEEPSEEK.md`.

| Question | Script / file | Run here? | One-line result |
|---|---|---|---|
| Q1 Is "schooling first" stable? | `scripts/q1_threshold_sweep.py` | yes (2 s) | Default reproduced exactly; forward share depends on the schooling threshold: 96-97% at +0.5 y/decade, 84-91% at +1.0, 65-70% at +1.5 |
| Q2 Placebo fertility cannot contaminate | `scripts/q2_adult_stock_placebo.py` | yes (10 s) | Inconclusive: lag dominates for one fertility series, lead dominates for the other; no clean direction in 10-year changes |
| Q3 Logistic vs exponential-to-floor on complete transitions | `scripts/q3_form_race.py` | yes (3 s), 9 countries only | With the plateau observed the 7-parameter double-logistic wins BIC in 6 of 9; ranking among the 4-parameter forms is unstable |
| Q4 Methods verdicts | `q4_methods_params.json` | no (needs panel, 16 cores) | Parameters, corrected arithmetic, regimes, decision rules |
| Q5 How far back can backcasts be trusted? | `scripts/q5_backcast_validation.py` | yes (10 s) | Donor-based backcasts beat naive by 30-80% for most series out to 40 years; trend extrapolation is worse than naive beyond 10 years; GDP is not recoverable |

All results are exploratory, on the data in `data/` (about 5 MB, all from the repo). Every script writes its outputs to the working directory; run from `results/` as
`python3 -I ../scripts/<script>.py ../data`.

## Q1 details (`results/q1_reproduction.txt`, `q1_sweep.csv`, `q1_reverse_cases.txt`)
Three-event sample, forward share of identifiable countries (n identifiable in brackets), window 1960-2010 / 1965-2010 / 1970-2015:
- schooling threshold +0.5 y per 10 y: 95.8-97.0% across release thresholds and windows [24-33 identifiable]
- +1.0 y (the paper's default): 91.2% / 91.2% / 88.2% at release 3 points [34]; 83.9-87.5% at release 2 points; 88.0-88.9% at release 5 points
- +1.5 y: 65.4-70.4% [22-30]; reverse cases rise from 3 to 7-10 because a stricter take-off moves the schooling date later.
Implication for Paper 1: report a range and the threshold, not "91%". The pre-registered flag (forward share below 75% in any cell with at least 20 identifiable countries) fires.
Release dates start at 1991 in every country (series start), so every pair with release at 1991 is left-censored; the sweep keeps the paper's censoring rule.

## Q2 details (`results/q2_adult_stock_placebo.txt`)
Adult attainment stock (mean years of schooling, population 25+, 5-year grid) with country and year fixed effects, standardised, country-clustered SEs:
- outcome `effective_fertility`: lag S(t-10) -1.02 (0.20), current -0.60 (0.17), lead S(t+10) -0.32 (0.19)  -> the past matters more than the future
- outcome `tfr_observed_1950plus`: lag -0.30 (0.22), current -0.54 (0.19), lead -0.84 (0.20) -> the future matters more
- 10-year changes: dF on prior/next/following dS: -0.24 (0.06), -0.22 (0.06), -0.11 (0.04); dS on prior/next/following dF: -0.08 (0.04), -0.19 (0.04), -0.12 (0.04): symmetric, no clean direction.
The two fertility series disagree; before 1950 `effective_fertility` is a modelled reconstruction and from 1950 it should equal the observed TFR, so the difference needs explaining (E-task in the letter). Do not cite Q2 as evidence for or against any of the three readings.

## Q3 details (`results/q3_form_race_summary.txt`, `q3_form_race.csv`)
Nine countries (BEL, CHE, DNK, FIN, FRA, ITA, NLD, NOR, SWE), first transition up to the first sustained rebound. FULL window BIC winners: double-logistic 6, logistic 2, exponential-to-floor 1; median hold-out RMSE (last 10 years) 0.29 for exponential-to-floor and double-logistic, 0.34 for logistic.
Artificially left-censored windows (start after 20% of the fall): double-logistic 3, exponential-to-floor 2, Gompertz 2, logistic 1 (n=8). Too few countries and an unreliable pre-1950 series: the result does not settle N4's claim; it shows the UN-style double-logistic is the form to beat.

## Q5 details (`results/q5_backcast_summary.txt`)
Anchor 1990, hidden 1950-1989, six series, random and rich-to-poor donor splits. "Truth" is the best available series, itself modelled for 1950-1989, so skill measures agreement with those reconstructions.
- Trend extrapolation (M1) is worse than carrying the 1990 level back beyond 10 years for fertility, child mortality and life expectancy (and for GDP up to 20 years); it helps only for urbanisation and schooling.
- Donor-dynamics (M2) and analog (M3) skill vs naive: fertility 0.4-0.5, child mortality 0.3-0.55, life expectancy 0.3-0.55, urbanisation 0.3-0.6, schooling 0.6-0.8 (random split). Rich-to-poor: M2 fails for life expectancy (-0.08 to -0.69) and GDP; M3 is the robust one (life expectancy 0.31-0.56) but weak for fertility (0.04-0.13) and GDP (0-0.12).
- 80% intervals built from a calibration half cover 62-95% (often 62-72% in the rich-to-poor case): intervals are too narrow there and must be widened or conformalised per scenario.

Note: `results/q5_backcast.csv.gz` (6.5 MB of raw errors) is regenerated by the script and is not committed.
