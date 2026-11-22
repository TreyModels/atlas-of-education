#!/usr/bin/env python3
"""Run 1c: the same event study, split by region.

Trey's claim is not that the mechanism fires everywhere at 20% -- it is that it fires
where the pipeline actually captured the female reproductive window (Japan, Thailand),
and has not fired where it hasn't (Philippines, Vietnam, Africa). A pooled estimate
averages exactly that heterogeneity away, so test it separately.
"""
import gzip, json, os, urllib.request
import numpy as np

SRC = "/var/minis/workspace/atlas/research/records/2026-11-22-massification-panel/sources/wdi_sweep"
CACHE = "/var/minis/workspace/wb_regions.json"


def load(n):
    d = json.load(gzip.open(os.path.join(SRC, n + ".json.gz")))
    return {(r[0], int(r[1])): float(r[2]) for r in d if r[2] is not None}


def regions():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    u = "https://api.worldbank.org/v2/country?format=json&per_page=400"
    d = json.load(urllib.request.urlopen(u, timeout=90))
    m = {}
    for c in d[1]:
        if c.get("region", {}).get("value"):
            m[c["id"]] = c["region"]["value"]
    json.dump(m, open(CACHE, "w"))
    return m


def rows_for(thr, keep):
    ter, tfr = load("ter"), load("fertility")
    out = []
    for iso in sorted({i for (i, y) in ter}):
        if not keep(iso):
            continue
        ys = sorted(y for (i, y) in tfr if i == iso)
        if len(ys) < 18:
            continue
        vals = [(y, ter[(iso, y)]) for y in ys if (iso, y) in ter]
        below, c = False, None
        for y, v in vals:
            if v < thr: below = True
            elif below and v >= thr and c is None: c = y
        if c is None: continue
        if sum(1 for y in range(c - 10, c) if (iso, y) in tfr) < 3: continue
        for y in ys:
            k = y - c
            if -15 <= k <= 30:
                out.append((iso, y, k, tfr[(iso, y)], c))
    return out


def fit(rows, K=None):
    isos = sorted({r[0] for r in rows}); years = sorted({r[1] for r in rows})
    ii = {c: i for i, c in enumerate(isos[1:])}; yi = {y: i for i, y in enumerate(years[1:])}
    n = len(rows)
    ncol = 1 + len(ii) + len(yi) + (2 if K is None else 2)
    X = np.zeros((n, ncol)); y = np.zeros(n)
    for r, (iso, yr, k, v, c) in enumerate(rows):
        X[r, 0] = 1
        if iso in ii: X[r, 1 + ii[iso]] = 1
        if yr in yi: X[r, 1 + len(ii) + yi[yr]] = 1
        o = 1 + len(ii) + len(yi)
        X[r, o] = k
        X[r, o + 1] = max(0.0, k - (K if K is not None else 0.0))
        y[r] = v
    XtX = X.T @ X
    b = np.linalg.lstsq(XtX, X.T @ y, rcond=None)[0]
    u = y - X @ b
    order = np.argsort([r[0] for r in rows], kind="stable")
    Xs, us = X[order], u[order]; gs = [rows[i][0] for i in order]
    meat = np.zeros_like(XtX); g0 = 0
    for g in range(1, len(gs) + 1):
        if g == len(gs) or gs[g] != gs[g0]:
            s = Xs[g0:g].T @ us[g0:g]; meat += np.outer(s, s); g0 = g
    XtXi = np.linalg.pinv(XtX); V = XtXi @ meat @ XtXi
    o = 1 + len(ii) + len(yi)
    return ((b[o], np.sqrt(max(V[o, o], 0))), (b[o + 1], np.sqrt(max(V[o + 1, o + 1], 0))), len(isos), n)


if __name__ == "__main__":
    reg = regions()
    groups = {
        "East Asia & Pacific": "East Asia & Pacific",
        "SE Asia only": ("SEA", ["IDN", "KHM", "LAO", "MMR", "MYS", "PHL", "THA", "VNM", "SGP", "TLS", "BRN"]),
        "Europe & Central Asia": "Europe & Central Asia",
        "Latin America & Carib.": "Latin America & Caribbean",
        "South Asia": "South Asia",
        "Sub-Saharan Africa": "Sub-Saharan Africa",
        "Middle East & N. Africa": "Middle East & North Africa",
    }
    print("HINGE K=+15, threshold 20% tertiary GER — by region")
    print("change<0 => decline steepens 15 years after crossing (framework's claim)\n")
    for label, spec in groups.items():
        if isinstance(spec, tuple):
            keep = lambda i, s=set(spec[1]): i in s
        else:
            keep = lambda i, r=spec: reg.get(i) == r
        rows = rows_for(20.0, keep)
        if len({r[0] for r in rows}) < 3:
            print(f"{label:26s} too few countries"); continue
        (c1, s1), (c2, s2), ncty, n = fit(rows, K=15)
        t = c2 / s2 if s2 > 0 else float("nan")
        flag = "STEEPENS" if (c2 < 0 and abs(t) > 1.96) else ("flattens" if (c2 > 0 and abs(t) > 1.96) else "-")
        print(f"{label:26s} n={ncty:3d}  pre-slope {c1:+.4f}  change {c2:+.4f} ({s2:.4f})  t={t:+5.2f}  {flag}")
        # latest post-period level
        if rows:
            late = [r[3] for r in rows if r[2] >= 20]
            print(f"{'':26s}        mean TFR at k>=20: {np.mean(late):.2f}" if late else "")
