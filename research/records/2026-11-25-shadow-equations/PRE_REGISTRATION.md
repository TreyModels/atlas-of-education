# PRE-REGISTRATION — first-pass placement of shadow-education equations (25 Nov 2026)

Status: **first-order / exploratory build**, written BEFORE the first run and BEFORE literature verification.
Purpose: put the shadow-education equations from Trey's inventory where they belong by first-order reasoning, build
the scripts, run them, and only then check the literature to see whether the assumed forms are wrong.

## What is being built
A synthetic cohort model with five modules, each hosting the equations Trey supplied (catalogue numbers refer to
the pasted "Master Equation Inventory"):

1. **Household tutoring demand** — multinomial choice among none / own-teacher / other-teacher / commercial
   (catalogue 23, 57–63), with the joint budget constraint (70), expenditure share (64) and income/price
   elasticities (65–69) computed as outputs.
2. **Learning production** — CES school/tutoring production (26, 28, 30–31, 71–75), with a SES × tutoring
   interaction (72, 76).
3. **Admissions gate** — score bar versus quota seats (81–82); the contest-success form is represented by
   ranking on the produced score for the first pass, not yet by a Tullock probability.
4. **Earnings** — Mincer returns (42–43) with an admission/credential shift.
5. **Distribution** — Gini, rich–poor learning gap, tutoring-participation gap and concentration index
   (123–131).
Teacher incentives (176–177) enter only as a ban/access policy flag in this pass; the market-clearing equations
(83–85) are not solved — the fee is exogenous and this is stated as a limitation.

## First-order assumptions (to be checked against the literature later, not assumed true)
- Tutoring demand rises with household income and falls with price; lower school quality raises demand.
- Own-teacher tutoring gets a utility premium (the "favour/own-teacher" channel); a ban removes that option.
- Tutoring adds to learning via a CES nest with school instruction; the elasticity of substitution is 0.5 and
  the school weight is 0.5. All parameter values are illustrative, not estimates.
- A bar gate admits the top half by score; a quota reserves 50% of seats for the bottom 40% by income (hard reserved-seat competition).
- Earnings depend on years of schooling, ability and admission; the Mincer slope is illustrative.
- Rural access reduces the non-price inconvenience of non-own providers; a cash transfer raises the bottom
  quintile's income by 30%.

## Scenarios (pre-declared)
baseline (bar gate), quota gate, own-teacher ban, rural access, cash transfer to bottom quintile, quota+ban,
quota+rural. Seeds: pilot 3, full 10. Primary read-outs: tutoring participation and own share, spending share,
income elasticity, price elasticity, learning mean/Gini/rich-poor gap, admission rate by income quintile,
earnings Gini, tutoring-participation gap, concentration index.

## Stop / honesty rules
- Every parameter is flagged illustrative; no causal language; no empirical validation claimed.
- If a mechanism's sign or magnitude is implausible in the pilot, fix the mapping (not the data) and record it.
- Literature verification comes AFTER this build: each equation's real published form, variables and units will
  be checked; equations that do not survive that check are relabelled or removed.
- Preserve all logs, commands, hashes and outputs; no secrets; simulation only.
