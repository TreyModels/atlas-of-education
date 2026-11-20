> **SYNTHETIC EXERCISE — DESIGN DOCUMENT.** Panelists are AI-constructed composite personas whose positions are
> inferred from the published literature. Nothing here is a statement by, or endorsed by, the named individuals or
> any living person. This file is a **design precommitment**, not evidence.

# SUCCESS_CRITERIA — operational definition of "reproducing massification/universalization"

**Status: BINDING GATE for task-37 (model/calibration).** No fitting starts until this file is registered.
**Declared:** 2026-11-20, before any massification-phase fit. **Amendments** require a new timestamp + hash and do not
apply retrospectively. "Observed" = on-disk measured series; "simulated" = model output; no imputed cell is an
observation.

## 1. What the terms mean operationally (design choices, predeclared)

- **Massification** of a level = the cohort participation/completion share crosses from below 50% to at least 50%
  between two observed periods. **Universalization** = near-universal completion of a level: primary completion
  ≥95%, lower-secondary ≥90%, upper-secondary ≥90% (cohort completion, not enrollment).
- **"Reproducing" universalization** = the model generates (a) the observed massification/universalization transition
  for the predeclared series, (b) with the midpoint year within ±5 years and the final level within ±5 pp, (c) on a
  held-out country and a held-out period it did **not** fit, (d) beating naive benchmarks, and (e) **not** generating
  universalization where the observed series did not universalize (false-positive test). All five are required.
- A model that needs the transition as a supplied schedule, or that matches only after fitting to that series, has not
  reproduced it (it has restated it).

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

## 5. Naive benchmarks (must be reported alongside)

Persistence (last observed value carried forward), linear trend, cohort progression (constant transition rates),
and — for description only — the UIS/WDI modelled series. A model that loses to any of these is not a result.

## 6. Data discipline

Every series carries: source, table, vintage, observed/imputed flag, definition (completion vs enrollment vs
attendance; cohort vs stock), and the role label. Data defined differently across countries/years are harmonised **or
excluded** before fitting; no silent splicing. Series already marked `unresolved` in `04_data/TARGETS_*.csv` stay
unresolved — they cannot be targets.

## 7. Gate and amendment

- **task-37 may not begin calibration until this file is registered** in `08_council/brief_013/` and acknowledged by
  the Lead. The runner's first action is to write the fit/check/holdout table from §2 into its own predeclaration and
  reproduce the tolerances verbatim.
- Any change to §2–§4 requires a dated amendment, a new hash, and disclosure; it may not be applied to already-run
  cells.
- This definition is a design choice, not an empirical claim; disagreements are recorded in the deliberation.
