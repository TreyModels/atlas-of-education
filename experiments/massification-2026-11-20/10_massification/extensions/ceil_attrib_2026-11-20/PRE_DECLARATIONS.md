# PRE-DECLARATIONS — EXP-1 CEIL-ATTRIB

**`LABEL: SYNTHETIC` for the generator side; `OBSERVED` for the PHL UIS series side.**
Experiment: **EXP-1 CEIL-ATTRIB** from Council brief 021 (D112 #1), SYNTHESIS_021 §4.
Worker CA · created 2026-11-20 (Asia/Shanghai) · **written before any run**.
This file is frozen on creation: its sha256 is written to `PRE_DECLARATIONS.sha256` before
`code/run_ceil_attrib.py` is executed, and repeated in `RUN_MANIFEST.json`.

**No threshold, bar, lag rule, ablation definition or verdict rule in this file may be changed
after results are seen.** If an ablation cannot be implemented as declared below, it is
**reported as not implemented**, not silently approximated.

---

## 0. Scope and question

Which account carries the PHL upper-secondary ceiling?

1. the **lower-secondary pipeline** (cohort flow: upper completion is inherited from lower
   completion a stage earlier);
2. the upper **gate/demand mechanism** (schooling × markets: child-work incentive + quality);
3. **calibration/measurement** (`m`, build-out timing).

**Data used.** Frozen `generator_v1_2/code/sim_v1_2.py` + `results/synthetic_panel_v1_2.csv`
(hashes in §2); PHL `completion_upper_secondary` / `completion_lower_secondary` from
`10_massification/data/UNIVERSALIZATION_SERIES.csv` (11 observed each); `SE.SEC.DURS` /
`SE.PRM.DURS` from `09_relations/data/panel_wdi_long.csv` for the lag provenance. No web,
no external data, no writes outside this directory.

---

## 1. Frozen extract from SYNTHESIS_021 §4, EXP-1 — **verbatim**

Quoted from `08_council/brief_021/SYNTHESIS_021.md`, §4 "EXP-1 — CEIL-ATTRIB", items 2 and 5,
character-for-character (line breaks preserved):

> 2. **What changes if positive vs negative.** Predeclared three-account decision matrix (fixed before the run):
>    (a) *pipeline-consistent* (Test B) → the residual is **reclassified** as lower-pipeline inheritance; D63 stays
>    **UNABLE as to cause**, but the object moves from "upper gate" to "lower pipeline"; no demand/exit-cost claim.
>    (b) *mechanism-carried + gate-loss* → v1.2's demand/quality block earns its place as the **candidate account** (still
>    UNABLE as to cause). (c) *calibration-carried* → v1.2's ceiling claim is **withdrawn as a mechanism result** (it is a
>    calibration artefact). (d) *mixed* → undetermined; no claim, no re-tuning.

> 5. **Numeric threshold + falsifier.** **Test A (ablation):** ceiling is **mechanism-carried** iff ≥ 2 of {γ = 0;
>    household work incentive off; flat cohort} move upper UIS 2024 by **≥ 2.0 pp**, while {m sweep 1.05/1.10/1.12;
>    build-out timing ±5 y} move it by **< 1.0 pp**. **Calibration-carried** iff m or build-out moves it by **≥ 2.0 pp**
>    while the mechanism ablations move it by < 2.0 pp. **Test B (pipeline):** with a declared **3-year lag** (±1 y
>    nearest observation; 2 and 4 y as sensitivity, not verdict-changing), **pipeline-consistent** iff
>    `upper_t / lower_{t−3} ∈ [0.90, 1.10]` in **≥ 2/3** of observed pairs; **gate-loss** iff `< 0.90` in ≥ 2/3.
>    **Falsifier:** a "mixed" outcome (neither test reaches a bar) → record **UNDETERMINED**, no claim.

Item 6 (closed-claim check), also verbatim:

> 6. **Closed-claim check.** No C1–C4 reopening; no re-fit of v1.2 (ablations only); **D63 is not "explained"** —
>    only reclassified; WT4 is not re-scored; no direction claim (R13-safe).

The frozen block's one-sentence question (item 1, verbatim): "it asks whether the D63 residual
is an upper-level phenomenon at all."

---

## 2. Frozen objects, invariance requirement and STOP rule

| frozen object (read-only) | sha256 |
|---|---|
| `generator_v1_2/code/sim_v1_2.py` | `61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c` |
| `generator_v1_2/PARAMS.md` | `0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3` |
| `generator_v1_2/results/synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| `v1_2/PRE_DECLARATIONS.md` (v1.2 spec) | `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` |
| `generator_v1_2/RUN_MANIFEST.json` | `36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876` |

**Baseline invariance requirement.** The unmodified copy of `sim_v1_2.py` in this directory
(`generator_v1_2/code/sim_v1_2.py`, byte-identical to the frozen file, with a byte-identical
copy of `v1_2/PRE_DECLARATIONS.md` at `v1_2/PRE_DECLARATIONS.md` so the code's own frozen-hash
guard and its relative path resolution are preserved) must reproduce
`results/synthetic_panel_v1_2.csv` **byte-for-byte**.

- **If the baseline reproduction is not byte-identical to sha256 `14729c51…acf5ac`, STOP and
  report; no Test A or Test B result may be issued from this experiment.**
- Ablations are **declared in-memory switches** on that unmodified copy. The frozen generator
  directory `generator_v1_2/` is never written to. The scored run (`results/synthetic_panel_v1_2.csv`)
  is unchanged; every ablation panel written here is a declared variant, not a new scored run.

---

## 3. Verdict vocabulary (exactly as the frozen block defines; no invented words)

| token | applies to | meaning (from the block) |
|---|---|---|
| `MECHANISM-CARRIED` | Test A | ceiling is mechanism-carried by the frozen Test A bar |
| `CALIBRATION-CARRIED` | Test A | ceiling is a calibration/measurement artefact by the frozen Test A bar |
| `PIPELINE-CONSISTENT` | Test B / overall | the observed upper/lower ratio sits in [0.90, 1.10] in ≥ 2/3 of observed pairs |
| `GATE-LOSS` | Test B | the ratio is < 0.90 in ≥ 2/3 of observed pairs |
| `MIXED` | Test A | neither the mechanism bar nor the calibration bar is reached |
| `UNDETERMINED` | Test B / overall | no test reaches a bar (the block's falsifier), or the outcome combination is outside the four matrix cells |

No other verdict word is used. `MIXED` and `UNDETERMINED` are distinct: `MIXED` is the Test A
component outcome "neither account carried"; `UNDETERMINED` is the overall falsifier outcome
when neither test reaches a bar (and the default for a matrix combination not covered by (a)–(c)).

---

## 4. Ablation definitions — declared in full **now**

All variants are applied to an **unmodified copy** of v1.2 by one declared switch at run time.
All 30 synthetic countries are simulated under every variant, with the **same seed, the same
draw order and the same shock realisations** as the frozen run; only the declared switch differs.
Country traits and the twin/cohort shock-sharing rules are unchanged. Test A reads
`SYN00_PHL_LIKE` upper **UIS-convention** completion in **2024** (`comp_uis[2] × 100`, where
`comp_uis = m × comp_coh`, clipped to 1). `baseline` = frozen parameter block.

| variant id | declared switch | exact implementation | role |
|---|---|---|---|
| `baseline` | none | frozen `P` unchanged | reference (must equal frozen panel) |
| `gamma0` | γ = 0 | `P["gamma"] = 0.0` | mechanism |
| `work_off` | household work incentive off | set `w_child = 0` and `farm = 0` for **every** country in the four-state block, so child market-work earnings `earn_L = 0.32·AGE_W_L·max(w_child/0.32, 0.55·farm) = 0`; the `work` state remains available at zero earnings. Only this incentive term is removed; no other household parameter changes. | mechanism |
| `flat_cohort` | flat cohort (no boom; 1970 level) | for `SYN00_PHL_LIKE` only, replace its cohort path `S(t)` by its 1970 value `S(1970)` in every year; its population path and all other traits unchanged. (The other 29 synthetics keep their own paths; they do not enter Test A.) | mechanism |
| `m1.05` | m sweep | `P["meas_completion_factor"] = 1.05` | calibration |
| `m1.10` | m sweep (reference) | `P["meas_completion_factor"] = 1.10` = frozen value; must give Δ = 0.000 | calibration (reference) |
| `m1.12` | m sweep | `P["meas_completion_factor"] = 1.12` | calibration |
| `buildout_m5` | build-out timing −5 y | `P["seat_t50"] ← (seat_t50_L − 5)` for **all four levels**; all else unchanged | calibration |
| `buildout_p5` | build-out timing +5 y | `P["seat_t50"] ← (seat_t50_L + 5)` for **all four levels**; all else unchanged | calibration |

**Declared sensitivity, not verdict-bearing:** `upper_only_m5` / `upper_only_p5` shift only the
**upper-secondary** build-out centre (`seat_t50[2] ± 5`). The frozen text does not say which
level, so the whole-schedule ±5 y shift is the verdict-bearing reading (the declared build-out
schedule is the calibration object) and the upper-only shift is reported alongside; it cannot
change the Test A verdict.

**Declared sensitivity, not verdict-bearing:** the cohort-flow (identity-bound, `m = 1`) upper
2024 value under baseline, for transparency only.

Ablations are applied to all 30 countries (uniform treatment) and do not modify the frozen
generator, the frozen panel or any file outside this directory.

---

## 5. Test A classification rule — declared in full **now**

Let `Δ_v = upper_uis_2024(v) − upper_uis_2024(baseline)` in percentage points.

- **Mechanism set** `MECH = {gamma0, work_off, flat_cohort}`; `mech_hits = #{v ∈ MECH : |Δ_v| ≥ 2.0}`.
- **Calibration set** `CAL = {m1.05, m1.12, buildout_m5, buildout_p5}` (m1.10 is the baseline
  reference, Δ = 0 by construction, and is not counted as a calibration move);
  `calib_ge2 = any_{v∈CAL}(|Δ_v| ≥ 2.0)`; `calib_lt1 = all_{v∈CAL}(|Δ_v| < 1.0)`.
- `MECHANISM-CARRIED` iff `mech_hits ≥ 2` **and** `calib_lt1`.
- `CALIBRATION-CARRIED` iff `calib_ge2` **and** `mech_hits = 0` (i.e. every mechanism ablation
  moves it by < 2.0 pp).
- Otherwise `MIXED` (neither account carried by the frozen bars).

Boundary convention: "≥ 2.0 pp" and "< 1.0 pp" are applied to the absolute deviation, compared
as exact decimal values to 1e−9 (no rounding before comparison). Deltas are reported to 4 dp.

---

## 6. Test B classification rule — declared in full **now**

**Declared lag = 3 years.** For each observed PHL upper-secondary completion year `t`:
target lower year = `t − 3`. Use the observed lower-secondary value at exactly `t − 3` if present;
otherwise the **nearest observed lower-secondary year within ±1 y** of `t − 3` (i.e. `t−4`, `t−3`
or `t−2`); if no lower observation exists in that window, **the pair is dropped**. One pair per
observed upper year; no imputation, no interpolation, no re-fitting. Ratio `= upper_t / lower_{t−3}`
(both in percent; the ratio is unitless).

- `n` = number of constructed pairs.
- `PIPELINE-CONSISTENT` iff `#(ratio ∈ [0.90, 1.10]) / n ≥ 2/3`.
- `GATE-LOSS` iff `#(ratio < 0.90) / n ≥ 2/3`.
- Otherwise `UNDETERMINED`.
- Both bars cannot hold simultaneously (`2/3 + 2/3 > 1`).
- Lag 2 and lag 4 are computed with the **same** pair rule and reported as **sensitivity, not
  verdict-changing**. One further declared sensitivity (not verdict-changing): nearest available
  lower observation at **any** distance (unbounded), to show whether dropping pairs at lag 3
  changes the reading.

**Lag provenance (recorded now).** `SE.PRM.DURS` = 6 for PHL over the whole WDI window;
`SE.SEC.DURS` = 4 (1970–2016), 5 (2017), 6 (2018–2024). WDI's secondary duration measures the
whole secondary stage, not the lower-secondary stage alone; the 3-year lag is the **declared**
brief value, consistent with the lower-secondary stage length used by v1.2 (`DUR = (6, 3, 3, 4)`)
and with an ISCED lower-secondary stage of three years. The WDI duration series is recorded as
provenance and is **not** used to re-derive or re-optimise the lag.

---

## 7. Overall CEIL-ATTRIB decision — ordered rule declared **now**

The single overall token is assigned by this fixed order (the matrix (a)–(d) of §1, with the
precedence stated explicitly so it cannot be chosen after seeing results):

1. If **Test B = `PIPELINE-CONSISTENT`** → overall = **`PIPELINE-CONSISTENT`** (matrix (a): the
   residual is reclassified as lower-pipeline inheritance; D63 stays UNABLE as to cause; no
   demand/exit-cost claim). Test A's component verdict is reported alongside and does not
   override the reclassification; it is stated as a caveat on what the synthetic 2024 level can
   be attributed to.
2. Else if **Test A = `MECHANISM-CARRIED`** and **Test B = `GATE-LOSS`** → overall =
   **`MECHANISM-CARRIED`** (matrix (b): the demand/quality block is the candidate account,
   still UNABLE as to cause).
3. Else if **Test A = `CALIBRATION-CARRIED`** → overall = **`CALIBRATION-CARRIED`** (matrix (c):
   v1.2's ceiling claim is withdrawn as a mechanism result).
4. Otherwise → overall = **`UNDETERMINED`** (matrix (d)/falsifier: no claim, no re-tuning).

The precedence in (1) is declared because Test B locates the **observed** residual while Test A
attributes the **synthetic** 2024 level; the matrix's cell (a) is stated on Test B alone.

---

## 8. Reporting discipline (frozen)

- Every generated row/file carries `SYNTHETIC`; every PHL series row carries `OBSERVED`.
  Mixed files label each row.
- **No causal claim, no direction-of-causation claim, no forecast, no policy claim.**
- **No re-fit** of v1.2 and no parameter change after seeing results. Ablations only.
- **D63 is not "explained"** by this experiment — at most **reclassified** in location, and only
  if Test B reaches its bar. D63 remains UNABLE as to cause.
- **WT4 is not re-scored**; C1–C4 are not reopened; v1.2's frozen checks are not re-scored.
- A mixed or undetermined outcome is a **legitimate finding**, reported as such, not rescued by
  adding variants or moving bars.
- The three-account matrix outcome is recorded even when the result is negative for one account.

---

## 9. No-threshold-change statement

The thresholds `≥ 2.0 pp`, `< 1.0 pp`, `[0.90, 1.10]`, `≥ 2/3`, the 3-year lag and the ±1 y
pair window above are copied from the frozen EXP-1 block or declared here **before** execution.
They will not be changed after results. Any post-hoc observation is labelled post-hoc and is not
used for a verdict.
