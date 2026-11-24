# REPORT — E8 Fisher randomization inference (placebo permutations)

**Record:** `research/records/2026-11-25-e8-fisher-ri/`. **Branch:** `research/e8-fisher-ri-2026-11-25`.
**Base:** `origin/research/e6e8-sequencing-2026-11-25` @ `bd782be` (E8 record and cited estimator).
**Pre-registration:** `PRE_REGISTRATION.md`, commit **`4e466a3`** — written and committed **before any analysis
run** (the only commit in this record that precedes the data/gate commit).
**Data + reproduction-gate commit:** **`263bef2`**. **Results commit:** branch head containing this report.
**Date:** 25 November 2026. **Author:** `e8-fisher` (delegated lane; Lead: `lead`).

**Language rule:** association only. The strongest reading permitted and used here is **"consistent with"**.
No causal claim is made. This record adds an inferential check; it does not re-estimate, replace, or re-interpret
the published E8 point estimates and bootstrap CIs as causal effects.

---

## 1. Purpose and scope

E8's published inference is a country-cluster bootstrap on Callaway–Sant'Anna (CS) event-study estimates. This
record adds an independent, design-based **Fisher randomization inference (RI)** check over two pre-registered
placebo re-assignments of the fee-abolition treatment, on the same committed outcome panel and the exact same
estimator:

- **Primary statistic `T0`** = CS ATT at event time `e = 0` (the abolition year).
- **Secondary statistic `Tpost`** = unweighted mean of CS event ATTs at `e = +1..+6`.
- **Families:** P1 placebo-date and P2 placebo-country, **B = 10,000 each**, master seed **20261125**, per-permutation
  RNG `numpy.random.default_rng([20261125, family_code, i])`.
- **p-values:** two-sided `p2 = (1 + #{|T_perm| ≥ |T_obs|}) / (B_eff + 1)`; one-sided-positive
  `p+ = (1 + #{T_perm ≥ T_obs}) / (B_eff + 1)`; Monte Carlo SE `sqrt(p(1−p)/(B_eff+1))`.

Everything above (including the placebo-date windows, the ±2-year exclusion, the placebo-country pool and draw rule,
the decision rule, and the stop-on-gate-failure rule) was fixed in `PRE_REGISTRATION.md` before the data were
downloaded or any statistic was computed. Outcome: WDI primary GER (`SE.PRM.ENRR`), annual, SSA sample, 1990–2015,
verified-8 dates. The secondary E8 outcome (`SE.SEC.ENRR`) is out of scope and was not permuted.

**Estimator (cited).** `att_cs` from
`research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py` @
**`bd782be4d15c834f054b1ecc650e54565f6b292f`**: CS ATT(g,t) with universal base period `g−1`, not-yet-treated
controls (never-treated allowed, ≥3 controls), event time `−5..+6` (event `−1` is not estimable in that code because
`t = g−1` is the base period), cohort-size-weighted event aggregation. `scripts/e8_ri.py` re-implements the same
arithmetic vectorised for the 20,000 permutations and **verifies it against the cited `att_cs`** on the observed
assignment: max abs difference **7.11e-15** across all 11 event ATTs (`T0` diff 0.0, `Tpost` diff 3.6e-15;
tolerance 1e-10), recorded in `results/e8_ri_results.json -> verifier`.

---

## 2. Data and reproduction gate (must pass before permutations)

**Data.** WDI bulk CSV for `SE.PRM.ENRR`, `https://api.worldbank.org/v2/en/indicator/SE.PRM.ENRR?downloadformat=csv`,
download vintage **Last Updated 2026-11-11**, raw zip sha256 `ca495dfe…`; committed as exactly the panel used:
`data/e8_primary_ger_panel.csv` (4,836 rows, 251 countries, 1990–2015, sha256 `365bcd43…`), with
`data/wdi_region_map.csv` (SSA filter; 48 SSA countries in the analysis sample), `data/acquire_wdi.py`, and
`data/SHA256SUMS`. Raw downloads are re-obtainable from the pinned URL and verified against the pinned hash; they are
kept out of git. The gate compares the committed panel to a fresh parse with **0.0** difference.

**Gate command (host):** `/Users/treymenefee/neon-boot/venv/bin/python scripts/repro_gate.py` →
`results/repro_gate.json`, `gate_pass = true`.

| gate check | reproduced | committed / published | max abs diff | result |
|---|---|---|---|---|
| CS `ATT(e=0)` | `12.44362392207772` | `12.44362392207772` (published 12.44) | `0.0` | PASS |
| `SE_boot(e=0)` (500 cluster bootstraps, seeds 1000+i, Pool(8)) | `7.550738928931049` | `7.550738928931049` (published 7.55) | `0.0` | PASS |
| all 11 event-time ATTs (`e=−5..+6`) | — | `results/e8_event_SE.PRM.ENRR_verified8.csv` | `2.220e-16` | PASS (tol 1e-6) |
| all `ATT(g,t)` rows | — | `results/e8_att_gt_SE.PRM.ENRR_verified8.csv` | `<1e-6` | PASS |
| committed panel vs raw download | — | `data/e8_primary_ger_panel.csv` | `0.0` | PASS |
| cited script blob | — | `bd782be:…/e8_fee_event_study.py` | blob match | PASS |

Sample: SSA ∩ panel **n = 48** countries, **8** verified-treated countries in the panel, **40** never-treated
placebo-country candidates. The gate **passed**, so permutations were run; if it had failed the pre-registered rule
was to stop and report the failure with no permutation run.

---

## 3. Observed statistics (the RI comparators)

| statistic | value (pp) | definition / effective n |
|---|---|---|
| `T0` | **12.44362392207772** | CS cohort-weighted event ATT at `e = 0`; **7 cohorts** contribute |
| `Tpost` | **25.260746369507263** | unweighted mean of event ATTs `e = +1..+6`; all six event rows estimable |

Event ATTs used (`e`: ATT): `−5`: 6.3894, `−4`: 1.3454, `−3`: −0.1283, `−2`: −0.0270, **0**: 12.4436,
`+1`: 23.8244, `+2`: 25.9429, `+3`: 22.1208, `+4`: 25.1932, `+5`: 28.5608, `+6`: 25.9224. These reproduce the
published E8 verified-8 table (see gate). **Disclosure:** MOZ 2004 has no 2003 (base-year) observation, so MOZ
contributes no event rows and the observed statistics are 7-cohort weighted averages; this is the same behaviour as
the published result (`n_treated = 7` at `e = 0`) and no value was imputed.

---

## 4. Permutation design as executed

- **P1 placebo-date (10,000):** the 8 verified countries stay treated; each date is redrawn independently and
  uniformly from `W_c = {y ∈ 1990..2010 : outcome non-missing in y−1 and y} \ {g_c−2 … g_c+2}`, countries in
  ascending ISO3 order. Window sizes: ETH 15, GHA 12, KEN 11, LSO 15, MOZ 12, MWI 11, TZA 15, UGA 15 (none empty).
- **P2 placebo-country (10,000):** the 8 dates are kept; 8 countries are drawn without replacement from the 40
  never-treated SSA countries (`P` sorted ascending ISO3) and the dates are assigned by a uniform random bijection in
  ISO3 order. The original 8 countries become never-treated controls.
- Undefined statistics are excluded and `B_eff` reported (none occurred: `B_eff = 10,000` for all four cells).
- Multiprocessing (8 host workers) is a performance setting only; per-permutation RNG makes results invariant to
  scheduling. Determinism spot checks (permutations 0, 5000, 9999 in each family, recomputed serially in the parent)
  match the stored CSV to **0.0**.
- Total runtime ≈ 26 s on the host.

---

## 5. RI results

Permutation distributions and p-values (`results/e8_ri_results.json`, `results/e8_ri_summary.csv`,
per-permutation draws in `results/e8_ri_perms.csv.gz`, 20,000 rows — 2 families × B=10,000 permutations; `T0`/`Tpost`
are columns):

| family | statistic | `T_obs` | perm mean | perm SD | min | max | q2.5 | q50 | q97.5 | #(\|T_perm\|≥\|T_obs\|) | B_eff | **p2** | **p+** | MCSE(p2) | MCSE(p+) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| placebo-date | `T0` | 12.4436 | −0.9021 | 1.2504 | −5.6765 | 3.7839 | −3.3147 | −0.9054 | 1.5791 | 0 | 10,000 | **9.999e-05** | **9.999e-05** | 1.00e-04 | 1.00e-04 |
| placebo-date | `Tpost` | 25.2607 | −2.5383 | 3.7550 | −14.0150 | 14.1795 | −8.7078 | −3.0341 | 5.9596 | 0 | 10,000 | **9.999e-05** | **9.999e-05** | 1.00e-04 | 1.00e-04 |
| placebo-country | `T0` | 12.4436 | −0.4028 | 2.1487 | −6.5522 | 17.4027 | −3.7844 | −0.7095 | 4.8831 | 5 | 10,000 | **5.999e-04** | **5.999e-04** | 2.45e-04 | 2.45e-04 |
| placebo-country | `Tpost` | 25.2607 | −1.0433 | 5.1683 | −31.5059 | 26.8083 | −10.9730 | −1.1642 | 9.5478 | 2 | 10,000 | **2.9997e-04** | **2.0e-04** | 1.73e-04 | 1.41e-04 |

Full quantiles (2.5/5/25/50/75/95/97.5) are in `results/e8_ri_summary.csv`; effective-cohort distributions:
P1 `n_t0 = 8` in every permutation; P2 `n_t0` mean 5.51 (min 1, max 8) because kept dates land on drawn countries
with data gaps (no imputation — the estimator's skip rule applies exactly as in the observed run); P2 `n_post_events`
mean 6.00 (min 5).

**Reading.** Under both placebo schemes the observed statistics sit far in the upper tail: no placebo-date draw and
5/10,000 placebo-country draws reach `|T0_obs|`; 0 and 2/10,000 reach `|Tpost_obs|`. `p2 = 9.999e-05` is the exact
resolution floor `1/(B+1)`, i.e. **"no placebo draw reached the observed statistic"**, not an estimate that the tail
probability is zero; its MCSE is 1.0e-4. The placebo-country distribution is wider and has a heavier right tail
(mean −0.40, SD 2.15 for `T0`; max 17.40), so its p-values are larger (`5.999e-04` / `2.9997e-04`) but still below
0.05.

---

## 6. Pre-registered decision

Rule (`PRE_REGISTRATION.md` §9): `robust` = all four two-sided p-values `< 0.05`; `partially robust` = `T0` both
families `< 0.05` but not all four; otherwise `not distinguishable from placebo`.

| condition | value | met |
|---|---|---|
| `p2_date(T0) < 0.05` | 9.999e-05 | yes |
| `p2_country(T0) < 0.05` | 5.999e-04 | yes |
| `p2_date(Tpost) < 0.05` | 9.999e-05 | yes |
| `p2_country(Tpost) < 0.05` | 2.9997e-04 | yes |

**Classification (verbatim): `robust`.** Pre-registered implication: *"consistent with a date-specific association;
RI passes both placebo schemes."* This is an association reading only. It does **not** establish a causal effect,
does not replace the published bootstrap CIs (which remain wide: `T0` CI includes zero), and is conditioned on the
two placebo schemes and the 40-country never-treated pool (see Limitations).

---

## 7. `t*` leg — **NOT-ESTIMABLE**

`t* = t_abolition + L_primary` is reported as **NOT-ESTIMABLE** in this record, with **no proxy, imputation, or
"standard cycle length" fill-in**:

| component | sourced | note |
|---|---|---|
| `t_abolition` | **8 / 8** | `data/fee_dates.csv` @ `bd782be`, `status=VERIFIED` |
| `L_primary` | **0 / 8** | no committed repo file states primary-cycle length by country-year for these 8 |
| `t*` | **0 / 8** | therefore excluded by the pre-registered sourcing rule |

Citation: `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` §3–4 and `paper2/BULGE_ARRIVAL_STATUS.md` §A–B @
`origin/research/bulge-arrival-2026-11-25` @ `1b91a71`. The bulge-arrival pre-registration records the same data
gate as failed and registers `t*` as NOT-ESTIMABLE; auditor-supplied cycle-length candidates are recorded there as
**unadopted candidates**. No `t*`-centred estimate is computed anywhere in this record.

---

## 8. Reproducibility

```
# host, from this record root
/Users/treymenefee/neon-boot/venv/bin/python data/acquire_wdi.py     # download + pin + build committed panel
/Users/treymenefee/neon-boot/venv/bin/python scripts/repro_gate.py   # gate PASS required (results/repro_gate.json)
/Users/treymenefee/neon-boot/venv/bin/python scripts/e8_ri.py        # 2 x 10,000 permutations (~26 s)
```
`acquire_wdi.py` must run first: `repro_gate.py` checks the committed panel against the gitignored raw extract
`data/wdi_SE.PRM.ENRR/` that the acquisition step creates and hash-pins.
Environment: host python `/Users/treymenefee/neon-boot/venv/bin/python`, numpy 2.2.6, pandas 2.3.3. Hashes:
perms CSV `9d04926c…`, summary CSV `afb4e29c…`, panel `365bcd43…` (recorded in `results/e8_ri_results.json ->
files`). Determinism: per-permutation seed derivation, spot-checked at permutations 0/5000/9999 per family (diff 0.0).

---

## 9. Limitations and disclosures

1. **Small treated sample.** 7–8 treated countries and a 48-country SSA sample; RI p-values complement, and do not
   replace, the published wide bootstrap CIs (`T0` CI includes zero). The `e=0` statistic is the least stable
   estimate; the larger post-period values dominate `Tpost`.
2. **Missing-data asymmetry across the placebo worlds.** Observed `T0` uses 7 cohorts (MOZ 2004 lacks a 2003 base
   year); P1 permutations all use 8 cohorts at `e=0` (each window year guarantees a base year); P2 `n_t0` varies
   (mean 5.51, min 1). The estimator's skip behaviour is identical throughout and nothing is imputed, but the
   comparability of effective n across observed/placebo worlds is a genuine limitation, not corrected post hoc.
3. **Exchangeability assumptions.** P1 treats dates as exchangeable within each country's feasible window (after
   excluding the true date ±2); P2 treats never-treated SSA countries as exchangeable carriers of the same 8-date
   pattern. Both are strong; the p-values are conditional on these pre-registered schemes.
4. **Control-pool contamination risk.** The 4 unresolved-date countries (CMR, ZMB, RWA, BDI) are never-treated
   controls in the E8 main specification and in `P`, exactly as in the observed statistic; if any of them actually
   abolished fees in-window, both the control pool and `P` are contaminated. The direction is not signed.
5. **Outcome and estimator fixed.** One outcome (WDI gross primary GER; labelled OBSERVED, modelled where WDI says
   modelled), one estimator (CS, universal base `g−1`, not-yet-treated controls), one event window. No
   specification search was performed, and none of the published E8 numbers was changed.
6. **Data vintage.** Pinned to WDI Last Updated 2026-11-11; the gate confirms the committed E8 verified-8 numbers
   reproduce exactly on this vintage. A future WDI revision would change the panel, and `acquire_wdi.py` will
   refuse to rebuild silently (pinned hash).
7. **p-value resolution.** With B = 10,000 the smallest attainable two-sided p is 9.999e-05 (MCSE 1.0e-4). The
   placebo-date result is at that floor, so it should be read as "no placebo draw in 10,000 reached the observed
   statistic", not as a precise tail probability.
8. **Decision-rule label.** `robust` is the pre-registered reporting label, not a significance claim beyond the four
   reported p-values; no multiplicity correction was registered, and all p-values (two- and one-sided, both
   statistics, both families) are reported.
9. **No causal language.** "Consistent with" is the strongest reading used. The record makes no claim that fee
   abolition caused the observed GER movements.

**Deviations from the pre-registration: none substantive.** The only additions are an extra flat summary table
(`results/e8_ri_summary.csv`; no new statistics) and recording the reproduction-gate summary inside the RI JSON.

**Documentation erratum (numeric, no effect on results).** `PRE_REGISTRATION.md` §11 forecast "40,000 rows" for the
per-permutation CSV. That was a 2× bookkeeping error — `T0` and `Tpost` are columns of the same 20,000 permutation
rows (2 families × B = 10,000), not extra rows; the committed `results/e8_ri_perms.csv.gz` has exactly 20,000 data
rows. The pre-registration text is left as committed (unchanged); no statistic, p-value, draw, or label is affected.

---

## 10. Claims → source map

| claim | value | source file | field |
|---|---|---|---|
| observed `T0` | 12.44362392207772 | `results/e8_ri_results.json` | `observed.T0` |
| observed `Tpost` | 25.260746369507263 | `results/e8_ri_results.json` | `observed.Tpost` |
| `p2(T0)`, placebo-date | 9.999e-05 | `results/e8_ri_results.json` | `families.placebo_date.T0.p_two_sided` |
| `p+(T0)`, placebo-date | 9.999e-05 | same | `…T0.p_one_sided_positive` |
| `p2(Tpost)`, placebo-date | 9.999e-05 | same | `families.placebo_date.Tpost.p_two_sided` |
| `p2(T0)`, placebo-country | 5.999e-04 | same | `families.placebo_country.T0.p_two_sided` |
| `p2(Tpost)`, placebo-country | 2.9997e-04 | same | `families.placebo_country.Tpost.p_two_sided` |
| `p+(Tpost)`, placebo-country | 2.0e-04 | same | `…Tpost.p_one_sided_positive` |
| MCSEs | 1.00e-04 / 2.45e-04 / 1.73e-04 / 1.41e-04 | same | `…mcse_two_sided`, `…mcse_one_sided_positive` |
| B_eff | 10,000 (all cells) | same | `families.*.B_eff_*` |
| quantiles, means, SDs | table §5 | `results/e8_ri_summary.csv` | per-row fields |
| classification | `robust` | `results/e8_ri_results.json` | `decision.classification` |
| gate values | ATT0 exact, max\|ΔATT\| 2.220e-16 | `results/repro_gate.json` | `estimator_reproduction.*` |
| `t*` | NOT-ESTIMABLE, `L_primary` 0/8 | `results/e8_ri_results.json` | `t_star.*` |
