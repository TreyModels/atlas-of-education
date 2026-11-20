# FINDINGS — EXP-18 **PART-REPAIR** (v1.7): the consistency repair is made, the bar is missed

**`LABEL: SYNTHETIC` for every generator number; `LABEL: OBSERVED` only for the PHL
`completion_<level>` comparison object. No causal or direction claim is made anywhere. The
parameters are post-observation (the two-tier class was specified after the PHL outcome was
known), so this cell is not an independent test of A5. The closing rule below was
pre-committed and is not renegotiated.**

## 1. The answer, in one paragraph

The licensed repair was made: the **participation decision** now comes from the frozen v1.3
four-state block, called unchanged, with **no new parameter** (110 → 110, 0 introduced).
It works exactly as EXP-16 measured — the repaired arm's participation share equals the frozen
block's own `demand_share` in **45/45** declared cells (0.995644 / 0.953477 / 0.800311 at
2024, against the frozen v1.6 arm's 0.900000 / 0.900000 / 0.820000) — and it does **not** put
the class on the observed path: **A17 scores 0/33 within ±5 pp** (A10: 0/33; the untiered
comparator A00: 9/33), crossings **1/3**. **The bar is missed and the pre-committed closing
rule fires: the generator line closes at representation-only, and no successor generator is
predeclared this phase.** Verdict string: **`PATH-FAILED`**; check table `results/v1_7_checks.csv`.

## 2. What the repair changed, cell by cell

| level | A17 mean deviation | A17 best / worst | A10 (v1.6) at 2024 | A17 at 2024 | moved by |
|---|---:|---|---:|---:|---:|
| primary | **−16.86 pp** | −10.66 / −25.02 | −17.05 | **−10.66** | **+6.39 pp** |
| lower-secondary | **−30.05 pp** | −17.74 / −37.53 | −17.74 | **−17.74** | **0.00 pp** |
| upper-secondary | **−33.11 pp** | −13.38 / −43.24 | −17.62 | **−13.38** | **+4.24 pp** |

- **Primary moved up, and only late.** The demand share rose to the frozen block's own
  0.995644, but the admission rate is pinned at the tier capacity: at the 2018 entry cohort
  `seats/cohort = 0.862887` and `admitted/cohort = 0.862887` — exactly the one-place-per-pupil
  ceiling `K_H + K_O = seats`. The 2024 cell therefore reads **87.64 pp** against the observed
  **98.30 pp**.
- **Lower-secondary did not move at all** (`completion_uis` bit-identical to the frozen v1.6
  arm in **55/56** years, including every observed year). Its admission was already at the
  capacity ceiling in both arms (`admitted/cohort = seats/cohort = 0.783725` at the 2021
  entry cohort). The participation repair is a **no-op** there: the lower deficit is not a
  participation object.
- **Upper-secondary moved up ~4 pp but remains the largest miss.** Its admission is *not*
  capacity-bound: at the 2018 entry cohort `demand/cohort = 0.647593`, `seats/cohort =
  0.802845`, and `admitted/cohort = 0.531026` — the **unfilled Tier-O margin**
  (`unfilled = 0.564282`) is what stands between demand and admission.

## 3. Why the level still does not follow (the object that loses it)

The repair removed the *participation* margin (it is the block's own now) and exposed the
**next** declared object, which this licence does not allow to move:

1. **The one-place-per-pupil tier capacity** (`K_H + K_O = seats`): at primary and lower the
   repaired class admits exactly the adequate-place stock, so the untiered arm's declared
   `phys_cap = 1.15` crowding allowance is not carried by the two-tier declaration.
   `results/capacity_decomposition.csv` (report-only arithmetic on A17's own panel) puts the
   size of that allowance at the primary 2018 entry cohort: **+13.15 pp** of completion
   (→ 100.8 pp, clipped to 100, against 98.30 observed); at the lower 2021 entry cohort
   **+11.20 pp**; at the upper 2021 entry cohort **+14.97 pp**. *(The column prints `nan` where
   the completion year falls outside the 2025 panel window; the readable entries carry the
   message. The table is a decomposition, not an arm: no alternative capacity value was run
   and no alternative count exists.)*
2. **The Tier-O take-up margin at upper-secondary**: the menu's declared quality discount
   (`q_O = 0.55`) leaves 43–66 % of Tier-O places unfilled, so admission sits below demand
   even though seats exceed demand. This is the **structural** part EXP-16 classified as
   `MIXED` at upper — declared here and reported as a sensitivity, **never tuned**.
   `results/upper_structural_sensitivity.csv` gives the menu effect (repaired arm minus
   untiered comparator) at upper: **−10.74 pp (2010) to −20.98 pp (2022)**, −14.99 pp at 2024,
   with upper admission 0.656 against the comparator's 0.800 in 2024.

**The honest one-liner:** the participation margin is no longer the binding object; the level
path is set by the declared tier capacity and the declared Tier-O take-up margin, both
structural, neither licensed to move. The untiered comparator (A00) scores **9/33** because it
carries the 1.15 allowance and no Tier-O margin — that is a statement about which
**declaration** binds, not about the repair's direction, and it is **not** a claim that the
repair "made the model worse" (that phrasing is banned and is not made).

## 4. The structural (upper) sensitivity — declared, reported, not fitted

Upper-secondary is counted in the 33-cell verdict (every observed cell is counted), but no menu
value was moved: `q_O` stays 0.55, `h_share`, the cost multiples, `H_h`, `a_gate` and
`risk_pen` are untouched, and the "re-specify the tier menu" route stays closed (D144(5)).
The sensitivity table shows both arms' upper paths year by year, with the repaired arm's
unfilled share and queue ratio. The upper residual is the **menu**, and the report says so
rather than attributing it to participation.

## 5. Representation carried forward — holds as predeclared, with a loss that must be read

`results/representation_cells.csv` (30 cells = 2010–2024 × lower, upper):

| leg | result | threshold |
|---|---|---|
| (a-i) `unfilled ≥ 0.10` | **15/30** — **15/15 upper, 0/15 lower** | ≥ 15/30 |
| (a-ii) `queue_ratio ≥ 1.10` | **30/30** | ≥ 15/30 |
| (a-iii) same-year coexistence (any cell) | **15/15** | ≥ 8/15 |

The guard **passes at exactly the threshold**, and it passes **through the upper cells alone**.
**The repair destroys the lower Tier-O unfilled margin**: lower `unfilled` is 0 in 14/15 years
and 0.090248 in 2024 (max), so the lower tier object becomes **queue-only**. A **stricter
reading** — coexistence present at *both* lower and upper in the same year — scores **0/15**;
that stricter count is reported in the check table and in
`v1_7_checks_detail.csv`. **No rescue is attempted:** the predeclared leg is the declared leg,
and the loss at lower is exactly what EXP-16's P1/P2 diagnostics warned of. This is the single
most important caveat on any future citation of "representation is preserved".

Companion (non-verdict-bearing, D134(4) corrected contrast): `same_level` (spare upper seats
with rationed applicants) is **0/15 in A00 and 15/15 in A17** — the bimodal switch, not the
participation switch, is what that contrast measures.

## 6. Crossings

**1/3.** Upper-secondary passes trivially (neither series crosses 90 by 2025: model max
62.93 pp). Primary never crosses by 2025 (max **88.66** pp vs the observed crossing in 2017);
lower never crosses (max **80.56** vs 2024). Both misses are consequences of the same two
objects named in §3.

## 7. Guards — all pass (this is a clean negative, not a broken run)

| guard | result |
|---|---|
| S0 construction check | **PASS** — A00 = **9/33**, medians **−4.300824 / −29.435131 / −27.585738** (EXP-7's V1 construction) |
| G1 A00 identity | **PASS** — byte-identical to the frozen v1.3 panel, sha256 `47d4b082…` |
| G2 counterfactual identity | **PASS** — A17's upper admission through A00's accounting reproduces the **11 replay-determined** upper pipeline columns **0 differing / 18 480 cells**; the 5 columns the frozen hook cannot determine (`admitted_overage, enrolment, ger, teachers, ptr`) are **reported** with their counts and the mechanism (239/239/239/857/890 of 1 680), never asserted |
| G3 schooling-supply identity | **PASS** — **0 differing / 53 760 cells** (8 supply columns × 30 countries × 56 years × 4 levels) |
| G4 projection order + ledger | **PASS** — 0 forbidden same-year economy reads; 102 ledger rows with mechanism and sign; W1/W2/W3 declared |
| G5 determinism | **PASS** — two complete runs, **18/18** result files byte-identical |
| G6 predeclaration integrity | **PASS** — embedded sha256 `3778afe3…`; 35 declared scalars checked; freeze record matches |
| G7 no-fit audit | **PASS** — 0 of 26 audited objects chosen by reference; band hits **0** |
| G8 count-blind | **PASS** — predecl frozen before any observed open; **2** allowed opens (phase A demographic input: 2 indicators retained, 2 398 rows skipped on arrival; phase C scoring: 33 cells after every arm); **1** blocked attempt (phase-ARMS positive control: `BLOCKED-AS-REQUIRED`); 0 outcome values before SCORE |
| G9 repair in force | **PASS** — 45/45 cells: A17's participation share equals the frozen block's own |

## 8. The closing rule (pre-committed) — what happens now

The bar is **≥ 17/33 and 3/3 crossings** (EXP-7's, unchanged; D147(i) reads the narrower
label). **It is missed: 0/33, 1/3.** Per D144(6) and the Council block §5.3.5, **the generator
line closes at representation-only**:

- **No successor generator is predeclared this phase**, and no v1.8 is built.
- The model line becomes **descriptive**: the class is published as a **representation result**
  (coexistence at upper, queue at both tiers), κ as a **within-window description** (D138), v1.2
  as a **placement instrument**.
- The next work is measurement, not specification: **EXP-19 PLACES-BOUND** (is the required
  coverage bounded by anything on disk?) and **EXP-20 USE-REG** (what κ may be used for, and
  what re-opens HKG).
- **EXP-17's λ\* = 1.11465019198434 stays `REQUIRED-STATE (EXP-17)` with the `DERIVED` target
  0.8076 attached. No λ is adopted.** EXP-17's scope flag is carried: λ\* was solved on the
  v1.2 panel, where the 2018 gate is capacity-limited, and it does **not** transfer to the
  repaired class's gate.

## 9. What this cannot claim

1. **Nothing about the Philippines.** Every generator number is SYNTHETIC; the PHL series is
   OBSERVED and enters only as the comparison object. `SYN00_PHL_LIKE` is a synthetic anchor.
2. **No causal and no direction claim.** "The participation margin causes…", "capacity
   explains the timing", "the repair made the model worse" are all barred, and none is made.
3. **Not an independent test of A5** (the class and its values are post-observation), **not**
   evidence for or against any demand theory, and **"demand falsified"** is not said in any
   paraphrase.
4. **No fitting.** No parameter was chosen by reference to the bar, the `[73,77]`/`[55,85]`
   bands, or any observed cell; no grid was searched; the 26-object no-fit audit is 0 and the
   band scan is 0. The one interpretive choice (tier capacity = seats, not `1.15·seats`) was
   fixed **before the run** by the licence ("the consistency part only") and its arithmetic is
   reported as a decomposition, not as an arm.
5. **No re-score, no re-tune, no re-freeze.** v1.6's `PATH-FAILED` stands; EXP-14's checks are
   not re-scored; A10 is not re-run "as a verdict" (it appears only as a provenance column in
   `observed_path_A17.csv`, labelled as the frozen v1.6 arm).
6. **Parks stay parked**: A3 demand line **KILLED** (D130); exit-cost/induction **PARKED**;
   HKG **`DEFER-HKG`** (D133); C1–C4 **closed**; κ **WINDOW-ONLY**; **D63 `UNABLE as to
   cause`**; the phase verdict (D76/D77) untouched.
7. **The closing rule is pre-committed** and nothing in this file reopens it. A future Council
   that wants another generator re-specification must authorise it as a **new** decision; it
   cannot be read out of this cell.
8. **HELD data stay HELD**, named and unused (the full D135 list is in the predeclaration
   §10); no proxy was substituted.

## 10. Files

`results/v1_7_checks.csv` (check table), `results/v1_7_checks_detail.csv`,
`results/observed_path_A17.csv` (the 33 cells with the A00 comparator),
`results/crossing_check.csv`, `results/representation_cells.csv`, `results/panel_A17.csv`,
`results/panel_A00_v13cols.csv`, `results/panel_A17CF_identity.csv`,
`results/counterfactual_identity.csv`, `results/schooling_identity.csv`,
`results/repair_in_force.csv`, `results/propagation_ledger.csv`,
`results/capacity_decomposition.csv`, `results/upper_structural_sensitivity.csv`,
`results/no_fit_audit.csv`, `results/count_blind_audit.json`, `results/guard_report.json`,
`results/determinism_run2/`, `RUN_MANIFEST.json`, `SHA256SUMS.txt`.
