# Lab battery 2026-11-20_b — 15 predeclared experiments (5 clusters × 3)

**Status: PREDECLARED BEFORE ANY RUN. Thresholds, falsifiers and verdict vocabulary in this file are frozen at
its sha256 (see `RUN_MANIFEST.json`); no threshold may be changed after results are seen.**
Extension of `lab_2026-11-20` (E1–E10) into post-secondary absorption, tertiary crossing structure, geo-size
scaling, regional post-secondary proxies and a geo-fragmentation simulation.
**Labels:** every cell carries `observed` / `derived` / `check` / `simulated`. Proxies are **declared** below and
labelled `derived`. **No causal and no direction claims** (push vs pull direction stays barred, R13/D77); results
are descriptive/associational. The phase remains **CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT; this battery does
**not** reopen C1–C4 (D76). Cluster 5 is **SIMULATED — not evidence** (labelled in every row and file).

## 0. Data on disk (read-only), units and labels

| id | file | rows | content | status carried |
|---|---|---|---|---|
| D1 | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | 2,458 | 6 systems (KHM/CHN/HKG/JPN/KOR/PHL), GER/completion/NER/OOS/population, 1970–2025 | observed (source vintage on row) |
| D2 | `10_massification/data/UNIVERSALIZATION_TIMING.csv` | 128 | crossing years by level × threshold (15/50/90/95), band, censoring | observed/derived/reconstructed per row |
| D3 | `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` | 5,622 | 39 series × 6 systems, 1995–2024 (incl. wage-share, services, agri, GDP p.c. PPP, urban, population) | observed (ILO/WDI modelled labelled in source) |
| D4 | `09_relations/data/panel_wdi_long.csv` | 63,571 | 30-country WDI long panel, 62 indicators, 1971–2024 | observed (WDI modelled where noted) |
| D5 | `09_relations/data/panel_wdi_wide.csv` | 1,951 | same 30-country panel, wide | observed |
| D6 | `09_relations/data/economic_complexity_panel_30ctys.csv` | 896 | 30 countries, 1995–2024, `eci_sitc`/`eci_hs92` | observed (ECI) |
| D7 | `10_massification/data/BASELINE_SERIES.csv` | 145 | PHL 17 regions × cohorts 1960–64 / 1990–94: education Gini, mean years of schooling, by sex | observed (PIDS 2025, published tabulation) |
| D8 | `10_massification/data/STATE_CAPACITY.csv` | 1,800 | fiscal/delivery/enforcement dimensions | observed/check/unable |
| D9 | `10_massification/data/POLICY_TIMELINE.csv` | 18 | dated policy events | policy fact |

**Six-system sample** = KHM, CHN, HKG, JPN, KOR, PHL. **30-country sample** = the 30 ISO3 in D4/D5/D6.

### Declared proxies (fixed before running — all `derived` unless stated)

- **`ABSORB_F` (formal-absorption proxy)** = `SL.EMP.WORK.ZS`, wage-and-salaried workers as % of total employment
  (ILO modelled estimate; label `observed-modelled`). Proxy for **formal-sector absorption** of the labour force.
- **`ABSORB_S` (structural absorption proxy)** = `SL.SRV.EMPL.ZS`, services employment share (ILO modelled).
  Secondary/sensitivity proxy; a Q-expansion reading is *not* claimed — it is a structure variable.
- **`ABSORB_AG`** = `SL.AGR.EMPL.ZS`, agriculture employment share (residual structure proxy).
- **`GRAD_SUPPLY`** = `SE.TER.CUAT.BA.ZS`, population with tertiary (BA+) attainment, 25+ (WDI modelled; `derived`).
- **`QUEUE` (graduate-queue depth, derived)** = `GRAD_SUPPLY / ABSORB_F × 100` = BA+ holders per 100
  wage-and-salaried jobs. Higher = more degree-holders per formal job. **Declared as DERIVED proxy, not a measured
  queue.** Where `ABSORB_F = 0` or missing the cell is dropped (never imputed).
- **`MARKETS` (number-of-markets proxy, derived)** = `SP.URB.TOTL.IN.ZS/100 × SP.POP.TOTL / 1,000,000` = urban
  population in millions, i.e. **one predeclared "market" per 1,000,000 urban residents**. Stated as a proxy; no
  claim that this equals the number of actual local markets/exam centres/school districts.
- **`SIZE`** = `log(SP.POP.TOTL)`; **`URBAN`** = `SP.URB.TOTL.IN.ZS`; **`LGDP`** = `log(NY.GDP.PCAP.PP.CD)`.
- **`SEC`** = `SE.SEC.ENRR.UP` (upper-secondary GER) where used; **`TER`** = `SE.TER.ENRR` (tertiary GER).

### Estimators (fixed)

- OLS with **country-clustered** SEs (CR1, G/(G−1) correction) for panel slopes; `within` = country-demeaned,
  `between` = country means. Report slope, se, 95% CI (normal), n, number of clusters. No controls except where
  a specification says so; every specification listed is run and reported.
- Spearman rank correlation for small-n structure comparisons (n ≤ 6), with n always reported.
- Medians and [IQR] across countries; "inside cross-country IQR" = value in [Q1, Q3] of the cross-country
  distribution of that variable at crossing.

### Verdict vocabulary (fixed)

`SUPPORTED` / `NOT SUPPORTED` / `PARTIAL` / `DATA LIMITED` / `UNABLE` / `SIMULATED-THRESHOLD-MET` /
`SIMULATED-THRESHOLD-MISSED`. `PARTIAL` = sign/met in one specification set but not both declared sets.
All cells are reported, including nulls and failures. `DATA LIMITED` = fewer usable observations than the
predeclared minimum; `UNABLE` = the estimand is not computable on disk (never replaced by a guess).

---

# CLUSTER 1 — Post-secondary absorption (X1–X3)

**Question:** does tertiary expansion move together with formal/graduate absorption, and is any association
replicable at 30-country scale? **ABSORB_F is the primary declared absorption proxy (`ABSORB_F`); `ABSORB_S` is the
predeclared sensitivity proxy.** Absorption is **not** measured directly on disk (no graduate employment/unemployment
series by education); every result is a proxy association, not an absorption rate.

## X1 — tertiary expansion vs formal absorption, 6 systems (1995–2024)
- Unit: country-year. Sample: 6 systems; observed 1995–2024 on D3. Dep: `TER`; regressors: `LGDP`, `URBAN`,
  `ABSORB_F`. Estimand: **within** (country-demeaned) and **between** partial slope of `TER` on `ABSORB_F`.
- **Threshold:** *SUPPORTED* if the within slope CI excludes 0 **and** the sign is the same as the `ABSORB_S`
  sensitivity (same spec with `ABSORB_S` in place of `ABSORB_F`). *PARTIAL* if only one of the two.
  **Falsifier → NOT SUPPORTED:** within CI includes 0, or the sign flips between the two absorption proxies.
- Small-n warning declared: 6 countries / 5–6 effective clusters; magnitudes not transferable.

## X2 — 30-country replication of X1 (1995–2024)
- Unit: country-year on D4 (30 countries). Same dep/regressors. Estimand: pooled and between slope of `TER` on
  `ABSORB_F`, country-clustered.
- **Threshold:** *SUPPORTED (replication)* if the 30-country within/pooled slope lies **inside the X1 within 95% CI**
  and sign agrees; *PARTIAL* if sign agrees but point is outside the interval.
  **Falsifier → NOT SUPPORTED:** point outside the X1 CI with opposite sign.
- Minimum for a verdict: ≥10 countries and ≥100 observations; else DATA LIMITED.

## X3 — graduate-queue depth vs tertiary expansion, 30 countries
- Unit: country-year on D4/D5. Dep: `QUEUE` (derived); regressor: `TER`; three predeclared specifications:
  (a) levels, country FE; (b) `log1p(QUEUE)` on `log(TER)`; (c) first differences (Δ) of both.
- **Threshold:** *SUPPORTED* if the `TER` coefficient CI excludes 0 and is **sign-stable across ≥2 of 3**
  specifications. *PARTIAL* if 1 of 3. **Falsifier → NOT SUPPORTED:** CI includes 0 in ≥2 of 3.
- Data minimum: ≥10 countries. If `SE.TER.CUAT.BA.ZS` usable cells < 60, report DATA LIMITED.
- Note: `QUEUE` mixes a modelled attainment stock with a modelled employment share; its *level* is not
  interpretable as a measured queue, only its **relative movement** within country.

---

# CLUSTER 2 — Tertiary crossing structure (X4–X6)

**Question:** do tertiary milestones (massification ≥15% GER, universalization ≥50% GER) require the same
economic-structure package as secondary milestones, or a different one?
Milestones are read from D2 (`tertiary`/15, `tertiary`/50, `secondary`/50, `secondary`/90, `upper secondary`/50);
crossing years **never fitted** (R4/A4). Structure variables at the crossing year, read from D3 (6 systems):
`LGDP`, `URBAN`, `ABSORB_S`, `ABSORB_AG`.

## X4 — structure typicality at tertiary crossings vs secondary crossings
- Unit: country × milestone. For each milestone set, compute median [IQR] across countries of each structure
  variable at the **band midpoint** of the crossing year (left-censored: use first observed year; right-censored:
  use last observed year and mark `right-censored`, no median claim).
- **Threshold:** a milestone set is *structure-typical* if, for the same variable, **≥4/6 countries** fall inside
  the cross-country IQR **on ≥2 of 3 structure variables** (`LGDP`, `URBAN`, `ABSORB_S`).
  **Falsifier → NOT SUPPORTED:** ≤3/6 on ≥2 of 3 variables.
- Declared reporting: both milestone sets {tertiary 15, tertiary 50} and {secondary 50, secondary 90} reported;
  the number of dated crossings per set is reported (12 rows in D2 for tertiary thresholds over 6 systems;
  censored rows excluded from medians but reported).

## X5 — same package or different package? (direct contrast)
- Unit: milestone set. Estimand: for each of `LGDP`, `URBAN`, `ABSORB_S`, the difference in median at
  **tertiary-50** crossings vs **secondary-90** crossings; and the pooled cross-country IQR width per variable.
- **Threshold:** *same package* if |difference in medians| ≤ 0.50 × pooled IQR width in **≥2 of 3** variables;
  *different package* if |difference| > 0.50 × pooled IQR in ≥2 of 3. (50% of IQR is the predeclared overlap rule.)
  **Falsifier:** if the per-variable sign of the difference is not consistent with a single ordering, report
  PARTIAL and the variable-level table, never a package claim.
- Minimum: ≥4 dated crossings in each set, else DATA LIMITED.

## X6 — spacing between secondary and tertiary crossings vs structure
- Unit: country. Dep: gap = (tertiary-50 crossing year − secondary-50 crossing year) (or secondary-90 if
  secondary-50 censored; the substitution is declared per country and reported). Regressor: same structure
  variables at the **secondary** crossing.
- Estimand: Spearman ρ per structure variable; n = number of countries with both crossings dated.
- **Threshold:** *structure-related* if |ρ| ≥ 0.70 for ≥2 of 3 variables with consistent sign; *NOT SUPPORTED*
  if |ρ| < 0.40 for all. **Falsifier → UNABLE:** fewer than 4 countries with both crossings dated (predeclared:
  n≥4 is the floor for any ρ to be reported; n≤3 → UNABLE).

---

# CLUSTER 3 — Geo-size scaling (X7–X9)

**Question:** do population/urban size and the number-of-markets proxy scale with tertiary/secondary GER, and does
the city-state (HKG) behave differently from large systems (CHN/PHL/KHM)? **Explicit small-n caveats everywhere.**

## X7 — size and tertiary/secondary GER, 30 countries
- Unit: country-year on D4, 1995–2024 (primary window), 30 countries. Dep: `TER` (and `SEC` as secondary dep).
  Regressors: `SIZE`, `MARKETS`, `LGDP`, `URBAN`. Four fixed specifications: (a) between (country means),
  (b) within (country-demeaned), (c) pooled with country FE, (d) pooled without controls — all reported.
- **Threshold:** *size-scaled* if the `SIZE` coefficient CI excludes 0 with the same sign in **between** and
  **within**, and the point estimate is ≥ 0.10 in at least one; *PARTIAL* if only one of between/within.
  **Falsifier → NOT SUPPORTED:** CI includes 0 in both, or sign flips between between and within.
- Do not multiply by `MARKETS` and `SIZE` jointly (collinear by construction: `MARKETS` = urban pop in millions);
  `SIZE` specs and `MARKETS` specs are **separate** and both reported. Min: ≥10 countries.

## X8 — city-state vs large systems (HKG vs CHN/PHL/KHM)
- Unit: system. Sample: HKG (city-state/autonomous) vs the three large systems. Dep: duration tertiary-15 →
  tertiary-50 crossing (from D2) and volatility = SD of annual changes in `TER` (D1).
- **Threshold:** *faster* if duration(large)/duration(HKG) ≥ 1.5; *smoother* if volatility(large)/volatility(HKG)
  ≥ 2.0. **Falsifier → NOT SUPPORTED:** both ratios < 1.2. n ≤ 4 per side — **descriptive only, no inference,
  no "scaling law" claim**; report every individual ratio, not only the median.
- If HKG or a large system lacks a dated tertiary-50 crossing, report the censored case as UNABLE for that pair
  and use the remaining pairs; n = number of usable pairs is reported.

## X9 — number-of-markets proxy and tertiary GER, 6 systems + 30 countries
- Unit: country-year. Sample: (i) 6 systems on D3 1995–2024; (ii) 30 countries on D4. Dep: `TER`. Regressor:
  `MARKETS` (derived; one market per 1M urban residents). Specs: between and within, each with and without `LGDP`,
  all four reported; country-clustered.
- **Threshold:** *association* if the within CI excludes 0 and the sign is stable across the two samples
  (6-system and 30-country); *PARTIAL* if supported in one sample only.
  **Falsifier → NOT SUPPORTED:** CI includes 0, or sign flips between the two samples.
- Declared caveat: `MARKETS` is mechanically a monotone transform of urban population; an association with GER is
  **not** evidence that "more markets" matter — any association must be read against the `URBAN`-only spec that is
  also reported (same estimator, `URBAN` in place of `MARKETS`). If the two specs disagree in sign, the result is
  reported as NOT SUPPORTED for the market-count reading.

---

# CLUSTER 4 — Regional post-secondary proxy (X10–X12), Philippines

**DECLARED LIMITATION (binding for every cell in this cluster): regional tertiary enrolment is NOT observed on
disk. There is no PHL regional tertiary GER/participation series. All cells use regional attainment/inequality
proxies from D7 (PIDS 2025, published tabulation, two cohorts) and national tertiary GER from D1; no cell is a
measurement of regional post-secondary participation, and no causal or policy-effect claim is made.**

## X10 — regional convergence in schooling across cohorts
- Unit: region (17) × cohort (1960–64, 1990–94), D7, sex-aggregated (mean over the two sex rows; report sex-split
  as a check). Dep: ΔMYS = MYS(1990–94) − MYS(1960–64). Estimand: Spearman ρ(ΔMYS, MYS_initial) across 17 regions.
- **Threshold:** *convergence* if ρ < 0 and ≥12/17 regions have ΔMYS > 0. *NOT SUPPORTED* otherwise.
  **Falsifier → NOT SUPPORTED:** ρ ≥ 0 or <12/17 improving.

## X11 — regional inequality and the national tertiary expansion
- Unit: region (17) × cohort. Dep: ΔGini = Gini(1990–94) − Gini(1960–64). Estimands: (a) count of regions with
  ΔGini ≤ −0.02; (b) Spearman ρ(ΔGini, Gini_initial); (c) side-by-side national tertiary GER 1971→2024 (D1)
  reported as context ONLY (not regressed, no causal read).
- **Threshold:** *post-secondary-proxy equalizing* if Gini falls ≥0.02 in ≥10/17 regions AND ρ(ΔGini, initial Gini) < 0.
  **Falsifier → NOT SUPPORTED:** fewer than 10 improve, or ρ ≥ 0.

## X12 — whose schooling grew more? (gradient by initial attainment)
- Unit: region (17). Estimand: ratio of median ΔMYS in the bottom-quartile regions by initial MYS to the
  top-quartile regions (quartiles formed on MYS_initial across the 17 regions; declare exact quartile membership).
- **Threshold:** *pro-poor gradient* if ratio(bottom/top) > 1.0; *NOT SUPPORTED* if ratio ≤ 1.0.
  Report the full 17-region table, the quartile cut-offs and the medians.
- Note: this is a **change-in-attainment proxy**, not a post-secondary expansion measure; `DATA LIMITED` is not
  triggered (17/17 regions observed) but the **limitation above is printed in the results row**.

---

# CLUSTER 5 — Geo-fragmentation simulation (X13–X15) — **SIMULATED, NOT EVIDENCE**

**Stipulated toy model (fixed before running; stdlib-only Python preferred, numpy allowed; deterministic with
declared seeds).** A system is split into K ≥ 1 regions/markets. Each market k has: capacity `cap_k` (max annual
intake as a share of its cohort), a participation ceiling `ceil_k` drawn from `U[0.35, 1.00]` (heterogeneous
ceilings — the fragmentation channel), and a share `s_k` of the national cohort (equal shares by construction unless
a check says otherwise). Demand/pressure `d_t` grows logistically: `d_{t+1} = d_t · r · (1 − d_t/dmax)` with
`r = 0.08`, `dmax = 1.10`, `d_0 = 0.10`. Aggregate participation at t = Σ_k s_k · min(d_t, cap_k, ceil_k).
National cohort weight is constant. Ceiling crossing = first t with aggregate participation ≥ 0.50; if it never
crosses within 80 periods, right-censored (report as >80, never imputed). **All outputs labelled SIMULATED.**
Ambient seeds: ≥200 per cell, base seed declared (20261120); same latent draws across counterfactuals (**paired**).

## X13 — does splitting delay the ceiling crossing?
- K ∈ {1, 2, 4, 8, 16, 32}; 200 seeds/cell; capacity per market scaled so Σ cap_k is constant (total capacity fixed)
  unless the split is declared to change total capacity (sensitivity cell reported separately).
- Estimand: median crossing year by K; Δ = median(K=32) − median(K=1).
- **Threshold (SIMULATED-THRESHOLD-MET):** Δ ≥ 3 years. *PARTIAL* if 1 ≤ Δ < 3. **Falsifier:** |Δ| < 1 year.
- Report the **full distribution** (median, IQR, % right-censored), not only the median.

## X14 — does splitting smooth the approach to the ceiling?
- Same design. Estimand: volatility = SD of annual aggregate participation changes computed over the crossed
  pre-ceiling window; ratio V = volatility(K=1)/volatility(K=32), median over seeds.
- **Threshold:** *smoother* if V ≥ 1.5; *PARTIAL* if 1.1 ≤ V < 1.5. **Falsifier → NOT SUPPORTED:** V < 1.1.

## X15 — heterogeneity dose: fraction of closed/ceiling-bound markets
- Same design with K = 8; fraction f ∈ {0, 0.25, 0.50, 0.75, 1.0} of markets whose ceiling binds **below** the
  national demand path (declared operationalisation: `ceil_k` capped at 0.40 for a binding market — a stipulated
  closure; the remaining markets keep `U[0.35,1.00]`). 200 seeds/cell.
- Estimand: median crossing year by f; Spearman ρ(crossing year, f) over the 5 f-cells.
- **Threshold:** *monotone delay* if ρ ≥ 0.90 **and** median(f=1.0) − median(f=0) ≥ 2 years; *PARTIAL* if ρ ≥ 0.90
  with smaller delay. **Falsifier → NOT SUPPORTED:** ρ < 0.90.
- Declared saturation read: report whether the delay effect from f=0→0.5 exceeds the f=0.5→1.0 effect (diminishing
  returns); no threshold attached to that sub-read (reported, not adjudicated).

---

## Reporting rules (binding for every cluster)

1. Predeclared thresholds fixed at this file's sha256; results may not change them. Any deviation = disclosed
   amendment in the cluster `RUN_MANIFEST.json` **and** in `FINDINGS.md`, labelled post-hoc.
2. Every cell reports `observed` / `derived` / `check` / `simulated`; proxy-derived cells additionally name the proxy.
3. All specifications declared here are run; nulls, failures and `DATA LIMITED`/`UNABLE` are reported, never dropped.
4. n and number of clusters reported on every regression row; small-n caveats printed where n ≤ 6 or clusters ≤ 6.
5. No causal language, no direction (push/pull) claim, no policy-effect claim. Closed phase untouched (D76).
6. `RESULTS.csv` (battery) has one row per experiment with the predeclared verdict; per-experiment detail lives in
   each cluster's `results/` CSVs and is cited by filename in `FINDINGS.md`.
7. Deterministic: every script seeds declared; re-running reproduces the results CSVs byte-for-byte (checked by the
   consolidation step).
