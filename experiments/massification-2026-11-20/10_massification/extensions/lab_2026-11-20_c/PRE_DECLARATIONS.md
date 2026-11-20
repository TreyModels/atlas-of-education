# Lab battery 2026-11-20_c — five Council-anchored experiments (Y1–Y5)

**Status: PREDECLARED BEFORE ANY RUN.** Thresholds and falsifiers are **copied verbatim from the Council's
brief-017 anchoring blocks** (`08_council/brief_017/SYNTHESIS_017.md` §D, sha256 `47e28af7…`; decisions D88–D92).
The Lead adds only the *operationalisation* needed to make each block executable (declared below, never changing a
threshold). This file is frozen at its sha256 (in `RUN_MANIFEST.json`); no threshold may move after results.
**Authority:** the Synthetic Council (Council-2) issues the 5 experiments per delivered results batch (D89); the
Lead predeclares and executes. **No causal or direction claims; no C1–C4 reopening; phase remains CLOSED at
PARTIAL/DESCRIPTIVE/EQUIVALENT (D76).** Every verdict is descriptive (`SUPPORTED`-as-constraint / `NOT SUPPORTED` /
`UNABLE`), never PASS.

## 0. Data on disk (read-only, all usable per Council D92)

`10_massification/data/`: `UNIVERSALIZATION_SERIES.csv`, `UNIVERSALIZATION_TIMING.csv`, `JOBS_AND_MARKETS_PANEL.csv`,
`STATE_CAPACITY.csv`, `SCHOOL_EXPANSION.csv`, `BASELINE_SERIES.csv`, `POLICY_TIMELINE.csv`.
`09_relations/data/`: `panel_wdi_long.csv` (30 countries, 62 indicators, 1971–2024), `panel_wdi_wide.csv`,
`economic_complexity_panel_30ctys.csv`.
**Blocked/HELD (never sent, user approval required):** PSA microdata, WB Enterprise Surveys, annual
capacity/enforcement, real per-pupil spending, subnational sector employment (E4), the named expansion file.
**No Y experiment needs a new data ask.**

**Estimators (fixed):** Spearman rank correlations on country-level cells; rank-partial correlation = Pearson
correlation of rank residuals after regressing ranks on the ranked control (declared where used). Cross-lag partial
correlations are country-demeaned, reported for every lag/direction. `n` and the number of countries are always
reported. Where cells are too few the verdict is `UNABLE` (never imputed).

**Verdict vocabulary:** `SUPPORTED` / `NOT SUPPORTED` / `UNABLE`. For a *screen that can only earn a candidate
note*, `SUPPORTED` means "the predeclared candidate account survives", `NOT SUPPORTED`/`UNABLE` means "discard".

---

## Y1 — Ceiling-residual candidate-account screen (opportunity-cost vs demand-returns)

**Channel:** markets (demand/returns) + cohort flows — screens which candidate account can be named for the
unexplained ceiling residual (A10/D63).
**Discriminating action:** positive → the A1 write-up may list "foregone income / opportunity cost" as a
*descriptively-supported candidate account* (never a mechanism; no direction claim). Negative → that account is
**UNABLE / discarded** from D63's candidate list.
**Data (no ask):** `panel_wdi_long.csv` (30 countries): `SE.TER.ENRR` (ceiling outcome); `SL.AGR.EMPL.ZS`
(opportunity cost), `SL.UEM.1524.ZS` (youth unemployment), `SL.EMP.WORK.ZS` (formal wage-share = returns/demand);
control `NY.GDP.PCAP.PP.CD`. Check on 6 systems: `UNIVERSALIZATION_SERIES.csv`
(`completion_upper_secondary`, `ger_tertiary`) vs `JOBS_AND_MARKETS_PANEL.csv` (`SL.AGR.EMPL.ZS`,
`SL.EMP.WORK.ZS`).
**Operationalisation (Lead, declared):** ceiling = mean of the **last 3 observed** `SE.TER.ENRR` values per country
(within 2000–2024); each candidate = mean of that country's last 3 observed values of the indicator; income
confound removed by **rank-partial** on `NY.GDP.PCAP.PP.CD` (last-3 mean). Report raw and partial ρ for all three
candidates, plus n.
**Threshold + falsifier (verbatim):** the opportunity-cost account earns a candidate note **only if** the
income-partialled Spearman satisfies ρ(ceiling, agri-share) ≤ **−0.40** AND ρ(ceiling, youth-unemp) ≤ **−0.40**;
**falsifier → UNABLE/discard** if either |ρ| < 0.40 or sign is positive. A discard threshold, never a claim.
**Closed-claim check:** no C1–C4 reopening; between-country Spearman only (R13-safe); no capacity-mechanism claim.
**Cost/rank:** small; rank #1.

## Y2 — Cross-channel lead-lag constraint (schooling ↔ markets)

**Channel:** the central schooling↔markets interaction.
**Discriminating action:** positive (a visible one-way lead) → becomes a predeclared, target-free descriptive
constraint the model class must reproduce in its fit window (a check, never a fitted schedule). Negative (null both
ways) → the write-up states the schooling↔market interaction is **not detectable cross-sectionally** (reinforces
EQUIVALENT); the model is not required to reproduce a lead-lag the data do not show.
**Data (no ask):** `panel_wdi_long.csv` (30 countries, 1971–2024): schooling = `SE.SEC.ENRR`, `SE.TER.ENRR`;
markets = `SL.SRV.EMPL.ZS`, `SL.EMP.WORK.ZS`.
**Operationalisation (Lead, declared):** country-demeaned series for schooling and market variables; cross-lag
**partial** correlations (controlling the own-series lag 1) for lags 1–3 in both directions; full 2×2×3 matrix
reported; n = countries with ≥8 usable observations per pair.
**Threshold + falsifier (verbatim):** "descriptively visible" **only if** one direction has |partial r| ≥ **0.25**
at ≥2 **consecutive** lags with consistent sign **and** the reverse direction is < 0.25; **falsifier → NOT
SUPPORTED** ("interaction not detectable"; equivalence).
**Closed-claim check:** R13-safe — lead-lag *description* only, never a push/pull direction or complementarity
claim; no C1–C4 reopening.
**Cost/rank:** small; rank #4.

## Y3 — Capacity floor-not-ceiling observed check (6 systems)

**Channel:** government (state capacity) + scaling — observed descriptive check of A10/R29.
**Discriminating action:** positive → the write-up may carry a descriptive "capacity correlates with the floor, not
the ceiling" sentence. Negative → D64 crude-proxy caveat dominates; capacity descriptive support reported
**UNABLE**.
**Data (no ask):** `STATE_CAPACITY.csv` (delivery: PTR primary/secondary, teachers), `SCHOOL_EXPANSION.csv` (PHL PTR
path, hires), `UNIVERSALIZATION_SERIES.csv` (`completion_primary`, `completion_lower_secondary`,
`completion_upper_secondary`, `ger_tertiary`), `JOBS_AND_MARKETS_PANEL.csv` (`SE.XPD.TOTL.GD.ZS` fiscal).
**Operationalisation (Lead, declared):** across the 6 systems, `ΔPTR-improvement` = PTR(earliest observed,
≥1995) − PTR(latest observed, ≤2024) for **secondary** PTR (`SE.SEC.ENRL.TC.ZS`/`SE.SEC.PTR` from the jobs panel),
positive = improvement. Floor = latest observed `completion_primary`; ceiling = latest observed
`completion_upper_secondary` (fallback modern `ger_tertiary` if completion missing — recorded per country). Report
all pairwise ρ, n, and each country's values. Predicted sign (declared): **positive** for floor, and |ρ| < 0.50 for
the ceiling.
**Threshold + falsifier (verbatim):** descriptive support **only if** ρ(ΔPTR-improvement, floor level) has the
predicted sign with |ρ| ≥ **0.50** AND |ρ(ΔPTR-improvement, ceiling level)| < **0.50** (or sign-inconsistent);
**falsifier → UNABLE / not separable** otherwise. Six system points only — small-n caveat printed.
**Closed-claim check:** does not reopen C4 (annual observed capacity/enforcement); uses only the already-ruled
partial PTR/teacher path (D53/R26); no "capacity explains timing" claim (D61/R28).
**Cost/rank:** small; rank #3.

## Y4 — World-society rival false-positive check (descriptive null model)

**Channel:** rival comparison (A5b); one pillar of the EQUIVALENT headline.
**Discriminating action:** positive (the null generates upper-secondary ≥90 for a system that never crossed — an R6
false positive) → supports the D77 scoping that the rival field's emptiness rests on ordering/spacing **and** the
upper-secondary non-crossing. Negative (no false positive) → the write-up must **soften** the rival-distinction
claim; the null rival is not distinguished on that margin.
**Data (no ask):** `UNIVERSALIZATION_TIMING.csv` (crossing years, bands, censoring) + `UNIVERSALIZATION_SERIES.csv`
(completion series).
**Operationalisation (Lead, declared):** the predeclared null = "each level crosses its 90% threshold at the
cross-system **median** crossing year for that level (band midpoints; dated crossings only; censored rows
excluded and listed)". A cross-system median is computed per level/threshold from the timing file. "Never crossed"
= the observed series' final value < 90 AND the timing row is right-censored/absent. Count systems where the null
implies a ≥90 crossing but the observed record shows none. Also list every level/country so the scoring is auditable.
**Threshold + falsifier (verbatim):** the rival is *distinguished on the upper-secondary margin* **only if** the
null generates an upper-secondary ≥90 crossing for ≥1 system that never crossed; **falsifier → NOT DISTINGUISHED**
(rewrite the A5b sentence accordingly).
**Closed-claim check:** null-model scoring only; no direction claim; no C1–C4 reopening.
**Cost/rank:** small; rank #2.

## Y5 — Portability design data-completeness audit (design-only)

**Channel:** cohort flows / scaling — portability design to CHN/HKG (PARKED-ARMED, D40/D75).
**Discriminating action:** positive (the D75 six-constraint diagnostic-transfer needs **zero new data asks**) → the
transfer can be predeclared run-ready. Negative (a missing series) → name the exact held DATA ASK; nothing sent.
**Data (no ask):** `UNIVERSALIZATION_TIMING.csv` + `UNIVERSALIZATION_SERIES.csv` (CHN/HKG crossings/spacing/
censoring), `POLICY_TIMELINE.csv` (dated pushes), `JOBS_AND_MARKETS_PANEL.csv` (economy inputs).
**Operationalisation (Lead, declared):** fill the D75 transfer checklist with one row per required input: initial
cohorts, observed economy series, policy dates, capacity trajectory, level-gate mapping, measurement definitions.
Each row = input, the on-disk file/indicator that supplies it (or NONE), status `present-on-disk` /
`already-held-ask` / `NEW-ASK` (must be none), and the CHN and HKG values where present. Output = checklist CSV +
a verdict row. No model run, no portability claim.
**Threshold + falsifier (verbatim):** "data-complete" **only if** every D75 input is present-on-disk or
already-ruled-held (no *new* data ask); **falsifier** = any newly-named missing series → recorded as a held DATA ASK
and the design marked `BLOCKED-ON-DATA` for that input.
**Closed-claim check:** design-only — no run, no portability claim, no C1–C4 reopening (D75).
**Cost/rank:** small; **rank #5 → DROP-FIRST** (de-risks a parked path; changes no verdict now).

---

## Reporting rules (binding)

1. Predeclared thresholds frozen at this file's sha256; no post-hoc change. Any deviation → disclosed amendment in
   the run manifest and FINDINGS.
2. Every cell reports its label (`observed`/`derived`); proxies named; `UNABLE`/`NOT SUPPORTED` reported, never
   dropped.
3. n and n_countries on every correlation row; small-n caveat where n ≤ 6.
4. No causal language; no direction (push/pull) claim; no policy-effect claim; closed phase untouched (D76).
5. Deterministic scripts, fixed seeds (no RNG needed except any seeded resampling, which must be declared);
   the Lead re-runs every script and requires byte-identical results.
6. **Drop-first = Y5.** If the fleet were thin, run Y1/Y4/Y3 first (Council D90 ranking); Y5 is ordered here for
   completeness of the slate and is labelled design-only.
