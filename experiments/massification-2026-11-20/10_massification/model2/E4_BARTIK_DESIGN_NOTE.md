# E4 BARTIK SECTOR-DEMAND PULL — design note (NO analysis performed, NO direction claim)

**Status:** design note only, prepared in spare capacity at the executor's request (D25: E4 elevated to KEEP as
the next identification route after the income-channel cell). **Nothing here was run; no data were analysed; no
result or direction claim is made.** Every claim in any future E4 run remains capped by R13/EQUIVALENT. No git
writes (executor commits). Prepared by `deepseek-exp2` (experiment-runner-2), 2026-11-20.

## 1. Question and estimand (what E4 would identify)

Does **local sector-demand pull** — plausibly exogenous growth in the sectors a region is exposed to — raise
schooling/completion/transition (or reallocate cohorts across education and sectors)? The estimand would be a
local demand-pull response, **not** the system-wide push/pull direction: a Bartik design identifies a *regional
demand exposure* effect, and comparing it with a supply-push design (E1 redesign or E2/E3 pair) is what could
eventually speak to direction. **No direction claim is made here.**

- Primary outcome: upper-secondary completion (cohort basis) and tertiary transition proxy (gross-intake proxy
  labelled `check` per `10_massification/data/DATA_NOTES_MASSIFICATION.md`).
- Secondary outcomes: sectoral employment shares (agri/industry/services, status shares), formal/informal where
  measured (KHM single cell only — do not extrapolate).
- Unit: subnational region × cohort (or region × year with cohort exposure mapped by age/entry year).
- Estimand: cumulative effect of a one-SD increase in Bartik exposure on the outcome, with event-time dynamics.

## 2. Data needed (precise) — and what is currently missing

**Required for a credible Bartik design (all observed; no imputation as observation):**
1. **Subnational employment by sector** (≥1-digit, preferably 2-digit), annual or 5-yearly, 1995–2024, with
   **baseline shares** at a fixed t0 and consistent region boundaries. Needed both for base weights and for
   leave-one-out national growth.
2. **Subnational schooling outcomes**: upper-secondary completion, tertiary transition, and (if possible)
   completion by cohort, matching region definitions and cohort timing.
3. **National sector growth rates** (observed), with the region's own contribution removed (leave-one-out).
4. **Regional covariates**: GDP pc (or proxy), urbanisation, remittances, population/cohort size, teacher supply
   (PTR), education spending where available.
5. **Pre-period outcomes** (≥5 pre-treatment years) and a clean exposure timing (which cohorts are exposed).

**Currently available:** `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` is **country-year only** (6
countries, 1995–2024; sector/status/LFPR/NEET/GDP/urban/remittances/spending/teachers/PTR) and
`UNIVERSALIZATION_SERIES.csv` is country-level education flows. **There is no subnational/regional dimension on
disk**, so E4-Bartik cannot be fielded as a regional design with the present data.
**Blocked routes already recorded by data-hunter** (`DATA_NOTES_MASSIFICATION.md`): PSA LFS/FIES/APIS HTTP 403
(PHL microdata); ILOSTAT 403 (occupation, informality, earnings by education); OECD 403; Enterprise Surveys API
unavailable. **Subnational sector employment is not on disk and is not in the blocked list as a named source** —
it needs a targeted pull (national statistics offices, World Bank subnational, provincial yearbooks).

**Fallback if subnational data cannot be secured:** report **DATA BLOCKED** for E4 (no simulated substitute
prescribed as identification; a country-level shift-share could be run only as a descriptive `check`, explicitly
not identification). This is a design decision for the Council/executor.

## 3. Exposure construction (to predeclare before running)

- Bartik/shift-share: `B_{r,t} = Σ_s ω_{r,s,t0} · g^{(-r)}_{s,t}`, where `ω` = baseline sector shares in region
  r at t0 (fixed, no reweighting), and `g^{(-r)}` = national growth of sector s excluding region r (leave-one-out
  to avoid mechanical own-shock feedback; a version using national growth including r is a robustness row).
- Sector level: 1-digit baseline; 2-digit if the subnational series allow (predeclare; no post-hoc switch).
- t0: earliest common year with sector shares and outcomes (predeclare; sensitivity: two alternative t0s).
- Exposure timing: map exposure to cohorts by school-entry age (declare the mapping; e.g., exposure at age 12
  affects upper-secondary completion 4–6y later); declare lag structure (−3 to −5 years) before estimating.
- Normalisation: standardise B within country-year (z-score) so effects are per-SD.
- **First stage / relevance** predeclared: report first-stage F and instrument strength; if weak (F < 10
  declared), cap at descriptive (no causal claim).

## 4. Estimator and specification (to predeclare)

- Baseline: two-way FE (region + year) event-study
  `Y_{r,t} = α_r + λ_t + Σ_{k=-5..5} β_k B_{r,t-k} + X'_{r,t}γ + ε_{r,t}`, cluster by region (CR1).
- Alternative: first-difference and long-difference (5y/10y) specifications; cohort-exposure variant using
  cohort entry year rather than calendar year (predeclare which is primary).
- Estimand reported: cumulative β over post-exposure horizon, with event-study plot and joint tests.
- Heterogeneity: baseline sector mix (agriculture-heavy vs services-heavy), baseline completion level.

## 5. Pre-trends and placebo (predeclared, with thresholds)

- **Pre-trends:** event-study pre-coefficients for k=−5…−1; joint test **p > 0.10** and no monotone pre-trend
  (predeclare the monotone test); pre-2013 placebo cohorts. If pre-trends fail → **no causal claim**, R10 event,
  descriptive only.
- **Placebo / falsification:** (a) fake exposure timing (shift B back 3–5y before the actual shock), (b) outcomes
  for cohorts too old to be exposed (must be null), (c) negative-control sectors with no plausible schooling
  link, (d) leave-one-out exposure construction as robustness. Predeclare expected null/negative signs; failure
  → no claim.
- **Rivals tested as controls/limitations:** national trend/cohort composition; regional schooling supply
  (teachers/PTR/spending); migration and remittances; overlapping reforms (PH K-12 2013, free SUC tuition 2018,
   4Ps CCT); human-capital/world-culture alternative predictions. Each with a predeclared test or a stated
  limitation.
- **Power / MDE:** compute with observed outcome variance and the available number of regional clusters; state
  the minimum detectable effect (in SD and pp completion) at 80% power, α=0.05, before running; if underpowered,
  cap the claim at descriptive (PATRINOS underpowered-at-national-scale warning, and M2c's size-bias result).
  Predeclare the minimum cluster count acceptable.

## 6. Claim caps, labels and stop-rules

- **Labels:** observed vs simulated stated; no imputed cell as observation; no closed shadow claim re-fit.
- **R13/EQUIVALENT:** no push/pull direction or complementarity claim from this design; Bartik identifies a
  local demand-pull response only, and must be paired with a predeclared push design to speak to direction.
- **Verdict vocabulary (SUCCESS_CRITERIA §4):** PASS / PARTIAL / FAIL / EQUIVALENT, plus **DATA BLOCKED** if
  series are absent; PASS-CONDITIONAL only under a declared channel mixture (Amendment A1 §3).
- **Stop-rules to cite on failure:** R3/R13 (equivalence/direction bar), R10 (pre-trends fail → no causal
  claim), R14/R15 (scaling/reproduction caps), R5 (no new moment → re-parameterisation, not improvement).
- **Acceptance:** must meet `08_council/brief_013/INTAKE_ACCEPTANCE.md` common bullets (data provenance/roles,
  labels, fair rival, numeric decision rule, failure rule + stop-rule link, deliverables) and copy
  SUCCESS_CRITERIA §2–§4 + Amendment A1 verbatim before any run.

## 7. Questions for Council/executor/data-hunter (ASK)

1. **Authorise a subnational data pull** (named sources) for E4: PH regional sector employment + regional
   schooling outcomes (PSA blocked; World Bank subnational/provincial yearbooks?), and/or CHN provinces as
   replication. Without a subnational dimension, E4 cannot be fielded as Bartik — confirm DATA BLOCKED route.
2. **Confirm sector level and base year** (1-digit vs 2-digit; t0) and the allowed sensitivity set before
   predeclaration.
3. **Confirm exposure-to-cohort mapping** and the primary lag horizon.
4. **Confirm whether a country-level shift-share descriptive check** is acceptable as a labelled fallback (not
   identification), or whether E4 should stop at DATA BLOCKED.
5. **Confirm the predeclaration template/acceptance** for E4 under A4 (timing outcome) — the Council Amendment A4
   text is pending; E4 should not predeclare until A4 and the timing series (`UNIVERSALIZATION_TIMING.csv`,
   dated timelines, crossing-year estimates) land.

**No analysis was run for this note; no direction claim; no git writes.**
