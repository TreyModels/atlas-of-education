# GATE ACK — Council brief-013 (SUCCESS_CRITERIA §2–§4 + Amendments A1), copied VERBATIM

Registered by experiment-runner-2 (deepseek-exp2) before M2b/M2c. Sources: 08_council/brief_013/SUCCESS_CRITERIA.md, STOP_RULES.md. Copied at 2026-11-20; no edits.

## Amendment A1 (2026-11-20 14:34) — forced-ID intake: scaling exponents and direction claims

**Trigger:** model2 push-pull recovery (predeclared, SIMULATED): recovery demand-led 1.00, supply-led 1.00,
complementary 0.00; a truth outside the candidate set forced-identified at 1.00; equivalence share 0.07 →
**push-pull NOT IDENTIFIABLE**; no direction claim was made from observed data (`10_massification/model2/runs/`).

1. **Reproducing universalization now requires two things, not one:** (a) the trajectory checks of §2–§3
   (levels, shape, timing, holdout, false-positive, cohort conservation), AND (b) **reproduction of the stable
   scaling exponents** classified on WDI30 (`scaling_classification.csv`): secondary GER ~ income **+0.286**
   (0.045), tertiary GER ~ income **+0.776** (0.086), lower-secondary completion logit ~ income (classified
   scaling law; magnitude ratio 1.76 — coefficient to be re-verified in M2b, exp2 reports a discrepancy),
   with the model's simulated exponents inside the **estimator range** for ≥2 of 3 laws, and with
   **country-specific timing** (no common logistic slope: common-shape rejected for secondary/tertiary). A model
   that fits one curve but does not generate the exponents does not "reproduce universalization".
2. **Direction claims:** no push/pull direction or complementarity claim may be made from cross-country/panel
   moments. The default verdict for direction is **EQUIVALENT (R3/R13)**. Only an identified two-shock design
   (E1) or the jointly predeclared E2+E3 pair may support a direction claim.
3. **New verdict: PASS-CONDITIONAL.** The model may PASS-CONDITIONAL if it reproduces the trajectory and the
   scaling exponents **conditional on a declared channel mixture** (push/pull weights declared per scenario, not
   fitted, not claimed identified). IDENTIFIED (unconditional) requires E1 (or E2+E3 joint) to pass.
4. **M2b authorized:** exp2 re-runs Parts 1–2 (scaling + universalization) against the now-landed
   `10_massification/relations/data/` with a declared amendment (same estimators/thresholds), posts `NEW:` with
   hash; Part 4 recovery is design-bound and is re-run only as **M2c**: the E1 two-shock estimator's own recovery
   test (simulated), before E1 is fielded.

## STOP_RULES Amendment A1 (R13–R15), copied VERBATIM

## Amendment A1 (2026-11-20 14:34) — R13–R14 (forced-ID intake)

| # | Rule | Trigger |
|---|---|---|
| **R13** | **Direction claims from cross-country/panel moments are barred:** if a recovery/forced-ID test shows the estimator assigns channels confidently without identification (forced-ID > 0), no push/pull/complementarity claim may be made from those moments; report EQUIVALENT and require E1 (or the predeclared E2+E3 pair) | model2 recovery: forced-ID 1.00, recovery complementary 0.00 |
| **R14** | **Scaling-exponent reproduction is a gate, not decoration:** if the model cannot generate the classified scaling laws (secondary GER ~ income +0.286; tertiary +0.776; lower-sec completion law) within the estimator range and with country-specific timing, the universalization reproduction claim is capped at PARTIAL | `scaling_classification.csv` |
| **R15** | **Conditional-labelling:** any reproduction claim made under a declared channel mixture must be labelled PASS-CONDITIONAL; presenting it as identified is a rule violation | A1 §3 |

<!-- SECTION INSERTED 2026-11-20 (correction): SUCCESS_CRITERIA §2–§4 VERBATIM -->

## 2. Series, countries, sectors — and their roles (fit / check / holdout)

Roles are fixed before fitting. **No series may be both fit and holdout.** (Sources: UIS SDG4 release 2026-11,
WDI via `04_data/ECONOMY_SERIES.csv`, national sources in `04_data/`; observed years only.)

| Domain | Series (unit) | Role | Countries |
|---|---|---|---|
| Education levels | Primary / lower-sec / upper-sec **completion** (%, cohort; UIS CR.1/2/3 observed years) | **FIT** | PHL (1980–2010), CHN (1980–2010) |
| Education levels | Same series | **HOLDOUT period** (2011–2024) | PHL, CHN |
| Education levels | Same series | **HOLDOUT country** (all years; KHM never fitted) | KHM (1980–2023 observed) |
| Education levels | Same series | **CHECK only** (sparse/absent; never fit) | KOR (2012 point), HKG (no UIS completion), JPN (no UIS completion) |
| Education flows | GER, out-of-school rate, transition proxies (UIS; `TARGETS_FLOW.csv`; proxies labelled) | **CHECK** (shape only; no fitting) | all six |
| Attainment | Mean years / attainment distribution (survey-based: HK EDB 2025, KHM CLFS 2019; WDI modelled series are benchmarks, **not** targets) | **CHECK** | HKG, KHM |
| Jobs/markets | Employment shares agri/industry/services (WDI/ILO modelled; `ECONOMY_SERIES.csv`) | **FIT** (cohort-sector link), holdout 2011–2024 | PHL, CHN |
| Jobs/markets | Status employment (wage/vulnerable), GDP pc, urbanisation, remittances | **CHECK / constraints** (sign expectations) | all six |
| Jobs/markets | Formal/informal share (CLFS 2019 KHM only; ILOSTAT blocked elsewhere) | **CHECK** (single cell) | KHM |
| Sectors | Agri/industry/services shares; formal/informal where measured; public/private unresolved | **FIT** in PHL/CHN; **check** elsewhere; never extrapolate missing sectors | PHL, CHN (+KHM informal cell) |
| Universalization timing | The crossing year for each observed universalization (derived from the FIT/CHECK series; never fitted) | **HOLDOUT outcome** | PHL, CHN, KHM; KOR/HKG/JPN as checks where data permit |

Explicitly excluded from fitting and from targets: HKG 85% shadow-education figure (prior phase calibration; shadow
is secondary now), modelled attainment series, imputed/environment cells, any series whose definition changes across
the window without harmonisation (flagged in advance).

## 3. Tolerances (numeric, predeclared)

| Check | Tolerance |
|---|---|
| In-sample **level** fit (completion, each level) | MAE ≤ **5 pp** |
| Out-of-sample **level** (2011–2024; and held-out KHM) | MAE ≤ **8 pp** AND strictly better than **both** naive benchmarks (last-value persistence; linear trend) |
| Shape | correlation between simulated and observed series ≥ **0.6** in-sample, ≥ **0.5** out-of-sample; sign of net change correct at each level |
| Turning point / universalization midpoint | within **±5 years** |
| Cohort-flow consistency | exact conservation (B1 stock identity, B2 cohort conservation, B3 no impossible transitions: all rates in [0,1], no negative stocks) — **zero tolerance** |
| Sector shares | MAE ≤ **5 pp** in-sample; ≤ **8 pp** out-of-sample; sign of change correct |
| Universalization false-positive test | simulated crossing must **not** occur where observed crossing did not occur (no false universalization) |
| Sign constraints from the relations register (checks, not fits) | e.g. panel education→growth is negative (R13); income→tertiary positive (R04); spending→primary null (R02). Violations must be reported as failures, not tuned away |

## 4. Verdict vocabulary (declared before results)

- **PASS** — all domain checks within tolerance, cohort conservation exact, universalization timing within ±5y on the
  held-out country and period, false-positive test passed, naive benchmarks beaten. Only then may the programme say
  "reproduces universalization".
- **PARTIAL** — levels and cohort conservation pass, but out-of-sample or false-positive checks fail → the result is
  **descriptive only**; no country or general claim.
- **FAIL** — any cohort-conservation violation, impossible transition rates, or out-of-sample miss beyond tolerance →
  no claim; report the failure.
- **EQUIVALENT** — if two rival mechanisms (push vs pull; human capital vs world culture vs queue) fit the same
  moments equally well within tolerance and no predeclared discriminating test separates them, report **equivalence**;
  do not choose a winner.

