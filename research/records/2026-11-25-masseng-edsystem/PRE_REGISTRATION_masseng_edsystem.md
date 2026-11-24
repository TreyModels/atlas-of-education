# PRE-REGISTRATION — full-system behavioural prototype + multiverse over equation choices (eduengine)

**Committed BEFORE code and BEFORE any run.** SIMULATION ONLY on the existing `eduengine` toy worlds
(no country fit, no causal claims, no empirical validation). The engine is NOT rewritten: the four
connected pieces are already present in `engine/eduengine/` and are wired by choosing their existing
switches/parameters:

1. **Family affordability incl. forgone earnings.** `Engine.anchored_choice` / `step` compute the
   per-year cash available (`income − subsistence + borrow·income + CCT`), the required outlay
   (`fees + need_frac(income)·child_wage(age)` = direct cost + forgone child earnings replacement),
   and exit children for whom `need > cash` (liquidity, `reason=1`) or who choose to stop (`reason=0`).
   Equation choices: cash-only (no borrowing, constant replacement share), credit with constant
   replacement share, credit with a poverty-line (logistic) replacement share.
2. **Learning / school quality.** Quality comes from PublicSchools (teacher pay/monitoring/budget/
   class-size), PrivateSchools entry, and TutoringMarket (tutoring gain). Equation choices: public
   only; public+private; public+private+tutoring. (The engine's learning production is held fixed;
   the multiverse varies which quality/supply channels exist, not the core learning equation.)
3. **Limited-place gates at levels.** Bar versus quota gates at the four level transitions
   (`gates`), with limited places enforced by the engine's gate pass probabilities and cash-first
   affordability.
4. **Credential → labour outcomes.** QueueLabour (credential floors, queueing) versus
   CompetitiveLabour (price-taking returns), with the engine's existing credential floors.
5. **Rural/urban structure.** Low vs high rural distance cost + urban share (the only rural/urban
   representation in the engine: rural children pay `rural_cost` beyond primary; no migration, no
   sorting, no remittances — those are declared missing, not invented).

**Multiverse (bounded, declared before runs).** One choice per axis, full cross-product:
- affordability ∈ {cash_only, credit_constant, credit_poverty} (3)
- supply/funding ∈ {fixed_budget, fiscal_loop} (2)
- learning/supply configuration ∈ {public_only, plus_private, plus_private_tutoring} (3)
- gates ∈ {bar, quota} (2)
- credential→jobs ∈ {queue_floors, competitive} (2)
- rural/urban ∈ {low_penalty, high_penalty} (2)
= **144 combinations × 10 seeds (0–9) = 1,440 runs**, N=400 children/cohort, T=70 years,
measure_from=35, base world `formal_loop` (fiscal-capable), other parameters at the world defaults.
This is a bounded grid of **equation/mechanism choices**, not a parameter sweep; every level is
illustrative.

**Outcomes (per run; all seed-level).** Attainment: `completion_primary`, `completion_lower`,
`completion_upper`, `completion_tertiary`; wealth-quintile arrays `completion_*_q`, top-minus-bottom
gaps; `parity_location_lower/upper`, `parity_wealth_lower/upper`. Push-out decomposition from the
engine's child states: liquidity exits (`reason=1`), choice exits (`reason=0`), never-started
(`reason=4`), share of started, by wealth quintile and urban/rural. Tutoring: `tut_rate`,
`tut_by_q` (quintile), `tut_by_grade` (grades 1–16); gate-adjacent grades (6, 9, 12) vs non-gate
(4, 7, 10, 13); level shares: primary (grades 1–6), lower (7–9), upper (10–12), tertiary (13–16);
where tutoring piles up = share of grade-level tutoring at each level and gate-adjacent vs not.
Labour/quality: `formal_share_gdp`, `q_pub`, `mpl_primary`, `edu_gdp`.

**Pre-declared analysis.**
1. For every outcome, one-way η² (between-variant variance / total variance) for each axis; report
   the ranked movers by outcome and by stage. This says which equation choices move attainment /
   inequality / tutoring at which stage; it is a variance decomposition, not a causal effect.
2. **Non-identification rule:** an axis is *not distinguished* by an outcome if the 5–95 % outcome
   ranges of its variants overlap by ≥ 80 % of the union range; report such cases as "not
   identifiable from this outcome". Also report pairwise overlap for gate vs affordability and
   jobs vs learning axes.
3. Group tables for the baseline and for the extreme variants: who is pushed out (liquidity vs
   choice vs never) by wealth quintile and rural/urban; who buys prep and spends by quintile;
   where tutoring piles up by level and gate-adjacency.
4. **PHL coupling attempt (not calibration):** compare the simulated lower-secondary completion
   distribution with the committed PHL UIS/WDI `lsc` observation (same variable label only);
   report the gap and explicitly list incompatible constructs (GER/attainment vs completion;
   migration; rural-urban sorting; remittances; no country-specific fit). The Bray 2M fit (95/2M,
   best max-z 0.432, wide accepted ranges) is a simulation fit, not identification, and is not used
   to validate anything here.
5. Seed-level uncertainty: mean and 90 % interval across 10 seeds for every reported cell; no
   p-values; no causal language; every parameter illustrative.

**Missing mechanisms, stated not invented:** migration/emigration; rural–urban sorting and
residential choice; remittances and kin transfers; informal/formal employment composition beyond
the queue/competitive switch; teacher labour supply outside the engine's pay/monitoring channel;
country-specific calibration. Any comparison to PHL is a construct-limited level check.

**Execution:** server `ssh -p 45973 root@connect.cqa1.seetacloud.com` (key only, do not shut down),
`/root/miniconda3/bin/python`, ≤ 12 workers (shared 15-core quota); all compute on the server; fresh
output files only; code/engine hashes, commands, logs and seeds preserved; results committed to
`research/masseng-edsystem-2026-11-25`. Stop rules: engine import/shape failure or >2 % non-finite
metrics → stop and report traceback; no silent retries.

**Deviations log:** (to be filled before any affected run)
