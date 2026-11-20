# PRE-DECLARATIONS — Loop 8: relations→model wiring, re-run of the synthetic frontier

**EVERYTHING IS SYNTHETIC / POSSIBILITY-ONLY.** Authorised follow-on (task B); the programme stays
**CLOSED** — this does not reopen any closed claim, does not re-fit closed targets, and is not evidence.
Brief-008 identification limits stand. Relation-slot claims PENDING. Written BEFORE any loop-8 run.

Reuse: `05b_experiments/loop6/code/synth.py` (generator), `loop6/code/relation_arms.py` (eps_ec and
two-margin arms), `loop7/code/family_map.py`; `09_relations/{RELATION_CANDIDATES.csv, MODEL_PLUG_MAP.md}`;
`08_council/brief_009/`; `02_lit/SHADOW_TARGETS.csv` targets.

## Wiring (declared; graded relations become PARAMETER DISTRIBUTIONS, never point fits)

| Relation | Estimate (graded; from RELATION_CANDIDATES) | Wired into (loop-6 model object) | Declared distribution |
|---|---|---|---|
| R01 spending→secondary GER | 0.111 world (Asia 0.189; low-GER 0.132; non-Asia 0.010 ns) — correlational | twoway completion logit: `s_t` intercept += b01·log(spend_ratio), lag 5y; spend_ratio~U[0.8,1.6] | b01 ~ Triangular(0.010, 0.111, 0.189) |
| R04 income→tertiary GER | 0.848 world (Asia 1.075; non-Asia 0.281 ns) — correlational | twoway college-entry: `c0_eff = c0·(income_ratio)^b04` | b04 ~ Triangular(0.281, 0.848, 1.075) |
| R07 fertility→primary completion | −0.189 (se 0.044) — plausibly causal (resource dilution) | twoway completion: `s0_eff = s0·(births_ratio)^(−b07)`; births_ratio~[0.6,1.3] relative to 2.0 | b07 ~ Triangular(0.10, 0.189, 0.30) |
| R13 education→growth (`eps_ec`) | **−1.035 (se 0.240, p<0.001); no subgroup positive** — not identifiable as causal, but rejects the model's eps_ec>0 prior | twoway `REGIMES[*]['eps_ec']`, `d_ec` | eps_ec ~ Triangular(−1.035, 0.0, 0.6) (mode at 0; positive arm not assumed); explicit arm eps_ec ∈ {−1.035, 0, 0.3, 0.6} |
| R21 gate proximity→tutoring | HK 2003 +35.2pp S1-3→S6-7; prior 0.7/0.8 — correlational | shadow demand: stakes concentrated toward terminal stage `stakes_eff(s) = stakes(s)·(1+b21·(prox(s)−0.5))`, `prox=s/(n−1)` | b21 ~ U[0.4, 1.0] (around prior 0.7/0.8) |
| R22 income elasticity of tutoring spend | 1.33 spend elasticity (Korea bands); participation elasticity lower — correlational | shadow demand income term: `B_INC_eff = 0.55·b22`, and income-gradient spend computed with it | b22 ~ Triangular(0.6, 1.0, 1.3) |
| R23 two-margin (extensive × intensive) | participation 86.0→66.4 (−19.6pp) while spend/student +23% — correlational | stage intensity multiplier `fee_mult_eff(s) = fee_mult(s)·(1 + b23·(prox(s)−0.5))` (adds an intensity/spend margin alongside the participation margin) | b23 ~ U[0.10, 0.60] |
| R24 urban→tutoring | JPN 2.62×, KHM 2.29× — correlational | shadow demand location term: `urban_mult_eff = base_urban_mult·(r24/2.0)` | r24 ~ Triangular(2.29, 2.29, 2.62); urban_mult floor 1.2 |
| R29 tutoring price elasticity | NOT IDENTIFIED; twoway prior −1.1 — declared prior | shadow demand price coefficient | B_FEE_eff ~ U[0.5, 2.0] (around prior 1.1) |
| R41–R49 ECI/complexity | correlational / methodological; **ECI data PENDING** (`04_data/complexity/` absent) | — | **PENDING: not wired, no imputation; CX-type direction rows remain unscoreable and are carried from loop 7** |

Unchanged and declared: R02/R03/R05/R06/R08–R12/R14–R20/R25–R28/R30–R40 are **not** wired (unidentified or
out of the scored margin); they stay declared priors. The demand-level intercept stays the fixed structural
constant **A0 = −1.5** for every draw (no relation supplies it) — recorded in advance as the known blocker.

## Sampling design (same as loop 6, extended)

Latin hypercube, **256 draws × 5 matched seeds**, same seed base (20261120 / 10,000+draw·10+seed) and same
target set as loop 6. Extended parameter vector (17): arch, stakes_scale, pub, income, returns_scale,
cost_mult, teacher_cap, delta, fee_mult_scale, eps_ec, b01, b04, b07, b21, b22, b23, r24, B_FEE_scale
(+ births_ratio). Within-draw seed sd = sampling noise; across-draw spread = parameter uncertainty.

## Estimand and decision rule (declared before running)

- **Primary estimand:** per-target fraction of draws inside the observed range, inside/256, loop-6-before vs
  loop-8-after (before values from `loop6/runs/frontier.csv`; same targets and tolerances).
- **"Frontier shrink" (predeclared):** a target with **0/256 in loop 6 becomes ≥1/256 in loop 8** with the
  same predeclared target band and no fitting. Primary shrink candidates named in advance: **KOR stage
  gradient** and **HKG stage gradient** (both 0/256 in loop 6). Also reported per-target deltas for all 8
  loop-6 targets.
- **Empty-support persists** if both KOR and HKG stage gradients remain 0/256. Report plainly either way.
- **eps_ec arm (R13):** run eps_ec ∈ {−1.035, 0, 0.3, 0.6} (synthetic outcomes; panel estimate is negative,
  so the positive arm is run against it, never assumed).
- **KOR two-margin arm (R23):** joint test — participation falling 86/75.4/66.4 (±5 pp) AND intensity margin
  ≥ +15% stage spend rise; report joint/participation-only/intensity-only/neither counts over 256 draws.
- **No tuning:** wiring, distributions and decision rule fixed here; if the frontier does not shrink, say so.
- Failures logged; no threshold changed after seeing results. Everything SYNTHETIC/POSSIBILITY; no
  validation language; no closed claim reopened.
