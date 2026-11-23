# Handoff run, 23 Nov 2026 (server: AutoDL, key auth)

Scripts in `scripts/`, outputs in `results/`, older server outputs kept for provenance in `server_prior_outputs/`.
Every output here was produced by the script of the same name that is saved here. Server data path /root/work/data.

| Job | Status | What happened |
|---|---|---|
| 1 Full matrix with country trends | ran now | `scripts/full_matrix_trends.py` -> `results/full_matrix_trends_out.txt`. 126 edges significant with country effects; 45 with trends; 25 in both. Electricity -> lower-secondary: +0.333 (SE 0.083) FE, +0.052 (SE 0.098) with trends, n=1,343, 129 countries. The README's "+16.05" is NOT produced by this script (REVIEW traces it to tight/results.json, n=471, one spec). |
| 2 Power check | ran now | `scripts/boppart_power.py` (500 panels) -> `results/bpower_out.txt`. See below. |
| 3 Input prices, income controlled | ran now (rebuilt) | `scripts/input_prices_controlled.py` -> `results/input_prices_controlled_out.txt`. |
| 4 Individual marriage model | not run; plan | `PLAN_jobs_4_and_7.md` |
| 5 Cohort model out of sample | ran now (fixed) | `scripts/cohort_huge_fixed.py` -> `results/cohort_huge_out.txt`, `cohort_huge.json`, `cohort_abs_mse.txt`. |
| 6 CES recovery | ran now | `scripts/ces_fast_indep.py` -> `results/ces_indep_out.txt`. |
| 7 UN marriage / co-residence merge | not run; plan | `PLAN_jobs_4_and_7.md` |
| 8 Reconciled STATUS | see `PUBLISHABLE.md` for the audit; a full STATUS rewrite is left undone | |

## Job 2 result (plain words)
In a world where electricity truly raises schooling (S-curve rollout, timing partly independent of development):
a true effect of 20 points (0 -> 100% electrified) is detected in 91% of panels with country trends (49% without);
10 points in 45% (20% without); 5 points in 17%; 40 points in 100%. Where there is no effect, trends give 2-4% false
positives. In the original no-effect world with 500 panels: 98% false alarms without trends, 4% with.
So the trend test is not blind to smooth electrification effects, at the simulated sample size (120 countries x 45 years).
BUT the real-data panel is much smaller (1,343 rows) and the trend coefficient is 0.052 +/- 0.19 (95%): it is
compatible with zero and with an effect the simulation would call large. "Dies under trends" = "cannot be separated from
development at this sample size", not "shown to be zero".
Caveats: simulation effect is contemporaneous in level; the test regresses 10-year change on starting level.

## Job 3 result
The original script is lost and its magnitudes (+0.445 etc.) are NOT reproduced by this rebuild (mine are ~0.02 on the same
sign); construction details differ (I use decade change in log(price/GDPpc) x 1990 farm share, year-pooled decade effects).
Qualitatively: wage-jobs effect (-0.014, significant) vanishes once income growth is controlled (-0.002, n.s.); farm-exit effect
halves (+0.024 -> +0.012) and with country trends falls to +0.007 (+/-0.005). Births: zero in every spec. Price-only and ratio
specs are algebraically identical once income change is controlled. Paper 04's wage-jobs claim should be dropped; farm exit is weak.

## Job 5 result
Fixes: the server copy had a SyntaxError (`global` after assignment) and every bootstrap draw reused the same RNG state;
seeds in the power study were shared across true values. Fixed copy ran. Out of sample (last two cohorts, 149 countries):
schooling channel improves prediction in 15% of countries, worsens it in 16%, median gain 0 (fitted alpha is 0 in 68%).
Pooled squared error is lower with schooling (0.70 vs 1.14) but that is driven by a few high-fertility countries
(mean paired gain 0.44, SE 0.22). The script's own "mean gain -460%" bootstrap line is an artefact of dividing by near-zero errors; ignore it.
Power: with a true alpha of 0.15 the design finds a gain in 90% of simulated worlds; at 0, 2% (so the design can see schooling effects of that size).
Caveat: schooling is interpolated using later observations (mild look-ahead); the 'true' world is the model's own structure.

## Job 6 result
Redone with independent seeds per true value (200 sims each): estimated sigma 0.002/0.500/0.996/1.500 for true 0/0.5/1/1.5;
coverage 97.5/94/95/95%. The earlier identical-bias rows were a seed-reuse artefact, now fixed; recovery holds under the
estimator's own model (this is a weak test). Real-data estimate is unchanged: 0.43 [0.31, 0.56], P(>1)=0%. The structural
claim should still be dropped: the wage is economy-wide, the price is the investment-price index, and the data are not
Boppart's. Note the run that produced `server_prior_outputs/ces_out.txt` was `ces_fast.py` (vectorised), not `ces_bayes.py` as the pack's scripts suggest.

## Provenance flags
- `bw2_out.txt` came from boppart_world.py with N_PANELS=100 (server) while the pack copy says 500; `bw_out.txt` header said 200. `scripts/boppart_world.py` is the server copy (100); `boppart_power.py` reruns the original no-effect world at 500 panels.
- `gdppc_log.json` holds GDP per head in levels (e.g. 1432), not logs, despite the name.
- The pack's CLAUDE.md contains a server password in plain text; it was NOT copied here. Rotate it.
