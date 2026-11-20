# MODEL ARCHITECTURE — tiered, occupation-aware synthetic education economy (user directive, 2026-11-20)

**Status: design directive (Lead-recorded, from Dr. Menefee's verbal specification). Not results, not evidence.**
This supersedes the "one education variable → one growth relation" picture and becomes the target architecture for
the synthetic-data generator (v1). Plain English first, then the formal sketch. Every relationship must be a
**declared assumption** labelled as such; the fact register (`synthetic_2026-11-20/facts/`) says which facts the
synthetic world must reproduce.

## The user's specification, restated

1. **Different levels do different economic work — they are not the same variable.**
   - **Literacy / primary**: a *prerequisite* for the first industrial step ("if you start making your country
     literate, you get some economic bonus — I've been to China; it led to basic industrialization"). It is a
     threshold condition for labour-intensive manufacturing/formal wage work, not a general growth engine.
   - **Lower secondary**: the "horse race" starts here — competition for formal rungs, credentials, rank.
   - **Upper secondary / tertiary**: more specialised, more options, but returns depend on the *occupational
     structure* — "you need more than fifth grade to work in an office," but a large economy has many jobs.
2. **The non-farm economy is not one thing.** Formal networks, informal networks, family enterprise,
   street-food/self-employment are distinct absorbers with different returns to schooling. In the informal
   economy literacy may barely pay; the formal wage economy is where the schooling premium lives.
3. **The Philippines case is an absorption-composition question.** It "produces capacity for a bunch of office
   workers" (BPO/clerical), but the economy has many other jobs. The question is not "how many graduates" but
   **which occupations the schooling capacity fits** — and what happens to the marginal graduate when the office
   rung is full.
4. **Different dynamics in different places.** The same level of schooling can pay off in one economy and not in
   another because the job structure differs; the model must therefore carry country-specific economic structure,
   not a single global production function.

## Architecture (v1)

### Layer 0 — synthetic economy states
Each synthetic country-year carries four state blocks:
- **Economy/complexity**: `ECI`-like complexity index `X_{c,t}` (occupational variety + product sophistication),
  income `Y_{c,t}`, urbanisation `U_{c,t}`.
- **Sector mix**: shares `s_ag, s_inf` (informal/self-employed/street-food/family), `s_man` (industry),
  `s_srv` (formal services incl. office/BPO). `s_ag + s_inf + s_man + s_srv = 1`.
- **Job ladder**: rungs `r = 1..R` (elementary formal, clerical/office, technical, professional/managerial) each with
  a demand `J_{r,c,t}` that grows with `X` (complexity creates rungs) and with sector shares.
- **Takeoff state** `T_c ∈ {pre-industrial, industrializing, diversified}`: a regime switch, not a continuous
  variable. Returns to literacy are ~0 in pre-industrial, positive in industrializing, and literacy is no longer
  the binding margin in diversified economies (where the horse race is at secondary+).

### Layer 1 — schooling supply (cohort flow; the old model's bug fixed)
Cohorts → intakes by level → progression/survival → completion → graduates by level `G_{L,c,t}` for
L ∈ {primary, lower-sec, upper-sec, tertiary}. GER bounded ≤105; completion is a cohort-flow object, not a product
of fitted probabilities. (Reuse the corrected stock-flow algebra from generator v0 / Z1.)

### Layer 2 — absorption / matching (the heart of the user's point)
A graduate of level L can be absorbed by:
- the **informal block** (always available, low return, no credential requirement; "street food / family
  enterprise") — this is the residual absorber;
- a **formal rung r** whose required level is ≤ L and which still has vacancies.
Matching is rank-based: when formal vacancies at a rung are fewer than qualified graduates, the surplus queues
(the horse race) or falls into the informal block. **Returns**: wage = rung wage × (1 + premium × completed level)
× rank factor; informal wage = base informal productivity (weakly related to literacy, stronger once `T` upgrades).
- **Primary/literacy** pays off mainly by raising informal/agricultural productivity *and* by enabling the
  industrializing transition (a threshold: `T` upgrades only if literacy ≥ declared threshold and other
  preconditions are met).
- **Secondary/tertiary** pays off only when a matching formal rung exists; extra graduates beyond the rungs do not
  raise growth, they raise queue length/credential inflation.

### Layer 3 — growth
`g_{c,t}` = productivity growth in each sector weighted by shares + a **composition term**: moving a worker from
informal to a formal rung adds a finite step; once the rungs are full, further schooling adds queue, not growth.
This reproduces the user's "economic bonus from literacy" (takeoff) and the weak aggregate education–growth
relation at higher levels (horse race redistributes rather than creates).

### Layer 4 — synthetic output (what we generate)
Multiple synthetic economies with different `X` paths, sector mixes and takeoff dates (including a PHL-like one
with a narrow office sector). Outputs: cohort flows, enrolments/completions by level, formal/informal employment
shares, queue lengths, wages, GDP growth. The generator emits a panel plus a "reproduction checks" table.

## Predeclared checks for v1 (to be frozen before the run)

- **A. PHL signature** (from the fact register): primary completion ≥90 first in 2017; lower-secondary ≥90 in
  2024; upper-secondary **never** ≥90 by 2024 (≤~76); tertiary GER 16.3 → 51.1 (1971–2025). One parameterisation,
  no per-level rescue.
- **B. Literacy vs schooling horse race**: in synthetic cross-country data, the literacy–growth association should
  be positive where the economy is industrializing/diversified, while the years-of-schooling proxy–growth
  association is weak or null — i.e. the model mechanically reproduces the user's 2015 pattern **only if the
  takeoff/occupation structure is in it**.
- **C. No horse race at primary**: at low schooling levels the return is broad/flat (no rank competition); the
  rank/queue premium should appear only at lower-secondary+.
- **D. ECI gating**: a given schooling increment yields more growth in high-`X` economies (more rungs) than in
  low-`X` ones — the threshold the user described.
- **E. Composition > totals**: two economies with the same graduate count but different sector mixes should have
  different growth and queue outcomes (the Philippines-vs-diversified point).
- **F. Identity/accounting**: no negative stocks, GER ≤105, cohort conservation exact, employment shares sum to 1.

## What this replaces

The v0 generator (one demand ceiling per level + capacity gate) stays as the **arithmetic skeleton**; v1 adds the
takeoff regime, the sector/occupation block, rank-based matching and the queue. The longitudinal ECI panel
(`longitudinal_2026-11-20/`) supplies the empirical gradients that v1 must reproduce (literacy vs years; ECI
interaction; tercile slopes), with the caveat that those are 30-country associations, not causal estimates.

---

## Amendment A1 (user clarification, 2026-11-20, dashboard) — education → complexity is the hypothesis

**Status: design directive. Not implemented in v1 as delivered. Requires a v1.1 predeclaration before any run.**

The user has restated the hypothesis that the generator must encode, distinct from what v1 does today:

1. **The hypothesis is education → economic complexity (ECI).** More education builds economic complexity.
   **Growth is a different outcome** and is not the target of this hypothesis. The user prefers **ECI over GDP**
   as the outcome measure. (The earlier H2 test, ECI → growth, is a different question and does not test this claim;
   it returned negative in the 30-country panel.)
2. **Existing evidence to build on (do not redo):** `09_relations/LITERACY_ECI_DEMOGRAPHY.md` —
   - ECI ~ adult literacy **stock**: 0.001 (se 0.005, p = 0.83) → **no relation**;
   - ECI ~ **primary completion lagged 10 years**: **0.593** (se 0.176, p = 0.001) → the schooling **flow** tracks
     complexity;
   - ECI ~ upper-secondary attainment: 0.055 (ns); ECI ↔ log GDP pc jointly determined (0.568 / 0.322, no direction);
   - the Growth Lab growth projection does not predict realised growth (−0.004).
   Plain reading: **the schooling FLOW tracks complexity; the literacy STOCK does not.** That asymmetry is the
   anchor the synthetic world must encode, not a fact the synthetic world may "discover".
3. **What v1.1 must add to the generator (declared, not fitted):**
   - **Education → X with a lag.** The complexity index `X_{c,t}` must accumulate from the *schooling flow*
     (recent completion/attainment increments, lag ~5–10 years), not from the literacy stock level. v1 as delivered
     has **no education → X channel at all** — its `X` is a deterministic function of income, urbanisation and a
     country offset (`x_income_coef`, `x_urban_coef`, `xoff`); schooling supply responds to `X`, and `X` opens
     rungs, but nothing feeds education *into* `X`. That is the gap.
   - **Keep the two-way structure:** `X` opens occupational rungs (`x_open`) and raises rung demand (already in v1);
     education now also raises `X` (new). The user's model is a feedback loop, not a one-way ladder.
   - **Declared functional form and parameters** (e.g. a declared elasticity of `ΔX` on lagged flow increments),
     frozen in a v1.1 predeclaration before the run. The only observed anchors permitted are the association
     estimates above, labelled as observed/derived associations — **not** causal effects.
   - **Literacy's role stays as in the directive**: a takeoff condition (prerequisite for the first industrial
     step), not a general growth engine — and check B (below) currently fails in exactly this respect.
4. **v1.1 checks (to be frozen before the run), replacing/adding to A–F:** an education → `X` association is
   positive with a 5–10-year lag in the synthetic world; the literacy stock is weak as a predictor of `X` while the
   flow is strong (the asymmetry); plus the existing E/F accounting gates retained, D re-tested in a powered
   specification, and B re-specified so the literacy association is located in the takeoff transition.

Why this amendment is needed: as delivered, v1's complexity channel is one-directional (income/urbanisation → X →
rungs/education), so the user's mechanism cannot appear. The fix is a declared model change with new predeclared
checks — **not** a post-hoc re-fit of v1 (see `FINDINGS.md` §4).

### What v1.1 must also change (recorded 2026-11-20 after the authoritative v1 delivery)

1. **Remove the per-level PHL anchor interpolation.** v1's check A passes *by construction*: the PHL-like country's
   four supply paths are interpolated through the declared PHL-01/02/03 anchors, so "one parameterisation, no
   per-level rescue" is not tested. v1.1 must carry either one declared supply parameterisation for all countries or
   an explicitly enumerated set of declared country types, and must re-score A honestly (expect it to fail unless the
   mechanism genuinely produces the dates).
2. **Adopt the ablation rule.** A synthetic horse-race PASS (check B) is **non-diagnostic unless the ablation
   fails**: in v1 the literacy association survives both the takeoff ablation (+2.37 → +2.29) and the full job-ladder
   ablation (→ +2.10), so the pattern is over-determined and carries no information about the mechanism. v1.1's
   check B must pass only if switching off the relevant layer *materially attenuates* the association.
3. **Derive, don't stipulate, the upper-secondary seat cap.** v1's load-bearing object is the stipulated seat cap
   (0.845 → 0.875 of the cohort); put the ceiling on the floor's growth path and the anchor asymmetry vanishes. v1.1
   must model who hires upper-secondary completers (demand side) and derive capacity from that, or label the
   asymmetry result as an assumption rather than a reproduction.
4. **Carry the completion/GER denominator note** (`facts/STYLIZED_FACTS.md` §12; `10_massification/data/
   DATA_NOTES_MASSIFICATION.md`): a cohort-flow model cannot produce completion > GER, so any completion-based
   target must declare its denominator; do not fit completion up to observed levels.

---

## Amendment A2 (user directive, 2026-11-20, dashboard) — demographic overflow, quality collapse, and the child-labour block (v1.2)

**Status: design directive. Not implemented. A v1.2 predeclaration must be frozen before any v1.2 run**
(`v1_2/PRE_DECLARATIONS.md` is that frozen spec).

### The user's reading, restated

The Philippine story is **not a "seats" story in the abstract**: a **baby boom moved through the school-age
population**, and schools and teachers were **not built fast enough** — seats overflowed, and **quality collapsed**
(congestion, high pupil–teacher ratios, double shifts, overcrowded classrooms). The **out-of-school block should be
borrowed from the Atlas `childworld` model** ("unless it's broken"), with the default assumption: **if a child is not
in school, that child is in child labour/work**, and **families compete for school places**. This demographic/quality
layer is the missing piece: it is what turns a cohort surge into a completion ceiling and a learning collapse.

### What is borrowed, and from where

| element | source | sha256 | what we take |
|---|---|---|---|
| four-state household block (`school` / `both` / `work` / `neither`) and the household utility decision | `engine/childworld.py` at parent-repo HEAD (retrieved read-only: `git -C /Users/treymenefee/massification_live show HEAD:engine/childworld.py`) | `ae73adb2a6d9c75d59966390e4304437479ff310a8724093e9108e9d26a23cab` | the **state structure, choice logic and parameter names** — `y_med` household income, `w_child` child wage, `farm`, `compat` work–school compatibility, `v0`/`decay` schooling value, `cost`, `neither`, `girl_care`, `haz` hazardous share |
| Monte-Carlo/ABC wrapper, age-aligned variant, Sobol sensitivity | `engine/childworld_mc.py` (`944d1040…`), `childworld_agealigned.py`, `childworld_sobol.py` | per `MODEL_INVENTORY.md` rows #6–#7 | only the *design pattern* (parameter draws, composition tests); **not** any posterior or calibrated value |

**Borrow caveats (from the programme's own review — these travel with the code):** `MODEL_INVENTORY.md` row #6 says
childworld was **"Not run in this audit (only inspected)"**, that its **observation equation is not the ILO child-labour
definition**, and that its **values are stylised**; row #7 says **v1 failed the India composition test** and that the
**baseline "neither" share (0.421) was flagged for validation**. Therefore:

1. **Borrow the structure, not the values.** Every borrowed element is labelled **`BORROWED-FROM-ATLAS / structural`**
   in `PARAMS.md` and in the code header, with the source file and sha256 above. No childworld prior, posterior,
   country target or output number is imported as a parameter.
2. **No passive "neither" residual** (user directive). The four states are retained for the decision logic, but
   **out-of-school children default to work/child labour**; "neither" is allowed only as a **declared, bounded option**
   (domestic care, disability, inaccessible school) whose share is reported, not a free sink to absorb any out-of-school
   residual.
3. **State every deviation** from childworld in `v1_2/PRE_DECLARATIONS.md` (observation measure, child-labour
   definition, rationing rule, cohort/year structure).

### What v1.2 adds (the layer v1 lacks)

- **Layer 1b — demographics as a declared input.** The observed PHL cohort path (`UNIVERSALIZATION_SERIES.csv`
  `cohort_population_0_14` / `population_total`, the baby-boom shape) enters as a **declared input, not fitted**. Other
  synthetic countries get declared cohort paths (boom / flat / decline) so the mechanism can be seen to matter.
- **Layer 1c — capacity built with a lag, and quality as an output.** Seats and teachers are built with a lag from
  declared PHL expansion series (`10_massification/data/SCHOOL_EXPANSION.csv` PTR/hires,
  `10_massification/data/STATE_CAPACITY.csv` delivery). **Congestion/quality = f(cohort/seat ratio, PTR, class size)**
  and it feeds **completion, learning and dropout**, not just intake. This is the piece that makes a boom produce a
  ceiling rather than a transient queue.
- **Layer 2b — household four-state block with rationing.** State chosen by the borrowed decision logic; **families
  compete for limited seats** — when qualified demand exceeds seats the surplus is **rationed by a declared rule**, and
  the rationed child is out of school and defaults to work. Child wage, work–school compatibility, schooling value and
  decay, and school cost are declared parameters (drawn from the childworld parameter *names*, with our own declared
  ranges).
- **Layer 3 — unchanged growth/composition logic**, plus the Amendment-A1 **education → complexity** channel.

### v1.2 predeclared checks (frozen in `v1_2/PRE_DECLARATIONS.md`; see that file for exact thresholds)

(a) the PHL ceiling/asymmetry can be produced by **cohort surge + seat lag + quality collapse** with **no per-level
anchor interpolation** (the "one parameterisation" clause v1 failed); (b) out-of-school / child-labour shares are
plausible and **responsive to cohort size**; (c) PTR/congestion **rises during the boom then falls**; (d) identity:
no completion > GER beyond the disclosed UIS 3–5-years-above-grade denominator; (e) the **education → complexity**
channel (A1) is still present and positive with a 5–10-year lag.

**No post-hoc rescue parameters.** If the mechanism cannot produce the asymmetry without per-level anchors, that is
the finding — the asymmetry then has to be attributed to the stipulated capacity path, not to a reproduction.

---

## Amendment A3 (user directive, 2026-11-20, dashboard) — education DEMAND signals, their interaction with the wider economy, and the shadow block at the gates

**Status: design directive. Not implemented. Requires a frozen predeclaration before any run.** The shadow-education
part is specified in `shadow_module/SHADOW_MODULE.md` + `shadow_module/PRE_DECLARATIONS.md` (frozen by the W2 worker);
this amendment fixes the demand-signal architecture it plugs into.

### The gap this closes

v1/v1.2 model **supply** (cohort flows) and **capacity** (seats/teachers/quality) and carry a household block, but the
**demand side is implicit and the economy interaction is under-modelled**. The user's directive is to model
*education demand signals and their interaction with the wider economy* accurately: what makes a family demand the next
level or a credential; what makes tutoring worth buying; and why the same schooling is worth different amounts in
different economies. The programme has already measured the PHL symptoms — flat graduate wages, 39% overeducation,
1-in-5 vertical mismatch, BPO absorption ~80k/yr against a much larger graduate flow — but has not *modelled the
signals* behind them.

### The declared demand-signal block (Layer 2c)

**Household demand for level `L` in country `c`, year `t`** is a declared function of:

1. **Expected net return to the credential**, `E[R_{L,c,t}] = P(advance_{L,c,t}) × (w_formal(L)_{c,t} − w_informal_{c,t}) × H × access − cost(L) − foregone earnings`,
   where `H` is a declared horizon/discount factor, `access` is a declared network/eligibility term (education–job
   credential alignment, as in the PIDS evidence on licence premia only when matched), and `cost` is declared fees +
   opportunity cost.
2. **Gate probability** `P(advance_L)` — the probability of actually being admitted/promoted at the gate: a declared
   logistic/rationing function of **seats vs qualified demand**, queue length, and credential rank. This is the object
   shadow education buys.
3. **Sector structure and the job ladder** — rung demand `J_r` (from `X`, sector mix and the twins' office/mfg bias)
   determines which credentials have a destination. This is the mechanism behind "the same schooling has different
   value in different economies" (Caselli–Coleman skill-biased technology; the programme's own twins).
4. **Migration and remittances** — a **declared** channel: a destination-wage differential × declared migration
   probability raises `E[R_L]` for exportable credentials (nursing, IT, care), and remittance income raises household
   liquidity (and may finance tutoring). **LABEL: DECLARED / NOT-VERIFIED — `10_massification/lit/PUSH_PULL.md`
   records that the remittance→schooling coefficient is NOT VERIFIED (Clemens/Yang not retrievable); no literature
   coefficient may be inserted.** The channel is a declared behavioural assumption to be tested, not an estimated
   relationship.
5. **Family income / liquidity** — the four-state household block's `y_med` distribution; liquidity constraints can
   block a positive expected return (declared).
6. **Shadow education (v1.3, from W2)** — tutoring demand `D_shadow = f(gate pressure, expected returns, family income)`;
   tutoring raises `P(advance)` and/or credential rank; **near-zero at primary**; HKG-high / PHL-mid / KHM-low
   ordering as a declared check. Shadow is a **signal of gate pressure**, not a generic add-on.

### Feedback loop (the "interaction with the wider economy")

study demand → enrolment/flow → **gate pressure** (queue/rationing) → return expectations and shadow demand →
credential composition of graduates → **rung matching** (absorption) → wages/queues → next period's expectations.
Simultaneously, schooling flow raises `X` with a lag (Amendment A1) and `X` opens rungs and shapes sector mix; the
ladder governs the marginal return (v1 check D) while gate pressure governs the shadow/horse-race margin.

### Predeclared checks for A3 (frozen in the v1.3 predeclaration; thresholds to be stated before any run)

- **d1.** Household demand for the next level responds **positively** to expected returns (declared sign).
- **d2.** Demand responds **positively** to gate pressure/queue length at the gate (the horse-race margin).
- **d3.** **Sector-mix heterogeneity**: the same graduate flow yields different demand and different returns in the
  manufacturing-biased vs office-biased twin (composition > totals, extended to demand).
- **d4.** **Migration/remittance channel present and labelled**: an export-credential premium is visible when the
  declared migration probability is on, and is switched off under the declared counterfactual — reported, not claimed.
- **d5.** **Shadow demand near-zero at primary**, positive and pressure-increasing at secondary/tertiary gates (W2's
  checks c1–c5), and the HKG/PHL/KHM ordering check (HKG 85% is a **second-hand, upper-secondary-only, upper-bound
  target** — `02_lit/COUNTRY_CARDS/HKG.md:15,19,38` — not a system-wide rate).
- **d6.** Accounting/identity gates retained (shares in [0,1], non-negative demand, cohort conservation).

**No causal or direction claim is licensed.** All demand equations are **declared behavioural assumptions**; the checks
ask whether the declared model *reproduces the predeclared patterns*, not whether any family or country behaves this
way.

---

## Amendment A4 (Council-merged theory frame, 2026-11-20, cycle 12) — DECLARED-THEORY: scaffold, induction, exit cost, shadow at the gates

**Status: DECLARED-THEORY. Theory-only; NOT evidence; NO parameters; NO new layer. Gated.** Source of record:
`08_council/brief_020/THEORY_FRAME.md` (combined frame from the two PI working papers: hysteresis paper — brief 019;
assembly paper — brief 020), admitted by Council decisions D102–D105. Both papers are **candidate theory**, never
authority and never evidence (D49: no citation of unread material; their reference lists do not enter the verified
ledger).

### The frame in one paragraph (as adopted)

Mass schooling is a **scaffold** whose forward adoption is a local gain (literacy unlocks the first industrial step;
credentials give employers a cheap screen), but whose installation **transforms the state** from which exit must later be
attempted — complementary capital, cohort demography, institutional rules and the distribution of competence all
reorganize around it (Assembly: induced competence §3.2; hysteresis: exit-cost state transformation C_M/C_D/C_E/C_K,
not a sunk cost). What the scaffold installs into persons is **induced competence** — literacy, numeracy and
schedule-discipline assembled *within development* on a conserved architecture by repeated exposure, with no ancestral
counterpart as a coordinated whole. The two papers meet at the **educational credential**: an induced competence whose
exit is asymmetric (it persists after its value decays because employers screen, applicants acquire, schools expand and
regulators gate). The programme's own anchor — the PHL system whose floor and middle crossed 90 but whose upper-secondary
ceiling never did — is read as the junction: **induction at the floor, exit cost at the ceiling.**

### How the frame maps onto the model (no code change is licensed by this amendment)

| frame element | where it already lives | status |
|---|---|---|
| literacy = takeoff prerequisite | `MODEL_ARCHITECTURE.md` Amendment A1 (v1.2 Layer 1c/2b) | declared assumption; **candidate grounding — PARKED per D104 (DT1 null); no theory citation** |
| school formats persons (schedule-discipline, numeracy) | A3 household block (school/both/work/neither) | declared assumption; **candidate grounding — PARKED per D104 (DT1 null); no theory citation** — not encoded as an "induction" parameter |
| demographic overflow → quality collapse | v1.2 (Amendment A2; `generator_v1_2/`) | declared synthetic mechanism, now being tested |
| shadow education = niche expansion at the gates | `shadow_module/` (Amendment A3 + W2 frozen predeclaration) | declared design; not yet built/run |
| credential = junction (competence + asymmetric exit) | WT2/WT4/DT5 tests (descriptive) | test slate, not a model parameter |
| exit cost / complementarity → persistence | WT3; conditional gate | **no layer until WT1 AND WT3 both non-null** |

### Binding gates (from D101 and D104)

1. **Exit-cost / complementarity layer:** may be added ONLY if **WT1 AND WT3 both return non-null**; then only as a
   **declared** (never fitted) term, tested by the D81 ablation rule (a synthetic persistence PASS is non-diagnostic
   unless the ablation fails). If either is null, the exit-cost layer is **PARKED** and the hysteresis paper is cited
   only as a scored rival with no empirical footprint.
2. **Induction naming:** the generator may *name* the induction mechanism in its declared-assumption provenance ONLY if
   **DT1 AND DT2 both return non-null**. If either is null, the induction grounding is **PARKED** and Amendments A1/A3
   keep their current "declared" label with no theory citation.
3. Any model change under (1) or (2) requires its own frozen predeclaration before the run, and must remain
   **DECLARED-ASSUMPTION**, never fitted, never called evidence.

### What is explicitly NOT encoded (and must never be claimed)

Release (ancestral-reference) claims; the extended developmental window as administered input; the tracker/physicist
agency ranking; genetic-sameness transplant/migration designs; relational self-domestication ("niche-specified phenotype
share" has no on-disk proxy); assembly §8 Predictions 1/3/4; hysteresis Predictions 2/3; and every micro citation the
papers marshal. **Neither paper is falsification-tested by this programme**; the reachable disconfirmers (assembly §8
#2/#5, hysteresis high-switching-cost corollary) are descriptive only (D105). No causal or direction claim is licensed.

---

## Amendment A5 (user directive, 2026-11-20, dashboard — second structural point) — BIMODAL-GATE: two-tier gates, untaken free seats, and tier-specific exit cost

**Status: design directive (first-class model requirement). A v1.5 predeclaration must be frozen before any run.**
This supersedes the single-gate framing of A3-D's successor experiment (`v1.4 BINDING-GATE`): the user's point is that
the Philippine pattern is **bimodal within the same system**, not one scarce gate.

### The user's structural point (recorded)

Low-cost, if not free, seats go **untaken** by families choosing out of education at upper-secondary (and starting at
lower-secondary — some primary, though primary is basically universalised) — **at the same time as extreme competition
at the gates**. That coexistence is the interesting object. The correct label for the A3-D result is therefore **"the
unrationed single-gate model cannot represent a bimodal system"** — a **model-specification failure**, never "demand
falsified". Demand is revealed and strong (shadow education, queues for good schools, parental reaction to closures,
credential chasing).

### The two-tier structure (v1.5)

1. **Tier O — open-access, low-cost/low-quality seats** that can go **unfilled**. Near-zero private cost; low quality
   and low return; take-up is an **equilibrium** between quality, opportunity cost and the option value of work.
2. **Tier H — rationed high-quality gates**: good SHS tracks, university slots, credentialed jobs. Capacity-constrained
   **places/slots** with queues, rank, exam/credential rationing and **shadow competition**. `P(advance) < 1` by
   construction, so demand pressure has something to press against.
3. **Explicit outside option**: work / child labour / informal / migration — reuse the v1.2 childworld four-state
   block (`school`/`both`/`work`/`neither`; out-of-school defaults to work; no passive "neither" sink). The outside
   option is why free seats can sit empty while elites queue: the low tier's return can be below the option value of work.
4. **Sorting**: families sort by income / ability / taste into (i) high-gate competition (returns high, costs and risk
   high), (ii) low-tier seats (cheap, low return, can be declined), or (iii) out of school. Returns differ by tier.
5. **Tier-specific exit cost (theory refinement for the Council, WT-adjacent):** exiting the **low-quality open seat is
   cheap — and people do it**; exiting the **credential gate is expensive — and nobody does**. This is more testable
   than "exit cost" as a single quantity. The Council is asked to consider a WT-adjacent test with the same
   no-direction-claim discipline; it is **not** a re-opening of D101 (no exit-cost layer until WT1 ∧ WT3).

### Predeclared checks for v1.5 (freeze before run; report mixed/negative honestly)

- **(a) Bimodality in one system:** simultaneous **untaken low-cost seats** AND **excess demand/queues at the high
  gates** in the same synthetic country-year (declared thresholds in the v1.5 predeclaration, e.g. an unfilled-seat
  share above a declared floor while the high-gate queue/acceptance ratio exceeds a declared bar).
- **(b) Level pattern:** primary near-universal while upper-secondary **stalls** (the v1.2/v1.3 PHL signature bands).
- **(c) Shadow placement:** shadow demand **concentrated at the high gates**, low at the open tier.
- **(d) Ceiling from sorting/quality/outside-option with NO free taste parameter** — the declared work-incentive weight
  removed; ceiling must emerge from the tier structure. Mixed/negative reported as such; **no rescue, no fitting to the
  known PHL outcome**.
- **(e) No-re-fit guard:** with the new bimodal block **off**, v1.5 must reproduce the current generator panel
  byte-for-byte (the v1.3/v1.4 guard convention).

### Data

**HELD DATA ASK (do not fabricate):** true seat utilisation / quality is **not on disk** — DepEd/CHED seats vs
enrolment, private/public shares, SHS voucher take-up, by track/region. Until granted, v1.5 may use **declared proxies**
already on disk — enrolment vs cohort, PTR/capacity (`STATE_CAPACITY.csv`, `SCHOOL_EXPANSION.csv`), private share
(`SE.PRM.PRIV.ZS`, `SE.SEC.PRIV.ZS`) — each labelled **DERIVED** and each with its distortion stated. **Never invent a
utilisation number or a quality series.**

### Prohibitions

No "demand falsified" language anywhere. No re-tune of A3-D. No fitted demand/quality parameter (R4/R27). No causal or
direction claim. No C1–C4 reopening. HELD data stays HELD. The tier structure and the outside-option parameters are
**declared assumptions**, tested by ablation, never called evidence.

### A4 addendum (user macro-principle, 2026-11-20, dashboard) — THE ONE-WAY RATCHET ("no reverse button")

**Status: DECLARED-THEORY (theory-only, never evidence). No parameters; no layer.** The user's formulation is recorded
in `THEORY_FRAME.md` §1 and D125: on the development/industrialisation path **nobody ever says "go back"**; shocks
produce **setbacks, not reversal to the prior configuration**; the options are **path-created** (build wafer fabs vs keep
exporting labour, not "return to the prior state"); a Polanyi-like one-way transformation, stronger — the double
movement happens *inside* the installed state. The illustrative examples (Manila→hill tribe) are thought experiments and
must **not** be modelled literally.

**Model requirement (declared, not fitted):** the generator carries a **declared one-way ratchet** —
- **no reverse/reversal term** anywhere in the transition rules;
- shocks enter only as **declared inputs** and may move **levels** (setbacks), never reverse the **path**;
- the option set is **path-created** (available choices depend on prior installation).
This is **stronger than the hysteresis paper's exit-cost asymmetry** — **exit cost is *why* the ratchet holds**. It is
consistent with both papers (scaffold adoption → no exit; schooling installs competences → options change). The v1.5
BIMODAL-GATE spec must not imply reversibility.

**Honesty bound:** our data show **setbacks without reversal** (PHL upper-secondary 2017→2022 −8.16 pp, recovery to
75.03, never ≥90; WT4 zero sustained exit episodes, descriptive and fragile) — a **bounded observable implication, NOT
a test of the strong claim**. The strong claim ("nobody ever goes back") is **untestable on our data**; no reversal
diagnostic may be proposed as if reachable; any future one must be predeclared and labelled **descriptive**.

### A5 addendum (cycle-14 integration + user macro-principle, 2026-11-20)

1. **Precondition from D121/V2 (the generator cannot hold a pipeline):** v1.5 must also satisfy the **declared cross-level
   accounting link** `upper_t ≤ κ · lower_{t−3}` with **κ declared from an observed median (never fitted)** — v1.2's
   synthetic ratio exceeds 1.10 in 12 anchor-type years (max 1.444) while the observed PHL maximum is 1.072. The bimodal
   tier structure is built **on top of** that link, not instead of it.
2. **The high gate includes the job rung, not only the school gate (cycle-14 V8):** the model's binding queue is
   **rung-4 absorption** (`rung4_emp/rung4_demand` ≈ 0.151 for the PHL-like type), not the school-gate advance probability
   (≈0.999). Tier H must therefore carry both the **rationed school gate** (good SHS tracks/university slots) **and** the
   **credentialed-job rung**, as the theory frame's "credential gate" specifies.
3. **One-way ratchet (D125):** v1.5 transition rules carry **no reverse/reversal term**; shocks enter only as **declared
   inputs** and may set back levels, never reverse the path. The spec must state this explicitly and test it only by
   construction (no reversal term present), not by a reversal diagnostic the data cannot support.
4. **v1.2 validity-scope disclosure (D119) applies to every layer built on it:** v1.2 is **crossing/endpoint placement,
   not a path** (within ±5 pp of the observed PHL series in 9/33 year-level comparisons; median lower −29.44, upper
   −27.59 pp; 24–37 pp low before 2021). Any v1.5 statement inheriting v1.2 levels inherits that scope.
5. **No "demand falsified" language** anywhere; correct label = "the unrationed single-gate model cannot represent a
   bimodal system". No re-tune of A3-D; no fitting to the known PHL outcome.
