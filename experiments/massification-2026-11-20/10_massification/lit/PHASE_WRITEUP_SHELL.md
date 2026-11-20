<!-- SHELL / OUTLINE — NOT RESULTS. Writer: lit-archivist, 2026-11-20, under Council-2 phase write-up order.
Every number below is LIFTED from already-produced outputs; each table row carries its source file. No new
analysis, no re-fit, no direction claim, no causal claim. Observed vs simulated labelled line by line.
Blocked sources are listed as design-only and are NOT load-bearing anywhere in this shell.
Unread citations: none. Nothing here is cited that I have not seen in the programme's own outputs or data.
Location: 10_massification/lit/ (my write scope). Executor may mirror to 06_report/ — agreed location note in §0. -->

# PHASE WRITE-UP SHELL — two publishable objects
**(a) a bounded negative on income-scaling; (b) an equivalence / identification map with one unreproduced asymmetry**

**Status: SHELL.** Section headings, table skeletons, and the exact existing numbers that go in each cell. This is the
writing plan for two papers, not a results document. Every claim is capped at what the committed outputs support.

**Headline sentence for both objects (use verbatim as the paper's one-line result):**
> *Conditional level reproduction + observational equivalence + an unreproduced asymmetry.*

---

## §0. Agreed framing, scope and labelling (both objects)

**0.1 What is being claimed.** That the cohort-flow model class, **at these specifications and on this record**, (i) cannot generate the positive income-scaling sign without an exogenous supply channel, and (ii) leaves the cross-country push-pull direction unidentified while reproducing conditional levels and leaving one observed asymmetry unreproduced. **Nothing about the world beyond the record is claimed.**

**0.2 Observed vs simulated label convention (binding in every table).**
- `OBS` = observed value from a cited series/table on disk (source named).
- `SIM` = simulated value from a committed run (arm named).
- `DERIVED` = arithmetic on an OBS value (formula stated).
- Any cell without one of these labels does not enter the paper.

**0.3 Blocked sources are not load-bearing (binding).**
- PSA FIES/APIS/LFS (returns by education), Enterprise Surveys credential module, OECD/ILOSTAT: **DATA BLOCKED**.
- Consequence: the **human-capital** and **signalling/MMI** rivals are **design-only**, listed in every results table and **not claimed as tested**. The equivalence map must say "untested", never "equivalent".
- No unread citation appears in either object.

**0.4 Location.** Files under `10_massification/lit/` (lit-archivist scope); `06_report/` mirror to be produced by the executor if the Council prefers the single external entry point.

---

# OBJECT (a) — Bounded negative: the cohort-flow model class cannot generate positive income-scaling without an exogenous supply channel

## (a).1 The claim, stated at its true strength
At the A3 specification and on these panels, the three rivals produce **wrong-sign out-of-sample exponents**, **contain zero of three required exponent cells**, and **lose to a naive linear trend on holdout**. The income-scaling repair is a **one-cell budget (R27), and it failed**. Therefore: *as specified*, the class cannot be credited with reproducing income-scaling; an exogenous supply channel would be needed. **Not claimed:** that income-scaling is absent in the world.

## (a).2 Table A-1 — the scaling criterion (all numbers from committed outputs)
| Cell | Rival | Result | Status | Source |
|---|---|---|---|---|
| OOS exponent, secondary schooling | rival 1 / 2 / 3 | **−1.89 / −0.38 / −0.74** | SIM | A1 addendum (`model/anchor_out/A1_ADDENDUM_C1_C10.md`) |
| OOS exponent, tertiary | rival 1 / 2 / 3 | **−1.23 / −0.14 / −0.35** | SIM | same |
| Sign check | all three rivals | **signs_ok 1/3** | SIM | `STATUS.md` §3k / line 260 |
| Containment in A3 range | all three rivals | **contained 0/3** | SIM | same |
| Within 1 s.e. of A1 | all three rivals | **0/3** | SIM | `STATUS.md` line 271 |
| Repair cell | — | **FAIL, 0/3 contained** | SIM | A1 addendum; `STATUS.md` §3k |
| Fit MAE (PHL) | all rivals | **6.16–7.43 pp** vs a **5 pp gate** | SIM | `STATUS.md` line 261 |
| Holdout MAE (PHL) | all rivals | **4.80–6.26 pp** | SIM | same |
| CHN fit/holdout | all rivals | **7.03–8.83 pp** | SIM | same |
| Naive benchmark: persistence | — | **8.60 pp** | SIM | `STATUS.md` line 82 |
| Naive benchmark: linear trend | — | **4.35 pp** | SIM | same |
| Verdict vs benchmark | — | **all three rivals lose to the linear-trend benchmark** | SIM | same |

## (a).3 Required scope paragraph (write in full, do not shorten)
The negative is **bounded on four dimensions** and the paper must say all four:
1. **Specification-bounded** — this is the A3 specification with one repair cell (R27); it is not a proof about all cohort-flow models.
2. **Record-bounded** — the income-scaling test uses the panels declared in the pre-registration; it is not a global test.
3. **Sign-bounded** — the finding is that *these rivals* cannot produce the required positive sign without an exogenous supply channel; a model with such a channel is outside the tested class, so the negative does not extend to it. **This is the boundary the Council should treat as the paper's contribution: it locates where the class must be extended, not where the world must be.**
4. **Benchmark-bounded** — the decisive comparison is against **linear trend (4.35 pp)** and **persistence (8.60 pp)**, not against zero. Losing to persistence would be trivial; losing to linear trend is the informative failure and must be foregrounded.

## (a).4 Figures / tables to build (from existing files only, no new estimation)
- Fig A-1: OOS exponent scatter with the A3 admissible range shaded; wrong-sign points labelled.
- Fig A-2: fit vs holdout MAE by rival, with the 5 pp gate and the 4.35 pp linear-trend line drawn on.
- Table A-2: the R27 one-cell repair budget log (what was tried, that it failed, that no further repair is permitted).

---

# OBJECT (b) — Equivalence / identification map + the unreproduced PHL asymmetry

## (b).1 The claim
The record is reproduced **conditionally on level** but the model set is **observationally equivalent** on the crossings; the cross-country push-pull **direction is not identifiable** (R13 / forced-ID); and one observed asymmetry — **primary 2017, lower-secondary 2024, upper-secondary never ≥90, tertiary 2024–25** — is **unreproduced by every model on disk**.

## (b).2 Table B-1 — observed anchor signature (the target)
| Milestone | OBS value | OBS crossing | Status | Source |
|---|---|---|---|---|
| M0 | completion_lower ≥50 already before 1999 | left-censored | OBS | A1 addendum |
| M1 | primary GER ≥100 in **1977**; NER ≥95 in **1976** | left-censored ≤1977 | OBS | A1 addendum; `findings.txt` |
| **Primary completion ≥90** | 83.16 (1999) → 87.45 (2013) → **91.92 (2017)** → 95.40 (2021) → 98.30 (2024) | **2017** | OBS | A1 addendum C8 |
| M2 lower-secondary completion ≥90 | 92.41 (2024) | **2024** | OBS | A1 addendum |
| M3 upper-secondary completion ≥90 | 59.70 (1999) → **75.03 (2024)**, peak 76.43 (2017) | **never by 2024** | OBS | A1 addendum; A5B report |
| M4 tertiary GER ≥50 | 16.34 (1971) → 47.41 (2024) | **2024–25 band (2025)** | OBS | A1 addendum C9; A5B report |

**The asymmetry, stated exactly:** order is **primary < lower-secondary < tertiary**; **upper never crosses**. This is the anchor criterion (A6/R23).

## (b).3 Table B-2 — the 12-arm record (ALL `SIM`; observed comparisons in the last column)
| Rival | Arm | fit MAE | hold MAE | M0 | M1 | M2 | M3 | M4 | vs OBS |
|---|---|---|---|---|---|---|---|---|---|
| demand_led | law_only | 2.03 | 4.42 | 1960 | 1966 | — | — | 1960 | M2/M3 miss |
| demand_led | capacity_gated | 1.85 | 4.51 | 1960 | 1966 | — | — | 1960 | miss |
| demand_led | capacity_only | 3.29 | 4.55 | 1979 | 1966 | **2028** | **2031** | 1960 | M2 in ±5y but R29-flagged |
| demand_led | none | 1.05 | 6.11 | 1967 | 1966 | — | — | 1960 | miss |
| education_led | law_only | 2.16 | 5.19 | 1960 | 1966 | — | — | 1960 | miss |
| education_led | capacity_gated | 2.05 | 5.26 | 1980 | 1966 | **2025** | **2027** | 1960 | M2 in ±5y but R29-flagged; M3 post-window |
| education_led | capacity_only | 3.02 | 6.12 | 1961 | 1966 | — | — | 1960 | miss |
| education_led | none | 1.37 | 5.88 | 1967 | 1966 | — | — | 1960 | miss |
| complementary | law_only | 2.17 | 4.57 | 1960 | 1966 | — | — | 1960 | miss |
| complementary | capacity_gated | 1.97 | 4.01 | 1963 | 1966 | — | — | 1960 | miss |
| complementary | capacity_only | 2.47 | 5.94 | 1960 | 1966 | — | — | 1960 | miss |
| complementary | none | 1.32 | 5.94 | 1980 | 1966 | **2038** | — | 1960 | M2 outside ±5y |
Source: `model/anchor_out/anchor_table.csv`, `findings.txt`, `A1_ADDENDUM_C1_C10.md`. **No arm reproduces M2+M3.** M4 = 1960 in **all 12 arms including no-push** (C9) → **NOT DISCRIMINABLE**, excluded from PASS/FAIL, "untested" not "64-year miss".

## (b).4 Table B-3 — corrected crossing accounting (Council-2 rule)
| Milestone | OBS | SIM arms | Accounting |
|---|---|---|---|
| M0 | left-censored | 1960–1980 | boundary constraint only; constant capacity back-fill |
| M1 | left-censored ≤1977 | 1966 | boundary constraint only |
| M2 | 2024 | 2025 / 2028 / 2038 | **clean in-tolerance 0/12**; 2025 & 2028 are R29-flagged (same-arm post-window M3 at 2027/2031); 2038 outside ±5y |
| M3 | never by 2024 (75.03) | none ≤2024; 2027, 2031 post-window | **R6 in-window 12/12 pass; 2/12 post-window overshoots** → R29 ceiling flag |
| M4 | 2024–25 | 1960 all arms | **not discriminable** (initial value ≥50) → untested |

## (b).5 Table B-4 — the equivalence map (R13)
| Comparison | Result | Status | Source |
|---|---|---|---|
| capacity_gated vs law_only, demand_led | holdout **1.85 vs 2.03** | SIM | A1 addendum |
| capacity_gated vs law_only, complementary | holdout **1.97 vs 2.17** | SIM | same |
| crossings, demand_led | law M2=None → gated M2=None (**TIE**) | SIM | A1 addendum A10 |
| crossings, education_led | law None → gated **2025** (gated better) | SIM | same |
| crossings, complementary | None → None (**TIE**) | SIM | same |
| **Overall capacity-timing credit** | **1 of 3 arms → NOT credited; EQUIVALENT/mixed** | SIM | same (R24/R29) |
| A2d capacity-leads-intake | cross-correlation **−0.427 at lag 6** (no positive lead) | SIM | `A2D_CAPACITY_LEADS_INTAKE.md` |
| Ceiling residual (upper-sec 75.03 vs 90) | **14.97 pp, UNABLE** — candidate accounts listed, no discriminating observable | OBS+SIM | A1 addendum A10/R29 |

**Forced-ID / R13 statement to write out:** the cross-country push-pull **direction is not identifiable** on these data; the forced-identification exercise does not separate the rivals, so the paper reports an **equivalence set**, not a direction. **No direction claim anywhere in the text** (R13/R24/R25).

## (b).6 Table B-5 — the four testable rivals against the same record (A5b)
| Rival | predicted primary | lower | upper | tertiary | order correct | upper FP | equivalent (±5y, no FP)? | source |
|---|---|---|---|---|---|---|---|---|
| world-society timing (shared r,t0) | **2014** | none | none | none | no | no | **no** — but see scope refinement | A5B_REPORT |
| state-building step (spend, teachers) | none | none | none (NaN covariate) | none | no | no | no | same |
| demographic/cohort contrast | none | none | none | none | no | no | no (upper extrapolation −122 pp, implausible) | same |
| formal-model shapes (per-level logistic) | **2023** | none to 2050 | none to 2050 | none to 2050 | no | no | no | same |

**⚠ A5b SCOPE REFINEMENT — mandatory in the paper, do not omit.** World-society's predicted primary crossing is **2014**, and the observed is **2017** — that is **within ±5 years**. Therefore the emptiness of the equivalence set **cannot** be argued from primary timing. It rests on: **(i) ordering/spacing** (world-society produces near-simultaneous crossings and cannot generate primary→lower→tertiary spacing) and **(ii) the upper-secondary never-crossing** (no rival produces it). The paper must state this explicitly, or a reviewer will find that the one rival closest on primary was dismissed on a claim the ±5y rule does not support.

## (b).7 ⚠ C8 REPORTING GAP — mandatory disclosure (do not bury)
The observed **primary completion ≥90 crossing in 2017** is a milestone the committed **A1 model outputs never recorded**: M1 was defined as NER ≥95 / GER ≥100, which is left-censored by construction, and **per-arm fitted series were not persisted**. The asymmetry was therefore tested **with its first element missing**, and the model-side counterpart of the 2017 milestone is **not recoverable from existing outputs**. **No re-fit was performed** (Council-2 rule). State this as a **reporting gap of A1**, not as evidence for or against any mechanism.

## (b).8 Table B-6 — event evidence (descriptive only, no causal claim)
| Event | Affected level | OBS crossing | Event→crossing gap | Verdict |
|---|---|---|---|---|
| PHL 1987 compulsory-primary lineage | primary | 2017 | −30 y | **context, not mechanism** |
| PHL K-12 2013 (RA 10533) | upper-secondary | never by 2024 | — | context, not mechanism (no crossing to align) |
| PHL free SHS 2016 | upper-secondary | never by 2024 | — | context |
| PHL free tertiary 2018 | tertiary GER | 2025 | −7 y (outside ±5) | context, confounded with K-12/free SHS |
Source: `A5B_REPORT.md` (D50/D51). **The state-push mechanism is not established by these data and may not be assumed** (A7/R24).

## (b).9 Model defects to disclose in the limitations section (from C10)
1. **Capacity is constant back-filled** before first observed input (PTR first observed 2000; spending 1995) — pre-1995/2000 crossings (M0 1960, M1 1966/1977, M4 1960) carry **no point-timing credit**.
2. **Enforcement is de jure only** (compulsory-duration mapping from `POLICY_TIMELINE.csv`), not measured enforcement (attendance/penalties DATA BLOCKED).
3. **Double-count defect:** the enforcement proxy sits inside `G(C)` while also being a step function of the same law dates → **`law × G(C)` counts compulsory-length changes twice**. Not repaired (no re-fit allowed). **Any capacity-timing claim must treat the gate as contaminated** until the proxy is measured independently or removed.

---

## §1. What the two objects do NOT claim (write as an explicit box in both papers)
1. Not that income-scaling is false in the world — only that this model class cannot generate the sign without an exogenous supply channel (§a.3).
2. Not that any rival is *better* — all are equivalent or fail (§b.5).
3. Not a direction of push-pull (§b.5, R13).
4. Not a causal effect of any PHL event (§b.8).
5. Not that capacity has no effect — only that it is **not credited** on the crossings (1/3 arms) and that the gate is contaminated (§b.9).
6. Not that the 2017 milestone was reproduced — it was **not recorded** (§b.7).
7. Nothing from the blocked sources contributes to either claim (§0.3).

## §2. Section-by-section plan for the two papers
**Paper (a):** Intro (the income-scaling requirement) → pre-registration and one-cell budget → Table A-1 → the four bounded dimensions of the negative → the linear-trend benchmark as the decisive comparator → what an exogenous supply channel would have to do → limitations (§a.3).
**Paper (b):** Intro (the anchor asymmetry) → the observed signature (Table B-1) → the 12-arm record (B-2) → corrected accounting (B-3) → equivalence map (B-4) → the four rivals and the **scope refinement** (B-5/B-6) → **C8 disclosure** → event evidence as context (B-8) → defects (B-9) → what is not claimed (§1).
**Shared:** both papers carry the same one-line headline and the same §1 box.


---

## Provenance verification (added by executor, 20 Nov; figures re-derived, not re-fit)

The two figures cited from STATUS must be sourced to the run artifacts:
- **naive linear trend = 4.35 pp and persistence = 8.60 pp** — source `10_massification/model/calib/calibration_table.csv`,
  sha256-16 **552e0cce04bd148d** (values 4.352883341604888 / 8.599852941176476).
- **repair-cell PHL fit MAE 6.16–7.43 pp** — source `10_massification/model/calib/repair_table.csv`,
  sha256-16 **34b0a5bc98e3d603** (PHL_fit_mae 6.1627–7.4326); companion `repair_scaling.csv` **7330a8785e28619f**,
  `scaling_check.csv` **a07077c4e38253af**.
- **Canonical mirror:** this shell lives in `10_massification/lit/` (canonical); it is listed in
  `06_report/EXTERNAL_CHECKIN.md` read order. These figures are **observed-run diagnostics**, not new claims.
