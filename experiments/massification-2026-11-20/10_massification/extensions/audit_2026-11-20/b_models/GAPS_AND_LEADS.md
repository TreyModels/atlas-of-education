# GAPS AND LEADS — what the old models can and cannot carry forward

**Audit:** evidence auditor, 2026-11-20. Companion to `MODEL_INVENTORY.md` / `MODEL_INVENTORY.csv` in this
directory. Every number below is sourced to a file listed in the inventory; defect ids (D-01…) are defined there.
**No model was run or re-fitted for this note.**

**How to read the confidence tags.** `[ROBUST]` = the conclusion survives every defect found, including the ones
that invalidate a number. `[FRAGILE]` = the conclusion is real but the quoted magnitude/target is defective and must
be re-derived before use. `[ARTEFACT]` = the result is produced by a coding or measurement error and cannot be used
as evidence in any direction.

---

## (a) What the model class provably cannot do — on this record, at these specifications

These are the limits the Council can rely on. They are stated at the strength the artefacts support, with the rule
that governs each.

### a.1 Generate the observed positive income-scaling sign out of sample — `[ROBUST]`
Committed generated OOS exponents (three rivals) are **negative** where the record's classified laws are positive:

| law | required | generated (demand / education / complementary) | source |
|---|---|---|---|
| secondary GER ~ income | **+0.286** (0.045) | **−1.893 / −0.379 / −0.743** | `model/calib/scaling_check.csv`; `STATUS.md` L85–91 |
| tertiary GER ~ income | **+0.776** (0.086) | **−1.229 / −0.137 / −0.353** | same |
| after the predeclared repair | same | **−2.734 / −2.527 / −1.034**; **−0.319 / −1.317 / −0.391**; signs_ok 1/3, contained 0/3 | `model/calib/repair_scaling.csv` |

The *sign* test is transform-consistent and survives D-11 (orphan artefact), D-12 (logit-vs-log range) and D-13
(self-contradictory target range). The structural cause is stated in the repair predeclaration and confirmed by the
code: enrolment is a bounded cohort stock while the income index is unbounded exponential, so the ratio's log–log
slope is forced negative (`model/PRE_SCALING_REPAIR.md`; `model/pushpull.py` L115–119). Adding an income-facing
intake/continuation margin (six parameters) did not restore the sign.
**Governing rules:** R4 (supplied law — the exponents may not enter as schedules), R14 (scaling reproduction caps the
claim at PARTIAL), R17 (repair must be structural), R27 (repair budget exhausted).
**Honest bound:** this is a result about *this class/implementation* (cohort-flow stock, no exogenous supply
channel), not about the world and not about every possible cohort model — the closeout says the same and the audit
agrees.

### a.2 Beat a naive linear trend on any completion holdout it was scored on — `[ROBUST]`
| cell | holdout MAE (3 rivals) | linear-trend benchmark | verdict |
|---|---|---|---|
| PHL smoke | 4.84 / 5.40 / 6.08 | **4.35** | loses (`calib_phl.log`) |
| PHL pooled | 7.23 / 4.38 / 5.38 | 4.35 | loses (`calibration_table.csv`) |
| CHN pooled | 8.70 / 7.38 / 7.82 | **2.64** | loses badly |
| KHM held-out | 28.24 / 32.23 / 31.26 | 6.89 (persistence) / 8.91 (trend) | loses by ~4× |
| repair cell | 5.44 / 6.26 / 4.80 | 4.35 | loses |
| anchor 12 arms | 4.01–6.12 (2014–2024) | **no matched benchmark computed** | one arm (4.01) is below 4.35 but on a different window (D-08) — not comparable |

Rule R1 and R18 make "loses to linear trend" PARTIAL-at-best, and the pattern is consistent across every cell where
the benchmark was actually computed. This is the single most decision-relevant failure: it means the model has not
demonstrated information beyond a straight line on the outcome it claims to explain.

### a.3 Identify push vs pull vs complementary — `[ROBUST]` as a statement about the design
- Recovery on its own simulated data: demand 1.00, supply 1.00, **complementary 0.00**, **forced-ID 1.00**,
  equivalence 0.07 → NOT IDENTIFIABLE (`model2/runs/recovery.csv`, `model2_meta.json`).
- The estimator that could license a direction claim (E1 two-shock) fails its own predeclared recovery:
  **median |bias| 0.5546 > 0.50**, sign accuracy 0.93/0.92 at σ=0.5, 0.74/0.68 at σ=1.0 (`model2/runs/m2c_meta.json`).
- Panel lead–lag is not identifiable (2 usable countries; `model2/runs/lead_lag.csv`).
**Rules:** R13 (no direction claim from panel moments), R3 (equivalence), R16 (E1 may not be fielded).
**Consequence the Council must hold onto:** "the rivals are EQUIVALENT" is *not* evidence for any channel. A5b's
empty equivalence set and M2's forced-ID make the same point from two directions: the available moments do not
separate the mechanisms.

### a.4 Reproduce the PHL ceiling asymmetry — `[ROBUST]` as a failure, `[FRAGILE]` in its accounting
Observed: primary ≥90 in 2017, lower-secondary ≥90 in 2024, tertiary GER ≥50 in 2024–25, **upper-secondary never ≥90
(75.03 in 2024)** (`10_massification/data/UNIVERSALIZATION_SERIES.csv`, spot-checked). The model side:
- **M2 clean in-tolerance hits 0/12**; 2025 and 2028 occur only in arms that post-window cross M3 (2027, 2031)
  (`anchor_out/A1_ADDENDUM_C1_C10.md` table; `anchor_out/anchor_table.csv`).
- **No rival reproduces the ordering/spacing**: equivalence-to-observed set EMPTY (`model2/runs/a5b_final_scoring.txt`).
  Caveat that must travel with it: world-society's primary crossing (2014) *is* within ±5 y of 2017, so the
  emptiness rests on ordering/spacing and the upper-secondary non-crossing (`10_massification/lit/PHASE_WRITEUP_SHELL.md`
  §(b).5).
- **Timing**: E6 fails its own predeclared rule (logistic 2/6 PASS; needs ≥2/3 of scored milestones) (`runs/e6_meta.json`).
**Rules:** R6 (false positive), R23 (asymmetry is the anchor criterion), R29 (capacity buys the floor, not the
ceiling), R19 (timing miss is structural).
**Fragile part:** the milestone *vector* itself was tested with its first element (primary ≥90, 2017) missing on the
model side (C8), and the M1/M4 milestones are GER-based on a mis-scaled series (D-02). A new attempt must not inherit
that.

### a.5 Port a fixed behavioural core — `[FRAGILE]` (the only completed port-like test fails)
KHM, never fitted, same θ as the pooled PHL+CHN fit: **28.24 / 32.23 / 31.26 pp** MAE on 2011–2024 against an 8 pp
tolerance and a 6.89/8.91 naive benchmark (`calib/calibration_table.csv`). This is closer to a portability test than
anything in the portability cell (which was never run) and it fails by ~4×. Rule R1; the A6/A7 design would apply
R20.

### a.6 Represent enrolment rates at all — `[ARTEFACT]`
`ger_lower` 332.8–1477.0 %, `ger_upper` 837.3–3514.4 %, `ger_tertiary` 583.4–3247.9 % across **all 1458** smoke rows
(`model/smoke/structure_smoke.csv`), while `accounting_checks.csv` reports **0 failures** because the check never
bounds GER (D-02, D-16). Every GER-based output of this implementation is unusable: M1 (primary GER ≥100), M4
(tertiary GER ≥50, hence 1960 in all arms), and any GER level comparison. The cycle-length factor is constant over
time, so it shifts levels and thresholds but **not** the log–log slopes — which is why a.1 is unaffected.
**Rule:** R2 (zero-tolerance conservation/validity) — the check was supposed to catch this and did not.

### a.7 Implement the K-12 mechanism it claims — `[ARTEFACT]`
`PRE_ANCHOR_A1.md` M1 declares "cycle-length switch + cohort exposure" and A7 retains "the cohort mechanics of the
cycle extension" as the one live state-push mechanism. `configs.CYCLE['PHL']` is a single constant dict
(primary 6, lower 4, upper 2); `pushpull.run` reads `cyc['upper']` with no year dimension. There is **no cycle
switch in the code**. The anchor's K-12 content is therefore a marker (`marks[t]` from 2013) and nothing else
(D-21). This removes one of the two mechanisms A7 said remained live.

**Bottom line for (a):** the class, as coded, cannot (i) generate the scaling sign, (ii) beat a trend, (iii)
identify direction, (iv) reproduce the asymmetry, or (v) port to KHM; and two of its outputs (GER, K-12 cycle) are
not implemented as described. None of this proves the world is otherwise — it proves this instrument is finished
without a re-specification.

---

## (b) What is salvageable **without re-fitting**

These are assets that can be used by a new design as *inputs, constraints or comparison objects*. Using them is not
a re-fit; presenting them as new evidence would be.

1. **Observed data cells with provenance** — the completion/GER/transition series in
   `10_massification/data/UNIVERSALIZATION_SERIES.csv` (spot-checked: PHL 1999/2017/2024 primary 83.16/91.918/98.305,
   lower 58.86/81.255/92.414, upper 59.70/76.433/75.025, all `status=observed`), `04_data/TARGETS_FLOW.csv`,
   `ECONOMY_SERIES.csv`, `JOBS_AND_MARKETS_PANEL.csv`, `SCHOOL_EXPANSION.csv` (PTR 37→27→24 observed/high).
   These carry the programme's real information.
2. **The declared exogenous inputs** — TFR and urbanisation paths with S/A labels (`model/configs.py`), cycle
   lengths, policy dates, and the capacity series C_t committed in `anchor_out/run_meta.json`
   (C(1960)=0.2337, C(1970)=0.2952, C(2017)=0.7964, C(2024)=0.7925). Reusable as declared inputs to any new model,
   provided the enforcement component is removed or independently measured (D-09).
3. **The behavioural core's accounting skeleton** — the single-year cohort/ageing engine
   (`pushpull.py` L67–77) is conservative and survives B1/B2; the *population* part is reusable. The schooling stock
   algebra is not (D-02).
4. **The rival-switch architecture** — three rivals from one code path with the same exogenous paths
   (`pushpull.run` `e_s=0` / `e_d=0` / both). The *design* is sound and reusable; the current implementations are
   not the point.
5. **The no-target-as-parameter invariant** — B4 plus `configs.py`'s S/E/A/F labelling is a genuine discipline worth
   carrying forward; it is the reason the audit could establish what is and is not fitted.
6. **Persisted θ for the two calibration cells** — `calib/calibration_table.csv` (`theta_json`, 9 rows) and
   `calib/repair_table.csv` (3 rows, 20 parameters). These are the only old-model parameter sets on disk and they
   can be **evaluated** on new moments without re-estimation (see c.2). This is the one path that turns the old model
   into a test rather than an artefact.
7. **The predeclared designs that were never run** — A6/A7 portability (`PRE_PORTABILITY_A6_A7.md`), the E2 cohort
   design with its honest MDE (`PRE_EXP_E2_PH_K12.md`), E3 (`PRE_EXP_E3_PH_NURSES.md`), the M2c-2 conforming recovery
   predeclaration (`M2C2_PREREG.md`). They are gate-compliant, written before data contact, and still executable.
8. **The negative results as publishable objects** — sign failure, non-identifiability, E6 timing miss, empty
   equivalence set, KHM port failure, and the capacity non-credit. They are the phase's actual output and they are
   reusable as the *premise* of the next design, not as results to defend.

**Not salvageable:** the anchor's 12-arm crossing table (θ and per-arm series lost, D-03), `m2b_scaling.csv` (D-04),
`scaling_check.csv` as a pipeline (D-11), the GER series (D-02), the "0 accounting failures" claim (D-16), and the
capacity-timing claim through the current gate (D-09).

---

## (c) Five concrete "different direction" candidates

Each line: **what would be done — and the test that would make it a real test rather than a re-parameterisation.**

1. **Re-specify the stock–flow class before anything else (the class, not the parameters).**
   Build enrolment as a *single-cohort* stock identity (one entering cohort × progression × level duration, no
   accumulated cycle multiplier), bound-check every rate including GER ≤ 100 (+ over-age allowance), and implement
   the declared K-12 cycle switch as an actual time-varying `cyc` — the two things D-02 and D-21 show are missing.
   **Real test:** the model must reproduce observed GER *levels* (e.g. PHL tertiary 16.34 in 1971 → 52.99 in 2026)
   and the M1/M4 crossing years with **no target as a parameter and no per-country scale factor**; if a free scale
   factor is needed to land the level, it is re-parameterisation and the claim is void.
   **Rule:** R2 (conservation/validity) + R12 (new cell, no retro-fit). Do not re-label the old cells.

2. **Test the declared behavioural core on a genuinely new moment (frozen θ, one shot).**
   Take the persisted θ from `calib/calibration_table.csv` and score it, unchanged, on a moment never used in any
   fit: the KHM transition/dropout/out-of-school series, or the PIDS regional mean-years/Gini gradient (NCR vs ARMM,
   predeclared direction and ordering, check-only per A7b §3).
   **Real test:** θ frozen, sign/magnitude predeclared, one evaluation, failure reported as failure. It becomes a
   re-parameterisation the moment θ is re-estimated or the moment is chosen after seeing the fit.
   **Rule:** R5 (a new discriminating moment is the *only* admissible improvement) + R20 (fixed behaviour).

3. **Corrected portability diagnostic (CHN then HKG) with the enforcement proxy removed.**
   Freeze behaviour and parameters, re-set only declared country inputs (TFR/URB/cycle/policy dates/capacity built
   without the de jure enforcement step), report crossing *intervals* under censoring, and state what transfers and
   what does not.
   **Real test:** if any behavioural parameter has to move to match CHN/HKG, portability = FAIL (R20); fixed-behaviour
   reproduction within the A4 timing bands = a real timing result. **Must not run before (1)** — porting a broken
   stock identity measures the breakage, not portability. **Rule:** R20/R22/R28.

4. **A rival field that can actually win — benchmarks as rivals, not straw men.**
   Put the linear-trend and persistence benchmarks, and a cohort/fertility-only rival (the OUTSIDE truth that
   forced-ID absorbed), into the *same* comparison table as the mechanistic rivals on the milestone vector.
   **Real test:** predeclare that **beating both benchmarks is necessary** for any claim; report the equivalence set
   including the benchmarks. If a straight line wins, the mechanistic rival field is not evidence and the honest
   output is the identification-limits map.
   **Rule:** R3 (equivalence), R11 (fair rival matching — a structurally barred rival voids the comparison),
   R13 (no direction claim).

5. **An identification design that passes its own power test before it touches data.**
   Run the conforming **M2c-2** recovery predeclaration (4 truths, 60×20 panel, recovery ≥0.80, forced-ID = 0.00,
   complementarity detection ≥0.80) and field E1 **only if** it passes; the alternative is to stop at the equivalence
   map and publish it. If E3's PRC/CHED series can be obtained, the predeclared E2+E3 pair is the only other legal
   route to a direction claim.
   **Real test:** the recovery thresholds must be met on the *actual* design (not a smaller proxy), predeclared before
   the field run; any post-hoc size threshold is a re-parameterisation.
   **Rule:** R16 (interaction-estimator sufficiency), R13, R4.

**One sentence for the Council:** the evidence supports *re-building the stock–flow instrument and re-testing the
declared core on new moments*; it does not support another attempt to fit the same completion series harder.

---

## (d) Candidates that would violate a rule and must NOT be run

| would-be direction | why it is barred | rule |
|---|---|---|
| Re-run the repair cell, or tune η_in / m_k / κ / PUSH / capacity weights to close the ceiling or fix the sign | the one-cell budget is spent; "improvement" on the same moments is re-parameterisation, not identification | **R27**, **R5**, **R12**, **R17** |
| Fit the OOS income-scaling exponents, or enter them (or any logistic schedule/ceiling/crossing year) as an input | supplied law — the model must generate the relation | **R4**, **R14** |
| Add parameters/channels and report the better fit of the same completion moments | no new discriminating moment | **R5** |
| Move the fit/holdout split, fold KHM or 2014–2024 back into fitting, or relabel an OOS miss as calibration | no retro-fits; the split is predeclared | **R12** |
| Claim capacity timing from the current gate (enforcement proxy inside G(C), double-counting the law dates) | the gate is contaminated; capacity-timing must beat law-only cleanly | **R28**, **R29**, **R24** |
| Make any push/pull/complementarity direction claim from the panel or rival comparison | forced-ID 1.00; E1 not sufficient | **R13**, **R16** |
| Call the human-capital or signalling/MMI rivals "equivalent" — or "tested" | they are untested (PSA / Enterprise Surveys blocked) | **R11**, D48, write-up §0.3 |
| Re-present M4 (tertiary GER ≥50, 1960 in all arms) as a timing PASS or FAIL | not discriminable — initialisation artefact | C9; **R19** |
| Present any GER level or GER-based milestone from this implementation as evidence | the series is 3–35× out of range and the accounting check never bounded it | **R2**, **R7** |
| Field E1 without a passing conforming recovery test | predeclared sufficiency failed (bias 0.55 > 0.50) | **R16** |
| Re-run the old anchor and re-quote the 12-arm table as a new result | θ and per-arm series were never persisted; re-running is a new fit, not a reproduction | **R12**, **R5** |

---

## (e) Priority if the Council asks for one thing

**Do (1) first and only (1).** Every other candidate is either blocked on data (3, 5-partly), already negative (4),
or only meaningful once the instrument stops producing 1500 % enrolment rates and a cycle switch that does not
exist. The old model's most useful output is the precise list of what it cannot do; the next model should be built so
that list is shorter, not re-fitted until it looks better.
