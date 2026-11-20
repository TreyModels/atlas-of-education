# Complexity → model map

Where economic complexity can enter the massification/two-way model, with sign expectations and the
honest status (observed index vs assumed elasticity). **Complexity is a country-level index, not a
mechanism**; it may condition relations and proxy latent capability, never identify a causal effect.

| model quantity | role of complexity | expected sign | status | plug point |
|---|---|---|---|---|
| State capacity / school-place supply | higher ECI ⇒ more administrative/fiscal capability ⇒ more places, higher quality | + | observed index as proxy; elasticity assumed | `twoway.py` capacity term; `massabm` `cap_cost` |
| Formal-job creation | higher ECI ⇒ more formal/complex jobs available for educated workers | + | observed index; elasticity assumed (Council P47: +0.40) | `twoway.py` `eps_ec` / job-creation term |
| Complex-job share | higher ECI ⇒ larger complex-job sector | + | observed index; elasticity assumed (P48: +0.60) | `twoway.py` complex-share parameter |
| Returns to schooling / credential demand | higher ECI ⇒ higher skill premium and credential demand | + (weak) | correlational; to be estimated in `09_relations` | household return parameter; `massabm` wage path |
| Upper-stage tutoring take-up | higher ECI ⇒ higher senior-stage shadow demand | + (weak; Council P49: +0.30 pp/sd) | assumed, direction-only | tutoring demand intercept by stage |
| Growth (education→economy) | complexity's growth projection is the Growth Lab's own ECI-implied forecast | + on growth | observed `growth_proj`; not an education effect | comparison benchmark, not a parameter |
| Country typology | low vs high complexity as a conditioning axis (with state capacity) | — | observed index | `COUNTRY_TYPOLOGY.md`, scenario families |

## Do not

- Do not treat ECI as a measure of schooling or of education quality.
- Do not use rank changes as level changes, or splice SITC/HS92/HS12.
- Do not claim complexity causes education demand; it is endogenous to income, schooling, and
  industrial policy.
- Do not use the Growth Lab's `growth_proj` as evidence for an education→growth effect.

## Data

`04_data/complexity/ECONOMIC_COMPLEXITY.csv` (tidy, 6 countries × 1995–2024),
`ECONOMIC_COMPLEXITY_WIDE.csv` (country summary), `COMPLEXITY_METHOD.md` (definitions and caveats).
Relations using ECI are added to `09_relations/RELATION_CANDIDATES.csv` (ECI rows).
