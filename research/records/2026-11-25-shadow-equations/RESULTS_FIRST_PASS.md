# First-pass results — shadow-education equation placement (SIMULATION, illustrative)

Run: `python3 run_shadow_scenarios.py --full` — N=20,000 pupils, 10 seeds, 7 scenarios, 1.3 s on the Mac.
Parameters are **illustrative**, not estimates. This is the build Trey asked for: place the equations by
first-order reasoning first, check the literature afterwards.

## What was placed where
- **Household demand** (catalogue 23, 57–70): multinomial logit over none / own-teacher / other-teacher /
  commercial; income and price enter utility; spending share and elasticities are outputs.
- **Learning production** (26, 28, 30–31, 71–76): CES nest of school instruction and tutoring hours, plus a
  SES × tutoring interaction.
- **Admissions gate** (81–82): score bar versus a hard reserved-seat quota (50% of seats contested by the
  bottom 40% by income; the rest by everyone else). The Tullock contest form is deferred.
- **Earnings** (42–43): Mincer equation with an admission/credential shift.
- **Distribution** (123–131): Gini, rich–poor learning and admission gaps, tutoring-participation gap,
  concentration index.
- **Teacher incentives** (176–177): only a ban flag in this pass; effort model deferred.

## Baseline (bar gate, no policy)
| metric | value |
|---|---|
| tutoring participation | 36.8% |
| own-teacher share of pupils | 20.3% |
| learning Gini | 0.568 |
| admission gap, richest vs poorest fifth | +15.6 pp |
| tutoring-participation gap, richest vs poorest fifth | +20.2 pp |
| earnings Gini | 0.182 |
| price elasticity of participation (own fee, ±10%) | −0.33 |

## Scenario changes vs baseline (paired over seeds)
| scenario | participation | own share | learning Gini | admission gap | tutoring gap |
|---|---|---|---|---|---|
| hard quota | 0.0 | 0.0 | 0.0 | **−29.2 pp (flips sign)** | 0.0 |
| own-teacher ban | **−15.6 pp** | **−20.3 pp (to zero)** | **+9.6 pp** | −6.9 pp | −5.6 pp |
| rural access | +1.8 pp | −0.6 pp | −1.1 pp | +0.9 pp | +0.5 pp |
| cash transfer to bottom fifth | +0.6 pp | +0.3 pp | −0.4 pp | −1.3 pp | −2.2 pp |
| quota + ban | −15.6 pp | −20.3 pp | +9.6 pp | −32.8 pp | −5.6 pp |

## First-order reading (to be checked against the literature)
1. **The ban does what a ban does mechanically** — the own-teacher market goes to zero — but it does **not**
   equalise learning: the learning Gini rises by 9.6 points in this model because richer households can still
   buy other/commercial tutoring while poorer ones lose the option. The admission gap narrows only modestly.
2. **A hard quota changes who is admitted, not how much anyone learns.** The admission gap flips from +15.6 to
   −13.6 pp by construction; the learning Gini is unchanged because the quota reallocates seats, not teaching.
   That is a design choice of this first pass (seats are the only rationed good), not a finding.
3. **Cash transfers and rural access are weak levers here.** The transfer moves the bottom quintile's spending a
   little; rural access raises participation slightly but does not narrow the gaps and even widens the admission
   gap a touch. These are the kind of results the literature check should attack first.
4. **The price elasticity is small (−0.33)** because the alternatives are close substitutes in this
   parameterisation; this is an assumption, not an estimate.

## Honest limitations
- All coefficients are illustrative; no calibration, no empirical validation, no causal language.
- The tutoring fee is exogenous; market clearing (83–85) is **not** solved.
- Admissions are a score gate plus a hard quota; the contest-success form (81) is **not** implemented yet.
- The CES complementarity (30–31) is imposed by ρ=0.5, not estimated.
- The literature has **not** been checked yet; the next step is to verify each equation, variable/unit and
  mechanism against the actual papers (Dang & Rogers 2008; Tansel & Bircan 2006; Kim & Lee 2010; Bray 2009;
  and the repo's Bray et al. 2016/2018 targets) and to relabel anything that does not survive.

Files: `shadow_model.py`, `run_shadow_scenarios.py`, `test_shadow_model.py`, `results_first_pass.json`,
`EQUATION_PLACEMENT.md`, `PRE_REGISTRATION.md`.
