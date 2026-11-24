# PRE-REGISTRATION — v2b scale/replication extension (task-21; committed BEFORE v2 results are inspected)

**Same question, same decision rule as v2; a power/replication extension, not a rescue.** v2b does not replace
v2 and the two are reported separately.

**Design:** N = **100,000 households/country** (10× v2 per-run kernel cost); **512 countries** in the same
8 declared types; **5 worlds** (P, S, C, R, Rm misspecified-Pritchett) + s=0 null; 7 links (fertility deferred
to v2.1); **80 groupings** (64 seeded random + 16 declared typology split-pairs); **6 specifications** (adds
10y + region-style control and 5y + control to v2's four); **3-level measurement-error dose ladder** (0×, 1×,
2×: sigma 0.05/0.10); **10 seed blocks** (20261124 + 100·k, k=0..9). Cells = 7×80×6×3×10 = 100,800; ×5 worlds =
504,000 regressions. Cross-world indistinguishable iff all ten pairwise 95 % CIs overlap; **wall iff share ≥ 75 %
with cluster-bootstrap CI**; robust-across-groupings per world as before.

**Compute/provenance:** region-42, `multiprocessing.Pool(96)` (series generation parallelised too, unlike v2's
serial series phase), per-worker `OMP/MKL/OPENBLAS_NUM_THREADS=1`; NumPy 1.24.1 reference. Expected wall
10–25 min (declared: if exceeded, the run continues and wall is reported; grid is not reduced post hoc).
GPU not used (no CuPy in image after two attempts; kernel is small elementwise work; no GPU number counts
without fixed-seed NumPy-vs-CUDA equivalence). Seeds/layout/wall/nproc recorded in a server provenance note.

**Decision rule:** identical to v2. Do not tune toward a wall; report both patterns and the dose ladder.
## Deviations log
- (to be filled)
