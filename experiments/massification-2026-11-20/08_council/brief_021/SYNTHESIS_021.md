> **SYNTHETIC EXERCISE — COUNCIL-2 SYNTHESIS (brief 021, cycle 13).** Panelists are AI-constructed composite
> personas; nothing here is a statement by any living person. This is a **research-direction ruling, not evidence**.
> Write scope `08_council/brief_021/` only; append-only. **No bridge post** (D87); **no external message**.
> No model code was executed in this session — every number below was re-derived arithmetically from the delivered
> CSVs and is listed with its path in §1.

# SYNTHESIS 021 — WT/DT adjudication, the SR-9 authority ruling, and five anchored experiments

**Batch adjudicated.** `10_massification/extensions/wt_2026-11-20/` (predecl sha256 `d3ad365e…`) and
`10_massification/extensions/dt_2026-11-20/` (predecl sha256 `6ed67b82…`); both predeclared before execution;
both deterministic on re-run (verified, §1).

**Also read and ruled on.** `generator_v1_2/FINDINGS.md` + `TUNE_LOG.md` (the conditional A–E PASS record); the
v1.2.1 NER addendum in flight (`generator_v1_2_addendum/`, predecl frozen 22:55, results 22:56–22:57, **no manifest/
FINDINGS/SHA256SUMS yet**); `shadow_module/PRE_DECLARATIONS.md` + `PRE_DECLARATIONS_S1_NOTE.md`; and the full HKG
package (`hkg_transfer_2026-11-20/`, predecl sha256 `99be01d7…`, checklist SR-1/SR-2/SR-9).

---

## Step-back (mandatory, per BIG_PICTURE_RULE.md)

1. **First-order goal, one sentence.** A longitudinal model in which *massification/universalization* is produced by
   **schooling, government and markets each standing the others up**, with cohort flows and country/sector variation,
   that reproduces **which** PHL milestones crossed and **when** (floor and middle yes, upper-secondary ceiling no) —
   and then, as a **diagnostic only**, HKG's primary-NER timing; shadow secondary.

2. **KEEP / PARK / KILL (delta vs cycle 12).**
   - **KEEP** — synthetic **v1.2** (W1), now with its **conditional record** (§2.6) and with **CEIL-ATTRIB** (EXP-1)
     as its validity gate; the **A3 demand-signal block** (now the build target); the **W2 shadow module** (frozen,
     ranks #4); the **HKG package** (authority now conditional — §3); the **A1 write-up**; **M/V** (still not executed —
     see drift).
   - **KEEP-NEW** — the **measurement line** (NER construct, `m`/denominator, provenance). It is new because both the
     batch and the model record turned on measurement this cycle.
   - **PARK** — the two papers (already PARKED by D99/D102 and now by the closed gates D106/D107); the exit-cost layer;
     the induction grounding; **portability execution** (authority granted but gated — §3); **DT3** (HELD).
   - **KILL** — re-running or re-scoring any WT/DT cell; any further paper-test slate this phase; using **WT4** as
     evidence for the paper; stacking a demand or shadow layer on v1.2 **before** CEIL-ATTRIB attributes the current
     ceiling; treating the cohort-flow NER as the UIS stock NER; the "now theory-grounded" label in
     `MODEL_ARCHITECTURE.md` Amendment A4 (it contradicts D104's binding gate #2 — §2.6).

3. **The one thread that most advances the model.** **The v1.2 → v1.3 demand-at-gates build, entered through
   CEIL-ATTRIB.** Before a demand layer (A3) or a shadow layer (W2) is stacked on v1.2, establish *which declared block
   carries the current upper-secondary ceiling* — the mechanism (quality/household demand), the calibration/measurement
   (`m`, build-out timing), or the lower-secondary pipeline. Everything else this cycle is either a **gate** on that thread
   (measurement, HKG) or **paper-side closure**.

4. **Drift check.** Three red flags.
   - **R1 — paper-test treadmill.** Two consecutive results cycles (WT, DT; ten cells) spent on candidate theories;
     both conditional gates closed null; none of the ten touch the model's critical path, and the cycle-10 Z1–Z5
     slate has **no separate delivered artifact** (no Z directory under `10_massification/extensions/`); its
     validity-gate idea survives only as the synthetic v1 check F, not as the M/V re-specification it was meant to be.
   - **R2 — knife-edge laundering.** v1.2's PASS rides on `m = 1.10` (admissible window ≈ 1.09–1.11) and on
     design-phase calibration; an **armed** HKG port would sit on top of it.
   - **R3 — measurement-defect recurrence.** WT2 (unit mismatch), DT4 (non-monotone depth proxy), WT5 (cross-year
     ratio — originating in **this Council's own block**), and v1.2 FINDINGS §1.2's "1.136 (upper 2018)" (also
     cross-year — §2.6) are **four instances of one error class in two cycles**.
   **Red-flag count: 3** → D11 requires kill or a written critical-path justification. **Justification (recorded):**
   the phase verdict is locked (D76/D77) and no on-disk test can change it; therefore the Council's authority is spent
   only on (a) the live model line (CEIL-ATTRIB → v1.3), (b) measurement, (c) the write-up. The **paper-test series is
   terminated** with this batch; the drop-first of the new five is the paper-side kill-test. No closed claim reopened;
   no battery re-run; no model code run to rescue anything.

5. **If only one thing mattered this week:** **CEIL-ATTRIB** — it decides whether v1.2's ceiling is a mechanism result
   at all. **Drop-first of the five: ASYM-K** (paper-side; cannot unlock D101 even if positive).

---

## 1. What arrived, and what was actually verified

| item | source file | check | result |
|---|---|---|---|
| WT predeclaration hash | `wt_2026-11-20/PRE_DECLARATIONS.md` | sha256 | `d3ad365e7a0f…` — **matches** manifest |
| DT predeclaration hash | `dt_2026-11-20/PRE_DECLARATIONS.md` | sha256 | `6ed67b82be1f…` — **matches** manifest |
| HKG predeclaration hash | `hkg_transfer_2026-11-20/HKG_TRANSFER_PRE_DECLARATIONS.md` | sha256 | `99be01d7…` — **matches** checklist |
| WT determinism | `wt_2026-11-20/results/` vs `_determinism/run_b/` | sha256 on both CSVs | byte-identical (`92b4323f…`, `5bfb933f…`) |
| DT determinism | `dt_2026-11-20/results/run1` vs `run2` | sha256 on both CSVs | byte-identical (`e28935ac…`, `e0e263d3…`) |
| WT1 aggregates | `wt_2026-11-20/results/DETAIL.csv` | recount `fall_run`/`rise_run` rows | **264** rise / **117** fall = **0.443182**; medians **11.128309** / **6.686363** = **0.600843** |
| WT1 heterogeneity | same | zero-fall series | **42/96** — matches FINDINGS |
| WT3 Spearman | `DETAIL.csv` (`P1×C1`) | independent rank-residual recomputation | raw **+0.072527**, income-partial **−0.520072** — matches to 6 dp |
| WT4 PHL series | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | read 11 observed values | 2017 **76.432953**, 2022 **68.276512**, 2023 **71.929314**, 2024 **75.025253**; drawdown **8.156441** |
| WT4 tertiary | same | read series | 2016 **38.344741**, 2018 **28.116623** (−10.228), 2025 **51.071883** |
| WT5 ratios | `04_data/TARGETS_SHADOW.csv` | recompute | 85/45 = **1.888889** (cross-year); 40/45 = **0.888889** (1996 same-year); 85/72 = **1.180556** |
| DT1 | `dt_2026-11-20/results/DETAIL.csv` | read headline | median partial **+0.014610**, raw **+0.386690**, **2/5** ≥ 0.40, n **91/5** |
| DT2 | same | read models | `E_entrant` **+1.605375** (p **0.000359**); `gap0` **+0.326706** = **0.204×**; D1 **1.654508**, diff **2.22e−16** |
| DT4 | same | read headline + country rows | partial **+0.202294**; top **10/11**, bottom **2/11**; sensitivity **−0.071034** |
| DT5 | same | read headline + regression | joint **14/24 = 0.583333**; PHL residual z **−0.507831** |

**Five new findings from the verification (all corrected in the record, §2.6):**

- **N1 — WT1's depth failure is not an aggregation artefact.** Equal-weighting the five indicators instead of pooling
  gives a median count ratio **0.333** (passes) and a median depth ratio **0.590** (still fails 0.50). The null survives
  the obvious robustness check; the *substantive* reading is "direction-consistent, magnitude short, indicator-dependent"
  (attainment 0.244 and tertiary 0.572 vs primary completion 0.724 and lower completion 0.607), not "the paper adds
  nothing".
- **N2 — WT2's 100% is worse than "near-vacuous".** On a common pp metric (`D_cred_pp_change_DIAGNOSTIC` vs
  `D_dest_pp_change`, both in `DETAIL.csv`), decoupling holds in **7/10**, not 10/10: KHM (19.9 vs **43.4**),
  PHL (20.3 vs **21.7**) and VNM (34.8 vs **44.0**) have the destination growing **faster** than the credential. The
  first leg is not merely easily satisfied — for three countries it points the other way.
- **N3 — WT4's fragility is real, but the FINDINGS sentence is wrong.** The frozen rule needs **≥3 consecutive
  observed years** below 71.433 (`PRE_DECLARATIONS.md:273–274`). Post-2017 observations are 2022, 2023, 2024; only 2022
  is below. "One more year at 2022 levels" gives a **2-year** run, not an episode — it would take **two** more observed
  years. The correct fragility is sharper and more damning of the pass: **2023 clears the 5 pp trigger by 0.496 pp**
  (71.929 vs 71.433) and **2024 clears the 2 pp recovery band by 0.592 pp** (75.025 vs 74.433).
- **N4 — v1.2 FINDINGS §1.2's "1.136 (upper 2018)" is not a same-year observed ratio.** Upper completion is not
  observed in 2018; 1.136 = **75.025 (upper completion 2024) ÷ 66.046 (upper GER 2018)** — the same cross-year class as
  WT5. The admissible same-year ratios are **0.925** (primary 2017), **0.901** (lower 2017), **1.094** (upper 2017),
  **1.045** (primary 2024). Separately, `completion/GER` is **not** the quantity `m` converts (m maps the model's
  cohort-flow completion to the UIS convention), so the `m = 1.10` justification is analogical, not arithmetical. The
  declaration survives as a convention; the justification must be restated as such.
- **N5 — `MODEL_ARCHITECTURE.md` Amendment A4 contradicts D104.** The A4 table labels Amendment A1 and A3 "now
  **theory-grounded** by assembly §3.2" / "declared assumption, theory-grounded". D104's binding gate #2 says that when
  either DT1 or DT2 is null the assumptions keep their "declared" label **with no theory citation**. DT1 is null. The
  A4 rows must be corrected to "candidate grounding — **PARKED** per D104 (DT1 null); no theory citation" before the
  next model run.

---

## 2. Battery adjudication

**One-line ruling: all ten recorded verdicts are correct as predeclared; the defects are in *what the tests can
support*, not in the arithmetic or the rule application.** Both dispositions are **ACCEPT** — no cell is re-executed;
the only RETURNs are record corrections (§2.5).

### 2.1 WT battery — verdicts and readings

| cell | recorded verdict | ruling on the verdict | ruling on the reading |
|---|---|---|---|
| **WT1** | NOT SUPPORTED | **CORRECT** (depth 0.601 > 0.50; falsifier is "either ratio > 0.5") | Direction is as predicted (count 0.443, depth 0.601); magnitude short. The block's binary negative arm ("the paper adds nothing") **over-reads a margin miss** — record the qualified reading (N1). |
| **WT2** | NOT SUPPORTED | **CORRECT as predeclared** (falsifier fired: 4/10 > 1/3) | **VOID as a test of the paper.** Unit mismatch (N2) and the reversal leg counts *dips*, not exits (PHL's 2018 tertiary dip recovers to 51.07 by 2025). **Neither "no footprint" nor "reversibility" is licensed.** The question is untested. |
| **WT3** | NOT SUPPORTED | **CORRECT** (income-partial −0.520; sign flip) | Correct and sufficient: Y1 lesson repeats (raw 0.429 for the alternative pair absorbed to 0.046). The saturation-ceiling artefact critique is right. |
| **WT4** | SUPPORTED (descriptive) | **CORRECT as predeclared** (zero episodes; tertiary recovery observed) | **Near-tautological** — a ceiling that never approaches 90 cannot produce a 5 pp-below-peak exit. The fragility is **understated and mis-stated** (N3). May not travel as evidence for the paper. |
| **WT5** | DESIGN-ONLY / NOT SCORED | **CORRECT — the worker's refusal to score is exactly right** | The 1.889 is cross-year; the one same-year primary+senior pair on disk (HKG 1996, 40/45) shows **no gradient (0.889)**. The 2003/2010 gradients are **within-secondary** (2.003, 1.181) and cannot substitute. **The error originated in brief 019's block — this Council's own** (§2.4). |

**Named defects, WT battery:** (W1) WT2's decoupling leg is unit-incoherent and its reversal leg does not operationalise
"adoption does not reverse"; (W2) WT4's FINDINGS sentence "one more year … would flip it" is false under the frozen rule
(N3) and understates two sub-1-pp margins; (W3) WT5's cross-year ratio is a **Council-side** authoring error. None of the
three changes a verdict word; none is a reason to re-run.

### 2.2 DT battery — verdicts and readings

| cell | recorded verdict | ruling on the verdict | ruling on the reading |
|---|---|---|---|
| **DT1** | NULL (negative) | **CORRECT** (median partial 0.0146 < 0.40) | Real but **thin**: 5/30 countries, 91 country-years; eligibility selects on data availability. Scope the reading to "on this 5-country overlap". |
| **DT2** | NON-NULL (support) | **CORRECT** (+1.6054, p = 0.00036; `gap0` = 0.204×) | Correct, and the discriminating part (income-controlled survival + `gap0` subordination) is what passed. **Partly arithmetic** (cohort replacement) — label stands. It is the batch's one descriptive support; it does **not** satisfy D104 alone. |
| **DT3** | UNABLE (HELD) | **CORRECT** | No number, no fabrication. |
| **DT4** | NULL (falsifier) | **CORRECT as predeclared** | **NOT a falsification of Prediction 5.** The depth proxy is a product of two z-scores and is non-monotone: **COL** (completion mean 106.556) has depth **−1.574** (bottom half); **LAO** (81.116) has depth **+0.291** (top half); `corr(depth, z_cmpt) = 0.356`. The proxy does not order countries by "installation depth". Relabel **NULL-BY-CONSTRUCTION / uninformative**; a re-specified depth index is a new predeclaration, never a rescue. |
| **DT5** | NULL (falsifier) | **CORRECT as predeclared** (joint 58.3% passes; PHL z −0.508 > −1.0) | Near-circular; PHL's WDI 2021 attainment break mechanically triggers the reversal rule. The cross-sectional result does not address the **time-series** residual (D63). No re-score of WT2/WT4. |

**Named defects, DT battery:** (D1) DT4's operative proxy fails a measurement-validity precondition — the falsifier is
a construction artefact; (D2) DT1's null is coverage-thin and must be scoped; (D3) DT5 is near-circular and its PHL
series break is recorded, not repaired. None changes a verdict word; none is a reason to re-run.

### 2.3 Are the two PARKs correct? — **Yes, both, with one nuance each**

- **D101 gate (exit-cost/complementarity):** requires **WT1 AND WT3 both non-null**. WT1 NOT SUPPORTED ∧ WT3 NOT
  SUPPORTED → **gate not met → PARKED. Correct.** Nuance: the paper is **not footprintless** — it has one consistent
  descriptive corollary (WT4) and a direction-consistent, magnitude-short count leg (WT1 = 0.443). The honest label is
  *"no demonstrated footprint for the defining mechanism; one consistent descriptive corollary and one direction-
  consistent margin miss."* Do not upgrade it; do not erase the corollary.
- **D104 gate (induction grounding):** requires **DT1 AND DT2 both non-null**. DT1 NULL ∧ DT2 NON-NULL → **gate not met
  → PARKED. Correct.** Nuance: the asymmetry is itself a result — the paper's self-declared *most diagnostic* test
  passed (DT2), its cheapest failed on coverage (DT1). Record that as a descriptive footprint **in the cohort
  decomposition**, not as a grounded mechanism. The conjunction rule binds as written; no re-interpretation to open it.
  **Compliance fix owed:** N5 (A4 label) must be corrected; "now theory-grounded" is exactly the citation D104 bars.

### 2.4 WT4 fragility and WT5 cross-year error — addressed

**WT4 (the only SUPPORTED cell).** Zero exit episodes is correct as predeclared, but the pass rests on two sub-1-pp
margins (N3) and is near-tautological given the known non-response. Two further checks strengthen the reading:

- **Provenance is homogeneous.** Every PHL completion observation in `UNIVERSALIZATION_SERIES.csv` carries
  `source = UIS_SDG4_2026_11`, `vintage = UIS SDG4 release 2026-11`, `status = observed` — so the 2017→2022 dip is **not**
  a vintage splice. It is a real feature of this release.
- **The pass is not an exit-cost result.** A 5 pp-below-peak definition cannot detect an "exit" from a ceiling that never
  rises to the gate; WT4 confirms non-response, not the paper's mechanism. It stands; it does not travel.

**WT5 (the cross-year ratio).** The 1.889 is 2010 senior-secondary (85) ÷ 1996 primary (45) — different years, different
survey frames. The only same-year primary+senior pair on disk is HKG 1996 = **40/45 = 0.889** — **no gate gradient**. The
2003 stage gradient (S1-3 35.1 → S6-7 70.3 = **2.003**) and the 2010 lower→senior gradient (**1.181**) are
**within-secondary**, not primary→senior, and cannot satisfy the block's support clause. **The defect is ours, in
brief 019's WT5 block**, not the worker's; the NOT SCORED handling is accepted in full. **Process rule adopted (D?):**
every number in a new anchoring block must be re-derived from disk **before** the predeclaration is frozen; a block
number that cannot be reproduced from a named file+row is a blocking error.

### 2.5 Disposition (per battery)

| battery | disposition | record corrections (no re-execution) |
|---|---|---|
| **WT** | **ACCEPTED** — verdicts stand; predeclaration, determinism and all-cells reporting verified | WT4 FINDINGS sentence corrected (N3); WT2 annotated **VOID / no interpretive weight**; WT5 recorded as a **Council-side authoring error**, design-only stands |
| **DT** | **ACCEPTED** — verdicts stand; predeclaration, determinism and all-cells reporting verified | DT4 relabelled **NULL-BY-CONSTRUCTION / uninformative**; DT1 coverage caveat scoped; DT5 near-circular + 2021 break recorded |

**No cell is RETURNED for re-execution.** The only RETURNs are record items (two WT, one DT) to the record owner for
correction before the Lead merges.

### 2.6 The v1.2 conditional record (adjudicated here because it gates SR-2 and the HKG ruling)

`generator_v1_2/FINDINGS.md` + `TUNE_LOG.md` disclose: (i) check (a) is scored on the UIS-convention series with one
declared `m = 1.10`; (ii) the admissible window is ≈ **1.09–1.11** (m = 1.05 → primary 2022 FAIL; m = 1.12 → upper
**78.03** FAIL); (iii) the cohort-flow series would fail (a); (iv) the parameters were calibrated in the design phase;
(v) the upper ceiling is **demand/quality-driven**, not boom-driven (flat-cohort 2024 = **73.2**, never ≥ 90). **Ruling:**
checks A–E **PASS CONDITIONAL** is the correct and only honest label; "v1.2 passes its PHL checks" may not be written
without the condition. Corrections owed: (N4) restate the `m` justification as a **convention**, not an observed ratio;
delete/repair the 1.136 entry. (N5) fix the A4 table label. Neither correction changes a v1.2 check value.

---

## 3. SR-9 ruling — HKG run authority

### 3.1 What the three stop rules say now

| gate | state at ruling time |
|---|---|
| **SR-1 (measure)** | The frozen v1.2 model has **no NER object**. The v1.2.1 addendum has produced a **draft** NER column (results 22:56–22:57) but (**a**) it is not a delivered artifact — no `RUN_MANIFEST.json`, `FINDINGS.md`, `SHA256SUMS`, determinism note; (**b**) its own §2.1 declares the object a **cohort-flow NER analogue, not the UIS stock NER**; (**c**) the smoke test shows the analogue is **non-monotone** (SYN00_PHL_LIKE primary: first-at-or-above 90 in **1970**, first-sustained 5 y **2007**, minimum **75.14 in 1978**, **11** decreases). The crossing rule is predeclared (5-year sustained), but the object is noisy at the threshold. → **SR-1 remains BLOCKED-MEASURE at the construct level.** |
| **SR-2 (PHL precondition)** | v1.2 checks A–E **PASS CONDITIONAL** (§2.6): `m = 1.10`, window ≈ 1.09–1.11, design-phase calibration, ceiling demand/quality-driven. → **SR-2 is CONDITIONAL, not unconditional-clear.** **Path defect:** the checklist's SR-2 test reads `synthetic_2026-11-20/v1_2/`, which still holds only `PRE_DECLARATIONS.md`; the delivered code/results are in **`generator_v1_2/`** (`code/sim_v1_2.py`, `PARAMS.md`, `results/reproduction_checks_v1_2.csv`). The frozen HKG predecl's §5a ("its code does not yet exist") is therefore stale. A **status note** (not an edit to the frozen predecl) must fix the path before the gate check is trusted. |
| **SR-9 (authority)** | No Council decision after D75 authorises the run. → **this ruling supplies it, conditionally.** |

### 3.2 Ruling: **AUTHORISE-WITH-CONDITIONS**

**Authority is granted; execution is gated on H1–H6 below.** The grant is not a finding that the run will be
informative, and it does **not** clear SR-1 or SR-2 by itself. If **H1** fails, this authorisation is **VOID for the
current NER object** and the run is `BLOCKED-MEASURE(SR-1)` — not "deferred pending a new decision".

### 3.3 The conditions (all must hold before any command in checklist §5 is executed)

| # | condition | test / evidence |
|---|---|---|
| **H1 — measure admissibility (clears SR-1 at the construct level)** | The NER **construct-equivalence test** (EXP-3) must return **ADMISSIBLE**: the stock reconstruction and the cohort-flow analogue differ by **≤ 2.0 pp** in every year where the analogue is in the 85–95 band, **and** the implied first-sustained crossing years differ by **≤ 1 y**. Crossing definition fixed as **first sustained 5-year crossing** before the comparison. | EXP-3 result file; if FAIL → `BLOCKED-MEASURE(SR-1)`, authorisation void |
| **H2 — delivered addendum + SR-2 path** | The v1.2.1 addendum must be a **delivered** artifact: frozen predecl hash, `RUN_MANIFEST.json`, `FINDINGS.md`, determinism note, `SHA256SUMS`, two byte-identical runs. The SR-2 gate must also carry a **status note** correcting its path to `generator_v1_2/` (the checklist still reads the predecl-only `v1_2/`); the frozen predecl is not edited. | checklist §2 pre-run verification; manifest; status note |
| **H3 — SR-2 recorded as PASS-CONDITIONAL** | The port meta must carry `m = 1.10` **with** the 1.09–1.11 window, the m = 1.05 / 1.12 failure points, the design-phase calibration disclosure, and "ceiling demand/quality-driven, not boom-driven". No HKG file may say "v1.2 passes". | text audit of `results/hkg_declared_inputs.csv` + run meta |
| **H4 — D7–D9 anti-leak** | Every D7/D8/D9 declared value must cite an **on-disk observed** HKG series, or be marked `DECLARED` with a rationale that **does not reference 1974/1979**; every value hashed **before** the run; PA-1/PA-2 audits must show **zero** post-hoc change. A D7–D9 value chosen with the target years in view = `FAIL-RE-FIT`. | `results/hkg_declared_inputs.csv` + PA-1/PA-2 |
| **H5 — D75 six constraints + banner + closed verdict set + asymmetric-information disclosure** | §3.4 and §3.5 restated verbatim in substance. Every file carries `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`. FINDINGS must state that **TRANSFER-FAILS is the informative outcome** and TRANSFER-HOLDS is **weakly** informative, because D9 delivery pace can place the crossing. | PA-5/PA-6 grep audits |
| **H6 — scope** | Timing-only; primary NER only; 1974/1979 only; ±5 y; no completion series for HKG; no level in the verdict; no claim about HKG, portability, capacity-timing, or the phase verdict; D63/D76/D77 untouched. | predecl §2–§4; FINDINGS limits section |

### 3.4 The D75 six constraints (restated)

- **(i)** Fixed PHL behaviour/parameters; **only declared country inputs re-set** (R20).
- **(ii)** **No re-fit, no extra free parameters, no target fitting** — any occurrence = **FAIL**, and the moved
  parameter must be named.
- **(iii)** HKG **timing-only, levels check-only**; targets **NER ≥ 90 in 1974**, **NER ≥ 95 in 1979**;
  threshold-specific; **never spliced**.
- **(iv)** CHN (the other portability arm) only with censoring rules and the 1986-law **−27 y** miss reported as is.
  *Not triggered by an HKG-only run; restated because D75 is the governing decision.*
- **(v)** The **standing scaling FAIL** is printed in every table.
- **(vi)** Verdict vocabulary **DIAGNOSTIC-TRANSFER only** — `TRANSFER-HOLDS` / `TRANSFER-FAILS` / `FAIL-RE-FIT`;
  **never `PASS`**; and the predecl must say **what it would change** given the anchor's own misses.

### 3.5 Standing label and verdict set

```
SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE
```

Closed verdict set: `DIAGNOSTIC-TRANSFER: TRANSFER-HOLDS` · `DIAGNOSTIC-TRANSFER: TRANSFER-FAILS` ·
`DIAGNOSTIC-TRANSFER: FAIL-RE-FIT` · `BLOCKED-*(SR-n)` (terminal state, **not** a verdict). `PASS`, `SUPPORTED`,
`NOT SUPPORTED`, `REPRODUCED`, `VALIDATED`, `CONFIRMED`, `PORTABLE`, `HOLDS` remain **forbidden strings** in every HKG
output file. A split result is `TRANSFER-FAILS`, with both errors reported.

### 3.6 What the run would and would not license

| outcome | licenses | does **not** license |
|---|---|---|
| **TRANSFER-HOLDS** | "Under the frozen PHL parameterisation and the declared HKG inputs, the model places the two primary NER crossings within ±5 y of the recorded years." A statement about the **simulator's timing behaviour**. At most it justifies (not compels) a later **proposal** to re-fit the anchor against a cross-system timing criterion — which would itself need a new decision + predecl. | portability (R22); evidence about HKG; an anchor upgrade; a phase-verdict change (D76/D77); "capacity explains timing" (D61/R28); any direction/causal claim (R13). |
| **TRANSFER-FAILS** | "The timing error recurs on a second, high-capacity system", strengthening the existing reading that the anchor's timing misses are a **model-class** property. Note-only. | everything above; plus any claim about HKG's history or about the papers. |
| **FAIL-RE-FIT** | nothing — the run is **void as a diagnostic**; the moved object and its before/after value must be named. | any verdict. |
| **BLOCKED-*** | nothing — **no diagnostic was produced**. Never reported as a result, never described as a model or HKG failure. | any verdict. |

**In one line:** *no outcome of this transfer can change the closed phase verdict, and none may be reported as if it
could.*

### 3.7 What would clear the authority later, and what voids it

- **Clears:** H1–H6 satisfied, plus a checklist §2 hash verification and the SR-7 determinism gate.
- **Voids:** any of the six D75 constraints; any H1–H6 failure; a D7–D9 post-hoc change; a measure substitution (GER or
  completion for NER); a widened tolerance; a second run that differs.

---

## 4. The five anchored experiments (D89 standing order)

**Slate (info-gain order):** CEIL-ATTRIB **#1** · A3-D **#2** · M1-NER **#3** · A3-S **#4** · ASYM-K **#5 /
DROP-FIRST**. All are on-disk or frozen-object work; none re-runs a WT/DT battery; none is a toy; none reopens C1–C4;
none makes a direction claim. **Drop-first: ASYM-K** — paper-side, the exit-cost thread is PARKED, and even a positive
cannot unlock D101 (which needs WT1 ∧ WT3). It can only confirm a negative; that is the definition of a rabbit hole.

### EXP-1 — CEIL-ATTRIB: which account carries the PHL upper-secondary ceiling? (rank **#1**)

1. **First-order channel link.** **Schooling + cohort flows + markets** — locates the ceiling in one of three channels:
   the lower-secondary **pipeline** (cohort flow), the upper **gate/demand** (schooling × markets), or the **calibration/
   measurement** (`m`, build-out timing). One sentence: it asks whether the D63 residual is an upper-level phenomenon at
   all.
2. **What changes if positive vs negative.** Predeclared three-account decision matrix (fixed before the run):
   (a) *pipeline-consistent* (Test B) → the residual is **reclassified** as lower-pipeline inheritance; D63 stays
   **UNABLE as to cause**, but the object moves from "upper gate" to "lower pipeline"; no demand/exit-cost claim.
   (b) *mechanism-carried + gate-loss* → v1.2's demand/quality block earns its place as the **candidate account** (still
   UNABLE as to cause). (c) *calibration-carried* → v1.2's ceiling claim is **withdrawn as a mechanism result** (it is a
   calibration artefact). (d) *mixed* → undetermined; no claim, no re-tuning.
3. **Why it is not a niche.** The ceiling is the phase's single open object (D63); WT4 — the only SUPPORTED cell in the
   batch — rides on it; v1.2's central claim is that it *generates* the ceiling. A reader of the first-order question
   cares whether "the ceiling" is a gate, a taste parameter, or arithmetic.
4. **Data on disk.** Frozen `generator_v1_2/code/sim_v1_2.py` + `results/synthetic_panel_v1_2.csv` (sha in the manifest);
   declared in-memory ablation switches (**the scored run is unchanged** — ablations are declared variants, as in
   `FINDINGS.md` §2); PHL `completion_upper_secondary` / `completion_lower_secondary` from
   `10_massification/data/UNIVERSALIZATION_SERIES.csv` (11 observed each); `SE.SEC.DURS` / `SE.PRM.DURS` from
   `09_relations/data/panel_wdi_long.csv` for the lag. No DATA ASK.
5. **Numeric threshold + falsifier.** **Test A (ablation):** ceiling is **mechanism-carried** iff ≥ 2 of {γ = 0;
   household work incentive off; flat cohort} move upper UIS 2024 by **≥ 2.0 pp**, while {m sweep 1.05/1.10/1.12;
   build-out timing ±5 y} move it by **< 1.0 pp**. **Calibration-carried** iff m or build-out moves it by **≥ 2.0 pp**
   while the mechanism ablations move it by < 2.0 pp. **Test B (pipeline):** with a declared **3-year lag** (±1 y
   nearest observation; 2 and 4 y as sensitivity, not verdict-changing), **pipeline-consistent** iff
   `upper_t / lower_{t−3} ∈ [0.90, 1.10]` in **≥ 2/3** of observed pairs; **gate-loss** iff `< 0.90` in ≥ 2/3.
   **Falsifier:** a "mixed" outcome (neither test reaches a bar) → record **UNDETERMINED**, no claim.
6. **Closed-claim check.** No C1–C4 reopening; no re-fit of v1.2 (ablations only); **D63 is not "explained"** —
   only reclassified; WT4 is not re-scored; no direction claim (R13-safe).
7. **Cost / rank.** **Medium. Rank #1.**

### EXP-2 — A3-D: demand-signal core implementation (v1.3 Layer 2c) (rank **#2**)

1. **First-order channel link.** **Markets + schooling** — the demand side: expected returns × gate probability ×
   sector structure × migration/remittances. One sentence: it converts the last declared taste parameter (the upper-secondary
   work-incentive weight) into a demand-derived object.
2. **What changes if positive vs negative.** *Positive* (d1–d3 hold, replacement robust, ablation matters) → a declared,
   ablation-tested demand block; the ceiling becomes demand-derived and v1.3 is wired. *Negative* → the ceiling stays a
   declared taste parameter; the A3 core is PARKED and no layer is added.
3. **Why it is not a niche.** It targets the generator of the ceiling and implements the user's explicit "education
   demand signals" directive. It is the difference between a model that *generates* the ceiling and one that stipulates it.
4. **Data on disk.** v1.2 panel + v1.2.1 NER panel; `generator_v1_2/PARAMS.md`; `10_massification/data/POLICY_TIMELINE.csv`,
   `JOBS_AND_MARKETS_PANEL.csv`, `STATE_CAPACITY.csv`, `UNIVERSALIZATION_SERIES.csv`. **Migration/remittance channel:**
   DECLARED / NOT-VERIFIED — `10_massification/lit/PUSH_PULL.md` records the remittance→schooling coefficient as **not
   verified**; no literature coefficient may be inserted. A measured remittance→schooling coefficient remains **HELD**.
5. **Numeric threshold + falsifier.** **d1:** +10% `E[R]` → next-level demand share **≥ +1.0 pp** in all three country
   types, sign positive in every scored cell. **d2:** gate pressure doubling (R→2R) → gate-level demand **≥ +0.5 pp**,
   and shadow demand rises more than non-gate demand. **d3:** office-biased twin's upper demand − mfg-biased twin's
   **≥ +2.0 pp** at equal graduate flow. **d6:** identities (shares in [0,1], cohort conservation, non-negative demand).
   **Discriminating replacement test:** replace the declared work incentive with `E[R] × P(advance)`, **no other
   parameter re-tuned**; ceiling is **demand-robust** iff upper UIS 2024 stays in **[73, 77]**; outside by > 2.0 pp →
   report, **do not re-tune**. **Ablation bar (D81):** with the demand block off, upper 2024 must move **≥ 3.0 pp**, else
   the block is decorative. **Falsifier:** any d1–d3 failure, or replacement outside [73, 77] by > 2 pp, or ablation
   < 3 pp.
6. **Closed-claim check.** No C1–C4; no fitted "demand parameter" (R4/R27); a synthetic PASS is **non-diagnostic unless
   the ablation fails** (D81-2); the migration channel is declared, not estimated; no causal claim.
7. **Cost / rank.** **Large. Rank #2.**

### EXP-3 — M1-NER: construct equivalence of the cohort-flow NER analogue (rank **#3**)

1. **First-order channel link.** **Schooling + measurement** — does the model's NER object measure what the HKG target
   measures? One sentence: it decides whether a DIAGNOSTIC-TRANSFER comparison is a comparison or a measure artefact.
2. **What changes if positive vs negative.** *Admissible* → SR-1 clears at the construct level; the HKG run may use the
   object with a declared caveat. *Not admissible* → the run must use a stock object or return
   `BLOCKED-MEASURE(SR-1)`; the analogue is labelled a cohort-flow analogue only.
3. **Why it is not a niche.** It is the hinge of the SR-9 authority question, D75(iii)'s "never spliced", and PA-4. Without
   it, a TRANSFER-HOLDS/FAILS would be uninterpretable (measure vs timing).
4. **Data on disk.** v1.2.1 NER panel (`admitted_official`, `cohort`, `ner*` columns — draft, on disk);
   `data/gmr_observed_6countries_1970_2024.csv` HKG NER/ANER 1971–1996 as a **construct reference only**;
   `UNIVERSALIZATION_SERIES.csv` PHL `ner_primary` (30 observed) as a second reference. No DATA ASK.
5. **Numeric threshold + falsifier.** Stock analogue = **mean of `admitted_official / cohort` over the last `dur`
   years** (declared, parameter-free). **Admissible** iff |stock − flow| **≤ 2.0 pp** in **every** year where the flow
   analogue ∈ [85, 95] **and** the implied first-sustained crossing years differ by **≤ 1 y**. **Falsifier:** > 2.0 pp
   at any such year, or a ≥ 2 y crossing difference. **Declared expected sign:** during expansion the flow analogue
   leads the stock (flow ≥ stock), so the bias, if present, makes crossings **earlier** — the direction that could flatter
   a 1974/1979 target.
6. **Closed-claim check.** No C1–C4; measurement only; does not re-score v1.2 checks; no direction claim; the observed
   HKG series is a construct reference, **not** a validation of the synthetic model.
7. **Cost / rank.** **Small. Rank #3.**

### EXP-4 — A3-S: shadow-at-gates module, W2 frozen design (rank **#4**)

1. **First-order channel link.** **Markets + schooling at the gate** — positional demand: tutoring as a signal of gate
   pressure. One sentence: it is the only place the gate-pressure channel is measured.
2. **What changes if positive vs negative.** *Positive* (c1, c2, c4a, c5, c6 hold) → the gate-pressure channel matches
   the declared ordering; W2 is wired into v1.3 as a demand signal. *Negative* → the module stays design-only; "shadow at
   the gates" has **neither on-disk (WT5) nor synthetic** footing this phase.
3. **Why it is not a niche.** The user's revived shadow direction; WT5's own conclusion is that the real test is the
   v1.3/W2 module, not a re-tabulation. A reader of the first-order question cares whether gate pressure is a measurable
   demand signal.
4. **Data on disk.** `shadow_module/PRE_DECLARATIONS.md` (frozen) + `PARAMETERS.csv`; v1.2.1 NER panel; `04_data/TARGETS_SHADOW.csv` (HKG 1996/2010, **low confidence**); `09_relations/data/shadow_gradients.csv` (HKG 2003; KOR 2023).
   **HELD:** PHL/KHM/CHN/JPN participation rates (`TARGETS_SHADOW.csv` rows `unresolved`; no imputation).
5. **Numeric threshold + falsifier.** Frozen checks: **c1** ∂D/∂lnR ≥ 0 in every scored cell **and** R→2R raises D by
   **≥ +10.0 pp** at g2 in all three country types; **c2** +25% φ raises D by **≥ +2.0 pp** at g2 in all three;
   **c3** `D_g0 ≤ 0.025` and `≤ 0.20 · D_g1` — **structural consistency only**; **c4a** `D_{HKG,g2,2020} ∈ [0.75, 0.95]`;
   **c4b** `D*_HKG − D*_PHL ≥ 0.10` and `D*_PHL − D*_KHM ≥ 0.05`; **c4c** no country-specific behavioural parameter (else
   **VOID**); **c5** identities; **c6** v1.2 panel **byte-identical** with shadow off (else **VOID**). **Falsifier:** any
   c1/c2/c4 failure → module not wired; report, no rescue.
6. **Closed-claim check.** Does **not** reopen the closed shadow incidence/mechanism claim (brief 008/D76); **c3 is
   structural, not empirical** — observed primary tutoring (PHL **23.8%** 2010; KHM **41.3%** 2012-13,
   `02_lit/SHADOW_TARGETS.csv:18,11`) contradicts it as an empirical claim and stays out of scope; no causal claim; cannot
   change D63.
7. **Cost / rank.** **Medium. Rank #4.**

### EXP-5 — ASYM-K: recovery-time asymmetry kill-test (rank **#5 / DROP-FIRST**)

1. **First-order channel link.** **Schooling + cohort flows** — the paper's return-path asymmetry, operationalised as
   *time to recover* rather than *depth* of a fall. One sentence: does a fall take longer to undo than the rise that
   created it?
2. **What changes if positive vs negative.** *Positive* → one operationalisation has a descriptive footprint; **D101
   still stands** (needs WT1 ∧ WT3), so **no layer, no gate reopening**. *Negative* → **KILL** the exit-cost reading for
   this phase (not merely PARK).
3. **Why it is not a niche.** It is the sharpest remaining on-disk reading of the paper's defining claim, and it is cheap.
   It is also the only way to close the batch's core question without re-running WT1.
4. **Data on disk.** `09_relations/data/panel_wdi_long.csv` — the same 96 qualifying series used by WT1 (n ≥ 15 observed
   years); `10_massification/data/UNIVERSALIZATION_SERIES.csv`. No DATA ASK.
5. **Numeric threshold + falsifier.** For each fall-run ≥ 3 pp that later regains its pre-fall level: **recovery
   duration** (years from trough to pre-fall level). For each rise-run ≥ 3 pp: **rise duration** (start to peak).
   **Support** iff `median(recovery) / median(rise) ≥ 1.5` **and** **≥ 60%** of matched pairs recover slower than the
   corresponding rise. **Falsifier:** ratio < 1.5 or < 50% of matched pairs → **KILL**.
6. **Closed-claim check.** No C1–C4; **cannot unlock D101 even if positive**; no direction claim; does not re-score WT1.
7. **Cost / rank.** **Small. Rank #5 → DROP-FIRST.**

### Slate table

| rank | id | title | channel | cost | verdict-changing? | drop order |
|---|---|---|---|---|---|---|
| **#1** | **CEIL-ATTRIB** | Which account carries the PHL ceiling: pipeline / gate / calibration | schooling + cohort + markets | medium | yes (reclassifies D63's location) | last |
| **#2** | **A3-D** | Demand-signal core (expected returns × gate probability × sector × migration) | markets + schooling | large | yes (converts the ceiling to a demand object) | 4th |
| **#3** | **M1-NER** | Cohort-flow vs stock NER construct equivalence | schooling + measurement | small | gates HKG (SR-1) | 3rd |
| **#4** | **A3-S** | Shadow-at-gates module (W2 frozen) | markets + schooling at the gate | medium | adds a declared module | 2nd |
| **#5** | **ASYM-K** | Recovery-time asymmetry kill-test | schooling + cohort flows | small | no (closes a PARKED thread) | **DROP-FIRST** |

---

## 5. Labels, limits, data

- **SYNTHETIC EXERCISE.** Panelists are **AI-constructed composite personas**; nothing here is a statement by any living
  person. The Council's rulings are **research direction, not evidence**.
- **No causal or direction claim** anywhere in this brief (R13); no "the paper is validated", "reproduces induction/
  hysteresis", "portability holds", or "capacity explains timing" language. Neither paper is falsification-tested by this
  programme (D105).
- **No C1–C4 reopening.** No closed claim is re-scored. The DT4 relabel is a **label correction**, not a re-verdict.
- **HELD (named, never fabricated):** credential wage-premium series (PSA FIES/LFS; WB Enterprise Surveys);
  PHL/KHM/CHN/JPN shadow participation; behavioural/reform series (DT3); annual capacity/enforcement; real per-pupil
  spending; subnational sector employment; HKG/CHN historical timing series beyond the GMR file.
- **No web, no external request, no external message** (D87). **No model code executed** in this session; verification was
  arithmetic re-derivation from the delivered CSVs (§1).
- **Numbers quoted** are from the paths in §1 or from the anchoring-block sources named in §4; any number not given a path
  is a **threshold proposed for a future run**, not a finding.

---

## 6. For the Lead's merge (BIG_PICTURE / COUNCIL_STATE delta)

**BIG_PICTURE step-back line for cycle 13:** goal unchanged; **KEEP** v1.2 (conditional) + A3 + W2 + HKG (conditional
authority) + A1 write-up + new measurement line; **PARK** both papers, exit cost, induction grounding, portability
execution, DT3; **KILL** re-scoring the WT/DT cells, further paper-test slates this phase, and the A4 "theory-grounded"
label; **one thread** = v1.2→v1.3 entered through CEIL-ATTRIB; **red-flag count 3** with the written critical-path
justification recorded; **drop-first = ASYM-K**.

**Next 3 actions (cycle 13):**
1. **Merge the decisions** (`D108` onward), record the WT/DT dispositions, and fix the three record items + the A4 label
   (N3, N4, N5).
2. **Dispatch EXP-1 (CEIL-ATTRIB) and EXP-3 (M1-NER) first** — they are the cheapest and they gate the rest; EXP-2 (A3-D)
   after CEIL-ATTRIB's attribution is in; EXP-4 (A3-S) after the v1.2.1 addendum is a delivered artifact.
3. **Hold the HKG run to H1–H6**; no checklist §5 command until H1 passes; **drop ASYM-K** unless the user asks for the
   paper thread to be reopened.

**COUNCIL_STATE one-liner:** *Cycle 13 — WT/DT accepted with named defects (verdicts stand, no re-runs; DT4 relabelled
uninformative); both gates confirmed PARKED; SR-9 = AUTHORISE-WITH-CONDITIONS (H1–H6, DIAGNOSTIC-TRANSFER only); five
anchored experiments, drop-first ASYM-K.*

---

## 7. Files written this cycle

| file | what it is |
|---|---|
| `brief_021/SYNTHESIS_021.md` | this document — step-back, battery adjudication, SR-9 ruling, five anchored experiments |
| `brief_021/PROPOSED_DECISIONS.md` | the proposed decisions in house format, placeholders `D?` (log ends at D107) |
| `brief_021/VERIFICATION_021.csv` | every number quoted in §1 with its file, the re-derived value and the match flag |

**No edits outside `08_council/brief_021/`.** No bridge post. No external message.
