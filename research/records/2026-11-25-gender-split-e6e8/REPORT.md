# REPORT — gender split of the E8 fee-abolition event study (Leg A) + `t*` bulge data gate (Leg B)

**Branch:** `research/gender-split-e6e8-2026-11-25` (base `origin/research/e6e8-sequencing-2026-11-25` @
`bd782be`). **Record:** `research/records/2026-11-25-gender-split-e6e8/`.
**Author:** `gender-split` (delegated worker; Lead `lead`), task-3. **Date:** 25 November 2026.
**Compute:** host venv `/Users/treymenefee/neon-boot/venv/bin/python` (numpy 2.2.6, scipy 1.15.3, pandas 2.3.3);
**no AutoDL box and no GPU used** (box under a cross-window lease). Power: nothing started, stopped or watched.

**Commits.** `875ffd8` — `PRE_REGISTRATION.md` alone, committed **before any analysis run and before the sex-GER
panels were downloaded/opened**. `829fbb3` — WDI/UIS acquisition script + exact committed panels + sha256
provenance. This report's commit adds the analysis scripts, the Leg B gate script, the results and this report.

**Language.** Association only. "Consistent with", "the estimate is", "is associated with" — never
"effect of abolition", "caused", "drives". Every series here is **OBSERVED (WDI/UIS)**; the E8 record's own labels
apply to reused inputs. Nulls and failures are reported.

---

## 0. What was run, and what is labelled what

| item | source | label |
|---|---|---|
| `SE.PRM.ENRR.FE` primary GER, female (%), annual | WDI bulk CSV of the UIS series, vintage **2026-11-11**, zips sha256-pinned in `data/input_hashes.csv` | **OBSERVED (WDI/UIS)** |
| `SE.PRM.ENRR.MA` primary GER, male (%), annual | same | **OBSERVED (WDI/UIS)** |
| `SE.PRM.ENRR` primary GER, total (%) — **reproduction gate only** | same | **OBSERVED (WDI/UIS)** |
| 8 verified abolition dates | `../2026-11-25-e6e8-sequencing/data/fee_dates.csv` @ `bd782be`, sha256 `1a08d465…`; VERIFIED rows only | VERIFIED (independent audit) |
| estimator | `att_cs` / `boot_rep` logic of `../2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py` @ `bd782be`, imported directly | reused, unchanged |

Committed panels: `data/wdi_sex_ger_panels.csv` (18,252 rows, iso3×indicator×year×value), 
`data/wdi_pooled_ger_panel.csv` (9,542 rows), `data/wdi_metadata_country.csv`. Acquisition:
`scripts/acquire_wdi_sex_ger.py` (downloads the three WDI bulk CSVs, verifies their sha256, writes the long panels,
records URLs + vintage + panel sha256s in `data/input_hashes.csv`). No imputation, interpolation, or gap filling.

---

## 1. DATA GATE (Leg B) — verdict: **NOT-ESTIMABLE**

The pre-registered rule (`PRE_REGISTRATION.md` §B) requires all three inputs below, and explicitly refuses
ecological DHS-API aggregates and borrowed `L_primary` values. Gate run: `scripts/legb_data_gate.py`; evidence:
`results/legb_data_gate.json` (scan timestamp `2026-11-24T17:16:01Z`, **197 refs / 5,424 unique paths**).

| required input | status | exact negative-result evidence |
|---|---|---|
| `L_primary` = primary-cycle length by country-year for MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA | **MISSING** | Path scan of all 197 refs: **0** paths match `primary.duration/_cycle/_length/L_primary/ISCED/education.structure`. Worktree content scan: the only `L_primary` hits are this record's own pre-registration and gate script. The only education-structure file in any ref is `public/reference/east-asia-schools/source/systems.json` (keys: Hong Kong, Japan, South Korea) — an East-Asia city school model with **no SSA primary-cycle lengths**. `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` @ `origin/research/bulge-arrival-2026-11-25` (blob `e3e4709…`) records `L_primary` **sourced 0/8**, `t*` UNSOURCED 0/8, auditor candidate durations **"not adopted"** |
| sex-disaggregated final-grade primary repetition **or** primary→secondary transition/progression series, annual | **MISSING** | **0** ref paths match `rept/prsl`; worktree content scan **0** hits for `SE.PRM.REPT` / `SE.PRM.PRSL` outside this record's gate script. Public WDI probe: `SE.PRM.REPT.ZS` = *Repeaters, primary, **total** (% of total enrollment)* (HTTP 200) — a total-sex series, not sex-disaggregated, and not committed; `.FE/.MA` and `PRSL` variants returned HTTP 429 (rate-limited, **inconclusive**, irrelevant to the gate because no such series is committed). The DHS public indicator catalogue (4,655 indicators) has **0** indicators matching repeat/transition/progression/grade/enrolment |
| DHS IR individual-recode microdata for the 8 countries around `t*` (or an equivalent committed cohort-level, sex-comparable bulge outcome) | **MISSING** | **0 `.dta` files across all 197 refs** (DHS terms forbid redistribution). DHS IR is login-gated and **not publicly downloadable** — logged attempts: direct flat-file URLs 404, landing page 200 but login-gated, IPUMS-DHS API 403 (`../2026-11-23-dhs-micro/README.md` + `data/microdata_probe.txt` @ `origin/research/dhs-micro-2026-11-23`). The Africa-11 dataset request that contains **all 8 E8 countries is "NOT SUBMITTED"** (`../2026-11-24-dhs-acquisition/application/NEXT_ACTION_2026-11-24.md`, §1) and **0 of 54** standard-DHS E8 IR waves are held (`../2026-11-25-bulge-micro-dhs/BULGE_MICRO_STATUS.md` @ `origin/research/bulge-micro-dhs-2026-11-25`) |

**Explicitly rejected as a substitute (pre-registered):** the DHS-API **ecological** record
`research/records/2026-11-24-dhs-api-ecological-2026-11-24` is **NOT a valid sex-comparable bulge outcome**. Its
unit is the DHS-published **country × survey round × background category cell** (e.g. `data/panel_survey.csv` is
country×survey with `pipeline_sec_plus` = share of *women* with secondary-or-higher attainment; `data/panel_edu2_*`
/ `panel_edu4_*` are country×survey×education cells). It does not identify the `t*`-completion cohort, has no
final-grade repetition or transition outcome, and has no male counterpart. Its own README says "Nothing here is
microdata: the unit is the DHS-published cell". Used for this test it would change the estimand from a
sex-comparable bulge outcome to an ecological attainment margin — so it is not used.

**Pre-registered consequence applied.** Leg B is reported **NOT-ESTIMABLE**. The `t*` table was not built, no
bulge event study was run, no proxy was constructed, and **no auditor `L_primary` candidate was borrowed**. Exact
missing series:

1. `L_primary` (primary-cycle length by country-year) for MWI, ETH, UGA, LSO, TZA, KEN, MOZ, GHA.
2. A sex-disaggregated final-grade primary **repetition** series, annual, for the 8 countries around
   `t_abolition`..`t*+6`.
3. A sex-disaggregated **primary→secondary transition/progression** series (WDI `SE.PRM.PRSL.ZS` / UIS
   equivalent — total-sex only in WDI), annual.
4. **DHS IR individual-recode** files for the 8 countries' waves near `t*` (0 of 54 standard-DHS waves held).

Re-entry conditions from `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` §7 (year-varying `L_primary` source; at least
one committed repetition and one transition series; a secondary-capacity/intake series; hashed raw E8 inputs)
still stand.

---

## 2. Reproduction gate (pooled) — shown BEFORE the sex split is read — **PASS (exact)**

Pre-registered gate: pooled `SE.PRM.ENRR`, verified-8 dates, SSA, 1990–2015, same estimator and data route must
reproduce the E8 record's **`ATT(0) = 12.4436`** within 0.50 pp.
(`scripts/gender_split_e8.py`; `results/pooled_reproduction_gate.json`, `…_reproduction.csv`.)

| quantity | this run | bd782be reference |
|---|---|---|
| pooled CS `ATT(0)` | **12.44362392207772** | 12.44362392207772 |
| absolute deviation from the exact reference | **0.0** (deviation from the rounded 12.4436 literal = 2.4e-05) | — |
| event-by-event max abs deviation, all 11 events (−5..+6) | **2.22e-16** | `results/e8_event_SE.PRM.ENRR_verified8.csv` @ `bd782be` |
| sample | 48 SSA countries with ≥1 observed year; 8 verified treated in sample; 7 treated contribute at e=0 (MOZ 2004 lacks the 2003 base year in the outcome series); 30 controls (mean) at e=0 | same |

**Gate verdict: PASS.** The pooled estimate reproduces the E8 record's committed value exactly, so the sex split
is interpreted (per pre-registration §A5).

*Method note:* the E8 record's CIs are normal-approximation (`att ± 1.96·bootstrap SE`). This record's
pre-registered CIs are **percentile** intervals and its bootstrap seeds are `20261125+i` (not the E8 record's
`1000+i`), so **CI endpoints are not expected to match across records — the gate is the point estimate, and it
matches exactly**.

---

## 3. Leg A — female vs male primary GER around fee abolition

Design as pre-registered: CS `ATT(g,t)`, universal base `g−1`, not-yet-treated controls, event `−5..+6`,
cohort-size-weighted aggregation; SSA 1990–2015; 500 country-cluster bootstrap replicates (`seed = 20261125+i`,
percentile 95% CI); **paired** bootstrap for the female−male difference (the same country draw builds both sexes'
panels). All series **OBSERVED (WDI/UIS)**, vintage 2026-11-11. Treated counts: 7 at e=0 (MOZ lacks 2003 base);
6 at −5, +3, +4, +5 (missing base/event cells); 7 otherwise; controls 27–30 per event. Event `−1` is undefined by
construction (it is the universal base period).

### 3.1 Female primary GER — event study (`results/e8_event_SE.PRM.ENRR.FE_verified8.csv`)

| event | ATT_F | 95% CI | treated n |
|---|---|---|---|
| −5 | 6.46 | −2.73, 12.11 | 6 |
| −4 | 1.07 | −8.87, 7.82 | 7 |
| −3 | 0.74 | −9.12, 6.98 | 7 |
| −2 | 0.19 | −3.57, 4.96 | 7 |
| **0** | **11.63** | **3.34, 29.68** | 7 |
| +1 | 21.82 | 6.90, 44.30 | 7 |
| +2 | 23.53 | 8.06, 46.44 | 7 |
| +3 | 20.04 | 6.09, 43.02 | 6 |
| +4 | 20.44 | 8.44, 44.97 | 6 |
| +5 | 26.56 | 8.92, 51.02 | 6 |
| +6 | 24.45 | 8.77, 46.66 | 7 |

### 3.2 Male primary GER — event study (`results/e8_event_SE.PRM.ENRR.MA_verified8.csv`)

| event | ATT_M | 95% CI | treated n |
|---|---|---|---|
| −5 | 6.29 | −0.09, 11.70 | 6 |
| −4 | 1.82 | −5.97, 7.60 | 7 |
| −3 | −0.82 | −7.29, 4.38 | 7 |
| −2 | −0.09 | −3.90, 3.64 | 7 |
| **0** | **13.38** | **4.73, 34.06** | 7 |
| +1 | 25.81 | 10.08, 49.50 | 7 |
| +2 | 28.19 | 12.36, 51.93 | 7 |
| +3 | 24.20 | 8.25, 44.42 | 6 |
| +4 | 24.12 | 9.70, 44.32 | 6 |
| +5 | 30.43 | 13.41, 47.99 | 6 |
| +6 | 27.75 | 11.85, 43.71 | 7 |

Both sexes show flat pre-trends at e=−2/−3 (female 0.19, 0.74; male −0.09, −0.82, all CIs spanning zero) and large
positive on-impact/post estimates — the same qualitative pattern as the pooled E8 result.

### 3.3 Female − male difference (`results/e8_event_difference_verified8.csv`)

| event | ATT_F − ATT_M | 95% paired-bootstrap CI | boot reps |
|---|---|---|---|
| −5 | +0.17 | −3.98, 3.80 | 498 |
| −4 | −0.76 | −4.08, 1.83 | 500 |
| −3 | +1.56 | −2.28, 4.12 | 500 |
| −2 | +0.28 | −3.49, 2.98 | 500 |
| 0 | −1.75 | −4.53, 0.34 | 500 |
| +1 | −3.99 | **−7.09, −0.53** | 500 |
| +2 | −4.67 | **−8.61, −0.87** | 500 |
| +3 | −4.16 | −10.47, −0.00 | 498 |
| +4 | −3.68 | −9.86, 1.74 | 498 |
| +5 | −3.87 | −9.51, 3.42 | 500 |
| +6 | −3.30 | −9.12, 2.26 | 500 |

### 3.4 Pre-registered primary statistic

`D = mean_{e=+1..+6} ATT_F(e) − mean_{e=+1..+6} ATT_M(e) = **−3.94 pp**`
(mean female post = 22.81 pp; mean male post = 26.75 pp),
**95% paired country-cluster bootstrap CI = [−8.72, +0.29] pp**, 498 of 500 replicates used (2 replicates lacked an
estimable +1..+6 cell for one sex). `ATT_F(0) = 11.63 [3.34, 29.68]`; `ATT_M(0) = 13.38 [4.73, 34.06]`, reported
separately as pre-registered.

**Decision per the pre-registered rule (§A6):** the 95% CI of `D` **includes zero** → **"no detected sex difference
in the post-abolition primary-GER trajectory (D = −3.94 pp, 95% CI [−8.72, +0.29])"**. The point estimate is
male-higher, but the pre-registered uncertainty interval does not separate the two sexes. Descriptive
event-level estimates are negative at e=0 and all post horizons; their CIs exclude zero only at +1 and +2 (and sit
on the boundary at +3). That event-level pattern is **not** the pre-registered statistic and is not read as a
robust sex difference: it is 2–3 of 6 post horizons, the summary CI includes zero, and the treated sample is 7.
No causal language is used; the permitted reading is "both sexes' post-abolition primary GER trajectories are
similar, with a male-higher point estimate that is not statistically separated".

---

## 4. Deviations and limits

1. **None in the pre-registered primary statistic or its sample.** The sex split uses the frozen design; the only
   deviations are documented methodology notes below.
2. **Gate target literal.** The pre-registration writes the target as `12.4436`; the exact bd782be value is
   `12.44362392207772`. Reproduced value equals the exact value (max event deviation 2.22e-16); the 2.4e-05
   "deviation" is rounding in the pre-registration text only.
3. **Percentile CIs** (pre-registered) differ from the E8 record's normal-approximation CIs; point estimates are
   identical. Bootstrap draws are seed/order dependent, so CI endpoints are not compared across records.
4. **Small treated sample:** 7 treated countries at e=0, 6 at some horizons; CIs are wide. Bootstrap replicates
   where an event was not estimable are excluded from that event's CI and counted (498–500 across events).
5. **WDI vintage:** panels acquired 2026-11-25 from the WDI bulk CSV stamped **Last Updated Date 2026-11-11**;
   zips and derived panels are sha256-pinned in `data/input_hashes.csv`. Re-pulling later may change values.
6. **WDI public-indicator probe** for sex-disaggregated repetition/transition variants returned HTTP 429
   (rate-limited) and is recorded as inconclusive — it does not affect the Leg B verdict, which rests on the
   absence of any committed series in the repo.
7. **No compute beyond the host** was used (no AutoDL box, no GPU); no power/watcher/cron action was taken.
8. All nulls above are reported, not dropped.

---

## 5. Reproduction

```
cd research/records/2026-11-25-gender-split-e6e8
# 1. acquire + verify the exact panels (downloads the WDI bulk CSVs, checks sha256)
/Users/treymenefee/neon-boot/venv/bin/python scripts/acquire_wdi_sex_ger.py
# 2. pooled reproduction gate + Leg A sex event studies + paired bootstrap
/Users/treymenefee/neon-boot/venv/bin/python scripts/gender_split_e8.py
# 3. Leg B data gate (repo-wide scan + DHS evidence)
/Users/treymenefee/neon-boot/venv/bin/python scripts/legb_data_gate.py
```

Outputs: `results/pooled_reproduction_gate.{json,csv}`, `results/e8_event_SE.PRM.ENRR_verified8_reproduction.csv`,
`results/e8_event_SE.PRM.ENRR.FE_verified8.csv`, `results/e8_event_SE.PRM.ENRR.MA_verified8.csv`,
`results/e8_event_difference_verified8.csv`, `results/gender_split_results.json`, `results/legb_data_gate.json`.

---

## 6. Claims → source map

| claim | number | source file / field |
|---|---|---|
| pooled reproduction gate | ATT(0) = 12.44362392207772, max event deviation 2.22e-16, PASS | `results/pooled_reproduction_gate.json` |
| female ATT(0) | 11.63 pp [3.34, 29.68] | `results/e8_event_SE.PRM.ENRR.FE_verified8.csv`, event 0 |
| male ATT(0) | 13.38 pp [4.73, 34.06] | `results/e8_event_SE.PRM.ENRR.MA_verified8.csv`, event 0 |
| female mean post (e=+1..+6) | 22.81 pp | `results/gender_split_results.json`, `female.mean_post_1_6` |
| male mean post (e=+1..+6) | 26.75 pp | `results/gender_split_results.json`, `male.mean_post_1_6` |
| primary statistic D | −3.94 pp, 95% CI [−8.72, +0.29], 498 reps, includes zero | `results/gender_split_results.json`, `difference` |
| event-level male-higher at +1/+2 | −3.99 [−7.09, −0.53]; −4.67 [−8.61, −0.87] | `results/e8_event_difference_verified8.csv` |
| Leg B verdict | NOT-ESTIMABLE | `results/legb_data_gate.json`, `verdict` |
| L_primary sourced 0/8 | 0/8, no in-repo source | `results/legb_data_gate.json`, `evidence.L_primary`; `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` @ `1b91a71` |
| sex-disaggregated repetition/transition missing | 0 ref paths, 0 content hits | `results/legb_data_gate.json`, `evidence.sex_disaggregated_repetition_or_transition` |
| DHS IR missing | 0 `.dta` / 197 refs; 0/54 waves; Africa-11 request not submitted | `results/legb_data_gate.json`, `evidence.dhs_ir_microdata` |
| DHS-API ecological aggregates invalid substitute | country×survey×education cells; 0/4,655 indicators on repetition/transition | `results/legb_data_gate.json`, `evidence.dhs_api_ecological_aggregates` |
