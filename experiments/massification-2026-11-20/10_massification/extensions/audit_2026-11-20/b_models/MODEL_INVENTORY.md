# MODEL INVENTORY — old models (anchor, model2, scaling estimators)

**Audit:** evidence auditor, `extensions/audit_2026-11-20/b_models/`, 2026-11-20.
**Question put to the audit:** build a complete, honest inventory of the programme's OLD MODELS so the Council can
choose new directions. **Do not re-fit anything.**
**What was done:** read code, predeclarations, committed outputs, logs and data cells. **No model was run or
re-fitted.** One code-level diagnostic was executed to test what a committed script actually returns (D-04); it read
an existing panel, produced no model output, and is disclosed in place.

**Base:** `/Users/treymenefee/massification_live/experiments/massification-2026-11-20` (all paths below are relative
to `10_massification/` unless they start with `06_`/`08_`).
**Verdict vocabulary:** the gate's five tokens (`PASS` / `PARTIAL` / `FAIL` / `EQUIVALENT` / `not-run`). Where a cell
is an *estimator register* rather than a gate-scored model, the verdict is `ESTIMATOR` (no gate verdict applies) —
these are counted separately and never as PASS.

**Standing gate cap (read, not re-litigated):** the phase is capped at PARTIAL/DESCRIPTIVE + EQUIVALENT, scaling
criterion FAIL, no direction claim (`06_report`-level closeout `MASSIFICATION_CLOSEOUT.md` §2; `08_council/
brief_013/STOP_RULES.md` R13/R17/R23/R27; `08_council/brief_013/SUCCESS_CRITERIA.md` A8). This inventory tests
whether the artefacts *earn* those labels, not whether the labels were allowed.

---

## 1. System map — what the "old models" actually are

| group | what it is | code | gate-scored? |
|---|---|---|---|
| **A. behavioural core** | single-year cohort-flow push–pull simulator, 6 countries, 3 rivals as channel switches | `model/pushpull.py` | only via B |
| **B. anchor (A1)** | PHL driver: capacity index + 4 arms × 3 rivals = 12 arms, DE fit 1999–2013, crossings M0–M4 | `model/anchor.py` | **yes** |
| **C. pre-anchor calibration** | PHL-only and pooled PHL+CHN fits, KHM held-out country | `model/calibrate.py` | yes (diagnostic) |
| **D. scaling repair** | structural income-facing margin added to A, fitted on completion, judged on OOS exponents | `model/repair.py` | **yes** |
| **E. scaling estimators** | (i) relations/pattern-scout two-way FE register; (ii) model2 five-estimator, two-sample estimation | `relations/scripts/scaling_laws.py`, `model2/code/m2.py` | supplies the targets, not scored |
| **F. rival / identification cells** | model2 recovery (simulated), M2b re-run, M2c E1 recovery, A3/A5/A5b rivals, E6 timing | `model2/code/*.py` | partly |
| **G. predeclared, never run** | portability A6/A7, JPN/KOR/HKG timing, E2 K-12, E3 nurses | `model/PRE_*.md` | **not-run** |

The anchor (B) is *not* a different model from A: it calls `pushpull.run()` and adds a capacity-gated push and a
fit/crossing harness. "12 arms" = 3 rivals × {law_only, capacity_gated, capacity_only, none}.

---

## 2. Structure, equations and parameters actually implemented

### 2.1 Behavioural core — `model/pushpull.py` (sha256 `0cf3dceb…`)

Per country, per year t (1960–2040), ages 0–84, state = population, educated share, GDP index, intake rate:

```
births_t      = 0.5 · Σ_{a=15..49} pop_{a,t−1} · TFR_t / 35
pop_{0,t}     = births_t ;  pop_{a,t} = pop_{a−1,t−1} · s_a          (s = {child .995, adult .994, old .96})
job_opp_t     = exp(0.012 (t−1960)) · (1 + e_s (educ_share − 0.15))
g_t           = g0 + 0.5 e_s max(0, educ_share − 0.15) + shock_t
gdp_t         = gdp_{t−1} (1 + g_t)
intake_t      = clip(intake_{t−1} · [1 + 0.1 e_d (job_{t−lag_d}/job_t − 1)], 0.2, 1)      # repair may add ×gdp^{eta_in}
p_k           = clip(a_k + g_k ln gdp + u_k · urb + m_k ln gdp [+ 0.02 e_d ln job], lo_k, hi_k)   k∈{pri,low,up,ter}
p_pri, p_low += push_floor(t) ;  p_up, p_ter += push_ceiling(t)
ent = pop_6 · intake ;  prim = ent · cyc_pri ;  low = prim · p_pri · cyc_low
up  = low · p_low · cyc_up ;  ter = up · p_up · p_ter · cyc_ter
GER_l = 100 · stock_l / Σ pop[band_l]
completion_primary = 100 p_pri ;  completion_lower = 100 p_pri p_low ;  completion_upper = 100 p_pri p_low p_up
agri = clip(0.75 e^{−0.35 ln gdp} + 0.02) ;  services_share_nonag = clip(0.45 + 0.08 ln gdp + 0.15 educ)
formal = clip(0.25 + 0.55 educ + 0.05 ln gdp) ;  educ_t = 0.97 educ + 0.03 min(1, (up+ter)/prim)
```

Free parameters and how set: 14 in `calibrate.KEYS` (`p_pri0,p_low0,p_up0,g_pri,g_low,g_up,u_pri,u_low,u_up,e_s,e_d,
lag_s,lag_d,g0`) with declared bounds (`calibrate.BOUNDS`); 6 more in the repair (`eta_in,lag_in,m_pri,m_low,m_up,
m_ter`, `repair.BOUNDS`). All other constants (TFR/URB paths, cycle lengths, survival, 0.75/0.35/0.45/0.08/0.15/0.25/
0.55/0.05, 0.012, 0.02, 0.97/0.03, PUSH 0.05, CEIL 0.25, κ 0.75, capacity weights .5/.3/.2, 40→20 PTR map, 2→5 %GDP
map, compulsory 6/10/13) are **declared assumptions**, labelled S/E/A in `model/configs.py` or hard-coded in
`anchor.py`/`pushpull.py`.

**Two equations matter for everything downstream:**

1. `completion_*` **do not depend on the cohort flow at all** — they are the fitted progression probabilities (or
   their products). Text claims "completion is generated from the same cohort flow" (`PREDECLARATION_AMENDMENT_013.md`
   §G; `pushpull.py` L132–133 comment). Code says otherwise: the population vector enters only `GER_*`. This is a
   code/text disagreement, not a nuance (D-01).
2. `prim → low` multiplies by `cyc_low` **on top of** the already-cycle-multiplied `prim`, so `low/up/ter` are
   inflated by accumulated cycle lengths. Measured in the committed smoke output: `ger_lower` 332.8–1477.0 %,
   `ger_upper` 837.3–3514.4 %, `ger_tertiary` 583.4–3247.9 % over **all 1458 rows**
   (`model/smoke/structure_smoke.csv`). GER is not on the observed scale (D-02).

### 2.2 Anchor driver — `model/anchor.py` (sha256 `bd96f067…`)

- **Capacity index** `C_t ∈ [0,1]`: delivery 0.5 (PTR, `(40−PTR)/20`), fiscal 0.3 (`(%GDP−2)/3`), enforcement 0.2
  (`compulsory years/13`); missing input → weight dropped, remaining renormalised; flat back-fill before the first
  observation. Committed series: C(1960)=0.2337, C(1990)=0.2952, C(2017)=0.7964, C(2024)=0.7925
  (`model/anchor_out/run_meta.json`).
- **Gate** `G(C)=C^κ`, κ=0.75 (declared; A10 amendment replaced the earlier logistic).
- **Arms**: `law_only` (G≡1), `capacity_gated` (marker·G), `capacity_only` (G, no marker), `none`; PUSH=0.05,
  CEIL=0.25 applied to upper/tertiary only.
- **Fit**: 14 parameters, `differential_evolution(seed=4242, maxiter=18, popsize=6, polish=False)`, window 1999–2013;
  holdout 2014–2024; crossing years 1960–2040, never fitted.
- **What is persisted**: fit/holdout MAE, n, M0–M4, R6 flag (`anchor_out/anchor_table.csv`), the capacity series, and
  the A2d best triple (`run_meta.json`). **The fitted θ for any of the 12 arms is not written anywhere** (D-03).

### 2.3 Scaling estimators

- **Pattern-scout register** (`relations/scripts/scaling_laws.py`, `relations/data/scaling_laws.csv`): two FE
  structures per law — country+year FE ("within") and year FE ("between"), CR1 clustered. Values used by the gate:
  S1 secondary 0.0904 / 0.2154; S2 tertiary 0.8482 / 0.5666; S4 lower-sec completion 0.2468 / 0.1690.
- **model2** (`model2/code/m2.py`): five estimators (10y long-diff, between, country-ts NW, first-diff, levels
  two-way FE as reference) × two samples (UIS6, WDI30), plus logistic fits, common-shape tests, lead–lag, rivals, and
  a **simulated** 4-truth recovery test. Produced the three "classified scaling laws" that Amendment A1 adopted as
  the reproduction target: secondary **+0.286 (0.045)**, tertiary **+0.776 (0.086)**,
  lower-sec completion (logit) **+1.174 (0.157)** (`model2/runs/scaling_estimates.csv`).

---

## 3. Cell-by-cell inventory

### 3.1 A1 ANCHOR — the 12-arm PHL descriptive run

| field | value |
|---|---|
| id | `A1-ANCHOR` |
| paths | `model/anchor.py`; `model/anchor_out/anchor_table.csv`, `findings.txt`, `run_meta.json`; log `model/anchor.log` |
| structure | §2.2; emits `completion_*` (parameter products) and `GER_*` (mis-scaled, §2.1) |
| parameters | 14 free, DE seed 4242 / maxiter 18 / popsize 6; κ=0.75, PUSH=0.05, CEIL=0.25, capacity weights .5/.3/.2 — all declared, none reported per arm |
| data | observed PHL completion from `04_data/TARGETS_FLOW.csv` (loaded through `calibrate.load_completion`); WDI education %GDP from `04_data/data/wdi_4countries_long.csv`; PTL/PTR from `10_massification/data/SCHOOL_EXPANSION.csv`; both loaders **hard-code the old iCloud path** (D-05) |
| key output | `fit_mae` 1.05–3.29 pp (19 pts), `hold_mae` **4.01–6.12 pp** (14 pts); M0 1960–1980, M1 1966, M2 ∈ {2025, 2028, 2038} or none, M3 none ≤2024 but **2027 / 2031** post-window, M4 **1960 in all 12 arms**; R6 in-window 12/12 pass; A2d best `('demand_led', 6, −0.427)` (`anchor_out/findings.txt` L26) |
| verdict | **PARTIAL** (descriptive) — as pre-declared under D57/A8; the M2/M3 crossing test is the only in-window content |
| status | **load-bearing** |
| defects | D-01, D-02, D-03, D-05, D-08, D-17, D-18, D-21 |

**What the 12 arms show, honestly.** Only two milestones are informative. **M2 (lower-secondary ≥90, observed 2024):**
0/12 clean hits; 2025 (education_led/capacity_gated) and 2028 (demand_led/capacity_only) are inside ±5 y but sit in
arms that overshoot M3 in 2027/2031 (A1 addendum table; `anchor_out/A1_ADDENDUM_C1_C10.md`). **M3 (upper-secondary
≥90, observed never):** no arm crosses by 2024 (R6 pass 12/12) but two arms cross afterwards — a ceiling-channel
overshoot flagged under A10/R29. **M0/M1** are left-censored boundary constraints at 1960/1966. **M4 = 1960 in every
arm including the no-push arm** — not a timing miss but an initialisation artefact: the model's tertiary GER is
already 583–3248 % in 1960 (D-02), so the ≥50 threshold is met before the run starts.

**Capacity does not earn its claim.** `law_only` vs `capacity_gated`: demand_led M2 None→None (tie), education_led
None→2025 (gated "better"), complementary None→None (tie) → credit in 1 of 3 rivals, and that one is the arm that
post-window crosses M3 (findings L41–47). Holdout MAE actually *worsens* under the gate in 2 of 3 rivals
(4.42→4.51; 5.19→5.26; 4.57→4.01). **Verdict on the arm: EQUIVALENT** (`A1-CAPACITY` below), which is what
`findings.txt` concludes — correctly.

**A1 is weaker than "PARTIAL" on two counts that the documents themselves disclose but the tables do not:**
(a) the A6 milestone vector's first element, primary completion ≥90 in 2017, was never recorded on the model side
(C8 — per-arm series not persisted, so it cannot be recovered without a re-fit); (b) no naive benchmark is computed
on the anchor's own 2014–2024 holdout, yet the closeout and A1 addendum compare its 4.01–6.12 pp to the
*calibration cell's* linear-trend value 4.35 pp computed on 2011–2024 (D-08).

### 3.2 A1 capacity contrast (the arm-level cell the Council will ask about)

| field | value |
|---|---|
| id | `A1-CAPACITY` |
| paths | same as A1; arm columns of `anchor_out/anchor_table.csv`; `model/PRE_ANCHOR_CAPACITY.md` |
| structure | 4 arms × 3 rivals, identical fit/holdout/seeds |
| parameters | gate form and weights declared, not fitted; sensitivity over κ ∈ {0.5,0.75,1.0} **declared but never run** (D-07) |
| data | capacity inputs above; enforcement is a deterministic function of the same law dates |
| key output | ties 2/3, gated better 1/3, gated worse on holdout in 2/3; A2d r = −0.427 at lag 6 (see A2D) |
| verdict | **EQUIVALENT** (capacity-timing not credited) |
| status | **load-bearing** |
| defects | D-07 (κ sensitivity absent), D-09 (enforcement double-count), D-10 (A2d invalid) |

### 3.3 A2d capacity-leads-intake

| field | value |
|---|---|
| id | `A2D` |
| paths | `model/A2D_CAPACITY_LEADS_INTAKE.md`; code inside `anchor.py` L159–174; result in `anchor_out/findings.txt` L26 |
| structure | cross-correlation of ΔC_t and Δ(enrolment) at lags 0–6, best |r| over 3 rivals × 7 lags |
| parameters | θ fixed at the **midpoint of the bounds**, not fitted; `push_series` set to the whole arm dict |
| data | simulated enrolment from the model + the declared capacity series |
| key output | best `('demand_led', lag 6, r = −0.4272)`; predeclared lags were 2–4 (`PRE_ANCHOR_A2.md` A2d) |
| verdict | **not-run (invalid as executed)** — see defect |
| status | diagnostic-only |
| defects | **D-10**: `th['push_series'] = armser['capacity_gated']` is `{'floor':{…},'ceiling':{…}}`; `pushpull.run` does `push_series.get(t, 0.0)` with an integer year → **0.0 every year**. The capacity push is OFF in the A2d simulation, so the correlation is between an exogenous capacity path and a *baseline* enrolment path; it cannot test "capacity leads intake". The doc's headline "DESCRIPTIVE-NEGATIVE: not supported" is therefore not supported by its own run. Secondary defects: the declared lag window was 2–4 but 0–6 was scanned; the max over 21 correlations is selected, not tested. |

### 3.4 Pre-anchor calibration cells (PHL, PHL+CHN, KHM)

| field | value |
|---|---|
| id | `CAL-PHL`, `CAL-PHLCHN`, `CAL-CHN`, `CAL-KHM` |
| paths | `model/calibrate.py`; `model/calib/calibration_table.csv`; logs `model/calib_phl.log`, `model/calib_phl_chn.log` |
| structure | §2.1 with θ fitted by DE (PHL: seed 2026/60/12; pooled: seed 2027/40/10), fit 1980–2010 (observed rows → 1999–2010), holdout 2011–2024, KHM never fitted |
| parameters | θ persisted as `theta_json` per row (the only place any old-model θ survives) |
| data | `04_data/TARGETS_FLOW.csv` `status==target` completion; `04_data/ECONOMY_SERIES.csv` sector shares (check only) |
| key output | **PHL-only** (log only, no longer in the CSV): fit 0.95/1.20/1.09, hold **4.84/5.40/6.08**, naive persistence 8.60, **trend 4.35**, sector check 19.96/2.47/12.77 pp (`calib_phl.log`) → **PARTIAL**, loses trend. **Pooled PHL+CHN** (`calibration_table.csv`): PHL fit 5.57/4.65/4.61, hold 7.23/4.38/5.38, corr 0.965/0.986/0.980, `beats_persistence=True`, **`beats_trend=False`**; CHN fit **8.65/9.69/9.80 (n=4)** > 5 pp → **FAIL**; hold 8.70/7.38/7.82 vs trend **2.64**; **KHM** all-years 34.11/35.94/35.70 (n=40), 2011–24 **28.24/32.23/31.26** (n=23) vs naive 6.89/8.91 → **FAIL by ~30 pp**; sector check 8.4–25.6 pp on n=90 |
| verdict | PHL **PARTIAL**; CHN **FAIL**; KHM **FAIL** |
| status | diagnostic-only (superseded by the A6 1999–2013 anchor window) |
| defects | D-06 (CSV overwritten by the pooled run, so the PHL-only cell exists only as a 4-line log; `STATUS.md` still cites calibration_table hash `13c93588…`, the overwritten version, while the current file is `552e0cce…`); D-05 (hard-coded old ROOT) |

### 3.5 Scaling criterion, unrepaired cell

| field | value |
|---|---|
| id | `SCALING-UNREPAIRED` |
| paths | `model/calib/scaling_check.csv` (sha256 `a07077c4…`); narrative `10_massification/STATUS.md` L85–91; `model/PRE_ANCHOR_A1.md` amendment block |
| structure | OOS log–log slopes of GER secondary/tertiary and logit completion on the income index, per rival, segments `fit_1999_2010` / `oos_2011_2024` |
| parameters | none fitted here — the θ from the PHL calibration cell |
| data | simulated model series + the model's own GDP index |
| key output | OOS secondary **−1.893 / −0.379 / −0.743**; tertiary **−1.229 / −0.137 / −0.353**; completion logit **+0.0320 / +0.0396 / +0.0312**; targets +0.286 / +0.776, A3 ranges [0.0904,0.2154] / [0.5666,0.8482] |
| verdict | **FAIL** (wrong sign, 0/3 contained) |
| status | **load-bearing** |
| defects | **D-11: no generator script exists in the tree.** No `.py` in `10_massification/` writes this file or computes `generated_exponent` (grep: only `STATUS.md` and `PHASE_WRITEUP_SHELL.md` reference it). The single most-cited negative number in the programme is an **orphan artefact**. Also `fit_1999_2010` is a window the anchor superseded (A6 = 1999–2013). |

The **sign** failure is unambiguous and does not depend on any range: all three rivals generate negative secondary and
tertiary income slopes against a required positive sign. That conclusion survives D-12/D-13/D-14 below.

### 3.6 Scaling criterion, repair cell

| field | value |
|---|---|
| id | `SCALING-REPAIR` |
| paths | `model/repair.py`; `model/calib/repair_table.csv`, `repair_scaling.csv`; log `model/repair.log`; predecl `model/PRE_SCALING_REPAIR.md` |
| structure | adds income-facing intake margin (`eta_in`, `lag_in`) and progression income exponents (`m_pri…m_ter`) to §2.1; 20 free parameters; fit PHL+CHN 1980–2010; OOS exponents are checks |
| parameters | `theta_json` persisted (20 values/row) |
| data | same completion targets; holdout untouched |
| key output | PHL fit **7.43/6.47/6.16** (gate 5) / hold **5.44/6.26/4.80**; CHN fit 7.42/8.83/9.35, hold 4.14/8.72/7.03; OOS secondary **−2.734/−2.527/−1.034**; tertiary **−0.319/−1.317/−0.391**; completion **+11.465/+1.868/+2.546**; `signs_ok 1/3`, `contained 0/3`, `within_1se_A1` false |
| verdict | **FAIL** |
| status | **load-bearing** |
| defects | **D-12** (completion-law comparison is unit-mismatched: the model's *logit* slope is tested against the relations *log-log* range [0.169,0.2468] — `repair.exps` vs `repair.A3`); **D-13** (the A1 secondary target 0.286 lies **outside** the A3 containment range [0.0904,0.2154], so the criterion is self-contradictory); D-14 (the θ can be re-derived, but the cell is barred from re-run by R27) |

### 3.7 model2 — estimator register and identification cells

| field | value |
|---|---|
| id | `SCOUT-SCALING` / `M2-SCALING` / `M2-UNIV` / `M2-RIVALS` / `M2-RECOVERY` / `M2B` / `M2C` |
| paths | `relations/scripts/scaling_laws.py` → `relations/data/scaling_laws.csv`; `model2/code/m2.py` → `runs/scaling_estimates.csv`, `scaling_classification.csv`, `logistic_fits.csv`, `logistic_common_tests.csv`, `lead_lag.csv`, `rivals.csv`, `recovery.csv`; `code/m2b.py` → `runs/m2b_scaling.csv`; `code/m2c.py` → `runs/m2c_recovery.csv` |
| structure | see §2.3; recovery = 4 truths × 5 seeds, 30×30 simulated panel, AIC rival selection |
| parameters | estimator coefficients only; recovery DGP parameterised in code (`m2.recovery`) |
| data | `09_relations/data/panel_wdi_eci.csv`, `panel_wdi_wide.csv`, `04_data/ECONOMY_SERIES.csv`, `04_data/data/gmr_observed_6countries_1970_2024.csv`; never the imputed panel |
| key output | 91 scaling rows → **3 classified laws**: secondary +0.286 (0.045, n=30), tertiary +0.776 (0.086, n=30), lower-sec completion (logit) +1.174 (0.157, n=28); logistic common-slope test `shared_parameters=False` (AIC 3052.9, common-r not finite); lead–lag **NOT IDENTIFIABLE** (2 countries, `lead_lag.csv`); rivals **supply wins 15/23**, demand 8/23, median OOS RMSE 0.123 vs 0.182, median push coefficient +0.0257; recovery **demand 1.00 / supply 1.00 / complementary 0.00**, **forced-ID 1.00**, equivalence 0.07 → **NOT IDENTIFIABLE** |
| verdict | `M2-RECOVERY` **FAIL (not identifiable)**; `M2C` **FAIL (E1 not sufficient)**; `M2B` **FAIL (void — D-04)**; estimator cells `ESTIMATOR` |
| status | M2-RECOVERY, M2C **load-bearing**; M2-SCALING / M2-UNIV / M2-RIVALS diagnostic-only; M2B **failed** |
| defects | **D-04** (M2b returns the regression **intercept**, not the slope — see below), **D-14** (A1 target = this estimator's own between estimate), **D-15** (model2 findings narrative contradicts its own rivals count) |

**D-04 in detail (m2b).** `code/m2b.py::fit` does `b, se, e = ols_cluster(...)` where `ols_cluster` prepends a ones
column, then returns `float(b[0])` — the **intercept**. For the `within` branch it returns the intercept of a
regression on two-way-demeaned data (≈0 by construction); for the `yearFE` branch it returns the intercept of the
year-dummy regression. Committed consequences: every "within FE" row in `runs/m2b_scaling.csv` is **0.000**
(1e−16) and every "yearFE" row is an intercept (+2.282, +1.968, −9.325, −12.601, +1.600, −3.463 …). Diagnostic
performed (read-only, one regression, no model re-fit): on the same panel, secondary-completion-yearFE gives
**intercept 2.2822, slope 0.169**; the demeaned regression gives intercept −0.000, slope 0.377. The slope 0.169
matches the relations register's S4-between value 0.1690 exactly — i.e. the correct number was already on disk.
`runs/m2b_findings.txt` states "Log-level within-FE gives the larger coefficient (reproducing the ~+1.17 relay)" —
the same file's within-FE values are 0.000, so the sentence is false on its own output.

**M2b's founding "discrepancy" is a row mix-up.** `AMENDMENT_M2b.md` and `runs/m2b_findings.txt` set
"M2 original between (WDI30) **+0.843**" against the scout relay **+1.174**. But `runs/scaling_estimates.csv` has
lower-secondary between = **+1.174** (se 0.157, n=28) and upper-secondary between = **+0.843** (se 0.157, n=30). The
+0.843 is the **upper-secondary** row. Model2's own lower-secondary estimate already equalled the relay. The
"estimator range +0.84 … +2.3" then codified in `08_council/brief_013/SUCCESS_CRITERIA.md` A3 is built from that
mix-up plus intercepts; a defensible range exists directly in `scaling_estimates.csv` (**1.174 / 1.199 / 1.190 /
1.620 / 2.071** across estimators), but it is not the range the gate adopted. See D-04b.

### 3.8 Rival / identification cells (A3, A5, A5b, E6)

| id | paths | structure | key output | verdict | status |
|---|---|---|---|---|---|
| `A3A` | `model2/code/a3_a5.py`; `runs/a3_remittances.csv`; `model2/A3_PREREG.md`, `A3_D55_STATUS.md` | log-log NW(2) remittances→GER, controls + trend, PHL 1995–2024; predeclared β∈[0.10,1.50] for tertiary | tertiary **β=−0.213 (se 0.070, n=27)**, secondary −0.018, primary +0.124; secondary lead-placebo t=3.33 | **FAIL** (sign + band) | failed |
| `A3B` | `runs/a3b_simulated.csv` | simulated design expectation only; E3 DATA BLOCKED | nursing +19.4 % vs placebo −4.3 %/+3.3 % | **not-run** (simulated, no claim) | diagnostic-only |
| `A5` | `runs/a5_rivals.csv`, `a3_a5_findings.txt`; `A5_PREREG.md` | 5 reduced-form rivals, PHL pre-2013 fit → 2013–2024 | labour-queue wins OOS (2.81 / 4.37); **equivalence rule (≤0.5 pp on MAE *and* event-break) not met** (event gaps 2.3 / 3.43) | **PARTIAL** (ranking only, no anchor comparison) | diagnostic-only |
| `A5B` | `code/a5b.py`; `runs/a5b_scores.csv`, `a5b_final_scoring.txt`; `A5B_REPORT.md` | 4 testable rivals on crossings/ordering, fit 1999–2013 | world-society moves only primary (2014 vs 2017 observed); formal shapes primary 2023; the other two predict nothing; **equivalence-to-observed set EMPTY** | **FAIL** (all rivals distinguished) | **load-bearing** |
| `E6` | `code/e6.py`; `runs/e6_timing_independent.csv`, `e6_findings.txt`, `e6_meta.json`; `E6_PREREG.md` | 4 single-curve forms fitted only pre-crossing; 24 scored form×milestone rows | logistic 2/6 PASS (median \|err\| 5.5 y), Gompertz 1/6 (8.0 y), linear 0/6, exponential 0/6 → rule "≥2/3 of scored milestones PASS" **fails**; scout agreement **0/9 within 1 y** | **FAIL** (R19 structural timing miss) | **load-bearing** |

A5b caveat that must travel with any citation: world-society's primary crossing (2014) **is** within ±5 y of 2017,
so the empty equivalence set rests on ordering/spacing and the upper-secondary non-crossing, not on primary timing —
`10_massification/lit/PHASE_WRITEUP_SHELL.md` §(b).5 says this explicitly; `A5B_REPORT.md` alone does not.

### 3.9 Predeclared, never run

| id | path | declared design | status | why it matters |
|---|---|---|---|---|
| `PORTABILITY-A6/A7` | `model/PRE_PORTABILITY_A6_A7.md` | CHN then HKG with **frozen PHL behaviour**, only declared country inputs re-set | **not-run** (parked by R22/D75) | the only gate-legal portability design on disk; blocked because the anchor is PARTIAL |
| `TIMING-JPN/KOR/HKG` | `model/PRE_TIMING_JPN_KOR_HKG.md` | crossing-year intervals under censoring; N=5 provisional | **not-run** (DATA BLOCKED for JPN/HKG; A4 pending) | would field the timing estimand that E6 shows is mostly censored |
| `E2-PH-K12` | `model/PRE_EXP_E2_PH_K12.md` | cohort-exposure DiD, MDE ≈4.0 pp declared, claim cap descriptive | **not-run** | predeclares its own underpowering honestly (≈6 pre points) |
| `E3-PH-NURSES` | `model/PRE_EXP_E3_PH_NURSES.md` | Abarcar–Theoharides replication (9:1) | **not-run / DATA BLOCKED** | no PRC/CHED series on disk |

### 3.10 Legacy predeclaration (superseded)

`model/PREDECLARATION.md` (task-37 scaffold) declares fit 1980–2010 / holdout 2011–2024, six countries, and "NOTHING
HAS BEEN FITTED". Superseded by `PREDECLARATION_AMENDMENT_013.md` (§ roles, §I sector check-only) and, for the
anchor, by A6 (1999–2013 / 2014–2024). Status **superseded**; retained because its "no target coded as a parameter"
rule is still the standard the audit applies.

---

## 4. Defect register

Severity: **S1** = changes a verdict or makes an artefact unusable; **S2** = material mislabel/ambiguity;
**S3** = housekeeping/provenance.

| id | sev | defect | evidence | consequence |
|---|---|---|---|---|
| **D-01** | S1 | `completion_*` are parameter products, not cohort-flow outputs. Text: "completion is generated from the same cohort flow". Code: `completion_primary = p_pri`, etc. | `pushpull.py` L132–137; `PREDECLARATION_AMENDMENT_013.md` §G | the two fit series (completion) contain no cohort dynamics; "cohort-flow model" describes only the GER branch. The PASS-relevant claim "generated from the flow" is false as written |
| **D-02** | S1 | GER is mis-scaled by accumulated cycle lengths: `low = prim·p_pri·cyc_low` after `prim = ent·cyc_pri` | `pushpull.py` L115–119; measured `smoke/structure_smoke.csv`: ger_lower 332.8–1477.0, ger_upper 837.3–3514.4, ger_tertiary 583.4–3247.9 % (1458/1458 rows >100) | every GER-based milestone and any GER-based fit is on the wrong scale; M4=1960 is an artefact of it; GER is labelled a "CHECK" but the anchor uses it for M1/M4 |
| **D-03** | S1 | no fitted θ is persisted for any of the 12 anchor arms; no per-arm series; `run_meta.json` has only `arms`, `capacity_series`, `a2d_best` | `anchor_out/run_meta.json`; addendum C8 | the anchor result cannot be reproduced or re-scored from committed artefacts; only a re-fit (barred by R27/R12) could recover it |
| **D-04** | S1 | `m2b.py::fit` returns the **intercept**, not the slope, in both branches | `model2/code/m2b.py` L19–39 vs `ols_cluster` L6–14; `runs/m2b_scaling.csv` (within = 0.000; yearFE = intercepts); read-only diagnostic: yearFE intercept 2.2822 / slope 0.169, demeaned intercept −0.000 / slope 0.377 | `m2b_scaling.csv` is void; `m2b_findings.txt`'s resolution sentence is contradicted by its own table |
| **D-04b** | S1 | the M2b "discrepancy" is a row mix-up: 0.843 is the **upper-secondary** between estimate; model2's lower-secondary between is 1.174 (the "scout relay") | `runs/scaling_estimates.csv` (both rows, se 0.157); `AMENDMENT_M2b.md` table; `SUCCESS_CRITERIA.md` A3 | the estimator range +0.84…+2.3 adopted by A3/R14 rests on a misquote; a defensible range (1.17–2.07) exists on disk |
| **D-05** | S1 | both loaders hard-code the **old iCloud root**, not BASE, and swallow failures with `except Exception: pass` | `anchor.py` L12/18–30; `calibrate.py` L15/18 | re-running from BASE either reads the old tree (as the committed run did — `anchor.log` last line prints the old path) or silently drops the fiscal and PTR inputs and still exits 0. Input provenance is not guaranteed by the code |
| **D-06** | S2 | pre-anchor PHL-only calibration lost: the pooled run overwrote `calib/calibration_table.csv`; the PHL-only numbers exist only in `calib_phl.log`; `STATUS.md` still cites hash `13c93588…` while the file is `552e0cce…` | `calib_phl.log`, `calib_phl_chn.log`, `STATUS.md` L79, `SHA256SUMS` | the two cells' labels are no longer recoverable from the CSV; the hash trail conflicts |
| **D-07** | S2 | κ-sensitivity (0.5/0.75/1.0) and capacity-weight sensitivity are **declared but never run**; only κ=0.75 exists | `PRE_ANCHOR_CAPACITY.md` A10 §1; `anchor.py` KAPPA=0.75; no sensitivity output anywhere | the declared robustness check for the only new mechanism is missing |
| **D-08** | S2 | anchor holdout (2014–2024) is compared to a benchmark computed on 2011–2024, and the comparison is stated as "all arms lose to trend (4.35)" | `anchor_out/anchor_table.csv` (hold 4.0148 for complementary/capacity_gated); `calibration_table.csv` (`naive_trend` 4.3529); `MASSIFICATION_CLOSEOUT.md` §2 | one arm (4.01) is *below* 4.35, so the blanket claim is false on its face; and no benchmark was computed on the anchor's own window |
| **D-09** | S2 | enforcement proxy sits inside `G(C)` while being a step function of the same law dates used by the marker → `law × G(C)` double-counts compulsory-length changes | addendum C10.3; `anchor.py` L58–60 vs L77–79 | any capacity-timing claim is contaminated until the proxy is measured independently (self-disclosed, not repaired) |
| **D-10** | S1 | A2d runs with the push channel off (arm dict passed where a year→value series is expected) | `anchor.py` L163 (`th['push_series'] = armser['capacity_gated']`) vs `pushpull.py` L106 | the capacity-leads-intake test is invalid; its negative conclusion is unsupported |
| **D-11** | S1 | `scaling_check.csv` has **no generator script** in the tree | grep: only `STATUS.md`/`PHASE_WRITEUP_SHELL.md` mention it; no `.py` computes `generated_exponent` | the programme's central negative number is an orphan artefact with no reproducible pipeline |
| **D-12** | S2 | the completion-law containment compares a **logit** slope to a **log-log** range | `repair.py::exps` (logit) vs `repair.A3['completion_low']` = [0.169,0.2468] from `relations/data/scaling_laws.csv` S4 | the "contained 0/3" row for the completion law is a unit mismatch, not a finding |
| **D-13** | S1 | the two scaling targets are mutually inconsistent: A1 requires secondary **+0.286**, A3 containment is **[0.0904, 0.2154]** | `repair.py` A1/A3 dicts; `relations/data/scaling_laws.csv` S1; `SUCCESS_CRITERIA.md` A1/R14 | a model that generated exactly A1's value would **fail** A3 containment; the criterion is unwinnable on S1 |
| **D-14** | S3 | the A1 "target" is model2's own between estimate (+0.286, se 0.045 = `scaling_estimates.csv` row 1); the A3 range is the relations FE estimator | as above | the target is not independent of one of the two estimators that define it; the "independent estimator" claim covers only the model, not the target |
| **D-15** | S2 | `model2/runs/findings.txt` says the pull terms "fit education better out-of-sample in most countries", while the same file reports demand better in **8/23** | `runs/findings.txt` Part 3 + "STRONGEST DISCRIMINATING EVIDENCE" (i); `runs/rivals.csv` (8 demand, 15 supply) | narrative contradicts data in the load-bearing findings file |
| **D-16** | S2 | accounting checks report **0 failures** while GER is 3–35× too high; B3 only tests completion ≤100 and GER ≥0 | `pushpull.accounting_checks` L149–168; `smoke/accounting_checks.csv`; `smoke/structure_smoke.csv` | "0 accounting failures" is a **false pass**: the check that was supposed to bound rates does not bound GER, so R2's zero-tolerance claim is unearned |
| **D-17** | S2 | `findings.txt` line 10 was hand-corrected (sigmoid → C^0.75) but `anchor.py` L182 still writes the **sigmoid** sentence | `anchor_out/findings.txt` L10 vs `anchor.py` L182; sha of findings = `4c21e3f6…` in `SHA256SUMS` | the committed findings file is **not reproducible** from the committed code; re-running silently reintroduces a wrong gate description |
| **D-18** | S3 | `anchor.py` docstring cites PRE_ANCHOR_A1 sha `b7020cf4…` and PRE_ANCHOR_CAPACITY sha `702d5c7a…`; actual files (and `SHA256SUMS`) are `3f1f2294…` and `f0e21614…` | `anchor.py` L3; `SHA256SUMS` | R12's "predeclaration hash" control does not close: the run's declared authority documents cannot be matched to the committed ones |
| **D-19** | S3 | `06_report/MASSIFICATION_CLOSEOUT.md` does not exist; the closeout is at repo root | `ls 06_report/` | path drift in handoff references |
| **D-20** | S3 | `e6_meta.json` has `"bounded_forms": []` while `e6_findings.txt` applies a rule about "bounded forms" (logistic/Gompertz) | `runs/e6_meta.json` vs `runs/e6_findings.txt` | machine-readable summary cannot reproduce the verdict logic |
| **D-21** | S1 | the K-12 cycle-length switch is **declared but not implemented**: `configs.CYCLE['PHL']` is one constant dict (primary 6 / lower 4 / upper 2) and `pushpull.run` reads `cyc['upper']` with no year dimension | `PRE_ANCHOR_A1.md` M1 ("cycle-length switch + cohort exposure") and A7 (cohort mechanics retained); `configs.py` CYCLE; `pushpull.py` L53, L116–119 | the anchor's K-12 mechanism is a marker only; one of the two mechanisms A7 kept live cannot be tested by this code |

---

## 5. Counts (27 rows in `MODEL_INVENTORY.csv`; 25 gate/diagnostic cells + 2 supporting artefacts)

| verdict | n | cells |
|---|---|---|
| PASS | **1** | `CORE-SMOKE` — automated accounting only, and the automated check is incomplete (D-16); not evidence of structural validity |
| PARTIAL | **3** | `A1-ANCHOR`, `CAL-PHL`, `A5` |
| FAIL | **10** | `CAL-CHN`, `CAL-KHM`, `SCALING-UNREPAIRED`, `SCALING-REPAIR`, `M2-RECOVERY`, `M2C`, `M2B`, `A3A`, `A5B`, `E6` |
| EQUIVALENT | **1** | `A1-CAPACITY` |
| ESTIMATOR (no gate verdict) | **4** | `SCOUT-SCALING`, `M2-SCALING`, `M2-UNIV`, `M2-RIVALS` |
| not-run | **6** | `A2D` (invalid as executed), `A3B`, `PORTABILITY-A6/A7`, `TIMING-JPN/KOR/HKG`, `E2`, `E3` |
| supporting (no verdict) | **2** | `CORE-PUSHPULL` (the core, scored only through A1/CAL/D), `PREDECL-LEGACY` (superseded) |

| status | n |
|---|---|
| load-bearing | 11 (`A1-ANCHOR`, `A1-CAPACITY`, `CORE-PUSHPULL`, `SCALING-UNREPAIRED`, `SCALING-REPAIR`, `SCOUT-SCALING`, `M2-SCALING`, `M2-RECOVERY`, `M2C`, `A5B`, `E6`) |
| diagnostic-only | 9 (`CORE-SMOKE`, `CAL-PHL`, `CAL-CHN`, `CAL-KHM`, `M2-UNIV`, `M2-RIVALS`, `A2D`, `A3B`, `A5`) |
| failed | 2 (`M2B`, `A3A`) |
| not-run | 4 (`PORTABILITY`, `TIMING`, `E2`, `E3`) |
| superseded | 1 (`PREDECL-LEGACY`) |

**Zero PASS among gate-scored model cells.** The single PASS is an automated accounting check that D-16 shows to be
incomplete — it should be read as "the B1–B4 assertions as coded fired zero times", not "the model conserves".

---

## 6. What could not be verified

- **The A1 fitted parameters.** Not on disk (D-03). The 12-arm table cannot be independently reconstructed.
- **`scaling_check.csv` provenance.** No script, no log line producing it, no seed. Its numbers are used verbatim by
  the closeout, the A1 addendum and the write-up shell (D-11).
- **The relations register's own run.** `relations/scripts/scaling_laws.py` is present and readable, but
  `relations/logs_fit.txt` covers the universalization fits, not the scaling laws, and no log for
  `scaling_laws.csv` was found. The FE methodology is legible from code; the executed vintage is not.
- **Any pre-2013 fit of the E2/E3 cells** — never run, so nothing to verify.
- **`06_report/MASSIFICATION_CLOSEOUT.md`** — absent (D-19); the root `MASSIFICATION_CLOSEOUT.md` was read instead.
- **Data cells**: PHL completion values were spot-checked against `10_massification/data/UNIVERSALIZATION_SERIES.csv`
  (1999 primary 83.16, 2017 91.918, 2024 98.305; lower 58.86/81.255/92.414; upper 59.70/76.433/75.025 — all
  `status=observed`). The observed signature quoted in the documents is correct.

---

## 7. What was inspected (sha256-16)

`model/`: `anchor.py` bd96f06745f21570 · `pushpull.py` 0cf3dceb93e28057 · `calibrate.py` 73fe03b70df68925 ·
`repair.py` 07c8f6848baec89c · `configs.py` e935621eddc07b6e · `anchor.log` fa7d52d0418327cd ·
`anchor_out/anchor_table.csv` 2a6d4e8ea76f49d7 · `anchor_out/findings.txt` 4c21e3f64cc3ad0f ·
`anchor_out/run_meta.json` 837784e63a109595 · `anchor_out/A1_ADDENDUM_C1_C10.md` 02c5f47620169b95 ·
`calib/calibration_table.csv` 552e0cce04bd148d · `calib/repair_table.csv` 34b0a5bc98e3d603 ·
`calib/repair_scaling.csv` 7330a8785e28619f · `calib/scaling_check.csv` a07077c4e38253af ·
`calib_phl.log` 52db27496fd42981 · `calib_phl_chn.log` 402148f83d9f3dd7 · `repair.log` bc7e4740c42da54d ·
`smoke/structure_smoke.csv` dc3a244824c46629 · `smoke/accounting_checks.csv` 358ad48783931015 ·
`PREDECLARATION.md` 215bdc500d4740b2 · `PREDECLARATION_AMENDMENT_013.md` 5f7899142176c68d ·
`PRE_ANCHOR_A1.md` 3f1f22947adeb4ed · `PRE_ANCHOR_A2.md` 54527cd9bcacd820 · `PRE_ANCHOR_CAPACITY.md` f0e2161450c7d013 ·
`PRE_PIVOT_ANCHOR.md` a4a39810c96b7f09 · `PRE_SCALING_REPAIR.md` 0f57e51e35973d1a ·
`PRE_TIMING_JPN_KOR_HKG.md` 66100b57659bf1d8 · `PRE_PORTABILITY_A6_A7.md` 533730072d12e16d ·
`PRE_EXP_E2_PH_K12.md` 6447fcc93cc42318 · `PRE_EXP_E3_PH_NURSES.md` 8708015c8abc4428 ·
`A2D_CAPACITY_LEADS_INTAKE.md` a139f6ff03f6f144 · `GATE_TODO.md` e54d7133a0c7cf54 · `README.md` cf3ff2f241b858a8`

`model2/`: `code/m2.py` 383e932122bb84be · `code/m2b.py` e443d837f4a95f81 · `code/m2c.py` b2f779fcd1aa8ea8 ·
`code/a3_a5.py` 6c72bbb22c9c6068 · `code/a5b.py` 989735619d628e95 · `code/e6.py` 4c4a0f1ce3bce4e7 ·
`runs/scaling_estimates.csv` 32c2db22f3d94d0e · `runs/scaling_classification.csv` 757d5ed47d702772 ·
`runs/recovery.csv` 116f18f9824a2451 · `runs/rivals.csv` 7f627f081a74a707 · `runs/logistic_fits.csv` e7f8c9bf6d92bcb8 ·
`runs/logistic_common_tests.csv` 65768870a3869ff0 · `runs/lead_lag.csv` f168240f702a0882 ·
`runs/findings.txt` abb0e7d673deaefb · `runs/model2_meta.json` 9e0918a599b69bdb · `runs/m2b_scaling.csv` 63e658d3d98df86c ·
`runs/m2b_logistic_compare.csv` 4afdbf6894c5e106 · `runs/m2b_findings.txt` 08456fd6aabd0680 · `runs/m2b_meta.json` 8c93100120f2aefb ·
`runs/m2c_recovery.csv` 02e233e55e73380b · `runs/m2c_findings.txt` 9e88769077dd0581 · `runs/m2c_meta.json` 9937d246a8b460d0 ·
`runs/a3_remittances.csv` a5b36db8235bdb1d · `runs/a3b_simulated.csv` ea71c6a50acc498c · `runs/a5_rivals.csv` 64a2f8d8e14aaa40 ·
`runs/a3_a5_findings.txt` 7f20f771e59f1816 · `runs/a3_a5_meta.json` c7238528292096ed · `runs/a5b_scores.csv` 7d36563e60e97e75 ·
`runs/a5b_findings.txt` 79ec9f8dee811615 · `runs/a5b_meta.json` 8fd0f6e52a50c081 · `runs/a5b_final_scoring.txt` 1eb0c97ac6cca411 ·
`runs/a5b_final_meta.json` c39631fa5f8d7b8b · `runs/a5b_pairwise_equivalence.csv`, `runs/a5b_equivalence_to_observed.csv`,
`runs/a5b_rivals_by_milestone.csv`, `runs/a5b_timing_alignment.csv` · `runs/e6_timing_independent.csv` 93dd0608df8d6fb6 ·
`runs/e6_findings.txt` fe92c475b5b8af96 · `runs/e6_meta.json` 3a9efa55804f53ca · docs `PRE_DECLARATIONS_M2.md`,
`EXPERIMENTS_M2.md`, `EXPERIMENTS_M2B_M2C.md`, `EXPERIMENTS_E6.md`, `AMENDMENT_M2b.md`, `ERROR_LOG_M2.md`,
`GATE_ACK_BRIEF013.md`, `A3_PREREG.md`, `A5_PREREG.md`, `A5B_PREREG.md`, `M2C_PREREG.md`, `M2C2_PREREG.md`,
`M2C_INTAKE_GAP_NOTE.md`, `E6_PREREG.md`, `A3_D55_STATUS.md`, `A5B_REPORT.md`, `ANCHOR_CELLS_A3_A5.md`,
`RUN_MANIFEST_M2.json`, `RUN_MANIFEST_M2B_M2C.json`

`relations/`: `scripts/scaling_laws.py` c84198c894c0e157 · `data/scaling_laws.csv` a80bd206893112b5 ·
`data/universalization_fits.csv` 1641c174c084d66b · `logs_fit.txt`

gate / write-up: `08_council/brief_013/SUCCESS_CRITERIA.md`, `STOP_RULES.md`; root `MASSIFICATION_CLOSEOUT.md`;
`10_massification/lit/PHASE_WRITEUP_SHELL.md`; `10_massification/STATUS.md` (read for provenance cross-checks);
`SHA256SUMS`; `10_massification/data/UNIVERSALIZATION_SERIES.csv` (spot-check only).
