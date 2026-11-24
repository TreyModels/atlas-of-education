# Competing synthetic worlds: a minimal design check

`competing_worlds.py` is a CPU-only NumPy benchmark, **not** the Atlas CUDA engine. It makes 15 synthetic country-period cells, stipulates the same national mean fertility and schooling share in three worlds, and generates new observations. It makes no substantive historical claim.

- `effect`: schooling reduces individual births, in a world with no selection.
- `common_trend`: schooling and fertility move together over time, but schooling has no within-cell effect.
- `selection`: an unobserved type determines both schooling and fertility. There is no schooling effect. The latent type perfectly predicts schooling by design, making the observed subgroup distributions identical to `effect`. This is a deliberately strong demonstration, not a realistic complete model.

The two gradient worlds share the exact same individual-level observational distribution; in the `effect` world intervening to provide schooling changes births, whereas in the `selection` world it does not. The models have exactly equal probabilities for each observed aggregate total, not merely similar plots. Subgroup outcomes can distinguish the deliberately different `common_trend` world from the two gradient worlds but *cannot* separate schooling causality from selection. If the models are observationally equivalent, more historical observations of the same variables do not fix that identification problem. Other assumptions, interventions, or independent variables might.

This is **oracle** scoring, not training or calibration: it stipulates and supplies the correct model rates in advance and tests new draws. Results are a toy demonstration, not a realistic power analysis, cannot validate an estimator, and do not establish what will happen with actual data. It uses Poisson outcomes and fixed schooling counts. Simulation accuracy must be tested separately from scientific validity.

Run with Python 3 and NumPy:

```sh
python3 -I competing_worlds.py --seed 71201 --reps 200 --n-per-cell 400 --out results/demo
```

Writes `summary.json`, `first_macro.csv` and `first_micro.csv`. JSON reports the log-likelihood advantage of the gradient model over the no-gradient model on fresh simulated counts, plus stipulated causal intervention contrasts. Random generator seeds and arguments are recorded. `--contrast`, `--n-per-cell` and `--reps` control sensitivity. More replicates improve Monte Carlo precision, but cannot remove the constructed A/C non-identification. If moving to the real engine, predefine mechanisms, fit each fairly to actual training targets, and compare predictions on held-out country-period and microdata samples. Repeat over independent seeds and fully document engine and batch layout.

Local check: Python 3.10, NumPy 2.2.6; two independent invocations with default arguments produced byte-identical result files (`diff -qr run1 run2` returned zero). In this deliberately easy default case the gradient model had higher micro likelihood in 200/200 effect replicates, 0/200 common-trend replicates and 200/200 selection replicates. Those figures do not generalize beyond the specified toy setup.
