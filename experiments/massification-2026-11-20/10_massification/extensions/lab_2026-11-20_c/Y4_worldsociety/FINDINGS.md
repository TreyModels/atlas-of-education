# Y4 — World-society rival false-positive check (descriptive null model) — FINDINGS

**Verdict: `DISTINGUISHED`** (the predeclared null generates an upper-secondary >= 90 crossing for systems whose
observed record shows none). Descriptive null-model scoring only — no direction claim, **C1–C4 not reopened**.
All verdict statistics are `label=derived`, computed from observed series; nothing is imputed.

## Predeclared rule (frozen, quoted verbatim)

> the rival is DISTINGUISHED on the upper-secondary margin only if the null generates an upper-secondary >=90
> crossing for >=1 system that never crossed; falsifier -> NOT DISTINGUISHED.

## Null model (operationalisation, exactly as predeclared)

For each level with dated 90% crossings, the null is **"each system crosses 90 at that level's cross-system
median crossing year"**. The median uses **band midpoints of dated non-censored crossings only**; censored rows
are excluded from the median and listed, with the exclusion reason, in `results/Y4_MEDIAN_INPUTS.csv`. Primary
median = one midpoint per system (system-collapsed) then median across systems; the all-rows median and a
left-censored-inclusive sensitivity are also reported in `results/Y4_LEVEL_SUMMARY.csv`.

**Per-row "never crossed" rule applied** (recorded per row in `results/Y4_AUDIT.csv`): the observed record shows
a crossing if the observed final value is >= 90 **or** any 90% timing row for that country/level is a dated
(non-censored) crossing. "Never crossed" = no crossing in that record, i.e. final value < 90 with no dated
crossing, **or** the 90% timing row is right-censored, **or** the series/timing row is absent (the predeclared
rule includes absent; those rows are individually flagged as data absence, not evidence of non-crossing).

## Result (numbers verbatim in `results/`)

| level | null median year | never crossed | null false crossings (incl. absent) | evidence-backed | level verdict |
|---|---|---|---|---|---|
| primary | **1974.5** | **0** | **0** | **0** | NOT DISTINGUISHED |
| lower secondary | **2008** | **2** | **2** | **1** | DISTINGUISHED |
| secondary | **2009** | **1** | **1** | **1** | DISTINGUISHED |
| **upper secondary** | **2011.5** | **4** | **4** | **2** | **DISTINGUISHED** |
| tertiary | NA | **4** | **0** | **0** | UNABLE (no 90% rows in timing file) |

`results/Y4_LEVEL_SCORE.csv`; totals `results/Y4_SUMMARY.csv`.

- **Upper-secondary margin (the A5b/D77 margin):** null year **2011.5**, derived from **1** dated non-censored
  crossing in **1** system (HKG). Four systems never crossed 90 in the observed record: **CHN, JPN, KHM, PHL**
  (**3** have an observed series; JPN has none). The null therefore falsely crosses **4** systems; **2** of
  these (CHN, PHL) are fully testable because their observed series reach the null year. The predeclared
  threshold is met (>= 1), so the verdict is `DISTINGUISHED`.
- **Across all four scored levels:** the null falsely crosses **7** system-level cells including absent records,
  of which **4** are evidence-backed against a record that reaches the null year.
- Observed upper-secondary final values: CHN **79.39**, KHM **28.74**, PHL **66.05** (below 90); KOR **100.32**,
  HKG **106.08** (at/above 90); JPN **NA**. The independent completion channel agrees on who never crossed:
  CHN **87.52**, KHM **27.87**, PHL **75.03**, KOR **99.46** (`results/Y4_AUDIT.csv`).
- The one apparent final-value quirk is PHL secondary: its final value is below 90 but it carries a dated
  crossing (**2022**), so the record does show a crossing and it is not counted as never-crossed.
- Sensitivity: including dated left-censored crossing years puts the upper-secondary median at **2002.75**;
  the verdict is unchanged (the same never-crossed systems still receive a null crossing).

## Caveats

- The upper-secondary null rests on **1** dated non-censored crossing, so it is thin; the predeclaration forbids
  changing the rule, and the sensitivity median (**2002.75**) preserves the verdict.
- KHM's upper-secondary record ends before the null year, so its null crossing is not directly testable; JPN's
  upper-secondary series and 90% timing row are absent. Neither is needed for the verdict — the **2** testable
  cases (CHN, PHL) already satisfy the >= 1 threshold.
- Null-model scoring only: the null is a point prediction that every system crosses at one median year, so it
  assigns a crossing to every system by construction. The finding is therefore about the observed never-crossed
  set, not about a fitted world-society process.

## Reproducibility

`code/run.py` exits 0, is deterministic (no RNG, no network, no imputation), and was re-run; `shasum -a 256
results/*.csv` was byte-identical across runs:

| file | sha256 |
|---|---|
| `results/CLUSTER_RESULTS.csv` | `37cccb5aa30b83109627f5959709428553633746190770008543b15a91f0185f` |
| `results/Y4_AUDIT.csv` | `e05c2e12a4d32f9d72482d34932ffce5295b80a7b12e73c2fe234d82315d06dd` |
| `results/Y4_LEVEL_SCORE.csv` | `a41b8cfacdeb4b2f9df6d80034238c2ad5eda32b560ec39528b15264429e2f31` |
| `results/Y4_LEVEL_SUMMARY.csv` | `c6cfa946894898125d07f63ca5066ec8ff6951808752172f7f386f2debe4dc1e` |
| `results/Y4_MEDIAN_INPUTS.csv` | `6bf3b3b690a8c90a59bcfaa32c55e2c6fcff7b68e05b9e95ee5b7594c977d36a` |
| `results/Y4_SUMMARY.csv` | `407250e46d9e4ba2a8a4a91ecd4ff3c8b4138f248cf536db638c1b36b7de69da` |
