# PRE-REGISTRATION — synthetic multiverse matrix (task-19)

**Branch:** `research/synthetic-matrix-2026-11-24`, from Phase A head `394fb32`. **Committed before code and
before any matrix run.** Everything is **SIMULATION**: a synthetic analogue of the empirical E1/Q3 multiverse,
not evidence about real economies; no causal language.

**Why:** Phase A's H1 was one regression; the wall is a *matrix* claim (E1: 272 links × 50 typologies, 5 travel).
This run builds the matrix on the four non-degenerate literature worlds (P Basu–Van, S Nordtveit,
C Bray/Jayachandran, R Pritchett; Phase A parameterisation, committed at `394fb32`).

**Design (fixed):**
- **Panel:** 72 synthetic countries per world, 25 years, fee abolition at t=10. Country nuisance vector
  `(sigma_y, sigma_a, mu_y, mu_a, w_child, shadow_cost, f_pub_pre, y_sub0)` drawn once per country from declared
  uniform ranges with RNG seed 20261124, **identical across worlds** (paired design). Batch layout `N=10,000,
  threads=256, blocks=40`, port NumPy backend.
- **Links (7):** the variables the kernel generates — children-in-employment share, study+work, visible work,
  hidden work, tutoring rate, mean learning, mean income — each regressed on the synthetic **GER** (schooling
  expansion). Link definition: same 10-year/5-year/level association as an E1-style panel link.
- **Groupings (15):** 12 random partitions of the 72 countries into 4 groups (RNG 20261125) + 3 declared
  typologies (quartiles of `sigma_y`, of `mu_y`, of `w_child`). Groups of 18 countries.
- **Specifications (3):** S1 10-year differences + decade FE; S2 5-year differences + five-year-bin FE;
  S3 levels + country FE + year FE. Country-clustered SE (`t` = 1.96 for 95 %).
- **Statistics:** for each link×grouping×specification cell estimate the slope per world. A cell is
  **cross-world indistinguishable** iff all six pairwise 95 % CIs overlap. Report the cross-world
  indistinguishability share. **Robust-across-groupings** per world: a (link, spec) is robust iff >=12/15
  groupings give the same-sign, |t|>1.96 estimate as the world's full-sample slope; report robust share per
  world out of 21.
- **Decision rule (fixed):** wall demonstrated iff cross-world indistinguishability >= 75 %; otherwise separable.
  Do not tune to force a wall; report both patterns. Comparison targets: E1 empirical robust-travel rate
  **5/272 = 1.8 %** (scaled: 5/272 of links travel; our robust share is the analogue) and Q3 **87 %** minority-
  effect mislabelling (qualitative comparison only — different statistic).

**Failure/limits:** a world that cannot generate the links is reported; matrix cells with insufficient variation
are reported, not dropped silently; 72 countries is a feasible-matrix declaration (E1's 50 typologies are
approximated by 15 groupings — declared).

## Deviations log
- (to be filled)

## Deviations log (filled)
- S3 specification design initially had an intercept collinear with country dummies; fixed before any matrix
  result was inspected (implementation bug, no rule change).
