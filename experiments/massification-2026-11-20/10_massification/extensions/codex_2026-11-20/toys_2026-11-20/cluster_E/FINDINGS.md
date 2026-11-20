# Cluster E — toy findings (#13 migration/remittance, #14 sector shock × access, #15 information/roads)

**ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

These are three small stdlib toy models built for `COUNCIL_TOY_SPECS_015.md` (Cluster E).
They demonstrate what a stipulated mechanism *can* generate. They do **not** estimate
anything, they are **not** calibrated, and they do **not** reopen the closed massification
phase (closeout `787f1792…`; direction unidentifiable R13, income-scaling sign wrong
R27/C1, ceiling residual 14.97 pp UNABLE, capacity floor-not-ceiling A10/R29, timing
censored). No phase file, closed-anchor file, results table or git branch was touched.
A threshold **PASS** below means only *the stipulated rules mechanically generate the
declared pattern*; a **FAIL** is reported with equal prominence and was **not** re-run,
re-seeded or re-parameterised.

- Design and thresholds were frozen in `PRE_DECLARATIONS.md` **before** the run
  (sha256-16 `2cdc053aa03ae921`, pre-run stamp `2026-11-20T11:06:43Z`).
- 200 seeds per cell, all latents drawn once per seed and shared across arms
  (paired counterfactuals), one-factor shocks, matched starting conditions.
- `RESULTS.csv` holds all 369 rows: every arm including failures, plus auxiliary
  sensitivity arms and 17 verdict rows. Seed schedule: E13 `20261120+0…199`,
  E14 `20461120+0…199`, E15 `20661120+0…199`.
- Re-running `code/run_all.py` reproduces `RESULTS.csv` byte-for-byte
  (sha256 `f8cb72d18bd8aff1…`); `code/verify_results.py` re-derives all 17 verdicts
  from the CSV and finds 17/17 agreement.

---

## 1. Verdict summary

| ID | Predeclared rule | Observed | Verdict |
|---|---|---|---|
| **T13-P1a** | remittances raise applications ≥ 4.0/cycle (+2.0 pp) | **+8.05/cycle (+4.02 pp)** | **PASS** |
| **T13-P1b** | remittances raise completion ≥ 1.0 pp | **+3.54 pp** | **PASS** |
| **T13-P2** | route raises completion ≥ 8.0 pp | **+15.22 pp** | **PASS** |
| **T13-P3** | local formal posts identical in all arms | **45 in all 4 cells, all 200 seeds** | **PASS** |
| F13 | no/perverse route or remittance effect | neither | not triggered |
| **T14-P1a** | open access: A applications ≥ +30 | **+106.50** | **PASS** |
| **T14-P1b** | open access: A completer ≥ +25 | **+90.07** | **PASS** |
| **T14-P1c** | reallocation not expansion: \|Δ total completer\| ≤ 10 | **+24.68** | **FAIL** |
| **T14-P2a** | closed/open application response ≤ 0.50 | **0.3029** | **PASS** |
| **T14-P2b** | closed/open completer response ≤ 0.50 | **0.3015** | **PASS** |
| **T14-P3** | placebo B ≥ +30 and A ≤ −20 | **+106.73 / −74.11** | **PASS** |
| **T14-P4** | closed vacancies ≥ 10 and open ≤ 3 | **8.35 / 0.00** | **FAIL** |
| F14 | demand works without access | not triggered (30 % attenuation) | not triggered |
| **T15-P1** | info×road interaction ≥ 0.06, road=1 effect ≥ 0.10 | **+0.0307; +0.0634** | **FAIL** |
| **T15-P2** | road ≥ 0.05/hh, teacher ≥ 2.0 pp, info ≥ 0.03/hh | **+0.2265, +6.67 pp, +0.0481** | **PASS** |
| **T15-P3** | admissions flat (≤0.02/hh) and queues ≥ 0.05/hh | **−0.00002; +0.0481** | **FAIL** (queue margin, by 0.002) |
| F15 | no interaction (\|diff-in-diff\| < 0.03) | 0.0307 — 0.0007 above the floor | not triggered (marginal) |

**4 of 14 predeclared thresholds failed** (T14-P1c, T14-P4, T15-P1, T15-P3). None of the
three falsifiers was triggered; F15 survived by a hair.

---

## 2. #13 — Migration and remittance route

200 origin households, 20 cycles, origin seats deliberately **non-binding** (170; peak
applications 134), local formal posts fixed at **45** in every arm and cycle.

| cell | applications/cycle | apply rate | completions/cycle | completion rate | unique migrants | household resources | local posts | local output |
|---|---|---|---|---|---|---|---|---|
| route=closed, remit=off | 91.09 | 45.55 % | 80.47 | **40.24 %** | 20.00 | 2.50 | 45 | 73.35 |
| route=closed, remit=on | 96.84 | 48.42 % | 85.54 | 42.77 % | 20.00 | 2.64 | 45 | 73.35 |
| route=open, remit=off | 125.89 | 62.95 % | 110.91 | **55.45 %** | 78.50 | 2.50 | 45 | 72.08 |
| route=open, remit=on | 133.94 | 66.97 % | 117.98 | **58.99 %** | 82.31 | 2.77 | 45 | 72.74 |

Paired contrasts (200 seeds, 95 % CI):

| contrast | applications/cycle | completion (pp) |
|---|---|---|
| route open − closed (remit off) | **+34.81** [34.06, 35.55] | **+15.22** [14.89, 15.54] |
| remittances on − off (route open) | **+8.05** [7.65, 8.44] | **+3.54** [3.36, 3.71] |
| remittances on − off (route closed, diaspora only) | +5.75 [5.43, 6.07] | +2.53 [2.39, 2.68] |

Readings.

1. **Schooling rises with the route while local jobs do not move at all**: completion
   +15.2 pp with local posts at exactly 45 in every arm and seed (T13-P3). The entire
   response is the demand/willingness-to-pay channel (the route premium enters the value
   of the credential), not a local-labour-demand channel. This is the cleanest
   illustration in the Cluster E set.
2. **Remittances add a smaller positive effect, same sign** (+3.54 pp vs +15.22 pp
   route), and they act only through the household cash constraint (they do not enter the
   value of the credential). The declared margins pass comfortably.
3. **Migrants counted once matter**: unique persons ever migrating = 78.5 under the open
   route vs 20 diaspora-only when closed. Per-cycle flow is 45.0, so counting person-cycles
   over 20 cycles would report ≈ 900 and overstate the stock ~11×. The count-once number
   is the one reported.
4. **Local output falls slightly under the route** (73.35 → 72.08, −1.27 output units,
   −1.7 %), although the local post count is unchanged: migrants are selected from
   completers (brain drain), so the fixed 45 posts are staffed by fewer completers. This
   was predeclared as an auxiliary expected sign (down) and is reported descriptively.
   Remittances partially offset it (+0.66).
5. **Sensitivity, no threshold**: halving the route premium to 1.2 still gives
   +11.36 pp [11.07, 11.65] and +51.6 unique migrants — the *sign and ordering* are not
   fragile to halving the premium, but the margin's size is a property of the imposed 2.4.
   The number to remember is the **order of magnitude the assumption buys**, not 15.2 pp.

---

## 3. #14 — Sector-demand shock × field access

200 leavers, two fields, seats deliberately **non-binding** (150/field), shock = +2.5
return in one field only. `vacancies = max(0, posts − licensed completers)`, posts 30
base, 55 in the shocked sector.

| cell | apps A | apps B | apps total | completers A | completers B | completers total | vacancies A |
|---|---|---|---|---|---|---|---|
| no shock, open | 74.11 | 73.88 | 147.99 | 65.45 | 65.39 | 130.84 | 0.00 |
| targeted A, open | 180.60 | 0.00 | 180.60 | 155.52 | 0.00 | 155.52 | 0.00 |
| placebo B, open | 0.00 | 180.60 | 180.60 | 0.00 | 155.57 | 155.57 | 30.00 |
| no shock, closed | 22.12 | 120.21 | 142.34 | 19.50 | 104.48 | 123.98 | 10.51 |
| targeted A, closed | 54.38 | 97.89 | 152.28 | 46.65 | 84.80 | 131.45 | 8.35 |
| placebo B, closed | 0.00 | 180.60 | 180.60 | 0.00 | 155.57 | 155.57 | 30.00 |

Paired shock effects (vs the access-matched no-shock baseline):

| effect | open access | closed access | closed/open ratio |
|---|---|---|---|
| Δ applications, field A | **+106.50** [105.50, 107.49] | **+32.26** [31.73, 32.79] | **0.303** |
| Δ licensed completers, field A | **+90.07** [89.04, 91.11] | **+27.16** [26.61, 27.70] | **0.302** |
| Δ total licensed completers | **+24.68** [23.93, 25.43] | +7.47 [7.05, 7.89] | — |
| placebo B shock: Δ apps B / Δ apps A | +106.73 / −74.11 | +60.40 / −22.13 | — |

Readings.

1. **Field specificity is unambiguous where access is open**: field-B applications go to
   exactly zero under a field-A shock, and the placebo arm is a perfect mirror image.
   The falsifier "no field specificity" is not triggered.
2. **The gate attenuates but does not eliminate the demand pull** (0.303 of the open
   response). Gated-sector completions still rise by 27.2 (from 19.5 to 46.7): the shock
   reallocates the *eligible* pool toward the field, but most of the population cannot
   follow the demand. This is the intended illustration of "demand without access".
3. **T14-P1c FAILED, and it is the most useful negative in this battery.** The shock also
   raises *total* licensed completers by +24.68, far above the ≤ 10 "pure reallocation"
   margin. With a value-threshold application rule, raising one field's return also lowers
   the bar for applying *at all*, so a sectoral shock has a participation margin as well as
   a field-switching margin. In the open arm total applications rise 147.99 → 180.60.
   Implication (hypothesis, not finding): an empirical design that cannot separate total
   participation from field switching cannot identify a "sectoral pull" — it will read a
   general demand expansion.
4. **This arm sits at a corner solution**, which limits what it can illustrate:
   `SHOCK = 2.5` exceeds the entire aptitude range (1.0), so switching is 100 %, field B
   empties completely, and the reallocation margin is degenerate. A stipulated smaller
   shock would have produced partial switching, but that arm was **not** predeclared and
   was **not** run; the corner is a stated limitation, not a result to be trimmed.
5. **T14-P4 FAILED on the margin**: after the targeted shock, closed-access vacancies
   are 8.35 (declared ≥ 10) vs 0.00 open (declared ≤ 3). The direction is right — the gate
   leaves posts unfilled — but the size was over-predicted. Note also that the gated sector
   already had 10.51 vacancies with no shock, and the shock *reduces* them by 2.16: a
   demand shock without access cannot fill the gap, it only nudges a queue.
6. **Sensitivity, no threshold**: tightening the gate to 15 % shrinks the closed-access
   responses further (Δ apps A +16.23, Δ completers A +13.76 vs +32.26/+27.16 at 30 %),
   as the access interpretation predicts.

---

## 4. #15 — Neighbour information and roads

Two villages of 60 households per seed (untied, kin-tied), 8 factor arms, paired within
seed; per-household values pooled over the 120 households. Seats bind at every level
(16/6/2, +1 per level with teacher), so admissions are capacity-capped by design.

| cell (info, road, teacher) | applications/hh | admissions/hh | completions per 100 hh | queue |
|---|---|---|---|---|
| 0,0,0 | 0.746 | 0.399 | 32.93 | 20.82 |
| 0,0,1 | 0.780 | 0.447 | 39.48 | 19.93 |
| 0,1,0 | 0.959 | 0.400 | 32.99 | 33.54 |
| 0,1,1 | 0.989 | 0.450 | 39.69 | 32.36 |
| 1,0,0 | 0.779 | 0.399 | 32.88 | 22.79 |
| 1,0,1 | 0.812 | 0.447 | 39.52 | 21.90 |
| 1,1,0 | 1.022 | 0.400 | 32.90 | 37.35 |
| 1,1,1 | 1.052 | 0.450 | 39.68 | 36.17 |

Paired effects (200 seeds, 95 % CI):

| quantity | estimate |
|---|---|
| info effect on applications, road = 1 | **+0.0634/hh** [0.0600, 0.0669] |
| info effect on applications, road = 0 | **+0.0328/hh** [0.0301, 0.0354] |
| **difference-in-differences** | **+0.0307/hh** [0.0266, 0.0347] |
| road main effect on applications | **+0.2265/hh** [0.2212, 0.2318] |
| teacher main effect on completions | **+6.67 pp** [6.49, 6.84] |
| info main effect on applications | **+0.0481/hh** [0.0458, 0.0504] |
| info effect on admissions | **−0.00002/hh** [−0.0002, 0.0001] |
| info effect on unmet applications (queue) | **+0.0481/hh** [+0.0458, +0.0504] |
| info effect on completions | −0.027 pp [−0.094, +0.040] |

Readings.

1. **The interaction is present, positive and precise — but smaller than declared**
   (+0.0307 vs the 0.06 margin; the road=1 effect is +0.063 vs the 0.10 margin). It arises
   entirely from the stipulated exposure channel (contact probability 0.30 without a road,
   0.70 with one): the per-exposed-household effect is roughly the same in both regimes
   (+0.09 at road=1, +0.11 at road=0), so the interaction is a *dose* effect, not a
   complementarity. Declaration FAILED; mechanism direction upheld.
2. **Information moves queues, not places.** Admissions are flat to five decimal places
   (−0.00002/hh) while queues rise +0.0481/hh: under fixed seats every extra application is
   an unfilled demand, not a completion. T15-P3 failed only because the queue margin
   (0.05) was set a hair above the observed 0.0481; the "places" half of the rule held
   exactly.
3. **Roads dominate information** as an application driver (+0.2265/hh vs +0.0481/hh),
   because they cut the travel-cost term at every level. Distance gradients are visible:
   in the control cell the nearest quartile applies 1.0818/hh vs 0.4483/hh in the farthest;
   with roads the far quartile rises to 0.8215.
4. **With fixed seats, road access redistributes admissions rather than adding them**:
   nearest-quartile admissions fall 0.5875 → 0.4638/hh when roads open, while the farthest
   quartile rises 0.2358 → 0.3327/hh (lottery among a larger applicant pool). Another
   reminder that an application-side "information" effect is not a completion effect.
5. **Teacher supply is the only factor here that moves completions** (+6.67 pp), because it
   is the only factor that changes seats and the completion draw. The declared +2.0 pp
   margin passed with room.
6. **Kin transmission is stipulated, not tested**: tied villages show +0.079 applications/hh
   over untied in the control cell (0.7855 vs 0.7065), mechanically from the imposed +0.22
   signal. Reported for completeness; it carries no evidential weight.
7. **Sensitivity, no threshold**: with the road travel reduction cut to 0.30 the interaction
   shrinks to +0.0391 (still below the 0.06 margin) — the declared margin would fail at
   either road strength.

---

## 5. Why the four thresholds failed (and what that is worth)

| Failure | Observed vs rule | Mechanism reading |
|---|---|---|
| **T14-P1c** | +24.68 vs \|Δ\| ≤ 10 total completers | A value-threshold application rule gives a sectoral shock a **participation margin** as well as a switching margin; the corner-solution shock (2.5 > aptitude range) makes this maximally visible |
| **T14-P4** | 8.35 vs ≥ 10 closed-access vacancies | The gated pool is larger than assumed and the shock pulls more of it into the field; the *direction* (posts unfilled without access) held, the declared size did not. No-shock gated vacancies were already 10.51 |
| **T15-P1** | +0.0307 vs ≥ 0.06 interaction | The interaction is a contact-probability dose effect (0.30 vs 0.70), and primary applications are partly cash-constrained and saturating; the declared margins were set above what this dose can buy |
| **T15-P3** | queue +0.0481 vs ≥ 0.05 | Marginal miss (0.002). The substantive half of the rule — admissions flat to −0.00002/hh — held exactly |

No failed threshold was re-run with different seeds, different parameters or a different
shock size. The corner solution in #14 and the near-miss in #15 are reported as-is; they are
themselves the honest content of the exercise.

---

## 6. What this does and does not show

**Can be said (about the toys, not the world):**

- A demand/remittance channel can raise origin schooling with local formal employment
  pinned flat (E13) — but only because origin seats were stipulated non-binding; with
  binding seats the same demand push would have shown up as a queue, not completions.
- An access gate can attenuate a sectoral demand signal to ~30 % of its open-access
  response while leaving a visible vacancy proxy (E14).
- Information can raise applications more where roads exist (E15, +0.031/hh) and still
  leave admissions unchanged when seats are fixed; roads can redistribute admissions
  spatially without adding a single place.
- Every magnitude here is a property of an imposed parameter: the route premium 2.4, the
  shock 2.5, the exposure probabilities 0.30/0.70, the 45 fixed local posts.

**Cannot be said:**

- Nothing here is an estimate, a calibration, or evidence for/against any historical
  claim, including the demand-pull hypothesis for massification.
- Nothing reopens the closed phase or touches R13 / R27 / C1 / A10 / R29. The admissible
  next cell remains the observed provider-entry supply-response test in
  `COUNCIL_REVIEW_014.md` §3.1, not these toys.
- The toys cannot rank mechanisms. Where a toy "confirms" an intuition, that is a property
  of its stipulated rules.

**Predeclared predictions these toys would license as hypotheses for real-data tests**
(not findings): (i) a route-opening event should move origin completion even with local
formal employment flat, and the remittance component should be the smaller part;
(ii) sectoral-demand tests must separate total participation from field switching, or they
will misread general expansion as sectoral pull; (iii) information × accessibility tests
should expect queue responses, not completion responses, wherever places are fixed.

---

## 7. Integrity notes and deviations

1. **Disclosed unit fix (T15-P3 only).** The first run compared the *per-village total*
   queue against the declaration's **per-household** margin and therefore recorded a PASS.
   The implementation was corrected to the per-household rule stated in
   `PRE_DECLARATIONS.md`: exactly two rows changed (`info_effect_queue` and
   `threshold_queues_not_places`, both now per household, 2.888 → 0.0481), the verdict
   became **FAIL**. No other estimand value or verdict changed; the only other edits were
   the definition-text clarifications noted in item 2. No model parameter, seed, draw or
   threshold was changed.
2. **Definition-text clarifications (E14, reporting only).** The observed closed/open
   ratios (0.3029, 0.3015) and the open-access vacancy level (0.00) are now written into
   the threshold-row `definition` fields so the ratios behind T14-P2 and T14-P4 are
   readable directly from `RESULTS.csv`. Values and verdicts unchanged.
3. **Control-arm calibration only.** Constants were fixed during code development against
   control-arm base rates (`code/base_rate_check.py`, control arms only; no treatment arm
   was inspected before the thresholds were frozen). No threshold was derived from an
   observed treatment effect.
4. **Determinism.** Two full runs produce byte-identical `RESULTS.csv`
   (sha256 `f8cb72d1…`). `code/verify_results.py` re-derives 17/17 verdicts from the CSV
   alone.
5. **Boundaries respected.** Writes only under `extensions_archive/toys_2026-11-20/cluster_E/`;
   no iCloud writes; no git operations; no phase, closeout or closed-anchor file read or
   written; no other cluster's directory touched.

---

## 8. Files and reproduction

```
cluster_E/
├── PRE_DECLARATIONS.md      frozen before the run (sha256-16 2cdc053aa03ae921)
├── RESULTS.csv              369 rows: all cells, contrasts, sensitivities, 17 verdict rows
├── FINDINGS.md              this file
├── RUN_MANIFEST.json        parameter vectors, seeds, verdicts, hashes, deviations
└── code/
    ├── common.py            CSV schema, label, CI helper
    ├── exp13_migration.py   #13 migration/remittance route
    ├── exp14_sector.py      #14 sector shock x field access
    ├── exp15_diffusion.py   #15 neighbour information and roads
    ├── run_all.py           writes RESULTS.csv
    ├── base_rate_check.py   control-arm base rates (design-time, writes nothing)
    └── verify_results.py    re-derives all verdicts from RESULTS.csv
```

Reproduce: `cd code && python3 run_all.py` (Python 3.10.2, stdlib only, ≈3 s) then
`python3 verify_results.py`.

— Cluster E build, brief 015 follow-on. Illustrative only; not evidence.
