# Claims ledger (24 Nov 2026)

Status key: **HOLDS** (recomputed or verified in this record or an earlier verified record), **NARROWED** (true but weaker than
stated), **DEAD** (killed by a later test), **ARTEFACT** (produced by data availability or design), **UNVERIFIED** (reported by a
paper or reviewer; not recomputed in this session). "Source" names the branch/file where the number lives.

## A. Results that hold

| # | Claim | Number | Status | Source |
|---|---|---|---|---|
| A1 | Schooling take-off precedes agricultural labour release | 31 forward, 3 reverse of 34 identifiable; 30 undetermined; both-exact median lead 18 y (n=18, IQR 8.0-30.8) | HOLDS (recomputed in fix/sequencing) | `fix/sequencing-censoring-2026-11-24`, `results/sequencing_stats.json` |
| A1b | **Threshold sensitivity of A1 (new, `research/records/2026-11-24-next-tests/`)**: the paper's default reproduces exactly (64/64 dates, 31/3/30, median lead 18, n=18), but the forward share of identifiable countries is 95.8-97.0% at +0.5 y of schooling per decade, 83.9-91.2% at +1.0 (default), 65.4-70.4% at +1.5 (7-10 reverse cases) | NARROWED: report a range, not 91% | `q1_sweep.csv` |
| A2 | Robustness of A1 to a +15 y schooling-date error | 26 of 34 still forward | HOLDS | same |
| A3 | Schooling vs fertility ordering | strict schooling-first 24/64 = 37.5% (CI 26.6-50.0), 20 ties, 20 fertility-first | HOLDS (Council recomputation) | `research/records/2026-11-25-council-novelty/DECISION.md` |
| A4 | Schooling-fertility link is a level gradient | 71-99% negative-significant in levels vs 0-7% in ten-year changes over 13,800 partitions | UNVERIFIED here (23 Nov battery record) | `corr-battery-2026-11-23` |
| A5 | Future-schooling placebo | 52.9% vs 58.8% of cells (~90%) | HOLDS (battery README) | `corr-battery-2026-11-23` |
| A6 | Orthogonalised placebo (new) | with S(t) and S(t+10) together and country FE, future vs current coefficient: lower-secondary completion -0.96 vs -0.80, secondary enrolment -0.91 vs -1.04, tertiary enrolment -1.16 vs -0.17; primary completion is the exception (-0.52 vs -1.09) | HOLDS as a regression, exploratory (22 Nov panel, 5-year country-years). **Interpretation open:** consistent with a common trend, with anticipation/quantity-quality (fertility choices respond to expected schooling of the next generation), or with a schooling effect; the lead-lag design cannot separate them | `results/placebo_orthogonal.txt` |
| A7 | Schooling timing tracks transition onset | +0.164 (0.047), n=90; midpoint +0.270 (0.072) | HOLDS | `fix/n4-shape-2026-11-24` |
| A8 | Income at onset is unrelated to timing (new) | -0.318 (0.583), n=68, R2 0.01; schooling stays +0.278 (0.061) with GDP control (n=63) | HOLDS, post hoc | `results/n4_gdp_mortality.txt` |
| A9 | Starting child mortality (new) | explains 29% of onset and 53% of midpoint variance (n=66); the date mortality fell is unrelated (+0.083 (0.132)) | HOLDS as a regression; interpretation (level proxy for initial development) untested; schooling coefficient falls from 0.164 to 0.115 (0.047) with it, on a smaller sample (n=60) | same |
| A10 | Few links travel | 5 of 272 robust everywhere; 161 no better than random | UNVERIFIED here (grouping-multiverse-400; methods paper) | `research/methods-multiverse-paper-2026-11-23` |
| A11 | Farm decline does not predict fertility change | -0.0003 (0.0058); MDE 0.016 births (n=503); earlier version +/-0.004 | UNVERIFIED here (reported in the 23 Nov subsistence-v2 record) | `subsistence-v2-2026-11-23` |
| A12 | Input prices move farm labour | fertiliser price -> farm exit +0.445, wage jobs -0.243, births -0.006; OLS elasticities 1.24/1.11 (Gemini reports 1.24-1.40 elsewhere) | UNVERIFIED here; association only | `integrate`/22 Nov `04_input_prices_move_labour.md`, `subsistence-v1/v2` |
| A13 | Supply block beats demand block in ten-year changes | +0.456 (0.174) vs +0.006 (0.203), n=78, 51 countries | UNVERIFIED here (supply-demand record) | `research/supply-demand-2026-11-23` |
| A14 | Fee abolition raises primary GER | +21.7 to +28.6 points over t+1..t+5, flat pre-trend, placebo(-6 yrs) flat | HOLDS as computed; **dates only partly verified; TWFE with staggered timing** (see C3) | `research/records/2026-11-22-massification-panel/results/final/findings.txt` |
| A15 | Poor countries below replacement | 8 of 119 crossers: ARM 1994, CHN 1991, NPL 2019, VNM 1998, GEO 1992, IND 2020, ALB 2002, BTN 2012 | HOLDS (119 crossed, 75 never; earlier "111" superseded) | `research/records/2026-11-22-session/results/replication_and_crossers.txt` |
| A16 | Philippine demand models lose to persistence | best 7.458 vs persistence 6.600, trend 11.794; b_h at bound | HOLDS (manuscript) | `research/masseng-v6/manuscripts/Philippine_demand_rivals.md` |

## B. Results that are dead, narrowed or artefacts

| # | Claim | What happened | Status |
|---|---|---|---|
| B1 | Electricity -> lower secondary (+16.05) | single specification; +0.05 +/- 0.19 with country trends; 11 of 32 links flip sign more than random | DEAD |
| B2 | Paid employment -> tertiary (+1.43) | median 0 over 1,536 specifications, positive-significant in 27.9%; null across all groupings | DEAD |
| B3 | Early marriage slows lower secondary (-0.116) | change-on-change reverses (+0.020 -> -0.027); circular shift p = 0.08 | DEAD |
| B4 | Care-work loop, credential inflation | absorbed by GDP/urbanisation (+0.009, t=0.17); credential gap correlates -0.15 vs -0.62 for attainment | DEAD / NARROWED |
| B5 | Tipping points, scaling | wrong-sign autocorrelation (-0.025); variance fails 16,000 surrogates (p=0.42) | DEAD |
| B6 | **"Labour-market demand precedes schooling in only 7% of 58 countries"** | the narrow demand series (paid-employment share, agricultural employment share) start in 1991 for every country; 92% of the 108 schooling take-offs are dated by 1990; only 7 of 108 countries have a schooling take-off dated more than 5 years after the first paid-employment observation (so demand could precede it by a meaningful margin) | **ARTEFACT** (this record) |
| B7 | Child-labour/electricity -0.417 (P>0=0.02) as "independent confirmation" | one Bayesian association, sparse survey years, electricity itself fragile; (c) variant invalid | NARROWED |
| B8 | "Robust everywhere" certifies a homogeneous effect | known-truth simulation: a link planted in one third of countries is labelled robust ~85% of the time | **NARROWED** (new); see `results/known_truth_sim_summary.md` |
| B9 | "Schooling follows fertility by 18 years" (6-year schooling, 190 countries) vs N1's schooling-first | different measures, but unreconciled | UNVERIFIED tension; E10 |

## C. Corrections to external reviews (Gemini) found this session

1. Gemini called the 34 sequencing countries "non-censored". They are *identifiable*; only 18 have both dates exact.
2. Gemini (and our own drafts) treated "7%" and "28%" as a pair to reconcile. They are different quantities (28% = supply onset
   precedes schooling, raw and contaminated by data start; 7% = narrow demand precedes schooling), and the 7% is itself an artefact (B6).
3. Fee-abolition dates in `scripts/final_tests.py` are secondary-source and partly conflicting (web check, 24 Nov): Malawi 1994
   (some sources 1995 school year), Uganda 1997 (consistent), Kenya 2003 (consistent), Lesotho 2000 (consistent), Cameroon 2000
   (a World Bank note says 1999), Ghana 2005 (consistent with FCUBE 2005; one dataset lists 1997), Ethiopia 1995 (one dataset
   says 1994), Tanzania 2001 (one dataset says 2003), Rwanda 2003, Burundi 2005, Zambia 2002 (consistent with the 2000-2003
   cluster), Mozambique 2004 (one dataset lists 2005). **No primary-source verification was possible here.** The estimator is
   two-way fixed effects with staggered adoption, which is biased under heterogeneous effects; use a heterogeneity-robust
   estimator (E8).
4. "Pre-registered nulls": only the fertility audit has a preregistration file; the Philippine v5 protocol precedes its fits but
   is not blind; most nulls are exploratory.
5. Gemini's cited paths for +0.05 +/- 0.19 (`2026-11-23-dashboard/README.md`), 60%/75% sign-flip shares (methods paper) and
   CR.3 67.5% -> 75.0% (`experiments/massification-2026-11-20/04_data/CLAIM_VERIFICATION.md`) were **not opened** in this session.
6. Gemini's unverified figures, not recomputed here: 38.4M regressions, exponential-to-floor 49% BIC / RMSE 0.31 vs logistic 7% / 0.48,
   pronatalist +0.035 (0.025) over 38 policies with max TFR 1.83, mortality-leads-fertility 12 years (IQR 3-19), mortality level +0.0067 vs volatility +0.0020.
