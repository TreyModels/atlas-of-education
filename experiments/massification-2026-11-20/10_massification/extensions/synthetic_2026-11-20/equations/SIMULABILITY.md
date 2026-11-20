# SIMULABILITY — which families can become a generative simulator, in what order, and what must be stipulated

Short companion to `EQUATION_REGISTER.csv` / `.md`. "Simulable" here means: *a competent person could write the code
today and know which numbers are data, which are estimates, and which are assumptions.* It does not mean the output
would be true.

## 1. Readiness ranking (1 = most ready)

| rank | family | can it generate data today? | needs | main ambiguity | verdict |
|---|---|---|---|---|---|
| 1 | **Formal push-pull (PP)** | Yes — machinery already exists and runs | a rebuild of two blocks (see §2); income, urbanisation, fertility, cycle lengths on disk | high: 14 free parameters with *two disagreeing declared bound sets*; no observed job series (the model invents its own) | **simulable after rebuild** — machinery is the asset, the equations are not |
| 2 | **Scaling / trajectory (SC)** | Yes — as an empirical *constraint*, and as a curve-fitter | panel of GER/completion + GDP pc (on disk, n≈1,000) | the *exponents* are well estimated; the *shape* (logistic vs Gompertz) is not identified — E6 failed for every form | **simulable as targets/checks, not as a law** |
| 3 | **Demographic / cohort (DEM)** | Yes — pure accounting, no estimation needed | TFR paths (4 of 6 countries on disk; KOR/JPN assumed) | constants are conventions (female share 0.5, 35-year span, 3 survival bands) and the cohort→completion link is **not established** | **simulable as bookkeeping; the behavioural link is not** |
| 4 | **State capacity (SB)** | Yes — with a gate that is declared, not fitted | PTR + spending %GDP + policy dates (all on disk for PHL) | which weights, which κ, and what "enforcement" means when nothing measures it | **simulable only as a declared assumption with a sweep** |
| 5 | **Sectoral / structural (SEC)** | Yes — as declared reduced forms | sector shares (but ILO-**modelled**, not measured) | the functional forms are invented; no canonical form exists in the literature | **simulable, not estimable** |
| 6 | **Human capital (HC)** | Only with an invented response rule | a returns→enrolment elasticity (NOT FOUND) and a level-specific return series (BLOCKED) | the price is known (8.8%), the response is not | **not simulable without stipulating the bridge** |
| 7 | **Labour queue / credential (LQ)** | No, not for expansion | employer requirement schedule / job postings (absent); class transition data (BLOCKED) | the four real equations describe *effort and winners*, not enrolment levels | **not simulable for massification**; usable only as a distributional add-on |
| 8 | **World society (WS)** | No | a coded adoption corpus, INGO ties, democracy index (absent) | no specification, no coefficients, no series | **not simulable at all** |

**The pattern.** Rank order runs almost exactly opposite to theoretical importance. The family the project is *about*
(human capital) ranks sixth; the family with the best equations (queue/credential) ranks seventh; the family with the
best claim on the anomaly (world society) cannot be simulated at all. What *is* ready is the arithmetic (cohorts), the
empirics (exponents and curves) and the project's own machine.

## 2. What must be fixed before any generator is built

These are not preference items. Each one is a code-level defect that would make synthetic output unusable.

1. **Enrolment scale.** `pushpull.py` L114–120 multiplies cycle lengths into an already cycle-multiplied stock, so
   committed GER runs 332.8–3514.4 per cent (audit D-02). A generator that emits GER from this block emits nonsense, and
   every crossing-year result built on it is an artefact (M4 = 1960 in all 12 arms, including the no-push arm).
2. **Completion must come from the cohort.** Completion is currently `100·p_pri·p_low·p_up` — a product of fitted
   probabilities that never sees the population vector (audit D-01), despite the code comment saying otherwise. If
   completion is the fit series *and* the output of interest, it has to be reconstructed from the flow.
3. **One parameter-bound set.** `configs.py` and `calibrate.py` disagree on `e_d` (0.8 vs 0.6), `lag_d` (5 vs 3),
   `lag_s` (8 vs 6) and `g0` (0.05 vs 0.045). Pick one, in one file.
4. **The K-12 switch.** Declared in three predeclarations, absent from the code: `CYCLE['PHL']` has no year dimension
   (audit D-21). Any cohort-exposure experiment is unimplementable until this exists.
5. **The A1/A3 contradiction.** The target secondary exponent 0.286 lies outside the containment range
   [0.0904, 0.2154] (audit D-13). A generator scored on both fails by construction. Choose one criterion.

## 3. Identifiable — may be calibrated or imposed as a target

| object | value | why it is identifiable |
|---|---|---|
| Mincer private return | **0.088** world / 0.087 EAP | compiled from ~139 economies; a price, stable across decades |
| Place premium | **3.99** (3.71–4.36) | Mincer on >2m workers, 43 countries, selection-corrected |
| Nurse-supply response | **9** licensed nurses per migrant; +126%; pass rate 38.4% | a causal DiD design with a policy shock |
| Income gradients | sec **0.215** between / 0.090 within; tert **0.567** / **0.848**; lower-sec completion **0.169** / **0.247** | n ≈ 1,000, 28–30 countries, two FE structures, stable signs |
| Sector-share gradients | agri **−0.990** between; industry **0.143** between / **0.528** within | same panel, n = 1,017 (but shares are ILO-modelled) |
| Cohort-size semi-elasticity | **−0.189** (0.044) | negative in 10/10 splits, significant in 8; the only relation the phase grades plausibly causal (R07) |
| S-curve parameters | e.g. PHL secondary K=92.3, r=0.0525, t0=1971.9 | only where a series starts well below ceiling and completes take-off — **68 of 194** series, never elsewhere |
| Push-pull lead-lag *moments* | wage-share→secondary F=4.11; tertiary→GDP F=6.52; completion→GDP −0.667 | estimable as moments; **not** as direction |

## 4. Not identifiable — must be declared assumptions, never calibrated

Every item below has **no estimate in the literature layer and no data on disk**. Calibrating any of them to the
observed series would be fitting the answer.

| object | where it lives | why it must stay an assumption |
|---|---|---|
| **Returns → enrolment response** (elasticity, lag) | HC-03 | no estimate in any retrieved source; PSA earnings BLOCKED |
| **Capacity gate exponent κ and the 0.5/0.3/0.2 weights** | SB-01, SB-02 | Council-declared; sensitivity over κ **announced but never run** |
| **Enforcement intensity e_t** | SB-03 | zero enforcement series in the package; the current proxy is de jure duration and is double-counted |
| **Requirement-ratchet speed g** | LQ-08 | "NOT FOUND"; no requirement schedule exists |
| **Intake damping 0.1, autonomous job growth 0.012, baseline educated share 0.15** | PP-01, PP-03 | bare code constants with no source |
| **Educated-share adjustment 0.97/0.03** | PP-08 | no educated-labour-share series exists to fit it |
| **Sector constants 0.75 / 0.35 / 0.45 / 0.08 / 0.15 / 0.25 / 0.55 / 0.05** | SEC-01…03 | chosen; literature has no form; audit calls the block a relabelled income term |
| **PUSH 0.05 and CEIL 0.25** | SB-01 | additive probability points chosen by hand |
| **Survival 0.995/0.994/0.96; female share 0.5; 35-year span** | DEM-01, DEM-02 | declared approximation, no life table |
| **ECI → schooling** | SEC-05 | no specified form anywhere; the growth-premium replication failed |
| **Mincer–behaviour bridge (any form) at all** | the whole HC family | the single largest gap (§6) |

## 5. What a v0 generator should actually do

1. **Start with cohorts, not with the old model.** Births from TFR → one-year ageing → entry at six. Exit nothing.
   This is the only block that is arithmetic rather than assumption.
2. **Impose the income gradients as a monthly/annual check**, not as an input schedule (the programme's R4 rule): the
   generator should be *asked* for 0.215 / 0.567 / 0.169 and allowed to fail.
3. **Build the completion chain from the flow** (`cohort_t × Π transition`), then express GER as a stock ratio on the
   correct denominator, and assert `0 ≤ GER ≤ 105` as a hard validity gate before any output is written.
4. **Declare, in one file, every constant in §4** with a range, and label the output `SIMULATED — assumptions not
   estimated`. No exception.
5. **Reproduce the observed ordering, not the levels**: PHL primary 2017 → lower-secondary 2024 → upper-secondary
   *never* → tertiary 2024–25. A generator that crosses the top level fails, regardless of fit (R6).
6. **Do not fit lead-lag moments.** Max |partial correlation| after own-lag control is 0.208 across 24 cells, so the
   visible schooling–market co-movement is shared trend; a generator tuned to match a strong lead-lag is over-fitting
   the trend and will not survive resampling.

## 6. The one honest sentence

Out of 43 relationships, **10 are equations the literature states, 13 are narrative, and 20 exist only because this
programme wrote them down** — and the most important link of all, from a price or a gate to a family's decision to keep
a child in school, is not among the 10. A synthetic-data generator built on this register can reproduce the *shape* of
massification and the *gradients* that accompany it. It cannot yet claim to reproduce a *mechanism*, and the honest
output label for anything it produces is: **simulated from declared assumptions, with no mechanism identified.**
