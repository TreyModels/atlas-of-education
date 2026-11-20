# EXPERIMENTS — result records

One record per experiment, using the template in `00_handoff/templates/07_report_templates.md`.
Pre-declarations are in `PRE_DECLARATIONS.md` and were written before the runs. Failures and
amendments are in `ERROR_LOG.md`. Every number below is **simulated model output**, not an
observed country value, unless explicitly labelled otherwise. Per-run commands, raw CSVs, logs and
`findings.txt` are in `runs/<EID>/`.

**Counts:** completed = 12 cells (E0, E2, E3, E5, E7, E8, E10, E13, E13b, E14, E15, E18);
pilot only = 1 (E19+E20); failed to execute = 0 substantive (all failures were implementation
bugs, fixed and logged, not dropped); proposed/not run = 5 (E4, E9, E11, E16, recovery study);
data blocked = Hong Kong within E19.

**Headline table:** `SUMMARY_TABLE.csv`. **Manifest:** `RUN_MANIFEST.json`.

---

## E0 — Phase 0: environment, smoke, known-answer gate

**ID and question.** Can the harness be trusted before any behavioural claim? Environment,
smoke runs, cohort-arithmetic known answer, implementation invariants.

**Status.** completed.

**Purpose.** validation / accounting.

**Why the comparison is informative.** A leaked people or money ledger would make every
behavioural difference uninterpretable; a model that cannot conserve 200 children cannot explain
massification.

**Model and version.** massabm copied unmodified (sha256 `model.py` 2b6484e7…,
`params.py` 6a4d133a…); triad copied unmodified (sha256 `model.py` 7b22d93c…). No source edits.

**Initial conditions and timeline.** massabm smoke `N=4000`, 1920-2035; triad `emergence` quick
`N=1500`, `T=140`.

**Arms and shared controls.** Not a comparison: gates. (1) environment record, (2) massabm smoke,
(3) triad smoke, (4) known-answer cohort ledger (E2), (5) massabm invariants under default,
`reform_rule='never'`, `mode='no_floor'`, `mode='lottery'`, all-gate tutoring ban.

**Outputs.** Exit codes, PASS/FAIL of C1–C9 and V1–V7, exact known answers.

**Assumptions / sources.** Declared in `runs/E2_cohort_arithmetic/README.md`.

**Sampling.** Deterministic checks + one model seed each; no statistical claim.

**Verification.** All gates PASS. Exact known answers reproduced: admission share
0.3000 = min(SEATS,N)/N; final money residual 0.00e+00; formal employment ≤ vacancies every year.
Invariants: 0 failures across 5 massabm worlds. One real finding: an all-gate tutoring ban with
the default `tut_ban_leak=0.5` does **not** delete tutoring (4,464 units) because it models an
informal substitute market; with `leak=0.0` spend is exactly 0.

**Result.** Environment: macOS 26.6.2 arm64, 8 cores / 8 GB, Python 3.11.17, numpy 2.4.6,
scipy 1.17.1, pandas 3.1.1, matplotlib 3.11.2, PYTHONDONTWRITEBYTECODE=1. massabm smoke exit 0 in
3.5 s (8.3 s under load), reform year 2013. triad smoke exit 0 in ~1 s.

**Interpretation.** The accounting substrate is trustworthy for the runs below; the tutoring-ban
leak result shaped E18's arm design.

**Evidence to collect next.** Nothing; this is a gate.

**Reproduce.** `logs/phase0_results.txt` has the exact commands and exit codes; runner
`code/exp/{kat_cohort,invariants}.py`.

---

## E2 — Cohort arithmetic and conservation stress (known answer)

**ID and question.** Do people, money, jobs and seats conserve in a small deterministic cohort
system, and what breaks first when enrolment is pushed above or below capacity?

**Status.** completed.

**Purpose.** accounting / validation.

**Why the comparison is informative.** With zero dropout and all pass, completion must equal
`min(seats, N)/N` exactly. Any deviation is a coding error, not a finding.

**Model and version.** `code/exp/kat_cohort.py` — **independently named new implementation, not a
reproduction** of any stock engine. Declared ledger: 200 children/cohort, 10 grades, zero dropout,
all pass, 60 fixed university seats, 150 fixed formal vacancies, no migration, 40 years, explicit
`START_FUND` endowment for the fiscal warm-up.

**Initial conditions and timeline.** 40 one-year steps, starting empty.

**Arms and shared controls.** Structural stress, deterministic: baseline; seats = 0; seats ≥ cohort
(2000); enrolment cap 100 < 200; seats 60 with cap 100.

**Outputs.** Per-year people/money/job flows (`kat_cohort.csv`), per-cohort conservation, 9 check
families C1–C9.

**Assumptions / sources.** Formal wage 1.0; informal wage 0.5 for un-hired completers; tax 10% on
formal wages; school cost 0.15 per pupil-year. All declared in the module docstring.

**Sampling.** None — deterministic.

**Verification.** PASS on C1 people, C2 seats, C3 stock identity, C4 money identity + endowment,
C5 jobs, C6 nonnegativity, C7 probabilities, C8 limit cases, C9 cap stress; 0 failures.
Exact known answers: admission share 0.3000 across every matured cohort; money residual 0.00e+00.

**Result.** All 9 checks PASS. The one design defect found (no tax base in the first decade, which
drove consumption negative) is recorded in `ERROR_LOG.md` #1 and was fixed by making the warm-up an
explicit endowment stock, not a hidden subsidy.

**Interpretation.** A correctly conserved cohort ledger requires an explicit fiscal warm-up. This
is a modelling lesson, not a substantive one. No behavioural interpretation is drawn.

**Evidence to collect next.** None.

**Reproduce.** `"$PY" exp/kat_cohort.py --csv <out>/kat_cohort.csv`; exit 0.

---

## E3 — Household liquidity, credit and shocks

**ID and question.** Is dropout driven by ability to pay or willingness to invest, and how far does
each financing instrument move participation at matched resources?

**Status.** completed (reps=3, N=5000, 18/18 runs, 48 s).

**Purpose.** mechanism / policy counterfactual.

**Why the comparison is informative.** All arms share the same realized ability and shock draws;
only the financing rule changes. The baseline arm is the naive comparator.

**Model and version.** massabm unmodified. No new module: the financing instruments already exist
as `borrow` (a quantity of credit, share of income per year), `shock_sigma`, school costs and
`cct_path`.

**Initial conditions and timeline.** 1920-2035; outcome window = entry cohorts 1995-2012 and
labour market 2010-2030; K-12 reform exogenous 2013 in all arms.

**Arms and shared controls.** (1) baseline `borrow=0.5`; (2) hard cash cutoff `borrow=0`;
(3) expanded credit `borrow=1.0`; (4) temporary shock `shock_sigma=0.9`; (5) shock + no credit;
(6) free basic schooling (all basic costs 0) + existing CCT. Seeds 21000+r, matched.

**Outputs.** Basic completion (all, Q1, Q5), Q5−Q1 gap, college entry Q3–Q5, liquidity-driven exit
share (all, Q1), choice-driven pre-basic exit (Q1), tutoring spend per child, degree share.

**Assumptions / sources.** massabm's `borrow` is a **quantity**, not a price; no interest rate is
modelled. Reported as such.

**Sampling.** 3 matched seeds per arm; values are means with sd across seeds.

**Verification.** Invariant gate E0 passed on this model; 0 failed runs; all arms finite.

**Result.** (mean over 3 matched seeds; seed sd ≈ 0.001-0.006.)

| arm | basic | basic Q1 | Q5−Q1 gap | college Q3–5 | liquidity exits | liquidity exits Q1 |
|---|---|---|---|---|---|---|
| baseline | 0.715 | 0.462 | 0.321 | 0.378 | 0.404 | 0.704 |
| hard cash cutoff | 0.501 | **0.017** | **0.781** | 0.355 | 0.728 | **0.983** |
| expanded credit | **0.742** | **0.665** | **0.090** | **0.463** | 0.248 | 0.574 |
| temporary shock | 0.714 | 0.408 | 0.388 | 0.383 | 0.521 | 0.785 |
| shock + no credit | **0.212** | **0.001** | 0.634 | 0.187 | 0.898 | 0.999 |
| free basic + CCT | 0.749 | 0.611 | 0.178 | 0.396 | 0.399 | 0.662 |

Every predeclared contrast clears 2 seed sd by a large margin: hard cutoff raises Q1 liquidity
exits by +0.280 (2sd ≈ 0.015) and widens the Q5−Q1 gap by +0.460 (2sd ≈ 0.010); expanded credit
narrows the gap by −0.231 (2sd ≈ 0.008); free schooling + CCT raises Q1 completion by +0.149
(2sd ≈ 0.004).

**Interpretation.** Supports: liquidity is a **binding** constraint in this model, and the
credit-shock interaction is multiplicative — a shock alone costs Q1 5 points of completion, but a
shock without credit costs 46 points (Q1 completion 0.001). Willingness-to-invest does not need to
be invoked to explain the gradient: equally able poor children stop because they cannot pay.
Contradicts any reading of dropout as rejection of schooling. Cannot identify: the *price* of
credit (no interest rate exists), the real-world elasticity of dropout to credit, or whether real
families' borrowing limits look like `borrow=0`.

**Evidence to collect next.** A household survey linking borrowing capacity, shocks and dropout
(Philippines FIES/APIS or a dedicated panel) to replace the assumed `borrow` schedule; a credit
price would need an interest-rate block before any welfare statement.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E3.py --reps 3 --N 5000 --workers 2 --out runs/E3`.

---

## E5 — Memory, learning and decision horizons

**ID and question.** Does the credential race require learning from realized outcomes, and how does
the memory window change the trajectory?

**Status.** completed (reps=3, N=5000, 15/15 runs, 80 s).

**Purpose.** mechanism.

**Why the comparison is informative.** `belief_decay` is the weight kept on older observed
outcomes; holding realized opportunities and the seed list fixed, only the memory length changes.
`belief_speed` (mean one-year absolute change in believed CE income, 1980-2030) is the direct
response-speed estimand.

**Model and version.** massabm unmodified (`belief_decay`, `belief_mode`).

**Initial conditions and timeline.** 1920-2035; cohorts 1995-2012.

**Arms and shared controls.** M0 decay 0.0 (one-year memory); M1 0.5; M2 0.88 (baseline, ≈5 years);
M3 0.99 (near-infinite); M4 selection-corrected learning at baseline decay. Seeds 22000+r.

**Outputs.** Basic completion, college entry Q3–Q5, degree share, tutoring per child Q3–Q5,
belief_speed.

**Assumptions / sources.** `decay=1.0` is infinite memory and is reported as a limit, not a
plausible parameter. No claim of behavioural realism.

**Sampling.** 3 matched seeds; sd across seeds reported.

**Verification.** 0 failed runs; belief series finite; E0 invariants apply.

**Result.**

| arm | basic | college Q3–5 | degree | tutoring/child Q3–5 | belief_speed |
|---|---|---|---|---|---|
| M0 decay 0.0 | 0.729 | **0.212** | 0.091 | 0.0400 | **0.2966** (±0.0191) |
| M1 decay 0.5 | 0.720 | 0.368 | 0.161 | 0.0570 | 0.0832 (±0.0036) |
| M2 decay 0.88 (baseline) | 0.718 | 0.386 | 0.168 | 0.0588 | 0.0309 (±0.0005) |
| M3 decay 0.99 | 0.699 | **0.511** | **0.237** | 0.0673 | **0.0116** (±0.0003) |
| M4 selection-corrected | 0.706 | 0.436 | 0.200 | 0.0545 | 0.0269 (±0.0013) |

Predeclared test: response speed must be monotone in the memory window and differ between extremes
by >2 seed sd. It is monotone (0.297 > 0.083 > 0.031 > 0.012) and the extremes differ by 0.285 vs
2sd ≈ 0.038 → **supports a memory effect**. College entry Q3–5 moves from 0.212 to 0.511
(Δ = +0.299, 2sd ≈ 0.047) — memory length is not a cosmetic parameter.

**Interpretation.** Supports: longer memory makes families stick with the credential longer,
producing deeper completion (0.091 → 0.237 degree share) and *less* one-year volatility. This is a
real structural lever: a model with very short memory looks like a different country. Challenges:
the direction is not the intuitive one — better/more information (short memory is *more* responsive
to the latest outcomes) produces *worse* long-run investment in this structure, because recent
outcomes are noisy. Cannot identify: which memory length real families have; that needs panel
data on expectations.

**Evidence to collect next.** Expectation data (e.g. return-perception modules in household
surveys) to anchor `belief_decay`; a recovery test to see if these outcomes could distinguish
memory lengths from other parameters.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E5.py --reps 3 --N 5000 --workers 2 --out runs/E5`.

---

## E7 — Gate density and tutoring clustering

**ID and question.** Does tutoring concentrate where a gate's payoff is discontinuous at the
margin, and does moving the bar move the spending or destroy it?

**Status.** completed (reps=3, N=5000, 30/30 runs, ~100 s; findings regenerated from the written
raw CSV after a formatting bug — see `ERROR_LOG.md` #6).

**Purpose.** mechanism / policy analogue.

**Why the comparison is informative.** Moving one gate's bar while holding cohorts, prices and the
other gates fixed changes the stakes at that margin only. Tutoring take-up is measured at each gate
separately, so "does the spending follow the stakes?" is a direct test.

**Model and version.** massabm unmodified (`bar_basic` sweep; `tut_ban` arms).

**Initial conditions and timeline.** 1920-2035; gate rates measured 2000-2012; cohorts 1995-2012.

**Arms and shared controls.** Bar sweep on the basic completion gate:
{-2.0, -1.5, -1.0, -0.5, 0.0, +0.5} score units (median student ≈ 0). Gate-ban arms:
{none, apex, board, all_formal}. Seeds 3000+r.

**Outputs.** Share of gate-takers who tutor at each gate; share of total tutoring spend by gate;
basic-gate tutoring as the bar moves; completion; college entry Q1; liquidity exits.

**Assumptions / sources.** Score units are N(0,1)-like by construction (`sigma_exam=0.5`,
`bar_basic=-1.8` default). Bans use `tut_ban_leak=0.5` (informal substitute market), per the stock
model; leak=0 behaviour is documented in E0.

**Sampling.** 3 matched seeds per arm; sd across seeds.

**Verification.** 30/30 runs; 0 failures; raw + summary CSVs retained.

**Result.** Baseline 2000-2012 tutoring take-up (share of gate-takers): **board 0.933**, apex 0.443,
college 0.280, **basic 0.040**. Spend by gate: basic 756, apex 1,678, college 647, board 1,019;
apex = 40.9% of all tutoring spend, board = 24.9%.

Basic-gate bar sweep:

| bar | tutoring at basic gate | basic completion | college Q1 |
|---|---|---|---|
| −2.0 | 0.022 (±0.000) | 0.718 | 0.021 |
| −1.5 | 0.085 | 0.709 | 0.018 |
| −1.0 | 0.234 | 0.675 | 0.012 |
| −0.5 | 0.463 | 0.596 | 0.006 |
| 0.0 | 0.650 | 0.457 | 0.002 |
| +0.5 | 0.752 (±0.006) | 0.287 | 0.003 |

Ban arms (total spend; completion): none 4,100 (0.716); apex 3,686 (0.717); board 4,075 (0.718);
all_formal 3,601 (0.717). **Spending reroutes; it does not disappear.** All-gate ban cuts total
spend only 12% while completion is unchanged — demand survives, and the stock model's declared
informal leak absorbs it.

**Interpretation.** Supports the clustering hypothesis strongly: the highest-stakes discrete gates
(board, apex) carry most of the tutoring, and pushing the basic gate toward the median student
raises tutoring there from 2% to 75% (Δ = +0.729 vs 2sd ≈ 0.012) while completion falls from 0.72 to
0.29. Tutoring follows the discontinuity, not the year of schooling. The ban result is the
strongest warning: closing a gate moves spending rather than removing it, unless enforcement is
complete (E18 shows the leak=0 case). Cannot identify: whether real tutoring is productive or
test-specific (E10 addresses that); whether the informal substitute is as effective as the stock
model's `leak=0.5` assumes.

**Evidence to collect next.** Gate-specific tutoring take-up and price data (Philippine review
centres, HK tutorial chains) to calibrate the leak; exam-calendar timing data.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E7.py --reps 3 --N 5000 --workers 2 --out runs/E7`
then `code/exp/post_E7.py runs/E7`.

---

## E8 — The race and the floor: 6 arms

**ID and question.** Does a categorical eligibility floor explain anything beyond a ranked labour
queue? H0: it does not.

**Status.** completed (reps=4, N=6000, 72/72 runs, 332 s).

**Purpose.** mechanism / reproduction-quality check of the October manuscript's six-arm design.

**Why the comparison is informative.** 2×3 design separates ranking from the eligibility rule:
persistence and exclusion should move with the floor; intensification (invest more as returns
compress) should need the rank race.

**Model and version.** massabm unmodified; design follows `massabm/experiments8.py:floor_test`
(ARMS dict reused verbatim), re-run at reps=4 with the Council's requested repetition, and seed
dispersion reported.

**Initial conditions and timeline.** No K-12 reform; cohorts entering 1995-2012; labour market
2010-2030; formal-demand scale ∈ {0, 1, 2}.

**Arms and shared controls.** {ranked, unranked} × {no floor, adaptive employer floor, fixed
rule-set floor `{elite:4, mid:4, routine:3}`}; seeds 19000+r matched across arms and scales.

**Outputs.** Diploma completion (all, Q1); formal-employment rate below diploma vs diploma holders;
college entry Q3–Q5; slope of Q3–Q5 college entry on degree holders' absolute income across scales.

**Assumptions / sources.** As in the stock design; floors are a single parameter set, not
country-specific.

**Sampling.** 4 matched seeds; sd across seeds reported separately from the across-scale slope.
This is 2× the pilot (reps=2) so the pilot can be compared.

**Verification.** 72/72 runs; 0 failures; pilot and reps=4 summaries both kept.

**Result.** reps=4, N=6000, 72/72 runs (seed sd in brackets):

| arm | diploma | diploma Q1 | formal rate:<dip | formal rate:dip | college Q3–5 | slope |
|---|---|---|---|---|---|---|
| ranked, no floor | 0.771 (0.001) | 0.571 (0.004) | 0.122 | 0.351 | 0.493 (0.002) | −0.039 |
| ranked, adaptive floor | 0.770 (0.000) | 0.569 (0.002) | 0.119 | 0.225 | 0.542 (0.010) | −0.064 |
| ranked, fixed rule-set floor | 0.772 (0.001) | 0.572 (0.003) | 0.117 | 0.354 | 0.492 (0.002) | −0.049 |
| unranked, no floor (lottery) | 0.731 (0.003) | 0.538 (0.003) | 0.436 | 0.450 | 0.180 (0.013) | **+0.151** |
| unranked, adaptive floor | 0.771 (0.001) | 0.570 (0.003) | 0.118 | 0.207 | 0.614 (0.002) | +0.036 |
| unranked, fixed rule-set floor | 0.771 (0.001) | 0.571 (0.002) | 0.118 | 0.495 | 0.478 (0.008) | +0.630 |

Floor effects holding **ranking fixed**: adaptive floor −0.0011 diploma (2sd ≈ 0.0026),
−0.0022 formal rate below diploma (2sd ≈ 0.0026), +0.0489 college Q3–5 (2sd ≈ 0.021); fixed
rule-set floor +0.0004 diploma, −0.0041 formal rate below diploma (2sd ≈ 0.0042, borderline).
Under **unranked lottery** the fixed floor produces large exclusion: formal rate below diploma
0.118 vs 0.436, and college Q3–5 +0.298.

The pilot (reps=2) had unranked-lottery slope **+0.221**; at reps=4 it is **+0.151**, matching the
stored/manuscript value the Council flagged (+0.151). So that pilot exception was a small-sample
artefact, and it is reported here rather than quietly replaced.

**Interpretation.** The floor's *own* contribution beyond ranked hiring is at or below seed noise
for persistence and exclusion under ranking, while the **rank race** is what flips the
intensification slope (ranked arms < 0; unranked arms > 0). The floor bites hard only where
ranking is absent (lottery + fixed floor). This **challenges** a reading in which the relational
floor is a separate engine of persistence, and **supports** the manuscript's own separation
(ranking → intensification). Not identified: a floor design with different enforcement or vacancy
response; the stored manuscript numbers' provenance is unknown (no commit history in `01_sources`),
so direction, not magnitude, is what we compare.

**Interpretation.** The floor's *own* contribution beyond ranked hiring is close to null in this
parameterization; its exclusion effect appears only when ranking is switched off. This **challenges**
a reading in which the relational floor is a separate engine of persistence, and **supports** the
manuscript's own separation (ranking → intensification). Not identified: a floor design with
different enforcement or vacancy response; the stored manuscript numbers' provenance is unknown
(no commit history in `01_sources`), so direction, not magnitude, is what we compare.

**Evidence to collect next.** Employer vacancy/requirement microdata (job postings by credential
requirement) to calibrate whether real floors are binding in the way the fixed-floor arm assumes.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E8.py --reps 4 --N 6000 --workers 2 --out runs/E8`.

---

## E10 — Learning vs test performance (Yang-style omega)

**ID and question.** How much of tutoring's effect is productive learning versus test-specific
performance, and does the policy conclusion change with that split?

**Status.** pilot-strength completed (reps=2, N=5000, 12/12 runs).

**Purpose.** mechanism / theory discrimination.

**Why the comparison is informative.** omega changes only whether a tutored year builds later
skill; it cannot change the exam score in the same arm. If pass rates are flat while later income
responds, the two channels are separated by construction.

**Model and version.** massabm + documented EXTENSION (`tut_hc_equiv`, identity-tested at 0).
This is an **independently named new implementation of a Yang-style productive/test split, not a
reproduction of Yang's model** (see `code/new/README_EXTENSION.md`).

**Initial conditions and timeline.** 1920-2035; cohorts 1995-2012.

**Arms and shared controls.** omega ∈ {0.0, 0.5, 1.0} (productive share of `tut_effect` credited as
schooling-year equivalents) × {full college cost, half cost from 1995}; seeds 23000+r.

**Outputs.** Basic completion (pass rate), college entry Q3–Q5, degree share, college and basic
income 2010-30, tutoring spend.

**Assumptions / sources.** Mapping declared: one tutored gate-year yields
`omega × 0.25` schooling-year equivalents of skill (`hc_school` per year).

**Sampling.** 2 matched seeds per cell.

**Verification.** Identity test passed; 12/12 runs; 0 failures.

**Result.** Pass rates are flat in omega (basic completion 0.7166 → 0.7167, Δ = +0.0001 vs
2sd ≈ 0.0037) while later college income rises 4.104 → 4.195 (Δ = +0.092 vs 2sd ≈ 0.042) and
college entry Q3–5 rises 0.377 → 0.385 (Δ = +0.0075, 2sd ≈ 0.0079 — marginal). Tutoring spend is
essentially unchanged (4,091 → 4,172).

**Interpretation.** Supports separability: the omega split changes *later* skill and income without
changing measured pass rates, so "a test gain" and "a skill gain" are different objects. At these
effect sizes the place-allocation effect is small and marginal. Cannot identify: the true omega, or
whether test-specific tutoring has positional value beyond the exam; that requires data on later
job performance of tutored vs untutored students who passed the same gate.

**Evidence to collect next.** Follow-up earnings or university performance of tutored vs untutored
gate-passers (e.g. Philippine licensure re-takers; HK DSE cohort studies).

**Reproduce.** `PYTHONPATH=code/ext_massabm "$PY" code/exp/run_E10.py --reps 2 --N 5000 --workers 2 --out runs/E10`.

---

## E13 — Graduate-supply shock with a matched competitive benchmark

**ID and question.** When more graduates arrive against fixed formal vacancies, who bears the
adjustment — and does the answer depend on the surplus/slot account rather than the data?

**Status.** completed (reps=3, N=5000, 18/18 runs, 81 s).

**Purpose.** mechanism / reproduction-quality check of the October `grad_supply` design.

**Why the comparison is informative.** Same households, same shock, same fixed vacancies in both
worlds; only the wage-formation and hiring account differ. Relative wages ("the ratio") are shown
to rise in **both** worlds, which is why the ratio cannot discriminate.

**Model and version.** massabm unmodified; design follows `massabm/experiments8.py:grad_supply`.

**Initial conditions and timeline.** No K-12 reform; college cost shock from 1995; labour market
2010-2030.

**Arms and shared controls.** {surplus (slots, floors, ranking), competitive CES skill market} ×
{no shock, college half price 1995, 80% off 1995}; seeds 20000+r.

**Outputs.** Paired changes vs no-shock: degree share, diploma holders' absolute income, graduates'
absolute income, dip/deg ratio, diploma holders' formal-employment rate.

**Assumptions / sources.** Stock `hc_fair` world has **no formal/informal margin** (its formal rate
is undefined = 0). That limitation is exactly what E13b fixes; E13 is kept as the stock
reproduction.

**Sampling.** 3 matched seeds; sd across seeds.

**Verification.** 0 failures; invariant gate passed.

**Result.** College half price from 1995, paired change vs no shock:

| world | Δ degree share | Δ diploma income | Δ degree income | Δ dip/deg ratio | Δ formal rate (diploma) |
|---|---|---|---|---|---|
| surplus | +0.135 | **−0.058 (sd 0.018)** | −0.333 | +0.047 | **−0.151 (sd 0.022)** |
| competitive CES | +0.130 | **+0.295 (sd 0.005)** | −0.442 | +0.171 | not defined |

The predeclared sign pattern holds: in the surplus world diploma holders lose absolute income and
formal access; in the competitive world they gain absolute income as they become scarcer. The
dip/deg ratio rises in both (+0.047, +0.171), confirming the manuscript's methodological point that
relative wages cannot separate the accounts.

**Interpretation.** Supports the surplus account **as stated for these two worlds**. But the
competitive world here has no formal sector at all, so the exclusion comparison is not matched —
which is why E13b was built. Cannot identify: which account describes the Philippines; the
comparison is internal to the model.

**Evidence to collect next.** Same as E13b, plus real vacancy data by credential requirement.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E13.py --reps 3 --N 5000 --workers 2 --out runs/E13`.

---

## E13b — Matched-elasticity rival (Council priority)

**ID and question.** Does the competitive-account rival reproduce the *same* diploma-holder losses
once it is given a formal/informal margin, the same households, the same shock and the same
vacancy path? If yes at any substitution elasticity, the manuscript's discriminating claim is
contradicted.

**Status.** completed (reps=6, N=5000, 72/72 runs, 282 s).

**Purpose.** theory discrimination — the Council's stated "only experiment that can change the
paper's claim".

**Why the comparison is informative.** Both worlds now have formal/informal margins, so both
estimands — Δ absolute income and Δ formal-employment probability — are defined in both. Only the
wage-formation rule and the hiring rule differ (credential floor + rank vs CES skill prices +
productivity hiring). sigma ∈ {0.5, 1, 2} varies the elasticity of substitution between skilled and
unskilled labour, i.e. how imperfectly graduates substitute for diploma holders.

**Model and version.** `code/ext_massabm`, new `mode='hc_fair_slots'` (documented; stock modes
untouched; extension identity-tested). Cobb-Douglas guard at sigma = 1.

**Initial conditions and timeline.** As E13 (no K-12 reform; 1995 tuition shock; labour 2010-30).

**Arms and shared controls.** {surplus, rival at sigma ∈ {0.5,1,2}} × {no shock, half price, 80%
off}; seeds 20000+r; 6 paired reps.

**Outputs.** Δ diploma holders' absolute income; Δ diploma holders' formal-employment probability;
Δ dip/deg ratio; Δ degree income.

**Assumptions / sources.** Formal vacancies = elite+mid+routine `vac_paths` in both worlds. The
rival hires by `hc_ability*A + hc_school*(ys−10)` + noise, with no credential term and no floor.

**Sampling.** 6 matched seeds; seed dispersion reported separately. Large dispersion at sigma=0.5
is itself a result (the CES ratio is volatile).

**Verification.** 72/72; 0 failures; sigma=1 runs (the singular case) produce finite output.

**Result.** Paired change vs no shock, college half price (and 80% off in brackets):

| world | sigma | Δ diploma income | Δ formal rate (diploma) | Δ dip/deg ratio |
|---|---|---|---|---|
| surplus | — | −0.061 (0.019) [−0.042] | −0.154 (0.024) [−0.168] | +0.047 |
| rival | 0.5 | −0.059 (0.059) [−0.015 (0.142)] | **+0.017 (0.025)** | +0.297 |
| rival | 1.0 | −0.034 (0.021) [−0.032] | **+0.024 (0.017)** | −0.145 |
| rival | 2.0 | **+0.042 (0.004)** [+0.070] | −0.006 (0.003) | +0.088 |

**Predeclared decision rule fires:** at sigma ≤ 1 the rival's point estimate of Δ diploma-holder
absolute income is ≤ 0, so C3's sharp version ("only the surplus account can make diploma holders
lose") is **CONTRADICTED**. Precision caveat (reported, not hidden): at sigma=0.5 the negative is
inside its own seed dispersion (2sd ≈ 0.12–0.28); at sigma=1 it is ≈ −1.6 seed sd (just under a
2-sd bar); at sigma=2 the rival clearly produces gains.

**Interpretation.** The robust discriminator is **not** absolute income but the
**formal-employment margin**: it falls substantially only in the surplus world (−0.15, −0.17) and
never falls in the rival (+0.017, +0.024, −0.006, −0.015). So the defensible claim is: *credential
floors, not competitive skill pricing, are what push diploma holders out of formal jobs when
graduates surge — but a low substitution elasticity alone can also depress their absolute income.*
This directly challenges the manuscript's sharper framing and should change its claim from "the
competitive account cannot reproduce the fall" to "the accounts are distinguished by formal access,
not by absolute income". Cannot identify: the true sigma; whether real formal hiring reads
credentials or skills.

**Evidence to collect next.** Employer hiring data showing whether formal access depends on the
credential or on measured skill, plus an estimate of the skilled/unskilled substitution elasticity
for the Philippines.

**Reproduce.** `PYTHONPATH=code/ext_massabm "$PY" code/exp/run_E13b.py --reps 6 --N 5000 --workers 2 --out runs/E13b`.

---

## E14 — Actor knockouts (triad necessity and lock-in)

**ID and question.** Which actor's gain from the credential is necessary for the pipeline to
deepen, and does removal after maturity reverse it (lock-in)?

**Status.** completed (reps=3, N=2000; necessity 24 runs + lock-in 24 runs; triad is cheap).

**Purpose.** mechanism / theory sufficiency.

**Why the comparison is informative.** No actor's rule refers to another's; removing one actor's
*gain* (not the actor) tests whether a three-part motor is doing the work or the actors are
substitutes.

**Model and version.** triad unmodified, own `necessity` and `lockin` designs (seeds 100+r, 200+r).

**Initial conditions and timeline.** T=140, urbanisation 10%→80%.

**Arms and shared controls.** All 8 combinations of {household, employer, state} gain present /
absent from year 0; lock-in: each actor removed early (year 0) vs late (year 90); kin networks
restored at year 90. Two worlds: as built, and weak skill return.

**Outputs.** End-state mean years of schooling, share upper-secondary+, share tertiary+, share of
hiring by credential, employer floor, state funding frontier.

**Assumptions / sources.** Removal = the actor's gain from the credential is zeroed; the actor is
still present and behaves. Reported as the model's own knockout design.

**Sampling.** 3 matched seeds; end state = mean over years 110-139 (lock-in: 120-139).

**Verification.** 0 failed runs; triad invariants (nonnegative stocks) hold by construction of the
reported series; outputs finite.

**Result.** As-built world: full system 11.6 mean years; remove household gain → 8.2 (−3.5);
employer → 10.0 (−1.7); state → 10.5 (−1.2). Full system adds +4.32 years over all-removed, and
every actor contributes → **three-part motor**, with the household leg the largest. In the weak
skill-return world the employer leg shrinks to +0.26 years — the employer leg only matters where
credentials carry information productive tasks do not.

Lock-in is **actor-specific**: household removed late ≈ removed early (8.1 vs 8.2 → no hysteresis);
state removed late ≈ early (10.5 vs 10.4 → no hysteresis); but employer removed late leaves the
pipeline almost intact (11.6, tertiary 0.38) versus 10.0 when removed early → strong hysteresis for
the employer leg. Restoring kin networks at year 90 does not undo credential hiring (mean years
11.7) but collapses credential-hire share to 0.05, so the floor survives while the hiring technology
reorganises.

**Interpretation.** Supports a three-actor motor in the as-built world and **challenges** any
single-actor story. The lock-in result is the interesting one: only the employer's credential
screening is path-dependent. Habit, regulation or household expectations alone are not enough to
lock in the pipeline in this structure.

**Evidence to collect next.** Historical employer screening technology data (when firms adopted
credential screens) for one country, to test the hysteresis claim.

**Reproduce.** `PYTHONPATH=code/triad "$PY" code/exp/run_triad_E14_E15.py runs 3 2000 2`.

---

## E15 — State priorities and capacity (triad)

**ID and question.** Do different state objectives produce different schooling paths at equal
budgets, and does the investing state come out ahead on its own ledger?

**Status.** completed (reps=3, N=2000, 24 runs).

**Purpose.** mechanism / policy counterfactual (political objectives are scenarios).

**Why the comparison is informative.** A frozen state is the naive benchmark for "does investing
pay?"; order and peer motives are alternative non-fiscal justifications with the same budget rule.

**Model and version.** triad unmodified, `experiments_r4.state_motive` design (seeds 700+r).

**Initial conditions and timeline.** T=140.

**Arms and shared controls.** fiscal whole-career (as built); fiscal 10-year horizon 10% rate;
fiscal 25-year horizon 4%; never invests (frozen); rentier with budget; rentier + order after unrest
year 30; rentier + keeping up with peers; fiscal + order.

**Outputs.** Pipeline depth, year each level is funded, discounted net fiscal balance (income-tax
ledger and income+consumption-tax ledger), vs the frozen state.

**Assumptions / sources.** No overseas/remittance channel in triad, so even the combined ledger
understates the tax base — stated by the model's own design. Rentier arms capture no tax, so the
combined-ledger comparison is not defined for them.

**Sampling.** 3 matched seeds.

**Verification.** 0 failures.

**Result.** The fiscal investing state is **worse off** than the frozen state on both ledgers:
−4.10 (income tax only) and −4.20 (income + consumption tax), at 6%. It still deepens the pipeline
(11.6 vs 10.4 mean years, tertiary 0.38 vs 0.21). Order and peer motives fund only lower secondary
(level 2) and never upper secondary/tertiary; the fiscal 10-year-horizon state funds nothing beyond
primary (10.2 years, tertiary 0.14). A rentier with order motive funds L2 at year 41; peer
emulation at year 34.

**Interpretation.** **Challenges** a fiscal-benefit explanation of state schooling investment: in
this structure the state invests and loses money on its own ledger, so the model must be read as
saying that non-fiscal motives (order, legitimacy, emulation) or misperception carry the
investment, or that the model's tax base is too narrow. The frozen-state comparison is the naive
benchmark and it wins on the ledger — that is a substantive negative for the "investment pays"
story, not a coding failure. Cannot identify: which motive real states had; these are scenarios.

**Evidence to collect next.** Budget and tax-base series plus archival budget debates for one
country, to see whether the measured fiscal return was positive.

**Reproduce.** `PYTHONPATH=code/triad "$PY" code/exp/run_triad_E14_E15.py runs 3 2000 2`.

---

## E18 — China-style Double Reduction synthetic variants (with no-effect baseline)

**ID and question.** Under what conditions does suppressing commercial tutoring plus expanding
school support reduce the paid tutoring burden — and does Trey's hypothesis (school homework help
and teacher feedback substitute for commercial tutoring) survive in this structure?

**Status.** completed (reps=3, N=5000, 18/18 runs, 90 s).

**Purpose.** policy counterfactual — **synthetic**, not a measured Double Reduction effect.

**Why the comparison is informative.** The no-effect baseline (A0) is the untreated system, so any
difference is the declared mechanism. Arms separate the ban from the support from their
combination, and vary enforcement and access.

**Model and version.** `code/ext_massabm` EXTENSION: school support = 0.5 score units of zero-price
gate preparation (one exam sd) for a share of the cohort; ban = `tut_ban` with `tut_ban_leak`.
This is an **independently named new implementation, not a reproduction** of any Chinese policy
model.

**Initial conditions and timeline.** 1920-2035; outcomes over cohorts 1995-2012.

**Arms and shared controls.** A0 no-effect baseline; A1 ban only (leak 0.5, default informal
substitute); A2 ban fully enforced (leak 0.0); A3 school support only, universal; A4 ban + support;
A5 ban + support, 60% access. Seeds 27000+r.

**Outputs.** Paid tutoring spend by gate; take-up at each gate; basic completion; college entry;
degree share; college/basic income.

**Assumptions / sources.** Support = 0.5 exam sd, public cost 0.30 index units per supported
pupil-year (declared; **not** budget-constrained in massabm). No COVID or labour-market shock is
modelled; this is not the 2021 China residual.

**Sampling.** 3 matched seeds; sd across seeds.

**Verification.** Extension identity-tested; 18/18; 0 failures. One verdict-logic amendment
disclosed in `ERROR_LOG.md` #12.

**Result.**

| arm | paid tutoring spend | apex share of spend | board take-up | basic completion | college Q3–5 |
|---|---|---|---|---|---|
| A0 no-effect baseline | 4,092 | 0.411 | 0.932 | 0.717 | 0.372 |
| A1 ban only (leak 0.5) | 3,669 (−423 vs A0) | 0.341 | 0.870 | 0.716 | 0.389 |
| A2 ban fully enforced | **1,519 (−63%)** | 0.000 | 0.000 | 0.717 | 0.394 |
| A3 support only (universal) | **4,815 (+723)** | **0.675** | 0.829 | **0.724** | 0.312 |
| A4 ban + support | **4,098 (+6 vs A0)** | 0.675 | 0.687 | 0.725 | 0.310 |
| A5 ban + support, 60% access | 3,855 (−237 vs A0) | 0.565 | 0.740 | 0.719 | 0.340 |

**Predeclared verdict.** Substitution was to be accepted if ban+support spend fell below ban-only
spend by >2 seed sd with no learning loss. It does **not**: ban+support spend is +429 **above**
ban-only (2sd ≈ 107), i.e. back to the untouched baseline. The learning guard *passes* (completion
is +0.008 **higher**, not lower — the auto-generated "LEARNING CHANGED" line tested |Δ| rather than
"lower", corrected and disclosed in `ERROR_LOG.md` #12 and `runs/E18/README.md`).

**Interpretation.** **The strongest negative result in the suite: Trey's school-support
substitution hypothesis is not supported by this structure.** Universal free school support
*raises* paid tutoring spend by 18% and nearly doubles the apex gate's share of spend (0.41 → 0.68),
because support moves more students near a high-stakes cutoff, where a marginal score gain is worth
most. Only full enforcement of a ban reduces paid spend (−63%), and it does so by removing the
market, not by substituting school support. Partial access (60%) reduces spend modestly (−6%) and
leaves completion unchanged, which is the only configuration where support helps without
intensifying the race. Cannot identify: whether real Chinese school support was accompanied by
the kind of gate-stakes reduction this model lacks, or whether enforcement was the operative
mechanism. Not a measured Double Reduction effect.

**Evidence to collect next.** Dated, gate-specific Chinese tutoring-price and take-up series
2019-2024 separated by enforcement intensity and by school-support exposure; a real
no-effect baseline requires pre-2021 trends, not a synthetic arm.

**Reproduce.** `PYTHONPATH=code/ext_massabm "$PY" code/exp/run_E18.py --reps 3 --N 5000 --workers 2 --out runs/E18`.

---

## E19 + E20 — Descriptive gate paths and cross-country transfer (pilot)

**ID and question.** E19: what do comparable model gate paths look like for the Philippines vs a
mature-gate East-Asian schedule? E20: does grafting the Philippine overseas/recognition channel
onto a Korea-like schedule improve on a naive persistence benchmark?

**Status.** **pilot only** (reps=2, N=5000, 6 runs). Hong Kong: **data blocked**.

**Purpose.** description / transfer.

**Why the comparison is informative.** Descriptive reconstruction is the only defensible use of an
uncalibrated default model. The transfer comparison is model-to-model and includes a declared null.

**Model and version.** massabm unmodified, presets `philippines` and `korea`.

**Initial conditions and timeline.** 1920-2035.

**Arms and shared controls.** PH baseline; Korea-like preset; Korea-like + PH overseas/recognition
channel (transfer). Seeds 29000+r.

**Outputs.** Cohort basic completion and degree share at 10/20/30/40-year horizons; informal share;
income premium; the manuscript's calibration table for the PH default model.

**Assumptions / sources.** Nothing is calibrated; defaults are used. **All numbers are simulated.**

**Sampling.** 2 matched seeds.

**Verification.** 6/6 runs; 0 failures.

**Result — E19 descriptive (simulated).** PH baseline cohort basic completion: 0.730 (1980), 0.740
(1990), 0.662 (2005), 0.674 (2018); degree share 0.198 (1990), 0.152 (2015). Korea-like path:
basic 0.801 → 0.820, degree 0.324 → 0.470.

**The default model does not match the manuscript's own stated targets.** Model vs target:
basic completion entry 1990-95 = **0.739 vs ~0.55-0.62** (too high); Q1 = 0.423 vs ~0.35-0.40
(too high); Q5 = 0.815 vs ~0.90+ (too low); basic→college transition 2008-12 = **0.227 vs ~0.70**
(far too low); prof-track entry share = **0.097 vs ~0.04-0.06** (too high); tertiary GPI
**0.868 vs ~1.2-1.3** (too low); degree share 0.198 vs ~0.14-0.20 (inside); informal share 0.514 vs
~0.5-0.6 (inside); board-exam tutoring 0.933 (matches "high"); basic-gate tutoring 0.057
(matches "thin"); OFW professional share 0.156 vs "<~0.25" (inside).

**Result — E20 transfer (declared null).** Grafting the PH overseas channel onto the Korea-like
schedule: degree share 0.470 → 0.402, basic 0.820 → 0.818, informal share 0.394 → 0.292. The
transfer does **not** improve on the naive persistence benchmark for basic completion (Δ = −0.002)
and *lowers* the degree share; only the informal share moves materially.

**Interpretation.** E19: the manuscript's qualitative claims must be read as coming from a
calibrated parameter set, not from the defaults; the default model's largest miss is the
basic→college transition (0.23 vs 0.70), which is a substantive warning before any policy use.
E20: the declared null holds — a small overseas channel does not move aggregates driven by the
domestic formal sector. Nothing about Hong Kong is claimed; HK is data blocked.

**Evidence to collect next.** Load the local HK school-planning series and a Philippine
basic→college transition series; calibrate before any HK/PH descriptive or transfer claim. Then
re-run E19/E20 with a frozen calibration and an untouched holdout.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E19_E20.py --reps 2 --N 5000 --workers 2 --out runs/E19_E20`.

---

## Proposed cells (NOT run — recorded as proposed, never claimed)

- **E4 children's four states (childworld):** proposes using `childworld.py` school/work/both/
  neither states; not run (budget).
- **E9 return compression and outside options:** partly covered by the E8 slope; not separately run.
- **E11 education–economy mechanisms (floorworld S1–S5):** not run.
- **E12 long-run massification trajectories:** covered descriptively only inside E19.
- **E16 credential information/recognition:** not run (no reader-model module built).
- **Cross-cutting multimechanism recovery study:** not run.
- **Atlas engine cells** (floorworld, childworld, relfloor*, firms/model.py): inspected only; no cell
  claimed.

---

## E18b — FAIR substitution test for the school-support hypothesis (follow-up, Council brief 002)

**ID and question.** E18's support module was a universal, free, additive +0.5 sd score boost with no
demand channel, no budget, no capacity limit and no teacher/homework change; under rank gates that
mechanically crowds takers to the threshold. If support is allowed to crowd out paid tutoring's
marginal value, or is targeted or capacity-limited, does paid tutoring fall relative to ban-only?

**Status.** completed (6 arms × 3 matched seeds = 18/18 runs, N=5000, 91 s).

**Purpose.** fair test of the Council's C10 hypothesis; corrects the unfair-test criticism of E18.

**Why the comparison is informative.** Every arm uses the same cohorts, seeds (27000+r), ban
(`tut_ban=['apex','board']`, leak 0.5), support level (0.5 sd) and outcome window as E18, so the only
difference from E18 is that support now damps tutoring's marginal effect.

**Model and version.** `code/ext_massabm`, new declared parameter `tut_suppress`: a supported pupil's
tutoring effect becomes `tut_effect × clip(1 − tut_suppress·s, 0, 1)` with s = 0.5 score sd.
`tut_suppress=0` is the stock E18 additive behaviour. This is an **independently named new
implementation of a substitution channel, not a reproduction**. A literal CES elasticity-2 aggregator
was predeclared as rejected for this test: any finite-elasticity CES has a positive cross-partial
(additive/complementary) and cannot produce crowding-out — implementing it would have repeated E18's
unfair test in different clothing.

**Arms.** A0 untreated baseline; C0 ban only; C1 ban + universal support, suppress=1 (halves tutoring
value at s=0.5); C2 universal suppress=2 (full displacement — a limit case); C3 support targeted to
Q1–Q2 (40% of cohort), suppress=2; C4 support capacity/budget-capped at 25%, suppress=2.

**Outputs.** Paid tutoring spend total and by gate; apex share of spend; board take-up; basic
completion (learning guard); college entry.

**Sampling.** 3 matched seeds; sd across seeds.

**Verification.** 18/18 runs; 0 failures; extension identity test still passes after the patch.
One formatting bug in the auto learning-guard line (2sd=nan) is disclosed in `runs/E18b/README.md`;
the underlying completion values are correct and higher than ban-only in every arm.

**Result.** Paid spend (mean of 3 matched seeds), difference vs ban-only C0 with 2 seed sd:

| arm | paid spend | vs C0 | apex share | board take-up | completion |
|---|---|---|---|---|---|
| A0 untreated | 4,092 | +423 | 0.411 | 0.932 | 0.717 |
| C0 ban only | 3,669 | — | 0.341 | 0.870 | 0.716 |
| C1 ban + support, suppress=1 | **2,377** | **−1,291.5 (2sd 92)** | 0.526 | 0.607 | 0.723 |
| C2 ban + support, suppress=2 (limit) | 0 | −3,668.5 (2sd 91) | 0.000 | 0.000 | 0.726 |
| C3 ban + support targeted Q1–Q2, suppress=2 | **3,327** | **−341.4 (2sd 149)** | 0.333 | 0.871 | 0.718 |
| C4 ban + support capacity-capped 25%, suppress=2 | **2,427** | **−1,241.2 (2sd 101)** | 0.308 | 0.563 | 0.719 |

**Predeclared decision rule fires: C10 is WITHDRAWN.** Every non-limit substitution/targeting/
capacity arm puts paid spend below ban-only by more than 2 seed sd (C1 −1,291.5 vs 2sd 92.3;
C3 −341.4 vs 148.7; C4 −1,241.2 vs 101.4), and completion is *higher* than ban-only in all of them.
C2 is a construction limit (supported pupils face zero marginal value from tutoring) and is not relied on.

**Interpretation.** Corrects E18: the earlier "the race absorbs the subsidy" result is an artefact of
an additive, universal, unbudgeted support input with no demand channel. Once school support genuinely
substitutes for the marginal value of paid tutoring — or is targeted to the bottom two quintiles, or is
capacity-limited — paid spend falls sharply, and learning does not fall. The defensible claim is:
*an additive universal support subsidy is absorbed by the race; a substitutive, targeted or
capacity-limited one is not.* Cannot identify: the true substitution elasticity, or whether real
Chinese school support operated through the tested channel. Still synthetic, not a measured Double
Reduction effect.

**Evidence to collect next.** Dated Chinese tutoring take-up/price series by enforcement and
school-support exposure; a direct estimate of the substitution elasticity between school homework help
and paid tutoring.

**Reproduce.** `PYTHONPATH=code/ext_massabm "$PY" code/exp/run_E18b.py --reps 3 --N 5000 --workers 2 --out runs/E18b`.

---

## E13c — LEVEL-MATCHED rival for the graduate-supply shock (follow-up, Council brief 002)

**ID and question.** E13b's worlds were not level-matched (baseline formal share 0.286 vs 0.463; rival
degree income up to 32.3 vs 2.93). Are E13b's formal-probability findings an artefact of those level
differences?

**Status.** completed (calibration 15 runs + 36/36 stage-2 runs, N=5000, 189 s).

**Purpose.** theory discrimination; level-matched version of Prediction 2.

**Why the comparison is informative.** Both worlds now have (i) the same baseline formal share
0.2862, (ii) the same vacancy path shape, (iii) the same households, shock and seed list, and (iv) as
close a degree-income level as is achievable without changing household behaviour.

**Model and version.** `code/ext_massabm`, `mode='hc_fair_slots'` with two declared level-matching
parameters: `fair_slots_mult` (scales the rival's formal vacancy count) and `fair_income_scale`
(scales the rival's wage level). Stock modes untouched; extension identity test still passes.

**Initial conditions and timeline.** No K-12 reform; 1995 tuition shock; labour market 2010-2030.

**Arms and shared controls.** Surplus vs level-matched rival at sigma ∈ {0.5, 1, 2}, × {no shock,
college half price 1995, 80% off 1995}; 3 paired reps; seeds 20000+r.

**Outputs.** Paired change vs no shock in diploma holders' formal-employment probability, diploma
absolute income, degree income and dip/deg ratio.

**Sampling.** 3 paired reps; calibration is deterministic given sigma (seed 20000).

**Verification.** 36/36 runs; 0 failures; calibration achieved and logged in `e13c_calibration.csv`.

**Result — achieved level match.** Formal share matched at every sigma (unmatched 0.4634/0.4002/0.3980
→ **0.2795 / 0.2795 / 0.2875** vs target 0.2862). Degree income matched at sigma=2 (1.987 → **2.706**
vs target 2.926, −7.5%); at sigma=0.5 and 1.0 the wage scale could not hit the target without changing
entrants (achieved 11.388 and 1.457), so those cells remain income-mismatched — stated, not hidden.

Paired change vs no shock (mean over 3 matched seeds; seed sd in brackets), college half price:

| world | sigma | Δ formal rate (diploma) | Δ diploma income | Δ dip/deg ratio |
|---|---|---|---|---|
| surplus | — | **−0.1511 (0.0217)** | −0.0583 (0.018) | +0.0466 |
| rival | 0.5 | +0.0085 (0.0108) | −0.0270 (0.0480) | +0.0422 |
| rival | 1.0 | +0.0095 (0.0077) | +0.0001 (0.002) | −0.1020 |
| rival | 2.0 | −0.0054 (0.0027) | +0.1252 (0.017) | +0.1157 |

At 80% off the pattern is the same: surplus Δformal −0.1641 (0.019); rival +0.0204 / +0.0119 / −0.0150.

**Predeclared decision rule fires the other way from E13b: Prediction 2 SURVIVES in its
formal-access form.** The surplus world shows a large formal-probability fall (−15.1 pp, 7× its seed
sd); the level-matched rival never falls materially (σ=0.5 and 1.0 are *positive*; σ=2 is −0.5 pp, a
20-30× smaller magnitude and not economically meaningful). The diploma-income fall also disappears in
the rival once levels are matched (σ=2 shows +0.125, σ=1.0 ~0, σ=0.5 noisy-negative but inside its
own seed sd) — so E13b's income-based contradiction was indeed a level artefact.

**Interpretation.** Prediction 2 is defensible **only in its formal-access form**: credential floors,
not competitive skill pricing, are what push diploma holders out of formal jobs when graduates surge.
The absolute-income version of the claim does not survive level-matching (consistent with E13b's
precision caveat). Cannot identify: the true substitution elasticity; whether real formal hiring reads
credentials or measured skill. Residual limitation: degree-income level matching is exact only at
σ=2; the income estimand at σ=0.5/1.0 should be read as directionally informative only.

**Evidence to collect next.** Employer hiring data distinguishing credential from measured-skill
screening, and an estimated skilled/unskilled substitution elasticity for the Philippines.

**Reproduce.** `PYTHONPATH=code/ext_massabm "$PY" code/exp/run_E13c.py --reps 3 --N 5000 --workers 2 --out runs/E13c`.

---

## E21 — External enrolment benchmark vs observed UIS/WDI GER (new data, data-hunter)

**ID and question.** Do the uncalibrated massabm cohort trajectories reproduce the LEVEL and SHAPE of
observed gross enrolment ratios in the Philippines and a Korea-like schedule, using only observed
UIS/WDI cells?

**Status.** completed (4 model runs, 2 presets × 2 seeds, N=5000, 10 s).

**Purpose.** external validation of the education series; supplies the observed benchmark that E19
lacked.

**Why the comparison is informative.** E19 compared the model with the manuscript's own rough targets
(internal). This cell uses an independent, source-attributed observed series (UIS SDG4 2026-11, UIS
EDUNONCORE Feb-2020, WDI-via-UIS), so model error is measured against observation rather than against
the paper.

**Model and version.** massabm unmodified, presets `philippines` and `korea`. Model GER is declared as
enrolment stock / (N × stage duration), with the secondary duration switching 4→6 on the model's own
K-12 reform flag — not tuned to the data. Observed GER is in percent, so the model ratio is ×100.

**Initial conditions and timeline.** 1920-2035 model; comparison window 1980-2020.

**Arms and shared controls.** Two presets; seeds 31000+r.

**Outputs.** Model vs observed GER by level: n overlapping observed years, means, correlation, MAE,
bias; full year-by-year series with observed source provenance.

**Assumptions / sources.** Only observed cells used; years where the observed series is absent are
skipped, not imputed. The Korea-like preset is a **stylised schedule, not a calibrated Korea**, so a
miss there is a statement about the preset.

**Sampling.** 2 seeds; model variation across seeds is negligible relative to the level gaps reported.

**Verification.** 172 series-years matched; 0 failed runs; unit conversion checked (initial version
had a percent/fraction mismatch, caught and fixed before reporting).

**Result.**

| country | indicator | n | years | observed mean | model mean | corr | MAE (pp) | bias (pp) |
|---|---|---|---|---|---|---|---|---|
| PHL | ger_primary | 37 | 1980-2020 | 102.1 | 99.7 | 0.309 | **3.4** | −2.4 |
| PHL | ger_secondary | 36 | 1980-2020 | 72.3 | 79.9 | −0.326 | 12.6 | +7.6 |
| PHL | ger_tertiary | 36 | 1980-2020 | 27.3 | 24.6 | **−0.397** | **5.4** | −2.7 |
| KOR | ger_primary | 21 | 2000-2020 | 100.0 | 100.0 | 0.643 | 0.7 | 0.0 |
| KOR | ger_secondary | 21 | 2000-2020 | 97.7 | 88.6 | 0.607 | 9.0 | −9.0 |
| KOR | ger_tertiary | 21 | 2000-2020 | 93.7 | 41.0 | 0.156 | **52.7** | −52.7 |

**Interpretation.** For the Philippines the default model gets the **levels** roughly right — primary
and tertiary within 3-5 pp, secondary +7.6 pp — which is more encouraging than E19's comparison with
the manuscript targets suggested. But it fails the **shape** of the tertiary series (corr −0.40): the
model's tertiary ratio does not track the observed post-1990 expansion, so its trend should not be
used for forward statements without calibration. The Korea-like preset badly under-predicts tertiary
GER (41 vs 94) — unsurprising for a stylised schedule, and a warning against reading any Korea-like
result as a Korea forecast. Cannot identify: whether recalibration of the tertiary gate (cost, apex
seats, overseas channel) would fix the shape or whether the mechanism is missing.

**Evidence to collect next.** Use `04_data/data/gmr_annual_1980_2020_imputed.csv` (flagging imputed
cells) to extend the benchmark to Cambodia, China, Hong Kong and Japan; fit the model to pre-2010
observed cells and evaluate on 2011-2020 as a genuine holdout.

**Reproduce.** `PYTHONPATH=code/massabm "$PY" code/exp/run_E21.py --reps 2 --N 5000 --workers 2 --out runs/E21`.

---

## C1 — Recovery / identification study (cross-cutting; batch C, task-8)

**ID and question.** Given only six aggregate moments with measurement error, can the three rival
generators be told apart — surplus/relational-floor, Yoo fixed cutoff, competitive CES — and what
happens to a truth that is not in the candidate set?

**Status.** **completed** (61 s, 2 measurement-error datasets per truth, N=2000).

**Purpose.** recovery / identification; the cross-cutting study the handoff ranks highest.

**Why the comparison is informative.** All three candidates are fitted to the *same* moments by
minimum weighted distance; the classifier is whichever family's best grid point is closest. If the
fitted distances are nearly tied, the moments cannot separate the mechanisms no matter how well each
fits.

**Model and version.** massabm unmodified for the surplus/floor world (`mode='full'`, grid:
floor ∈ {none, adaptive, fixed} × college cost ∈ {0.4, 0.6, 0.8}) and the competitive world
(`mode='hc_fair_slots'`, grid: σ ∈ {0.5, 1, 2} × `hc_school` ∈ {0.03, 0.05, 0.07}); plus
`code/new/toy_generators.py` — **independently named new implementations, not reproductions** of
Yoo or any atlas engine — for the Yoo fixed-cutoff rival (grid: t* ∈ {−0.5, 0, 0.5} × β ∈ {0.15,
0.25, 0.35}) and for the truth outside the set (random-among-eligible).

**Initial conditions and timeline.** massabm 1920-2035, cohorts 1995-2012, labour 2010-2030; toy
models are cross-sections of 2,000 households.

**Arms and shared controls.** Four truths (G1 surplus/floor, G2 Yoo, G3 competitive CES, G4 outside)
× 2 noise draws each; measurement error lognormal σ = 0.06 with additive σ = 0.02 on the gap.

**Outputs.** Six moments (completion, tertiary share, degree premium, formal share, prep take-up,
Q5−Q1 completion gap); confusion matrix; distances; recovery share.

**Assumptions / sources.** Toy generators are declared reduced forms, not estimates; the moment set is
deliberately the kind of aggregate available from survey/administrative series.

**Sampling.** 2 noise draws per truth; candidate grids 9 points per family.

**Verification.** 0 failed runs; truth moments and candidate moment surfaces written to CSV for audit.

**Result.** Confusion matrix (rows = truth, columns = assigned family; 2 draws each):

| truth | surplus/floor | Yoo | competitive CES |
|---|---|---|---|
| G1 surplus/floor | **1** | 0 | 1 |
| G2 Yoo cutoff | 0 | **2** | 0 |
| G3 competitive CES | 2 | 0 | **0** |
| G4 outside (random among eligible) | 2 | 0 | 0 |

Distances: the surplus/floor and competitive-CES candidates fit G1 and G3 almost identically
(e.g. G3: d_surplus 0.012-0.019 vs d_competitive 0.012-0.019 — a tie, broken arbitrarily by
floating-point ordering), while the Yoo family is clearly separated (distance 25-29 on the
massabm-truth datasets).

**Interpretation.** **NO IDENTIFICATION between the surplus/floor and competitive-CES worlds on
these six aggregate moments** — the competitive generator is never recovered (0/2), and its fitted
distance is statistically indistinguishable from the surplus candidate's. Yoo's fixed-cutoff world
*is* recovered (2/2) because its prep take-up is 1.0 and its Q5−Q1 gap is 0.05, which no other
family can match. The truth outside the model set is confidently (2/2) assigned to the surplus
family: **forced identification** — the candidates claim to identify a generator that is not in the
set. By the predeclared generator-level rule 2 of 3 are recovered (PASS), but the substantive verdict
is the stronger negative: these moments cannot separate the two accounts the paper is about.
Cannot identify: whether richer moments (gate-specific tutoring, formal vs informal transitions,
distribution near the cutoff) would separate them — that is the next design.

**Evidence to collect next.** Add distributional moments near the admission cutoff, credential-specific
formal-transition rates, and tutoring-by-gate data to the moment set; re-run recovery with a truth
outside the set that includes measurement error in *panel* form.

**Reproduce.** `PYTHONPATH=code/massabm MASSRUN_EXP=code/exp "$PY" code/exp/run_C1.py --N 2000 --out runs/C1`.

---

## C2 — E11 education–economy mechanisms (atlas floorworld S1–S5, Philippines; batch C)

**ID and question.** In floorworld's structures S1–S5 with the same Philippine schedules, is the
1980–2020 rise in enrolment and formal jobs **generated** by the economy–education feedback, or
**supplied** by the exogenous schedules?

**Status.** **completed** (aggregate 56-year scalar model; instant).

**Purpose.** mechanism / atlas-engine (first atlas cell in this package).

**Why the comparison is informative.** Freezing the supplied schooling schedules at their 1980 values
removes the input-driven channel; whatever rise remains must come from the structure's own
wage-premium response and job generation. `supplied_share = 1 − frozen_rise/baseline_rise`.

**Model and version.** `floorworld.py` copied **unmodified** from
`01_sources/atlas-main-55732f4/engine/` into `code/engine/floorworld.py`; structures S1–S5;
country schedules `COUNTRIES['Philippines']`; `th` = midpoint of each `PRIORS` range (declared; same
for every structure so structures are compared at identical parameters).

**Initial conditions and timeline.** 1980–2035; report years 1980/1990/2000/2010/2020/2035.

**Arms and shared controls.** 5 structures × 2 schedule regimes (baseline supplied PHL schedules;
`floor_lower`/`floor_upper`/`he_cap`/`vshare` frozen at 1980 values).

**Outputs.** floor, tertiary, formal, complex, informal, output, surplus, overeducation by year;
supplied-share decomposition 1980–2020.

**Assumptions / sources.** floorworld's own stylised schedules and priors; `th` midpoints are a
declared choice, not an estimate.

**Sampling.** Deterministic given `th`; no random draws in these structures (the engine's MC layer was
not used).

**Verification.** Runs to completion for every S and regime; `c2_floorworld.csv` and
`c2_decomposition.csv` retained.

**Result.** 1980→2020 (baseline) and supplied share:

| structure | floor | tertiary | formal | complex |
|---|---|---|---|---|
| S1 | 0.702→0.918 (supplied +1.13) | 0.200→0.350 (+1.00) | 0.144→0.357 (+0.23) | 0.001→0.041 (+0.36) |
| S2 | 0.702→0.914 (+1.14) | 0.200→0.301 (+1.00) | 0.097→0.306 (+0.10) | 0.000→0.004 (negligible) |
| S3 | 0.702→0.925 (+1.10) | 0.200→0.350 (+1.00) | 0.097→0.434 (+0.22) | 0.000→0.194 (+0.33) |
| S4 | 0.702→0.919 (+1.13) | 0.200→0.350 (+1.00) | 0.076→0.282 (+0.40) | 0.000→0.194 (+0.33) |
| S5 | 0.702→0.904 (+1.19) | 0.200→0.350 (+1.00) | 0.076→0.138 (+0.33) | 0.000→0.004 (negligible) |

**Interpretation.** **The schooling rise is supplied, not generated** in every structure: with the
supplied schedules frozen at 1980, basic completion does not rise at all (supplied share ≈ 1.1-1.2,
i.e. the frozen run can even fall), and the tertiary stock is entirely capped by `he_cap`. **The
formal-job rise is not from schooling**: 60-90% of it survives with schooling frozen in all five
structures, because it comes from the investment/industrial-policy path and, in S3/S4, capability
feedback. Which structure builds the *complex*-jobs leg is what separates S1 (legibility of human
capital) from S3/S4 (capabilities) and S2/S5 (industrial policy): complex jobs reach 19-20% in S3/S4
but stay negligible in S2/S5 at these priors. So the honest headline: **schooling is supplied;
formal jobs are not supplied by schooling** — no structure generates the education rise itself under
this design. Cannot identify: whether a different `th` (e.g. higher `resp` or `budget`) would let the
premium response generate more of the enrolment rise; the midpoint priors are one draw.

**Evidence to collect next.** Sweep `resp`/`budget`/`v_protect` (the schooling-response parameters)
over the floorworld priors, and compare the generated education path with the observed PHL series.

**Reproduce.** `MASSRUN_EXP=code/exp "$PY" code/exp/run_C2.py --out runs/C2`.

---

## LOOP2 — Country configs, calibration loop, longitudinal cohort flows (iteration 2, task-12; Council brief 004)

**Status.** **completed** for: C3 finish, country configs, calibration loop (fit/check split, freeze
test), cohort ledger. **DATA BLOCKED**: shadow-education targets, wage-premium dynamics.

**Files.** `loop2/` — `COUNTRY_CONFIGS.md`, `CALIBRATION_TABLE.csv`, `freeze_both.csv`,
`cohort_ledger_annual.csv`, `cohort_horizon_table.csv`, `balance_checks.csv`, `findings.txt`,
`findings_ledger.txt`, `LOOP2_STATUS.md`, `configs.py`, `calibrate2.py`, `ledger.py`.

**Brief-004 amendments applied.** (1) every target row labelled `role` fit/check with a predicted
sign per candidate world, written before fitting; (2) fit 1980-2010, held out **2011-2024**, HKG is
the **untouched country**; (3) two real-data check-only moments excluded from the fit — WDI
industry+services employment share and agriculture share (formal-access / informality proxies);
shadow take-up and wage-premium dynamics declared data blocked, never fitted; (4) forced-ID rate
inherited from C1 = 2/2; (5) freeze-both symmetry test run for four countries; (6) fitted objects are
household demand, provider entry/capacity and teacher-tutor capacity — **shadow take-up and provider
mix are checks, never fitted shares**.

**New mechanism (brief 004's recommended structural variable).** Provider supply/entry and
teacher-tutor capacity added to the tutoring layer in `code/ext_massabm`: the paid-tutoring market
price rises with last year's take-up relative to sector capacity (`prov_capacity`, `prov_elasticity`),
and teacher-tutors serve a cheaper, capacity-limited share (`teacher_capacity`, `teacher_price_mult`).
Declared reduced form; stock behaviour unchanged when the mechanism is neutralised (tested).

**Result — per-country fit (MAE pp, fit 1980-2010 / held out 2011-2024):**

| country | role | in-sample | held-out | biggest held-out miss |
|---|---|---|---|---|
| PHL | fitted | 9.0 | 14.6 | formal-access proxy 36.3 pp |
| KHM | fitted | 38.8 | 19.6 | completion upper-secondary 45.8 pp |
| HKG | untouched | 10.4 | 28.2 | formal-access proxy 45.4 pp |
| CHN | fitted | 19.2 | 8.6 | completion upper-secondary 15.8 pp |

PHL tertiary GER: in-sample 2.7 pp but **held-out 16.5 pp** — the model fits the pre-2011 level and
misses the post-2011 shape, matching E21/E19.

**Result — freeze-both symmetry.** With wages/jobs frozen, tertiary GER rises *more* than baseline in
PHL (+6.6 vs −2.2), KHM (+2.5 vs −2.7), HKG (+2.2 vs +0.6) and less in CHN (+4.9 vs +7.4). With the
schooling feedback frozen, the formal-access path keeps 60-100% of its rise (PHL 8.0/12.7, KHM
12.3/9.9 — it rises more, HKG 2.1/3.8, CHN 8.5/12.3). **The two-way claim is largely a schedule in
this structure**: neither path is generated by the other.

**Result — cohort ledger.** Balance checks pass exactly for all four countries (stock-identity max
abs error 0.0, cohort-conservation error 0.0, no rate outside [0,1]). 10/20/30/40-year table in
`cohort_horizon_table.csv`; PHL upper-secondary completion falls from 0.741 (2000 cohort) to 0.627
(2020 cohort) because K-12 makes JHS holders non-completers of the basic cycle — a regime artefact
that the ledger makes visible rather than hides.

**Interpretation.** The assessable layer now exists: configs with every parameter labelled, a
fit/check calibration table with held-out misses, an exact-balancing cohort ledger, and a freeze test
that says the two-way story is a schedule. The biggest available miss is the **formal-access moment
(36-45 pp)**: the model's formal sector grows far more than observed employment structure, which
points at the labour-market block rather than at education. The biggest education miss is
**upper-secondary completion in KHM (45.8 pp)** and PHL's **post-2011 tertiary shape (16.5 pp held-out
vs 2.7 in-sample)**. Shadow-education targets are data blocked, so no shadow claim is made.

**Identifiability.** Calibration does not make surplus and competitive CES distinguishable — it moves
point estimates inside a family. Forced-ID rate stays 2/2. What would: gate-specific shadow take-up,
formal-vs-informal transition rates by credential, density near admission cutoffs, panel shock responses.

**Reproduce.**
`PYTHONPATH=code/ext_massabm:loop2 MASSRUN_EXP=code/exp "$PY" loop2/calibrate2.py --draws 24 --N 2000 --Nfine 3000 --out loop2`
`PYTHONPATH=code/ext_massabm:loop2 MASSRUN_EXP=code/exp "$PY" loop2/ledger.py --N 2500 --out loop2`
