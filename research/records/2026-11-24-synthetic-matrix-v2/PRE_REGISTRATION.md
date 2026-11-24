# PRE-REGISTRATION — heterogeneity matrix v2 (task-21, server region-42)

**Branch:** `research/synthetic-matrix-2026-11-24`; record `research/records/2026-11-24-synthetic-matrix-v2/`.
**Committed before any v2 run.** **SIMULATION only; no causal language; no tuning toward a wall.**
v1 (`be7e499`) = 72 countries × 7 links × 15 groupings × 3 specs → 55.6 % cross-world indistinguishable.

**v2 design (fixed):** 200 synthetic countries per world × 4 literature worlds (Phase A parameterisation), 25 y.
Country-level dispersion: nuisance vectors drawn from **wider** declared ranges (sigma_y .25–.95, sigma_a
.08–.45, mu_y −.40–.50, mu_a .70–1.50, w_child .02–.50, shadow_cost .10–.70, f_pub_pre .00–.45, y_sub0
.55–1.25). **Measurement error:** each link is observed with independent lognormal noise (sigma 0.05) on the
per-country-year series before differencing. **Model misspecification:** a seeded 20 % of countries are run
under a *different* world's parameters (wrong-mechanism countries), with the same seed across worlds. Same
7 links, **20 groupings** (16 seeded random 4-way partitions + quartiles of `sigma_y`, `mu_y`, `w_child`,
`f_pub_pre`), **3 specifications** (10y differences + decade FE; 5y differences + bin FE; 10y + income
control). Country-clustered SE (t = 1.96).

**Statistics/decision rule (unchanged from v1):** cell = (link × grouping × spec); cross-world
indistinguishable iff all six pairwise 95 % CIs overlap; wall demonstrated iff share ≥ 0.75. Robust-across-
groupings per world: (link,spec) robust iff ≥ 80 % of groupings same-sign/|t|>1.96; report count/21.
Comparison: E1 5/272 = 1.8 %; Q3 87 %.

**Compute:** server region-42 (96 cores, RTX 2080 Ti). Parallel driver: multiprocessing over country chunks
(series) and over matrix cells, 24 workers. NumPy backend (no GPU number counts without fixed-seed
NumPy-vs-CUDA equivalence: ints exact, floats within 1e-5 abs/1e-4 rel, pinned layout; CuPy absent in image).
Wall time, worker count, nproc, numpy version, seed block recorded in a server-run provenance note.

## Deviations log
- (to be filled)
