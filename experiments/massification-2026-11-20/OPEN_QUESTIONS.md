# OPEN QUESTIONS — what remains, what would settle it, and what it would cost

Compiled by the Lead from the fleet's work packages, the audit, the data ledger, and the two
synthetic Council sessions. Every item states a feasible data requirement, a decision threshold, and
a cost estimate. Items are ordered by how much they could change the paper, not by ease.

## A. Claims that must be withdrawn or rewritten before submission

The Council's brief 002 withdraw list (recorded because it is binding on the report's language):

1. **Withdraw**: the graduate-supply *absolute-income* discriminator ("the competitive world cannot
   reproduce diploma-holder losses"). A matched-elasticity rival does reproduce near-zero/negative
   diploma-income changes at σ ≤ 1 (E13b, 6 paired reps). Keep only the formal-employment-probability
   version, and say "simulation-only".
2. **Withdraw**: the basic-bar sweep (3%→76%) as a *discovery*. It is Yoo (2003)'s effort-near-cutoff
   result. Cite Yoo, keep only the ban/leak accounting as new.
3. **Withdraw**: E18's school-support arm as a *Double Reduction test*. It is a universal, free,
   additive +0.5 sd score module; the correct claim is the model-class one ("a universal score
   subsidy can be absorbed by the positional race") pending the E18b substitution test.
4. **Withdraw**: E3's liquidity collapse and E5's memory monotonicity as *discoveries*. They are
   near-mechanical consequences of the coded constraints; report as model sensitivity, not family
   behaviour.
5. **Withdraw**: any four-country / Hong Kong / transfer claim. The default Philippine model misses
   its own targets; Hong Kong data were blocked; the transfer result is model-to-model and null.
6. **Withdraw / re-scope**: "the floor is an engine of persistence". At 4 reps, the floor's own
   contribution to persistence holding ranking fixed is at seed noise (|Δ| ≤ 0.002). What survives is
   the floor's *movement* and the allocation rule.

## B. Ranked experiments that should run next

| # | experiment | arms / design | estimand | decision threshold | cost | status |
|---|---|---|---|---|---|---|
| 1 | **E18b fair substitution test** (Double Reduction) — **COMPLETED** | substitution (linear-damping) support; targeted bottom-quintile; capacity-capped | paid tutoring spend + completion guard | decision rule fired: C10 withdrawn. Universal substitution arm −1,292 vs ban-only (2sd 92); targeted −341 (2sd 149); capacity-capped −1,241 (2sd 101); completion higher in every arm. **Next: estimate the substitution elasticity** between school support and commercial tutoring from data. | done (91 s, 18/18 runs) | completed |
| 2 | **E13c level-matched rival** — **COMPLETED** | level-match formal share, degree-income level, vacancy path, shock; σ ∈ {0.5,1,2} | Δ diploma formal-employment probability | if the formal-probability gap survives level-matching ⇒ Prediction 2 survives in formal-access form | done (36/36 stage-2 runs, 189 s) | **survives in formal-access form**: surplus −0.1511 (±0.0217); rival +0.0085 / +0.0095 / −0.0054 at σ=0.5/1/2 (28× smaller at σ=2). Degree income matched only at σ=2 — caveat recorded. Withdraw the absolute-income version. |
| 3 | **China Double Reduction with real policy data** | dated policy/evidence timeline; separate: restriction-only, school homework/teacher-feedback support, provider substitution, household time; no-effect baseline; heterogeneous enforcement | paid vs unpaid tutoring; parent/student time; total burden | needs a measured exposure and a later outcome; correlation ≠ causality | data acquisition + 1–2 h | data blocked (policy text not fetched; UIS/China series partial) |
| 4 | **Recovery / identification study** | simulate data from each rival (Yoo, Kang, GXL, surplus) with survey error; mask generator; fit all rivals; include truth outside model set | confusion matrix; no-identification verdict | a model must recover its own generator better than rivals; ≥ 2 of 3 rivals must be distinguishable | 30–60 min | not run |
| 5 | **E16 credential information / recognition** | domestic detailed reader vs coarse reader vs skill test vs formal eligibility; vary signal accuracy, screening cost, network access, cross-border recognition independently | hiring errors, exclusion, wages, certification demand | one reader structure must dominate on a stated outcome; recognition change must move access independently of skill | 10–20 min | not run |
| 6 | **E12 long-run 10/20/30/40-year trajectories** — **COMPLETED (batch B4)** | exogenous schedule vs endogenous decision; vary workforce turnover and births | cohort entry/progression/completion; wage and employment mix | matching a rising curve must not require a supplied trend | done (5 seeds, 60/60) | **requires a supplied trend**: EXO entry 0.22→0.55 is input-driven; ENDO generated path collapses 0.404→0.020 (cobweb, seed sd up to 0.38); post-hoc smoothing still 0.218→0.108. Degree share and premium are generated; births/vacancy growth/completion/turnover are declared inputs. |
| 7 | **Calibrate the Philippine model to its own targets** | fit the parameters that produce basic→college 0.227 vs ~0.70, GPI 0.868 vs 1.2–1.3, Q5 completion 0.815 vs 0.90+ | fit misses and their sources | report the fit and the residuals; no country claim without it | 20–40 min | required before any PH claim |
| 8 | **Hong Kong gate-path reconstruction** | historical rural/urban change, HKCEE/HKALE/HKDSE transition, tutoring demand by grade/provider | descriptor of gates and tutoring | needs HKEAA + C&SD + EDB series (some 403) | data acquisition + 20 min | data blocked |
| 9 | **Philippines nursing response** | add private provider capacity to the massabm overseas channel | licensed nurses per migrant | must approach the Abarcar–Theoharides ~9 estimate, not 0.25 | 30–60 min | proposed; October paper already flags this as its own failure |
| 10 | **Atlas-engine cells** (`floorworld`, `childworld`, `relfloor`, `firms`, `tutoring_abm`) | run each at documented budgets, then dock against the paper's Triad/Massabm | engine-vs-paper agreement | any direction reversal is a finding | hours (explicitly out of this window) | not run |

## C. Data that would change the conclusions (and what blocks it)

| need | why it matters | status / blocker |
|---|---|---|
| Philippines PSA FIES/APIS/LFS + DepEd/CHED/TESDA administrative series | the worked case has no national administrative series in this pull | **PSA and DepEd returned HTTP 403**; recorded as an access request, not guessed |
| UNESCO UIS adjusted net attendance (SDG 4.1.x) | attendance vs enrollment vs completion distinction | not in the SDG4 release pulled; needs UIS bulk download |
| China Double Reduction policy text + provincial implementation timing | separates policy exposure from COVID and from the 2021 youth residual | not fetched; needs MOE + provincial sources |
| China gaokao/zhongkao places, NBS youth unemployment (old/new definitions) | the China graduate labour-market model relies on a fitted 2021 step | not fetched |
| Hong Kong HKEAA grade distributions + C&SD attainment + EDB places | gate-path reconstruction | partial (some pages fetched); HKEAA historical tables not obtained |
| Cambodia employer skill-need survey, employer hiring requirements | the floor is a legal/employer rule, not just a degree share | not fetched (mlvt.gov.kh) |
| ILOSTAT labour statistics | informality, youth unemployment | HTTP 403 |
| Abarcar & Theoharides (REStat 2024) replication data | the ~9-nurses-per-migrant target | paper read second-hand; data not obtained |

## D. The questions a reader should ask of this package

1. Which numbers here are **simulated**? All of `05_experiments/` and `05b_experiments/`. The
   `04_data/` numbers are observed, with retrieval dates and sources.
2. Which numbers are **reproduced** vs **archived**? `03_audit/REPRODUCTION_MATRIX.md` labels every
   one; stored `results/` values are archived, not rerun.
3. Which manuscript claims survive? See §A; the report may claim the formal-probability version of
   Prediction 2, the floor/race decomposition, and the many-dated-readers framing. It may not claim
   the income discriminator, the open-access Double Reduction effect, or country validation.
4. What is the strongest result in the package? The **negative** ones: the matched-rival failure of
   the income discriminator and the school-support result (pending E18b). Strongest positive:
   the liquidity result (conditional) and the reproduction of the mechanism suite.
5. What would make this publishable? A level-matched rival (running), a fair substitution test
   (running), calibration of the Philippine case to disclosed targets, and one external test the model
   was not tuned on.
