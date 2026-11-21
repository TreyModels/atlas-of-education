# FIX + RE-RUN — the `completion_uis ≤ 1.0` ceiling (DEBUG)

**LABEL: `DEBUG`.** Agent 2 cell of the model-debug work-stream. One named defect was repaired in a
**copy** of the v1.3 and v1.2 generator code, and the **EXP-21 conversion register** was re-run on the
repaired panels. Nothing was fitted; no parameter, seed, draw order or threshold was changed; no
delivered panel, register cell or write-up was edited. Every number below is a **count on a frozen
panel**, a **value read from a frozen panel**, or an **arithmetic identity** on those panels.

| | |
|---|---|
| cell | `10_massification/extensions/model_debug_2026-11-21/fix_rerun/` |
| contract | [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md), sha256 `5d7fb5c36aecc420e5e4839e6e48a43ed81fca5697a0bb0cb64df4ed3c7283e8` (**hashed before any repaired number was computed; enforced twice by the runner**) |
| parent contract | `../PRE_DECLARATIONS.md`, sha256 `7d8bade95407a2fe76c95a740e0c98a74f34962117b33846df37a7d6a48f56a9` (incl. **AMENDMENT 1**: measures are different objects), unchanged before/after |
| defect | `CAP-01` in `../cap_audit/results/CAP_AUDIT.md`; named in `08_council/DECISIONS.md` D160/D164 |
| delivered register | `../conv_reg_2026-11-20/`, predecl `1dd86bd1…` (**re-hashed and enforced at run time; not edited**) |
| determinism | **two runs, 12/12 artifacts byte-identical** (`results/DETERMINISM.json`) |
| delivered inputs | **12/12 unchanged before vs after** the whole cell (`results/INPUT_HASHES_DEBUG.json`) |

---

## 0. Headline (all numbers)

| item | before (as delivered) | after (repaired copies) |
|---|---|---|
| `completion_uis` capped at 1.0, v1.3 | **35 / 6,720** | **0 / 6,720** |
| `completion_uis` capped at 1.0, v1.2 | **35 / 6,720** | **0 / 6,720** |
| `completion_uis` capped at 1.0, A17 | **0 / 6,720** | **0 / 6,720** (panel unchanged) |
| max `completion_uis`, v1.3 / v1.2 | **1.0** | **1.044677728** |
| max `1.10 × completion_cohort` | **1.044677728** | **1.044677728** (unchanged) |
| `m`-constancy, v1.3 / v1.2 | `NOT-CONSTANT` **4.7043695535e-02** | `CONSTANT` **9.6646846082e-10** |
| `m`-constancy, A17 | `CONSTANT` **8.8395202269e-10** | `CONSTANT` **8.8395202269e-10** (unchanged) |
| register overall verdict | `REGISTER-BINDING` | `REGISTER-BINDING` (unchanged) |
| 12-cell counts | **4 INTER / 6 NOT / 2 THIN** | **4 INTER / 6 NOT / 2 THIN** (unchanged) |
| repaired capped cells with CR > GER | — (audit: 0 of 70 on delivered) | **0 of 70** (all are CR ≤ the model's own GER, which is 105.0 there) |
| `T` values, `n_pairs`, crossings | — | **18/18 register rows identical; 90/90 detail rows identical** |

**One-line result:** the 4.7043695535e-02 non-constancy was **entirely the cap** (wholly cap-induced);
after the fix `m = 1.10` is `CONSTANT` on all three panels, and **no register label moves** because the
register's `T` is built from observed series that the fix never touches.

---

## 1. The fix — exact diff

Two files were copied into `code/`, and **two hunks** were applied to each: the **path block** (so the copy
reads the frozen inputs from the original generator directory) and the **named clamp**. No other line
changed.

### 1.1 The defect line (v1.3)

`generator_v1_3/code/sim_v1_3.py:832` → `code/sim_v1_3_fix.py:835`

```diff
-            out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
+            out["comp_uis"][L, t] = max(0.0, P["meas_completion_factor"] * comp_coh)  # DEBUG FIX CAP-01: one-sided floor; declared UIS CR (older-cohort denominator) may exceed 1.0
```

### 1.2 The defect line (v1.2)

`generator_v1_2/code/sim_v1_2.py:610` → `code/sim_v1_2_fix.py:613`

```diff
-            out["comp_uis"][L, t] = clip(P["meas_completion_factor"] * comp_coh, 0.0, 1.0)
+            out["comp_uis"][L, t] = max(0.0, P["meas_completion_factor"] * comp_coh)  # DEBUG FIX CAP-01: one-sided floor; declared UIS CR (older-cohort denominator) may exceed 1.0
```

### 1.3 The path block (the only other hunk; no arithmetic)

```diff
-ROOT = Path(__file__).resolve().parent.parent   # generator_v1_3/   (v1.2: generator_v1_2/)
+# DEBUG COPY (model_debug_2026-11-21/fix_rerun): all frozen INPUTS are read from the
+# original generator_v1_3 directory; only the CAP-01 completion ceiling is repaired here.
+_ORIG_SYNTH = Path(__file__).resolve().parents[3] / "synthetic_2026-11-20"
+ROOT = _ORIG_SYNTH / "generator_v1_3"            (v1.2: / "generator_v1_2")
```

**What is deliberately unchanged** (and verifiable in the diff): the declared cohort-flow clip
`comp_coh = clip(a_entry * surv, 0.0, 1.0)` (CAP-02); the GER / `overage_cap` Z1 gate
`clip(..., 0.0, 1.05 × 100)` (CAP-06); the capacity gates `phys`, `adm_off`, `adm_oa`
(CAP-07/08/09); the survival clip `clip(..., 0.02, 0.995)` (CAP-03) **including its undeclared 0.02
floor (CAP-04, recorded below, not fixed)**; every share renormalisation (CAP-18/19); every threshold;
every parameter; the seed; the draw order; the `%.10g` output format.

---

## 2. The declared convention (stated explicitly, per AMENDMENT 1)

**`completion_uis` is a UIS completion rate (CR).** Its denominator is the population **3–5 years above
the official graduation age of the grade** — an **older cohort** — and it counts completers across years,
including **repeaters and over-age** pupils still completing the level. It is **not** a share of the
official age band and **not** a share of the entry cohort.

1. **CR is not bounded above by 1.0.** Completers in a year can exceed the 3–5-years-above-grade
   population when repeaters/over-age completion is spread across cohorts; the 1.0 ceiling is an
   **implementation artefact**, not a declared bound.
2. **CR is not bounded above by GER.** Completion and GER have different denominators (older cohort vs
   official age band; gross enrolment includes all ages). CR may **exceed** GER; that is a
   denominator/definition fact, not an arithmetic impossibility (PHL 2024: 98.3 completion on 94.0 GER).
3. **This is not an NER bound.** NER = official-age enrolment / official-age population and is
   **`≤ 100` definitionally**. Nothing here relaxes NER; no NER statistic is computed in this cell.
4. **`m = 1.10` is a declared measurement factor — a point convention, not a conversion.** It maps the
   cohort-flow object `comp_coh` to the UIS-convention object `completion_uis`. It is not fitted, not
   estimated, and carries no level claim for the observed record.

The repaired line is therefore the **declared object restored**: `completion_uis = max(0, 1.10 × comp_coh)`
— a one-sided floor only (0 cells bind it). The **declared** cohort-flow clip on `comp_coh` stays.

---

## 3. Method

1. **Copies** `code/sim_v1_3_fix.py` and `code/sim_v1_2_fix.py` were made from the delivered generators;
   the only changes are §1.1–§1.3. The copies resolve every frozen input (PARAMS, predeclarations, shadow
   module, data) from the original, unmodified generator directories; they write only into this cell.
2. `code/run_repaired.py` executes the **same simulation call the delivered `main()` makes** (v1.3:
   shadow-off host mapping then the scored shadow-on run; v1.2: `run_all()`), with seed `20261120`
   unchanged, and writes the repaired panel.
3. `code/uncap_cells.py` compares each repaired panel with the delivered panel **row by row and column by
   column** (T1) and writes `results/CAP_FIX_CELLS.csv`.
4. `code/verify_identity.py` measures the identity **in memory**, separating the model identity from the
   `%.10g` panel serialisation.
5. `code/run_conv_reg_repaired.py` is the delivered `run_conv_reg.py` **reused verbatim** except for:
   `ROOT` one directory deeper; the two capped panel inputs pointed at the repaired copies (A17 unchanged);
   the `cell` string marked DEBUG; and an added re-hash of the **delivered** threshold predeclaration
   (`1dd86bd1…`, read-only) so its inheritance is enforced, not asserted. `T`, the band, the in-band
   share, the range, the `THIN` gate, the crossing rule, the `1e-9` m test, the precedence and the
   traceability re-read are unchanged.
6. `code/run_all_debug.py` runs the whole cell twice and compares artifacts.

**T1 result (fix isolation).** For each of v1.3 and v1.2, the repaired panel has the same header and the
same 6,720 rows; **`completion_uis` is the only column that differs, in exactly 35 cells**; every repaired
value equals `1.10 × completion_cohort` to panel precision, and every one is `> 1.0`. Delivered panel
sha256: v1.3 `47d4b082f4ba5838…`, v1.2 `14729c5141a71dd9…` (unchanged). Repaired: v1.3
`48113e4e6e704041…`, v1.2 `de44a994ab019093…`.

**Determinism.** Two clean runs: panels are produced by an **independent second execution** of each
generator and are byte-identical; the register is a second execution on the byte-identical panel set, so
even its `panel_path` provenance column is identical. **12/12 artifacts byte-identical**
(`results/DETERMINISM.json`).

---

## 4. The fix delta — 35 cells per panel, uncapped

All 35 are **primary**, in **five** countries, **2012–2025**; none at lower, upper or tertiary; **the same
35 `(country, level, year)` cells on v1.3 and v1.2** (verified set equality). Unchanged maxima:
**`1.10 × completion_cohort` = 1.044677728**, delivered `completion_uis` max = **1.0**, repaired
`completion_uis` max = **1.044677728**. Deltas run **+0.000258707 … +0.044677728** (mean
**+0.0187814061714**).

| country | n cells | years |
|---|---:|---|
| `SYN00_PHL_LIKE` | 2 | 2024–2025 |
| `SYN07` | 14 | 2012–2025 |
| `SYN10_BOOM` | 2 | 2024–2025 |
| `SYN19` | 5 | 2021–2025 |
| `SYN23` | 12 | 2014–2025 |
| **total** | **35** | |

Full per-cell table (v1.3 = v1.2; both panels in `results/CAP_FIX_CELLS.csv`, 70 panel-rows; values are
`%.10g`):

| country | year | completion_cohort | uncapped = 1.10 × cohort | repaired − delivered |
|---|---|---|---|---|
| `SYN00_PHL_LIKE` | 2024 | 0.9162480129 | **1.007872814** | +0.007872814 |
| `SYN00_PHL_LIKE` | 2025 | 0.9200914783 | **1.012100626** | +0.012100626 |
| `SYN07` | 2012 | 0.9286930712 | **1.021562378** | +0.021562378 |
| `SYN07` | 2013 | 0.931290077 | **1.024419085** | +0.024419085 |
| `SYN07` | 2014 | 0.9334983933 | **1.026848233** | +0.026848233 |
| `SYN07` | 2015 | 0.9355748921 | **1.029132381** | +0.029132381 |
| `SYN07` | 2016 | 0.937437586 | **1.031181345** | +0.031181345 |
| `SYN07` | 2017 | 0.9391095923 | **1.033020552** | +0.033020552 |
| `SYN07` | 2018 | 0.9407097727 | **1.03478075** | +0.03478075 |
| `SYN07` | 2019 | 0.9422650926 | **1.036491602** | +0.036491602 |
| `SYN07` | 2020 | 0.943660401 | **1.038026441** | +0.038026441 |
| `SYN07` | 2021 | 0.9450899147 | **1.039598906** | +0.039598906 |
| `SYN07` | 2022 | 0.9462953797 | **1.040924918** | +0.040924918 |
| `SYN07` | 2023 | 0.9475406534 | **1.042294719** | +0.042294719 |
| `SYN07` | 2024 | 0.9486606483 | **1.043526713** | +0.043526713 |
| `SYN07` | 2025 | 0.9497070256 | **1.044677728** | +0.044677728 |
| `SYN10_BOOM` | 2024 | 0.9162480129 | **1.007872814** | +0.007872814 |
| `SYN10_BOOM` | 2025 | 0.9202209151 | **1.012243007** | +0.012243007 |
| `SYN19` | 2021 | 0.9093260974 | **1.000258707** | +0.000258707 |
| `SYN19` | 2022 | 0.9110359083 | **1.002139499** | +0.002139499 |
| `SYN19` | 2023 | 0.9125096006 | **1.003760561** | +0.003760561 |
| `SYN19` | 2024 | 0.9138734758 | **1.005260823** | +0.005260823 |
| `SYN19` | 2025 | 0.9153694921 | **1.006906441** | +0.006906441 |
| `SYN23` | 2014 | 0.9097506221 | **1.000725684** | +0.000725684 |
| `SYN23` | 2015 | 0.9118709384 | **1.003058032** | +0.003058032 |
| `SYN23` | 2016 | 0.913618185 | **1.004980004** | +0.004980003 |
| `SYN23` | 2017 | 0.9147273904 | **1.006200129** | +0.006200129 |
| `SYN23` | 2018 | 0.9157772285 | **1.007354951** | +0.007354951 |
| `SYN23` | 2019 | 0.9175346075 | **1.009288068** | +0.009288068 |
| `SYN23` | 2020 | 0.9189018906 | **1.01079208** | +0.01079208 |
| `SYN23` | 2021 | 0.9198101898 | **1.011791209** | +0.011791209 |
| `SYN23` | 2022 | 0.9213221451 | **1.01345436** | +0.01345436 |
| `SYN23` | 2023 | 0.9215761373 | **1.013733751** | +0.013733751 |
| `SYN23` | 2024 | 0.9226918262 | **1.014961009** | +0.014961009 |
| `SYN23` | 2025 | 0.9237353608 | **1.016108897** | +0.016108897 |

### 4.1 Measure question — do the repaired capped cells exceed GER? (AMENDMENT 1; audit §5 item 4)

For each of the 70 repaired panel-rows, `results/CAP_FIX_CELLS.csv` now carries the model's own `ger`
at that cell and the repaired CR against it (columns `ger_at_cell`, `cr_over_ger`, `cr_minus_ger_pp`,
`measure_verdict`), so the measure question is **measured on the re-run**, not asserted.

| question | repaired answer |
|---|---|
| capped cells with **CR > GER** | **0 of 70** (v1.3 **0/35**, v1.2 **0/35**) |
| capped cells with **CR ≤ GER** | **70 of 70** |
| GER at the fixed cells | **105.0 in all 70** (the declared Z1 gate is binding there) |
| repaired CR at the fixed cells | **100.0258707 – 104.4677728 pp** |
| repaired CR − GER spread | **−4.9741293 to −0.5322272 pp** (all negative) |
| whole-panel cells with CR > GER, delivered → repaired | **15 → 15** on v1.3; **15 → 15** on v1.2 |

**Verdict on the 35: none is a legitimate CR-above-GER case.** In all 35 the model's GER sits at its
declared 105 gate and the repaired CR is **below** it (100.03–104.47 pp). The cap therefore cut a CR
that was already under the model's own GER; it cannot be described as "holding CR down to GER" or as an
NER-style impossibility. The cells where the model does put CR above GER are 15 uncapped cells on each
panel (unchanged at 15 after the fix, because none of them was capped); the 35 capped cells are not among
them. These are arithmetic reads of the repaired panels; no causal claim is made.

A17: **0** cells where `1.10 × cohort > 1`; max `completion_uis` **0.9402099553**, unchanged.

---

## 5. `m`-constancy before / after (recomputed, 1e-9)

| panel | n tested | max_abs_dev_ratio before | before | max_abs_dev_ratio after | after |
|---|---:|---|---|---|---|
| v1.3 | 6,720 | **4.7043695535e-02** | `NOT-CONSTANT` | **9.6646846082e-10** | **`CONSTANT`** |
| v1.2 | 6,720 | **4.7043695535e-02** | `NOT-CONSTANT` | **9.6646846082e-10** | **`CONSTANT`** |
| A17 | 6,720 | **8.8395202269e-10** | `CONSTANT` | **8.8395202269e-10** | `CONSTANT` (unchanged) |

`n_not_testable = 0` on all three; `max_abs_dev_factor = 0.0` on all three; `max_abs_rel_residual`
1.0e-10 (A17) / 4.9752237843e-10 (repaired v1.3, v1.2).

**The 9.6647e-10 is serialisation, not model behaviour.** In memory the repaired object satisfies
`completion_uis = 1.10 × completion_cohort` **exactly**: `max |uis − 1.10·coh| = 0.0000000000e+00` on both
repaired runs (`results/IDENTITY_CHECK.json`). The panel writes `%.10g`, and re-reading two independently
rounded numbers leaves a ≤ ~1e-9 ratio deviation — the **same order as A17's 8.8395202269e-10**. The new
max deviation sits at `SYN08 / upper_secondary / 1974` (ratio 1.0999999990), a cell that was **never
capped**; the deviation has moved off the capped primary cells entirely.

---

## 6. Answers

### (a) Is `m` still constant only on A17 after the fix?

**No — it is no longer A17-only.** After the fix `completion_uis / completion_cohort = 1.10` within `1e-9`
on **all three** panels: A17 `8.8395202269e-10`, repaired v1.3 `9.6646846082e-10`, repaired v1.2
`9.6646846082e-10` — all `CONSTANT` (6,720/6,720 testable each). The A17-only constancy was an artefact
of the cap binding on the other two panels; with the cap removed, the constant is exact (in memory) on
every panel.

### (b) Was the v1.3/v1.2 `NOT-CONSTANT 4.7043695535e-02` cap-induced or real?

**Wholly cap-induced — confirmed with numbers.**

- The old maximum deviation is **exactly the boundary of the largest capped cell**: the largest capped
  `completion_cohort` is **0.9497070256** (`SYN07 / primary / 2025`); `1 / 0.9497070256 − 1.10 =
  −0.047043695535…`, which is `4.7043695535e-02` to every printed digit. A cap binding at 1.0 produces
  exactly this deviation; a model non-constancy would not sit precisely on `1/coh`.
- Uncapped max: **1.044677728**; delivered max: **1.0**; repaired max: **1.044677728** (the declared
  object is now emitted, not truncated).
- After the fix the maximum deviation falls to **9.6646846082e-10** — a factor **≈ 4.87 × 10⁷**
  smaller, below the `1e-9` test, and at an uncapped cell, from `%.10g` rounding alone (in-memory 0.0).

No residual real component survives above `1e-9`; a `MIXED` verdict is therefore **not** warranted.

### (c) Do the 12-cell interchangeability counts change?

**No: 4 `INTERCHANGEABLE` / 6 `NOT-INTERCHANGEABLE` / 2 `THIN` (plus 6 `NO-COMPLETION-SERIES` for
HKG/JPN), before and after.** The overall verdict stays **`REGISTER-BINDING`** (clause 2 fired: any
`NOT-INTERCHANGEABLE` or any `T` crossing 1.0; 6 cells cross).

**Why they cannot change.** The register's `T = observed completion / observed GER` on same-year observed
pairs; both sides are read from `10_massification/data/UNIVERSALIZATION_SERIES.csv`. The model panels
enter **only** the `m`-constancy block (and its console diagnostic). The fix changes a **model-reported**
object; it does not touch the observed series, the pair rule, or any threshold. Hence the 12 labels are
invariant by construction — and this was verified, not assumed:

- `CONV_REG.csv`: all 18 rows; **every field identical** except `predecl_sha256_12` — the delivered
  rows carry the register's frozen predeclaration `1dd86bd139a8`; the re-run writes the governing DEBUG
  predeclaration `5d7fb5c36aec` (the delivered `1dd86bd1…` file is re-hashed and **enforced** at run time,
  so its thresholds are inherited, not restated); all `n_pairs`, `T_min`, `T_max`, `range`,
  `in_band_share`, `n_in_band`, `band_ok`, `range_ok`, `crossing_year`, `crossing_interval`,
  `n_crossings`, `verdict` identical.
- `CONV_REG_DETAIL.csv`: **90/90 rows byte-identical** (all `completion_value`, `ger_value`, `T`,
  `in_band`).
- `CONV_REG_SYSTEM.csv`: **6/6 rows byte-identical**.
- `VERDICT.json`: `overall_verdict`, `counts`, `precedence_trace`, `frozen_thresholds` identical.

**Exactly which numbers moved:** (i) `M_CONSTANCY.csv` rows v1.3 and v1.2: `max_abs_dev_ratio`
`4.7043695535e-02 → 9.6646846082e-10`, `verdict` `NOT-CONSTANT → CONSTANT`, `panel_path` now the repaired
copies; (ii) `VERDICT.json` `m_constancy` (`v1.3`/`v1.2` → `CONSTANT`) and `m_constancy_max_dev`;
(iii) the console diagnostic `completion_uis == 1.0 exactly (capped)` `35 → 0`; (iv) the
`predecl_sha256_12` provenance column (12 rows) as above. **Nothing else.**

### (d) Would any level sentence in the write-up change?

**No level sentence (a sentence carrying a completion or GER level in pp) changes, and there are zero
published-number changes.** The gate-passed write-up is **not edited**. Its observed level numbers rest on
`UNIVERSALIZATION_SERIES.csv` (untouched), and its C-09 condition already bars fusing `completion_uis` with
observed completion. The affected claims are the **convention/diagnostic** claim C-13 and two table rows;
they are **prospective amendments**, not published-number changes, because each cites the **as-delivered**
`M_CONSTANCY.csv` — which is byte-unchanged — and therefore remains literally true of its cited object.

**A. `W-2.6`, claim C-13 (lines 239–245), verbatim:**

> `[C-13 · DECLARED + SIM · A17, v1.3, v1.2 panels · — · CLOSED]` `m = 1.10` is a `DECLARED` point
> convention on a **synthetic** panel — the identity `completion_uis / completion_cohort` is `CONSTANT` on
> A17 at `8.8395202269e-10` and `NOT-CONSTANT` on v1.3 and v1.2 at `4.7043695535e-02`, because **35 of
> 6,720** cells in each of those two panels cap `completion_uis` at 1.0 exactly where `1.10 ×
> completion_cohort > 1` ([`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv),
> columns `panel_path`, `completion_uis_column`, `completion_cohort_column`; V47) — and it is **not** a
> level convention for the observed record.

- **Before** (as delivered): A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02;
  35/6,720 capped.
- **After** (repaired copies): all three `CONSTANT`; v1.3/v1.2 9.6646846082e-10; 0/6,720 capped in the
  repaired copies, with 35 cells now > 1.0 (max 1.044677728).
- **Classification: prospective amendment** (the `SIM` sentence would read "CONSTANT on all three panels;
  the former v1.3/v1.2 `NOT-CONSTANT` was the CAP-01 ceiling"). **Not** a published-number change: the
  cited file, its numbers and the observed record are unchanged. The sentence's **explanation is
  confirmed** — the non-constancy was the cap.

**B. Appendix A, Table A-1, `m`-constancy row (line 497), verbatim:**

> | `m`-constancy | A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02 |
> [`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv) | `SIM` |

Before → after: v1.3/v1.2 `NOT-CONSTANT` **4.7043695535e-02** → `CONSTANT` **9.6646846082e-10**; A17
unchanged. **Prospective amendment** (same reason).

**C. Appendix A, Table A-1, capped-cells row (line 498), verbatim:**

> | capped cells | 35 of 6,720 per panel | same, `completion_uis`/`completion_cohort` columns | `DERIVED` |

Before → after: **35/6,720 → 0/6,720** in the repaired copies (as-delivered stays 35/6,720). **Prospective
amendment.**

**D. "Conditions that travel with it" (line 503), verbatim (first clause):**

> **Conditions that travel with it.** `CONSTANT` is A17-only and may never appear without the panel; `THIN`
> is unmeasured, not clean; …

Before → after: `CONSTANT` was **A17-only**; after the repair it holds on **all three panels**. The
condition remains correct for the **as-delivered** `M_CONSTANCY.csv`; if the write-up is amended to cite
the repaired object, the clause must become "`CONSTANT` is asserted per panel; after the CAP-01 repair it
holds on A17 and on repaired v1.3/v1.2". **Prospective amendment.**

**E. Provenance index, Table G-1 row 10 (line 707), verbatim:**

> | 10 | `m`-constancy and the 35 capped cells |
> [`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv) | `panel_path`,
> `completion_uis`, `completion_cohort` | V47 |

Still valid for the delivered file; a prospective amendment would point at
`fix_rerun/results/REPAIRED_M_CONSTANCY.csv` if the repaired object is ever cited.

**F. The "35/6,720 cells cap `completion_uis` at 1.0" statement — both objects named:**

- **As delivered** (the object the write-up cites): **true and unchanged** — v1.3 **35/6,720**, v1.2
  **35/6,720**, A17 **0/6,720** carry `completion_uis = 1.0` exactly where `1.10 × completion_cohort > 1`.
  The delivered panels were not modified (hashes `47d4b082…`, `14729c51…`, `e955f02d…`, unchanged).
- **Repaired copies (this cell):** **0/6,720** capped; the same 35 cells now carry the declared values
  `1.000258707 … 1.044677728` and the panels' max `completion_uis` is **1.044677728**.

**No observed value moves.** The three 2024 PHL completion values (`98.30461883544922`,
`92.4139633178711`, `75.02525329589844`), every `T`, every `T_min`/`T_max`, every crossing year, the
`level GER end years` (2018) and `ger_secondary` 2024 (`85.2945085684493`) are untouched.

---

## 7. What does not change

- **The observed record and the register's `T`**: 18/18 register rows and 90/90 detail rows identical
  (except the governing-predecl provenance column, declared above); 12-cell counts **4 / 6 / 2**;
  6 crossing cells; 6 `NO-COMPLETION-SERIES` (HKG/JPN); overall verdict **`REGISTER-BINDING`**.
- **A17**: panel byte-unchanged; m-constancy `CONSTANT` 8.8395202269e-10.
- **The five countries / primary-only incidence** of the cap; the uncapped max 1.044677728.
- **All thresholds** (band `[0.85, 1.15]`, share `≥ 0.80`, range `≤ 0.30`, `THIN < 3` pairs, `1e-9`),
  **all parameters**, the seed `20261120`, the draw order, the `%.10g` format.
- **All other clamps**: CAP-02 (declared `comp_coh` clip), CAP-06 (declared GER/Z1 gate), CAP-07/08/09
  (capacity), CAP-18/19 (renormalisations), CAP-15/16/17/21/22/23/24 — untouched.
- **`m = 1.10` remains a point convention, not a level conversion.** The fix makes the model identity
  `CONSTANT` on all panels; it does **not** make the observed completion/GER relation constant (that
  relation is measured `NOT-INTERCHANGEABLE` in 6 of 12 cells and crosses 1.0 in 6). D160's conclusion
  that a single constant conversion cannot carry a level claim **stands and is reinforced**.
- **The gate-passed write-up** `10_massification/lit/PHASE_WRITEUP.md`: not written by any code path in
  this cell; sha256 `d0820eb8311c315d…` recorded before and after the run (unchanged).

---

## 8. Checks and falsifiers (pre-declared)

| id | test | result |
|---|---|---|
| T1 | repaired vs delivered: same header/rows; only `completion_uis` differs; exactly 35 cells; each `= 1.10×coh` and `> 1` | **PASS** (v1.3 and v1.2; 35 each; 0 value mismatches) |
| T2 | m-constancy at `1e-9` on repaired v1.3, repaired v1.2, A17 | **PASS** — all `CONSTANT` (9.6646846082e-10 / 9.6646846082e-10 / 8.8395202269e-10) |
| T3 | cap-induced vs real: repaired deviation ≤ `1e-9` with uncapped max unchanged | **PASS** — 9.6647e-10; uncapped max 1.044677728 unchanged |
| T4 | register invariance: every field except m-constancy identical; counts unchanged | **PASS** — counts 4/6/2 identical; detail 90/90, system 6/6 identical |
| T5 | two runs byte-identical | **PASS** — 12/12 artifacts (`DETERMINISM.json`) |
| T6 | delivered inputs unchanged before/after | **PASS** — 12/12 unchanged (incl. write-up, parent predecl, CAP AUDIT) |
| A1 | AMENDMENT 1 / audit §5 item 4: repaired capped cells vs GER | **PASS / measured** — 0 of 70 with CR > GER; all 70 CR ≤ the model's own GER (105.0); CR−GER −4.9741293…−0.5322272 pp |

**No falsifier tripped. No FAIL, no MIXED.** Nothing was tuned.

---

## 9. Notes for the Lead / Council (text, not re-execution)

1. **The parent DEBUG contract's phrase "the cap masks the real non-constancy" is superseded.** There is
   **no residual real non-constancy** above `1e-9`: the entire 4.7043695535e-02 was the ceiling (b). The
   correct statement is that the cap *created* the apparent non-constancy, not that it masked one.
2. **D164 C-1 ("`CONSTANT` is A17-only")** remains valid as a citation condition on the **delivered**
   `M_CONSTANCY.csv`; under the repaired object `CONSTANT` holds on all three panels. A prospective
   amendment would restate it per panel.
3. **CAP-04 (survival floor 0.02, 24 tertiary burn-in cells) is recorded, not fixed.** It is undeclared,
   it binds 24/6,720 cells on all three panels (1970–1972, tertiary), and it is upstream of the completion
   object. It is **not** the named defect and this licence does not reach it. It remains to be adjudicated
   before any level sentence is called clean.
4. **CAP-14 / CAP-20** (non-binding guards, 0 cells): recorded by the audit, no action.
5. The repaired panels are a **DEBUG diagnostic object**, not a delivered panel, not a replacement, and
   not a reproduction claim. The closed `v1.5`–`v1.7` line stays closed; no successor generator is
   predeclared.
6. **Provenance note:** the parent contract carries **AMENDMENT 1** and hashes
   `7d8bade95407a2fe76c95a740e0c98a74f34962117b33846df37a7d6a48f56a9`. `CAP_AUDIT.md` records both
   this amended hash and the dispatch hash `748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553`
   and states that the contract was amended mid-audit; both files were hashed before and after this run
   and are unchanged (12/12 delivered inputs unchanged). This cell binds to the amended contract and
   applies the measure-aware reading throughout.
7. **A17's frozen v1.6 copy was not repaired.** The audit's "at minimum" list includes
   `generator_v1_7_partrepair/code/frozen/sim_v1_6_repair.py:1318`, but **0 cells bind there**, the A17
   panel is the comparison object and must stay frozen, and this cell's write scope names the v1.3 and
   v1.2 copies. Repairing it would produce a byte-identical A17 panel (0 cells bind), so the re-run is
   unaffected; the choice is disclosed rather than hidden.

---

## 10. Files and reproduction

```
code/sim_v1_3_fix.py            repaired v1.3 copy (2 hunks: path block + CAP-01)
code/sim_v1_2_fix.py            repaired v1.2 copy (2 hunks: path block + CAP-01)
code/run_repaired.py            generator driver (same call as delivered main())
code/uncap_cells.py             CAP_FIX_CELLS.csv + CAP_FIX_SUMMARY.json
code/verify_identity.py         in-memory identity check
code/run_conv_reg_repaired.py   delivered register runner, reused verbatim except: input substitution,
                                DEBUG cell label, and an added re-hash of the delivered threshold predecl
code/run_all_debug.py           two-run orchestrator + determinism + unchanged-input guard

results/panels/synthetic_panel_v1_3_repaired.csv
results/panels/synthetic_panel_v1_2_repaired.csv
results/CAP_FIX_CELLS.csv       35 cells x 2 panels, before/after + GER measure columns
results/CAP_FIX_SUMMARY.json    counts, maxima, column-diff proof
results/REPAIRED_CONV_REG.csv   repaired register (18 rows)
results/REPAIRED_M_CONSTANCY.csv
results/CONV_REG.csv            same bytes as REPAIRED_CONV_REG.csv
results/CONV_REG_DETAIL.csv     CONV_REG_SYSTEM.csv
results/VERDICT.json            results/console.txt  results/INPUT_HASHES.json
results/IDENTITY_CHECK.json     results/DETERMINISM.json  results/INPUT_HASHES_DEBUG.json
determinism_run2/               second run of everything
```

Reproduce (deterministic; ~85 s):

```
"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" \
  code/run_all_debug.py --run1 results --run2 determinism_run2
```

Everything in this cell is `DEBUG`; inherited `SYNTHETIC` / `OBSERVED` / `DERIVED` labels are preserved.
No web, no server interaction, no writes outside this directory.
