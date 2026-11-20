# ERROR LOG — Loop 3 (`05b_experiments/loop3/`)

## Run-level
- Final run: S1 15-row stage-matched table; S2 600-draw joint search per country + one-at-a-time
  grids; S3 675-point grid × 3 countries. **0 failed runs** (numpy-only, single process).

## Defects found and fixed before results were recorded
1. **First-pass model produced take-up ~0–2%** because the loop-2 dynamic price/entry block collapsed
   supply at the price floor (util collapse). Replaced the tatonnement with a declared **static long-run
   competitive equilibrium** (teacher capacity limited; commercial unlimited at unit cost; price at the
   marginal supplier). No result from the first pass is reported.
2. **Percentage/fraction display bug in S1** (model values shown as 0.2 instead of 20). Fixed and re-run;
   the final numbers in `runs/s1_table.*` are percentages.
3. First S1 draft flagged HKG from the calibration row only; fixed to flag HKG from its 2010
   lower/middle gradient checks, with the 85 senior row excluded from pass/fail.

## Interpretation issues / caveats
1. **The stage-matched baseline now UNDER-predicts shadow incidence** in HKG/KHM (opposite of loop 2's
   over-universalisation). Both failure directions are reported; neither is evidence of incidence.
2. **S2 has weak identification for HKG**: 2 targets are fitted with 8 free structural parameters, so
   the HKG "reproduces" result is not a validation; the PHL result (none works) and KHM (partial) are
   the informative ones.
3. **S2 parameter ranges are declared, not estimated** from data; "none works for PHL" means no
   combination *inside the declared ranges* reproduces 46.5/23.8/28.1, not that no model could.
4. **S3 is UNABLE, not a pass**: no observed fee moment exists for PH/HK/KHM; Korean fee moments exist
   but there is no KOR model variant. The grid is reported for structure only.
5. **Targets:** only observed cells from `02_lit/SHADOW_TARGETS.csv` and `04_data/TARGETS_SHADOW.csv`
   are compared; no imputed cell is used. HKG 0.85 is a calibration, never incidence evidence.
6. **Intake corrections:** 11 `use_as_model_target=YES` rows (not 6); loop-2 teacher-tutor entry effect
   54–67 pp (not 46–66). Corrected in `EXPERIMENTS_L3.md`; loop-2 files left unedited.
7. **Pending tests not run:** L2-4 recovery/forced-ID and L2-5 holdout are specified but not executed;
   no claim from them.
