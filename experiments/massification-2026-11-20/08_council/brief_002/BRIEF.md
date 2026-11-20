> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# RESULTS BRIEF 002 — new experiment suite (provisional, batch A)

- **sent by / date:** lead, 2026-11-20 ~12:45 Asia/Shanghai
- **purpose:** decide which of the 12 new experiment cells are genuine findings vs imposed by the
  coded rules; advise on the China school-support (Double Reduction) result, the matched-elasticity
  contradiction, and what the final report may claim.
- **what this informs:** the "what we learned" section and the claims/caveats in `SUMMARY_FOR_TREY.md`.
- **provisional or final?** PROVISIONAL — batch B (adversarial replication) is running in parallel;
  `E13b` and `E8` are being re-run at higher reps. A short brief 003 may follow.
- **follow-up cycle expected?** yes (brief 003 after batch B).

## 1. Artifacts

| artifact | path (relative to workspace root) | command | seeds | N | runtime | status |
|---|---|---|---|---|---|---|
| Experiment records (12 cells) | `05_experiments/EXPERIMENTS.md` | — | — | — | — | completed |
| Pre-declarations | `05_experiments/PRE_DECLARATIONS.md` | — | — | — | — | completed |
| Error/failure log | `05_experiments/ERROR_LOG.md` | — | — | — | — | completed |
| E0/E2 accounting gate | `05_experiments/runs/E2_cohort_arithmetic/` | new kat_cohort.py | deterministic | 200/cohort | <5 s | completed |
| E3 liquidity | `05_experiments/runs/E3/` | new run_E3.py on massabm | 21000+r | 5000 | 48 s | completed |
| E5 memory | `05_experiments/runs/E5/` | new run_E5.py | seed list | 5000 | 80 s | completed |
| E7 gate density | `05_experiments/runs/E7/` | new run_E7.py | 3000+r | 5000 | ~105 s | completed |
| E10 learning vs test (omega) | `05_experiments/runs/E10/` | new run_E10.py | seed list | 5000 | 60 s | completed |
| E13 graduate supply | `05_experiments/runs/E13/` | run_E13.py | 20000+r | 5000 | 81 s | completed |
| E13b matched-elasticity rival | `05_experiments/runs/E13b/` | run_E13b.py | — | 2000 | 13 s | completed, reps=1 (provisional) |
| E14 actor knockouts | `05_experiments/runs/E14_*/` | run_triad_E14_E15.py | — | — | — | completed |
| E15 state motives | `05_experiments/runs/E15_state_motive/` | run_triad_E14_E15.py | — | — | — | completed |
| E18 China school-support | `05_experiments/runs/E18/` | new run_E18.py | seed list | 5000 | 90 s | completed |
| E19/E20 HK/PH + transfer | `/tmp/massrun/runs/E19_E20/` (pilot; to be copied) | run_E19_E20.py | — | 5000 | 34 s | pilot only, HK DATA BLOCKED |
| Batch B replication | `05b_experiments/` (in progress) | — | — | — | — | running |

## 2. Claims table

| ID | claim | type | estimand | key numbers | where | set by hand | falsifier |
|---|---|---|---|---|---|---|---|
| C10 | School-based free exam support does **not** substitute for paid tutoring; it raises paid spend | simulation | Δ paid tutoring spend vs no-effect baseline | support-only Δ=+722.9 (2sd 63); ban+support vs ban-only Δ=+429.0 (2sd 107) | `05_experiments/runs/E18/findings.txt` | support worth 0.5 score sd; zero price; not budget-constrained; leak 0.5 | a support specification with substitute skill production producing Δ<0 |
| C11 | A full tutoring ban at leak=0 deletes 63% of paid spend, not all demand; at leak=0.5 only 10% | simulation | Δ total paid spend | ban enforced −2573; ban leak −423 | E18 | `tut_ban_leak` rule | a ban that leaves spend unchanged at leak=0 |
| C12 | Hard liquidity constraint collapses Q1 completion (0.462→0.017) and widens Q5–Q1 gap | simulation | Q1 basic completion, Q5−Q1 gap | 0.462→0.017; gap 0.321→0.781 | E3 | borrow=0; no interest rate modeled | credit expansion failing to close the gap |
| C13 | Longer memory raises college entry (0.212→0.511) and slows belief updating | simulation | Q3–5 college entry; belief speed | +0.2995; speed 0.297→0.0116 | E5 | belief_decay grid; population-average learning | non-monotone response |
| C14 | Basic-gate bar sweep moves tutoring 0.022→0.752; banning gates alone leaves 88% of total spend | simulation | share of takers; total spend | sweep +0.729 vs 2sd 0.012; ban-all total 4100→3601 | E7 | bar grid; gate payoff | sweep with no movement |
| C15 | Omega (productive share of tutoring) changes later income but not pass rates at this scale | simulation | pass rate; college income | pass 0.7166→0.7167; income 4.104→4.195 | E10 | omega grid; 0.25 yr per gate-year | pass-rate change under omega |
| C16 | Surplus world predicts diploma losers under graduate shock; competitive CES predicts gainers | simulation | Δ diploma income; Δ formal prob | −0.058 vs +0.295; −0.151 vs 0.000 | E13 | fixed vacancies; CES wage rule | — |
| C17 | **At matched elasticity and with a formal/informal margin in both worlds, the competitive rival ALSO produces diploma-income losses (σ=0.5, 1.0)** → the income-based discrimination fails | simulation | Δ diploma income at σ∈{0.5,1,2} | surplus −0.037/−0.019; rival −0.119/−0.124 (σ=0.5), −0.006/+0.016 (σ=1.0), +0.059/+0.094 (σ=2.0) | E13b | σ grid; reps=1; N=2000 | a 4–6 rep replication showing the rival never produces a fall |
| C18 | Actor contributions remain ordered household > employer > state in the abstract model | simulation | years of schooling | +3.34/+1.53/+1.06 of 4.29 (audit) | E14 | knockouts | reversal under plausible screening cost |
| C19 | Long-run simulated trajectories: PH-like default understates early basic completion (0.739 vs target 0.55–0.62) and college transition (0.227 vs ~0.70) | simulation | completion paths | see findings | E19 (pilot) | default params, uncalibrated | calibration that fits both |

## 3. Rivals the results are claimed to have beaten

- **rival 1 — competitive CES skill market, matched.** It wins on C16/C17: with a formal/informal
  margin and σ=0.5–1.0 it reproduces the diploma-income fall, so the absolute-income discriminator
  does not separate the accounts. The formal-employment-probability discriminator may survive
  (surplus −0.15 vs rival ≈ +0.02), and batch B is testing that.
- **rival 2 — Yoo (2003) fixed cutoff / quota.** It wins on C14: the bar sweep is the same object as
  Yoo's effort-near-cutoff result; the new content is the ban/leak accounting, not the sweep.
- **rival 3 — Ghaffarzadegan–Xue–Larson pipeline.** Competes on C18 and the nurse failure.
- **how a rival could win:** shown in each row; the crucial unrun cells are a higher-rep matched
  rival and a support-specification sensitivity for C10.

## 4. Questions to the Council (≤6)

1. **C10 (China school support):** is this a fair test of Trey's Double Reduction hypothesis, or does
   the coded score production function make support and tutoring complements by construction? If the
   result is "free universal exam prep intensifies positional spending", is that a real mechanism
   insight (the race absorbs the subsidy) or an artifact? What is the minimal alternative
   specification that would let substitution appear, and should we run it?
2. **C17:** does the matched-elasticity contradiction kill the paper's Prediction 2, or only the
   *income* discriminator? Is the formal-employment-probability result defensible given E13b's
   reps=1? What exactly may the paper claim after batch B?
3. **C12/C13:** are the liquidity and memory results discoveries or near-mechanical consequences of
   the coded borrowing/learning rules? Which one is safest to headline?
4. **C14:** after conceding Yoo, what is the residual novel claim from the gate experiment?
5. **C19:** the uncalibrated PH model misses its own targets — does this disqualify any four-country
   claim, and what is the minimum calibration a report must disclose?
6. What single claim should the final report lead with, and what should be explicitly *withdrawn*?

## 5. Known limitations and failures

- E13b used reps=1, N=2000 (provisional); batch B re-runs at 4–6 reps, N=3000.
- E19/E20 are pilot only; Hong Kong within E19 was DATA BLOCKED (no HK series loaded). They are not
  country validation.
- E3's `borrow` is a quantity (share of income), not a price; no interest rate is modelled.
- E10's omega is a new extension, not part of the delivered model.
- E18's school support is an extension module worth 0.5 score sd at zero price and is not
  budget-constrained in massabm.
- The model is loosely fitted to the Philippines; Korea is an uncalibrated sketch.
- The whole suite is simulation; none of it is causal evidence about any country.

## 6. Out of scope / do not read

- `01_sources/` (read-only snapshots), `fleet.nosync/` (user's live tree), `00_handoff/papers/`
  beyond orientation.

## 7. Budget

- **deadline:** ~20 minutes.
- **Council output:** reviews + deliberation + synthesis.
- **max words:** synthesis ≤900; per expert ≤400.
