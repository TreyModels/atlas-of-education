# COUNCIL REVIEW 014 — Codex toy/illustrative massification models

**Type:** design review only. The massification phase stays **CLOSED** (closeout tip `787f1792…`; headline
“conditional LEVEL reproduction + observational equivalence + an unreproduced asymmetry”). Nothing here re-fits,
reopens, or endorses a claim. **The Codex/Luna material is ILLUSTRATIVE: parameters are stipulated, not estimated;
no historical test was run.** Sources: `codex_bundle/RESEARCH_UPDATE.txt`, `codex_bundle/workspace/{model.py,
experiments.py,diffusion.py,takeoff.py,construction.py}`, `luna_bundle/outputs/luna-results.md`,
`luna_bundle/work/nsw-schools.csv`; closeout `MASSIFICATION_CLOSEOUT.md`; gate `08_council/brief_013/`.
Panel: LUTZ (measurement), PATRINOS (identification), PAGE (model/scaling), CARTWRIGHT (falsifiability); composites.

## 1. Helpful or not — cluster by cluster

| Cluster | Verdict | Genuine insight | Imposed / reduced-form parameters (not estimates) |
|---|---|---|---|
| **Constrained seats / admissions** (`model.py`, `experiments.py`) | **Useful sensitivity — strongest cluster** | **Net ≠ gross**: expanding public seats can be offset by private exit (30→50 seats yielded ~5 net admissions; 38→39 seats total fell 50→39). Fixed vs divisible supply 2,702 vs 15,500 cohort-seat settings; conditional mean shortfall 8.98. Elite public priority cut poor admissions 15.03 and total 17.12 per 100. | premium **4.0** (not an equilibrium wage), common demand, opportunity cost U[0,3.5), budgets {1.5,4}, private capacity 30, tuition 2, fixed cost 12, seat cost 1; one known break-even bug (decimal 1.40). |
| **Generational takeoff** (`takeoff.py`) | **Useful sensitivity** | Funded initial capacity dominates (cohort 30 baseline 102/75/14 vs funded 113/105/92); high child-work value collapses secondary/tertiary (63/4/0); “mandate only” without capacity (112/71/5). | N=120, seats [18,0,0], fees (.20,.36,.55), skill returns (.25,.40,.60), access/rank weights, cash/work distributions, **funded push imposed**, build_limit, capital=1. |
| **Rural construction / cost** (`construction.py`+`diffusion.py`) | **Novel policy-insight, but illustrative** | Fee abolition without cheap seats can **lower completions** (applications 23.36→28.70, completions 15.38→11.41 at cohort 30 when rural seats cost 2× urban); reserving one place moved the effect to +1.0; equal costs +5.59; cohort 60 ~+12. | rural_cost 1/2, reserve flag, seats [16,6,2,0,0,0], jobs (.23,.08), travel .06+.23d, spill .5, tuition/incidentals; “no dated seat schedule”. |
| **Jobs / credential feedback** (`experiments.py` item 5; Luna 3) | **Useful sensitivity** | Visible placements + responsive employers raise hires/applications (2.88→4.11; 35.12→41.23; low-resource 3.25→5.10); **no visibility → no demand response**; fixed vs responsive jobs 8 vs 19.94 at cohort 20. | visibility, enterprise responsiveness, 8 jobs, 200 matched populations, information reach; responsiveness imposed. |
| **Rival signatures** (`experiments.py` item 6; Luna 1–15) | **Artefact by construction — pedagogy, not discrimination** | The fixed-job check shows rank vs skill produce opposite output effects (30.45→32.24 skill; 28.24→28.03 rank); household fee cut 36.9→48.1 across all theories; abolishing eligibility/ranking arms 1.4 / 25.3. | Signatures are imposed; “preliminary Luna subsidy tests bundled treatment changes and **cannot rank theories**” (Codex’s own caveat). No observed discriminating moment. |
| **Temporary expansion** (Luna 7) | **Useful sensitivity** | All arms +~12 enrolments; later cohorts: supply-only no demand/hire effect; fixed jobs **−7.083 applications**; responsive employers +0.260 apps/+3 hires, decaying to none by cohorts 16–20; earlier version failed accounting and is superseded. | 12 leased seats, fee waiver, employer responsiveness, 200 paired seeds; temporary capacity is a shock with expectation effects, not an estimate. |
| **NSW opening order** (Luna 15) | **Too weak as a holdout; pilot only** | Six pairs preselected before outcomes (good practice); two scored: Bathurst HS 1883 vs Kelso HS 1976; Dubbo HS 1917 vs Wellington HS 1955; four unscored. | Exact-High-School classification dating misses earlier secondary instruction (Kelso public 1871 vs high 1976; Wellington Intermediate High 1923 vs High 1955; Maitland 1884↔1987); no district fees/applications/jobs/household covariates; deterministic tie by label. |
| **Diffusion / geography** (`diffusion.py`) | **Useful conceptual sensitivity** | Urban-elite start → rural diffusion with travel, information spill and tiered access (rural 28.6/15.4/0 vs urban 55.2/54.1/50.7; fee-free 38.2/11.4/0; travel+incidentals 39.5/15.9/0; with capital 208.5/137.7 vs 129.5/121.4). | seat/job/travel/spill/tier parameters all stipulated; “no dated seat schedule”; illustrative units. |

**Overall:** the bundle is a **mechanism sandbox** — useful for generating hypotheses and for teaching why net/gross,
supply constraints, information and employer response matter. It contains **no estimate, no calibration and no
historical test**, and most cross-cluster “results” are differences between stipulated parameter regimes.

## 2. Does any of it touch the closeout limits?

- **C1 (correct-sign income scaling — the missing exogenous supply channel).** **Not touched as evidence, but the
  one genuinely useful pointer.** The cohort-flow class failed R27 because income entered demand/progression margins
  only; Codex’s constrained-seats/private-entry cluster names the missing object — **provider entry and capacity
  response** — and shows why it is nonlinear (fixed-cost entry threshold, private exit under public expansion). That is
  a hypothesis for C1, not a test: there is no observed provider-entry series, no entry elasticity, no calibration.
  If the user reopens, this is the first place to look (see §3.1).
- **HC vs signalling vs queue.** **No discriminating test.** `model.py` switches the credential premium by an imposed
  “visibility” parameter; the rival-signature items compare stipulated regimes; Luna item 5 is a staged screening
  model, not an equilibrium vacancy test; item 15 is partially scored. Codex itself says the subsidy tests “cannot rank
  theories”. Nothing here could adjudicate the three rivals on observed data.
- **NSW opening-order holdout (a C3-type design).** **Too weak as-is.** Two of six pairs scored, both with fragile
  classification/dating (intermediate/central schools, 1884 vs 1987 reclassification), no linked district histories of
  fees/applications/jobs/households, no test of rival predictions. It is a **data-collection pilot**, not a holdout.
- **C2 (fixed-behaviour crossings) / C4 (de facto capacity and enforcement):** untouched. The temporary-expansion and
  takeoff items illustrate mechanisms but add no observed annual capacity or enforcement series.

## 3. Promising new direction, ranked (only if the user reopens; phase stays closed otherwise)

### 1. Provider-entry supply response as the C1 channel (best)

The one extension the toy material actually motivates, and the one that targets a documented closeout limit.

- **Question:** does observed provider entry/capacity respond to demand strongly enough to generate the correct-sign
  income-scaling exponents the cohort-flow class could not produce?
- **Arms:** high- vs low-demand-exposure regions (PHL: BPO/remittance/income growth) × provider-entry regime
  (open entry vs constrained — public/private school and HEI approvals, CHED/DepEd rules); 2×2 with a predeclared
  event/eligibility window.
- **Estimand:** first stage — elasticity of private provider entry/seats/programmes to demand; second stage — OOS
  income-scaling exponents from the model **with observed supply response** (no exponent supplied as parameter).
- **Threshold (predeclared):** first-stage entry elasticity positive and above a declared minimum; exponents positive
  and inside the A3 range for ≥2 of 3 classified laws; R27/R4 still binding.
- **Data cost:** 2–4 weeks — public CHED/DepEd programme approvals, HEI/school counts, private enrolment by region;
  PIDS/BEPER tables; PSA microdata still blocked (would need user approval).
- **Falsifier:** if the observed entry elasticity is ~0, or the sign stays negative with the measured supply response,
  **C1 is recorded as a negative result** (the missing channel is not there) and the phase stays closed.
- **Why it beats the rest:** it is the only direction that turns the toy’s structural lesson (fixed-cost entry) into an
  observable test of a stated closeout limit; the toys supply the hypothesis, not the evidence.

### 2. Employer skill visibility / credential requirement (C3-adjacent, hard)

- **Arms:** variation in employer skill visibility or credential requirements (licensing changes, blind/structured
  hiring, degree requirements; PHL PRC/civil-service rules, cross-country policy changes) × schooling outcomes.
- **Estimand:** schooling/enrolment/field response to a visibility/requirement shift.
- **Threshold:** predeclared sign and size; if no response, that is evidence against a pure signalling/queue reading
  (report as such, not as proof of human capital).
- **Data cost:** high — job-posting/employer-requirement series are not on disk; public licensing rules are obtainable,
  linked outcome data are the bottleneck (PSA 403; user approval).
- **Falsifier:** no detectable schooling response to a credible visibility/requirement change.
- **Rank 2** because the discriminating moment is the hardest to measure; the toy’s visibility parameter is a
  hypothesis-generator only.

### 3. De facto capacity/enforcement panel (C4)

- **Arms:** observed de facto capacity/enforcement (inspection reach, attendance/sanctions, construction, procurement)
  across districts/periods; estimand: capacity → crossing timing; threshold: capacity-timing beats law-only (A10) on
  crossings; data cost: 3–5 weeks public DepEd/DPWH/COA documents; falsifier: capacity again ties law-only → C4
  negative. Rank 3: hardest data, and the closeout already found capacity ties law-only with the proxies available.

**NSW** is not ranked; it is a pilot for a linked district-history dataset, not a next cell.

## 4. Risks / labelling if ever added to the branch

- **Illustrative ≠ estimate.** Every Codex/LUNA number is conditional on stipulated parameters; none may be quoted as
  a finding, calibrated parameter, or historical validation.
- **“All historical diffusion rows reproduced”** means their own synthetic rows, not history; “historical comparison
  partially scored” (2/6 pairs) is not validation.
- Required labels on any archived copy: `ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no
  historical test; phase closed; do not cite numbers as estimates.` Keep under `extensions_archive/`, never in results
  tables or the writeup's evidence columns. No new claim may cite it without a predeclared test and Council acceptance
  (A-gate/R-gate).

## 5. Bottom line for the user (plain language)

The toys are **useful for thinking, not for evidence**. They explain, cheaply, why expanding public seats can leave the
total unchanged (private providers exit), why free tuition without cheap seats can lower completions, and why
information and employer response matter — but every number is an assumption, and none of it tests the closed phase's
limits. The single direction worth reopening for is **provider entry and capacity response as the missing supply
channel**: measure it, then see whether the income-scaling sign flips. If that response is not there, the honest
answer is the closeout's negative result and the user's time is better spent publishing the limits than adding toys.
**Dissent:** PATRINOS — even the provider-entry cell is observational and may be underpowered; run it only with a
predeclared first stage. PAGE — the bundle's real value is the mechanism menu, not its numbers; CARTWRIGHT — the rival
“signatures” are stipulations and must never be called tests; LUTZ — NSW is a pilot and should not be described as a
holdout.

— Council, brief 014 (design review only; phase CLOSED; nothing pushed). Written to
`massification_live/extensions_archive/codex_2026-11-20/COUNCIL_REVIEW_014.md` at the user's request.
