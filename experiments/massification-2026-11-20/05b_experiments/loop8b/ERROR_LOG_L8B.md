# ERROR LOG — Loop 8b (`05b_experiments/loop8b/`)

## Run-level
- 256 LHS draws × 5 matched seeds × 4 country configs with ECI-conditioned wiring; eps_ec arm and KOR
  two-margin tabulation re-run. **0 failed cells.**

## Process deviation
- **L8B-1:** the wired frontier run was launched before `PRE_DECLARATIONS_L8B.md` was committed. The wiring,
  distributions and delta rule had been fixed in code from the task specification before execution, and no
  result was read before the predeclaration file was written; the file contents match exactly what was
  executed. Recorded honestly as a process deviation (not a data/result change).

## Interpretation issues / caveats
1. **SYNTHETIC/POSSIBILITY only; programme stays CLOSED; brief-008 limits stand.** No closed claim reopened;
   no validation language.
2. **Wiring correction:** loop 8's ECI PENDING was a false absence check; ECI data exist and are used here
   with `eci_hs92` (country means 2015–2024; ref 0.852). `eci_sitc` robustness only; ranks/growth_proj/HS12
   never used.
3. **ECI conditioning is assumed where the register is not identified:** b_eci_stake/ret/comp/formal are
   declared LHS distributions (0.05–0.25 / 0.05–0.20), flagged "assumed" for ret/formal (R44/R47/R48 are
   ns/negative). No parameter is set to a target.
4. **Five targets only reported, as instructed:** KOR gradient 0→0 (empty support persists), HKG gradient
   0→2 (shrink holds), KOR fee 28→27, KOR income-gradient 117→82, KOR two-margin joint 0/256.
   The full 8-target table is in `runs/frontier_before_after.csv` for audit; it is not reported as a result.
5. **Unscoreable ECI rows:** R44, R45, R46 (auxiliary/jointly produced), R47, R48, R49, CX-01…CX-04 —
   direction-only, never scored inside/outside.
6. Demand-level intercept still fixed (A0 = −1.5); biggest remaining impossibility unchanged (KOR falling
   gradient and joint Korean pattern).
