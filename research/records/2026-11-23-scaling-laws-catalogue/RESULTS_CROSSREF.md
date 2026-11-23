# Scaling catalogue — outcome against each feasible row

Cross-reference to the scaling tests (task-19, `research/scaling-2026-11-23` @ 8243dd9,
`research/records/2026-11-23-scaling/`). Written after reading that record's README and
`results/consolidated_verdicts.csv`. This closes the loop on the catalogue's feasibility audit.

## Feasible-now rows, and what happened

| catalogue row | outcome | verdict |
|---|---|---|
| Urbanisation vs income — S-curve vs power vs log-linear | Logistic beats both out of sample but by little: share RMSE 0.1523 (logistic) vs 0.1532 (log-linear) vs 0.1598 (power); 10,986 country-years, 208 countries; slope 0.572 (SE 0.030), midpoint about $3,647 | **regularity, not a law** — the functional form matters but a straight line is nearly as good |
| Wagner's law — spending share vs income | Elasticity 0.103 (SE 0.030), n=4,699/161, which fails hard; but the tax series definition is undocumented | **inconclusive, not a refutation** |
| Fertility vs income — power law? | Power exponent −0.263 (SE 0.013), n=11,345/213; mild curvature (+0.018, SE 0.008); out-of-sample unchanged | **regularity (power form acceptable, curvature mild)** |
| Weak Mincer proxy — schooling vs income log-linearity | Elasticity 0.378 (SE 0.027), n=5,925/202 | **not comparable to individual Mincer returns** — label as a country-level association only |

## Feasible-with-a-data-pull rows, and what happened

| catalogue row | outcome | verdict |
|---|---|---|
| Zipf / rank-size and Gibrat | **Not testable**: every UN WUP city URL returned 404 from the server, and GeoNames archives downloaded truncated/corrupt twice | the catalogue assumed free availability; that assumption failed. Needs a working city-population source (WUP via doi/UN Data Portal, or OECD/StatCan national city lists) |
| Heaps' law / occupation diversity | Testable, but ILOSTAT's API no longer exposes 2-/3-digit ISCO categories — only ISCO-08 1-digit (10 categories). Rarefaction-corrected exponent **0.333 (SE 0.011)**, 151 countries, 11,712 points: sublinear but *below* the 0.4–0.6 literature range (z ≈ −5.9) | **testable but depth-limited**; the 1-digit ceiling is the binding caveat, and the crude "categories vs workforce" slope (−0.002) demonstrates the sampling-effort trap |
| Gravity for migration | Not tested: no bilateral matrix plus distance table on the box | still feasible with a UN migrant-stock + CEPII pull |

## Not-feasible rows confirmed blocked

City output/wages/patents/infrastructure (urban superlinear β≈1.15, infrastructure β≈0.85, agglomeration),
firm data (firm scaling, Lotka/Price), school-level data (school-size economies, district-cost U-shapes),
credential/occupation crosswalks. The binding constraint remains city-level output, exactly as the catalogue
predicted.

## Two substantive bonuses from the scaling record

1. **The within-versus-between discipline.** Most education–income "scaling laws" are between-country
   regularities, not laws about change: secondary enrolment vs income is 0.215 (SE 0.035) between countries but
   0.090 (SE 0.124) within; upper-secondary attainment 0.312 vs 0.072; education stock vs output 1.176 vs 0.051;
   cohort size vs enrolment −0.612 vs −0.006. A handful survive both layers (tertiary enrolment, lower-secondary
   completion, services share, urban share vs enrolment). This is the same lesson as the session's
   trend critique, in another data setting.
2. **The "universal fertility collapse with female attainment" curve is rejected.** Using 4,394 country-cohort
   points, the best common exponential fits with R² = 0.78, but country effects explain 72% of the residual,
   the slope differs by country (F = 46.4), and the residual spread is 11% of the range; low-income countries
   slope +0.40 and 1950s cohorts +0.29. So there is no single attainment–fertility curve across countries.

## What this means for the catalogue's headline claims

The catalogue's feasibility audit was right about what needs city-level output and microdata. It was too
optimistic about free city-population data (WUP/GeoNames failed) and about occupation-category depth (ILOSTAT now
1-digit only). Of the scaling laws we could test: one is a regularity (urbanisation–income S-curve), one method
(Heaps) is testable but depth-limited and sits below the literature range, one is inconclusive (Wagner), and the
rest are blocked by data. None of this produces a new scaling law for our purposes; it produces a clean statement
of what is and is not measurable.
