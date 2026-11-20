# PRE-DECLARATIONS — experiment suite

Written BEFORE the substantive runs of the cells marked below (see the timestamp column in
`RUN_MANIFEST.json` for when each block was first written). A pre-declaration states the question,
hypothesis, estimand, arms, shared controls, outcomes, seeds, and the threshold that will count as
support or failure. Amendments are logged in `ERROR_LOG.md` and never silently overwrite a
pre-declaration. Cells are capped at ~20; target 8-12 completed.

Conventions used throughout
- **Model versions.** `massabm` = the October manuscript's Philippine ABM, copied unmodified from
  `01_sources/massification_project/code/massabm/` (sha256 of `model.py` 2b6484e7…, `params.py`
  6a4d133a…). `triad` = the three-actor model, copied unmodified (sha256 `model.py` 7b22d93c…).
  New mechanisms live in `code/new/` and are labelled **"independently named new implementation,
  not a reproduction"**.
- **Matched seeds.** Every arm of an experiment uses the same seed list. Seed dispersion (sd across
  matched seeds) is reported separately from parameter uncertainty, and is never presented as a
  confidence interval over the real world.
- **Naive benchmark.** Where a behavioural arm is compared with a mechanism, we report the
  no-mechanism arm (e.g. no floor, no tutoring, no reform) as the naive comparator.
- **Money units.** massabm: index units, informal adult wage = 1.0. triad: informal wage units.
- **Verdict words.** `supports` / `challenges` / `null` / `not identified` / `pilot only`.
- **Status vocabulary** (task spec): completed / pilot only / failed to execute / proposed / data blocked.

---

## E0 — Phase 0: environment, smoke, known-answer controls  [status: completed]

**Question.** Is the harness trustworthy enough that a behavioural result can be read?
**Predeclared checks.**
1. Environment record (OS, python, numpy/scipy/pandas, source hashes).
2. `massabm run.py smoke` exit 0, finite output.
3. `triad run_triad.py emergence --quick` exit 0.
4. **Cohort arithmetic known-answer test** (E2 core, independent new implementation):
   N=200 children/cohort, 10 grades, zero dropout, all pass, fixed 60 university seats, fixed 150
   formal vacancies, no migration, 40 years. Must pass C1 people conservation, C2 seat cap, C3 stock
   identity, C4 money identity + endowment not overdrawn, C5 job identity, C6 nonnegativity,
   C7 probabilities in [0,1], C8 limit cases (seats=0, seats≥N), C9 enrolment-cap stress.
   Known answers that must come out exactly: admission share = min(seats,N)/N = 0.30; money
   residual = 0; formal employment ≤ vacancies.
5. **massabm invariant checks** on real runs: people conservation per matured cohort, jobs identity
   per year, nonnegativity, probabilities in [0,1], fiscal ledger nonnegative; repeated under
   `reform_rule='never'`, `mode='no_floor'`, `mode='lottery'`, and all-gate tutoring ban.
**Decision rule.** Any failed check blocks substantive interpretation; diagnose before proceeding.

---

## E8 — The race and the floor: 6 arms  [status: completed]

**Question.** Does a categorical eligibility floor explain anything beyond a ranked labour queue?
**Hypothesis (from the October manuscript).** Persistence and exclusion should move with the floor;
the impulse to invest *more as returns compress* (intensification) should require the rank race,
not the floor. H0: the floor adds nothing beyond ranking.
**Estimand.** Arm means of: basic-diploma completion (all; poorest fifth Q1); formal-employment rate
of entrants below the diploma vs holders of it; college entry of Q3-Q5; slope of Q3-Q5 college entry
on degree holders' absolute income across formal-demand scales {0, 1, 2}.
**Arms (2×3).** ranking {on, off} × eligibility rule {none, adaptive employer floor, fixed rule-set
floor} = 6. **Shared controls:** identical cohorts, schedules, seeds, wage rules; no K-12 reform
(`reform_rule='never'`); formal-demand scale as the blocking factor; window = cohorts entering
1995-2012, labour market 2010-2030.
**Seeds.** 19000+r, r=0..reps-1 (matched across all arms and scales).
**Threshold.** Floor effect = (floor arm − no-floor arm) holding ranking fixed, with seed sd.
`supports` if |Δdiploma| and |Δexclusion| both exceed 2× seed sd and move in the manuscript's
direction; `null` if the floor delta is within 2 seed sd; `not identified` if the floor also moves
the intensification slope (the two mechanisms are not separable in this design).
**Also predeclared:** the arm must reproduce the *direction* of the stored October floor_test, not
its exact numbers (provenance of stored numbers unknown; see `MODEL_INVENTORY` note in EXPERIMENTS.md).

## E13 — Graduate-supply shock with a matched competitive benchmark  [status: completed]

**Question.** When more graduates arrive against fixed formal vacancies, who bears the adjustment —
and is the answer an artefact of the surplus (slot) account?
**Hypothesis.** Under the surplus account (slots, floors, ranking), graduates displace diploma
holders: diploma holders' formal-employment rate and *absolute* income fall. Under a competitive
skill-price market with imperfect substitution, diploma holders become scarcer so their absolute
income rises. The diploma/degree wage *ratio* can rise in both — so relative wages cannot separate
the accounts.
**Estimand.** Paired change vs "no shock" in: degree share; diploma holders' absolute income;
graduates' absolute income; dip/deg ratio; diploma holders' formal-employment rate.
**Arms.** 2 worlds {surplus, competitive CES} × 3 shocks {none, college half price from 1995,
college 80% off from 1995}. Shared controls: fixed formal vacancies (`macro_elasticity=0`), no K-12
reform, identical seeds 20000+r, same outcome window (2010-30).
**Threshold.** `supports` the surplus account if Δformal_rate_diploma < 0 AND Δdiploma_income < 0 in
the surplus world, with the competitive world showing Δdiploma_income > 0; magnitudes reported but
not used as evidence for a country. `challenges` if both worlds move the same way.

## E2 — Cohort arithmetic and conservation stress  [status: completed]

**Question.** Do people, money, jobs and seats conserve in a small deterministic cohort system, and
what breaks first when enrolment is pushed above/below capacity?
**Estimand.** Conservation discrepancy (people, money, jobs) per year and per cohort, in absolute
units; pass/fail of the 9 declared checks; the exact known answers.
**Arms (structural stress, deterministic).** (a) baseline small world; (b) fixed seats = 0;
(c) fixed seats ≥ cohort; (d) enrolment cap 100 < 200; (e) seats 60 with cap 100.
**Threshold.** `completed` only if all 9 checks pass; any conservation discrepancy > 1e-9 is a fail.
**Note.** No substantive interpretation is drawn from E2. It validates the accounting of E0/E8.

## E3 — Household liquidity, credit and shocks  [status: completed]

**Question.** Is a family's dropout driven by *ability to pay* or *willingness to invest*, and how
much does each financing instrument move participation at matched resources?
**Hypothesis.** A hard cash cutoff (`borrow` = 0) produces more liquidity-driven exit and an
income gradient steeper than graded credit; a temporary income shock does most of its damage where
credit is absent; a conditional transfer and zero-cost schooling act like credit but not identically
(the transfer is targeted, credit is not).
**Estimand.** By quintile: basic completion, college entry, liquidity-driven exit share, and the
Q5−Q1 gap in completion. All at the same realized ability draws and the same shock seeds.
**Arms (5).** (1) baseline `borrow=0.5`; (2) hard cutoff `borrow=0`; (3) graded/expanded credit
`borrow=1.0`; (4) temporary shock `shock_sigma=0.9` (with baseline credit); (5) shock + no credit
(`shock_sigma=0.9`, `borrow=0`); (6) zero-cost schooling + CCT (`cost_*≈0`, `cct_path` on).
**Shared controls.** Same cohorts, schedules, seeds 21000+r; no K-12 reform; K-12 exogenous 2013;
window = entry cohorts 1995-2012 for completion, 2006-2015 for college.
**Threshold.** `supports` if (2) vs (1) raises Q1 liquidity exits by more than 2 seed sd and widens
the Q5−Q1 completion gap; and (3) vs (1) narrows it. `null` if all financing arms are within
2 seed sd of each other. Report naive benchmark = baseline arm.
**Caveat pre-declared:** in massabm, `borrow` is a per-year share of income, not an interest rate;
results are about *quantity* of credit, not its price. No new credit-market module is added unless
the arms fail to separate, in which case the failure is recorded, not patched away.

## E5 — Memory, learning and decision horizons  [status: completed]

**Question.** Does the credential race require learning from realized outcomes, and how does the
memory window change the trajectory?
**Hypothesis.** With very short memory (belief_decay → 0) families overweight the most recent
outcomes → higher volatility and faster (noisier) response; with very long memory
(belief_decay → 0.99) the system is sticky and slow. A no-learning arm (fixed prior beliefs) is the
naive benchmark. If trajectories are indistinguishable, the mechanism is not identified by these
outcomes.
**Estimand.** (i) College entry of Q3-Q5 for cohorts entering 1995-2012; (ii) tutoring spend per
child Q3-Q5; (iii) basic completion; (iv) mean absolute one-year change in the belief series
(response speed); (v) dispersion of college entry across seeds (noise).
**Arms (5).** belief_decay ∈ {0.0, 0.5, 0.88 (baseline), 0.99} plus belief_mode
`selection_corrected` at baseline decay. Shared controls: same seeds 22000+r, no K-12 reform.
Pre-declared limit: `belief_decay=1.0` is *infinite* memory and is reported as a limit, not a
plausible parameter.
**Threshold.** `supports` a memory effect if college entry or response-speed differs across arms by
more than 2 seed sd and is monotone in the memory window; `null` otherwise.

## E7 — Gate density and tutoring clustering  [status: completed]

**Question.** Does tutoring concentrate where a gate's payoff is discontinuous at the margin, and
does moving the bar move the spending or destroy it?
**Hypothesis.** The share of gate-takers who tutor rises with the stakes of the gate; tutoring
spending is concentrated at the highest-payoff gates (board, apex); raising the basic bar toward the
median student moves tutoring to that gate without creating learning.
**Estimand.** (i) share of gate-takers tutoring by gate {basic, apex, college, board}; (ii) share of
total tutoring spend by gate; (iii) tutoring share at the basic gate as the basic bar sweeps
{-2.0,-1.5,-1.0,-0.5,0.0,+0.5} in score units; (iv) tutoring take-up by income quintile at each gate
(clustering test); (v) completion under each bar (naive benchmark = baseline bar).
**Arms.** bar sweep (6 levels) + gate ban arms {none, apex, board, all_formal} as the
"can you suppress tutoring by closing the gate" test. Shared seeds 3000+r, no reform change.
**Threshold.** `supports` clustering if the tutoring-rate ordering across gates is stable across
seeds and the bar sweep raises basic-gate tutoring by > 2 seed sd between the lowest and highest bar.

## E10 — Learning vs test performance (Yang-style omega)  [status: in progress / pilot]

**Question.** How much of tutoring's effect is productive learning versus test-specific performance,
and does the policy conclusion (access, places, cost) change with that split?
**Hypothesis.** When tutoring raises measured exam score but not later skill (omega→0, test-only),
more places go to tutored students with no aggregate skill gain; when tutoring is productive
(omega→1), the same spending raises measured and later skill. If outcomes are invariant to omega,
the design cannot separate the mechanisms.
**Estimand.** With omega = productive share of the tutoring effect: (i) gate pass rates and places
awarded; (ii) later human capital (the model's log-wage per year of schooling, H) and realized
income; (iii) total household tutoring spend; (iv) higher-education composition by quintile.
**Implementation (labelled).** The stock massabm's `tut_effect` only enters exam scores; schooling's
productive return is `hc_school*years`. We implement omega by splitting the tutoring effect into a
test component and a *credited schooling-year* component. This is an **independently named new
implementation of a Yang-style omega split, not a reproduction of Yang's model**: it adds a
`tut_hc_credit` multiplier in `code/new/massabm_omega.py` whose default 0.0 leaves massabm unchanged.
**Arms.** omega ∈ {0.0, 0.5, 1.0} × {baseline, college cost halved}. Shared seeds 23000+r.
**Threshold.** `supports` separability if later skill and income respond monotonically to omega while
measured pass rates are flat; `not identified` if pass rates also move with omega (mechanical).

## E14 — Actor knockouts (triad necessity/lock-in)  [status: planned → completed if run]

**Question.** Which actor's gain from the credential is necessary for the pipeline to deepen, and
does removal after maturity reverse it (lock-in)?
**Estimand.** End-state (years 110-139): mean years of schooling, share upper-secondary+, share
tertiary+, credential-hiring share, employer floor, state funding frontier, formal share; and the
year each milestone first occurs.
**Arms.** All 8 combinations of {household, employer, state} gain present/absent, matched seeds
24000+r; plus late removal at year 90 (lock-in). Shared controls: same N, T=140, urbanisation path.
**Threshold.** An actor is *necessary* if its absence reduces end-state tertiary share by more than
2 seed sd; *not necessary* otherwise. Lock-in `supports` if late removal moves end state less than
early removal (hysteresis).

## E15 — State priorities and capacity (triad)  [status: planned → completed if run]

**Question.** Do different state objectives (fiscal return, order after unrest, status/peer
emulation, rentier) produce different schooling and elite-composition paths at equal budgets?
**Arm.** state motive {fiscal-only, order-motivated after conflict years, peer-emulation, rentier
(no tax motive, rents only)}, × capacity {0.5, 0.9}. Shared seeds 25000+r.
**Estimand.** State funding frontier by year 40/80/120; share tertiary+; formal share; fiscal revenue.
**Threshold.** `supports` objective-dependence if frontier paths differ by > 2 seed sd at equal
budget. Political objectives are scenarios, not historical facts.

## E17 — Teacher tutoring vs school support  [status: pilot only / new module]

**Question.** Does substituting school-based homework help and teacher feedback for commercial
tutoring reduce paid tutoring, and does it help or hurt learning?

**New module.** `code/new/school_support.py` — **independently named new implementation, not a
reproduction** of Jayachandran's or any Chinese model. Declared rule: a fraction of the gate margin
that paid tutoring would buy can be supplied publicly; if the teacher is the same person who grades,
public support and paid tutoring are substitutes (withholding) or complements depending on a
declared `teacher_withhold` parameter.
**Arms.** (1) no support (baseline); (2) public school support at zero price, no withholding;
(3) support with teacher withholding (substitute: classroom instruction degraded in proportion to
teacher-tutoring share); (4) commercial tutoring banned with leak. Shared seeds 26000+r.
**Threshold.** `supports` substitution if paid tutoring spend falls by > 2 seed sd vs (1) while
learning is not lower; `challenges` if learning falls.

## E18 — China-style Double Reduction synthetic variants  [status: planned]

**Question.** Under what conditions does suppressing commercial tutoring plus expanding school
support reduce total household tutoring burden, and what does a no-effect baseline imply?
**Hypothesis.** A ban alone reroutes demand to a dearer informal market (massabm's
`tut_ban_leak`); a ban plus school support reduces paid spend more than a ban alone; with no real
mechanism change the no-effect baseline reproduces the baseline exactly.
**Estimand.** Paid tutoring spend by gate; total tutoring take-up; gate pass/completion; cost per
child. **Arms.** (1) no-effect baseline; (2) ban only (leak 0.5); (3) ban only (leak 0.0, fully
enforced); (4) ban + expanded school support (E17 module); (5) ban + heterogeneous enforcement
(leak 0.25). Shared seeds 27000+r.
**Threshold.** `supports` if (4) < (2) in paid spend by > 2 seed sd and no > 2-sd learning loss;
`challenges` if the ban reroutes rather than reduces. Not presented as a measured Double Reduction
effect.

## E19 — Hong Kong / Philippines descriptive gate paths  [status: planned / pilot]

**Question.** What do comparable model gate paths look like for the Philippines (K-12 reform,
licensure, overseas recognition) versus a mature-gate East Asian path (Korea-like preset)?
**Design.** Descriptive reconstruction only, clearly labelled simulated. Compare model cohort
trajectories with the manuscript's published targets, reporting where the default model misses them.
**Estimand.** Cohort basic completion, degree share, transition to college, licensure, overseas
professional share at 10/20/30/40-year horizons.
**Threshold.** No causal claim. `completed` when trajectories and target deviations are reported;
any statement about Hong Kong is data blocked unless a local HK series is loaded.

## E20 — Cross-country transfer with a held-out case and at least one null  [status: planned / pilot]

**Question.** If the Philippines-fitted structure runs on a Korea-like schedule, does it predict the
held-out cohort outcomes better than a flat/cohort persistence benchmark? Include at least one null.
**Design.** Parameters/schedules from the PH baseline (not calibrated on the held-out case); compare
with the Korea-like preset and with a naive persistence benchmark. Report at least one outcome where
transfer fails (predicted null). **Estimand.** MAE of model vs stated benchmark targets, flagged as
a model-to-model comparison, not a blind empirical validation.

---

## Cells NOT run (recorded as proposed, not claimed)
- E9 return compression/outside options (partially covered by E8 slope; not separately run).
- E11 education–economy mechanisms (floorworld S1–S5) — not run in this budget.
- E12 long-run massification trajectories — covered descriptively by E19.
- E16 credential information/recognition — not run.
- E4 children's four states (childworld) — not run.
- Cross-cutting recovery study — not run.
Every one of these is `proposed`, never counted as completed.
