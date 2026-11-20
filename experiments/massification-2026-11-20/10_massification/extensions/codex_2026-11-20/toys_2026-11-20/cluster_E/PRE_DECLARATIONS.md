# PRE-DECLARATIONS — Cluster E toys (#13, #14, #15)

**Status: ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no historical test; phase closed; do not cite numbers as estimates.**

This file was **frozen before the run**. It states the imposed parameter vectors, the
paired-counterfactual design, the predeclared thresholds, the verdict rules and the
falsifiers for the three Cluster E experiments of `COUNCIL_TOY_SPECS_015.md`
(§Cluster E, #13–#15). No threshold below was chosen by looking at a treatment-arm
result. Constants were fixed during code development using **control-arm base rates
only** (`code/base_rate_check.py` prints control arms only), so that the control cell
is neither at a floor nor at a ceiling.

Scope and non-claims:

- These are small stdlib toy models built on `model.py` / `takeoff.py` / `diffusion.py` logic.
- They are **not** estimates, **not** calibrations, **not** evidence about any historical case.
- They do **not** reopen the closed massification phase and say nothing about R13/R27/C1/A10/R29.
  No phase file, closed-anchor file, results table or git branch is touched.
- A threshold **PASS** below means only: *the stipulated rules mechanically generate the
  declared pattern*. It is a property of the assumptions, not of the world.
- **All** arms are reported, including failures and sensitivity arms.

---

## Protocol commitments (all three experiments)

| Item | Commitment |
|---|---|
| Language / deps | Python 3.10, stdlib only (`random`, `csv`, `statistics`, `math`) |
| Seeds per cell | **200** (exceeds the ≥100 requirement; ≥200 where cheap) |
| Pairing | All latent draws are generated **once per seed** by a single `draw(seed)` and shared verbatim by every arm; arms differ only in the stipulated factor. Contrasts are within-seed paired differences. |
| Matched starting conditions | Identical latent cohort/households/villages and identical initial state (diaspora stock, seat counts) across arms |
| One-factor shocks | Each contrast changes exactly one stipulated factor; the 2×2 / 2×2×2 designs hold everything else fixed |
| Estimand reporting | Applications, admissions and completions are reported separately; readiness is never conflated with completion |
| Uncertainty | Mean of paired per-seed differences, sample sd, normal-approximation 95% CI (z = 1.959964, n = 200) |
| All cells | Every arm is written to `RESULTS.csv`, PASS or FAIL, including the auxiliary sensitivity arms (labelled `sensitivity`, no threshold) |
| Labels | Every row carries `ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence; ...` |
| Writes | Only `extensions_archive/toys_2026-11-20/cluster_E/`; no iCloud writes; no git commit |

Seed schedule: E13 `20261120+0…199`; E14 `20461120+0…199`; E15 `20661120+0…199`.

---

## #13 — Migration and remittance route

**Question.** Can an external credentialed job route pull origin schooling while local
jobs stay flat, and do remittances add a *smaller*, positive effect?
**Arms** (2×2, paired): route {closed, open} × remittances {off, on} = 4 cells.
**Auxiliary sensitivity** (no threshold test): route premium halved to 1.2, route
open vs closed, remittances off.

### Imposed parameter vector (stipulated, illustrative)

| Parameter | Value | Meaning |
|---|---|---|
| `N` | 200 | origin households, re-exposed for `T = 20` school cycles |
| `SEATS_ORIGIN` | 170 | origin secondary seats — **deliberately non-binding** (peak applications ≈ 150); stated stipulation, isolates the demand channel |
| `FEE` | 1.0 | secondary fee (model.py public fee) |
| `INDIRECT` | 0.8 | uniforms/transport paid in cash; attendance cash cost = 1.8 |
| `V0`, `APT_VALUE` | 2.6, 0.6 | base demand for the credential + aptitude weight |
| `ROUTE_PREMIUM` | 2.4 | extra credential value when the external route is open *and* the household has route access |
| `ROUTE_ACCESS_P` | 0.45 | probability a household has route access (network/portability) |
| `REMIT_AMOUNT`, `KIN_P`, `M_REF` | 0.8, 0.35, 40 | remittance per kin-linked household per cycle, scaled by `min(1, M_prev/40)` |
| `DIASPORA` | 20 | pre-existing migrants at t=0 (keeps the closed/remit-on cell non-empty) |
| `LOCAL_JOBS` | **45, constant in every arm and cycle** | local formal labour demand is flat **by construction** |
| completion draw | `p = 0.82 + 0.12·aptitude` | per admitted pupil per cycle |
| migration draw | `p = 0.55 + 0.25·aptitude`, route open + route access only | per completer per cycle |
| decision rule | apply iff `v_i − c_i ≥ FEE` **and** `b_i + R_i ≥ FEE + INDIRECT` | demand + cash constraints |
| cash / opportunity cost / aptitude | `b ~ U(1.5, 3.5)`, `c ~ U(0, 3.5)`, `a ~ U(0,1)` | latent, shared across arms |

Migration is counted **once**: `unique_migrants` = unique persons who ever migrated over
the 20 cycles; the per-cycle flow is reported separately and not used as the headline.

### Predeclared thresholds (verdict rules)

| ID | Threshold | Verdict rule |
|---|---|---|
| **T13-P1a** | Remittances (route open) raise **applications by ≥ 4.0 persons per cycle** (= +2.0 pp of the 200-household cohort). **Declared sign: positive.** | PASS iff mean paired Δapps ≥ 4.0 |
| **T13-P1b** | Remittances (route open) raise **secondary completion by ≥ 1.0 pp** of cohort. **Declared sign: positive.** | PASS iff mean paired Δcompletion_pp ≥ 1.0 |
| **T13-P2** | Opening the route (remittances off) raises secondary completion by **≥ 8.0 pp**, declared sign positive, **while local formal jobs filled stay exactly 45**. | PASS iff mean paired Δcompletion_pp ≥ 8.0 |
| **T13-P3** | Local formal posts filled are **identical (45) in every arm and every seed**: flat local labour demand by construction. | PASS iff max absolute paired difference = 0 |
| **F13** (falsifier) | "No or perverse effect": triggered if the route completion effect is < 2.0 pp **or** ≤ 0, **or** the remittance application effect is ≤ 0. | PASS (not triggered) iff both channels operate with the declared positive sign and the route clears 2.0 pp |

**Declared auxiliary predictions (no pass/fail):** the route effect should survive
halving the premium with the same sign; and local output should *fall* under the open
route, because migrants are selected from completers (brain drain) while the local post
count is held at 45. Both are reported.

---

## #14 — Sector-demand shock × field access

**Question.** Does a sector-specific demand shock reallocate cohorts into the targeted
field, or just raise overall enrolment — and does reallocation require field access?
**Arms**: shock {none, targeted A, placebo B} × access {open, closed} = 6 conditions;
the 4 shocked cells are each paired against their access-matched no-shock baseline.
**Auxiliary sensitivity** (no threshold test): gate tightened to 15%.

### Imposed parameter vector (stipulated, illustrative)

| Parameter | Value | Meaning |
|---|---|---|
| `N` | 200 | school leavers per seed; each applies to one field |
| `V_BASE`, `APT_VALUE` | 1.2, 1.0 | base value + field-specific aptitude weight |
| `RETURN_BASE` | 2.0 | baseline field return |
| `SHOCK` | **2.5** | one-factor addition to the shocked field's return only |
| `FEE` | 1.0 | application fee; cash `b ~ U(0.8, 2.8)` |
| `SEATS` | **150 per field — deliberately non-binding** (peak field-A applications ≈ 150); stated stipulation isolates access/demand from seats |
| `GATE_SHARE` | 0.30 | closed access: field A open only to the top 30 % of the gate score (tracking / credential gate); field B always open |
| licence draw | `p = 0.80 + 0.12·aptitude_f` | licensed completers |
| sector posts | 30 base, **+25 in the shocked sector** | vacancy proxy = `max(0, posts − completers)` |
| opportunity cost | `c ~ U(0, 3.5)` | net value `v_if − c_i`; apply iff `net ≥ FEE` and allowed and affordable |

### Predeclared thresholds (verdict rules)

| ID | Threshold | Verdict rule |
|---|---|---|
| **T14-P1a** | Open access: the targeted shock raises **field-A applications by ≥ 30 persons**. | PASS iff mean paired Δapps_A ≥ 30 |
| **T14-P1b** | Open access: the targeted shock raises **field-A licensed completers by ≥ 25 persons**. | PASS iff mean paired Δcompleters_A ≥ 25 |
| **T14-P1c** | The shock **reallocates rather than raises** overall enrolment: |Δ total licensed completers| ≤ 10. | PASS iff |mean paired Δcompleters_total| ≤ 10 |
| **T14-P2a** | Closed access: field-A **application** response ≤ **50 %** of the open-access response. | PASS iff ratio ≤ 0.50 |
| **T14-P2b** | Closed access: field-A **completer** response ≤ **50 %** of the open-access response. | PASS iff ratio ≤ 0.50 |
| **T14-P3** | Placebo symmetry: an open-access shock to field B moves **B applications by ≥ +30 and A applications by ≤ −20**. | PASS iff both hold |
| **T14-P4** | Demand without access shows up as vacancies: after the targeted shock, sector-A unfilled posts ≥ **10** under closed access and ≤ **3** under open access. | PASS iff both hold |
| **F14** (falsifier) | "Demand works without access": triggered if the closed-access field-A response (applications **or** completers) is at least the open-access response. | PASS (not triggered) iff both ratios < 1.0 and closed completers < open completers |

---

## #15 — Neighbour information and roads

**Question.** Do prestigious-neighbour information, road access and teacher supply have
separable effects on applications — and does information raise applications **more**
where accessibility is high?
**Arms**: info {0,1} × road {0,1} × teacher {0,1} = 8 factor cells × 2 village tie types
(untied, kin-tied) = 16 reported cells, all paired within seed.
**Auxiliary sensitivity** (no threshold test): road travel reduction 0.30 instead of 0.55.

### Imposed parameter vector (stipulated, illustrative)

| Parameter | Value | Meaning |
|---|---|---|
| `H` | 60 households per village; two villages per seed (untied = 0, kin-tied = 1) | 120 households pooled per arm-seed |
| seats | primary/secondary/tertiary `(16, 6, 2)`, **+1 per level if teacher = 1** | admissions capped by seats; seats bind at every level |
| fees | `(0.19, 0.34, 0.52)` + `INDIRECT 0.12` | per level |
| travel | `(0.10 + 0.55·distance)·(1 − 0.55·road)/(1 + seats/15)` | distance acts at every level |
| value | `V0_k + 0.45·aptitude + SIGNAL_k·signal`, `V0 = (0.95, 1.55, 2.15)`, `SIGNAL = (0.35, 0.70, 0.95)` | |
| signal | `0.16 + 0.34·exposed + 0.22·tied` | |
| **information travels on roads** | `exposed = info ∧ (u_expo < 0.30 + 0.40·road)` | explicit stipulated mechanism: contact probability 0.30 (no road) vs 0.70 (road) |
| **kin transmission** | `+0.22` signal in tied villages | **STIPULATED ASSUMPTION**, labelled; not a test of the world |
| work penalty | `work·(0.80, 1.05, 1.30)_k`, `work ~ U(0.45, 1.20)` | |
| cash | `0.25 + 0.34·(i mod 3) + 0.28·U` | |
| completion draw | `p = 0.78 + 0.06·teacher + 0.08·aptitude` | |

Because seats bind at every level, the toy's structural prediction is
**applications up / admissions flat / queues up**. This is predeclared as T15-P3, not
discovered after the fact.

### Predeclared thresholds (verdict rules)

| ID | Threshold | Verdict rule |
|---|---|---|
| **T15-P1** | The information effect on applications/household is **≥ 0.06 larger at road = 1 than at road = 0**; the road = 1 effect is **≥ 0.10** and the road = 0 effect is **≤ 0.06**. Declared sign: positive interaction. | PASS iff all three hold |
| **T15-P2** | Separable independent effects, declared signs positive: road main effect on applications **≥ +0.05/hh**; teacher main effect on completions **≥ +2.0 pp**; info main effect on applications **≥ +0.03/hh**. | PASS iff all three hold |
| **T15-P3** | Information moves queues, not places: information effect on admissions **≤ 0.02/hh in absolute value** while unmet applications rise by **≥ 0.05/hh**. | PASS iff both hold |
| **F15** (falsifier) | "No interaction": triggered if the difference-in-differences is **< 0.03 applications/hh** in absolute value; the diffusion story would then collapse to capacity. | PASS (not triggered) iff |diff-in-diff| ≥ 0.03 |
| **T15-S** (stipulated, not a test) | Kin-tied villages show higher applications than untied villages. This follows from the stipulated `+0.22` signal and is reported as an **assumption**, not a finding. | no pass/fail |

---

## Reading rules (fixed now, not after the run)

1. A PASS is evidence only that the stipulated rules generate the declared pattern; the
   parameter vector is printed in full so a reader can see how much of the result is
   assumption.
2. A FAIL is reported with the same prominence as a PASS and is **not** re-run with a
   different seed set or parameter value.
3. The auxiliary sensitivity arms carry no verdict; they are reported to show whether a
   declared margin is fragile to a stipulated parameter size.
4. Nothing here adjudicates the closed phase, R13, R27/C1, A10/R29, or any historical
   claim. No number from this directory may be cited as an estimate.

— Cluster E build, brief 015 follow-on (design frozen before run)
