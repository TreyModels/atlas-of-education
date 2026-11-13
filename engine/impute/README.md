# `engine/impute` — the Atlas imputation system (to-do item A10)

A provenance-carrying country-year panel, a six-rung ladder of imputation methods with a common
`fit`/`predict` API, and a hold-out harness that deletes known points and scores error by method
and gap length (the B11 validation). numpy/scipy only in the core; pandas is used only to read the
packaged CSVs. Deterministic: every stochastic piece takes an explicit seed.

## Provenance

Every cell carries a flag, and the flag travels with the number:

| flag | meaning |
|---|---|
| `v` | verified: read from a named source / the packaged release file |
| `m` | from memory of an official release; not yet checked |
| `d` | derived: computed or imputed, never treated as an observation |
| `''` | missing: there is no number |

`ProvenancePanel` enforces the invariant "finite value ⇔ non-empty flag". Methods fit on `('v','m')`
by default; `use_flags=('v',)` restricts to verified data. `impute_panel(...)` returns a new panel
whose filled cells are flagged `d`; it refuses to overwrite a `v`/`m` observation unless asked
explicitly. The hold-out harness scores only `v` cells by default, so a method is never graded
against a number we supplied.

## The ladder

```python
from impute import ProvenancePanel, make_imputer

p = ProvenancePanel(entities, years, values)        # or from_long(records)
for name in ('linear', 'loglinear', 'scurve', 'cohort', 'kalman', 'amelia'):
    filled = p.with_fill(make_imputer(name).fit(p).predict())
```

| rung | class | what it does | intervals / draws |
|---|---|---|---|
| 1 | `LinearInterpolator` | straight line between nearest observed years | — |
| 2 | `LogLinearInterpolator` | straight line in log space (constant growth), linear fallback on non-positive segments | — |
| 3 | `LogitSCurve` | per-entity logit trend, bounded to `[lower, upper]` (default `[0,100]`); the S-curve rung for rates | — |
| 4 | `CohortBackcast` | cohort-replacement identity for attainment: recover each entering cohort's schooling from the observed aggregate means, then integrate the cohort series into gaps and out of span; `cohort_attainment()` exposes the recovered cohort nodes. Documented approximation: Barro-Lee file has the adult mean only; `replacement_years=40` sets the adult-life horizon. | — |
| 5 | `KalmanSmoother` | local linear trend observed with noise, batched over countries, RTS smoother; pooled hyperparameters by maximum likelihood (or `hyper=(q_level, q_slope, R)`); predictive intervals at `coverage` (default 0.90) | yes |
| 6 | `AmeliaMI` | chained equations on the deviation from the other countries' year mean, with the country's own lags and mean deviation; `M=20` draws with parametric uncertainty; Rubin pooling with the between-draw variance | yes / draws |

`predict(where=...)` fills an arbitrary boolean mask; the default fills every non-observation cell.
`ImputationResult` carries `values`, `where`, `method`, and, when available, `lower`/`upper`
(bounds), `draws` (multiple imputations) and `nominal` coverage.

## Hold-out harness

```python
from impute import holdout
rep = holdout(panel, methods=['linear', 'kalman', 'amelia'],
              gap_lengths=(1, 2, 3, 5, 10), n_replicates=3, seed=0)
print(rep.table('mae'))        # method x gap length
print(rep.coverage_table())    # interval coverage vs nominal, for the interval methods
```

Blocks of 1, 2, 3, 5 and 10 consecutive years are deleted from a damaged copy of the panel (with
anchors on both sides, no overlapping blocks), every method is refit, and the deleted cells are
scored. Only `v` cells are scored by default (`score_flags=`), and `score_transform=` allows
scoring a levels panel in log error. See `report.py` for the B11 markdown report.

## Run

```bash
python -m unittest engine.test_impute -v      # 35 fast tests, ~2 s (from the project root)
python -m engine.impute                       # B11 hold-out validation report (markdown)
python -m engine.impute --replicates 5 --datasets pwt,attainment,barro_lee
```

Data loaders (`from impute import data`): `load_pwt`, `load_attainment`, `load_barro_lee`,
`load_ilostat`, `load_learning_scores`, plus `near_complete` and `log_panel` helpers. The files are
read from `analysis/public_data/data/`.
