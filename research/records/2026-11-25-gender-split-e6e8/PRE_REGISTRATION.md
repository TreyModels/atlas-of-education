# PRE-REGISTRATION — gender split of the E8 fee-abolition event study (Leg A) + `t*` bulge data gate (Leg B)

**Branch:** `research/gender-split-e6e8-2026-11-25` (base `origin/research/e6e8-sequencing-2026-11-25` @
`bd782be`). **Record:** `research/records/2026-11-25-gender-split-e6e8/`. **Date:** 25 November 2026.
**Author:** `gender-split` (delegated worker; Lead `lead`), task-3.

**Status: written and committed BEFORE any analysis run and before the sex-disaggregated GER panels were
downloaded or opened.** All inputs, samples, estimator settings, the test statistic, the bootstrap, the reporting
rule, and both legs' data gates are fixed here. Deviations, if any, are listed in `REPORT.md` with the reason and
apply only to robustness, never to the pre-registered primary statistic.

Language rule (binding): **association only.** Permitted: "is associated with", "the estimate at event time e
is", "consistent with". Forbidden: "effect of abolition", "caused", "drives", "led to". Nulls and failures are
reported, never dropped.

---

## 0. What is reused, and from where

The estimator is the E8 record's own code, reused **unchanged in logic**: `att_cs(...)` (Callaway–Sant'Anna
ATT(g,t) with universal base period `g−1` and not-yet-treated controls, event time `−5..+6`, cohort-size-weighted
event aggregation), `boot_rep(...)` (country-cluster bootstrap), `load_wdi_outcome(...)`, `load_fee_dates(...)`,
`build_panel(...)` from
`research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py` @ `origin/research/e6e8-sequencing-2026-11-25`
@ `bd782be` (as reviewed in `ERRATUM.md` §B/§D of that record; the file is unchanged at that commit with respect to
estimation). Control-rule detail inherited from that code: controls are all countries not in the treated cohort
set (never-treated) plus treated countries whose abolition year is **strictly later** than `max(t, b)`; a cell is
estimated only when ≥3 controls have both `t` and `b` observed.

Fee dates: the **8 `status=VERIFIED`** rows of
`research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv` @ `bd782be`, sha256
`1a08d4652371f7a3c79a54725b79c48429a793e3d88252d170715018ddd8e2ab` (byte-identical at `bfb8c6f` and `9a0fd69`,
per that record's `ERRATUM.md` §B): MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004,
GHA 2005. The 4 `UNRESOLVED` dates (CMR, ZMB, RWA, BDI) are **excluded** from Leg A. No date is changed, added,
or re-derived.

---

## Leg A — female vs male primary GER around fee abolition

### A1. Outcomes and labels

| series | role | label |
|---|---|---|
| WDI/UIS `SE.PRM.ENRR.FE` — school enrolment, primary, gross %, **female** | outcome F | **OBSERVED (WDI/UIS)** |
| WDI/UIS `SE.PRM.ENRR.MA` — school enrolment, primary, gross %, **male** | outcome M | **OBSERVED (WDI/UIS)** |
| WDI/UIS `SE.PRM.ENRR` — pooled primary GER | reproduction gate only | **OBSERVED (WDI/UIS)** |

Source: World Bank WDI bulk CSV distribution of the UIS series
(`https://api.worldbank.org/v2/en/indicator/<CODE>?downloadformat=csv`). Panels are acquired once, at the vintage
recorded by the sha256 of the three downloaded zips in `data/input_hashes.csv`; the exact long panels used are
committed as `data/wdi_sex_ger_panels.csv` (iso3, indicator, year, value) and `data/wdi_pooled_ger_panel.csv`.
No imputation, no interpolation, no filling of gaps. Both sexes use the **same** acquisition vintage and the
WDI `Metadata_Country` region file from the same download.

### A2. Sample

- Sub-Saharan Africa as classified in the WDI `Metadata_Country` file (`Region` contains "Sub-Saharan").
- Years 1990–2015 inclusive (the E8 sample window at `bd782be`).
- Treated = the 8 verified countries (only those with usable outcome data for that sex enter that sex's
  estimation; the treated count is reported).
- Controls = never-treated SSA countries, plus not-yet-treated treated countries per the inherited control rule.

### A3. Estimator (fixed)

- Callaway–Sant'Anna `ATT(g,t)`, universal base period `g−1`, not-yet-treated controls, event time `e ∈
  {−5,…,+6}`, aggregated across cohorts by cohort size (the `att_cs` routine at `bd782be`).
- **Country-cluster bootstrap: 500 replicates.** Replicate `i ∈ {0,…,499}` draws countries with replacement using
  `numpy.random.default_rng(20261125 + i)` and re-runs the whole event study on the drawn panel (each draw entry
  treated as a distinct pseudo-country, exactly as `boot_rep` does). 95% CI = percentile interval
  (2.5th/97.5th percentiles of the 500 replicate statistics). Replicates in which an event time is not estimable
  are excluded from that event's CI and the count is reported (no failure is hidden).
- Same seeds, same 500 draws for the female and male series and for the pooled reproduction run — **one common
  set of country draws**, so everything is mutually comparable.

### A4. Primary statistic (fixed)

For each sex `s ∈ {F, M}` let `ATT_s(e)` be the cohort-aggregated event-time estimate and let

`ATT_s(0)` be reported **separately** for each sex.

**Primary statistic (pre-registered):**

`D = mean_{e=+1..+6} ATT_F(e) − mean_{e=+1..+6} ATT_M(e)`.

- `D` is the female-minus-male difference in the mean post-abolition (e=+1..+6) primary-GER event-time
  estimate, in gross-enrolment percentage points.
- **Paired country-cluster bootstrap** for `D`: each replicate uses the *same* country draw for both sexes, so
  the same countries enter both series; `D_b = mean_{e=+1..+6} ATT_F,b(e) − mean_{e=+1..+6} ATT_M,b(e)`; the 95%
  CI is the percentile interval of `{D_b}`. The number of replicates contributing is reported.
- Secondary descriptive output (not the primary statistic): event-by-event `ATT_F(e)`, `ATT_M(e)` and
  `ATT_F(e) − ATT_M(e)` with their bootstrap CIs; `ATT_F(0)` and `ATT_M(0)` reported separately; pre-trend
  estimates `ATT_s(−2)`, `ATT_s(−3)` (and `−4`, `−5` with treated `n` disclosed).

### A5. Reproduction gate (must pass before the sex split is trusted)

Run the pooled `SE.PRM.ENRR` verified-8 event study with the same code, sample window and acquisition route.
Pre-registered gate: the pooled **CS `ATT(0)` reproduces `12.44` pp**, i.e.
`|ATT_pooled(0) − 12.4436| ≤ 0.50` pp (tolerance allows documented WDI/UIS data revisions between vintages; the
acquired vintage's sha256 makes the comparison exact and auditable).
- **Gate passes** → the sex-split estimates are reported as the primary Leg A result.
- **Gate fails** → the sex-split estimates are reported as **NOT TRUSTED / diagnostic only**, the exact pooled
  `ATT(0)` obtained is reported alongside the 12.44 benchmark and its deviation, and no gender conclusion is
  drawn. The gate result is reported either way.

### A6. Reporting / decision rule (fixed)

- Report **sign and 95% CI of `D`**, plus `ATT_F(0)` and `ATT_M(0)` separately, and the event tables.
- If the 95% CI of `D` excludes zero: report "the female post-abolition primary-GER trajectory is higher than the
  male one by `D` pp on average over e=+1..+6 (descriptive association; no causal claim)".
- If the 95% CI of `D` includes zero: report "no detected sex difference in the post-abolition primary-GER
  trajectory (`D` = …, 95% CI …)".
- Either way report the pre-trends for both sexes and the pooled reproduction result. **No causal language**;
  the strongest permitted wording is "consistent with".
- If one sex's series cannot support the estimator (e.g. no usable treated-country coverage), Leg A is reported
  **NOT-ESTIMABLE for that sex** with the exact missing series/coverage, not proxied.

### A7. Secondary/robustness (reported, not part of the primary decision)

`ATT_F(e)` and `ATT_M(e)` at every event time; the difference event-by-event; the same D with a TWFE-style
comparison is **not** attempted (the E8 record uses CS as primary; TWFE is not needed here). The pooled all-12
unresolved-date set is **not** used for Leg A. Leave-one-country-out for `D` and `D` on the 1990–2015 window are
not re-litigated; any robustness added is labelled as such.

---

## Leg B — `t*` bulge by sex: data gate defined now, verdict registered as a gate

### B1. Definition (fixed; sourced, never invented)

`t* = t_abolition + L_primary`, where `t_abolition` is the verified date (8/8 sourced as in Leg A) and
`L_primary` is the **length of the primary cycle in years for that country at that time**.

`L_primary` must be sourced to a committed repo file stating primary-cycle length by country and year. This is the
sourcing rule of `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` on
`origin/research/bulge-arrival-2026-11-25` @ `1b91a711568d7e3cd6f074f5465df6bd8447ce48`, where `L_primary` is
recorded **sourced 0/8** and `t*` **UNSOURCED 0/8**. **The auditor's candidate durations (UGA 7, MWI 8, TZA 7,
KEN 8, GHA 6, and any others) are recorded there as "NOT adopted" and are NOT borrowed here.** No "standard 6–8
years" fill-in is permitted. `L_primary` and `t*` are therefore not constructed in this record unless a committed
source is found in the data-gate scan.

### B2. Data gate (run before any estimation; carried out in this record)

Required inputs, all mandatory:
1. an in-repo `L_primary` / primary-cycle-length (education-structure) file covering MWI, ETH, UGA, LSO, TZA,
   KEN, MOZ, GHA for years near their `t_abolition`–`t*` windows;
2. a **sex-disaggregated** final-grade primary **repetition** series (e.g. WDI/UIS repetition rate) **or** a
   **sex-disaggregated primary→secondary transition/progression** series, annual, covering the 8 countries around
   `t_abolition`..`t*+6`;
3. **DHS IR individual-recode microdata** for the 8 countries' waves around `t*` (needed for the cohort-level
   sex-comparable bulge outcome), since no annual cross-country series of final-grade repetition/transition by
   sex is in the repo.

Explicitly **not** accepted as substitutes (registered now, before the scan): DHS API **ecological**
country × survey × education aggregates (e.g. `research/records/2026-11-24-dhs-api-ecological/`'s
`panel_edu*` files and `ED_EDUC_W_SEH` etc.) — they are survey-level margins, not an annual country-level
final-grade repetition/transition series, do not identify the `t*`-completion cohort, and are not a
sex-comparable bulge outcome. Neither is any borrowed/assumed `L_primary`.

### B3. Pre-registered consequence

- If **all three** required inputs are found and committed: Leg B becomes estimable and would be run with the
  same CS family at `t*` (per the Paper-#2 pre-registration).
- If **any** is missing: Leg B is reported **NOT ESTIMABLE**, with the **exact missing series** named, the
  negative-result evidence recorded, **no proxy**, **no borrowed auditor dates**, and **no estimate**. This is
  the expected outcome; it is fixed here so that it is the pre-registered verdict, not a post-hoc excuse.

If the gate fails, the `t*` table is not built and no event study is run for Leg B.

---

## Outputs and discipline

- `data/`: exact committed long panels used (`wdi_sex_ger_panels.csv`, `wdi_pooled_ger_panel.csv`), acquisition
  script `scripts/acquire_wdi_sex_ger.py`, source sha256s in `data/input_hashes.csv`, and the Leg B gate evidence.
- `scripts/gender_split_e8.py`: analysis, importing/reusing the `bd782be` logic.
- `results/`: event tables (CSV), `results/gender_split_results.json` (all numbers incl. bootstrap replicate
  counts), reproduction-gate output, Leg B gate JSON.
- `REPORT.md`: data-gate section, pooled reproduction, Leg A numbers with uncertainty, Leg B NOT-ESTIMABLE
  verdict, deviations, claims→source map. Every table labels its series OBSERVED (WDI/UIS).
- Additive commits only; no force-push; never `main`.
- Any deviation from this document is listed in `REPORT.md` with the reason.
