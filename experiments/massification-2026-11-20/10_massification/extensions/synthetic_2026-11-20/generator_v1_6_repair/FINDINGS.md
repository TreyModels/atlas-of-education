# FINDINGS — EXP-14 **V16-REPAIR**: the repaired bimodal generator on the observed path

**`LABEL: SYNTHETIC` for every generator object; `LABEL: OBSERVED` for every PHL series; `LABEL: DECLARED` for
every behavioural assumption. This is a new cell with a new predeclaration. It is not evidence about the
Philippines or any country, it licenses no causal claim and no direction claim, it re-opens no C1–C4 claim, it fits
nothing to the known PHL outcome, and the phrase "demand falsified" is banned and not used in any paraphrase.**

- **Predeclaration:** `PRE_DECLARATIONS.md`, sha256
  **`6a554dc033828835431f65be2e5e218833fcdb56220baad8fbe53c3324e78991`**, embedded in the built code and
  re-verified before the run (26 declared-parameter checks). `PARAMS.md` sha256 `5e15dfba…`.
- **Base instrument:** frozen v1.3 code `70ae8f0e…` (verbatim copy), panel `47d4b082…`; assembled mechanically by
  `code/build_v16.py` (sha `38dd9413…`) into `code/sim_v1_6_repair.py` (sha `9c0e7998…`).
- **Verdict string:** `S0=PASS; S1=PATH-BAR-MISSED (0/33); S2=CROSSINGS-MISSED (1/3); S3=REPRESENTATION-HOLDS;
  C1=FAIL; C2=MIXED; C3=PASS; C4=PASS; C5=PASS; G1–G7=PASS; **ALL = PATH-FAILED**`.
- **Falsifier status: NOT TRIPPED.** No parameter was chosen by reference to the 17/33 bar or the `[55,85]` band; the
  A00 arm **is** byte-identical to `47d4b082…`; no undeclared within-year feedback exists. So this is the
  **negative branch** of EXP-14 §2, not a void run.
- **No file outside `generator_v1_6_repair/` was written.** (Pre-run smoke probes wrote to `/tmp` only; see TUNE_LOG.)

---

## 1. The answer in three sentences

**The repaired generator holds the coexistence and does not face the observed path: `REPRESENTATION-HOLDS` with
`PATH-BAR-MISSED` at 0/33** (bar ≥ 17/33; A00's untiered comparator is 9/33), and the crossings pass only where the
model and the record agree that no crossing happens (upper 1/3).

**The repair worked as designed and the design is what fails.** Removing v1.5's tier survival multiplier — the
obligation D134(3) demanded — recovers almost all of the collapsed level (primary 51.63 → **81.25**, lower 2024
51.57 → **74.67**, upper 44.89 → **57.41**), and the κ object now satisfies its bound in exactly the units it is
audited in; but the **tier block's own take-up margin** caps admission at **0.80** of the cohort against the frozen
block's **0.9957** applicant share, so no level can reach the record on these declared parameters.

**This is a cleaner negative than v1.5's because the object is now identified:** it is not the survival mapping, not
κ, and not the quality discount — it is the tier choice block's aggregate schooling demand plus the unfilled Tier O
places it generates, and both are reported as observables (applicant share, unfilled share) rather than hidden in a
survival exponent.

---

## 2. The scored table

| check | verdict | key numbers | threshold as frozen |
|---|---|---|---|
| **S0** construction | **PASS** | A00 = **9/33**, medians **−4.3008 / −29.4351 / −27.5857** pp | must equal EXP-7's V1 construction |
| **S1** observed path (A10) | **PATH-BAR-MISSED** | **0/33** (primary 0/11, lower 0/11, upper 0/11); medians **−16.96 / −34.89 / −39.80** pp; mean **−27.93** pp | ≥ 17/33 within ±5 pp |
| **S2** crossings | **CROSSINGS-MISSED** | primary: observed 2017, model **never** (max 81.32); lower: observed 2024, model **never** (max 78.11); upper: **neither crosses** (max 57.89) → **1/3** legs | ±5 y, 90/90/90 pp |
| **S3** representation | **REPRESENTATION-HOLDS** | unfilled Tier O ≥ 0.10 in **17/30** cells; Tier H queue ratio ≥ 1.10 in **30/30**; both in the same year **15/15**; `p4 ≤ 0.50` in **15/15**; `same_level` **A00 = 0 vs A10 = 15** | (a-i) ≥15/30, (a-ii) ≥15/30, (a-iii) ≥8/15 + p4; corrected contrast |
| **C1** child wage, A10 | **FAIL** | Δ upper 2024 = **0.000000 pp** (baseline 57.4057); declared sign **negative** | Δ < 0 |
| **C2** child wage, pre-cap object | **MIXED** | `demand_official` **−0.4776 pp** (holds); `A_H`, Tier-H queue **not defined** in A01D | declared signs ≤ 0 |
| **C3** phys_cap sensitivity | **PASS** | anchor path **0/33 at every** declared `phys_cap` ∈ {1.00, 1.05, 1.08, 1.15, 1.22, 1.30}; capacity-bound panel cells **3193/6720 (47.5 %) at 1.00 → 0 at ≥ 1.05** | reported in full (D139) |
| **C4** κ object | **PASS** | enforced object **0/53 violations**; realised object **20/53 (A00) → 1/53 (A01D)**; cap binds **23/53**; max cut **27.70 pp** | enforced 0; realised reported |
| **C5** lower register | **PASS** | target **80.76 internal / 80.896 observed**; chain identity error **0**; `m = 1.10` in **6720/6720** A10 cells, **0** at a clip boundary | both channels, 2021, m frozen |
| **G1** A00 identity | **PASS** | sha256 **`47d4b082…`** (6 720 × 89), byte-identical | exact |
| **G2** counterfactual identity | **PASS** | **0 differing / 598 080 cells** (A00CF vs A01D) | 0 differing |
| **G3** two exact checks | **PASS** | primary+lower schooling columns **23 520/23 520 identical**; tertiary **0** non-monotone cells | exact |
| **G4** order / one-way | **PASS** | **0** same-year economy reads in the admission region; replay **53/53** | 0 hits |
| **G5** frozen + determinism | **PASS** | 17 frozen inputs unchanged; **17/17** result CSVs byte-identical across two runs | all |
| **G6** predecl integrity | **PASS** | sha256 match; 26 parameter checks | exact |
| **G7** no-fit audit | **PASS** | 0 parameters chosen by a level bar | 0 |

**The 33-cell detail is in `results/observed_path.csv`** (A10 and A00 side by side against the observed cells). No
cell is within ±5 pp; the *closest* is upper 2024 at **−17.62 pp**. By contrast A00 passes primary 2013–2024
(6/11), upper 2022–2024 (3/11) and lower 0/11 — the 9/33 that EXP-7 scored.

---

## 3. Which obligation changed what

Three arms differ by exactly two declared objects: the per-tier **survival multipliers** and the open tier's
**return scale**. `D1_survonly` = v1.5's `v_O = 0.45 v_H` with the survival multipliers removed; `A10` = the repair
(`v_O = q_O v_H = 0.55 v_H`, no survival multiplier).

| arm | what it is | primary 2024 | lower 2021 | lower 2024 | upper 2024 | primary surv 2024 | lower surv 2021 | upper surv 2024 | 33-cell count |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A00** | frozen v1.3 (no tier block) | 100.00 | 67.41 | 85.87 | 76.64 | 0.9233 | 0.7818 | 0.8701 | **9/33** |
| **A11V15** | v1.5-faithful reconstruction | 51.63 | 43.73 | 51.57 | 44.89 | 0.5867 | 0.5832 | 0.8550 | 0/33 |
| **D1_survonly** | survival multipliers removed, `v_O = 0.45 v_H` | **81.25** | **58.62** | **74.67** | **57.41** | 0.9233 | 0.7818 | 0.8701 | 0/33 |
| **A10** | the repair (`v_O = 0.55 v_H`) | **81.25** | **58.62** | **74.67** | **57.41** | 0.9233 | 0.7818 | 0.8701 | 0/33 |

Three facts follow and each is a finding:

1. **The survival obligation (R4c) carries the whole level recovery.** Restoring untiered survival moves primary
   **+29.6 pp**, lower 2024 **+23.1 pp**, upper **+12.5 pp**. v1.5's collapse was, arithmetically, the survival
   exponent doing work A5 never asked it to do. D134(3) was right about the defect and right about the size.
2. **The return-margin re-location (R4a/R4b) is behaviourally inert at the declared values.** `D1_survonly` and
   `A10` are identical to 10 significant digits in every scored object — because the tier choice is a **15-cell
   discrete comparison** and the 0.45 → 0.55 change flips no cell. The discount is now at the *right margin*
   (utility/take-up) but that margin is **flat at 0.55**. The declared sensitivity shows it is live elsewhere:
   `q_O = 0.85` or `1.00` → upper 2024 **76.54** and **3/33**; `q_O = 0.40` → upper **42.73**. **Even at
   `q_O = 1.00` (no open-tier discount at all) the class reaches only 3/33**, so the path failure is *not* caused by
   the quality discount.
3. **The tier block's aggregate take-up is the binding object.** At primary 2024 the tier block's applicant share
   is **0.90** of the cohort (frozen block: **0.9957**) and its admission is **0.80** after unfilled Tier O places
   (unfilled share **0.169**; upper **0.605**; lower 2024 **0.178**). The 19.6-pp admission loss is what the observed
   path sees: it is ≈ the whole primary gap (−17.05 pp) and most of the upper gap (−17.62 pp). This is the same
   quantity v1.5 buried under survival, now reported as two observables.

**Reconciliation to v1.5 (guard against a silent re-implementation).** The reconstruction arm `A11V15` reproduces
the frozen v1.5 A10 panel **exactly**: `completion_uis` **6 720/6 720** cells identical (max abs diff 5.0e−11),
`admitted_official`, `enrolment` and `graduates` identical to within 5e−4 in count units, `demand_official`
**6 719/6 720** (one cell differs, `reconciliation_v15.csv`). The repaired generator is therefore a *measured*
departure from v1.5, not a different model wearing its name.

---

## 4. κ — what WINDOW-ONLY actually did here (D138)

**κ is not in the scored arm.** A10 has `kappa_link = FALSE`: no κ value enters any scored number, and no constraint
is enforced on the projection. The per-system register (PHL 0.9491, KOR 0.9898, KHM 0.5950, CHN 0.7222) is carried
as a **descriptive record only**.

The κ machinery exists in this cell for three audit purposes, all in the **diagnostic** arm A01D (`bimodal OFF,
kappa ON`) which is never scored and never described as a projection:

1. **R1 — the right object.** The cap is enforced on the upper official-age **admission rate** `a_u(s)` and the bound
   is set so that `e(s) = m · a_u(s) · surv_upper(s) ≤ κ · comp_uis_lower(s−3)` holds by construction. The audit
   recomputes `e(s)` from the panel with the same `m` and the same `surv`: **0/53 violations** (was 20/53 at the
   *completion level* in A00). **Enforced object = audited object.** The realised 3-year-later completion object is
   reported separately: **20/53 → 1/53** violations, the residual being the `surv(s) → surv(s+3)` drift over the lag —
   quantified per cell in `kappa_object_audit.csv`. This is exactly why κ cannot be a forward constraint: enforcing
   it at entry requires knowing survival three years later, which is look-ahead. D138 and R1 agree.
2. **R3 — the counterfactual identity.** A01D's upper admission **counts** vector, fed into A00's accounting, reproduces
   A01D **cell-for-cell, 0 differing of 598 080 cells**. The link changes nothing except through the declared channel.
3. **R5c — the pre-cap object.** The κ cap binds in **23/53** cells with a maximum cut of **27.70 pp**.

The realised-object residue (**1/53**) is reported as a finding, not smoothed: the completion-unit bound holds at the
year it is enforced, and the completion it implies three years later is what a panel audit sees.

---

## 5. `phys_cap` sensitivity of the floor (D139)

Run in A10 across the declared grid {1.00, 1.05, 1.08, 1.15, 1.22, 1.30} (`results/phys_cap_sensitivity.csv`):

| phys_cap | primary 2024 | lower 2021 | upper 2024 | 33-cell count | capacity-bound panel cells | primary phys/cohort 2024 |
|---:|---:|---:|---:|---:|---:|---:|
| 1.00 | 81.2539 | 58.6151 | 57.4057 | 0 | **3 193 / 6 720 (47.5 %)** | 0.9339 |
| 1.05 | 81.2539 | 58.6151 | 57.4057 | 0 | 0 | 0.9806 |
| 1.08 | 81.2539 | 58.6151 | 57.4057 | 0 | 0 | 1.0086 |
| **1.15** | **81.2539** | **58.6151** | **57.4057** | **0** | **0** | **1.05** |
| 1.22 | 81.2539 | 58.6151 | 57.4057 | 0 | 0 | 1.05 |
| 1.30 | 81.2539 | 58.6151 | 57.4057 | 0 | 0 | 1.05 |

**The finding is that the floor has no `phys_cap` bite in this cell.** The anchor's path is *identical* at every
declared value, and the capacity-binding regime closes completely between **1.00 and 1.05** — the declared **1.15** is
already past it, by more than two grid steps. In v1.3/v1.5 the floor was a capacity object where the crowding
allowance mattered; under the two-tier block admission is **take-up-limited** (0.80 applicant/admission vs a physical
capacity of ≥ 0.98 cohort), so the crowding allowance is not what delivers anything at the anchor. **Every floor
statement in this cell is therefore conditional on a convention that turns out not to bind for SYN00** — which
strengthens D139's warning rather than weakening it, and is a stronger statement than "the allowance carries the
floor". The panel-wide count (3 193 capacity-bound cells at 1.00, in the *other* 29 synthetic countries and the early
years) is reported so the reader can see where the allowance would matter.

---

## 6. The child-wage test, re-specified (R5b/R5c)

| leg | object | baseline | +10 % | Δ | declared | verdict |
|---|---|---:|---:|---:|---|---|
| **C1** (verdict-bearing, A10) | upper completion 2024 | 57.4057 | 57.4057 | **0.000000** | negative | **FAIL** |
| **C2a** (A01D pre-cap) | `demand_official` upper 2024 | 80.0311 | 79.5535 | **−0.4776** | negative | holds |
| **C2b** (A01D pre-cap) | `A_H` upper 2024 | — | — | — | negative | **not defined in A01D** |
| **C2c** (A01D pre-cap) | Tier-H queue ratio | — | — | — | ≤ 0 | **not defined in A01D** |
| composition (non-verdict) | upper completion 2024 under a binding cap | 53.5074 | 53.5074 | 0.0000 | not tested | reported |

**C1 fails with a zero, and the zero is the finding.** The declared +10 % shock moves **no** admission, unfilled or
completion object at the anchor, because the tier choice is a 15-cell discrete comparison and a 10 % child-wage rise
flips **none** of the 15 cells. This is the *same* class of defect D134(2) ruled on, one layer deeper: the old test
was structurally unfirable because the cap fixed total entry; **the new test is structurally unfirable because the
declared grid is too coarse to resolve it.** A post-hoc, non-verdict-bearing scan (disclosed below) locates the step:
×1.25 → Δ = 0.000, **×1.50 → Δ = −14.680 pp**. So the outside option *is* live on the upper-completion object; it
simply has a dead zone around +10 % that the declared design sits inside.

The contrast with the frozen single-gate block is the informative part: at +10 %, A01D's `demand_official` **does**
move (**−0.4776 pp**), because the frozen four-state block is continuous. The two-tier choice block's *quantisation*
is what makes the outside option inert — not the shock's object, and not the sign derivation (which the ×1.50 row
confirms: negative, as derived).

**C2 is `MIXED` because of a predeclaration-authoring error of my own, recorded and not rescued.** R5c named
**A01D** as the capped arm for `demand_official`, `A_H` and the Tier-H queue — but A01D is `bimodal OFF`, so it has
**no tier block** and cannot produce `A_H` or a Tier-H queue at all. This is exactly the error class D134(4) flagged
(the a-iv leg): naming an arm by one switch when two are orthogonal. The leg is reported as written (one of three
objects scorable, and it holds), and the two missing objects are reported in `child_wage_A10.csv` from a **post-hoc,
non-verdict-bearing arm `A11K`** (`bimodal ON + kappa ON`): `demand_official` 82.00 → 82.00, `A_H` 72.00 → 72.00,
queue ratio 0.9107 → 0.9107 — i.e. **also exactly zero**, the same quantisation. Neither the verdict nor any
threshold was changed when the error was found.

---

## 7. The lower register (D140)

`results/lower_channel_report.csv`, lower-secondary **2021** (the κ-chain year, **not** 2024):

```
model 58.6151 = 1.10 × 0.681570 (2018 admission rate) × 0.781819 (2021 survival)   [chain error 0.0]
targets:  80.76 pp internal-consistency  (upper 2024 untiered / 0.949)
          80.896 pp OBSERVED             (UNIVERSALIZATION_SERIES.csv, the compared cell)
provenance difference: +0.136 pp (observed − internal), declared, not reconciled
median-free channel reading: JOINT — rationing 49.30 % / survival 50.70 % (D140)
alternative literal order:   SURVIVAL-CARRIED at 50.70 %; action identical
survival ceiling at 2021:    0.784589 (surv_max 0.91); model 0.781819 (sits 0.28 pp inside)
gap to the observed cell:     22.281 pp
```

**Both channels are named in the same breath, as required**, and neither alone is presented as the cause. The tier
block **widens** the lower gap relative to A00 (13.489 pp → 22.281 pp) because the take-up margin cuts the 2018
admission rate (0.7838 → 0.6816) — i.e. the tier block adds rationing to a series that was already short on survival
and rationing. `m = 1.10` is a **convention**: `completion_uis / completion_cohort = 1.10 ± 1e−9` in **6 720/6 720**
A10 cells (max dev 2.2e−16), **0** at a clip boundary; in A00 **6 685/6 720** hold and **35** cells sit at the upper
clip (primary saturation) — the clip boundary is declared and counted, not silently skipped.

---

## 8. Guards, determinism, audit trail

- **G1**: A00 byte-identical to `47d4b082…` (6 720 rows × 89 columns). Two independent builds of the code produce it;
  the guard is checked before any check is scored and the driver refuses to score otherwise.
- **G2**: the counterfactual identity of R3 — **0/598 080** differing cells.
- **G3**: primary and lower schooling columns **23 520/23 520** identical between A01D and A00; tertiary admission
  moves only through the eligibility pool (**0** non-monotone cells across 56 years).
- **G4**: static audit of the admission region **0** same-year economy reads; numerical replay of the κ admission
  decision from its recorded pre-cap inputs **53/53**. The one within-year dependency that v1.5 disclosed
  (tertiary tier composition read from the *same-year* upper choice shares) is **removed**: it now reads the
  **entry cohort** (`t − DVEC[2]`). W1 (intra-level Tier O take-up clearing) is declared, not removed.
- **G5**: 17 frozen inputs unchanged; **17/17** result CSVs byte-identical across two complete runs
  (`results/` and `results/determinism_run2/`), seed 20261120, one PCG64 stream, no wall-clock.
- **G6**: predeclaration sha embedded at build time and re-verified; 26 declared-parameter checks against the
  code.
- **G7**: no parameter chosen by reference to a level bar. The q_O/h_share/phys_cap/survival-penalty grids are
  disclosed in full (`sensitivity_arms.csv`); **the scored value in every case is the pre-declared one**, including
  where a grid cell scores better (`q_O = 1.00`: 3/33 — still nowhere near the bar, and not adopted).

**R1 ratchet / no-reversal**: no reversal term was added, and no reversal diagnostic is inferred. **`NO REVERSAL
DIAGNOSTIC IS TO BE INFERRED FROM THIS RUN.`**

---

## 9. What this cannot claim

1. **No causal claim, no direction claim.** Nothing here says schooling causes anything, that either tier causes any
   outcome, or that the Philippines behaves like this model.
2. **`SYN00_PHL_LIKE` is not the Philippines.** It is one synthetic country whose trait block is anchored on an
   observed PHL path; the other 29 are declared draws. Every generator number is `LABEL: SYNTHETIC`.
3. **Not an independent test of A5.** The A5 parameters are post-observation; this run can only report what the
   declared class does, never whether A5 is true.
4. **Not "v1.5 passing", and v1.5 is not re-scored.** v1.5's verdict string stands permanently. This cell re-freezes
   no v1.5 check.
5. **Not a re-fit.** No parameter carries a `FITTED` label; nothing was calibrated to 75.025, to the 33 observed
   cells, to 80.76/80.896, or to any band. The declared parameters were fixed before the scored run.
6. **Never "demand falsified", in any paraphrase.** The A3 line stays **KILLED as a specification result** (D130).
   What this run shows is that the two-tier class can represent the coexistence and cannot hold the level on these
   declared parameters. Demand is revealed and strong (queues at the high gate, shadow education, credential
   chasing); a synthetic failure is not evidence about demand.
7. **The ceiling remains `UNABLE as to cause` (D63).** Nothing here attributes the PHL ceiling; a synthetic
   `PATH-FAILED` is non-diagnostic about the record and is attributed to *the model's own objects*.
8. **C1–C4 are not reopened.** No WT/DT cell was re-run or re-scored, no paper-test slate was added, A3-D was not
   re-tuned, and the v1.4 `c4a`/`c4b` FAILs stand.
9. **The "unfilled place" is a model object, not a measurement.** `V_O` is not capacity utilisation, not the
   out-of-school rate, and not a DepEd/CHED seat statistic. The HELD items below have no on-disk proxy and **none was
   fabricated**.
10. **The over-age top-up can absorb freed physical capacity.** The frozen rule `adm_oa = min(D_oa, phys − adm_off)`
    is unchanged, so an unfilled official-age place can be taken by an over-age applicant even though `V_O` is never
    reallocated *within* the tier. Disclosed as a known property of the frozen supply rule, not presented as
    validation of `V_O`.

**HELD, named and unused (D124(d), D135):** DepEd/CHED seats-vs-enrolment; private/public shares of enrolment and
provision; SHS voucher take-up; capacity utilisation (the object `V_O` would be validated against); PSA microdata;
WB Enterprise Surveys; real per-pupil spending; annual capacity/enforcement; a measured rung-4 credential-queue
series; PHL/KHM/CHN/JPN shadow participation; a measured remittance→schooling coefficient.

---

## 10. What would change the verdict (each needs a NEW predeclaration)

1. **Nest the tier choice in the frozen four-state block.** The tier block re-decides school-vs-outside and returns an
   applicant share of 0.80–0.90 where the frozen block returns 0.9957. A repair that *splits* the frozen schooling
   mass into H/O (instead of re-deciding it) is the single change most likely to change the observed-path count — and
   it is a re-specification of the block, not a parameter, so it cannot be done inside this cell.
2. **Give the tier choice continuous resolution** (or a declared smoothing) so that a 10 % child-wage shock can move
   it. The ×1.50 post-hoc row shows the object is live; the declared grid is too coarse.
3. **Model the tier shares as an object with an observed counterpart.** `h_share` is declared; the sensitivity shows
   the upper level moves 57.41 → 59.80 under `h_share + 0.10`, i.e. the share is doing real work that no on-disk
   series constrains.
4. **A measured places/enrolment series** (HELD) — the only route to making the floor a capacity object again.

**None of these was done here, and none will be done by re-running this cell.**

---

## 11. Disclosures (build-time, unflattering, no re-score)

1. **Pre-run probes.** Before the final freeze I ran machinery probes: the A00 identity, the v1.5-reconstruction
   equality, and a smoke run of A10. That smoke run therefore **saw A10's levels and the 0/33 count before the
   final predeclaration hash was taken**. No parameter, threshold, band, year set, arm-scoring rule or verdict word
   was changed as a result; the only pre-freeze amendment was the **addition of the diagnostic decomposition arm
   `D1_survonly`**, whose values are v1.5-declared (`v_O = 0.45`) and not chosen by any level. Recorded in
   `TUNE_LOG.md` C1.
2. **A predeclaration-authoring error of my own**: R5c named A01D (`bimodal OFF`) for `A_H` and the Tier-H queue,
   which that arm cannot produce. Recorded in §6 and TUNE_LOG C5; the leg is `MIXED`, not rescued.
3. **Post-hoc, non-verdict-bearing diagnostics** (labelled as such in `child_wage_A10.csv`): the child-wage
   magnitude scan ×1.25/×1.50 and the arm `A11K`. They are **not** in the frozen arm list, were computed after the
   scored run, and change no verdict.
4. **`demand_official` differs from v1.5 in one cell of 6 720** (the reconciliation row). Cause is not chased; it is
   reported because a silent "identical" would be false.
5. **`SHA256SUMS.txt` was regenerated after `FINDINGS.md` and `TUNE_LOG.md` were written** so the index covers the
   narrative files; no result file changed.

---

**`LABEL: SYNTHETIC` — built and run to the frozen predeclaration — not evidence — no causal or direction claim —
no reversal diagnostic inferred — C1–C4 not reopened — A3-D not re-tuned — v1.5's verdict stands — HELD data stays
HELD.** **Verdict: `PATH-FAILED` (representation-only; the ceiling remains `UNATTRIBUTED`).**
