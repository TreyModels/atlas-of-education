# ANALYSIS — strength-separable suite redesign, H1 and H4

**Task:** task-8. **Branch:** `research/suite-redesign-2026-11-24`. **Record:**
`research/records/2026-11-24-suite-redesign/`. **Run base commit:** `9ae1337` (code committed in the commit
that follows this file; see §9). **Run wall:** 424.7 s on the Apple M1, port NumPy backend (the port's NumPy and
MLX kernel transcriptions are bit-identical — cross-check max abs diff 0.0 on all five arrays for all three
worlds).

**This is SIMULATION.** Every number below is a model-conditional statement about this stylised
parameterisation. Nothing here is history, an identified causal effect, or evidence about schooling, child
labour, fertility, or any country. The word "wall" is used only as defined in `PRE_REGISTRATION.md` §2.

**Preregistered before code:** `PRE_REGISTRATION.md` (`5084abe`), amended once before the confirmatory run
(`Amendment 1`, `9ae1337`) with the design-probe evidence (`results/design_probe.json`). No confirmatory output
existed when the amendment was committed.

---

## 1. What was run

- **H1:** 24 synthetic countries x 3 worlds x 25 years, common nuisance across worlds, paired country inputs;
  country-decade 10-year differences `D_cl_observed` on `D_GER` with decade FE and 24 country clusters;
  country-level cluster bootstrap (400 resamples, paired) for slope CIs; a pooled fully-interacted model for the
  joint interaction test.
- **H4:** moment-matching calibration of each world to a common 6-moment target `M*`; calibration block (20 seeds)
  x 3 worlds; held-out (60 seeds) and replication (60 seeds) blocks; 1,500-household repeated cross-sections in
  t = 15..24; survey measurement layer; four pre-registered tie-breakers; label-permutation, `s = 0` and
  algebraic-equivalence placebos; Holm correction; chance band.
- Backend: the port's verified `sim_step` transcription (NumPy path used, `K = 0.20`, batch layout
  `N=10 000, threads=256, blocks=40`; NumPy vs MLX check 0.0 everywhere). Seeds fixed as preregistered.

**Design deviations forced by the shipped parameterisation (Amendment 1, committed before the run).**
The shipped suite's own fees-only arm is degenerate: at t = 0 the shipped smoke reports GER 0.000 for two of
three worlds and 0.127 for the third, with visible work 0.873–1.000 and hidden work 0.000
(`results/design_probe.json`; the same numbers are in the shipped `exp1` output). A test with a non-degenerate
state space therefore required (i) `theta_0` = the equal-weighted centroid of the three shipped weight vectors,
(ii) mechanism deviations scaled by `K = 0.20` (at shipped strength the `DGP_SCHOOL_PUSH` world cannot enter
schooling at all: post-shock GER ≈ 0.03, and no nuisance vector in the searched space matches it), (iii) a
non-degenerate design point for `M*`, (iv) nine calibration nuisance parameters, and (v) a ±0.05 absolute
macro-match tolerance instead of ±0.02. These are declared in `PRE_REGISTRATION.md` §7 and are design
amendments, not results.

---

## 2. H1 — the macro wall, tested properly: **separable**

The main regression (`D_cl_observed` on `D_GER`, decade FE, country-clustered SE; 360 country-decade rows per
world):

| world | macro slope `beta_w` | clustered SE | bootstrap 95% CI |
|---|---|---|---|
| P (subsistence) | **-0.155** | 0.013 | [-0.178, -0.116] |
| S (school push) | **-0.027** | 0.003 | [-0.031, -0.017] |
| C (crowding/tutoring) | **-0.270** | 0.020 | [-0.312, -0.212] |

- Joint interaction test (world x `D_GER`, two restrictions): **Wald chi2(2) = 112.0, p = 4.8e-25**.
- Pairwise slope-CI overlap coefficients: **P–S 0.00, C–P 0.00, C–S 0.00** (the preregistered wall criterion
  requires all three >= 0.75 and p > 0.05).

**Verdict: `separable`.** Under a real country-decade FE regression with an explicit slope-overlap statistic,
the three mechanism worlds are **not** macro-equivalent: the schooling–employment slope differs by a factor of
about 10 between the school-push and crowding worlds, and the 95% CIs do not overlap at all.

**Interpretation (simulation-conditional).** In this stylised model the "macro wall" is **not reproduced**. The
shipped suite never ran this test (audit §6.1); when it is run, the mechanisms are distinguishable at the macro
level because the fee shock interacts very differently with the mechanism weights. This does **not** falsify the
Atlas's empirical wall (E1/Q3 are about country panels, not this model); it says the wall cannot be *derived*
from this ABM, and equally that the ABM's macro behaviour is not "everything is development".

---

## 3. H4 — measured tie-breakers: **cannot test** (all rejected by the anti-tautology gate)

**Calibration (all worlds matched, residuals reported, not hidden):** `M* = [GER_pre 0.307, cl_pre 0.875,
sw_pre 0.183, GER_post 0.520, cl_post 0.789, sw_post 0.309]`; max |residual| — **P 0.0279, S 0.0406, C 0.0235**
(all <= 0.05). `s = 0` calibration residual 0.0233.

**Control identities (both pass):**
- `s = 0` worlds are **exactly identical**: max abs per-household difference 0.0 over five seeds (F1 pass).
- `s = 0` tie-breaker classification accuracy **0.333** (chance band [0.264, 0.402]).
- Algebraic-equivalence placebo (`ban = 1.8` vs `ban = 2.0`, identical kernel outputs; max abs diff **0.0**):
  binary accuracy **0.500** for all four tie-breakers (band [0.411, 0.589]; P3 pass).
- Label permutation: observed accuracies 1.000 vs permuted 95th percentiles 0.711–0.895 (p = 0.01–0.02).

**Descriptive accuracy (held-out n = 180; replication n = 180):** T1 1.000 / 1.000; T2 1.000 / 0.994;
T3 1.000 / 1.000; T4 1.000 / 1.000. **These numbers are not evidence of a tie-breaker** — see the gate below.

**Admissibility gate (preregistered, calibration block only):** regressing each measured feature on the known
DGP weights + macro moments gives **R^2 = 0.986 (T1), 0.974 (T2), 0.990 (T3), 0.991 (T4)** — all above the
pre-registered 0.90 threshold. **Every tie-breaker is rejected as a transform of the mechanism weights** and is
ineligible for the confirmatory test (F3).

**Matching-premise diagnostic (reported, not in the decision rule):** a macro-moments-only classifier reaches
**1.000** accuracy on the held-out units. The ±0.05 moment matching does not fully condition out macro
differences, so even if a tie-breaker had passed the gate, separation could not be attributed to micro data.

**Verdict: `cannot test` (F3)** — the model's measured observables are construction-implied functions of the
mechanism weights, and the macro-matching premise is only partially satisfied. The 1.000 accuracies are exactly
the tautology the audit warned about (audit §5), surviving a redesigned DGP, a measurement layer and moment
matching.

---

## 4. What this establishes

1. **The shipped suite's design was degenerate, not just untested.** Its fees-only arm sits at GER ≈ 0 and
   visible work ≈ 1, and its `DGP_SCHOOL_PUSH` world cannot enter schooling at all. Neither H1 nor H4 could ever
   have been run on it, which is why the audit's "not implemented" finding matters more than a coding bug.
2. **A real macro test does not reproduce the wall in this model.** With country-decade FE and a slope-overlap
   statistic, the three mechanisms are separable (p ≈ 5e-25; zero CI overlap). **The empirical aggregate wall
   stands as an empirical finding** — E1's 5/272 travelling links, Q3's 87 % minority-effect mislabelling, Q1's
   MSE/BIC zero-signal failures — **but the claim that this simulation *demonstrates* a generic collapse is not
   supported**: under separable mechanisms the slopes separate. "The wall" is a property of country panels, not
   of micro mechanism algebra, and the suite must not be cited as evidence that any set of distinct micro
   mechanisms necessarily collides in aggregate regressions.
3. **The micro tie-breaker remains untestable with model-derived observables.** After stronger separation, a
   survey measurement layer, and macro-moment matching, every candidate observable is predicted by the DGP
   weights at R^2 ≈ 0.97–0.99. **The tie-breaker question therefore remains open, not answered**: it is exactly
   why external measured microdata (tutoring / hidden-work / child-labour surveys, DHS Individual Recode) is
   required next, rather than a better classifier or a cleverer transform of model states.

**What would be needed next (not done here):** (i) a model whose mechanisms are faithful to the citations rather
than reduced-form weights; (ii) observables whose variation is not a deterministic function of the weights
(measurement-error structure, heaping/non-response correlates, real survey items); (iii) real microdata (DHS
Individual Recode route) to replace model-imputed proxies; (iv) an explicit unobserved-type dimension so that
conditional-on-macro micro variation is not identified by construction. Until then, the suite should not be used
to support the wall or any tie-breaker claim.

---

## 5. Limitations

- Model-conditional only; three stylised worlds; single machine; one design point (`K = 0.20`) chosen before the
  run and reported as a design amendment, not a result.
- The ±0.05 macro-match tolerance is wide; the macro-only control (accuracy 1.000) shows the matched worlds
  still differ in 10-year changes, so the H4 "conditional on matched macro moments" premise is only partially
  met.
- Survey measurement constants (misclassification, non-response, heaping, tutoring error) are design assumptions,
  not estimates; they are preregistered and are not tuned to any output.
- H1's 24 countries are synthetic and share one nuisance distribution; the country dimension is a device to run a
  real panel regression, not a country sample.
- H4's admissibility gate is pre-registered at R^2 > 0.90; it rejects all four observables here. That is the
  honest outcome, not a bug to be tuned away.

## 6. Files

`suite_redesign/model.py` (strength-separable worlds over the port kernel), `measure.py` (survey layer,
tie-breakers), `macro.py` (country panel, clustered FE, bootstrap, overlap), `calibrate.py` (M*, moment
matching), `tiebreak.py` (units, classifier, placebos, Holm), `run_all.py` (orchestration), `port_backend/`
(vendored, unmodified port kernel + provenance), `results/{calibration,h1_macro_wall,h4_tiebreakers,
run_manifest,design_probe}.json`. The upstream suite copy in `suite/unified_gpu_suite/` is untouched.

## 7. Reproduce

```bash
cd research/records/2026-11-24-suite-redesign/suite_redesign
PYTHONPATH=$PWD REDESIGN_BACKEND=numpy \
  /Users/treymenefee/atlas-work-2026-11-23/apple-venv310/bin/python run_all.py   # ~7 min
```

Deterministic given the pinned seeds and the nine-parameter search RNG (424242); two consecutive runs produced
identical calibration, H1 and H4 numbers (only wall time differed).

## 8. Declared deviations (append-only)

- **Amendment 1** (committed before the confirmatory run, `9ae1337`): theta_0 = centroid of the shipped vectors;
  mechanism scale `K = 0.20`; M* at a non-degenerate design nuisance; nine calibration nuisances (four original +
  mu_y, mu_a, w_child, shadow_cost, q_pub0); 800 candidates (was 200); match tolerance ±0.05 (was ±0.02). Reasons
  and probe numbers in `PRE_REGISTRATION.md` §7 and `results/design_probe.json`.
- **Verdict-logic fix before reporting:** the first pipeline execution counted tie-breakers that the
  admissibility gate had rejected as "separators"; corrected to treat rejected tie-breakers as ineligible (F3)
  before the reported run. The numerical outputs (calibration, H1 slopes, accuracies, placebos) were unchanged;
  only the verdict bookkeeping changed.
- Run base commit `9ae1337`; code committed in the follow-up commit; no numbers were changed after inspection.

## 9. Bottom line

- **H1: separable** — a real country-decade FE + overlap test does not reproduce the macro wall in this model
  (slopes -0.155 / -0.027 / -0.270; joint p = 4.8e-25; no CI overlap).
- **H4: cannot test (F3)** — all four measurement-layer tie-breakers are construction-implied transforms of the
  mechanism weights (R^2 0.974–0.991); the 1.000 out-of-seed accuracies are tautological; `s = 0` and the
  algebraic-equivalence placebo both fall exactly to chance, so the machinery is sound and the rejection is the
  model's, not the test's.
- **Neither result supports any real-world claim.** The suite's forward programme cannot validate the wall or a
  tie-breaker until the model and its observables change (see §4).
