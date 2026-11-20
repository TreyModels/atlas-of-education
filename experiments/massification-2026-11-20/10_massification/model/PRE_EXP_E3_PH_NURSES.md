# PRE-DECLARATION — E3: Philippine nurse visa-expansion demand-pull replication (Abarcar & Theoharides)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared, NOT run. **Authority:** Council brief 013
(`SUCCESS_CRITERIA.md`, `STOP_RULES.md`), Amendment **A1** (Council directive 68e9dfe6), repo-auditor GO.
**Simulated vs observed:** the design is an *observed-data replication*; if the required series are not on disk the
cell is **DATA BLOCKED** and any model-side elasticity is reported as **simulated**, never as a replication.

## A1 compliance (binding)
Scaling exponents out of sample are required (secondary GER~income +0.286 se 0.045; tertiary +0.776 se 0.086;
lower-secondary completion logit law; country-specific timing); single-curve fit = PARTIAL at best. **PASS-CONDITIONAL**
(declared mixture, weights declared not fitted) vs **IDENTIFIED** (E1 or the predeclared E2+E3 pair). **R13**: no
direction claims from cross-country/panel moments → EQUIVALENT; forced-ID test 1.00. Therefore E3 alone may not
establish demand-led direction; it is one half of the predeclared E2+E3 pair, and its claim is limited to
reproducing the published design's sign and order of magnitude.

## Question
Did the US nurse visa expansion raise expected returns to the nursing credential in the Philippines, producing an
origin-country training response (licensure and nursing-program enrollment), as in Abarcar & Theoharides (2024)?

## Design (predeclared, literature-anchored)
- **Shock:** US nurse visa expansion (the 2005–06 retrogression/expansion episode used by the published design);
  exposure timing from the published paper.
- **Arms:** treated = nursing programs/cohorts exposed to the visa expansion; control = non-nursing programs (and
  pre-expansion years). Difference-in-differences with the published design's comparison structure.
- **Estimand:** (i) origin licensed nurses per additional nurse migrant (published ≈ **9:1**); (ii) growth in
  licensed nurses per 100k; (iii) nursing licensure pass rate (published ≈ 38.4%); (iv) nursing-program enrollment
  response relative to non-nursing controls.
- **Threshold (brief 013 E3):** reproduce the published **sign** and **order of magnitude** of the ~9-nurses-per-
  migrant ratio (within a factor of ~2, declared), or report the model-vs-data gap explicitly. Pre-trends must pass
  (R10); placebo outcomes (non-nursing programs) must be clean.

## Data and fallback (declared)
Required: PRC nursing licensure counts/pass rates and CHED nursing-program enrollment (treated + non-nursing
controls). **These are not confirmed on disk.** On-disk candidates checked and declared: `04_data/TARGETS_FLOW.csv`
has `transition_to_tertiary` and `wage_premium_tertiary` (observed targets) but **no nursing-specific series**;
`ECONOMY_SERIES.csv` has OFW/labour-migration deployment and remittances but **no licensure or program enrollment**.
If PRC/CHED series are absent, the cell is **DATA BLOCKED**; the predeclared model-side computation may still be
reported as *simulated*: the demand-pull channel's predicted elasticity of origin training to a foreign-demand
shock, compared with the literature's 9:1 sign and magnitude — labelled **model output, not a replication**.
No imputation; no modelled series as observations.

## Predicted sign and threshold (predeclared)
- Predicted sign: **positive** origin training response to the visa shock; **positive** and roughly **9:1** order of
  magnitude for licensed nurses per additional migrant; non-nursing controls flat.
- PASS if: pre-trends pass AND sign positive AND estimate within factor ~2 of 9:1 (or literature's own CI), AND
  placebo controls null. PARTIAL if sign correct but magnitude outside factor 2 (report the gap). FAIL if sign
  reverses or pre-trends fail. DATA BLOCKED if the series are absent.

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
In-sample level MAE ≤ 5 pp; out-of-sample level (2011–2024; held-out KHM) MAE ≤ 8 pp AND strictly better than both
naive benchmarks (persistence; linear trend); shape corr ≥ 0.6 in-sample, ≥ 0.5 out-of-sample, sign of net change
correct; midpoint within ±5 years; cohort-flow consistency exact (B1–B3, zero tolerance); sector shares MAE ≤ 5 pp
in-sample, ≤ 8 pp out-of-sample, sign correct; universalization false-positive test; relation-sign constraints
R13/R04/R02 reported as failures if violated. **Verdict vocabulary:** PASS / PARTIAL / FAIL / EQUIVALENT, plus A1
PASS-CONDITIONAL vs IDENTIFIED. **Stop rules R1–R12 adopted** (R10 pre-trend; R11 rival matching; R12 no retro-fits).

## Literature anchors (registered, not parameters)
`10_massification/lit/PUSH_PULL_TARGETS.csv` (ACKed b8d0a277): 9 nurses per migrant; +126% licensed nurses per
100k; pass rate 38.4%; place premium 3.99; return 8.8%/yr. These are declared benchmarks/thresholds, **never fitted
values**. The two NOT-FOUND entries (lead-lag Granger direction; elasticity of formal employment to educated labour
supply) remain **data gaps** and are not filled by this cell.
