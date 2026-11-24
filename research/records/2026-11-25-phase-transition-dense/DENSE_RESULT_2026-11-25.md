# Dense 20x20 grid — pre-registered boundary verdict (SIMULATION ONLY)

Grid: 16,000 runs = 20 X levels (vac0 0.01–0.63, geometric) x 20 Y levels (fee 0.00–0.19) x 20 seeds x
2 gates (bar, quota). Executed by the parallel `lead-nb` session into `/root/work/equifinality_phase`
(16,000/16,000 ok, 0 failed, 800 cells, 1,100 s, 12 workers). Statistics computed by this record's
`analysis/dense_boundary2.py` with the pre-registered metric (see `PREREGISTRATION_PHASE_SWEEP_DENSE.md`
and `AMENDMENT_01_STATISTIC.md`; the amplitude-declaration bar arm was cancelled as a duplicate of this
grid, pre-analysis — no dense number was read before the statistic amendment).

## Verdict

| arm / response | J_max | location (vac0) | sharpness | verdict |
|---|---|---|---|---|
| **quota / tutoring Q5−Q1 gap** | **11.50** | **0.4005 → 0.5044** (interior) | **18.17** | **SIGNATURE** |
| **quota / gate-fail share** | **12.58** | **0.4188 → 0.5044** (interior) | **23.48** | **SIGNATURE** |
| quota / liquidity exit share | 11.91 | interior | 11.9 | supporting |
| quota / tutoring rate | 24.71 | interior | 31.3 | supporting |
| bar / tutoring gap | 2.88 | edge | 11.5 | PARTIAL |
| bar / gate-fail | 2.86 | interior | 5.3 | PARTIAL |

- Gate contrast bar vs quota: median |Δ tutoring Q5−Q1 gap| = **0.0741** (pre-registered threshold 0.05).
- Equifinal pairs: **374**; largest: Δcompletion 0.26 pp with Δtutoring rate 20.9 pp and Δliquidity 15.5 pp.

Interpretation: the arms-race boundary exists **only when the gate binds**, on the formal-vacancy axis
at ≈0.40–0.50 vacancies per cohort entrant. The bar gate is non-binding in this engine (gate-fail
≤1.3%), which is why the quick-grid bar arm returned ABSENT — that is a property of the model's gate,
not evidence against the mechanism in real systems. Caveat: quota completion is partly pinned by seat
share, so "same attainment" in the equifinal pairs is partly accounting identity.

SIMULATION ONLY. No causal language. Negative bar result preserved.
