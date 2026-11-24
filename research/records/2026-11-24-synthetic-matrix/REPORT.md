# REPORT — synthetic multiverse matrix (task-19)

**Branch** `research/synthetic-matrix-2026-11-24`, from Phase A `394fb32`. **Run 9 s panel + matrix** on the Apple
M1, port NumPy backend (MLX bit-identical), batch `N=10,000, threads=256, blocks=40`. **SIMULATION — synthetic
analogue of the E1/Q3 multiverse, not evidence; no causal language.**

## Matrix

72 synthetic countries × 4 literature worlds (P Basu–Van, S Nordtveit, C Bray/Jayachandran, R Pritchett),
25 years; country nuisance drawn once and paired across worlds; 7 links (children-in-employment, study+work,
visible work, hidden work, tutoring, learning, income) each regressed on synthetic GER; **15 groupings**
(12 random 4-way partitions + 3 declared typologies by `sigma_y`/`mu_y`/`w_child` quartiles); **3 specifications**
(10-year differences + decade FE; 5-year differences + bin FE; levels + country + year FE); country-clustered SE.

## Two numbers

| statistic | value | comparison |
|---|---|---|
| **cross-world indistinguishable share** | **175/315 = 55.6 %** | pre-declared wall rule: ≥ 75 % ⇒ wall; **55.6 % ⇒ separable (wall NOT demonstrated)** |
| **robust-across-groupings share per world** | **P 15/21 (71.4 %), S 14/21, C 15/21, R 14/21 (66.7–71.4 %)** | E1 empirical robust-travel = **5/272 = 1.8 %** |

So even at the matrix level the worlds are **not** collapsed: 44.4 % of link×grouping×specification cells
separate the four worlds; the remaining 55.6 % are indistinguishable — a *partial blur*, but below the
pre-declared 75 % wall threshold. We report it; no tuning toward a wall.

**The trap in the second number.** Within-world "robust across groupings" is 67–71 % in the synthetic matrix,
whereas in the empirical multiverse only 1.8 % of links travel. The synthetic model therefore manufactures
"robust everywhere" links far more easily than real data — exactly Q3's warning (87 % of minority-effect worlds
would be mislabelled "robust everywhere"). A single-world robustness certificate from a synthetic matrix is
**not** evidence of a real link, and the empirical E1 rate is the benchmark, not the synthetic one.

## Interpretation (SIMULATION only)

At the matrix level the Phase A single-regression result holds up: the wall is **not** a generic consequence of
distinct micro mechanisms in this parameterisation. Cross-world separability is strongest for child-employment
and tutoring links, weakest for learning/income links (per-link detail: `results/matrix_cells.json`). The
empirical wall remains an empirical finding about country panels; the synthetic multiverse is a trap-setter
(it will happily produce "robust" links), not a source of evidence.

## Limitations

72 countries / 15 groupings approximate E1's 50 typologies (declared); links are the kernel's feasible variables
(no fertility in Phase A — Phase B adds it); robustness and Q3's mislabel statistic are different quantities,
so the comparison is structural, not numerical; clustered CIs are normal approximations, not bootstrap.

## Files

`PRE_REGISTRATION.md`, `synth_loop/{model,port_backend,run_matrix}.py`,
`results/{matrix_summary,matrix_cells,run_manifest}.json`.

## Deviations log

- Matrix pre-registered at `e...`; S3 design initially collinear (intercept + country dummies) and fixed before
  any result was inspected (design bug, not a rule change).
