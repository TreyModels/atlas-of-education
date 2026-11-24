# PRE-REGISTRATION — heterogeneity matrix v2 (region-42, task-21)

**Committed before the v2 run. SIMULATION only; no causal language; no tuning toward a wall.** v1 (`be7e499`):
72 homogeneous countries, no measurement error → 55.6 % cross-world indistinguishable (below 75 % wall rule).

**Declared grid (scaled from the Lead's spec for feasibility; scaling stated here before the run):**
- **256 countries**, 8 declared synthetic types (dev × school-supply × labour-market), 32 countries/type;
  parameters drawn within type from declared distributions (paired across worlds).
- **Worlds:** P Basu–Van, S Nordtveit, C Bray/Jayachandran, R Pritchett, **Rm** = misspecified Pritchett
  (omitted tutoring channel: div=0.02), plus s=0 null (used for the control, not the matrix).
- **Links: 7** (child employment, study+work, visible work, hidden work, tutoring, learning, income; fertility/CEB
  deferred to v2.1 when the Phase B layer is integrated).
- **Groupings: 40** = 32 seeded random 4-way partitions of 256 + 8 declared typology split-pairs (4 types × 2
  sizes).
- **Specifications: 4** = 10y-differences + decade FE; 5y-differences + bin FE; levels + country + year FE;
  10y + income control.
- **Measurement-error dose ladder:** 0×, 1× (sigma 0.05 lognormal on each link series), 2× (0.10).
- **Seed blocks:** B1 seed 20261124, B2 seed 20261125 (replication); fixed.
- Cells = 7 links × 40 groupings × 4 specs × 3 doses × 2 blocks = 6,720; × 5 worlds = 33,600 regressions.
- **Decision rule:** cell indistinguishable iff all ten pairwise 95 % CIs (5 worlds) overlap; wall iff
  cross-world indistinguishable share ≥ 75 % with cluster-bootstrap 95 % CI; report both patterns and the
  dose ladder. Robust-across-groupings per world: (link,spec,dose) same-sign/|t|>1.96 in ≥80 % of groupings.
- **Compute:** region-42, `multiprocessing.Pool(96)`; per-worker `OMP/MKL/OPENBLAS_NUM_THREADS=1`; NumPy backend
  (no GPU number counts without fixed-seed NumPy-vs-CUDA equivalence). dhs-scout runs 48 workers concurrently in
  `/root/work/dhs-api` (coordinated); our pool adapts if load >96.

## Deviations log
- (to be filled)
