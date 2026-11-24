# MASSENG v5 Philippines prior screen

This folder contains a separate importance-screening experiment for the v5 R1 demand model. It does not change the model, country inputs, protocol, or existing result files.

The experiment draws four R1 mechanism parameters independently from explicit uniform priors: `b_h` (human-capital premium response), `b_p` (positional feedback), `b_r` (credential-threshold/formal-work response), and `lam` (declining cost sensitivity with saturation). All other parameters are fixed at the existing `outputs/PHL/v5/fit_R1.json` values. Because this fit was estimated using broader data, the experiment is conditional on empirically informed nuisance parameters and has data reuse; it is not a fresh independent calibration.

For each draw, a Gaussian pseudo-likelihood is computed from 1971–1995 GERs. It sums the three series' mean log densities, giving each series equal block weight. The fixed scales are 4, 4, and 5 percentage points for primary, secondary, and tertiary GER respectively. These are declared working scales, not official sampling errors. Since the v5 engine is deterministic conditional on parameters and drivers, the weights quantify compatibility under this chosen pseudo-likelihood, not a validated posterior uncertainty model.

The 1996–2024 comparison is retrospective and inspected as stated in `model/PROTOCOL_v5.md`. The runner compares weighted posterior-mean GER RMSE with a last-training-value persistence baseline. It reports weighted 90% intervals and importance effective sample size (ESS). A low ESS means the prior draw count is inadequate to characterize the weighted screen; no resampling is performed. No causal or preregistered significance claims are made.

Run commands from the repository root:

```sh
PYTHON=${PYTHON:-python3}
MODEL=work/masseng_checkout/research/masseng-v6/experiments/codex_bayes
$PYTHON "$MODEL/run_screen.py" --n-draws 512 --seed 20261124 --workers 1 --prior main --out "$MODEL/results_main"
$PYTHON "$MODEL/run_screen.py" --n-draws 512 --seed 20261124 --workers 1 --prior expanded --out "$MODEL/results_expanded"
$PYTHON "$MODEL/test_screen.py"
```

Each output directory must be new. `summary.json` records priors, fixed baseline parameters, fit/holdout diagnostics and limitations; `draws.json` contains each prior draw, log weight, normalized weight, and holdout prediction.
