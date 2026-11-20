# PRE-DECLARATION — E2: Philippine K-12 (RA 10533, 2013) cohort-exposure event study (supply push)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared, NOT run. **Authority:** Council brief 013
(`08_council/brief_013/SUCCESS_CRITERIA.md`, STOP_RULES.md), Amendment **A1** (Council directive 68e9dfe6), and
repo-auditor GO. Written before any data contact in this cell. **Simulated vs observed:** this is an *observed-data*
design; every number used as evidence must be an observed cell with `status=target` (or the declared fallback below).

## A1 compliance (binding)
A1 adds to brief 013: reproduction also requires **scaling exponents out of sample** — secondary GER~income
**+0.286 (se 0.045)**, tertiary GER~income **+0.776 (se 0.086)**, lower-secondary completion logit law, with
country-specific timing; a single-curve fit is **PARTIAL at best**. Verdict vocabulary adds **PASS-CONDITIONAL**
(declared channel mixture, weights declared not fitted) vs **IDENTIFIED** (E1, or the predeclared E2+E3 pair only).
**R13** applies: no direction claims from cross-country/panel moments → report **EQUIVALENT**; the forced-ID test
returned **1.00**. This cell therefore reports an event-study *association* under pre-trends, and any push-pull
*direction* claim must come from the E1 interaction (E2+E3 pair), not from the panel.

## Question
Did the 2013 K-12 reform (RA 10533: grades 11–12 added; SHS rollout from SY 2016–17) raise **upper-secondary
completion** and change the **transition to tertiary** for exposed cohorts, relative to unexposed cohorts?

## Design (predeclared)
- **Treatment = cohort exposure**, not school exposure. Cohorts reaching Grade 10 in SY 2016–17 or later faced the
  new 12-year cycle; earlier cohorts did not. Declared birth-year cut: **born ≥ 2000 = exposed (full/partial)**;
  born ≤ 1997 = **unexposed**. Birth years 1998–1999 are **excluded from the main estimate** (partial exposure) and
  shown as a placebo/robustness row.
- **Arms:** exposed vs unexposed cohorts (same country, same outcome definitions). No cross-country arm.
- **Estimand:** (i) upper-secondary completion rate (cohort completion, UIS CR.3); (ii) transition to tertiary;
  (iii) as a learning-independent check, lower-secondary completion (should be unaffected by adding grades 11–12).
- **Pre-trends:** cohort-series pre-trend over the pre-reform observed years; **placebo outcome** = lower-secondary
  completion (no mechanical effect); **placebo cohort** = partially exposed 1998–1999.
- **Confounders acknowledged:** SHS rollout capacity was phased; the 2020–21 COVID disruption overlaps the first
  full exposed cohort; both are declared and enter the interpretation, not the parameterisation.

## Data and fallback (declared)
Primary: `04_data/TARGETS_FLOW.csv` observed `status=target` completion rows (PHL 12 distinct years 1999–2024) and
`04_data/data/gmr_observed_6countries_1970_2024.csv` observed cells. **Coverage is thin**: the pre-reform observed
completion points are ~6–7 and the post-reform ~5–6; with COVID spanning 2020–21. If coverage is insufficient to
support a cohort design, the cell is reported **DATA BLOCKED** rather than reconstructed from imputed/modelled
cells. **No imputation, no modelled series as observations.** RA 10533 timeline from `02_lit`/brief docs.

## Predicted sign and threshold (predeclared)
- Predicted sign: **upper-secondary completion falls then rises** (the definition changes: a JHS holder is no longer
  an upper-secondary completer under the 12-year cycle), with a **net positive** post-reform change once SHS
  cohorts complete; **transition to tertiary falls initially** (two extra years delay entry) and recovers.
- Threshold for **PASS**: pre-trend not rejected (|slope| < 1 pp/yr over pre-period observed points) AND placebo
  outcome null (|effect| < 2 pp) AND the post-reform sign pattern above AND magnitude ≥ **3 pp** net on
  upper-secondary completion. If pre-trend fails → **PARTIAL/descriptive only** (R10). If coverage fails → DATA BLOCKED.

## Fit / check / holdout roles (brief 013 §2 reproduced verbatim)
| Domain | Series (unit) | Role | Countries |
|---|---|---|---|
| Education levels | Primary / lower-sec / upper-sec completion (%, cohort; UIS CR.1/2/3 observed years) | **FIT** | PHL (1980–2010), CHN (1980–2010) |
| Education levels | Same series | **HOLDOUT PERIOD (2011–2024)** | PHL, CHN |
| Education levels | Same series | **HOLDOUT COUNTRY (all years; KHM never fitted)** | KHM (1980–2023 observed) |
| Education levels | Same series | **CHECK only** | KOR (2012 point), HKG (no UIS completion), JPN (no UIS completion) |
| Education flows | GER, out-of-school rate, transition proxies (UIS; TARGETS_FLOW.csv; proxies labelled) | **CHECK (shape only; no fitting)** | all six |
| Attainment | Mean years / attainment distribution (HK EDB 2025; KHM CLFS 2019; WDI modelled = benchmark only) | **CHECK** | HKG, KHM |
| Jobs/markets | Employment shares agri/industry/services (WDI/ILO modelled; ECONOMY_SERIES.csv) | **FIT (cohort-sector link); holdout 2011–2024** | PHL, CHN |
| Jobs/markets | Status employment (wage/vulnerable), GDP pc, urbanisation, remittances | **CHECK / constraints (sign expectations)** | all six |
| Jobs/markets | Formal/informal share (CLFS 2019 KHM only; ILOSTAT blocked) | **CHECK (single cell)** | KHM |
| Sectors | Agri/industry/services shares; formal/informal where measured | **FIT in PHL/CHN; check elsewhere; never extrapolate missing sectors** | PHL, CHN (+KHM informal cell) |
| Universalization timing | Crossing year derived from the FIT/CHECK series; never fitted | **HOLDOUT OUTCOME** | PHL, CHN, KHM; KOR/HKG/JPN as checks |

## Tolerances (brief 013 §3 reproduced verbatim)
In-sample level MAE ≤ 5 pp; out-of-sample level (2011–2024; and held-out KHM) MAE ≤ 8 pp AND strictly better than
**both** naive benchmarks (persistence; linear trend); shape corr ≥ 0.6 in-sample, ≥ 0.5 out-of-sample, sign of net
change correct; midpoint within ±5 years; cohort-flow consistency exact (B1 stock identity, B2 cohort conservation,
B3 all rates in [0,1], no negative stocks) — zero tolerance; sector shares MAE ≤ 5 pp in-sample, ≤ 8 pp out-of-sample,
sign correct; universalization false-positive test; relation-sign constraints R13/R04/R02 reported as failures if
violated. **Verdict vocabulary:** PASS / PARTIAL / FAIL / EQUIVALENT, plus A1's PASS-CONDITIONAL vs IDENTIFIED.
**Stop rules R1–R12 adopted**, including R10 (pre-trend failure → no causal claim) and R12 (no retro-fits).

## What this cell may claim
An event-study association for exposed cohorts under pre-trends. It may **not** claim a push-pull direction from
this panel moment (R13); the direction claim requires the E1/E2+E3 predeclared pair.

## Power calculation (explicit; added per repo-auditor instruction 5, 2026-11-20)
Declared before estimation. With `n_pre` observed pre-reform cohort points and `n_post` post-reform points, and a
completion-series year-to-year residual sd `s` (PHL observed completion series show year-to-year changes of ~2–3 pp;
take `s = 2.5 pp` as the declared upper bound), the standard error of a cohort difference-in-differences estimate is
approximately `SE = s·sqrt(1/n_pre + 1/n_post)`. For the PHL observed coverage (`n_pre ≈ 6`, `n_post ≈ 6`):
`SE ≈ 2.5·sqrt(1/6+1/6) = 1.44 pp`, so the minimum detectable effect at 80% power / 5% two-sided is
`MDE ≈ 2.8·SE ≈ 4.0 pp`. The predeclared 3 pp net threshold is **below the MDE**, i.e. this cell is
**UNDERPOWERED for a 3 pp effect** at the observed coverage; it can only detect ≥4 pp. Consequence declared now:
a point estimate in (0, 3 pp) with a pre-trend-passing specification is reported as **INCONCLUSIVE**, not as
support; a null cannot be claimed either. If CHN (7 distinct years) or pooled coverage is used, `n_pre≈3–4`,
`n_post≈3–4`, `SE≈1.8–2.0 pp`, `MDE≈5–6 pp` — weaker still. The power limitation is part of the declared result and is
not worked around by imputation, by widening the window, or by pooling across countries with different definitions.

## AMENDMENT (repo-auditor Council adjudication D23, applied before running)
**Claim cap (binding).** The output of this cell is a **descriptive association only**, unless BOTH: (i) there are
**≥10 pre-reform observed completion points**, and (ii) pre-trends pass. With the observed coverage on disk (PHL ≈6
pre-reform completion points), condition (i) fails, so even under D23 the maximum claim is a **descriptive
association** — no causal claim, no directional push-pull claim (R13), no "reform raised completion" language. If
the Council later supplies a denser observed pre-period (≥10 points), the cap lifts only for this cell and only if
pre-trends pass; the cell is not re-run silently.
**Power (predeclared, see §Power above).** Declared s=2.5 pp, n_pre≈6, n_post≈6 → SE≈1.44 pp, MDE(80%)≈4.0 pp; the
3 pp threshold is below the MDE, so (0,3 pp) is predeclared INCONCLUSIVE.
**COVID sensitivity (predeclared, before running).** 2020–21 disruption overlaps the first full exposed cohort
(SY2020–21). Declared sensitivity set: (a) exclude 2020–2022 from the post period; (b) include a COVID-period
indicator/interaction; (c) report the headline estimate with and without COVID years. Rule: if the sign of the
estimated effect flips between (a) and (c), the cell is reported **INCONCLUSIVE/COVID-CONFOUNDED** — not support,
not a null. No re-specification may be chosen after seeing which version is "nicer" (R12).

## AMENDMENT — MDE ruling (repo-auditor instruction 3; D23)
**Ruling (binding, predeclared):** the cell PASSES only if the estimated post-reform effect is **≥ the predeclared
MDE ≈ 4.0 pp** (computed above: s=2.5 pp, n_pre≈6, n_post≈6, SE≈1.44 pp, 80% power) **and** pre-trends pass **and**
the placebo outcome is null. An estimate **below the MDE** is reported as **INCONCLUSIVE — not support and not a
null** (it cannot distinguish a true 3–4 pp effect from zero). Claim cap stands: with ~6 pre-reform observed
completion points the maximum claim is a descriptive association; COVID-year sensitivity per the section above must
be reported in the same table, and a sign flip between the COVID-excluded and COVID-included estimates makes the cell
**INCONCLUSIVE/COVID-CONFOUNDED**. No re-specification after seeing results (R12).
