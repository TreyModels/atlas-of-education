# Y2 — Cross-channel lead-lag constraint (schooling ↔ markets) — FINDINGS

**Verdict: `NOT SUPPORTED`** (descriptive screen; falsifier "interaction not detectable"; EQUIVALENT reinforced).
This is a **description only** — never a push/pull direction, complementarity, or causal claim. **C1–C4 are not
reopened.** All statistics are `label=derived`, computed from observed series; nothing is imputed or synthesized.

## Predeclared rule (frozen, quoted verbatim)

> "descriptively visible" only if one direction has |partial r| >= 0.25 at >=2 CONSECUTIVE lags with consistent
> sign AND the reverse direction is < 0.25 (at the same lags); falsifier -> NOT SUPPORTED ("interaction not
> detectable"; EQUIVALENT reinforced).

## What was run

30 countries, 1971–2024. Schooling = `SE.SEC.ENRR`, `SE.TER.ENRR`; markets = `SL.SRV.EMPL.ZS`,
`SL.EMP.WORK.ZS`. Each series country-demeaned over 1971–2024; cross-lag **partial** correlation controlling the
dependent series' own lag-1; lags 1–3; both directions; all 4 schooling×market pairs → 24 cells. Countries with
**8** usable observations per pair enter (`min_obs_per_country` in `Y2_LAG_MATRIX.csv`). No imputation; missing
cells dropped.

## Result (numbers verbatim in `results/`)

| quantity | value | source |
|---|---|---|
| cells evaluated | **24** | `Y2_SUMMARY.csv` |
| cells with \|partial r\| >= 0.25 | **0** | `Y2_SUMMARY.csv` |
| pairs SUPPORTED / NOT SUPPORTED / UNABLE | **0 / 4 / 0** | `Y2_SUMMARY.csv` |
| strongest \|partial r\| | **0.2079** | `Y2_SUMMARY.csv` |
| strongest cell | `SE.SEC.ENRR__SL.EMP.WORK.ZS`, **schooling_to_market**, lag **1** | `Y2_SUMMARY.csv` |
| strongest cell n | **700** obs, **30** countries | `Y2_SUMMARY.csv` |
| schooling→market partial r range | **0.1023** to **0.2079** (all positive) | `Y2_SUMMARY.csv` |
| market→schooling partial r range | **−0.0567** to **0.0904** | `Y2_SUMMARY.csv` |
| zero-order r range (no own-lag control) | **0.4899** to **0.7081** | `Y2_SUMMARY.csv` |
| rank-partial sensitivity, max \|r\| | **0.2465** (still < 0.25) | `Y2_SUMMARY.csv` |
| pair-window-demean sensitivity, max \|r\| | **0.1478** | `Y2_SUMMARY.csv` |

No direction reaches |partial r| >= **0.25** at even one lag, so no >=2-consecutive-lag run exists and the
reverse-direction clause is never activated. The strongest single cell (**0.2079**) is a schooling→market cell,
but it is a lead-lag *description* only and is below the predeclared bar.

The zero-order correlations (**0.4899**–**0.7081**) are much larger than the predeclared partials because both
series carry shared time trends; the predeclared estimator removes the dependent series' own lag-1, so the
verdict rests on the partial r range **0.1023**–**0.2079**, not on the zero-order values.

## Caveats

- Markets are observed only **1991**–**2024** (`SL.SRV.EMPL.ZS` covers **15** countries), so pair samples are
  unbalanced; the weakest pair has **13** countries in some cells.
- Pooled within-country (country-demeaned) association; no causal identification, no CIs (descriptive, no
  sampling model).
- The rank-partial sensitivity peaks at **0.2465**, close to but below the frozen **0.25** bar; this does not
  change the verdict and is reported for transparency only.

## Reproducibility

`code/run.py` exits 0, is deterministic (no RNG, no network, no imputation), and was re-run; `shasum -a 256
results/*.csv` was byte-identical across runs:

| file | sha256 |
|---|---|
| `results/CLUSTER_RESULTS.csv` | `2cbc47a42245dc91b28e26fa9ccb9d254657c8004e5d2bf8a345280131ddd031` |
| `results/Y2_COUNTRY_COVERAGE.csv` | `530d16d113682530701d44e839df956efcca240bbcf77d0032765d52a9277cf3` |
| `results/Y2_LAG_MATRIX.csv` | `3ae694c1aed8e652ac37e12b60c94255f233d4723600b5c9b650487123ab9edb` |
| `results/Y2_MATRIX_WIDE.csv` | `36ed247b91a040e43ed74ebf189c6aa86c7acd902bb43184ab409cfd77566ede` |
| `results/Y2_PAIR_VERDICTS.csv` | `ca357be3468d8c141ee0c95fde353ccaae9b88c0f2a30bf6bb2ac5e7aa9921ed` |
| `results/Y2_SENSITIVITY.csv` | `f984929424ad24f97b5d0c6fa386fd9a0319747066b150b1d89fb5e0d6839773` |
| `results/Y2_SUMMARY.csv` | `befedaf29af924e66a03b3568ad0b21174d3f9cc382e4febcee1a6f8d67460e4` |
