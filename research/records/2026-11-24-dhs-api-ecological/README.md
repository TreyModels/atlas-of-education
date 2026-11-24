# DHS public-API ecological sprint — record (2026-11-24, corrected + African-11 extension)

**Tasks:** task-16 (full public-API replication + construct split) and task-36 (11-country extension, access
follow-up, execution-ready individual test). **Branch:** `research/dhs-api-ecological-2026-11-24`.
**Status:** complete; numbers **corrected** after a fixed-effect bug fix (see below); estimates computed on the
server boxes, **never on the Mac**.

> **25 Nov 2026 append:** a second correction (cluster-bootstrap multiplicities, Neon audit item 1) is recorded in
> [`CORRECTED_RUN_2026-11-25.md`](CORRECTED_RUN_2026-11-25.md) — **provisional** until Neon's diff is applied.
> It moves the intervals (Africa-11 2-group ratio now includes 1.0) and the D4 wanted-vs-actual gap (~−0.196).

**One line:** in **all** DHS survey rounds the public API publishes with education breakdowns (369 surveys,
87 countries, 1985–2025), schooling is associated with **−1.58 children** (secondary vs none, within survey);
**98.8 % of 346 surveys** show a negative per-survey gradient; the result survives country FE, period FE and
country trends; it is the **same** for period TFR and cumulative completed fertility (standardised ratio
**1.003 [0.932, 1.077]**); the **wanted-fertility** gradient is materially weaker (−0.078 SD, p=0.0004); and the
**surviving-children** series is demonstrably different from TFR (corr 0.82; median gap 0.63 children). In the
**11 African countries** the gradient is steeper and the cohort pattern **steepens** rather than attenuates.
Everything is **OBSERVED / ECOLOGICAL**; no causal language; **not** a substitute for the blocked individual test.

## Read in this order

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | Main report: headline numbers, Q1 gradient + heterogeneity, Q2a window contrast, Q2b construct contrasts, cohort proxy, D1–D7 scorecard, limits, reproduction. **§0 is the correction notice — read it before quoting numbers.** |
| [`BUGFIX_FE_PARAMETERISATION.md`](BUGFIX_FE_PARAMETERISATION.md) | The estimator bug found and fixed after the first commit: what was wrong, how it was caught (validation against the prior record), old vs new numbers, verdict changes (D6), files superseded |
| [`AFRICA11_EXTENSION.md`](AFRICA11_EXTENSION.md) | task-36: the 11 African countries (MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA, BEN, NAM, SWZ) with the same construct split — Q1, Q2a, Q2b, cohort, heterogeneity, caveats |
| [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) | Fixed before any value was pulled (`88073d0`) |
| [`AMENDMENT_01.md`](AMENDMENT_01.md) | Pre-estimation data-availability amendment (`856c421`): denominators, hidden second dimension |
| [`data/`](data/README.md) | Cached public-API JSON, panels, checks, `MANIFEST.sha256` — **no microdata** |
| [`scripts/`](scripts) | `pull_dhs_api.py`, `build_panel.py`, `estimate.py` (corrected), `corrected_reduction.py` (independent cross-check) |
| [`results/`](results) | Corrected full-sample results, `africa11/`, `corrected/` cross-check, `server_box2/` logs; the first run's logs are kept as `server_superseded_biased/` |

## Compute / provenance

- Pull (network only) and `build_panel.py` on the Mac; **all estimation on servers**: first run region-42
  (`results/server_superseded_biased/`), corrected run on `connect.cqa1` box (`results/server_box2/`), 8 workers,
  24 s full sample / 13 s African-11, numpy 1.24.1 (local 1.24.3 — coefficients identical to 4 dp).
- No Mac compute (the earlier local attempt was killed and never resumed). No credentials, no gated files, no
  synthetic data.
- Cross-check: a second, independently written implementation reproduces every reported point estimate exactly
  and validates the estimator against the prior record (max |Δ| 0.0036).
