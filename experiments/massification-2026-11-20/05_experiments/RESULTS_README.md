# 05_experiments — what was actually run

Owner: experiment-runner. Scope: `05_experiments/` only; `01_sources/` was never edited.
All numbers here are **simulated model output**, not observed country data, unless labelled.

## Package contents

| file | what it is |
|---|---|
| `EXPERIMENTS.md` | one full record per experiment (question, arms, output definitions, result, interpretation, reproduce command) |
| `PRE_DECLARATIONS.md` | written before the runs: question, hypothesis, estimand, arms, controls, seeds, threshold |
| `PRE_DECLARATIONS_E18b_E13c.md` | predeclarations for the two Council-brief-002 follow-up cells |
| `SUMMARY_TABLE.csv` | 14 rows: estimand, arms, effect, uncertainty, verdict, runs, evidence status |
| `RUN_MANIFEST.json` | environment, source hashes, exact commands, per-cell wall times, failures, proposed-but-not-run list |
| `ERROR_LOG.md` | every crash, bug, amendment and budget concession |
| `runs/<EID>/` | runner script, raw + summary CSV, `findings.txt`, `run_meta.json`, README per cell |
| `code/massabm/` | unmodified copy of the October Philippine ABM (sha256 recorded) |
| `code/triad/` | unmodified copy of the three-actor model (sha256 recorded) |
| `code/ext_massabm/` | patched copy: school-support and omega extensions plus the matched-elasticity rival; **defaults identity-tested** against the unmodified copy |
| `code/new/README_EXTENSION.md` | what is new, what is a reproduction, and the declared assumptions |
| `code/exp/` | all runners and checkers |
| `logs/` | Phase-0 environment record, gate results, per-cell logs |

## Status counts

- **Completed: 14 cells** — E0 (Phase-0 gate), E2, E3, E5, E7, E8, E10, E13, E13b, E13c, E14, E15, E18, E18b
  (E13c and E18b are the Council-brief-002 follow-ups; see `PRE_DECLARATIONS_E18b_E13c.md`).
- **Pilot only: 1** — E19+E20 (descriptive/transfer; Hong Kong data blocked).
- **Failed to execute: 0 substantive** — all failures were implementation bugs, fixed and logged; no run was dropped from the record.
- **Proposed, not run: 5** — E4, E9, E11, E16, the cross-cutting recovery study, plus all atlas-engine cells. Never claimed.

## Strongest positive result

**Liquidity binds harder than preferences (E3).** With matched cohorts and seeds, removing access to
credit (a hard cash cutoff) cuts poorest-quintile basic completion from 0.462 to **0.017** and widens
the Q5−Q1 gap from 0.321 to 0.781; expanding credit cuts the gap to 0.090. A temporary income shock
alone costs Q1 5 points, but the same shock without credit costs 46 (Q1 completion 0.001). Nothing in
the model says poor families value schooling less — they stop because they cannot pay.

Also strong: **tutoring follows the discontinuity (E7)**. Take-up is 0.933 at the licensure board and
0.443 at the apex exam versus 0.040 at the basic gate; pushing the basic bar toward the median student
raises basic-gate tutoring from 0.022 to 0.752 while completion falls from 0.718 to 0.287.

## Strongest negative result (now corrected by the fair test E18b)

**An additive, universal, unbudgeted support subsidy is absorbed by the race (E18) — but that is not
the same as Trey's hypothesis failing.** The fair follow-up **E18b** gives support a demand channel and
the substitution appears immediately: paid spend falls to 2,377 with support halving tutoring's
marginal value (**−1,291.5 vs ban-only, 2 seed sd ≈ 92**), to 3,327 when targeted to the bottom two
quintiles (−341.4 vs 2sd 149), and to 2,427 when capacity-capped at 25% (−1,241.2 vs 2sd 101), with
completion *higher* in every arm. **C10 is therefore WITHDRAWN**; E18's negative result is re-scoped to
the additive/universal form. Original E18 numbers for the record: Adding universal,
free school support to the massabm tutoring layer *raises* paid tutoring spend by 18% (4,092 → 4,815)
and nearly doubles the apex gate's share of spend (0.41 → 0.68): support moves more students near a
high-stakes cutoff, where a marginal score gain is worth most. Adding support on top of a commercial-
tutoring ban returns paid spend to the untouched baseline (+429 vs ban-only, 2 seed sd ≈ 107).
Only full enforcement of a ban reduces paid spend (−63%), and it does so by removing the market, not
by substituting school support. The learning guard passes (completion is slightly *higher*), so this
is a demand-rerouting result, not a harm result.

Second negative, aimed at the paper's own claim: **the matched-elasticity rival (E13b) contradicts the
sharp C3 discrimination.** Once the competitive world is given a formal/informal margin, the same
households, the same shock and the same vacancy path, it reproduces zero-or-negative changes in
diploma holders' absolute income at substitution elasticity ≤ 1. What still discriminates cleanly is
the **formal-employment probability**: it falls only in the surplus world (−0.154, −0.168) and never in
the rival. The paper's claim should be restated about formal access, not absolute income.

Two further challenges worth the Council's attention: the floor's own contribution beyond ranked
hiring is at or below seed noise (E8), and the state's fiscal investment does not pay for itself on its
own ledger (−4.10 vs a frozen state at 0, E15).

## What the Council should scrutinise

1. **E13b** — the verdict fires on point estimates; at sigma=0.5 the negative is inside its own seed
   dispersion. The formal-margin estimand is the robust one.
2. **E18** — the school-support mechanism is a declared reduced form (0.5 exam sd, zero price) in a
   model with **no gate-stakes reduction and no COVID/labour-market shock**. It is not a measured
   Double Reduction effect and should not be quoted as one.
3. **E8** — the floor effect is null *under this parameterization*; a different enforcement or vacancy
   response could change it. The stored manuscript numbers have no provenance in `01_sources`, so only
   direction is compared.
4. **E19** — the default (uncalibrated) model misses the manuscript's own targets, especially
   basic→college transition (0.227 vs ~0.70). Any descriptive or policy use needs a calibrated freeze
   first.
5. **E14/E15** — triad cells ran at 3 reps / N=2000, not the model defaults; treat as pilot-strength.
6. **No atlas-engine cell ran** (floorworld, childworld, relfloor*, firms/model.py). They were
   inspected only.
