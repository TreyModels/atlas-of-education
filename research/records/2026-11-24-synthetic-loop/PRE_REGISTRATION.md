# PRE-REGISTRATION — synthetic diagnostic loop v2 (Phase A)

**Task:** task-18. **Branch:** `research/synthetic-loop-2026-11-24`. **Base:** `fc96f84`.
**Committed before any Phase A run.** Everything here is **SIMULATION**: a diagnostic/trap-setter, never
evidence about real economies; no synthetic datum is reported as observed; no causal language.
**Framing:** synthetic data are a diagnostic and trap-setter for the DHS day-one micro signature, not a
substitute for surveys.

## 1. Literature worlds (fixed before any test; no fishing)

Kernel = the verified port transcription (NumPy/MLX; `synth_loop/port_backend/`). Household state kernel is the
suite's 4-state school/work continuum. Each world fixes six parameters: four utility weights
`(w_pov, w_push, w_tutor, div)`, hidden cost `h_hidden`, hostility `psi`, public quality `q_pub0`:

| world | motivation | w_pov | w_push | w_tutor | div | h_hidden | psi | q_pub0 |
|---|---|---|---|---|---|---|---|---|
| P | Basu–Van subsistence/credit | 2.0 | 0.30 | 1.3 | 0.03 | 0.30 | 0.45 | 0.62 |
| S | Nordtveit hidden costs/hostility | 0.6 | 0.55 | 1.9 | 0.05 | 0.55 | 0.55 | 0.52 |
| C | Bray/Jayachandran tutoring/crowding | 0.5 | 0.40 | 1.8 | 0.25 | 0.30 | 0.45 | 0.55 |
| R | Pritchett flat learning / low quality | 0.7 | 0.30 | 1.6 | 0.18 | 0.25 | 0.40 | 0.38 |
| 0 | zero-signal null | \multicolumn{6}{c}{`theta_0` = equal-weighted centroid; `s = 0` identical across labels} |

Strength-separable design: `theta_w(s) = theta_0 + s*(theta_w - theta_0)`, `s in {0,1}`; at `s=0` all four
labels are the same model. **Design fix (declared):** the shipped parameterisation is degenerate (shipped smoke:
GER 0.000 for two worlds, visible work 0.87–1.00). A non-confirmatory design probe fixed the magnitudes above:
at a plausible nuisance configuration the four worlds give pre-shock GER 0.46–0.63 and children-in-employment
shares 0.49–0.67, i.e. all four are non-degenerate and inside a common state space. A first version with
`w_push=1.5, psi=0.55` made the Nordtveit world structurally unable to enrol (GER 0.00) — documented and fixed
before the run. No confirmatory H1/H4/ABC output existed at amendment time.

## 2. Calibration (binding)

Six moments: pre (t=0..9) and post (t=15..24) of **GER** (share enrolled), **children-in-employment share**
(states 1|2; *not* child labour), and **study+work share of children in employment** (states 1 / states 1|2 —
the WDI `SL.TLF.0714.SW.ZS` construct). Target `M* = [0.60, 0.55, 0.27, 0.77, 0.47, 0.50]`, declared
constants anchored to WDI children-in-employment for the 8 E8 countries (mean 31.4 %, 1990–2023) and plausible
pre/post levels; **tolerance ±0.10** absolute per moment (Phase A; wide because the model's work attractor
limits attainable employment shares — a declared model limitation, not a result). Eight nuisance parameters
calibrated per world by 300 seeded random draws (RNG 424242), two calibration seeds, unmatched cells reported.

## 3. H1 — exact macro-wall test on synthetic aggregates

24 synthetic countries per world; paired country nuisance `(sigma_y, sigma_a)` from the 3x3 grid; 25 years;
fee abolition at t=10 (`tuition_only`: f_pub 0.45→0). For each country and t=10..24 compute 10-year differences;
**exact** regression `D_cl_observed = alpha + beta_w*D_GER + decade FE` with country-clustered SE, plus a paired
country-bootstrap (400) for 95% CIs and the overlap coefficient `|CI_a∩CI_b|/|CI_a∪CI_b|`; joint interaction
Wald test across the four worlds. **Decision rule (fixed):** "cannot separate" iff joint p>0.05 **and** all six
pairwise overlaps >=0.75; otherwise "separable" — and if separable, report it; do not tune to force a wall.

## 4. H4 — micro tie-breakers, Phase A (static) and Phase B (dynamic, pre-registered here)

**Phase A panel (this run):** T1 state x consumption-quintile profile, T2 hours-band shape, T3 tutoring gradient,
T4 hidden-work proxy — computed on measured variables after the survey layer (misclassification, non-response,
heaping, consumption proxy; hidden work unmeasured). Seeds: calibration k=0..19, held-out 20..79, replication
80..139. Classifier: nearest centroid on calibration standardised features, four classes; chance 1/4, 95 %
binomial band; Holm across the four tie-breakers; **admissibility gate** R²(feature ~ weights + macro moments) >
0.90 rejects; placebos: s=0 control must be at chance; label permutation; algebraic-equivalence (ban 1.8 vs 2.0,
identical kernel). Verdicts: separates / cannot separate / cannot test (F3 if all rejected).
**Phase B (pre-registered, not run):** integrate the dose-model fertility/birth-history engine; two dynamic
observables that are not algebraic transforms of the school-weight vector: (B1) **birth spacing after a child
death** — within-mother comparison of the interval following a death vs the mother's other intervals; (B2)
**parity progression / age at first birth** — schooling gradient in PPR and in age at first birth by cohort.
Same gate/placebos/out-of-seed rules; decision rule: Phase B is worth running only if at least one dynamic
observable passes the admissibility gate and beats chance out-of-seed; otherwise the DHS signature relies on
design-based identification, not on simulation screening.

## 5. Identifiability pre-audit (rejection ABC, construct-correct)

Equal-weight rejection ABC: **5,000 prior draws**, top **10 %** accepted; priors `w_pov, w_push, w_tutor ~
U(0,3)`, `div ~ U(0,0.35)`; **all nuisances logged** (fixed at the calibrated null values). Targets: WDI
`SL.TLF.0714.ZS` children-in-employment for the 8 E8 countries (mean over 1990–2023, observed) and a
declared model-scale GER target; **construct-correct**: children in employment ≠ child labour; the model's
`cl_observed` is a share of children, and the WDI series is "children in employment", not a child-labour rate;
the study+work share is a share of employed children. Identifiability gate: `(q95-q05)/(prior range) > 0.80` →
**UNIDENTIFIED**. Report the table; expect several UNIDENTIFIED (the justified pre-audit finding).

## 6. DHS day-one micro signature (deliverable; pre-registered here)

When the DHS Individual Recode arrives, run:
- **Estimand (observational):** association between completed schooling and children ever born at the individual
  level, within cohort and survey round; **not** causal.
- **Sample:** women 40–49 (completed fertility) and 25–49 (all-female secondary), DHS IR rounds for the 8 E8
  countries; DHS weights; clusters at DHS cluster, stratified by round.
- **Specification:** `CEB = beta*edu_years + cohort FE + round FE + X'gamma + error`, `X` pre-declared
  (age, age², urban, region FE, survey round); robust/clustered SE.
- **Construct split:** repeat with surviving children (CEB − dead children) as EFR; never call it TFR; report
  the EFR/TFR lead-lag and the median |difference| as a construct diagnostic.
- **Micro signature (the trap-setter's purpose):** the Phase A/B tie-breaker panel computed on DHS IR/child
  records (where available): T1–T4 if the modules exist, otherwise Phase B dynamic observables from birth
  histories (death-spacing, PPR, age at first birth); decision rule: a signature "transports" only if the DHS
  point estimate lies inside the simulation's pre-registered interval **and** the same sign/ordering appears;
  otherwise report non-transport and do not use the simulation as evidence.
- **Decision rule / power:** pre-declare MDE and CI; report null results as results.

## 7. Rules

SIMULATION labels; no synthetic-as-evidence; no causal language; failures/nulls preserved; seeds and batch
layout logged; pre-registration before each run; Phase B proposed, not sprawled.

## 8. Declared deviations log

- (to be filled)
