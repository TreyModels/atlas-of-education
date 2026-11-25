# Paper A (E8) — Callaway–Sant'Anna-style group-time ATT on the fresh hashed WDI vintage

**Label: REPRODUCED EMPIRICAL ANALYSIS (fresh WDI vintage; CS-style group-time ATT). Paper A numbers remain the
AUTHOR-REPORTED baseline.** Artefact `results/audit/newgen/cs_estimator_fresh_wdi_2026-11-25.json`; script
`/tmp/cs_estimator.py` (box `/root/work/cs/cs_estimator.py`); panel manifest sha256
`d7296e1fed3eb6806ba5111de2538e7fcd206323832307a1fabeeaefc6c55ee4`.

## Estimator (declared deviations)

Callaway–Sant'Anna-style group-time ATT(g,t), **not-yet-treated control group**, t = g−3…g+6, treated change measured
from g−1, donor-pool change over the same window; **equal country weights** (cohort-size weighting would require
population/cohort data not in the WDI pull — declared deviation), no doubly-robust covariates. Treated countries/dates
from the manuscript (MWI1994, ETH1995, UGA1997, LSO2000, TZA2001, KEN2003, MOZ2004, GHA2005); 40-country SSA donor
pool. Inference: 500 country-cluster bootstrap replicates + 2,500 Fisher randomization-inference permutations per
scheme.

## Result — the delayed amplification REPLICATES under the author's estimator family

| quantity | CS-style new-generation (fresh WDI) | AUTHOR-REPORTED baseline |
|---|---|---|
| impact ATT(e=0) | **+12.322 pp** (bootstrap mean 12.308, 95 % CI [4.48, 22.64]) | +12.44 pp |
| post mean (e=+1..+6) | **+25.083 pp** | +25.26 pp |
| pre-trend e=−3 | +0.138 pp | −0.03 pp |
| event path e=0..6 | 12.32, 23.66, 25.79, 21.88, 24.94, 28.45, 25.78 | — |
| Fisher p (date / country) | **0.0044 / 0.0040** (2,500 each) | 0.0001 / 0.0003–0.0006 |

## Why the earlier simple-DiD run differed (A-35 resolution)

The fresh-WDI **simple DiD** (year-over-year treated change minus donor-pool year-over-year change) gave post mean
**+2.54 pp** and looked like non-replication. The **CS-style group-time ATT** (cumulative change from g−1, not-yet-
treated controls) gives **+25.08 pp**, matching the author's +25.26. **The difference was the estimator, not the data.**
Therefore A-35 moves from UNRESOLVED/ESTIMATOR-DEPENDENT to **REPLICATED under the CS-style estimator**; the simple-DiD
number remains recorded as estimator-sensitive, and neither is a contradiction of the other.

**Caveats:** equal country weights (no cohort-size weighting); no DR covariates; fresh WDI vintage may have revisions;
cluster bootstrap with only 8 treated countries is wide (CI [4.48, 22.64]) — impact magnitude is noisy even though the
post-average matches. No causal claim beyond the author's design.
