# Prior sensitivity results

Both screens used 256 independent prior draws with seed 20261124 and the same four-block likelihood structure. The posterior weights are highly concentrated in both runs, especially under the expanded prior. Treat summaries as an importance-screening diagnostic, not stable posterior estimates.

| Prior | ESS | ESS / draws | Holdout GER macro RMSE | Persistence RMSE |
|---|---:|---:|---:|---:|
| main | 5.94 | 0.0232 | 9.645 | 6.600 |
| expanded | 1.77 | 0.0069 | 7.065 | 6.600 |

Expanded ranges reduce ESS from 5.94 to 1.77 and improve the posterior-mean holdout RMSE relative to the main prior, but persistence remains better in both. This is material prior sensitivity and the screen is under-resolved at 256 draws. Model sigmoid overflow warnings appeared on some expanded-prior trajectories; the model output remained finite and the runs completed, but extreme-draw numerical behavior should be inspected before treating the expanded range as reliable.

The holdout was previously inspected in the v5 protocol, so these are retrospective comparisons. No mechanism or causal verdict follows from these scores.
