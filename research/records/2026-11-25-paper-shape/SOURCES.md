# Claims → source map (Paper N4)

Every number in `PAPER.md` traces to a file in this record. Raw data: `data/wdi_*.json` (World Bank API,
pulled 25 Nov 2026 by `scripts/pull.sh`) and `data/wb_countries.json`. Analysis: `scripts/analysis.py`
(seed 20261125). Results: `results/shape_results.json`, `results/country_descriptors.csv`,
`results/country_shape_parameters.csv`, `figures/fig1–fig4`.

| number in the paper | value | where it lives |
|---|---|---|
| countries in the pull / transition sample | 217 / 105 | `shape_results.json` → `data.countries`, `data.transition_countries`; rule in `data.transition_rule` |
| functional-form winners | exponential 51, Gompertz 30, linear kink 15, logistic 7, spline 2 | `functional_forms.best_form_counts` |
| hold-out RMSE | exponential 0.31, Gompertz 0.36, linear kink 0.39, logistic 0.48 | `functional_forms.mean_holdout_rmse` |
| descriptor distributions (Table 2) | onset 1967 [1964–1970]; midpoint 1982 [1976–1990]; duration 35 [28–41]; speed 0.19 [0.157–0.232]; floor 1.95 [1.56–2.45]; curvature 1.38 [1.17–1.83] | `shape_descriptors` |
| path uniformity | cross-country SD 0.017; mean abs deviation 0.011; PC1 explains 100% | `path_uniformity` |
| clustering | k=2, silhouette 0.275, 0/500 random partitions ≥ real (p<0.01) | `clustering.k_best`, `.silhouette`, `.null_test` |
| class profiles (Table 3) | class 1 n=58: onset 1964.7, midpoint 1977.4, duration 37.2, speed 0.220, floor 1.68, curvature 1.89; class 2 n=47: 1972.8, 1990.7, 30.3, 0.194, 2.36, 1.26 | `clustering.cluster_profiles` |
| k=3 robustness | silhouette 0.239; three group means in §5.6 | computed from `country_descriptors.csv` with `KMeans(k=3, random_state=11)` |
| descriptor correlations (§5.6) | onset–midpoint 0.68; duration–speed −0.47; duration–curvature 0.51; floor–onset 0.46; floor–midpoint 0.51 | `country_descriptors.csv`, Pearson correlations |
| determinant coefficients (Table 4) | mortality lead 0.240 (0.036) n=101 → onset; 0.301 (0.046) → midpoint; −0.168 (0.068) → duration; −0.014 (0.004) → curvature; urban −0.052 (0.025) → onset, −0.146 (0.036) → midpoint; schooling lead 0.049 (0.041) n=90; schooling level −0.246 (0.097) n=30 → onset, +0.583 (0.200) → duration, +0.024 (0.009) → curvature | `determinants` (each cell), `covariate_coverage` |
| collapse-curve negative (Section 6) | 4,394 country–cohort points, 158 countries; pooled R² 0.78; country residual share 71.6%; slope F 46.4 (313, 3,717 df); residual SD 0.847 (11.2% of range); 0.434 after rescale | `research/scaling-2026-11-23` @ `fd691a6`, `research/records/2026-11-23-scaling/results/scaling_results.json` → `sections.collapse`; summarised in that record's README |

Figures: `fig1_fitted_shapes.png` (fitted forms), `fig2_clusters.png` (descriptor-space clusters), 
`fig3_distributions.png` (shape distributions), `fig4_norm_curves.png` (aligned paths and class means).

**Provenance note:** the raw WDI JSON files (~33 MB) are included in `data/` in this record; the analysis is
fully reproducible with `scripts/pull.sh` then `scripts/analysis.py`. No server data were used (box2 was
unavailable). Correlation is not causation anywhere in this paper.
