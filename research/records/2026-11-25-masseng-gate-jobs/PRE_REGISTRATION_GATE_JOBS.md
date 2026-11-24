# PRE-REGISTRATION — v6 prototype: score/quota admissions gate + credential→jobs/earnings link

Written **before** the module code and before the toy run (this record is committed before `gate.py`,
`labour.py` and the toy are executed). Additive branch `research/masseng-gate-jobs-2026-11-25`, based on
`research/masseng-tutoring-2026-11-25` @ `b9d68c1`. The v5 engine and the Codex branch are **not** modified.

## Question

MASSENG v5 cannot carry two mechanisms that the full massification agenda needs: (1) a **selection gate** with
exam scores, limited places, quotas and pass rules (v5 entry is probabilistic demand with no score), and (2) a
**credential → job/earnings** link (v5 has no labour market). This task builds both as typed modules for the
**v6 prototype skeleton** (`research/masseng-v6/masseng_v6/`), switches them on/off, and runs a bounded toy
cohort to answer three descriptive questions:

- **Q1 who is pushed out** — admission/rejection by income group and ability, under bar vs quota vs capacity vs
  exam-pass gates;
- **Q2 who buys prep** — who purchases gate preparation, and how the gate rule changes prep demand and spending;
- **Q3 credential flows and pay** — how the gate rules change the final credential mix, formal employment and pay
  by group, under a credential-rationed queue vs a supply-responsive competitive labour market.

Everything is **simulation**; no empirical or causal claim.

## Modules to be built (new files, skeleton untouched)

1. `masseng_v6/education/gate.py` — `ScoreGate` + `apply_gate`: fractional-mass score-based admissions enforcing
   v5-style entry-funnel accounting (`EntryFunnel`, Q ≥ L ≥ E ≥ R from `masseng_v6.core.ledger`). Rules:
   - `capacity`: rank applicants by score, admit down to capacity;
   - `bar`: declared score threshold, then rank down to capacity (bar can bind before capacity);
   - `quota`: a declared share of places reserved for a declared group (bottom income deciles) among those
     meeting a lower quota threshold, the rest admitted by merit;
   - `exam`: a declared random pass probability applied before the capacity/bar rule; failers are the
     "exam-pass" pushout channel.
2. `masseng_v6/labour.py` — credential→jobs/earnings:
   - `QueueLabour`: formal vacancies, credential floors, ranking on a noisy credential+ability signal, fixed
     credential premia, informal fallback, explicit waiting queue over a declared vacancy schedule;
   - `CompetitiveLabour`: same vacancy stock but selection on true skill and wages that clear a declared
     supply-response schedule, so credential premia fall when a credential becomes more common.
3. Toy cohort model (record `scripts/toy_gate_jobs.py`): one synthetic cohort (declared, illustrative
   coefficients), two gates (lower→upper secondary; upper secondary→tertiary), a household prep decision, then
   the labour module. All switches default-off/fixed so the rest is unchanged.

## Declared model (all illustrative, none estimated)

- Population: N = 100,000 pupils per draw; income decile uniform; declared income multipliers (mean 1);
  ability ~ N(0,1); school quality = 0.5·standardised income + N(0,1).
- Gate scores: `score = 1.0·ability + 0.30·standardised income + 0.25·school quality + 0.55·prep + 0.50·noise`.
- Capacities as shares of the cohort: gate 1 (upper secondary) 0.65; gate 2 (tertiary) 0.30.
- Declared bars: gate 1 score ≥ 0.35; gate 2 score ≥ 0.75. Quota: 30% of gate-2 places reserved for the bottom
  30% of income with quota threshold −0.50. Exam pass: 0.80 at gate 2.
- Prep: binary purchase; cost = 2% of mean income / household income multiplier, so the relative cost is higher
  for the poor. Expected-value decision: buy iff `ΔP(admission)·V_credential > prep cost / income`, with
  `V = 0.35` (upper-secondary completion) and `V = 0.80` (tertiary) in mean-income units, `ΔP` from a declared
  logistic admission approximation (`scale = 0.5`) iterated to a fixed point (3 iterations).
- Labour: formal vacancies = 25% of the cohort, arriving 50% / 30% / 20% over three years; queue floor credential
  1 (upper secondary), skilled tier credential 2 (tertiary); queue signal = credential + 0.4·ability + noise;
  queue decision = wait if expected formal-minus-informal gain over the horizon exceeds informal income;
  fixed formal pay `w0·exp(0.06·(years−9))`, informal pay 0.55 × base; competitive regime: selection on true
  skill and `w_c = w0·exp(0.06·(years−9))·(S_ref/S_c)^(1/1.6)`, with S_c the credential's share of the cohort.
- Seeds: 10 independent noise draws (score noise, prep noise, labour signal noise). MASSENG v6 toy is
  stochastic here, so these are genuine Monte Carlo seeds; uncertainty is reported as mean ± sd across seeds.

## Arms (declared, bounded)

| arm | gate 1 | gate 2 | prep | labour |
|---|---|---|---|---|
| baseline | bar 0.35 / cap .65 | bar 0.75 / cap .30 | chosen | queue |
| no gate (open) | capacity 1.0 | capacity 1.0 | chosen | queue |
| gate2 capacity | bar | capacity .30 | chosen | queue |
| gate2 quota .30 | bar | quota .30 / bottom 30% | chosen | queue |
| gate2 quota .15 / .50 | bar | quota .15 / .50 | chosen | queue |
| gate2 exam .80 | bar | exam .80 then capacity | chosen | queue |
| each gate2 rule, prep off | as above | as above | off | queue |
| gate1 quota .30 | quota .30 | bar | chosen | queue |
| gate2 capacity .20 / .40 | bar | capacity .20 / .40 | chosen | queue |
| competitive labour | bar | bar | chosen | competitive |

About 20 arms × 10 seeds = about 200 runs; minutes at most on one core, run with ≤ 8 workers on the shared server.

## Read-outs (fixed before the run)

For each arm × seed: admission rates at each gate (overall; by income quintile; by ability quintile), rejection
mass, prep participation and prep spending share (overall / by income quintile), final credential shares (by
quintile), formal-employment share, queue/waiting fraction, mean pay by credential and by income quintile,
earnings Gini, and the credential premium.

## Decision rules / honesty rules

- **D1 (switch invariant):** with `prep_on=False, gate=('capacity',1.0), labour off`, the pipeline must reduce to
  the skeleton's open-access allocation and the run must be byte-reproducible given the seed. Gate OFF
  (capacity 1.0 everywhere) must admit all eligible mass (`realized == eligible`).
- **D2 (accounting):** every gate result must satisfy the `EntryFunnel` invariant and
  `realized + rejected_eligible == qualified`; the toy must assert conservation (each pupil has exactly one final
  credential and one labour status).
- **D3 (direction, declared):** a hard quota for the bottom group must raise that group's admission share and
  lower the non-quota group's; a bar binding above capacity must admit less than capacity; an exam pass below 1
  must raise the rejection count. If any fails, report the failure rather than tuning it away.
- **D4 (seed uncertainty):** report mean ± sd across 10 seeds for every headline quantity; do not report a single
  draw as a result.
- **D5 (no causal/empirical claims):** all coefficients declared; no country calibration; state non-identification
  explicitly. Migration, rural/urban sorting, country calibration, general-equilibrium wages, teacher supply and
  cohort dynamics are missing and must be listed.

## Stop rules

If a gate rule cannot be implemented without changing the v6 skeleton's accounting invariants, or the toy cannot
be made reproducible, report the failure and stop; do not rewrite the skeleton or fabricate the link.
