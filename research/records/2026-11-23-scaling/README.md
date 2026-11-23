# Scaling laws in our data: what is a law, what is only a regularity, what we cannot test

**Task 19**, branch `research/scaling-2026-11-23`, 23 Nov 2026. **Pre-registration:** committed
before any result (`f8f782f`, `PREREGISTRATION.md`). **Compute:** box2 only, 2 cores, single process.
**Data:** our country panel in `/root/work/data`, the prior project copied to
`/root/work/local_data/10_massification/` (used first, never re-derived), ILOSTAT occupation counts
pulled fresh from the public API, and GeoNames city populations (attempted; failed — see gaps).
**Rule applied** (from `10_massification/lit/SCALING_LAWS.md`): a *law* is a power law whose exponent
is stable across samples and estimators and which has an interpretation; a *regularity* is a stable
pattern without that; a *threshold* is a descriptive cut-point. We add one criterion: an exponent
that is strong between countries but weak or different inside countries is a between-country
regularity, not a law about what happens as a country grows. **A scaling regularity is not a causal
identification.**

## Data availability (what was used, where it came from)

| data | source (used vs downloaded) | coverage | used for |
|---|---|---|---|
| local scaling tables | `/root/work/local_data/10_massification/` (`relations/data/scaling_laws.csv` 30 within/between estimates, `model2/runs/scaling_classification.csv` 18 pairs × 5 estimators, `lit/SCALING_LAWS.md`) | 30 countries, 1970–2024 | consolidation, verdict rule |
| fertility, schooling, gender parity, urban share, GDP p.c. (levels), tax share | `/root/work/data/*.json` (programme panel) | 1960–2024, 246–261 areas | collapse curve, urbanisation–income, Mincer proxy, Wagner |
| occupation counts by ISCO-08 major group | ILOSTAT public API (`rplumber.ilo.org`), pulled fresh | 295 areas, 1969–2025; 151 countries usable | Heaps/rarefaction, regime break |
| city populations | UN WUP: not reachable (all known URLs 404); GeoNames `.zip` downloads truncated/corrupt twice | — | Zipf/Gibrat **not testable** |
| credential counts, BLS SOC, city GDP/wages/patents | not present on box2 | — | credential inflation, Bettencourt **not testable** |

## Verdict table (all exponents with SE and n; full machine-readable table in `results/consolidated_verdicts.csv`)

| relation | between-country exponent (SE) | within-country exponent (SE) | n / countries | verdict |
|---|---|---|---|---|
| secondary enrolment vs income (S1) | 0.215 (0.035) | 0.090 (0.124) | 1,042 / 30 | between-country regularity; within ≈ 0 |
| tertiary enrolment vs income (S2) | 0.567 (0.082) | 0.848 (0.172) | 1,037 / 30 | law-like candidate (stable both layers) |
| lower-sec completion vs income (S4) | 0.169 (0.034) | 0.247 (0.119) | 629 / 28 | law-like candidate (stable both layers) |
| upper-sec attainment vs income (S5) | 0.312 (0.052) | 0.072 (0.167) | 458 / 30 | between-country regularity; within ≈ 0 |
| services share vs income (S9) | 0.294 (0.039) | 0.275 (0.083) | 510 / 15 | law-like candidate (stable both layers) |
| agriculture share vs income (S7) | −0.990 (0.216) | −0.120 (0.083) | 1,017 / 30 | between-country regularity; within weak |
| education stock vs output (S10) | 1.176 (0.258) | 0.051 (0.108) | 458 / 30 | between-country regularity; within ≈ 0 |
| cohort size (fertility) vs enrolment (S11) | −0.612 (0.127) | −0.006 (0.219) | 1,069 / 30 | between-country regularity; within ≈ 0 |
| urban share vs enrolment (S13) | 0.012 (0.002) | 0.011 (0.004) | 1,069 / 30 | law-like candidate (semi-log; stable both layers) |
| 5-estimator stability test (18 pairs) | — | — | 30 / 30 | 3 called "scaling law (stable across estimators)" (secondary GER, tertiary GER, lower-sec completion vs GDP pc); 14 "period/region regularity"; 1 "unidentified" (primary GER vs income) |

**The discipline result.** Three education–income relations survive the local stability rule, but
only in the between-country cross-section; when the same relation is estimated inside countries, the
secondary-enrolment exponent collapses to zero (0.090, SE 0.124) and the attainment exponent does
too (0.072, SE 0.167). The relations we may call **law-like candidates** are tertiary enrolment,
lower-secondary completion, services employment share and urban share vs enrolment, where within and
between agree. Sector shares and education stocks are **regularities of the cross-section**, not laws
about change. The "levels strong, changes flipped" result from the parallel data job is exactly this
pattern: we reproduce it on our own fertility–attainment panel (below).

## (1) Fertility

**Universal collapse curve: rejected.** 4,394 country–cohort points (158 countries, cohorts born
1950–1996; cohort fertility measured at age 28, female attainment = secondary completion × gender
parity adjustment at age 20). The best common curve is exponential: fertility = 1.13 (SE 0.26) +
5.97 (SE 0.23) × exp(−0.0197 (SE 0.0025) × attainment), pooled R² = 0.78. But country identity
explains **71.6% of the remaining residual variance** (country intercepts R² = 0.914; country-specific
slopes R² = 0.955; slope-heterogeneity F = 46.4 on 313 and 3,717 df). Residual scatter is 0.847
births per woman, 11.2% of the fertility range; after a country-level rescaling it is still 0.434.
Residuals are structured: low-income countries +0.40 births above the common curve, high-income
−0.11; the 1950s cohorts +0.29, the 1970s cohorts −0.17. **Verdict: a common shape with country-
specific levels and slopes, not a single universal curve.**

**Levels vs changes (the scaling-law question).** Between countries the fertility–attainment slope is
−0.479; within countries at levels it is −0.299 (SE 0.026, t = −11.7); for ten-year changes within
countries it is only −0.056 (2,064 changes, 201 countries). The relation exists, but about **a sixth**
as strongly in changes as between countries. A between-country regularity, not a law of change.

**Fertility vs income:** power-law exponent −0.263 (SE 0.013), n = 11,345, 213 countries, R² = 0.50;
a squared term is small but nonzero (+0.0178, SE 0.008) and out-of-sample fit is unchanged (RMSE
0.398 vs 0.397), so a power law with mild curvature is adequate — a regularity, no canonical exponent.

## (2) Massification

**Heaps' law survives the sampling-effort correction, but below the literature band.** Raw distinct
occupational categories per country do not rise with workforce size at all (exponent −0.002): with a
fixed 10-category classification, raw counts are almost pure sampling artefact. The honest object is
the rarefaction curve (expected distinct categories at common sample size). Corrected, the exponent
is **0.333 (SE 0.011), 151 countries, 11,712 curve points**, country-clustered; per-country median
0.374 [IQR 0.319–0.468]. Strongly sublinear (proportional growth rejected, z = −58.8), but below the
0.4–0.6 Heaps range (z = −5.9 against 0.4). **Caveat: the classification is ISCO-08 one-digit only
(10 categories); two- and three-digit ILOSTAT series are deprecated in the public API, so the ceiling
truncates the curve and pushes the exponent down.** This is the best available test, not a clean one.

**Regime change at universalisation: curvature yes, threshold no.** Adding a squared log-size term
gives −0.058 (SE 0.0018, t ≈ −33): the accumulation curve saturates (diminishing returns). Splitting
countries by female attainment gives exponents 0.360 (27 countries, <50%), 0.403 (24, 50–80%),
0.387 (85, >80%): **no significant difference** (Welch t = −1.25, p = 0.22). The pre-registered
regime break at the universalisation threshold is **not found**; saturation is present but it is the
10-category ceiling as much as any theory of high-inhibition systems.

**Urbanisation vs income:** a logistic S-curve beats both a power law and a log-linear line out of
sample (RMSE 0.1523 vs 0.1598 vs 0.1532), n = 10,986, 208 countries; slope 0.572 (SE 0.030),
midpoint $3,647. The S-curve is confirmed, but the gain over a straight line is small — a regularity,
not a scaling law.

**Other development laws:** Wagner fails badly as stored (tax-share elasticity 0.103, SE 0.030,
n = 4,699, 161 countries — nowhere near >1), but the stored tax series has no documented definition,
so this is *not* a clean test. The country-level schooling–income elasticity (0.378, SE 0.027,
n = 5,925, 202) is a between-country association and **must not be read as a Mincer return**.

## What we could not test, and why (stated, not proxied)

- **Zipf/rank-size and Gibrat:** no city-population list. UN WUP is unreachable from box2 (404) and
  GeoNames downloads were truncated/corrupt twice; Gibrat also needs two waves. **Not tested.**
- **Bettencourt superlinear/sublinear scaling (β≈1.15/0.85):** we have no city GDP, wages, patents or
  infrastructure — only country data. Local catalogue verified the literature exponents (0.77–1.34);
  we cannot estimate them. **Not tested.**
- **Credential vs occupation counts:** no Credential Engine or BLS SOC series on box2. **Not tested.**
- **Gravity for migration, school-size economies:** no clean bilateral matrix or school-level data.

## What a scaling law would and would not prove here

A stable exponent would say the relation has a regular functional form across countries and time; it
would **not** identify a mechanism, a cause, or a policy lever, and it would not license transplanting
the urban Bettencourt exponents into schooling. The main finding is a discipline finding: in our own
data, most education and sector "scaling laws" are between-country cross-sectional patterns that
weaken or vanish inside countries, and the one universal collapse the theory wants — fertility on a
single attainment curve — is rejected by the residual structure.

## Files

`PREREGISTRATION.md` (pre-registered patterns, falsifiers, benchmark table); `scripts/analysis.py`
(panel tests: urban–income, Mincer proxy, Wagner, fertility–income, collapse, Heaps, Zipf attempt);
`scripts/consolidate.py` (merges local tables + new tests into verdicts, levels-vs-changes);
`scripts/regime_break.py` (curvature + threshold split); `results/` (`scaling_results.json`,
`consolidated_verdicts.json/.csv`, `regime_break.json`, `ilo_occupation_extract.csv`, `analysis.log`);
`data/` (copies of the local CSVs used, for traceability). Server working copy: `/root/work/scaling`.
