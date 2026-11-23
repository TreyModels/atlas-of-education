#!/usr/bin/env python3
"""Is the positive sign of "later female marriage age -> smaller future fertility
fall" an artefact of the estimator controlling for the STARTING fertility level?

The outcome is the ten-year change in births per woman and the regressor is the
level of female mean age at marriage at the start year.  The estimator (as in
full_matrix_trends.py) also controls for the starting fertility level.  Because
the starting level is negatively correlated with marriage age between countries,
that control can push the coefficient positive mechanically.

This script re-runs the same edge with and without the starting-level control,
with and without country trends, and also with the outcome replaced by the
future LEVEL of fertility (so the starting level is not on the left-hand side).
"""
import json
import numpy as np
from edge_marriage import S, build_rows, CTRL

EDGES = ["smam_f", "smam_gap", "nevermar_f_4549", "coresid_60plus"]


def dm(a, g):
    s = np.bincount(g, weights=a)
    c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit_variant(rows, trend, keep_level=True, future_level=False):
    if trend:
        cnt = {}
        for r in rows:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
        rows = [r for r in rows if cnt[r[0]] >= 4]
    if len(rows) < 150 or len({r[0] for r in rows}) < 10:
        return None
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    yr = np.array([r[1] for r in rows])
    gy = (yr // 10) * 10
    if future_level:
        yv = np.array([r[2] + r[3] for r in rows], float)   # y(t+10)
    else:
        yv = np.array([r[2] for r in rows], float)          # change
    xv = np.array([r[4] for r in rows], float)
    ylev = np.array([r[3] for r in rows], float)
    nctrl = len(rows[0]) - 5
    cs = [np.array([r[5 + j] for r in rows], float) for j in range(nctrl)]
    cols = [xv] + ([ylev] if keep_level else []) + cs
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, k], gi) for k in range(X.shape[1])])
    X = np.column_stack([dm(X[:, k], gy) for k in range(X.shape[1])])
    Y = dm(dm(yv, gi), gy)
    b = np.linalg.lstsq(X.T @ X, X.T @ Y, rcond=None)[0]
    u = Y - X @ b
    XtX = X.T @ X
    meat = np.zeros_like(XtX)
    for c in np.unique(gi):
        m = gi == c
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    Vb = np.linalg.pinv(XtX) @ meat @ np.linalg.pinv(XtX)
    return dict(b=float(b[1]), se=float(np.sqrt(max(Vb[1, 1], 0))),
                n=len(yv), nc=len(ui))


if __name__ == "__main__":
    out = {}
    for x in EDGES:
        if x not in S:
            continue
        rows = build_rows(x, "fertility", "grid10")
        for trend in (False, True):
            for keep in (True, False):
                r = fit_variant(rows, trend, keep_level=keep)
                out[f"{x}|trend={trend}|start_level_control={keep}"] = r
            r = fit_variant(rows, trend, keep_level=True, future_level=True)
            out[f"{x}|trend={trend}|outcome=future_level"] = r
    json.dump(out, open("/root/work/undata/results_nolevel.json", "w"), indent=1)
    for k, v in out.items():
        print(f"{k:58s} " + (f"b={v['b']:+.4f} se={v['se']:.4f} n={v['n']}" if v else "n/a"))
