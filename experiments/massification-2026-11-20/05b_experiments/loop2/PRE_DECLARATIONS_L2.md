# PRE-DECLARATIONS — Loop 2: bidirectional education–economy + endogenous shadow sector

Written BEFORE any loop-2 run. **NEW module, clearly named:** `loop2/code/twoway.py` — a compact,
declared two-way cohort-flow model. It is NOT massabm, NOT floorworld, NOT triad, and NOT a
reproduction of any paper result. It exists to test, in one auditable place, the four loop-2 claims
that batch C showed the current suite cannot test: education→economy, economy→education, shadow
education as an industry AND as a positional response, and country variants.

Standing rules: workers ≤ 2 (the module is numpy-only; no multiprocessing), `nice -n 10`,
`PYTHONDONTWRITEBYTECODE=1`, matched seeds 0..4, sd across replications reported separately, failed
runs logged, no imputed data cell cited as observed. Timebox ~40 min compute. Write only
`05b_experiments/loop2/`.

## Model in one page (all equations declared; all parameters listed in code)

Annual cohort flow, 40-year horizon, 15-year burn-in, N=1000 births/year. Schooling pipeline with
declared 4/4-year lags: secondary completes 4 years after entry, college completes 4 years after entry.
Workforce stock by education (basic 8y, diploma 12y, college 16y) with 40-year retirement.

**Education → economy (declared switch `eps_ec`, delay `d_ec`).**
  H_t = mean schooling years of the workforce.
  Complex (college-level) formal vacancies: Vc_t = Vc0 · B0 · (1+g_formal)^t · (H_{t−d_ec}/H_0)^{eps_ec}
  Routine (diploma) formal vacancies: Vr_t = Vr0 · B0 · (1+g_formal)^t
  Complex-job share = Vc/(Vc+Vr); formal-job share = (filled complex + filled routine)/workforce.
  `eps_ec = 0` is the demand-led world (schooling does not create jobs); `eps_ec > 0` is the
  education-led/complementary world. Productivity enters only through H in Vc — no free trend beyond
  the declared `g_formal`.

**Economy → education (declared switch `returns_feedback`).**
  Hiring: complex slots filled by college completers first; routine slots by diploma holders first
  (leftover college may take routine); the rest work informally at wage 1.0.
  Wages: w_c = w_c0·(Vc/C)^{1/σ}, w_r = w_r0·(Vr/D)^{1/σ}, σ = 2 (congestion; clipped).
  Beliefs are adaptive (EMA 0.7) on the previous year's hire probabilities/wages. Households then
  choose: secondary completion = logistic(a_s + b_s·(expected secondary return) + tut_effect·takeup_S);
  college entry = logistic(a_c + b_c·(expected college premium) + tut_effect·takeup_C) × feasible share,
  where `feasible` = P(household income ≥ 4× tuition cost) under a declared lognormal income
  (σ=0.8, median 1). `returns_feedback = 0` freezes the expected returns at their t=0 values (no
  economy→education channel).

**Shadow education as an industry (declared provider entry, prices, capacity) AND as a positional response.**
  Two gates: secondary completion (S) and college entry (C). For each gate:
  demand take-up = logistic(k0 + k1·log(1+return gap) + k2·log(R_gate) − k3·(price/income)), where
  R_gate = applicants ÷ seats is the **positional/competition** term (R_S from births vs declared
  upper-secondary places; R_C from college applicants vs complex-job seats).
  supply: commercial firms n_cm (capacity cap_cm, fixed cost F_cm, entry speed e_cm) and teacher-tutors
  n_tt (lower capacity cap_tt, lower fixed cost F_tt, faster entry e_tt). Providers enter when last
  year's profit > 0, exit when < 0 (declared speeds), subject to bounds.
  price: tatonnement p_t = p_{t−1}·(1 + adj·clip((Qd−Qs)/max(Qs,1), −0.5, 0.5)), bounded.
  effective tutoring = tut_eff × (Qs/max(Qd,ε))^{0.3} (class-size congestion), so the sector can expand
  endogenously but capacity dilutes quality.
  `shadow_mode = 'endogenous'` (entry on) / `'fixed_supply'` (provider counts frozen: supply cannot
  respond — the "industry missing" counterfactual) / `'off'` (tut_eff=0).

## Country variants (declared parameter sets; targets labelled observed vs proxy vs stylized)

| parameter | PH-like | HK-like | KHM-like | source/status |
|---|---|---|---|---|
| upper-secondary completion target | 0.750 (2024) | — (no completion obs.) | 0.279 (2023) | GMR observed panel (04_data) |
| tertiary GER target | 0.530 (2026) | 1.187 (2025) | 0.211 (2025) | GMR observed panel |
| degree/post-sec attainment target | — | 0.276 degree / 0.364 post-sec (2025) | 0.066 university (2019) | national_headline_figures (observed) |
| formal-employment target | — | — (proxy: post-sec 0.364) | 0.117 formal / 0.883 informal (2019) | national_headline_figures (observed) |
| senior-secondary tutoring target | — (none verified) | **0.85 (2010)** and 0.40 (1996) | — (Bray blocked; none verified) | Kwo & Bray 2011 via claim register, authors caveat "not statistically robust" |
| formal sector / informality | stylized high-informality middle | stylized high-formal | stylized very high-informality | declared, not measured |
| tuition cost, tutoring price, provider fixed costs | stylized | stylized | stylized | declared |

No imputed GMR cell is used as a target; only `gmr_observed_6countries_1970_2024.csv` values are cited
as observed. Where no target exists the cell says so and no miss is computed.

## Regimes (per country, 5 matched seeds, 40-year trajectories)

R1 demand_led: eps_ec=0, returns_feedback=1, endogenous schooling, shadow endogenous.
R2 education_led: eps_ec=0.6, d_ec=5, feedback=1, endogenous, shadow endogenous.
R3 complementary: eps_ec=0.3, d_ec=3, feedback=1, endogenous, shadow endogenous. (baseline)
R4 frozen schooling: as R3 but schooling path frozen at baseline (supplied attainment).
R5 frozen returns: as R3 but returns_feedback=0.
R6 fixed supply: as R3 but shadow_mode='fixed_supply'.
R7 no tutoring: as R3 but shadow_mode='off'.
R8 education-led + frozen schooling: as R2 but schooling frozen (needed for the decomposition).

## Predeclared estimands and decision rules

1. **Generated vs supplied formal/complex jobs.** At year 40 (and the 40-year mean):
   - supplied-by-demand jobs = Vc(R1) − Vc(R1 with H frozen at H_0) (the pure demand trend);
   - generated-by-schooling jobs = Vc(R2, endogenous) − Vc(R8, frozen schooling) (what endogenous
     schooling adds when eps_ec>0);
   - report both, plus complex-job share and formal-job share with sd across seeds.
2. **Direction verdict per country.** Ed_dir = Δ complex-job share (education-led vs frozen schooling);
   Ec_dir = Δ degree share (feedback on vs frozen returns). `complementary` if both > 2·sd;
   `education-led` if Ed_dir > Ec_dir and Ed_dir > 2·sd; `demand-led` if Ec_dir > Ed_dir and
   Ec_dir > 2·sd; `neither identified` if both within 2·sd.
3. **Shadow sector.** Report tutoring take-up by gate (S and C), spend per pupil, price, commercial
   vs teacher-tutor provider counts and share, and the return of the sector under fixed supply vs
   endogenous entry. Positional response test: take-up at R_C above vs below its 40-year median
   (within-trajectory) — predeclared direction: take-up higher when R_C higher, |Δ| > 2·sd.
4. **Literature misses.** HK: senior-secondary tutoring 0.85 (2010, caveat). PH: completion 0.750,
   tertiary GER 0.530. KHM: completion 0.279, formal share 0.117, university attainment 0.066.
   Report absolute misses; these are model-vs-target comparisons on observed cells only, not
   calibration (the parameter sets are stylized, not fitted).
5. **Failures.** Any seed with a non-finite value or an invariant failure (shares outside [0,1], negative
   stocks, solver divergence) is logged and excluded, with the count reported.

This is a stylized possibility model: no country-level causal claim, and no imputed cell is used.

---

## Amendments (recorded after the relevant runs; post-hoc where noted, never used to upgrade a verdict)

**Amendment L2-1 — first execution was deterministic (defect, fixed before results recorded).** The
first pass drew no random numbers, so all five "seeds" were identical and seed sd was 0. Declared
stochastic terms were added and the model re-run: a multiplicative formal-demand shock
(lognormal sd 0.06) on Vc/Vr and household decision taste noise (logit sd 0.15). The first-pass output
was deleted; no result is reported from it. A separate `UnboundLocalError` in the frozen-returns arm
(qc_ref binding) was also fixed; 15/135 first-pass trajectories failed on it and are not reported.

**Amendment L2-2 — Council brief 004 binding tests added after the first run.** (i) `R10_frozen_economy`:
vacancies and beliefs frozen at their t=0 values, schooling endogenous (tests whether attainment still
rises without the economy). (ii) freeze-schooling symmetry is reported from R4/R8: the complex-job
VACANCY path under frozen schooling. The previous "generated vs supplied" decomposition is retained.
No threshold changed.

**Amendment L2-3 — one-parameter shadow-demand calibration declared after the first run.** The common
household-demand shift (intercept added to both gate logits) is calibrated by bisection to the single
verified literature target (HK senior-secondary take-up 0.85, Kwo & Bray 2011 with the authors'
caveat). Provider entry costs, capacities and teacher-tutor capacity are held at their declared values;
the uncalibrated run is kept as a sensitivity table (`runs/L2_uncalibrated/`). This is a declared,
single-moment fit, not a claim that the shadow sector is identified.

**Amendment L2-4 — predicted signs for candidate worlds (written before the loop-3 recovery run, which
was NOT run in this timebox).** Candidate worlds and their predicted classifier signs:
- education-led (eps_ec=0.6, d=5): Ed_dir > 0, Ec_dir <= Ed_dir → classify education-led.
- demand-led (eps_ec=0): Ed_dir ~ 0, Ec_dir > 0 → classify demand-led.
- complementary (eps_ec=0.3 + returns feedback): Ed_dir > 0 AND Ec_dir > 0 → classify complementary.
- schedule-only truth (outside the candidate set: no feedbacks at all, `R10`-like): the classifier should
  return `neither identified`; **forced-identification rate** = share of such truths wrongly classified
  as one of the three candidates. The Council's recovery round (truths outside the candidate set,
  candidate-set fit, forced-ID rate) was specified but NOT run in this timebox — recorded as pending.

**Amendment L2-5 — held-out test pending.** The 1980–2010 fit / 2011–2024 held-out test on observed GMR
completion series (PH and KHM have observed series; HK has no completion observation) is specified but
NOT run in this timebox. Recorded as pending; no claim is made from it.
