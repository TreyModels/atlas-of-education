#!/usr/bin/env python3
"""Run 1b: is there a BREAK at the crossing, or just a straight line?

The event-study dummies above look linear across the whole window. A linear path
means the crossing marks where fertility passes the world trend, not a change in
slope. Test directly: piecewise-linear hinge at knot K.

TFR = a_i + g_t + c1*k + c2*max(0,k-K) + e   (cluster SE by country)
c2 < 0 and significant => decline steepens after K (framework's prediction).
"""
import gzip, json, os
import numpy as np

SRC = "/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"


def load(n):
    d = json.load(gzip.open(os.path.join(SRC, n + ".json.gz")))
    return {(r[0], int(r[1])): float(r[2]) for r in d if r[2] is not None}


def rows_for(thr, kmin=-15, kmax=30, shift=0):
    ter, tfr = load("ter"), load("fertility")
    isos = sorted({i for (i, y) in ter})
    out = []
    for iso in isos:
        ys = sorted(y for (i, y) in tfr if i == iso)
        if len(ys) < 20:
            continue
        vals = [(y, ter[(iso, y)]) for y in ys if (iso, y) in ter]
        if not vals:
            continue
        below, c = False, None
        for y, v in vals:
            if v < thr:
                below = True
            elif below and v >= thr and c is None:
                c = y
        if c is None:
            continue
        c += shift
        npre = sum(1 for y in range(c - 10, c) if (iso, y) in tfr)
        if npre < 3:
            continue
        for y in ys:
            k = y - c
            if kmin <= k <= kmax:
                out.append((iso, y, k, tfr[(iso, y)]))
    return out


def cluster_fit(rows, cols, kappa):
    isos = sorted({r[0] for r in rows}); years = sorted({r[1] for r in rows})
    ii = {c: i for i, c in enumerate(isos[1:])}; yi = {y: i for i, y in enumerate(years[1:])}
    n = len(rows)
    P = 1 + len(ii) + len(yi) + len(cols)
    X = np.zeros((n, P)); y = np.zeros(n)
    for r, (iso, yr, k, v) in enumerate(rows):
        X[r, 0] = 1
        if iso in ii: X[r, 1 + ii[iso]] = 1
        if yr in yi: X[r, 1 + len(ii) + yi[yr]] = 1
        for j, f in enumerate(cols):
            X[r, 1 + len(ii) + len(yi) + j] = f(k)
        y[r] = v
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ y, rcond=None)[0]
    u = y - X @ b
    order = np.argsort([r[0] for r in rows], kind="stable")
    Xs, us = X[order], u[order]; gs = [rows[i][0] for i in order]
    meat = np.zeros_like(XtX); g0 = 0
    for g in range(1, len(gs) + 1):
        if g == len(gs) or gs[g] != gs[g0]:
            s = Xs[g0:g].T @ us[g0:g]
            meat += np.outer(s, s); g0 = g
    XtXi = np.linalg.pinv(XtX)
    V = XtXi @ meat @ XtXi
    off = 1 + len(ii) + len(yi)
    res = [(b[off + j], np.sqrt(max(V[off + j, off + j], 0))) for j in range(len(cols))]
    return res, len(isos), n


if __name__ == "__main__":
    print("HINGE TESTS: TFR = country FE + year FE + c1*k + c2*max(0,k-K)")
    print("c2<0 & significant => decline STEEPENS after k=K (framework predicts K=15..20)\n")
    for thr in (15.0, 20.0, 30.0):
        rows = rows_for(thr)
        _, ncty, n = cluster_fit(rows, [lambda k: k], 0)
        print(f"--- threshold {thr:g}% : {ncty} countries, {n} country-years")
        for K in (0, 5, 10, 15, 20):
            (c1, s1), (c2, s2) = cluster_fit(rows, [lambda k: k, (lambda K: (lambda k: max(0.0, k - K)))(K)], K)[0]
            t = c2 / s2 if s2 > 0 else float("nan")
            flag = "STEEPENS" if (c2 < 0 and abs(t) > 1.96) else ("flattens" if (c2 > 0 and abs(t) > 1.96) else "no break")
            print(f"  knot k={K:+3d}: pre-slope {c1:+.4f} ({s1:.4f})  change {c2:+.4f} ({s2:.4f})  t={t:+.2f}  {flag}")
        print()
    print("PLACEBO (crossing moved 10y earlier, threshold 20%):")
    rows = rows_for(20.0, shift=-10)
    for K in (0, 10, 15, 20):
        (c1, s1), (c2, s2) = cluster_fit(rows, [lambda k: k, (lambda K: (lambda k: max(0.0, k - K)))(K)], K)[0]
        print(f"  knot k={K:+3d}: pre-slope {c1:+.4f}  change {c2:+.4f} ({s2:.4f})  t={c2/s2 if s2>0 else float('nan'):+.2f}")
