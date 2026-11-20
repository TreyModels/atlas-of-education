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


## Amendment A2 (2026-11-20 14:52) — loop-5 outcomes: fit window, scaling cap, conditional status

**Trigger:** task-37 PHL smoke fit PARTIAL/EQUIVALENT (holdout MAE 4.84/5.40/6.08 vs linear-trend 4.35; persistence
8.60; all three rivals lose to the trend benchmark); A1 scaling check FAILED (generated OOS exponents wrong sign:
secondary −1.89/−0.38/−0.74 vs +0.286; tertiary −1.23/−0.14/−0.35 vs +0.776); M2c recovery failed predeclared
sufficiency (median |bias| 0.55 > 0.50).

1. **Fit-window amendment (disclosed, accepted):** PHL smoke fit uses observed `status=target` rows only,
   **1999–2010** (n=16), holdout 2011–2024 (n=17). The gate's 1980–2010 window is not available in observed cells;
   this is a declared data-driven amendment, holdout unchanged. Because the window is shorter, in-sample fit is
   not comparable to the original gate and the model **cannot exceed PARTIAL** on this smoke.
2. **Scaling cap:** with wrong-sign generated exponents, the model does **not** reproduce the classified scaling laws
   → universalization reproduction is capped at **PARTIAL** until a structural repair generates the correct signs
   out of sample (R14/R16).
3. **Direction:** EQUIVALENT (R13); no push-pull direction or complementarity claim from these results.
4. **Repair rule:** a scaling-channel repair is admissible **only** as a new predeclared structural cell — a named
   behavioural mechanism (e.g., income→demand/feasibility channel), no exponent used as a parameter, fit/check/holdout
   roles unchanged, and the A1 exponents used only as checks. A repair that fits the exponents directly is a
   restatement and is rejected (R4).


## Amendment A3 (2026-11-20 14:56) — lower-secondary completion law is an estimator range, not a point

**Trigger:** M2b resolution (D15). The lower-secondary completion ~ income law is judged against the **estimator
range**: between-logit **+0.84**, all-year re-run **+1.36**, year-FE log-log **+1.97/+2.28**; the scout relay
**+1.174** is carried as the scout's value (its exact script was not executable in this environment — disclosed).
A1 §1/R14 therefore judges the model's generated logit/log exponents against this range, not a single point, and
requires the **sign** plus range containment (≥2 of 3 classified laws). No post-hoc narrowing of the range.


## Amendment A4 (2026-11-20 15:02) — timing regime for near-universal systems

**User directive.** For near-universal systems (JPN, KOR, HKG; any level at/above threshold for ≥10 observed years),
the outcome is the **timing of universalization**, not the level (definitions and tolerances in
`UNIVERSALIZATION_MILESTONES.md`).

1. **Milestones:** M1 primary NER≥95 (or GER≥100); M2 lower-secondary completion ≥90; M3 upper-secondary completion
   (or transition) ≥90; M4 tertiary GER ≥50. Crossing year = first observed year above threshold; band = adjacent
   observed years; left-censored = boundary constraint only; right-censored = false-positive test.
2. **Timing replaces level:** crossing year within **±5 years** (band midpoint), **±3 years** where the band ≤2 years
   and no definition break; levels become **check-only** (±5 pp, never fitted) for near-universal milestones.
3. **Single-curve fit:** must reproduce timing/midpoint, not the functional form; a level match without timing = PASS
   at most PARTIAL and is a structural miss; supplying the midpoint is R4-invalid.
4. **A1 interplay:** A1 scaling exponents remain required checks; timing is an additional required outcome for
   near-universal cells, not a substitute for the scaling check in expanding cells.


## A4 Clarification C1 (2026-11-20 15:10) — M0, N=5, reconstruction

M0 massification = cohort completion ≥50% (expanding systems); universalization M1–M4 as defined. Timing tolerance
**N = ±5 years** (band midpoint; ±3 y where band ≤2 y). Crossing years are holdout outcomes, never fitted. Censored
UIS ratios may be reconstructed from observed headcounts + documented population denominators, labelled
"reconstructed (not UIS)" with method/uncertainty and two-denominator sensitivity; never imputed as observation.
See `UNIVERSALIZATION_MILESTONES.md` C1.


## Amendment A5 (2026-11-20 15:20) — single-system anchor + portability (user design pivot)

1. **Anchor = PHL** (data-sufficiency argument in `ANCHOR_SYSTEM.md`). The programme's first product is a PHL model
   that shows the mechanisms; portability to CHN (massifying; state-push battery) then HKG (near-universal timing) is
   the test, not the starting point.
2. **Extra PHL success criteria:** (i) mechanism event reproduction for predeclared exogenous events — state push
   (K-12 2013; free SHS 2016; free tertiary 2018; places/teacher expansion) and demand pull (nurse visa 2005–06; BPO
   regional growth; remittances) — break sign/magnitude inside a predeclared band, pre-trend clean, placebos null;
   (ii) rival comparison: ≥3 fair rivals on the same PHL record and events, anchor must beat them on the event-break
   estimand and out-of-sample trajectory, else report EQUIVALENT; (iii) events are **exogenous inputs**, never fitted
   (R4/R12).
3. **Portability:** behavioural core + PHL parameter values transfer unchanged; only declared country inputs may be
   re-set (initial cohorts, observed economy series, policy-event dates/capacity, level-gate mapping, measurement
   definitions). Any behavioural re-fit = FAIL (R20). HKG levels are check-only (timing regime).
4. **Web baseline data:** researcher agents may and should search public sources (UNESCO UIS, World Bank, national
   statistical offices) for baseline series to fill the anchor's missing pre-1999 completion and the event/place
   series — each series recorded with source, vintage, observed flag; no imputation as observation; external
   *requests* still need user approval (site/data rules).
