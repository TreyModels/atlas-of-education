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
