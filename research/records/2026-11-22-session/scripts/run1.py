#!/usr/bin/env python3
"""Run 1: lag race. Does fertility fall AFTER tertiary enrolment crosses a threshold,
or was it already falling (quantity-quality) before?

Spec: TFR_ict = a_i + g_t + sum_k b_k D_ik + e, base k=-1, country-clustered SE.
Two-way FE absorbs country level and global year trend, so b_k is deviation from
the world fertility trend in the k years around crossing.
"""
import gzip, json, os, sys
import numpy as np

SRC = "/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
KMIN, KMAX = -15, 30


def load(name):
    d = json.load(gzip.open(os.path.join(SRC, name + ".json.gz")))
    return {(r[0], int(r[1])): float(r[2]) for r in d if r[2] is not None}


def crossing(ter, iso_years, thr):
    """first year ter >= thr with an earlier observation below thr (not left-censored)"""
    yr = sorted(y for (i, y) in iso_years)
    if not yr:
        return None
    vals = [(y, ter[(iso_years[0][0], y)]) for y in yr if (iso_years[0][0], y) in ter]
    if not vals:
        return None
    vals.sort()
    seen_below = False
    for y, v in vals:
        if v < thr:
            seen_below = True
        elif seen_below and v >= thr:
            return y
    return None


def build(thr=20.0, shift=0, min_pre=3):
    ter = load("ter"); tfr = load("fertility")
    isos = sorted({i for (i, y) in ter})
    rows = []
    crossed = {}
    for iso in isos:
        ys = [(iso, y) for (i, y) in tfr if i == iso]
        if len(ys) < 20:
            continue
        c = crossing(ter, ys, thr)
        if c is None:
            continue
        c += shift
        crossed[iso] = c
        npre = sum(1 for y in range(c - 10, c) if (iso, y) in tfr)
        if npre < min_pre:
            continue
        for (i, y), v in ((k, v) for k, v in tfr.items() if k[0] == iso):
            k = y - c
            if KMIN <= k <= KMAX:
                rows.append((iso, y, k, v))
    return rows, crossed


def ols_cluster(rows):
    isos = sorted({r[0] for r in rows})
    years = sorted({r[1] for r in rows})
    ks = sorted({r[2] for r in rows if r[2] != -1})
    ii = {c: n for n, c in enumerate(isos[1:])}
    yi = {y: n for n, y in enumerate(years[1:])}
    ki = {k: n for n, k in enumerate(ks)}
    n = len(rows)
    X = np.zeros((n, 1 + len(ii) + len(yi) + len(ki)))
    X[:, 0] = 1.0
    y = np.zeros(n)
    for r, (iso, yr, k, v) in enumerate(rows):
        if iso in ii: X[r, 1 + ii[iso]] = 1.0
        if yr in yi: X[r, 1 + len(ii) + yi[yr]] = 1.0
        if k in ki: X[r, 1 + len(ii) + len(yi) + ki[k]] = 1.0
        y[r] = v
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ y, rcond=None)[0]
    u = y - X @ b
    meat = np.zeros_like(XtX)
    start = 0
    order = np.argsort([r[0] for r in rows], kind="stable")
    Xs, us = X[order], u[order]
    groups = [rows[i][0] for i in order]
    g0 = 0
    for g in range(1, len(groups) + 1):
        if g == len(groups) or groups[g] != groups[g0]:
            Xg = Xs[g0:g]; ug = us[g0:g]
            s = Xg.T @ ug
            meat += np.outer(s, s)
            g0 = g
    XtXi = np.linalg.pinv(XtX)
    V = XtXi @ meat @ XtXi
    off = 1 + len(ii) + len(yi)
    out = {}
    for k in ks:
        j = off + ki[k]
        out[k] = (b[j], np.sqrt(max(V[j, j], 0.0)))
    return out, len(isos), n


def summarize(out, label, thr, ncty):
    print(f"\n=== {label} (threshold {thr:g}% tertiary GER) | {ncty} countries, base k=-1")
    print("  k    TFR relative to world trend   (cluster SE)")
    for k in sorted(out):
        b, se = out[k]
        star = "***" if abs(b) > 2.58 * se and se > 0 else ("**" if abs(b) > 1.96 * se and se > 0 else ("*" if abs(b) > 1.64 * se and se > 0 else ""))
        print(f" {k:+4d}   {b:+.3f}  ({se:.3f}) {star}")
    pre = [out[k][0] for k in range(-10, -1) if k in out]
    post = [out[k][0] for k in range(0, 21) if k in out]
    print(f"  mean b, k=-10..-2 (pre): {np.mean(pre):+.3f}")
    print(f"  mean b, k=0..+20 (post): {np.mean(post):+.3f}")
    print(f"  b at k=+15: {out.get(15, (float('nan'),0))[0]:+.3f} ; k=+20: {out.get(20, (float('nan'),0))[0]:+.3f}")


if __name__ == "__main__":
    for thr in (20.0, 15.0, 30.0):
        rows, crossed = build(thr=thr)
        out, ncty, n = ols_cluster(rows)
        summarize(out, f"MAIN", thr, ncty)
    # placebo: move every crossing 10 years earlier
    rows, _ = build(thr=20.0, shift=-10)
    out, ncty, n = ols_cluster(rows)
    summarize(out, "PLACEBO (crossing moved 10y earlier)", 20.0, ncty)
