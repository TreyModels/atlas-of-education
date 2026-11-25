# Response to external review (ChatGPT) — 25 Nov 2026

**Scope:** the “ALL ATLAS WORK” archive (`research/atlas-all-work-2026-11-25` @ `46950ab`) and the
reproduction-checked deposit (`research/shadow-education-contest-2026-11-25` @ `1c3417c`).
**Verdict accepted: MAJOR REVISION.** The review's critical findings were checked against the code and both
result files and are **confirmed**. Nothing below is a rebuttal; this is the triage and the fix plan.

## 1. Two result generations disagree — CONFIRMED

| | 420-run record (`verified_results…`, Paper B) | 540-run record (`hk_korea_comparative_with_cf4.json`) |
|---|---|---|
| design | **N = 400, T = 70** (420-era runner) | **N = 300, T = 46** (540 runner) |
| other params | y_median 3.0, subsist .15, borrow .5, contest_alpha 1.2/1.25, price .12/.11, max_e 4.0/4.5, elite_logw .85/1.15, bar gates 0/0/0 | y_median 2.2/2.0, subsist .35, borrow .25, alpha .25, price .16, max_e 6.0, elite_logw .50/.60, bar gates 2/4/10 |
| HK baseline elite Q5 | 30.0% | 46.36% |
| KR baseline elite Q5 | 24.6% | 36.12% |
| HK tax spend | 104.8 | 107.42 |
| KR tax spend | 107.4 | 106.46 |
| HK cap spend | 82.1 | 67.39 |
| KR cap spend | 74.1 | 76.42 |
| HK large-seat spend | 173.8 | 149.30 |
| KR large-seat spend | 122.3 | 128.00 |

The Paper B docx tables match the **420-run** generation; the reproduced run is the **540-run** generation.
The 420-era runner also uses the old `Engine(cfg, modules=…)`/`e.history` API and is **not runnable** against
the committed engine — so the 420 numbers are author-reported from a different model generation, not reproduced
here. **Fix:** freeze one canonical configuration; if the 540 spec is adopted, regenerate every paper table from
it; if the 420 spec is the intended model, port it to the current engine and rerun.

## 2. The combined-policy conclusion fails its own test — CONFIRMED

Using the 540 run (already recorded in `code/REPRODUCTION_CF4_2026-11-25.md`):

| arm | HK spend / elite Q5 | KR spend / elite Q5 | both-jurisdiction Win-Win? |
|---|---|---|---|
| Baseline | 100 / 46.36% | 100 / 36.12% | — |
| **CF1b cap −50%** | **67.39 / 41.96%** | **76.42 / 26.39%** | **YES (only arm)** |
| CF4a wage −50% + cap | 43.78 / **48.64% ↑** | 46.50 / 34.10% | NO |
| CF4b wage −50% + seats | **90.88 ↑** | **88.04 ↑** | NO |

The pre-stated Exp-7 falsifier is **not met**. The single-lever effort cap satisfies the stated criterion; every
wage-compression arm lowers spend but raises elite Q5 share. **Fix:** make this the central policy comparison;
stop claiming that only combinations reach the win-win zone. Also state explicitly which equity dimension
(elite Q5 share vs Q5−Q1 tutoring gap) the welfare criterion uses.

## 3. Model implementation — CONFIRMED

**A. Korea Grade-9 contest has no lasting prize (critical).** `core.py` sets `k['elite']` only for
`m_ == self.nlev - 2` (the G12 gate). The KR G9 gate is `kind=contest, share=0.35, fail='track', elite_logw=0.15,
set_voc=False`; winners and losers both continue, and `set_voc=False` prevents a track change. `contest_prep` still
prices the G9 contest from `elite_logw`, so households spend on a phantom prize. **Fix:** add an explicit G9
placement variable with lasting consequences (school quality, G12 eligibility, or wage), or remove the G9 contest
until implemented.

**B. Expected vs realized probabilities differ.** `contest_prep` uses `P = 1 − exp(−λ x^r)`; the realized gate
uses Gumbel-max Plackett–Luce ranking over `x_eff`. λ is calibrated to match aggregate seats, not individual
incentive gradients. **Fix:** use a consistent expected-probability calculation, or report the approximation and
a sensitivity test.

**C. Seat-share denominator.** `seats = max(round(share·N), 1)`; the share is of the entering cohort, not of
applicants. **Fix:** report applicants, seats, applicant:seat ratio, and realized admission rate per arm.

## 4. Calibration of the 540 design — CONFIRMED

The 540 baseline no longer recovers the Korean benchmarks the paper claims: Q5−Q1 participation gap **68.36 pp**
vs target 32.1; Q5/Q1 spend ratio **18.01×** vs target 3.4×; K–12 participation field differs from the 76.5%
benchmark. **Fix:** recalibrate with a declared procedure, keep a holdout of empirical moments, and rerun all
policy arms.

## 5. GPU scripts — CONFIRMED

- `gpu_bray_abc_and_contest_surface.py`: `theta[:,5]` (`teacher_threshold`) never enters the utilities or the
  moments; only five targets are used. A 7-parameter ABC cannot identify the teacher-threshold parameter.
  **Do not report it as a 7-parameter calibration.**
- The 2,000-point contest surface uses a simplified fixed-point best response; label it an approximate
  sensitivity exercise, distinct from the engine's realized contest.
- `gpu_e1_q3_wild_cluster_ri.py` panel mode builds `X = [1, x]` only, dropping controls/fixed effects; it is not
  a reconstruction of the E1/Q3 estimators. Label it accordingly or reconstruct the estimators.

## 6. Paper B medical-seat episode — ACCEPTED

Present the 2024 Korean medical-seat expansion as a motivating case with its own empirical limitations
(proposed 2,000, finalized ~1,500; 2024 spend KRW 29.2tn, 2025 ~27.5tn), and keep the seat-expansion paradox as a
**conditional simulation prediction**, not an established causal effect.

## 7. Reproducibility — PARTIAL

Positive: the 540-run reproduction matches the supplied reference output to floating-point precision and records
the failed combined-policy hypothesis. Remaining gaps: the 420 run is author-reported and its runner targets an
older engine API; Paper A's Exp 1/3/4/5 code and primary outputs are not in the reproduction record; the
all-in-one archive's `engine/` dir contains only `core.py`/`tutoring.py` (the full engine is in the reproduction
branch).

## 8. Remediation sequence (accepted, in order)

1. **Freeze the canonical model** — commit, params, data, env, seeds; preserve the 420 design as an earlier spec.
2. **Fix the contest architecture** — G9 consequence, expected/realized probabilities, seat reporting.
3. **Recalibrate** — recover Korean participation, gap and spend-ratio benchmarks; holdout moments.
4. **Rerun all policy arms** (incl. CF4a/CF4b) — report effort, expenditure, elite access, quintile outcomes, seed uncertainty; retain the failed CF4 result.
5. **Repair the GPU estimators** — connect every parameter to moments; reconstruct E1/Q3 estimators.
6. **Complete Paper A's replication package** — WDI inputs, scripts, raw outputs, Jacobian code, pre-declared rules.
7. **Rewrite Paper B's results/conclusion** — reproduced spec authoritative; separate conditional predictions from causal claims.
8. **Final manuscript audit** — regenerate all tables/charts from the canonical result files.

**Status:** triage recorded; none of the model fixes is implemented yet. The canonical-spec choice (restore the
420 design vs adopt the 540 design) and the G9-prize design are the two decisions that gate the rest.
