# PRE-DECLARATIONS — FIX + RE-RUN of the `completion_uis` ceiling (DEBUG)

**LABEL: `DEBUG`.** This is the **Agent 2** cell of the model-debug work-stream
(`../PRE_DECLARATIONS.md`, sha256 `748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553`,
including **AMENDMENT 1: measures are different objects**). It repairs **one named defect** in a **copy** of
the generator code, then re-runs the **EXP-21 conversion register** on the repaired panels and reports the
deltas. It adds **no reproduction claim**, predeclares **no successor generator**, **reopens nothing**, changes
**no threshold**, fits **nothing**, and **does not edit the gate-passed write-up**
(`10_massification/lit/PHASE_WRITEUP.md`). Every number it emits is labelled `DEBUG`.

This document is written and hashed **before** any repaired-panel number is computed. Its sha256 is in
`PRE_DECLARATIONS.sha256` and is **enforced by `code/run_conv_reg_repaired.py` at pre-input and again
immediately before the verdict is written** (D158(1)). A mismatch aborts with no verdict.

---

## 0. Machine-readable freeze fields

| field | value |
|---|---|
| cell | EXP-21 CONV-REG — **repaired re-run (DEBUG)** |
| defect | `CAP-01` (cap audit), named in D160/D164: `completion_uis` capped at 1.0 |
| fixed expression | `out["comp_uis"][L, t] = max(0.0, P["meas_completion_factor"] * comp_coh)` |
| removed expression | `out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)` |
| declared `m` | **1.10**, frozen, all levels and countries — a **point convention**, not a conversion |
| declared completion convention | **UIS completion rate (CR)**, denominator = population **3–5 years above the grade** (older cohort) |
| register thresholds | **inherited verbatim** from `../conv_reg_2026-11-20/PRE_DECLARATIONS.md`, sha256 `1dd86bd139a81c22e0ba2918728818fe7184775d925211a28fdd2be00b975410` |
| band / share / range / gate / tolerance | `[0.85, 1.15]` / `>= 0.80` / `<= 0.30` / `< 3` pairs → `THIN` / `1e-9` — **unchanged** |
| systems / levels | PHL, KOR, KHM, CHN × primary, lower_secondary, upper_secondary — **unchanged** |
| write scope | `10_massification/extensions/model_debug_2026-11-21/fix_rerun/` only |
| determinism | two clean runs, **byte-identical**; no clock in outputs; floats `%.10g` |

---

## 1. The defect (measured, not inferred)

`completion_uis` is the **declared** object `m × comp_coh`, `m = 1.10` frozen
(`generator_v1_2/PARAMS.md` §7; v1.6 `PRE_DECLARATIONS` R7c: "a CONVENTION, not a conversion"). **No
PARAMS, PRE_DECLARATIONS or MODEL_ARCHITECTURE text on disk places an upper bound of 1.0 on it.** The
implementation nevertheless writes

```python
out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
```

with `clip(x, lo, hi) = max(lo, min(hi, float(x)))`. It binds in **35 of 6,720 cells** on **v1.3**
(`sim_v1_3.py:832`) and the **same 35** on **v1.2** (`sim_v1_2.py:610`), all **primary**, five countries
(`SYN00_PHL_LIKE`, `SYN07`, `SYN10_BOOM`, `SYN19`, `SYN23`); the uncapped maximum is **1.044677728**; **0**
cells bind on **A17** (uncapped max 0.9402099553). Enumerated in `../cap_audit/results/CAP_AUDIT.md` §1 and
`CAP_AUDIT_CELLS.csv` (`clamp_id == CAP-01`).

Consequence recorded in D160: the m-constancy test reads `CONSTANT` on A17 (`8.8395202269e-10`) and
`NOT-CONSTANT` on v1.3/v1.2 (`4.7043695535e-02`). The v1.3/v1.2 non-constancy is **hypothesised to be the
cap**, not model behaviour; §5 test T3 measures it rather than assuming it.

---

## 2. The declared convention (stated explicitly, as AMENDMENT 1 requires)

**The object is a UIS completion rate (CR).** Its denominator is the population **3–5 years above the
official graduation age of the grade** — an **older cohort** — and it counts completers across years,
including **repeaters and over-age** pupils still completing the level. It is **not** a share of the official
age band and **not** a share of the entry cohort.

**Binding consequences:**

1. **CR is not bounded above by 1.0.** A year's completers can exceed the 3–5-years-above-grade population
   when repeaters/over-age completion is spread across cohorts; the ceiling at 1.0 is therefore an
   **implementation artefact**, not a declared bound.
2. **CR is not bounded above by GER.** The two objects have different denominators (older cohort vs official
   age band; gross includes all ages). CR may **exceed** GER; that is a denominator/definition fact, not an
   arithmetic impossibility (PHL 2024: 98.3 completion on 94.0 GER).
3. **This is not an NER bound.** NER is official-age enrolment / official-age population and **is `<= 100`
   definitionally**. Nothing here relaxes NER, and no NER statistic is computed in this cell.
4. **`m = 1.10` is a declared measurement factor — a point convention, not a conversion.** It maps the
   cohort-flow object `comp_coh` to the UIS-convention object `completion_uis`. It is not fitted, not
   estimated, not a level conversion for the observed record, and it carries no level claim.

**What the fix therefore is:** the declared identity `completion_uis = 1.10 × comp_coh` is restored with a
**one-sided floor only** (`>= 0`; a completion cannot be negative, and 0 cells bind the floor). The
**cohort-flow clip on `comp_coh` (`0.0, 1.0`) is a declared bound and is untouched** (CAP-02).

---

## 3. The fix — exact scope (measured defect only)

Inside this cell's **copies** (`code/sim_v1_3_fix.py`, `code/sim_v1_2_fix.py`), and nowhere else:

| # | change | reason |
|---|---|---|
| F-1 | `out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)` → `out["comp_uis"][L, t] = max(0.0, P["meas_completion_factor"] * comp_coh)` | **the named defect (CAP-01)** |
| F-2 | the copy's path block resolves frozen **inputs** from the original generator directory (`ROOT` override only) | a copy must read the frozen inputs; no arithmetic change |

**Explicitly NOT changed** (each is left exactly as delivered): the `comp_coh` cohort-flow clip `clip(a_entry *
surv, 0.0, 1.0)` (CAP-02, declared); the GER / `overage_cap` Z1 gate `clip(..., 0.0, 1.05*100)` (CAP-06,
declared); the capacity gates `phys`, `adm_off`, `adm_oa` (CAP-07/08/09, declared); the survival clip
`clip(..., 0.02, 0.995)` (CAP-03; the **floor** CAP-04 is undeclared but is **not** the named defect — it is
**recorded, not fixed**, per the audit); the share renormalisations (CAP-18/19); every threshold; every
parameter; the seed; the draw order; the output format.

**No new parameter. No fitting. No re-scoring of any delivered cell. No successor generator.**

---

## 4. The re-run specification

`code/run_conv_reg_repaired.py` is the delivered `../conv_reg_2026-11-20/code/run_conv_reg.py` **reused
verbatim** except for three mechanical substitutions that the re-run requires:

1. `ROOT` resolves one directory deeper (this cell sits two levels below `extensions/` rather than one);
2. the **three panel inputs** point at the **repaired copies**:
   `results/panels/synthetic_panel_v1_3_repaired.csv` and
   `results/panels/synthetic_panel_v1_2_repaired.csv`, with **A17 unchanged**
   (`generator_v1_7_partrepair/results/panel_A17.csv`);
3. the `cell` string in `VERDICT.json` reads `EXP-21 CONV-REG (DEBUG repaired re-run)`.

Everything else — the observed-series reader, the pair rule, `T = completion / GER`, the band, the in-band
share, the range, the `THIN` gate, the crossing rule, the m-constancy test at `1e-9`, the verdict precedence,
and the traceability re-read of every observed pair **against the observed series, not against any panel** —
is byte-for-byte the delivered logic. The delivered predeclaration `1dd86bd1…` is re-hashed and asserted
equal at run time; its thresholds are inherited unchanged.

**The panel substitution is the only input change.** The observed `T` series is untouched, so the 12
interchangeability labels are expected **not** to move; that expectation is tested (T4), not assumed.

---

## 5. Pre-declared tests and reporting (a)–(d)

Every test reports a number; a FAIL or a mixed result is reported as such and **nothing is tuned**.

- **T1 — panel identity (fix isolation).** Re-run each repaired generator copy (same seed `20261120`, same
  inputs) and compare its panel row-by-row with the delivered panel. **Pass** iff the two panels have the
  same header, the same 6,720 rows, **every** non-`completion_uis` column is byte-identical, and
  `completion_uis` differs in **exactly 35 cells per panel**, each equal to `1.10 × completion_cohort`
  (to panel print precision) and each > 1.0. Any other difference is a FAIL and stops the interpretation.
- **T2 — m-constancy after the fix.** Recompute `completion_uis / completion_cohort` against 1.10 at
  `1e-9` on repaired v1.3, repaired v1.2, and delivered A17. Report `max_abs_dev_ratio`, `n_tested`,
  `n_not_testable`, verdict.
- **T3 — cap-induced vs real (question b).** Report the uncapped maximum (`1.10 × completion_cohort`),
  the delivered maximum, the repaired maximum, and the before/after `max_abs_dev_ratio`. The test: if the
  repaired deviation falls to `<= 1e-9` (the float-print noise floor) while the uncapped maximum is
  unchanged, the `4.7043695535e-02` was **entirely cap-induced**; if a deviation survives above `1e-9`,
  part of it is **real** and is reported as such.
- **T4 — register invariance (question c).** Compare the repaired re-run register with the delivered
  `CONV_REG.csv`: every field except the m-constancy block must be identical; report the 12-cell counts
  (`INTERCHANGEABLE` / `NOT-INTERCHANGEABLE` / `THIN`) before and after, and the exact list of numbers that
  moved.
- **T5 — determinism.** Two clean runs of the whole cell into separate directories; every artifact
  **byte-identical** (`DETERMINISM.json`).
- **T6 — delivered inputs unchanged.** Hash the delivered v1.3 panel, v1.2 panel, A17 panel, the delivered
  conv_reg `PRE_DECLARATIONS.md` and `run_conv_reg.py` **before and after**; they must be unchanged. This
  cell writes only inside its own directory.

**Question (d) — the write-up.** The write-up is **not edited**. For every affected claim the report quotes
the sentence **verbatim**, gives the before/after number, and classifies it as a **prospective amendment**
(a `SIM`/convention sentence whose number moved) or a **published-number change** (a number in the
gate-passed text that a future, user-approved amendment would replace). The two panels' cap statement is
reported for **both** objects: **as-delivered** panels cap 35/6,720 cells at 1.0 (true, unchanged); the
**repaired copies** cap **0** cells.

---

## 6. Falsifiers (pre-declared)

The cell's interpretation is **withdrawn** and the result reported as `MIXED`/`FAIL` if any of the
following occurs:

1. a repaired panel differs from the delivered panel in any column other than `completion_uis`, or in more
   or fewer than 35 `completion_uis` cells (T1);
2. any repaired `completion_uis` is not `1.10 × completion_cohort` (T1);
3. the repaired m-constancy deviation stays above `1e-9` (T3) — then the non-constancy was **not** wholly
   cap-induced, and both parts are reported;
4. any of the 12 register labels or their `n_pairs` / `T_min` / `T_max` / `in_band_share` / `crossing_year`
   moves (T4);
5. two runs are not byte-identical (T5);
6. any delivered file's hash changes (T6).

---

## 7. Non-goals (binding)

- **No reproduction claim.** The repaired panel is a `SYNTHETIC` diagnostic object, not evidence about any
  country, not a forecast, not an estimate; country labels are synthetic.
- **No successor generator**; the closed `v1.5`–`v1.7` family stays closed (D150/D154/D167).
- **No causal or direction claim.** The fix moves a reported convention object; it does not identify a
  dynamic or license a level sentence.
- **No threshold change, no fitting, no new parameter.**
- **CAP-04** (survival floor 0.02, 24 tertiary burn-in cells) is **recorded only**: it is undeclared but is
  **not** the named defect, it is upstream and identical on all three panels, and this licence does not
  reach it.
- **CAP-14 / CAP-20** (non-binding guards) — **no action**.
- **The gate-passed write-up is not edited**; any change to it is a prospective amendment for the user.
- **No web; no server interaction.** Writes stay inside this directory.

## 8. Determinism and labels

One seed (`20261120`) inherited unchanged; floats `%.10g`; no wall-clock in any output. Every artifact carries
`DEBUG`; inherited `SYNTHETIC` / `OBSERVED` / `DERIVED` labels are preserved. Two runs must be byte-identical.
