"""Benchmark for the dependence diagnostics in Section 6.6 (review 2026-11-24).

What would 272 INDEPENDENT null-share series of length 400 give for the statistics the paper reports?
Reports mean |r|, share of positive pairs, max |r|, Li-Ji (2005) M_eff and the number of principal components for 90% of
the variance, averaged over 200 simulated matrices (seed 20261124).  Output: results/independence_benchmark.json
"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REC = os.path.dirname(HERE)
rng = np.random.default_rng(20261124)
R, M, REPS = 400, 272, 200
iu = np.triu_indices(M, 1)
def li_ji(C):
    ev = np.abs(np.linalg.eigvalsh(C))
    return float(np.sum((ev >= 1).astype(float) + (ev - np.floor(ev))))
rows = []
for _ in range(REPS):
    C = np.corrcoef(rng.standard_normal((R, M)), rowvar=False)
    v = C[iu]
    ev = np.sort(np.linalg.eigvalsh(C))[::-1]
    rows.append((np.abs(v).mean(), (v > 0).mean(), np.abs(v).max(), li_ji(C), int(np.searchsorted(np.cumsum(ev) / ev.sum(), 0.9) + 1)))
a = np.array(rows)
out = dict(draws=R, links=M, replications=REPS,
           mean_abs_r=dict(mean=float(a[:, 0].mean()), sd=float(a[:, 0].std())),
           share_positive=dict(mean=float(a[:, 1].mean()), sd=float(a[:, 1].std())),
           max_abs_r=dict(mean=float(a[:, 2].mean()), sd=float(a[:, 2].std())),
           li_ji_m_eff=dict(mean=float(a[:, 3].mean()), sd=float(a[:, 3].std())),
           pcs_for_90pct=dict(mean=float(a[:, 4].mean()), sd=float(a[:, 4].std())),
           observed=dict(mean_abs_r=0.041, share_positive=0.51, max_abs_r=0.44, li_ji_m_eff=157, pcs_for_90pct=162))
os.makedirs(os.path.join(REC, "results"), exist_ok=True)
json.dump(out, open(os.path.join(REC, "results", "independence_benchmark.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
