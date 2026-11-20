# CAPACITY_LAYER — state capacity: trajectory, alignment with crossing years, and the model gate

**Author:** `pattern-scout` · task-36 capacity layer · 2026-11-20 · write scope `10_massification/relations/`.
**Status: descriptive; capacity is an OBSERVED INPUT series, never a fitted parameter.** No direction claims (R13).
`10_massification/data/STATE_CAPACITY.csv` (data-hunter) was **not on disk** at the time of writing; this layer is built
from public observed series on disk and will be reconciled when that file lands. Governance (WGI) is **BLOCKED**
(WDI API returned HTTP 000/timeout for `GE.EST` during this window) — recorded, not substituted.

**Files:** `data/state_capacity.csv` (country-year components + index + coverage), `data/capacity_alignment.csv`
(milestone alignment), `data/capacity_leadlag.csv` (within-country lead-lag), `data/capacity_crosscountry.csv`
(cross-country association), `scripts/state_capacity.py`.

## 1. The index — declared construction

**Components (all observed; raw values kept in the CSV):**

| weight | component | source | direction |
|---|---|---|---|
| 0.15 | education spending, % of GDP | WDI `SE.XPD.TOTL.GD.ZS` | higher = more capacity |
| 0.10 | education, % of government expenditure | WDI `SE.XPD.TOTL.GB.ZS` | higher = more priority |
| 0.20 | tax revenue, % of GDP (revenue capacity) | WDI `GC.TAX.TOTL.GD.ZS` | higher = more capacity |
| 0.05 | government expenditure, % of GDP (state size) | WDI `GC.XPN.TOTL.GD.ZS` | higher = more capacity |
| 0.30 | primary teachers per pupil (inverted pupil-teacher ratio) | WDI `SE.PRM.ENRL.TC.ZS` | **inverted**: lower PTR = more capacity |
| 0.10 | teacher stock per 1,000 population | WDI `SE.PRM.TCHR` + `SE.SEC.TCHR` / `SP.POP.TOTL` | higher = more capacity |
| 0.10 | primary spending per pupil, % of GDP pc | WDI `SE.XPD.PRIM.PC.ZS` (sparse) | higher = more capacity |
| **0.15** | **governance / enforcement proxy: WGI government effectiveness** | **`GE.EST` — BLOCKED** | **not included; index renormalises over the other 0.85** |

Two normalisations, declared: **`capacity_index`** uses fixed panel-wide 5th–95th percentile bounds (comparable across
countries, but composition-sensitive); **`capacity_within`** uses each country's own 1971–2024 min/max (a *trajectory*
measure, comparable over time within a country, not across countries). Every row carries `n_components` and
`weight_coverage` (share of the 1.0 declared weight actually available); rows with coverage < 0.55 are dropped from the
time-series tests. **Weight sensitivity** (recomputed with equal weights / delivery-heavy / fiscal-heavy):
correlation with the declared index **0.973 / 0.955 / 0.896** — the trajectory is robust to the weights. Missing
components are never imputed; they change the composition, which is why coverage is reported on every row.

## 2. The anchor question — did PHL's completion crossing follow capacity or the law?

**Capacity trajectory (PHL, capacity_within 0–100; weight_coverage in parentheses):**
58.9 (2005, 1.00) → **83.4 (2019, 0.60)** → **89.1 (2021, 0.60)** → 83.6 (2023, 0.60).
**+35.2 index points** from the mean of the five years before the primary-universal crossing (49.5) to the crossing
year (84.7).

**Raw components behind it (WDI, observed):** primary pupil-teacher ratio **32.7 (1990) → 35.3 (2000) → 35.1 (2005) →
31.4 (2009) → 30.3 (2015) → 29.0 (2016) → 29.1 (2017)** — i.e. delivery improved from ~2005 and sharply after 2013.
Education spending %GDP 2.33 (2005) → 2.83 (2015) → **3.96 (2017)**; tax/GDP 11.9 (2005) → 13.0 (2015) → 13.6 (2017).
From `SCHOOL_EXPANSION.csv` (data-hunter, observed/`check`): ~200,000 K–6 teachers and ~40,000 senior-high teachers
hired 2012–2016 (PIDS 2025, ch.4 p.97, `check`); elementary students-per-classroom **39 (2010) → 29 (SY2019-20) → 32
(2021)** (DepEd/NEDA via PIDS 2025, `high`).

**Note on the directive's "PTR 37→27→24":** WDI primary PTR for PHL does **not** reproduce those numbers (it runs
~32–35 in the 1990s–2000s and ~29–30 by 2016–17). The 37→27→24 path is closer to a **classroom/teacher ratio** series;
the observed classroom ratio here is 39→29 (2010→2019) and 39→32 in the PIDS/NEDA series. Different denominator
definitions — both are reported, neither is spliced.

**Alignment with the crossing years:**

| PHL milestone | Observed crossing | 1987 law gap | Capacity at crossing (index) | Capacity change in the 5y before | Alignment verdict (descriptive) |
|---|---|---|---|---|---|
| primary universal | **2017–21** (mid 2019) | **+31 years** | 84.7 | **+35.2** | **capacity timing aligns; law timing does not** |
| lower-secondary universal | **2023–24** | +36 years | 87.5 | +4.4 | capacity already high and rising; law does not align |
| upper-secondary mass | **≤1999** (censored) | −14 years (before K-12) | 74.0 | +3.0 | massification PRECEDED both the K-12 law and the capacity peak |
| tertiary mass | **2024–25** | +6.5y after free tuition | 91.5 | +5.8 | capacity rising; free-tuition window itself negative (event layer) |

**Anchor verdict (descriptive, not causal):** in the Philippines, the **capacity build-up lines up with the universalization
crossing years far better than the statutory dates do** — the 1987 constitutional mandate precedes the primary crossing
by 31 years, the K-12 extension comes after upper-secondary massification had already occurred, and the crossings occur
in the period of sharpest capacity improvement (2005–2021). **This is an alignment statement, not identification:** the
capacity build-up is plausibly a *response* to participation demand at least as much as a cause of it, and the data
cannot order the two. R13 bars a direction claim.

## 3. Cross-country: does capacity predict crossing timing? (descriptive; the honest answer is no)

Spearman between mean 1980–2000 capacity and the crossing year (six countries, n=5 with datable crossings):
primary ρ=+0.15 (p=0.81), lower-secondary ρ=+0.10 (p=0.87), upper-secondary mass ρ=+0.41 (p=0.49), tertiary ρ=+0.30
(p=0.62). **All signs are the "wrong" way (higher capacity → later crossing) and none is significant.** Per-country
alignment: PHK (+35.2 before crossing) and KOR (+3.8, +6.4 before its censored crossings) show capacity rising;
**CHN falls** before its primary/lower-secondary crossings (−5.2, −12.6) and **HKG falls** before its primary (1978)
and tertiary (2007) crossings (−6.8, −16.0) — because their capacity build-up happened *earlier* than the recorded
crossing. So capacity alignment is **country-specific, not a cross-country law**.

**What cannot be identified:** (i) the causal direction between capacity and participation; (ii) the capacity level
before 1971 for the near-universal systems (censored); (iii) the governance/enforcement component (WGI blocked);
(iv) whether the index's composition shift (coverage 1.00 in 2005 vs 0.60 in 2019) drives the PHL result — the raw
components say the direction is real (PTR fell, spending rose), but the index magnitude is composition-sensitive;
(v) cross-country with n=5 on censored outcomes.

## 4. The model gate — declared functional form (observed input, not fitted)

**Declared, not estimated.** Capacity enters the anchor model as an **observed gate series** `K_t = capacity_index/100`
(use `capacity_index` for cross-country comparability, `capacity_within` for within-country trajectory; state which).
No coefficient is fitted to K.

1. **`massabm` (anchor, PHL):** use the model's existing cost-multiplier form — unit cost of a school place
   `= base_cost × (1 + cap_cost × (1 − K_t))`, with **`cap_cost = 0.5` as the model's declared default, NOT re-estimated**;
   equivalently, the state's ability to convert spending into places is `places_t = min(seats_demanded, K_t × spend_t / unit_cost)`.
   A capacity path is supplied from the observed series (`data/state_capacity.csv`), interpolated only between observed years
   (never extrapolated before the first observation; censored pre-1971 countries use the first observed year and are flagged).
2. **`twoway` (portability check):** capacity scales provider fixed cost `F_cm_eff = F_cm × (1 + λ(1 − K_t))` with **λ a
   declared sweep parameter (not fitted)**, and gates state seats as above. Report the model's crossing years against the
   observed ones; the gate is PASS only if the model produces the crossing years **without** K being reverse-engineered
   (i.e. with `K_t` supplied from data, not chosen to fit the outcome).
3. **Validation experiment (declared):** feed the observed PHL capacity path 1970–2024 into `massabm`; the model must
   produce primary universal crossing in **2017–21** and lower-secondary in **2023–24** within the ±5-year tolerance in
   SUCCESS_CRITERIA, and must NOT produce universalization where the observed series did not cross. If the model needs a
   *fitted* capacity coefficient to hit those years, the gate fails and that is the finding.
4. **Sensitivity:** run the gate with `cap_cost ∈ {0.25, 0.5, 1.0}` and `λ ∈ {0, 0.5, 1.0}`; report which arms survive.
   The index-weight sensitivity (0.973/0.955/0.896) is the uncertainty on K itself.

## 5. Files and reproduction

| File | Content |
|---|---|
| `data/state_capacity.csv` | 1,182 country-years × 30 countries, 1971–2024: raw components, normalised components, `capacity_index`, `capacity_within`, `n_components`, `weight_coverage`, declared weights string |
| `data/capacity_alignment.csv` | six countries × four milestones: capacity 5y before/at/after the crossing, change, rising flag |
| `data/capacity_leadlag.csv` | within-country 5-year-difference lead-lag correlations (capacity vs completion) |
| `data/capacity_crosscountry.csv` | Spearman capacity(1980–2000) vs crossing year, per level |
| `scripts/state_capacity.py` | reproduction (also documents the blocked WGI call) |
| `raw/` | WGI attempts (empty/failed) — the block is recorded |
