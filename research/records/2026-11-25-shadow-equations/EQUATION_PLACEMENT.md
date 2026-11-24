# Equation placement — first-order mapping (Trey's inventory → synthetic cohort model)

This is the placement I would defend on first-order reasoning. It is **not** yet checked against the original
papers; the literature check comes after the build, as instructed. Catalogue numbers refer to the "Master
Equation Inventory" Trey supplied (equations 1–183).

| Inventory # | Equation (short) | Where it belongs | First-pass implementation | Status / caveat |
|---|---|---|---|---|
| 23 | Multinomial choice probability | Household tutoring demand | Softmax over none / own / other / commercial | Generic form; not tied to a specific paper yet |
| 57–59 | Participation dummy, logit/probit | Household demand | Choice probabilities from the same MNL | Logit/probit are empirical specs, not behavioural laws |
| 60–63 | Intensity, two-part/hurdle, Tobit, double hurdle | Household demand (robustness) | First pass MNL; Tobit/hurdle flagged for Stage-1b | Tobit assumes a latent mechanism; not yet justified |
| 64–66 | Spending share, Engel curve, income elasticity | Demand outputs | Computed from chosen option and income | Descriptive, not causal |
| 67–68 | Own-price and cross-price elasticities | Demand outputs | Price ±10% re-run | Numerical elasticity, illustrative |
| 69 | Tutoring share of education spending | Demand output | Spend/Y, reported | Needs total education spending to be meaningful |
| 70 | Joint schooling+tutoring budget constraint | Household demand | Implicit in MNL (income/price terms); not solved | Explicit constraint is a Stage-2 task |
| 26, 28 | General/Cobb–Douglas production | Learning production | CES baseline; Cobb–Douglas as sensitivity | Functional form is an assumption |
| 30–31 | CES production, complementarity | Learning production | CES with ρ=0.5; cross-partial reported | Complementarity is imposed by ρ, not estimated |
| 71–75 | Tutoring in production, marginal product, dose–response | Learning production | CES tutoring nest + linear dose sensitivity | Empirical forms, not mechanistic laws |
| 72, 76 | Tutoring × schooling / SES interaction | Learning production | SES × tutoring-dummy interaction | Sign is a first-order guess |
| 81 | Contest-success admission probability | Admissions gate | Ranking on score for first pass; Tullock form deferred | Contest form needs a paper check |
| 82 | Household tutoring choice in admissions contest | Demand/gate link | Admission threshold enters demand only indirectly for now | Not yet a strategic contest |
| 83–85 | Tutoring-market equilibrium, provider profit, tax wedge | Tutor supply/market | Fee exogenous; supply not cleared; tax not modelled | Major limitation; Stage 2 |
| 86 | Reduced-form policy association | Scenario comparisons | Differences across scenarios, no causal claim | Not an identification design |
| 42–43 | Mincer earnings, exact % return | Earnings | ln w = α + β·schooling + γ·ability + δ·admitted + ε | Illustrative coefficients |
| 123–125 | Gini/Theil | Distribution | Gini implemented; Theil deferred | Measurement formulas |
| 129–131 | SES achievement gap, tutoring gap, concentration index | Distribution | All three implemented | Concentration index needs income ranking |
| 176–177 | Teacher incentive/effort, optimal effort | Tutor supply/policy | Ban/access flag only; effort model deferred | Needs Stage-2 supply module |

## Deliberate first-order choices (to be tested against the literature)
1. **Demand is a discrete choice, not a hours regression.** Participation and spending are the same decision in
   this pass; the two-part/hurdle alternative is the main robustness check later.
2. **Own-teacher tutoring carries a premium** (favour/relationship), and a ban removes that option rather than
   re-pricing it. This is the mechanism the repo's earlier model could not identify.
3. **Tutoring and school are CES substitutes with a fixed weight**; the first pass does not estimate the
   elasticity. Complementarity is therefore imposed, not found.
4. **Admissions are a score gate with a quota variant**, not a full contest; the contest-success equation is
   listed but deferred because it needs a strategic effort model, not just a score.
5. **The tutoring fee is exogenous**, so market-clearing (83–85) is not tested here. This is the biggest gap
   between the inventory and the first build.
6. **Every coefficient is illustrative**; the point of the first run is sign/magnitude sanity and code paths,
   not an empirical result.

## What the literature check must settle (after the build)
- Whether the published papers actually contain these equations in these forms, and with which variables/units.
- Whether the own-teacher premium is a behavioural law or a reduced-form association.
- Whether the CES/complementarity assumption matches any published tutoring-production estimate.
- Whether the contest-success form or a score gate is the right admissions representation.
- Whether a tutoring-market equilibrium is identified or must stay exogenous.
