# PRE-REGISTRATION — strength-separable suite redesign and honest H1/H4 test

**Task:** task-8. **Branch:** `research/suite-redesign-2026-11-24`. **Record:**
`research/records/2026-11-24-suite-redesign/`. **Base:** `9242214` (`origin/research/handoff-2026-11-24`).
**Written and committed BEFORE any redesign code was written and BEFORE any redesign output was inspected.**

**Status:** simulation methodology. Everything produced under this pre-registration is **SIMULATION**: a
model-conditional statement about this parameterisation, not history, not an identified causal effect, and not
evidence about schooling, child labour, fertility or policy. No causal language is permitted except in the
event-study style ("consistent with") and none is planned.

**Why this exists.** The audit (`research/suite-lit-review-2026-11-24` @ `4649cae`, `AUDIT.md` §6.1–6.3, §9)
shows that the shipped `exp1/exp2/exp3` do not implement their own pre-registered tests: exp2 contains no macro
FE regression and no slope-overlap statistic (H1 undefined); `strength` appears only in a docstring, so the Q1
zero-signal control (H4) cannot run; the four "micro signatures" are transforms of the same state mix, so
classifier recovery is tautological. The tie-breaker design note
(`research/suite-tiebreakers-2026-11-24` @ `e526c94`) specifies the required redesign. This pre-registration
operationalises that redesign and fixes every decision rule **before** code and results.

---

## 1. Model, worlds, strength parameter

**Kernel reuse.** The simulator is the port's verified transcription of the suite's CUDA `sim_step`
(`research/apple-silicon-gpu-2026-11-24` @ `52d74ec`: NumPy/MLX transcription, bit-identical across backends,
verified against 10 real CUDA launches with 0 integer mismatches). It is vendored unmodified into
`suite_redesign/port_backend/` with provenance. The redesigned scripts never edit the upstream suite copy.

**Household state kernel (unchanged semantics).** Four states: 0 school-only, 1 study+work, 2 visible work only,
3 hidden work. Utilities are the kernel's linear forms in `(w_pov, w_push, w_tutor, div_beta)` plus fixed
constants; the kernel is called once per simulated year with the year's scalars.

**Strength-separable worlds (binding).** Parameter vector
`theta_w(s) = theta_0 + s * Delta_w`, `w in {P, S, C}`, `s in {0, 1}`:

- `theta_0 = (w_pov=0.20, w_push=0.20, w_tutor=0.20, div=0.02)` — common baseline;
- `Delta_P = (+2.00, -0.10, +0.60, 0.00)` → `theta_P(1) = (2.20, 0.10, 0.80, 0.02)`;
- `Delta_S = (0.00, +1.80, +0.60, +0.03)` → `theta_S(1) = (0.20, 2.00, 0.80, 0.05)`;
- `Delta_C = (+0.10, +0.10, +2.00, +0.20)` → `theta_C(1) = (0.30, 0.30, 2.20, 0.22)`.

These `theta_w(1)` are exactly the shipped suite's `DGP_POVERTY`, `DGP_SCHOOL_PUSH`,
`DGP_CROWDING_TUTOR` weights, so the redesign is anchored to the existing design constants rather than inventing
new ones. At **s = 0 all three worlds are the same model** (`theta_0`): the zero-signal world is the null
control, not a fourth DGP label (fixing audit §6.2). The shipped `DGP_MIXED` is **not** a mechanism (audit §3.4,
claim 10 withdrawn) and is not a confirmatory world.

**Identity check at s = 0 (pre-declared failure F1).** With the same seeds and inputs, the three labels at
s = 0 must produce identical per-household arrays. A two-sample KS test per simulated year on the state mix and
on `work_hrs` must give p > 0.01 for all years; otherwise the redesign has failed and no control claim is made.

**Arms and shock.** Only the suite's `tuition_only` arm is used (fee abolition at t = 10): `f_pub` 0.45 → 0.00,
`h_hidden = 0.35`, `psi = 0.45`, `ban = 0` before and after. Fixed kernel constants: `w_child = 0.55`,
`shadow_cost = 0.32`, `q_pub` starts at 0.65 and follows the suite's dilution rule with `cap_scale = 0.30`,
`y_sub = y_sub0 * 0.985^t`. `y_sub0 = 0.90` unless a calibration cell sets it.

**Batch layout (pinned and logged).** Per aggregated run: `N = 10,000` households per country/unit,
`threads = 256`, `blocks = ceil(N/256) = 40`, `T = 25` years (t = 0..24), backend `mlx` (NumPy fallback), and
the launch layout is written to every results file.

---

## 2. H1 — the macro wall, operationalised as a real country-decade FE test

**Design (unmatched nuisance, common across worlds — the wall is about mechanism content, not calibration
leakage).** 24 synthetic countries. Country `c` gets a nuisance pair `(sigma_y, sigma_a)` assigned cyclically
from the 3x3 grid `sigma_y in {0.45, 0.55, 0.65}` x `sigma_a in {0.15, 0.20, 0.25}`; the same pair, the same
household inputs (`base_y`, `ability`), and the same household seed `20270101 + 100*c` are used for country `c`
in **all three worlds** (paired design). `sigma_y`, `sigma_a` are the only country-level heterogeneity.
`f_pub_pre = 0.45`, `y_sub0 = 0.90` for all countries.

**Observed macro aggregates (not kernel internals).** `GER = share(state <= 1)`; `cl_observed = share(state in
{1,2})` (children in employment; hidden work is unmeasured in real data and is excluded — audit §7.3). Both are
what a survey-like aggregate would report.

**Panel and regression.** For each country and each `t in {10..24}`, the 10-year change
`D_x(t) = x(t) - x(t-10)`; decade bin `d(t) = 1` for t in 10..14, 2 for 15..19, 3 for 20..24. Estimate, per
world,

    D_cl_observed = alpha + beta_w * D_GER + decade FE + e,   E[e | country] clustered by country,

by OLS with country-clustered SE (24 clusters). `beta_w` is the macro slope.

**Slope-overlap statistic (pre-declared).** A country-level cluster bootstrap (400 resamples of the 24
countries, same resample across worlds to preserve pairing) gives a 95% percentile CI for each `beta_w`. For
each pair `(w, w')` the overlap coefficient is
`O = length(CI_w ∩ CI_w') / length(CI_w ∪ CI_w')`. Estimate a pooled fully-interacted model
`D_cl_observed = world FE + decade FE + world x D_GER` with country-clustered SE and test the two interaction
coefficients jointly (Wald).

**Decision rule (fixed).** H1 result = **"cannot separate"** (the wall holds in this redesign) iff the joint
interaction test has p > 0.05 **and** `O >= 0.75` for all three pairs. Otherwise H1 result = **"separable"**,
reporting the slopes, CIs, overlaps and the interaction p. Either verdict is a legitimate result; neither is a
statement about real economies. Secondary outcome: `D_GER` regressed on `D_cl_observed` (reverse direction),
reported with the same statistics but not part of the decision rule.

---

## 3. H4 — micro tie-breakers on measured observables, with a zero-signal control

### 3.1 Units, seed blocks, and pairing

- Seed block index `k`: calibration `k = 0..19`, held-out `k = 20..79`, reserved replication `k = 80..139`.
  Unit seed `s_k = 20261125 + 100*k`.
- One unit = one (seed, world label, s) cell summarised on **measured** survey variables over post years
  `t = 15..24` (ten repeated cross-sections; states, tutoring, hours and the consumption proxy at t = 10..14 are
  not used).
- Primary test: `n = 180` units = 60 held-out seeds x 3 worlds at s = 1 (per-world recall n = 60).
- Replication: the same design on `k = 80..139` (n = 180).
- s = 0 control: held-out seeds x the 3 labels at s = 0 (n = 180); by construction the model is identical.

### 3.2 Macro-moment matching (calibration, binding)

**Target vector M\* (fixed by rule, not by outcome).** Moment vector
`M = (pre GER, pre cl_observed, pre study_work, post GER, post cl_observed, post study_work)` where pre = mean
over t = 0..9 and post = mean over t = 15..24. `M*` is defined as the **theta_0 model at the default nuisance**
(`sigma_y = 0.55`, `sigma_a = 0.20`, `f_pub_pre = 0.45`, `y_sub0 = 0.90`) averaged over the five calibration
seeds `k = 0..4`, computed once by `calibrate.py` and written to `results/calibration.json` **before** any
confirmatory profile is generated. It is a property of this model, not of real data and not of any world's
s=1 outcome.

**Nuisance parameters calibrated per world at s = 1:** `sigma_y in [0.35, 0.75]`, `sigma_a in [0.12, 0.30]`,
`f_pub_pre in [0.35, 0.55]`, `y_sub0 in [0.75, 1.05]` (4 parameters; everything else fixed). Search: 200
uniform-random candidates from a fixed RNG seed (`424242`), each evaluated on two calibration seeds (`k = 0,1`),
on the six moments of M. A cell is **macro-matched** if all six moments are within `±0.02` absolute of M*.
Choose the matched candidate minimising `max_abs_residual`; ties broken by lowest candidate index. If no
candidate matches, the world is **unmatched** (failure F2) and is excluded from the confirmatory H4 test;
the exclusion is reported and must not be described as a result about that mechanism.

**s = 0 calibration.** The s = 0 model is the same in all labels; calibrate it once against M* with the same
search and use the matched nuisance for all three labels. If it cannot be matched, F2 applies to the control.

### 3.3 Survey measurement layer (all tie-breakers use measured variables only)

Applied independently per unit-year: a simple random sample of 1,500 households from N = 10,000 (repeated
cross-section each year; equal weights), then, with the unit-seed RNG:

- **State reporting** (misclassification, pre-declared constants): true 0 → reported 0 (0.95) / 1 (0.05);
  true 1 → 1 (0.70) / 2 (0.20) / 0 (0.10); true 2 → 2 (0.80) / 1 (0.20); true 3 (hidden work) → **0 (0.60) /
  1 (0.40) — never reported as employment** (hidden work is unmeasured by design; audit §7.3, claim 9).
- **Hours:** recorded only for children reported in 1 or 2. True `work_hrs`, then for hidden-work children
  reported in 1 multiply by 0.5 (under-report), round to the nearest 5, add N(0, 2), clip to [1, 60].
- **Tutoring:** true take-up, reported with false-negative 0.20 and false-positive 0.05.
- **Consumption proxy:** `y_hh * lognormal(mu=0, sigma=0.35)`; quintiles from cut points fixed on the
  calibration block (pooled calibration units), applied to held-out/replication.
- **Item non-response:** state 3 %, hours 5 % (among reported employed), tutoring 4 %, consumption 6 %;
  missing at random, deleted per item. Shares are computed on non-missing denominators.

All constants above are design assumptions, labelled as such; they are not estimated.

### 3.4 Tie-breaker panel (four candidates, each a vector)

- **T1 — state x consumption-quintile profile.** Visible-work share in Q1–Q2; study+work share in Q2–Q4;
  school-only share in Q4–Q5; total-variation distance of the reported state mix between Q1 and Q5. (4 dims)
- **T2 — hours-band shape among reported-employed children.** Shares in ILO-style bands 1–13 h, 14–27 h,
  28–42 h, >=43 h; interquartile range. (5 dims)
- **T3 — tutoring gradient.** Tutoring take-up in Q4–Q5 minus Q1–Q2. (1 dim)
- **T4 — hidden-work proxy.** School-only share among reported children in Q1–Q2 (a lower-bound proxy for
  unmeasured hidden work). (1 dim)

Observables the model cannot emit (grade attainment, learning by grade, tutoring expenditure, teacher agent)
are **not tested** and are listed as required model extensions (audit §11 P0-7; tie-breaker note R4).

### 3.5 Classifier, admissibility gate, placebos, multiple testing, chance band

- **Classifier (fixed):** standardise each T using calibration-block means/SDs; nearest-centroid
  (three calibration centroids); ties to lowest world index. No tuning, no feature selection, no comparison of
  classifiers (audit §6.2 rationale).
- **Admissibility gate (tie-breaker note §2.3):** on the calibration block only, regress each component of T on
  `1 + w_pov + w_push + w_tutor + div + D_GER + D_cl_observed` (known in simulation). If any component has
  `R^2 > 0.90`, T is rejected as a transform of the DGP weights and not tested.
- **Chance band:** for 3-class, n = 180, `p = 1/3`, the 95 % binomial band is
  `p +/- 1.96*sqrt(p(1-p)/n) = [0.264, 0.402]`. "Beats chance" requires accuracy above the upper bound **and**
  a one-sided exact binomial p < 0.05, Holm-corrected across the four tie-breakers.
- **Placebos:** (P1) s = 0 control accuracy must lie inside the chance band; (P2) label permutation: 100
  permutations of the calibration labels, refit centroids, report the permutation accuracy distribution and a
  permutation p-value — the reported accuracy must not exceed the 95th percentile; (P3) algebraic-equivalence
  pair: the kernel's ban enters as a threshold (`ban > 0`), so `ban = 1.8` and `ban = 2.0` produce **identical
  utilities and identical outputs**; a binary classifier between those two "worlds" (60 held-out seeds x 2,
  n = 120) must lie in the 95 % chance band around 0.5 (`[0.411, 0.589]`); if it does not, the classifier is
  manufacturing signal and H4 is **invalid**.
- **Verdict categories (fixed):** (i) **"separates"** if at least one tie-breaker beats chance out of seed
  after Holm and survives replication; (ii) **"cannot separate"** if none does; (iii) **"cannot test"** if F1,
  F2 or P3 fails. Report all four tie-breakers, including rejected and null ones.

---

## 4. Failure categories (fixed in advance)

- **F1:** s = 0 worlds not identical (KS p <= 0.01 in any year) -> the control cannot run; no H4 claim.
- **F2:** a world (or the s = 0 control) cannot be matched to M* within ±0.02 -> excluded from H4, reported.
- **F3:** admissibility gate rejects all four tie-breakers -> H4 = cannot test (report R^2).
- **F4:** placebo P3 fails -> H4 invalid.
- **F5:** H1 countries unusable (missing years/NaNs) -> H1 cannot test.

## 5. Reporting rules

Every number in `ANALYSIS.md` is SIMULATION; the phrase "the wall" is used only as defined in §2's decision
rule; no claim about real countries, no causal verb, no "robust", no "identified". Data tiers: simulated
(model) throughout; the consumption proxy is model-imputed and labelled so. Seeds, batch layout, backend,
wall time, code commit and the calibration table are written into `results/run_manifest.json`. Failures,
unmatched cells and nulls are preserved. Any change to a rule above after results are seen voids the
confirmatory status and requires a dated amendment.

## 6. Declared deviations log (append during work)

- (to be filled)
