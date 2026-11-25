# DHS E1–E8 → model-prediction evidence map (bonus, 2026-11-25)

**Owner:** `contest-math` (re-tasked by Lead). **Status:** mapping only — no new estimation. Evidence base: the
executed eight DHS descriptive experiments (`wt5/dhs8`, branch `research/dhs-eight-experiments-2026-11-25`,
commit `30c90c7`; 92/92 feasible cells, 241 design-based estimates, 3 suppressed, 90 contrasts; QA-signed engine
`46c49065…`; all descriptive, non-causal).

**Question:** for the Model Zoo (`docs/audit/MODEL_ZOO_SCOPE.md` models #1–#10) and the Paper C regimes
(R1 own-teacher withholding / R2 private market / R3 state supply), which predictions can these eight experiments
actually test, which can they only constrain weakly, and which are untestable with DHS?

**Headline:** the DHS experiments contain **no tutoring, learning, gate/seat, time-use, earnings or expenditure
variables**. They are household demographic/attendance composition facts. They can constrain **household
demand-side distributional implications** (who attends, by wealth/residence/sex/cohort) and **falsify proxy
assumptions** (e.g. household size as kin support); they **cannot** test any tutoring-specific prediction
(participation response, supply form, withholding, provider mix) and cannot identify the Paper C regimes.

## 1. Mapping table (E1–E8 → prediction families)

Prediction families: **HC** = Becker human capital (#1); **POS** = Hirsch positional competition (#5);
**BRAY** = shadow-education demand (#6); **BIS** = Biswal/Jayachandran withholding (#7); **SPENCE** = signalling
(#3); **HAN** = Hanushek production (#4); **KR/CN** = state-supply/test-prep supply (#8/#9); **HH-TIME** (#10).

| exp | what it measures (executed, descriptive) | model predictions it can **test/constrain** | verdict |
|---|---|---|---|
| **E1** attendance 14–17 by wealth quintile | weighted attendance by quintile, 11 country-waves (KH 2005–2021-22, ID 2002-03–2017, PH 2017/2022, VN 2005ais); Q5−Q1 positive everywhere (+0.114 PH 2022 → +0.453 ID 2002-03) | **HC**: investment/participation rises with household resources — the *sign and monotonicity* of the wealth gradient is a demand-capacity implication (not a tutoring test). **BRAY**: only the "participation rises with household capacity" corollary, and only for *schooling* participation, not tutoring. **POS**: a uniformly positive gradient does **not** discriminate positional from human-capital demand (both predict it) | **Weak constraint only.** Cannot test tutoring; cannot discriminate HC vs POS |
| **E2** attendance by residence | urban−rural gap, 19 waves; positive everywhere (+0.015 PH 2017 → +0.263 ID 1994) | **HAN/HC**: urban-rural capacity/school-supply differences predict a positive gap; but no school-input measure is linked, so it is a composition fact. **POS**: gate access differences by residence would also predict a gap | **Indeterminate between models.** Useful as a *stylised fact* to match; not discriminating |
| **E3** attendance by sex | male−female gap, 19 waves; **Cambodia reverses** +0.235 (2000) → −0.055 (2021-22); PH female advantage throughout | **HC**: gendered returns/capacity predict either sign depending on context; **POS/SPENCE**: gate pressure can favour the sex with higher marginal return. The *reversal* is a within-country change that a mechanism should be able to reproduce qualitatively, but DHS has no gate/return data to test which mechanism | **Stylised fact for model comparison; not a discriminating test** |
| **E4** children ever born, women 40–49, by schooling | completed fertility by schooling; KH gap −3.24 (2005) → −0.81 (2021-22); PH 2022 −2.43; KH 2000 "12+" suppressed (n=25) | **HC/Becker quantity–quality**: negative education–fertility association is consistent, but selection, survival and survey eligibility are unaddressed; **cannot** separate HC from positional/credential channels | **Consistent-with, not a test.** Do not use as evidence for a schooling effect |
| **E5** birth before 20 by schooling, women 25–34 | negative gap (−0.18 KH 2005 to −0.41 PH 2022); schooling may postdate birth | **HC**: human-capital timing implication (education delays fertility) — but temporal order is not established; **POS/marriage-market** models also predict it | **Not discriminating; timing unidentified** |
| **E6** current school participation, women 20–24, by residence (person-record, D-01 deviation) | urban−rural participation gap; positive in most waves (+0.10–0.16 ID/VN), small in PH, PH 2022 negative (−0.030) | **HC**: continued participation by residence (capacity/access); **HAN** (supply) would predict it if urban schools are better, but no school data linked | **Weak constraint** |
| **E7** union before 20 by schooling, women 25–34 | negative gap, stable: KH −0.39 (2000) → −0.39 (2021-22); PH 2022 −0.55 | **HC**: education delays union (quantity/quality and marriage-market implications); **the non-narrowing over two decades** is a useful stylised fact against a simple "education expansion ends early union" story | **Stylised fact; no mechanism identification** |
| **E8** current household size, women 40–49, by schooling | KH null (BH q ≥ 0.39); PH 2022 −0.97 | **Falsifies a proxy assumption**, not a model: household size is **not** kin support and should not be used as a kin-support/withholding proxy in the Model Zoo. It also weakly constrains household-composition predictions | **Negative result — proxy falsification** |

## 2. What the DHS evidence **cannot** test (explicit "theory-only" list for the Zoo)

1. **Any tutoring prediction** — no participation, hours, expenditure, provider type (own teacher vs firm vs
   online), or tutoring prices: models #6 (Bray demand), #7 (withholding), #8 (test-prep supply), #9 (China state
   supply) and the Paper C supply-form question are **untestable with DHS**.
2. **Positional vs human-capital discrimination (#5 vs #1)** — requires gate/seat/elite-share and learning
   outcomes linked to households; DHS has neither.
3. **Signalling (#3)** — requires credentials vs skills/earnings; DHS has no earnings or learning measures.
4. **Hanushek production (#4)** — requires school inputs (PTR, teacher pay, materials) linked to achievement;
   DHS has no school and no learning data.
5. **Household time allocation (#10)** — no time-use module.
6. **Policy-change tests (China Double Reduction, HK/KR caps)** — no policy variation or tutoring variables in DHS.
7. **Mincer returns (#2)** — no earnings.

## 2b. Binding limitation for Paper C (carried from the data inventory)

**HK-vs-PH supply-form (own-teacher vs firm) is unobserved in both settings**, so the **emergence/supply-form
prediction cannot be tested with the current portfolio**; Paper C's empirical leg is **feasible-partial
(participation/hours only)** until codebooks/access are verified (`TUTORING_CODEBOOK_VERIFICATION.md`). The
theory-only list (withholding, positive school-supply `S`, learning decomposition `G=max(0,L−S)`, supply-form
equilibrium, informal prices/teacher hours/firm capacity) remains intact. The DHS experiments therefore cannot
fill this gap either: they contain no tutoring variables at all.

## 3. How the Zoo should use these eight experiments

* Use E1–E8 as **auxiliary distributional targets** only (wealth gradient sign, urban-rural gap, sex-gap reversal,
  education-fertility and education-union gradients, household-size null), labelled `DHS-descriptive` and kept in a
  separate evidence layer from simulation and from tutoring-data estimates (Zoo protocol §4).
* A model that **cannot reproduce** the *sign* of E1's gradient or the E3 reversal is **inconsistent** with these
  descriptive patterns; that is a *weak* consistency check, not a discriminating test, because many mechanisms can
  produce both.
* Do **not** report E4–E7 as effects of schooling; they are cross-sectional associations with selection and
  (for E5/E7) temporal ambiguity. Do **not** use E8 as a kin-support measure — PH 2022's −0.97 and KH's null show
  household size behaves independently of the construct.
* Where the Zoo needs tutoring/supply-form evidence, point to `TUTORING_DATA_INVENTORY.md`: PISA 2018/2022 for
  participation/hours (HK/PH/CN; ESCS quintiles), SEA-PLM 2019 for KH/PH (codebook check), CFPS/CIEFR for China
  expenditure and Double Reduction timing, KOSTAT for Korean provider-type/expenditure aggregates — and keep
  withholding/S/learning decomposition theory-only.

## 4. Provenance

* Execution: `wt5/dhs8` branch `research/dhs-eight-experiments-2026-11-25` @ `30c90c7`
  (`MILESTONE2_2026-11-25.md`, `runs/2026-11-25_final/estimates_final.csv` sha `83fc62f0…`, QA engine
  `qa/experiments_v2.R` sha `46c49065…`; QA sign-off `qa/QA_SIGNOFF.json`).
* Prediction families: `docs/audit/MODEL_ZOO_SCOPE.md` §1; Paper C regimes and represented/absent mechanisms:
  `docs/audit/PAPER_C_MODEL_GAP.md`.
* This file introduces **no new numbers**; all estimates quoted are from the committed milestone-2 table.
