# PRE-REGISTRATION — Master Equation Inventory experiment suite (task-40)

**Record:** `research/records/2026-11-25-equation-suite/`.
**Branch:** `research/equation-suite-2026-11-25` (from `origin/research/handoff-2026-11-24` @ `e8ba60c`).
**Author:** synthesist. **Written:** 2026-11-24/25, **committed before any code or run** (this file is the first
commit on the branch).
**Status:** DESIGN ONLY at this commit. No simulation has been run; no output exists yet.

## Purpose

The PI asked for ten self-contained experiments, one per block of the Master Equation Inventory (economics of
education; education and development; shadow education). This suite builds a **small, honest, runnable
demonstration for each block**: what the equation set implies in a known-truth or provenance-labelled world, where
the intuitive interpretation fails, and what the data can and cannot say. It is a methods-and-demonstration
suite, not a paper, and it is not an empirical test of any country.

## Non-negotiable rules for every script

1. **No causal claims.** Even where a DGP contains a true effect, script output is a statement about the
   simulation design ("the estimator recovers/does not recover the known parameter"), never about the world.
2. **No invented citations.** No script names a paper or DOI. The only external quantities used are the
   **Bray six-school targets** already committed in `research/shadow-equations-2026-11-25` @ `fdc8da0` and the
   repo's committed panels; both are provenance-labelled in `inputs/PROVENANCE.json`.
3. **Data tiers labelled.** `SYNTHETIC` (generated in-script from a stated DGP), `OBSERVED`/`RECONSTRUCTED`
   (committed repo panels, with branch/commit/sha256), `LITERATURE_TARGETS` (Bray targets). No imputation and no
   fabricated empirical validation.
4. **Smoke before full.** Every script supports `--smoke` (fewer seeds/replications, same code path). `run_all.py`
   runs smoke then full for every script and records both statuses.
5. **Report everything.** Nulls, failures, discarded runs and decision-rule misses are reported. A script that
   crashes is a reported failure, not a deletion.
6. **Bounded CPU.** Server runs use ≤32 worker processes; each worker is single-threaded (`OMP_NUM_THREADS=1`).
   Other agents share the box; no job is killed, nothing is shut down.
7. **Determinism.** Fixed seeds per script and per replication; the manifest records sha256 of every script and
   every output; the run records host, Python/NumPy version, command and wall time.

## The ten scripts (per-script pre-registration)

Each script prints one plain-English sentence and writes `results/<name>.json` plus a CSV table.

### S1 — `eq01_returns.py` — Mincer returns, ability bias, IV (inventory 42–56)
- **Demonstrates:** a log-wage regression recovers the schooling coefficient when ability is controlled; it is
  biased upward when ability is omitted and correlated with schooling; 2SLS using an instrument that shifts
  schooling but not wages recovers the true coefficient under the stated exclusion restriction.
- **DGP (SYNTHETIC):** n = 4,000; ability a ~ N(0,1); S = 10 + 2.2a + 1.5v; ln w = 1.0 + 0.09 S + 0.12 a + e;
  instrument Z affects S with coefficient 1.0 and does not enter wages.
- **Estimators:** OLS without ability; OLS with ability (oracle); 2SLS; also reports the exact percentage
  `100(e^b - 1)%` and a quadratic experience profile.
- **Decision rule (pre-declared):** under ability bias, OLS-without-ability bias is positive and its 95% CI
  excludes the truth, while 2SLS |bias| is smaller and its CI covers the truth in ≥90% of 200 replications.
  Null control: ability coefficient in the S equation = 0 → OLS and 2SLS both within 2 SE of the truth.
- **Outputs:** per-replication coefficients, bias, CI coverage; verdict per rule.

### S2 — `eq02_production.py` — Cobb-Douglas vs CES, complementarity (26–41)
- **Demonstrates:** a linear interaction regression can recover the sign of a CES cross-partial only when the
  omitted ability input is controlled; Cobb-Douglas is misspecified when the true technology is CES with ρ≠0.
- **DGP (SYNTHETIC):** A = B[ωS^ρ + (1−ω)T^ρ]^{1/ρ} + γ·ability + noise; ability correlated with S and T;
  worlds ρ ∈ {1.0 (linear null), 0.5 (complementary)}.
- **Estimators:** OLS interaction with/without ability; CES fit by 1-D grid over ρ with linear coefficients
  concentrated out; RMSE comparison of Cobb-Douglas vs CES.
- **Decision rule:** in the ρ=1 world the interaction CI includes 0 in ≥95% of replications; in the ρ=0.5 world
  the ability-controlled interaction is positive with CI excluding 0 in ≥80%; CES's recovered ρ is closer to the
  truth than Cobb-Douglas implies (ρ=1).
- **Outputs:** interaction coefficients, CES ρ grid, RMSEs.

### S3 — `eq03_tutoring_demand.py` — logit/probit, two-part/hurdle/Tobit (57–69)
- **Demonstrates:** when participation and amount are driven by different processes, a Tobit imposes one process
  and biases the income elasticity; a two-part (hurdle) model recovers the amount process. Under a single process
  the two agree.
- **DGP (SYNTHETIC):** n = 6,000 households; participation probit with income gradient 0.6; amount log-linear
  with income elasticity 0.8 (DIFFERENT world) or identical coefficients (SINGLE world). Zero censoring at no
  participation.
- **Estimators:** Tobit (EM), two-part (probit + OLS on log positive amount), OLS on all with zeros.
- **Decision rule:** DIFFERENT world: two-part |η̂−0.8| ≤ 0.15 and Tobit |η̂−0.8| > 0.15 in ≥90% of
  replications. SINGLE world: both within 0.15 of the truth. If the rule fails, it is reported as failed.
- **Outputs:** participation and intensity coefficients, elasticities, model comparison.

### S4 — `eq04_tutoring_production.py` — tutoring in production, inequality (70–80, 123–137)
- **Demonstrates:** a tutoring-input production model can show a ban reducing participation yet *raising* the
  learning Gini when richer households substitute into other tutoring; distributional conclusions depend on the
  substitution assumption, not on the equation's fit.
- **DGP (SYNTHETIC, illustrative):** 20,000 pupils; SES, school quality; tutoring take-up has an income gradient;
  learning = CES(school, tutoring) + SES gradient; scenarios: baseline, own-teacher ban, hard quota, cash transfer.
- **Real anchor (LITERATURE_TARGETS):** Bray six-school participation/own-share/teacher-share targets from the
  committed shadow-equations record; reported only as a descriptive external check (max-z distance), not as a fit.
- **Decision rule:** report Gini and top–bottom learning gap changes under each scenario; rule: "ban raises the
  learning Gini" if ΔGini > 0 with CI excluding 0; the model is *not* claimed to fit Bray if max-z > 2.
- **Outputs:** scenario table (participation, Gini, gaps), Bray distance.

### S5 — `eq05_admissions.py` — admissions contest, bar vs quota (81–86)
- **Demonstrates:** a hard quota changes *who* is admitted (by construction) but not effort or learning unless
  effort responds to the contest form; a bar and a quota are different rationing devices with different
  distributional incidence.
- **DGP (SYNTHETIC):** 10,000 pupils with ability and income; bar = score threshold; quota = reserved share for
  the bottom 40% by income; contest = Tullock effort with cost.
- **Decision rule:** report the income–admission gap sign flip, effort/tutoring response, and the welfare
  (learning-equivalent) change; rule: "quota flips the admission gap" if baseline gap > 0 and quota gap < 0.
- **Outputs:** admission shares by quintile, effort, gap flip.

### S6 — `eq06_growth.py` — augmented Solow, convergence, Nelson-Phelps (87–105)
- **Demonstrates:** a convergence regression can recover the known λ; an omitted TFP term that is correlated with
  human capital biases the human-capital coefficient; Nelson-Phelps-style catch-up is an interaction between
  distance-to-frontier and human capital.
- **DGP (SYNTHETIC):** 120 countries × 30 periods; growth = g0 − λ ln y0 + β_H H + u; H correlated with u
  (omitted TFP); a Nelson-Phelps world where growth gap = φ0 + φ1 H × gap.
- **Real part (OBSERVED AGGREGATES):** committed `x4_panel.csv` from the staging X2 record: descriptive
  cross-section of 2004→2018 attainment change on 1991 attainment and job share; association only.
- **Decision rule:** synthetic: recovered λ within 2 SE in the no-confound world; β_H sign flips or shrinks when
  the confounder is excluded (report both). Real: report coefficients with robust SE and label "descriptive".
- **Outputs:** synthetic recovery table, real cross-section table.

### S7 — `eq07_finance.py` — public finance, benefit incidence, cost-benefit (106–122)
- **Demonstrates:** the distributional incidence of a public education subsidy is a function of enrolment
  composition, not of the budget line; a progressive-looking universal subsidy can be regressive; NPV/IRR are
  arithmetic plus an assumed discount rate.
- **DGP (SYNTHETIC):** 100,000 households with income and enrolment probability rising in income; public unit
  cost; scenarios: universal, means-tested, quota.
- **Decision rule:** report benefit-incidence shares by quintile, concentration index, NPV and IRR at two
  discount rates; rule: "regressive" if the concentration index is positive (benefits skew rich).
- **Outputs:** incidence table, CI, NPV/IRR.

### S8 — `eq08_inequality.py` — inequality, decomposition, mobility (123–137)
- **Demonstrates:** Gini/Theil and intergenerational elasticity answer different questions; a Theil decomposition
  can attribute most inequality to between-group variation while the Oaxaca decomposition of the same gap says
  something different; a mobility transition matrix is not an elasticity.
- **DGP (SYNTHETIC):** two generations, 50,000 families; parent income and education → child education → child
  income with persistence parameter; two-group SES structure.
- **Decision rule:** report Gini, Theil within/between, intergenerational elasticity, rank-rank slope, transition
  diagonal, Oaxaca twofold decomposition; null world with zero persistence → elasticity CI includes 0.
- **Outputs:** inequality table, decomposition, mobility matrix.

### S9 — `eq09_identification.py` — DID/event study/IV/RD/synthetic control shell (138–167)
- **Demonstrates:** each identification design recovers its target in its own known-truth world and fails in the
  stated violation world. **Demonstration only; no causal claim about any real policy.**
- **DGP (SYNTHETIC):** (a) staggered adoption with heterogeneous effects → TWFE biased, group-time (CS-style)
  estimator closer; (b) endogenous treatment with a valid instrument → IV recovers, OLS does not; (c) sharp RD
  at a cutoff → local linear recovers the jump; (d) synthetic control for one treated unit.
- **Decision rule:** no-effect null: all estimators' 90% CIs include 0 in ≥90% of replications. In the effect
  worlds, report bias of naive vs design estimator; TWFE bias sign reported, no claim that it generalises.
- **Outputs:** per-design truth/estimates/bias table.

### S10 — `eq10_development.py` — LAYS, learning poverty, fertility/health (168–183)
- **Demonstrates:** LAYS and learning-poverty are arithmetic mappings of three inputs and can rank countries
  differently from enrolment; cross-country fertility/health associations are descriptive and sensitive to
  controls, construct choice (effective fertility vs TFR) and a future-schooling placebo.
- **Synthetic part:** 5,000 country-like units with EYS, HLS, schooling deprivation, learning deprivation;
  compare LAYS rankings and learning-poverty under the 625 HLS benchmark vs a shifted benchmark.
- **Real part (OBSERVED/RECONSTRUCTED):** committed `long_run_panel.csv` (Q2 record): 5-year grid 1950–2020,
  fertility (both `effective_fertility` and `tfr_observed_1950plus`), schooling, log income, urbanisation;
  country+year FE association, plus future-schooling placebo. Association only.
- **Decision rule:** synthetic: report rank correlation between LAYS and EYS and the share of units whose
  learning-poverty status changes when the benchmark moves 10%. Real: report associations for both fertility
  constructs and the placebo; no causal reading.
- **Outputs:** synthetic mapping table, real association table.

## Run protocol

1. Local smoke: `python scripts/run_all.py --smoke-only --workers 2` (Mac, numpy only; must pass before deploy).
2. Deploy: tar the record (scripts, inputs, prereg) to `/root/work/eqsuite/` on the 192-core server
   (`ssh -p 45973`, key only; **never shut it down**).
3. Full run: `OMP_NUM_THREADS=1 python scripts/run_all.py --workers 16` (≤32 workers; the box is shared with
   ABC/MASSENG agents). The manifest records per-script status, wall time and hashes.
4. Fetch `results/` back, write `SUITE_REPORT.md` with the plain-English results, commit and push.
5. Any script that fails is reported as failed with its traceback; no silent omission.

## Deviations

None at this commit. Any later deviation (changed rule, changed seed, changed data) must be logged in
`SUITE_REPORT.md` with a dated note; the pre-registered rules above are not edited after seeing results.

---

## Amendment 01 — system-map alignment and multiverse specs (committed BEFORE any run)

**Dated:** 2026-11-25, written after the Lead's task-40 scope update and **before any script was executed**
(the pre-registration commit `dabc458` precedes this amendment; no output exists at this commit). This amendment
does not delete anything above. It (a) places each script in Codex's system map, (b) places each script on one of
the four connected pieces, and (c) pre-declares the **set of defensible equation choices (multiverse)** that each
script must vary rather than report a single specification. The counting/decision rules in the S1–S10 sections
remain; where they say "the estimator", read "the multiverse of estimators listed below".

### Four connected pieces and the system map

The suite is organised around the chain **family affordability (incl. forgone earnings) → learning (school +
tutoring) → limited-place selection gate → credential→jobs**, embedded in Codex's system map
(families · schools-state · learning · exams-shadow · jobs-credentials · wider economy · dashboard · test bench).

| Script | System-map node(s) | Connected piece | Pre-declared multiverse of equation choices |
|---|---|---|---|
| S1 `eq01_returns` | jobs-credentials ↔ wider economy | 4 credential→jobs | OLS no controls; OLS with measured ability (oracle); 2SLS; experience quadratic vs linear; log vs exact-percentage premium |
| S2 `eq02_production` | learning ↔ schools-state | 2 learning | linear interaction without ability; interaction with ability; CES ρ grid {0.3, 0.5, 0.7}; Cobb-Douglas |
| S3 `eq03_tutoring_demand` | families ↔ exams-shadow | 1 family affordability | Tobit; two-part (hurdle); OLS on participants; probit vs logit participation |
| S4 `eq04_tutoring_production` | learning ↔ exams-shadow ↔ families | 2 learning (+ shadow inequality) | CES ρ {0.3, 0.5, 0.7}; SES gradient on/off; ban retention {0.5, 0.7, 0.9} |
| S5 `eq05_admissions` | exams-shadow ↔ schools-state | 3 limited-place gate | score bar; quota share {0.4, 0.5, 0.6}; contest effort weight {0.3, 0.8} |
| S6 `eq06_growth` | wider economy | 4 / wider economy | convergence with/without H; with/without initial income; Nelson-Phelps interaction; descriptive real cross-section |
| S7 `eq07_finance` | families ↔ schools-state ↔ dashboard | 1 affordability / state finance | universal; means-tested; quota; discount rate {5%, 8%} |
| S8 `eq08_inequality` | wider economy ↔ jobs-credentials ↔ learning | 4 / distribution | Gini; Theil decomposition; intergenerational elasticity; rank-rank; transition matrix; Oaxaca; persistence on/off |
| S9 `eq09_identification` | test bench | cross-cutting evaluation | TWFE; CS-style not-yet-treated controls; CS-style never-treated controls; OLS vs 2SLS; local-linear RD; synthetic control |
| S10 `eq10_development` | dashboard ↔ wider economy | 4 / dashboard measurement | HLS benchmark 625 vs 690; LAYS vs learning poverty; effective fertility vs TFR; FE vs pooled associations |

### Additional pre-declared reporting rules for the multiverse

1. Every script reports **all** specs in its row, not a selected one; a `multiverse` block gives each estimate,
   the min–max range, and `spec_robust = (sign is the same across all specs)`.
2. A claim of "positive/negative" is made only if `spec_robust` is true; otherwise the result is reported as
   "sign depends on the equation choice", with the range.
3. No coefficient is called causal. The multiverse is a statement about what the equations imply under
   defensible choices, not about the world.
4. Multiverse specs are implemented as separate equations/estimators, not by dropping inconvenient seeds or
   re-running until a sign appears. Seeds are fixed and shared across specs.
5. Data tiers are unchanged: SYNTHETIC unless the script's declared input is a committed panel
   (S6 descriptive cross-section, S10 observed panel) or the Bray literature targets (S4 descriptive check).

## Amendment 02 — nothing else changed before the runs

No seeds, no thresholds, no scripts existed at this commit. The smoke-then-full protocol and the ≤32-worker
server limit above are unchanged.

---

## Amendment 02 — final system-map scope (massification system; committed BEFORE any run)

**Dated:** 2026-11-25, after the PI's scope correction relayed by the Lead (the suite must cover the whole
**massification system**, not shadow education) and **before any script was executed**. Amendment 01 is
superseded *only* in its mapping table; its multiverse and reporting rules stand. Tutoring is now **one**
script/module (the exams-shadow part), not two.

Final ten scripts and mapping:

| Script | System part (Codex map) | Connected piece | Pre-declared multiverse of equation choices | Data |
|---|---|---|---|---|
| S1 `eq01_family_demand.py` | families (budgets, demand, forgone earnings, credit) | 1 affordability | budget without forgone earnings; with forgone earnings; credit-constrained; quantity-quality vs income-only | SYNTHETIC |
| S2 `eq02_supply_finance.py` | schools-state, finance, dashboard | 1 affordability / state supply | universal vs means-tested vs quota finance; supply response on/off; discount 5% vs 8% | SYNTHETIC |
| S3 `eq03_learning_quality.py` | learning, schools-state | 2 learning | Cobb-Douglas; CES ρ grid; value-added vs levels; teacher-input vs general input | SYNTHETIC |
| S4 `eq04_transitions_gates.py` | stage transitions and gates at all levels | 3 gate | exam bar; reserved quota; merit+income gate; fee gate | SYNTHETIC |
| S5 `eq05_returns_credentials.py` | jobs-credentials | 4 credential→jobs | OLS; 2SLS; credential/sheepskin dummy; overeducation/required schooling | SYNTHETIC |
| S6 `eq06_migration_rural_urban.py` | wider economy / families (migration, rural-urban) | cross-cutting | probit vs logit; with/without network; with/without remittances; rural-urban gap | SYNTHETIC |
| S7 `eq07_inequality_dashboard.py` | inequality, dashboard | 4 / distribution | Gini; Theil decomposition; IGE; rank-rank; Oaxaca; LAYS with HLS 625 vs 690; learning poverty | SYNTHETIC |
| S8 `eq08_growth.py` | wider economy | 4 / macro | convergence with/without H; with/without initial income; Nelson-Phelps; descriptive real cross-section | SYNTHETIC + OBSERVED cross-section |
| S9 `eq09_identification.py` | test bench | cross-cutting evaluation | TWFE; CS not-yet-treated; CS never-treated; OLS vs 2SLS; local-linear RD; synthetic control | SYNTHETIC |
| S10 `eq10_tutoring_shadow.py` | exams-shadow (the single tutoring module) | 2 learning / gate pressure | Tobit; two-part hurdle; OLS participants; CES ρ {0.3,0.5,0.7}; ban retention {0.5,0.7,0.9} | SYNTHETIC + LITERATURE_TARGETS (Bray) |

Pre-declared reporting rules from Amendment 01 apply unchanged to this table. The chain reported in every
script metadata is: **family affordability (incl. forgone earnings) → learning (school + tutoring) → limited-place
selection gate → credential→jobs**, with migration, inequality/dashboard, growth and the test bench as the
wider system. No coefficient is causal; the multiverse says what the equations imply under defensible choices.
