# Results and reproducibility

Run from the ZIP's top-level directory:

```bash
node test_model.js
node scripts/reproduce_results.js
```

The second command overwrites two files deterministically:

- `scenario_results_seed42.csv`: nine presets with seed 42, 850–1450, final population, regional density, monument log index, final-year soldiers, cumulative conflicts/sacks, rice balance and bonded workforce.
- `experiment_summary.json`: a paired 30-seed reference-versus-estate experiment ending 1250, plus a 50-run parameter sweep ending 1250 and three OLS regressions.

**How to interpret results:** These are outputs from a hypothetical mathematical system. They are not archaeological measurements, posterior historical estimates, or a published benchmark dataset. Single-seed differences can be unstable. Monte Carlo percentiles quantify variation under the model's pseudorandom generator and specified seeds, not the full uncertainty about historical Angkor.

**Why the results deserve caution:** The reference scenario ends with a substantial rice deficit and zero soldiers in 1450. This points to missing food storage, nonrice provisioning, seasonal allocation and historical trade mechanisms. The high R² values in the regression sweep suggest tight structural dependencies within the simulator. These limitations should be addressed before calibration.

To change experiments, edit `scripts/reproduce_results.js`. The script calls the same `model.js` engine used by the web interface. No external package is required.
