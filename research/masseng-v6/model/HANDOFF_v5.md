# Handoff: masseng v5, the demand engine. Work stopped 2026-11-22, 01:27 local, at the rate limit.

## Done and working
- **v1–v4 (`PROTOCOL.md`).** Complete and reproducible. v3 is the reported specification and the basis of the
  Bray report (Claude Docs). Results are in `outputs/PHL/v1..v4`, `outputs/KHM/v3` and `outputs/PHL/recovery.json`
  (failed: eta 75%, kappa 65%).
- **`PROTOCOL_v5.md`.** Registered before any v5 fit. It includes the credential-threshold driver, rival R5, the
  Grade 10→11 and Bac II rerouting tests, and the feedback-direction caveat.
- **`masseng/engine5.py`.** The three-value demand engine:
  - `b_h` premium, `b_p` positional share S_L (endogenous), `b_r` relational/threshold driver;
  - `eta` (R0 only), `eta_x`;
  - `kappa * exp(-lam * Z) * ln(1 + burden)`;
  - direct costs scaled by `c_scale`, plus forgone earnings;
  - household spending outputs (FIES-style shares, household share of total spending);
  - deferred tertiary pool (`h_def`, until age 25);
  - Grade 10→11 transition rate;
  - optional rationing of public upper-secondary places;
  - specs R0–R5.
- **`masseng/calibrate5.py`.** Fitting with fixed parameters from `config.v5.fixed_params`, a `target_map` for
  `targets_v5.json`, and scoring against benchmarks. `Model5.set_params` makes refits fast: about 0.25 s per run.
- **`tests/test_engine5.py`.** 8 invariants pass, including conservation for all specs. `tests/test_model.py`
  still passes, so v1–v4 are unchanged.
- **`config.json` `v5` blocks for PHL and KHM.** Cost schedules and v5 policy events. KHM costs are anchored to
  CSES 2019/20 spending per pupil.
- **Data agents' outputs** in `countries/*/sources/`: household costs, returns, government and flows, Cambodia
  demand and costs.

## Partial (agents stopped mid-task)
- **`countries/PHL/drivers_v5.json`, `countries/PHL/targets_v5.json`, `countries/KHM/drivers_v5.json`.** Written
  incrementally and possibly incomplete. Check the `verified` flags.
- **Not started:** the fit, score, inversion and figure scripts for v5, and any v5 fit.

## Next steps, in order
1. Inspect the drivers and targets files. Fill gaps: the premium series, `occ_credential_share`, FIES rows.
2. Add `v5.target_map` in each config, mapping `targets_v5.json` series to model indicators:
   - FIES national, bottom 30% and upper 70% for 2003 and 2006 → train;
   - FIES 2012 and 2023 → test;
   - NTA household share → `hh_share_total_spending`, test;
   - CHED totals → `enrol_tertiary` with transform `index_2016`, test;
   - DepEd Grade 10→11 → `trans_lsec_usec` 2018, test.
3. Add the latent / effective / realised outputs: per level × decile × sector × year, record qualified, demand at
   zero cost (latent), demand at actual cost (effective), and realised entrants. Then the decomposition of
   enrolment change into qualified / wanting / cost / places.
4. Write `scripts/fit_rivals5.py`, `score_rivals5.py`, `invert_demand5.py` and `make_figures5.py`, as specified in
   the stopped agent's brief (see the transcript).
5. Fit R0–R5 two at a time (2 cores), score, run the recovery test on the preferred rival, run the Cambodia port.

---
# Addendum 2026-11-22 10:26: Hong Kong port, plan for Kimi

## Data in hand
`countries/HKG/`: `wdi_series.json`, `facts.json`, `facts.md`, `population_by_age.json` (partial).

**Key facts:**
- **Funded first-year degree places:** 14,500/yr (1994/95 to about 2007), 15,000 from 2012/13, and 30,000 in the 2012
  double cohort.
- **The 60% post-secondary target** (2000 Policy Address) was met by about 2005/06, mostly through self-financed places.
- **HKDSE 3322 (day school):** 37.7% (2012), about 42–45% since.
- **Graduate earnings, bachelor's vs upper secondary at ages 20–24:** ratio 1.60 (1994) to 1.33 (2019).
- **Tutoring:**
  - Bray & Kwok 1998/99: S1–3 35%, S4–5 47%, S6–7 70%.
  - Bray et al. 2011/12: S3 53.8%, S6 71.8%.
  - Caritas 2010: senior secondary 85.5% (NGO survey, unverified; the source of the paper's "85%").
- **Students going abroad** (EDB S6 Pathway Survey): 14.5% of S6 leavers in 2020, 6.5% in 2025. Outside-HK share of
  bachelor's places: 15% (2012), 26% (2020), 13% (2025). Mainland share of outbound students: 22% to 47%.
  **The "half go abroad" claim is not supported.**

**Gaps:**
- population by single age (net migration; CBR inflated in 2001–12 by mainland births);
- household spending before 2019/20;
- tutoring after 2012;
- the HKCEE, JUPAS and 33222 series;
- WDI has no Gini or under-five mortality for HKG.

## Engine changes needed (build in `engine5.py`, the array engine; merge the rules with the v6 kernel later)
1. **Time-varying cycle structure.**
   - Old system: 6 + F1–5 + F6–7 + 3-year degree. New Senior Secondary (NSS): 6 + 3 + 3 + 4 (first S4 intake 2009,
     first HKDSE 2012).
   - Generalise the fixed 6 secondary + 4 tertiary grades into per-year stage lengths.
   - Reproduce the 2012 double cohort.
2. **Tertiary destinations as a joint choice with fractional rationing:**
   - funded local (quota as above, allocated by exam rank or proportionally — state the rule);
   - self-financed local degree or sub-degree (fee);
   - abroad or mainland (high cost, no quota);
   - none.
   - Target: the EDB pathway shares.
3. **Gates:** SSPA banding at P6, HKCEE at F5, HKALE at F7, then HKDSE at S6 and JUPAS. Use pass rates as inputs where
   known.
4. **Tutoring module.**
   - At each gate, tutoring take-up = f(competition: candidates per funded place; income decile).
   - Tutoring adds household cost, and changes rank within the cohort, not the number of places (zero-sum).
   - Targets: the prevalence by grade above.
   - This tests H3 (gate clustering).
5. **Government demand:**
   - free and compulsory schooling: 6 years (1971), 9 (1978), 12-year free (2008);
   - the 60% target, met through self-financed places (state-encouraged private supply);
   - the funded quota as the state's purchase.

**Expected contrast with the other two countries.** Realised enrolment is limited by places in Hong Kong, by cost in
the Philippines, and by cost plus the exam in Cambodia.

## Also pending from v6-branch review (fix before integration)
1. The admissions kernel allocates whole persons; the cohort model needs fractional seats.
2. Priority is decided by alphabetical applicant ID; replace with an explicit rule.
3. The Q ≥ L ≥ E funnel rejects cash transfers worth more than costs (4Ps); allow net-negative cost.
4. "Accessible empty seat" really means a seat someone ranked.
5. Dictionary-based state is slow; use array form.
6. The README cites a v5 overprediction that is not in the branch.
