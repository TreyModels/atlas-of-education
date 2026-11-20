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

Why this amendment is needed: as delivered, v1's checks B and D fail partly because the complexity channel is
one-directional (income/urbanisation → X → rungs/education), so the user's mechanism cannot appear. The fix is a
declared model change with new predeclared checks — **not** a post-hoc re-fit of v1 (see `FINDINGS.md` §4).
