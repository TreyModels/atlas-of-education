# PRE-REGISTRATION — E8 Fisher randomization inference (placebo permutations)

**Branch:** `research/e8-fisher-ri-2026-11-25` (additive, no force). **Record:** `research/records/2026-11-25-e8-fisher-ri/`.
**Base:** `origin/research/e6e8-sequencing-2026-11-25` @ `bd782be` (the E8 record and the cited `e8_fee_event_study.py`).
**Date:** 25 November 2026. **Author:** `e8-fisher` (delegated lane; Lead: `lead`).

**Status: written and committed BEFORE any analysis run.** No E8 statistic, permutation, or download-derived number
was computed when this file was committed. The only numbers quoted below are copied from the already-committed E8
record (`results/e8_event_SE.PRM.ENRR_verified8.csv` @ `bd782be`); they are the reproduction targets, not new results.

**Language rule:** association only. Permitted: "consistent with", "is followed by", "the estimate at event time e
is". Forbidden: "effect of abolition", "caused", "drives", "led to". Failures and nulls are reported, never dropped.

---

## 1. Purpose and scope

E8's published inference is a country-cluster bootstrap on the Callaway–Sant'Anna (CS) event-study estimates. This
record adds an **independent, design-based inferential check**: Fisher randomization inference (RI) over two
pre-registered placebo re-assignments of the fee-abolition treatment. It does **not** re-estimate or replace the
published E8 results; it asks whether the observed CS statistic is unusual relative to placebo assignments generated
by a fixed rule. RI's null is a sharp null of no country-specific treatment-time association, evaluated on the same
outcome panel and the exact same estimator.

Outcome: **WDI primary GER (`SE.PRM.ENRR`)**, annual, SSA sample, 1990–2015 — the E8 primary outcome. The secondary
outcome (`SE.SEC.ENRR`) is **out of scope** for this record (no extra permutation run; it is not used).

## 2. Data (committed, exact)

- Source: World Bank WDI bulk CSV for `SE.PRM.ENRR`,
  `https://api.worldbank.org/v2/en/indicator/SE.PRM.ENRR?downloadformat=csv` (raw zip hashed in `data/SHA256SUMS`).
- Acquisition script: `data/acquire_wdi.py` (downloads, unzips to `data/wdi_SE.PRM.ENRR/API_*.csv` +
  `Metadata_Country_*.csv`, builds the panel).
- Exact long panel used, committed as **`data/e8_primary_ger_panel.csv`** with columns `iso3,year,value` (years
  1990–2015, all countries present in the raw series; the analysis uses the same SSA filter as E8). Region map used
  for the SSA filter committed as `data/wdi_region_map.csv` (iso3, `Region`), extracted from the same metadata file.
- **No statistic is computed on data that is not committed.** The committed panel is byte-verified against the raw
  download inside the reproduction gate (`scripts/repro_gate.py`), and the gate's output is committed.

## 3. Estimator (cited, not rebuilt)

Exactly `att_cs` from `research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py` @ **`bd782be`**:
Callaway–Sant'Anna ATT(g,t) with a **universal base period g−1** and **not-yet-treated controls** (never-treated
allowed; minimum 3 controls), event time `e = −5..+6`, and **cohort-size-weighted event-time aggregation**
(`np.average(att, weights=cohort-share)`). Treated set: the 8 source-verified dates (MWI 1994, ETH 1995, UGA 1997,
LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005); the 4 unresolved-date countries (CMR, ZMB, RWA, BDI) are
never-treated controls, exactly as in the E8 main specification.

`e8_ri.py` calls a vectorised re-implementation of the same arithmetic for the 20,000 permutations and must verify it
equals the imported `bd782be` `att_cs` output on the observed assignment to **max abs difference < 1e-10** before any
permutation runs; that check is written to `results/e8_ri_results.json`. If the re-implementation cannot be verified
equal, it is not used and the cited pandas `att_cs` is used directly (documented in the report).

## 4. Reproduction gate (mandatory, BEFORE permutations)

Run the cited `att_cs` (and `boot_rep` for the SE) from `e8_fee_event_study.py` @ `bd782be` on the committed panel
and require, on `SE.PRM.ENRR`, dates = verified-8:

1. `ATT(e=0) = 12.44362392207772` within `1e-6` (published: 12.44);
2. every one of the 11 event-time ATTs (`e = −5..+6`) within `1e-6` of the committed
   `results/e8_event_SE.PRM.ENRR_verified8.csv` @ `bd782be`;
3. `SE_boot(e=0)` = `7.550738928931049` within `1e-6` (published: 7.55), using the same seeds `1000+i`, `i=0..499`,
   and `Pool(8)` code path;
4. the committed panel equals the raw-download long panel exactly (0.0 difference) on the common grid.

**Gate outcome rule:** if any check fails, **STOP**: no permutation run is executed, the failure is committed and
reported as a failure (no re-download with a different vintage, no sample or estimator tweak). If the gate passes,
the gate JSON is committed before the permutation results. The committed E8 record's own data vintage is not
recorded, so a vintage mismatch is a possible, reportable failure mode.

## 5. Test statistics (fixed)

For an assignment `A` (cohort-dates map), let `ev(e; A)` be the CS event-time ATT, estimated on the fixed committed
panel.

- **Primary statistic `T0(A) = ev(0; A)`** — CS ATT at event time `e = 0` (the abolition year, `t_abolition`).
- **Secondary statistic `Tpost(A) = mean{ ev(e; A) : e = +1,...,+6 }`** — unweighted mean over the available
  post-abolition event rows (event rows with no estimable cohort are skipped by the estimator, as in E8).
- Observed values: `T_obs = T(A_observed)` for the verified-8 assignment `A_observed`.

## 6. Permutation families (fixed)

Both families use **B = 10,000 permutations each**. The panel, the SSA sample, the estimator and the statistics are
identical across families; only the treatment assignment is re-drawn.

### 6a. Family P1 — **placebo-date** (`B = 10,000`)

- The 8 verified countries stay treated; only their abolition dates are re-drawn.
- **Feasible window for country `c`:** all years `y` in the closed integer range **`1990..2010`** such that the
  committed `SE.PRM.ENRR` panel has a non-missing value for `c` in **both** `y−1` (the universal base year) and `y`
  (event 0), and **excluding `y ∈ {g_c−2, ..., g_c+2}`** (the true date ±2 years) where `g_c` is that country's
  verified date. This yields the country-specific set `W_c`; if `W_c` is empty the country is not re-dated (and this
  is reported). The upper bound 2010 leaves at least 5 post years inside the 2015 panel end.
- **Draw rule:** for each permutation, draw each treated country's date **independently and uniformly** from its own
  `W_c`; countries are processed in ascending ISO3 order, each consuming one `rng.integers(0, len(W_c))` draw from
  that permutation's RNG. Dates may coincide across countries (independent draws; no rejection).
- Non-drawn countries remain never-treated controls. Missing-data rows are dropped by the estimator exactly as in the
  observed statistic; effective cohort counts are recorded per permutation.
- Interpretation: tests whether the observed date assignment is unusual relative to plausible dates in the same
  feasible window.

### 6b. Family P2 — **placebo-country** (`B = 10,000`)

- The 8 verified **dates are kept**; the treatment **labels are re-assigned to other countries**.
- **Candidate pool `P`:** all countries in the E8 sample (SSA ∩ committed panel, 1990–2015) that are **not** in the
  8 verified-treated set, i.e. **never-treated in the E8 main specification**. This includes the 4 unresolved-date
  countries, because the observed main specification also treats them as never-treated controls. `|P|` is recorded.
- **Draw rule:** draw 8 countries from `P` uniformly **without replacement**; assign the multiset of the 8 observed
  dates (all distinct: 1994, 1995, 1997, 2000, 2001, 2003, 2004, 2005) to the 8 drawn countries by a **uniformly
  random bijection** (permutation of the date vector). The original 8 countries become never-treated controls in
  that permuted world.
- No rejection sampling for data availability; missing rows are dropped by the estimator exactly as in P1.
- Interpretation: tests whether the observed country assignment is unusual relative to randomly chosen never-treated
  SSA countries carrying the same date pattern.

## 7. Random seeds (exact, deterministic)

- **Master seed: `20261125`.** One independent RNG stream per permutation; the stream depends only on
  `(master seed, family code, permutation index)`, so results are invariant to parallel scheduling and chunk order.
- Family codes: `1` = placebo-date (P1), `2` = placebo-country (P2).
- Derivation: `rng = numpy.random.default_rng([20261125, family_code, i])` for permutation `i = 0,...,9999`
  (list-seeded `SeedSequence` entropy). Draw order within a permutation: P1 — treated countries in ascending ISO3
  order; P2 — first the 8-country subset (`rng.choice(P, size=8, replace=False)` on P sorted ascending ISO3), then
  the date bijection (`rng.permutation(8)` applied to the date vector in the ISO3 order of the drawn countries).
- Worker count is a performance setting only; it must not affect any number.

## 8. P-values and Monte Carlo error (fixed formulas)

Let `k = #{ i : |T_perm,i| >= |T_obs| }` and `k+ = #{ i : T_perm,i >= T_obs }`, with `B_eff` the number of
permutations producing a defined statistic (undefined permutations are excluded from both numerator and denominator,
and `B_eff` is reported; expected to be rare/none).

- **Two-sided:** `p2 = (1 + k) / (B_eff + 1)`.
- **One-sided-positive:** `p+ = (1 + k+) / (B_eff + 1)`.
- **Monte Carlo SE of a reported p:** `MCSE(p) = sqrt( p·(1−p) / (B_eff + 1) )`.
- Also reported: permutation distribution count/mean/SD/min/max, quantiles (2.5%, 5%, 25%, 50%, 75%, 95%, 97.5%),
  and `#{T_perm >= T_obs}`. All four p-values (2 statistics × 2 families × 2 sides = 8) are reported.
- No multiplicity correction is applied; the four pre-registered two-sided p-values are reported individually and
  interpreted against the fixed decision rule below.

## 9. Decision / reporting rule (pre-registered)

Classification of the observed **primary statistic `T0`**, using the four pre-registered two-sided p-values:

- **`robust`** — `p2_date(T0) < 0.05` **and** `p2_country(T0) < 0.05` **and** `p2_date(Tpost) < 0.05` **and**
  `p2_country(Tpost) < 0.05`.
- **`partially robust`** — `p2_date(T0) < 0.05` **and** `p2_country(T0) < 0.05`, but the full `robust` condition
  fails (i.e. at least one `Tpost` p ≥ 0.05).
- **`not distinguishable from placebo`** — `T0` has a two-sided p ≥ 0.05 in at least one family.

Reporting obligations, fixed now:
- Report the classification verbatim, plus all p-values, MCSEs, quantiles and effective-n.
- Under `robust`: the E8 primary estimate may be described as "consistent with a date-specific association" with the
  RI check passing both placebo schemes. Under `partially robust`: the report must say the RI check is
  statistic/scheme-dependent. Under `not distinguishable from placebo`: the report must say that the date-specific
  association is **not supported by randomization inference**, and the E8 first-stage claim is downgraded to
  descriptive.
- The published E8 point estimates and bootstrap CIs stand as published; RI p-values are a separate inferential
  check, not a replacement. No causal language. No change to the E8 estimator, sample, dates, or panel after seeing
  p-values. No adjustment of `B`, the window, the ±2 exclusion, or the statistics post hoc.
- Any deviation from this pre-registration is listed in `REPORT.md` §"Deviations" with the reason and the effect.

## 10. `t*` leg — registered as NOT-ESTIMABLE

The bulge-arrival quantity `t* = t_abolition + L_primary` is **NOT-ESTIMABLE** in this record and is reported as such,
without proxy, imputation or a "standard cycle length" fill-in. `t_abolition` is sourced 8/8
(`data/fee_dates.csv` @ `bd782be`, `status=VERIFIED`); **`L_primary` is sourced 0/8**: no committed repo file states
primary-cycle length by country-year for these 8 (see `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` §3 and
`paper2/BULGE_ARRIVAL_STATUS.md` @ `origin/research/bulge-arrival-2026-11-25` @ `1b91a71`). Registered consequence:
`t*` status = NOT-ESTIMABLE, `L_primary` = 0/8, no `t*`-centred estimate is computed anywhere in this record.

## 11. Outputs

- `data/acquire_wdi.py`, `data/e8_primary_ger_panel.csv`, `data/wdi_region_map.csv`, `data/SHA256SUMS`.
- `scripts/repro_gate.py` → `results/repro_gate.json`.
- `scripts/e8_ri.py` → `results/e8_ri_results.json`, `results/e8_ri_perms.csv.gz` (per-permutation `T0`, `Tpost`,
  effective cohort counts; 40,000 rows).
- `REPORT.md` with the observed statistics, placebo distributions, p-values (two- and one-sided), MCSEs, gate
  outcomes, the `t*` NOT-ESTIMABLE section, limitations, and a deviations section.

## 12. Environment and compute

Host python `/Users/treymenefee/neon-boot/venv/bin/python` (numpy 2.2.6, pandas 2.3.3, scipy 1.15.3) is sufficient;
the warm AutoDL box may be used for the 20,000 permutations if its python environment is usable. Multiprocessing is
a performance setting only. No shutdown/reboot/power command and no watcher/timer/cron is created by this record.
