# Pre-registration: micro tie-breaker observables for the GPU suite (v1.0)

**Record:** `research/records/2026-11-24-suite-tiebreakers/` · branch `research/suite-tiebreakers-2026-11-24`
**Base commit:** `f7c2e1a` (`origin/research/handoff-2026-11-24`, which contains the payload at `51f9f02`).
**Author:** suite-auditor (task-4, Job B). **Written:** 2026-11-24 (UTC), **before any tie-breaker test**.
**Status:** DESIGN ONLY. No simulation was run for this document; no suite output was inspected; no numbers
below are empirical estimates. The only numbers are (a) exact binomial calculations for the *design's* error
rates and power, labelled as such, and (b) constants stipulated by this pre-registration.

**Chronology statement.** This file is committed before any test of the tie-breaker panel below. The
Apple-Silicon port branch (`research/apple-silicon-gpu-2026-11-24` @ `fd933d9`) reports a *PORT-PRODUCTION* run
of the existing exp1/exp2/exp3 (`HANDOFF.md` §6–7). The author of this record has **not opened** that output.
The existing exp2 features are explicitly **rejected** in §2 and any analysis of them is exploratory and
cannot serve as the confirmatory test. All confirmatory tests defined here require the redesigned outputs in
§3 and must be run by an owner who has not inspected their results before the run is executed.

**Purpose.** The Atlas's macro regression wall says aggregate panels cannot separate the competing micro
mechanisms (E1 `5/272`; Q3 `87 %` minority-effect mislabelling; Q1: MSE `97 %` and BIC `100 %` fail the
zero-signal control). The forward programme proposes *micro tie-breakers*. The suite's current tie-breaker
features fail before they are run: they are transforms of the DGP weights, and the Q1 zero-signal control is not
implementable in the current parameterisation (Job A audit, `research/records/2026-11-24-suite-lit-review/
AUDIT.md`). This document pre-registers (i) the redesign needed to make a tie-breaker test meaningful, (ii) a
panel of observables grounded in real survey instrumentation, (iii) the controls, (iv) out-of-seed and
out-of-world validation, (v) exact decision rules, and (vi) what would count as failure.

---

## 1. Questions and estimands

**Q1.** Conditional on matching a common macro-moment vector, can any micro observable recover the mechanism
family (poverty/subsistence vs school-cost push vs public-crowding+shadow-tutoring) better than the chance
band, out of seed, out of parameter region, and out of world (mixtures)?

**Q2.** Does the same observable fall to chance when mechanism strength is zero (the Q1 control), when labels
are permuted, and when two worlds are algebraically observationally equivalent?

**Q3.** Does any performance survive a survey measurement layer calibrated to real questionnaire practice
(sampling, item non-response, hours heaping, reference-period differences, unmeasured hidden work)?

**Estimands (all simulation-conditional; no historical or causal estimand).**

- `A_T`: out-of-seed 3-class accuracy of tie-breaker `T` on the macro-matched, fees-only arm, held-out seed
  block, with the fixed classifier of §6.
- `R_T,w`: per-world recall for `w ∈ {P, S, C}`.
- `A_T^reg`: accuracy on held-out parameter regions (±30 % perturbations; §5.2).
- `A_T^mix`: nearest-vertex accuracy on held-out mixture worlds (§5.3).
- `A_T^stress`: accuracy under the measurement-stress configuration (§4.2).
- `A_T^0`, `A_T^perm`, `A_T^placebo`, `A_T^macro`: the four control accuracies (§4.1).
- `R²_T`: calibration-block R² of `T` regressed on the three DGP weights and the matched macro moments —
  the admissibility diagnostic (§2.3).

**What is not an estimand.** No real-world mechanism share, no historical counterfactual, no causal effect, no
"true DGP" behind any country. Everything here is model-conditional and must be labelled simulation.

---

## 2. Why the current tie-breaker design is rejected (and what must change)

### 2.1 The rejection

The current `exp1` mechanism label **is** the parameter vector: `DGP_POVERTY = (w_pov=2.2, w_push=0.1,
w_tutor=0.8, div=0.02)`, etc. `exp2` then classifies those labels from four summary statistics that are
functions of the same state probabilities: `enrolled_work_hrs_p90` (a quantile of a deterministic hours
function of the income gap), `hidden_to_sw_ratio` (a direct nonlinear transform of the state mix),
`tutor_income_corr` (a correlation of a binary take-up that depends on income only through an affordability
threshold), and `mean_learn` (a state indicator times public quality and ability). The classifier recovers the
weights because the weights are what generated every feature. This is a tautology, not a measurement result.

The Q1 zero-signal control cannot be run because there is no strength parameter: setting all weights to zero
gives a different, degenerate world (`DGP_ZERO_SIGNAL`), not the three worlds with zero effect content.
`exp2` contains no zero-signal branch, no label permutation, no chance calculation, and no held-out parameter
region (Job A audit §6.2).

The repo's own shadow-education recovery study is the cautionary precedent: its "favour" and "thin" variants
are algebraically the same model (largest output difference 6.7e-16), yet a random-forest classifier separated
them 62 % of the time because their calibrated parameter ranges differed (`research/shadow-education/README.md`,
this branch). A classifier on synthetic worlds can manufacture discrimination from parameter ranges alone.
Any tie-breaker test must therefore include an algebraic-equivalence placebo (§4.1, C3).

### 2.2 Required suite redesign (binding on any test of this pre-registration)

**R1 — strength-separable worlds.** Replace the label-equals-parameter design with
`θ_w(s) = θ_0 + s·Δ_w`, `w ∈ {P, S, C}`, `s ∈ {0, 0.25, 0.5, 1.0}`, where `θ_0` is a common baseline
parameter vector and `Δ_w` is the mechanism-specific deviation. At `s = 0` all three worlds must be
distributionally identical (the same RNG-to-observable map given the same seed). This is verified by code
inspection and a KS/chi-square identity check in a calibration run *before* any discrimination test; if the
`s = 0` worlds are not identical within Monte-Carlo error, the redesign has failed and the suite cannot run the
Q1 control.

**R2 — macro-moment matching.** Define a pre-specified target macro vector `M*` (levels and 10-year changes of
enrolment, visible work, study-and-work overlap; see §3.1). For each world and each `s`, search the nuisance
parameters (preference scale, income/ability dispersion, cost levels) to match `M*` within a stated tolerance.
Only (world, parameter set) cells that match enter the tie-breaker test. Report the matched cells and the
matching residuals; cells that cannot be matched are reported as "not macro-equivalent" and are **not**
evidence for or against the wall.

**R3 — measurement layer.** Emit, in addition to the household states, the survey-like variables in §3.2, then
apply the measurement model of §4.2 (sampling, non-response, heaping, reference-period and hidden-work
under-reporting) before computing any tie-breaker. Tie-breakers are computed only on the measured variables,
never on model internals.

**R4 — output additions required by the panel.** Grade attainment; foundational learning outcome by grade;
tutoring expenditure (or hours) per enrolled child; household consumption/expenditure quintile; time
allocation (school, work, study-at-home/tutoring, chores); child age; and (for T7 only) a teacher agent with
own-pupil tutoring. Observables that the model cannot emit are not tested; they are listed as required model
extensions.

**R5 — seeds and blocks.** Calibration seeds `20261125 + 100·k`, `k = 0…19`; held-out seeds `k = 20…79`;
reserved replication seeds `k = 80…139`. No part of the held-out or reserved block may be inspected before the
confirmatory run. The same seed stream is used across worlds and arms (paired designs).

**R6 — no model changes after the test starts.** Any change to `Δ_w`, `θ_0`, the measurement model, the
classifier, or the decision rules voids the confirmatory status and requires a dated amendment plus a fresh
held-out block.

### 2.3 Admissibility test: "not a simple transform of the DGP weights"

For each candidate `T`, on the **calibration block only**, fit
`T ~ 1 + w_pov + w_push + w_tutor + div + d_ger + d_cl_total` (linear; the weights are known in simulation).
If `R²_T > 0.90`, `T` is **rejected** as a transform of the DGP weights and is not tested. Rationale: a
statistic that is almost perfectly predicted by the weights carries no evidence beyond them; the threshold
0.90 is a pre-registered design constant, not an estimate. Report every rejection with its `R²_T`.

This test does not rescue a bad observable; it only prevents the tautology. Passing it is necessary, not
sufficient: the discrimination test in §6 must also pass.

---

## 3. The tie-breaker panel

### 3.1 Common objects and notation

Worlds: **P** = poverty/subsistence (`w_pov` high), **S** = school push (`w_push` high),
**C** = crowding+shadow tutoring (`w_tutor`/`div` high). Mixtures are convex combinations of the three
`Δ_w` with Dirichlet weights.

Macro target vector `M*` (set from the redesigned model's own admissible range, not from real data): primary
gross-enrolment share; visible-work share; study-and-work share; and their 10-year changes under the fees-only
arm. `M*` is fixed once, before the confirmatory run, and recorded in the run log. Every world is calibrated to
`M*` within a tolerance of ±2 percentage points per moment (design constant).

**Classifier (fixed, no tuning).** Standardise each feature vector using calibration-block means/SDs;
classify by minimum Euclidean distance to the calibration-block world centroid (three centroids); ties go to
the lowest world index. No feature selection, no hyperparameter search, no classifier comparison. This is
deliberately the simplest possible rule, because Q1 showed that flexible criteria (MSE, BIC) reward complexity
rather than mechanism; a simple fixed rule cannot be accused of buying accuracy with flexibility.

**Units.** One held-out unit = one (seed, world) pair in the fees-only arm, summarised on the measured
variables. Primary test: `n = 180` units (60 held-out seeds × 3 worlds). Per-world recall: `n = 60` per world.
Secondary pooled-arms test: `n = 540` (60 seeds × 3 arms × 3 worlds), with per-arm recall required.

### 3.2 Tie-breakers

Each row states: what is measured; the survey precedent; the expected direction across **P / S / C**; why it
is not a simple transform (and its admissibility risk); the required model output; and the main failure modes.
Directions are *expected signs of the world differences*, pre-specified now; they are predictions, not results.

---

**T1 — Joint state × expenditure-quintile profile (primary-adjacent; high-dimensional object).**

*Measured:* the 4×5 matrix of child state shares {school only, study+work, visible work only, hidden/latent
work} by household consumption quintile; summarised by four pre-specified scalars: visible-work share in Q1–Q2,
study+work share in Q2–Q4, school-only share in Q4–Q5, and the total-variation distance of the state mix
between Q1 and Q5.

*Precedent:* ILO (2008) Resolution II defines the statistical categories; WDI/UCW indicators
`SL.TLF.0714.WK.ZS` ("work only") and `SL.TLF.0714.SW.ZS` ("study and work") operationalise the overlap among
children in employment; DHS-8 education items supply attendance/attainment; MICS-style child-labour modules
supply economic activity and chores. (ILO 2008 verified; WDI metadata verified 2026-11-24; MICS module
PARTLY VERIFIED — see Job A audit §8.)

*Expected direction.* **P:** visible and hidden work concentrated in Q1–Q2, study+work mass in Q2–Q3, school-only
only at Q5; steep negative income gradient of work. **S:** school-only mass extends into Q3–Q4; work
concentrated in Q1 but with a flatter gradient than P; hidden/latent work elevated at the bottom. **C:**
school-only high in all quintiles; work low everywhere; tutoring (and its expenditure) concentrated in Q4–Q5.

*Not a transform:* it is a joint distribution over states and income, not a single ratio; the model must
produce the income-state matrix and the survey must measure it. Risk: because the state mix is what the weights
determine, individual cells may still pass the admissibility threshold only because of the income gradient;
the `R²_T` diagnostic decides.

*Failure modes:* state misclassification in surveys (especially hidden work); the income proxy (consumption vs
income) is not the model's `base_y`; small per-quintile n; hidden work unobserved by design.

*Model output:* state × consumption-quintile distribution (R4).

---

**T2 — Work-hours distribution shape (banded, dispersive, bimodal).**

*Measured:* among children in employment, shares in the ILO-relevant bands `1–13 h`, `14–27 h`, `28–42 h`,
`≥43 h` per week; interquartile range; and a pre-specified bimodality statistic (Hartigan dip statistic if
implementable, otherwise the likelihood-ratio of a two-component vs one-component Gaussian mixture with fixed
initialisation). *Not* a single `p90`.

*Precedent:* ILO (2008) Resolution II uses a 14-hour cut-off for permissible light work; the ILO (2017) global
estimates report hours brackets including "27–42" and "43 or more" and separate household-chore hours. (Both
verified.)

*Expected direction.* **P:** more mass in the `≥28 h` bands and a more bimodal distribution (0 vs long hours).
**S:** more mass in the `1–13 h` band combined with schooling; less long-hours work than P. **C:** little work
mass overall; concentration in the lowest band.

*Not a transform:* banded distribution and bimodality are distributional, not a quantile of a deterministic
hours rule. *Admissibility risk:* high — `exp1` already makes hours a deterministic function of the income gap,
so this may fail the `R²_T` test. If rejected, report the rejection and keep the observable for a redesigned
model where hours are a behavioural choice.

*Failure modes:* heaping at 7/14/21/28/35 hours; reference-period differences (last week vs last year);
seasonality; child age composition; bands must not be chosen after seeing results.

*Model output:* weekly hours by state and child age (R4).

---

**T3 — Income gradient of tutoring expenditure (not take-up).**

*Measured:* among enrolled children, tutoring expenditure per child (and, separately, tutoring hours) regressed
on log household expenditure with a quadratic, reporting the slope at the median and at the 90th percentile,
plus a concentration index (Gini or concentration index) of tutoring expenditure among the enrolled.

*Precedent:* Bray & Kwok (2003, *Economics of Education Review* 22(6):611–620) on socio-economic patterns of
private supplementary tutoring; Tansel & Bircan (2006, *Economics of Education Review* 25(3):303–313) Tobit
analysis of private tutoring expenditures; Dang & Rogers (2008, *World Bank Research Observer* 23(2):161–200)
on the growth and inequality implications of private tutoring. Survey vehicles: LSMS/IES education-expenditure
modules and dedicated shadow-education surveys. (All three citations verified; DHS/MICS do **not** field
tutoring expenditure — that is a stated limitation, not something to be imputed.)

*Expected direction.* **C:** steep positive slope and high concentration at the top. **S:** near-zero slope
(tutoring is not the mechanism). **P:** low participation and a low, mostly affordability-driven slope.

*Not a transform:* the model currently has binary take-up with no expenditure; expenditure intensity and its
income gradient are new behavioural objects. Risk: if the model implements expenditure as a deterministic
function of income, it becomes a transform and should be rejected.

*Failure modes:* zero-inflation; recall bias; household- vs child-level measurement; consumption measurement
error correlated with education spending; small effective n among the poor.

*Model output:* tutoring expenditure/hours by household consumption quintile (R4).

---

**T4 — Learning-per-grade slope and the tutored/untutored gap (designated primary).**

*Measured:* foundational literacy/numeracy (e.g., can read a grade-2-level text; can do a grade-2-level
arithmetic item) among children by grade attained; slope of the learning outcome on grade from grade 2 to
grade 5; and the difference in that slope between tutored and untutored children. Reported as two scalars: the
public learning-per-grade slope and the tutored−untutored slope gap.

*Precedent:* Kaffenberger & Pritchett (2020, *IJED* 79:102272) learning profiles by grade; Pritchett (2013)
*The Rebirth of Education* (schooling vs learning); ASER Centre and Uwezo grade-based assessments; UNICEF MICS6
Foundational Learning Skills module; World Bank (2018) *World Development Report 2018* on learning. (Kaffenberger
& Pritchett, WDR 2018 verified; ASER/Uwezo domains verified but specific reports UNVERIFIED; MICS6 FLS module
PARTLY VERIFIED.)

*Expected direction.* **S:** high grade attainment but a flat public learning-per-grade slope (children move up
without learning) and a small tutored/untutored gap. **C:** flat public slope for untutored children, steeper
for tutored children, and a widening tutored/untutored gap; high attainment. **P:** low attainment, but among
the selected enrolled children the learning-per-grade slope is relatively steep (positive selection).

*Not a transform:* requires grade attainment and a learning outcome, neither of which exists in the current
model; it is a two-margin object (attainment × learning), not a state indicator.

*Failure modes:* test/curriculum differences; ceiling and floor effects; grade attainment endogenous to
learning; age-grade confounding in cross-sections; language of assessment; the model's learning production
function must be given a grade dimension without making learning a deterministic function of state.

*Model output:* grade attainment distribution; learning outcome by grade; tutoring exposure by grade (R4).

---

**T5 — Age-grade distortion (overage and repetition).**

*Measured:* share of enrolled children who are over-age for their grade; grade-repetition rate where
available; both by consumption quintile.

*Precedent:* DHS-8 woman's/household questionnaire items — "Have you ever attended school?", "What is the
highest level of school you attended: primary, secondary, or higher?", "What is the highest [GRADE/FORM/YEAR]
you completed at that level?" — combined with age (verified in the DHS-8 model questionnaire, 2023). MICS
education module supplies the same items for children.

*Expected direction.* **S:** high overage (enrolment surge without progression). **C:** low overage. **P:** high
overage among the few enrolled, but low absolute enrolment.

*Not a transform:* an age × grade joint object, absent from the current model.

*Failure modes:* age heaping; repetition questions are not standard in DHS, so repetition may be unavailable;
grade completion is measured only for the respondent (women 15–49), not for all children, in the DHS woman's
questionnaire.

*Model output:* child age, grade attained, enrollment history (R4).

---

**T6 — Time-allocation profile including the chore share.**

*Measured:* hours in the last week in (i) school, (ii) economic work, (iii) study at home/tutoring, (iv)
household chores, expressed as shares of a 168-hour week; plus the chore share by quintile and the
study-at-home share by quintile.

*Precedent:* United Nations (2004/2005) *Guide to Producing Statistics on Time Use: Measuring Paid and Unpaid
Work* (ST/ESA/STAT/SER.F/93; verified); ILO (2008) Resolution II distinguishes economic activity from household
services; ILO (2017) reports household-chore hours in the same brackets as work; MICS-style child-labour
modules collect chore hours. (UN guide verified from the PDF's series/sales number; title string PARTLY
VERIFIED — see Job A audit §8.)

*Expected direction.* **P:** work + chores high at the bottom, school low. **S:** school high, study-at-home
low, work low except at the bottom; chore share elevated where school costs bite. **C:** school high; tutoring/
study time concentrated at the top; chore share lower than P and S.

*Not a transform:* a four-way time budget, with a measured chore component that proxies the latent hidden-work
state. Risk: if the model allocates time deterministically from the state, the observable becomes a transform.

*Failure modes:* diary collection cost; stylised questions are noisy; seasonality; child self-report; the
168-hour constraint and school-day length must be measured consistently.

*Model output:* weekly time allocation and chore hours (R4).

---

**T7 — Own-teacher tutoring share (secondary; requires teacher agents).**

*Measured:* among tutored children, the share whose tutor is their own regular teacher, and the share of
teachers who tutor their own pupils.

*Precedent:* Bray, Kobakhidze, Liu & Zhang (2016, *IJED* 49:291–299) and Bray, Kobakhidze, Zhang & Liu (2018,
*J. Curriculum Studies* 50(4):435–455) document fee-charging tutoring by teachers in Cambodian public schools;
the repo's earlier shadow-education calibration uses the published pattern "own-teacher share 57.7 %, other-
teacher 40.9 %, 13 of 24 interviewed teachers tutoring" (`experiments/shadow-abm/src/tutoring_abm/README.md`).
(Both Bray citations verified.)

*Expected direction.* **C:** high own-teacher share, high teacher-tutoring share. **S:** low. **P:** low.

*Not a transform:* requires provider identity and teacher agents, which the suite does not have. It is listed
as a required model extension, not as a currently testable observable.

*Failure modes:* self-report and definition of "own pupils"; teacher sample small; the observable is only
meaningful if the model represents teacher incentives (Jayachandran 2014, DOI 10.1016/j.jdeveco.2014.02.008,
verified).

*Model output:* teacher agents; tutoring provider identity; teacher-side tutoring revenue/effort (R4).

---

### 3.3 Observable × world direction matrix (pre-specified)

Cells are expected signs of the world difference (`+` higher than the other worlds, `−` lower, `0` no predicted
difference); "n.t." = not testable until the model extension exists.

| Observable | P (poverty) | S (school push) | C (crowding+tutoring) | Primary statistic |
|---|---|---|---|---|
| T1 visible-work share, Q1–Q2 | + | + | − | share |
| T1 study+work share, Q2–Q4 | + | 0 | 0 | share |
| T1 school-only share, Q4–Q5 | − | + | + | share |
| T1 state-mix Q1–Q5 TV distance | + | + | − | total variation |
| T2 share ≥28 h | + | 0 | − | band share |
| T2 share 1–13 h among enrolled | − | + | 0 | band share |
| T2 bimodality statistic | + | 0 | − | dip/LR |
| T3 tutoring-expenditure slope | 0/low | 0 | + | slope |
| T3 tutoring concentration index | 0 | 0 | + | Gini/concentration |
| T4 learning-per-grade slope | + | − | − (public) | slope |
| T4 tutored−untutored gap | 0 | 0 | + | slope difference |
| T5 overage share | + | + | − | share |
| T6 chore share | + | + | − | share |
| T6 study-at-home share, Q4–Q5 | − | − | + | share |
| T7 own-teacher share | n.t. | n.t. | n.t. | share |

The matrix is a *prediction*; a tie-breaker whose direction is contradicted by the matched, held-out data is
reported as a directional failure even if its classification accuracy is high (accuracy could be driven by a
different feature of the world). This guards against post-hoc reinterpretation.

---

## 4. Controls (all must pass before any tie-breaker can be certified)

### 4.1 The four controls

**C1 — Q1 zero-signal control (the gate the current suite lacks).** In the R1 parameterisation, run the three
worlds at `s = 0`. They must be distributionally identical; the fixed classifier must be at chance. Decision:
`A_T^0 ≤ 0.3889` (the 95th percentile of Binomial(180, 1/3) divided by 180; exact calculation: the band is
count ≤ 70 of 180, with false-positive rate `P(X ≥ 71) = 0.0498`; the pre-registered band is accuracy ≤ **0.389**). If a tie-breaker exceeds this,
it is exploiting random or design artefacts and **cannot** be certified; the design is invalid for that
observable.

**C2 — Label permutation.** Shuffle the world labels within the held-out block with a fixed permutation seed and
rerun the classifier. `A_T^perm ≤ 0.389`. This catches leakage from the label-generation order or from any
seed-to-world coupling.

**C3 — Algebraic-equivalence placebo.** Construct a pair of worlds that are observationally equivalent by
construction, e.g. (i) add a common constant to all four utilities (choice-invariant), or (ii) move `w_tutor`
and `shadow_cost` jointly so that the tutoring take-up condition is unchanged for every household. Run the
two-class classifier on this pair. `A_T^placebo ≤ 0.561` (95th percentile of Binomial(180, 0.5): count ≤ 101 of
180 = 0.561, false-positive rate `P(X ≥ 102) = 0.043`; exact upper band). If the placebo exceeds chance, the classifier is picking up parameter-range or
seed artefacts — the failure the repo's shadow-education study documented at 62 % — and **all** tie-breaker
results are discarded. This control is mandatory and is the single most important safeguard in this design.

**C4 — Macro-only baseline.** After R2 matching, run the same classifier using only the matched macro moments
as features. It must be at chance (`≤ 0.389`). If it is not, the macro matching failed and the micro test is
invalid: the observable would be "predicting" the world from unmatched macro differences, i.e. re-discovering
the wall rather than breaking it.

### 4.2 Measurement layer and the stress configuration

Applied to the measured variables before any tie-breaker is computed:

- **Sampling:** draw `n_h = 1,000` households per country-wave (baseline) and `n_h = 500` (stress), with
  sampling weights; each simulation cell is one country-wave.
- **Item non-response:** 15 % missing on work hours and tutoring expenditure (baseline); 30 % (stress),
  missing-at-random within state×quintile.
- **Hours heaping:** round reported hours to multiples of 7 with probability 0.35, and to 14/21/28/35 with
  additional probability 0.15.
- **Reference-period:** make the "last week" measure noisier than the "last 12 months" measure by a
  pre-specified factor (the factor is a design assumption, reported and stress-tested; it is not estimated from
  data here).
- **Hidden-work under-reporting:** the latent hidden-work state is reported as "not working" with probability
  `p_hide`; baseline `p_hide = 0.5`, stress `p_hide = 0.8`. This is an assumption, labelled as such, chosen to
  make the unmeasured-state problem explicit; it must be reported in every result table.
- **Survey gaps:** country-waves are 5 years apart (baseline) and irregular with 3–8 year gaps (stress);
  only measured waves enter a tie-breaker statistic.

The **baseline** configuration is used for the primary test; the **stress** configuration is a required
robustness gate. A tie-breaker that passes baseline but fails stress is reported as "not survey-feasible".

---

## 5. Cross-validation design

### 5.1 Out-of-seed

Calibration seeds `k = 0…19`; held-out seeds `k = 20…79`; reserved replication `k = 80…139` (R5). The classifier
is fit on calibration only; accuracy is computed on held-out only. The reserved block is untouched until a
certification is claimed or an inconclusive outcome triggers replication.

### 5.2 Out-of-parameter-region

Calibration uses the vertex worlds `s = 1.0` plus ±15 % perturbations of each `Δ_w`. Held-out includes ±30 %
perturbations and `s ∈ {0.25, 0.5}`. A tie-breaker that only works at the exact vertices is not a tie-breaker;
it is a vertex detector.

### 5.3 Out-of-world (mixtures — the real target)

Held-out mixture worlds are drawn as `θ = θ_0 + Σ_w d_w Δ_w`, `d ~ Dirichlet(α)` with `α = (0.5, 0.5, 0.5)`
(design constant, fixed before the run, chosen to spread mass over the simplex), retaining draws whose dominant
weight `max(d) ≥ 0.6`; 60 held-out mixture draws × 3 arms. A mixture is
scored against its **dominant-weight** world. `A_T^mix` must be ≥ 0.70. Real countries are mixtures, not
vertices; a tie-breaker that only recovers vertices does not speak to the Atlas question.

### 5.4 Arms

Primary test on the fees-only arm (`tuition_only` in exp1; the closest to "no extra intervention", and the arm
used by the existing exp2). Secondary test pools the three arms and requires per-arm recall ≥ 0.70; this tests policy robustness
without letting arm effects substitute for mechanism signal.

---

## 6. Decision rules (exact)

Let `n = 180` held-out units, `k_pass = 144` (0.80 × 180), per-world `n_w = 60`, `k_w = 42` (0.70 × 60).

**Step 0 — Admissibility.** Compute `R²_T` on calibration only. If `R²_T > 0.90`: outcome **REJECTED (transform)**;
report `R²_T`; not tested.

**Step 1 — Control gates (mandatory, before looking at discrimination).**

| Gate | Statistic | Pass band (n = 180) |
|---|---|---|
| C1 zero signal (`s = 0`) | 3-class accuracy | ≤ **0.389** |
| C2 label permutation | 3-class accuracy | ≤ **0.389** |
| C3 algebraic-equivalence placebo | 2-class accuracy | ≤ **0.561** |
| C4 macro-only after matching | 3-class accuracy | ≤ **0.389** |

If any gate fails: outcome **INVALID (design)**, stop, report all four gates. No tie-breaker can be certified
from an invalid design.

**Step 2 — Discrimination (primary).** Outcome **CERTIFIED** only if **all** hold:

1. `A_T ≥ 0.80` (≥ 144/180) on the held-out seed block, fees-only arm.
2. `R_T,w ≥ 0.70` (≥ 42/60) for every world `w ∈ {P, S, C}`.
3. `A_T^reg ≥ 0.70` (out-of-parameter-region accuracy).
4. `A_T^mix ≥ 0.70` (mixture nearest-vertex accuracy).
5. Direction matrix (§3.3) not contradicted on the matched held-out data for that observable.
6. All of 1–5 hold under the **measurement-stress** configuration (`A_T^stress`).

**Step 3 — Multiplicity.** Designated primary tie-breaker: **T4** (learning-per-grade slope and
tutored/untutored gap). Secondaries: T1, T2, T3, T5, T6. For secondaries, apply Holm–Bonferroni across the
five tests at family `α = 0.05` on the one-sided exact binomial test of `A_T > 1/3`; because the five are
correlated (same units), Holm is conservative — state this. A secondary is only reported as certified if it
also passes Step 2 and its Holm-adjusted test.

**Step 4 — Outcomes.** Exactly one of: **CERTIFIED**, **FAILED** (a control passed but discrimination thresholds
were not met with adequate power, i.e. the point estimate is below 0.70 and the upper 90 % bound is below
0.80), **INCONCLUSIVE** (controls passed; accuracy in the region where the design cannot separate 0.70 from
0.80 — see §7), **INVALID (design)** (any control failed), **REJECTED (transform)** (admissibility failed).

**Step 5 — Replication.** If **INCONCLUSIVE**, run the identical analysis once on the reserved block
`k = 80…139` and report both. A claim of certification requires the reserved-block result to pass Step 2 as
well; if it does not, the outcome is **NOT CERTIFIED** regardless of the first block.

**Step 6 — Negative result.** If no tie-breaker certifies, report the null, the control accuracies, and the
rejections; **stop**. No new feature may be added to the same pre-registration. A new observable requires a
dated amendment committed before a fresh held-out block is touched.

---

## 7. Power and chance bands (design arithmetic, not data)

Exact binomial calculations for the pre-registered design (transparent; no empirical input):

| n | 3-class chance band (95th pct) | 2-class chance band (95th pct) | P(certify ≥0.80 \| true 0.85) | P(certify \| true 0.80) | P(certify \| true 0.75) |
|---|---|---|---|---|---|
| 180 | 70/180 = 0.389 (size 5.0 %) | 101/180 = 0.561 (size 4.3 %) | 0.973 | 0.544 | 0.069 |

Per-world recall `n_w = 60`, threshold 42/60 = 0.70: `P(pass | true 0.85) = 0.999`, `P(pass | true 0.80) =
0.978`, `P(pass | true 0.75) = 0.851`.

**What this means for the rules.** The design is powered to certify a *strong* discriminator (true accuracy
≥ 0.85) and is deliberately conservative about moderate ones: at a true accuracy of 0.80 the point estimate
exceeds 0.80 only about half the time. That is why Step 4 has an **INCONCLUSIVE** category and Step 5 a
reserved replication block, rather than a binary pass/fail. A null result from this design means "no strong,
survey-feasible discriminator was certified", not "no tie-breaker exists". The pre-registered decision rule
must not be relaxed after seeing the point estimate; if the outcome is INCONCLUSIVE, the reserved block is the
only permitted follow-up.

---

## 8. What would count as failure

1. **Design-invalid:** C1, C2, or C3 exceeds its chance band (the Q1 lesson: if a classifier can "recover" a
   world with no content, the whole approach is void for that observable). All results discarded.
2. **Matching-invalid:** C4 exceeds the chance band after R2 — the "micro" result is really a macro difference.
3. **Transform:** admissibility `R²_T > 0.90` — the observable is not independent of the DGP weights.
4. **Vertex-only:** passes at the vertices but fails out-of-region or mixture tests — not a tie-breaker.
5. **Not survey-feasible:** passes baseline measurement but fails the stress configuration — not usable with
   real questionnaires.
6. **Direction violation:** accuracy high but the pre-specified direction matrix is contradicted — the
   classifier found another feature; the observable is not doing the interpretation work claimed.
7. **Underpowered null:** if a tie-breaker is FAILED at a true accuracy between 0.70 and 0.80, report it as
   inconclusive rather than "no discriminator"; the design cannot distinguish those cases for a single
   observable. (This is a design limitation stated now, not an excuse to add features later.)
8. **Redesign failure:** if the three `s = 0` worlds are not identical within Monte-Carlo error, the suite
   cannot implement the Q1 control and this pre-registration is void; a new design and a new document are
   required.

---

## 9. Reporting rules (binding)

1. Report **every** tie-breaker, including rejected and failed ones, with its `R²_T`, control accuracies,
   point estimates, per-world recalls, and the full configuration grid. No selective reporting.
2. Report all seeds, the calibration/held-out split, the matched macro cells and residuals, the fixed `M*`, the
   classifier code hash, and the suite commit hash.
3. Label every table **simulation**; never "evidence about countries", never causal language. The suite is not
   history.
4. Data tiers: simulated / model-imputed / measured-survey; hidden work is latent/model-imputed and must be
   labelled so in every table.
5. Preserve failures: crashed cells, unmatched cells, seeds that did not converge, and any deviation from this
   document go into a "Failures and deviations" section, with the same prominence as results.
6. No change to the decision rule after seeing the held-out result. An amendment is allowed only with a dated
   entry stating what was known at the time, and it voids the confirmatory status of the run it affects.

---

## 10. What this pre-registration does not claim, and what it does not authorise

- Not history, not causal inference, not a claim about any country or about schooling, child labour, or
  fertility in the world. It is a design for a synthetic identification exercise.
- It does not authorise running exp1: the Commander owns the ported runs (task allocation). Tests under this
  document require the redesigned outputs of §2.2 and must be run by an owner who has not inspected their
  results.
- It does not validate the existing exp2 features; §2 rejects them by construction. Any use of the existing
  PORT-PRODUCTION exp2 output is exploratory and cannot be reported as confirmation.
- It does not claim that a passing tie-breaker would identify a real mechanism. Passing means: *within this
  model, after macro matching and with a survey-like measurement layer, this observable is informative about
  the mechanism family and is not a transform of the weights*. External validity is a separate, later question
  requiring real survey data (DHS/MICS/UCW/ILO time-use and expenditure surveys).
- It does not claim the panel is exhaustive. It is the set of observables that (a) real surveys can measure and
  (b) the redesigned model can emit; anything else is deferred.

---

## 11. Amendments

None. This is v1.0, committed before any test. Any future amendment must be appended here with a date, what was
known at the time, and which held-out block remains unexposed. The commit hash of this file and the exact
`M*` vector must be recorded in the analysis log before the confirmatory run.

**Sign-off.** Design-only record, prepared by suite-auditor (task-4, Job B), 2026-11-24. It supersedes no prior
pre-registration; it replaces the tie-breaker clauses of the suite's own PRE_REGISTRATION H4, which Job A found
unimplementable.
