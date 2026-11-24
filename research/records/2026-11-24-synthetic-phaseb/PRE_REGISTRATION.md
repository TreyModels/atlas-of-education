# PRE-REGISTRATION — Phase B: fertility/birth-history layer + dynamic micro signature (task-20)

**Branch:** `research/synthetic-phaseb-2026-11-24`, from matrix head `be7e499`. **Committed before code and
before any Phase B run.** **SIMULATION only; not evidence; no causal language.**

**Purpose.** Phase A's static tie-breakers were all rejected as transforms of the DGP weights (R² 0.93–0.996).
Phase B adds a minimal birth-history layer to test the pre-registered **non-transform dynamic observables**:
(B1) birth spacing after a child death (within-mother difference), (B2) parity progression by education, (B3)
age at first birth by education, and runs the fertility-stratum macro FE test.

**Birth-history layer (declared, minimal; not the full dose ABM — documented as such).**
4,000 women per world-seed, ages 15→40 (25 annual steps). Education `e in {0, 8, 12}` years with probabilities
set from the world's simulated post-reform GER (`P(8)=GER_post`, `P(12)=0.3*GER_post`, `P(0)=1-1.3*GER_post`,
clipped). Annual birth hazard `lambda = lambda0 * exp(-beta_e * e/8) * (1 - 0.10*parity)`; a child who dies
(annual mortality `mu * exp(-0.3*e/8)`) raises the next-year hazard by factor `rho` for two years (replacement).
World fertility parameters (declared, mechanism-motivated; independent of the school utility weights):
P `(0.42, 0.06, 0.10, 1.8)`, S `(0.34, 0.08, 0.08, 1.6)`, C `(0.30, 0.10, 0.06, 1.5)`,
R `(0.38, 0.05, 0.09, 1.7)`; `s=0` uses the parameter-wise mean (the null is identical across labels).

**Observables (per unit = world × seed):** B1 = mean next-birth interval after a child death − mean other
interval (within mother); B2 = PPR gradient (PPR at parity>=1 for e<=8 minus e=12); B3 = age at first birth
(e=12 minus e<=8). Units: calibration seeds k=0..19, held-out 20..79, replication 80..139 (seed = 20261125+100k
+ world offset), n=60 per world per block.

**Tests (fixed):** 4-class nearest-centroid on calibration-standardised features; chance 1/4, 95 % binomial
band; Holm across {B1,B2,B3}; **admissibility gate** R²(feature ~ weights + GER_post + cl_post) > 0.90 rejects;
controls: `s=0` must be at chance; label permutation. Verdicts: separates / cannot separate / cannot test (F3).
**Fertility-stratum macro FE:** split the 72 matrix countries into high/low simulated-fertility strata (median
CEB), re-run the 10-year country-decade FE slope of `D_cl_observed` on `D_GER` per world per stratum; report
cross-world separation in each stratum (55.6 % matrix baseline). **DHS signature update:** if a dynamic
observable passes the gate and beats chance out-of-seed, add it to the day-one signature (estimand, DHS IR
variable, specification, transport rule); otherwise say so and keep the design-based signature.

## Deviations log
- (to be filled)
