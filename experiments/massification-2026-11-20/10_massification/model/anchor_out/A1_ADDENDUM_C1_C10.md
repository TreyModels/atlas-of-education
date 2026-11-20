# A1 ADDENDUM — Council-2 items C1–C10 (no re-fit, no threshold change; verdict capped at PARTIAL)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** addendum to the committed A1 descriptive report (branch
`dbec38e`, `anchor_out/`). **Rules honoured:** no re-fit, no threshold change, no tuning, no direction claim; the
scaling criterion stays a printed FAIL; the A1 verdict **cannot improve beyond PARTIAL/DESCRIPTIVE** (D56/D57).
Items implemented here are those that can be produced **from existing outputs/data without re-fitting**; anything
that would require a new fit is explicitly not done.

## C8 — the A6 signature's missing first milestone: primary completion ≥90 in 2017
The official M0–M4 vector omits the A6 signature's first evident milestone because M1 is defined as **NER ≥95 / GER
≥100** (left-censored by construction), not primary **completion** ≥90. Observed (on-disk `UNIVERSALIZATION_SERIES.csv`,
status observed): primary completion **83.16 (1999) → 87.45 (2013) → 91.92 (2017)** → 95.40 (2021) → 98.30 (2024);
**first ≥90 = 2017**. This is the milestone that makes the PHL asymmetry legible: primary crossed ≥90 in 2017, while
upper-secondary stood at 75.03 in 2024 and never reached 90.
**Model side:** the A1 anchor table recorded M0 (completion_lower ≥50), M1 (GER primary ≥100), M2, M3, M4 — it did
**not** record a primary-completion ≥90 crossing, and the per-arm fitted series were not persisted.
**Disclosure:** the model-side counterpart of this milestone is therefore **not available from the committed outputs**;
no re-fit was performed to add it (Council-2 rule). This is recorded as a **reporting gap of A1**, not as evidence for
or against the capacity claim.

## C9 — M4 classification: NOT DISCRIMINABLE (not a timing miss)
Simulated tertiary GER is **already ≥50 in 1960 in all 12 arms, including the no-push arm**, whereas the observed
tertiary GER was **16.34 in 1971** and first crossed ≥50 only in the **2024–25 band**. The model's M4 crossing (1960)
therefore reflects an **unrealistic initial tertiary level**, not a timing failure of any mechanism: with a start value
above the threshold, the crossing year is not informative. **Classification: M4 NOT DISCRIMINABLE** — excluded from
the timing verdict (cannot be counted as PASS or FAIL), and reported as a model-initialisation defect to fix before any
future M4 timing claim.

## C10 — capacity construction disclosures and a double-count defect
1. **Constant back-fill before the first observed year.** The capacity index `C_t` interpolates flat before the first
   observed input (no data before it): the delivery component uses the PHL high-school PTR series (first observed 2000)
   and the fiscal component the WDI education-spending series (first observed 1995), so **pre-1995/2000 values are
   constant back-fills** of the earliest observation, not measurements. Any crossing before those dates (M0 1960,
   M1 1966/1977, M4 1960) is therefore evaluated against a **flat extrapolated capacity**, which is one more reason
   M0/M1/M4 carry no point-timing credit.
2. **De jure enforcement component.** The enforcement proxy is a **de jure compulsory-duration mapping**
   (compulsory years / 13; 6 years pre-1987, 10 after 1987, 13 after 2013) declared from `POLICY_TIMELINE.csv` — it is
   not measured enforcement (attendance/truancy/penalties are **DATA BLOCKED**).
3. **Double-count defect (recorded).** The enforcement proxy sits **inside** `G(C)` (weight 0.2) while also being a
   deterministic step function of the same law dates used by the **law marker**; `law × G(C)` therefore counts
   compulsory-length changes **twice** (once in the marker, once in the gate). This inflates the capacity-gated push
   exactly when a law marker turns on, and it is a specification defect. It is **not repaired here** (no re-fit
   allowed); any capacity-timing claim must treat the gate as contaminated until the enforcement proxy is either
   measured independently or removed (a new predeclaration + Council intake).

## Corrected crossing accounting (Council-2 rule; 12 arms = 3 rivals × 4 arms)
| milestone | observed | model arms | corrected accounting |
|---|---|---|---|
| M0 | left-censored (≥50 before 1999) | 1960–1980 | boundary constraint only (no point-timing credit); constant capacity back-fill |
| M1 | left-censored at ≤1977 (GER ≥100 in 1977; NER ≥95 in 1976) | 1966 | boundary constraint only |
| **M2** (lower-sec completion ≥90) | **2024** | 2025 (education_led/gated), 2028 (demand_led/capacity_only), 2038 (complementary/none) | **clean in-tolerance hits 0/12**: 2025 and 2028 are inside ±5 y but occur in arms that also post-window-cross M3 (2027/2031) → **R29-flagged**; 2038 is outside ±5 y |
| **M3** (upper-sec completion ≥90) | **never by 2024 (75.03)** | none ≤2024; 2027, 2031 post-window | **R6 in-window 12/12 pass** (no arm crosses by 2024); **2/12 post-window overshoots** (2027 education_led/gated; 2031 demand_led/capacity_only) → R29 ceiling-threshold flag |
| **M4** (tertiary GER ≥50) | 2024–25 band | 1960 all arms | **not discriminable** (initial value already ≥50) — C9 |

**Standing statements (unchanged):** scaling criterion **FAIL** (unrepaired OOS exponents secondary −1.89/−0.38/−0.74,
tertiary −1.23/−0.14/−0.35; repair cell FAIL 0/3 contained); capacity_gated does **not** beat law_only (same crossings;
holdout 1.85 vs 2.03 demand_led, 1.97 vs 2.17 complementary) → capacity-timing **not supported, EQUIVALENT**; A2d
cross-correlation −0.427 at lag 6 (no positive lead); ceiling residual 14.97 pp (upper-secondary 75.03 vs 90) with
candidate accounts **UNABLE** (no discriminating observable). **Verdict: PARTIAL/DESCRIPTIVE at most; no PASS; no
direction claim.** No re-fit, no threshold change, no git writes.
