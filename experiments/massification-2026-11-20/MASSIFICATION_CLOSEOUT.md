# Massification-first phase — CLOSEOUT

**Programme:** massification / universalization of education, schooling–government–market interaction,
push–pull between education and jobs/markets, scaling laws; shadow education secondary.
**Branch:** `experiment/massification-2026-11-20` · **authoritative tip:** `787f1792382b3aa4877e582f70acbc483287583a`
· **ZIP:** 13,853,346 B / 1,187 files, sha256 `5de0b4a62c9377224e9563f5773e1a9d1d304c8833664a804b20d3844373cebf`.
**Status:** stopped at the predeclared limit condition — **identification limits established for the
model class and evidence base**, with one anchor trajectory partially reproduced and documented as such.
**Honest headline (exact):** *“Conditional LEVEL reproduction + observational equivalence + an unreproduced
asymmetry.”*

## 1. What was built

- **Theory layer** (`10_massification/lit/`): massification theories, push–pull rivals, scaling-laws review,
  rival models on one record (`RIVAL_MODELS_ANCHOR.md`), state-capacity literature, dated timelines,
  phase write-up shell (`PHASE_WRITEUP_SHELL.md`).
- **Data layer** (`10_massification/data/`): jobs & markets panel (5,622 rows), universalization series
  (2,458 rows), baseline PHL regions/cohorts (144 rows), school expansion (27 rows, 19 observed),
  state capacity (1,799 rows: fiscal 611 / delivery 509 / enforcement 679), universalization timing
  (128 rows: 80 observed, 42 reconstructed flagged, 6 unable), policy timeline (18 rows).
- **Empirics** (`10_massification/relations/`): universalization fits (634 fits), universalization timing
  and pattern, E6 shape/timing comparisons, scaling laws (within/between), push–pull lead–lag, event windows
  (20 rows), capacity index (1,182 country-years × 30 countries).
- **Models** (`10_massification/model/`, `model2/`): declared cohort-flow push–pull model (`pushpull.py`,
  three rivals as channel switches), anchor model with 12 arms, rivals A5/A5b, M2b/M2c identification cells,
  E6 timing comparison, A2d capacity-leads-intake, threshold-13 gate predeclarations.
- **Gates** (`08_council/brief_013/`): A1–A10, R1–R29, D1–D78, `INTAKE_ACCEPTANCE.md`,
  `COUNCIL_STATE.md`, `COUNCIL2_INTAKE.md`, `ANCHOR_SYSTEM.md`, `ANCHOR_SLATE.csv`.

## 2. Results

### Anchor (Philippines) — CLOSED at PARTIAL / DESCRIPTIVE / EQUIVALENT (D76)
- Observed signature: primary completion ≥90 in **2017**; lower-secondary ≥90 in **2024**; upper-secondary
  **never ≥90** (75.03 in 2024); tertiary GER ≥50 in **2024–25**.
- Levels: fit MAE 2.03–3.29 pp; holdout 4.01–6.12 pp — but **loses to the linear-trend benchmark (4.35 pp)**;
  all rivals lose to the trend; no PASS.
- Crossing accounting (12 arms): **M0** left-censored (boundary only); **M1** left-censored **≤1977**;
  **M2 clean 0/12** (the single 2025 hit is R29-flagged, in the arm that overshoots M3); **M3** R6 in-window
  12/12 but 2/12 post-window overshoots (2027, 2031); **M4 not discriminable** (simulated tertiary GER ≥50 in
  1960 in all arms incl. no-push — initialisation artefact; excluded).
- **Ceiling residual 14.97 pp UNABLE** (no discriminating observable among foregone income, demand/returns,
  gate structure, enforcement).
- **C8 reporting gap:** the A6 signature's first milestone (primary ≥90, 2017) is observed but was never
  recorded in the committed A1 outputs (per-arm series not persisted) — the asymmetry was tested with its
  first element missing; disclosed, no re-fit.
- Capacity-gated model **EQUIVALENT** to law-only (ties 2/3, better 1/3); capacity-timing unsupported.

### Scaling laws — FAIL, recorded as a bounded negative (R27)
- OOS generated exponents **wrong-signed**: secondary GER~income −1.89 / −0.38 / −0.74 vs required **+0.286**;
  tertiary −1.23 / −0.14 / −0.35 vs **+0.776**.
- Repair cell FAIL: 0/3 contained; fit MAE 6.16–7.43 vs 5 pp; holdout loses to linear trend.
- **Bounded negative:** the cohort-flow model class cannot generate the positive income-scaling sign without
  an **exogenous supply channel**; this locates the required extension, not a claim about the world.

### Push–pull direction — not identifiable (R13)
- Recovery test: pure push and pure pull recoverable (1.00 each), but an outside truth is **forced at 1.00**
  (equivalence 0.07) → direction not identifiable from cross-country/panel moments.
- Panel lead–lag: growth→enrolment null; education→growth only tertiary (p<0.001, correlational);
  completion→growth negative — predictive only, no causal claim.
- Rival comparison: **equivalence set against the observed record EMPTY**; no testable rival reproduces the
  ordering/spacing; human-capital and signalling/MMI **UNTESTED** (sources 403) and never called equivalent.

### State capacity — floor, not ceiling (A9/A10, R28/R29)
- PHL capacity rises into the primary crossing (capacity_within 58.9 2005 → 89.1 2021; PTR 37→27→24 hires;
  spending 2.33→3.96 %GDP) yet upper-secondary stays 75.0 — a **direct counterexample to a pure capacity
  driver**. HKG 1974 (NER≥90) with high capacity + reform; CHN 1986 law → 2016 lower-secondary crossing
  (~30 y lag: enforcement/rural capacity). Cross-country capacity **does not predict crossing timing**
  (Spearman +0.15/+0.10/+0.41/+0.30, all ns, n=5) — country-specific alignment.
- Defect recorded: de jure enforcement proxy inside `G(C)` is collinear with the law marker → `law × G(C)`
  double-counts; needs a new predeclaration to repair.

### Timing — censoring, not dates
- JPN/KOR near-universal **before** the observation window (JPN primary ≤1971; KOR ≤1971/≤2000/2003);
  HKG NER≥90 **1974**, NER≥95 **1979**; CHN/PHL/KHM are the late group. The timing estimand is an
  **inequality** where censored.

### Portability — PARKED-ARMED (D75)
Design notes exist for CHN then HKG (fixed PHL behaviour, no re-fit, diagnostic vocabulary, never “PASS”);
not run because the anchor is PARTIAL/EQUIVALENT (R22).

## 3. Identification limits established

1. **Direction** (push vs pull vs complementary) is not identifiable from cross-country/panel moments —
   forced-ID 1.00; only a two-shock design (E1) could license a direction claim, and its recovery test showed
   size bias 0.55 > 0.50 → **E1 not sufficient**, so no direction claim is made (R13, M2c).
2. **Income-scaling sign** cannot be generated by this cohort-flow class without an exogenous supply channel
   (R27) — a class-level limit, not a tuning failure.
3. **The PHL asymmetry** (floor moves, ceiling does not) is not reproduced by any model on disk; capacity is
   a floor precondition, not a ceiling driver; the ceiling residual is UNABLE given available observables.
4. **Capacity timing** does not beat law-only (EQUIVALENT) and does not predict crossings cross-country.
5. **Data limits:** PSA/ILOSTAT/OECD/DepEd 403s; human-capital and signalling rivals untested; enforcement
   unmeasured; BEPER 2019 DATA BLOCKED; completion timing for HKG/JPN UNABLE (no UIS CR series).

## 4. Re-openers (C1–C4, D76)

- **C1:** correct-sign OOS income-scaling exponents with no exponent supplied as a parameter.
- **C2:** fixed-behaviour crossings within ±5 y on the corrected milestone vector (incl. primary 2017).
- **C3:** a discriminating push/pull/queue/capacity test — needs user-approved PSA / WB Enterprise Surveys data.
- **C4:** observed annual capacity and enforcement series (de facto, not de jure).

## 5. What this means

The programme did not reproduce country/sector massification trajectories in this model class on this
evidence base. It did establish **where and why**: direction is unidentifiable from the available moments;
the model class gets the income-scaling sign wrong; the Philippine asymmetry (floor vs ceiling) is not
reproduced; capacity is a floor precondition whose timing does not discriminate; and the near-universal
systems are censored before the data begin. Those are **identification limits**, documented as publishable
objects (bounded negative on income-scaling; equivalence/identification map + unreproduced asymmetry), with
explicit re-openers.

## 6. Artefacts

- This file; `10_massification/lit/PHASE_WRITEUP_SHELL.md`; `08_council/brief_013/` (A1–A10, R1–R29);
  `08_council/DECISIONS.md` (D1–D78); `08_council/COUNCIL_STATE.md`; `08_council/COUNCIL2_INTAKE.md`;
  `10_massification/STATUS.md` (incl. §3q/§3r incident + recovery); `LEAD_HANDOFF.md`, `NEXT_LEAD_PROMPT.md`,
  `06_report/AGENT_PROTOCOL.md`, `06_report/CONTEXT_ROTATION_PLAN.md`, `06_report/EXTERNAL_CHECKIN.md`.
- Provenance: linear trend 4.35 / persistence 8.60 → `calib/calibration_table.csv` (`552e0cce04bd148d`);
  repair MAE 6.16–7.43 → `calib/repair_table.csv` (`34b0a5bc98e3d603`).
- Delivery incident: iCloud sync race mid-checkpoint; remote restored to `3e3f705`, rebuilt from `/tmp`
  recovery to `787f179`; no history rewritten; iCloud worktree to be re-materialised from the canonical commit.
