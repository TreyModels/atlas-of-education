import os
#!/usr/bin/env python3
"""Bayesian analysis: which drivers earn their place, and how sure are we?

BMA1  onset year of the fertility transition (~60-90 countries), exact g-prior BMA
BMA2  10-year change in fertility, within country, exact g-prior BMA
HB    hierarchical model with country random intercepts (Gibbs), posterior P(beta>0)
"""
import json, os, gzip, itertools
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
rng = np.random.default_rng(4)

NAME = {"lsc": "girls finishing lower secondary", "sec": "secondary completion",
        "ter": "young people in higher ed", "gpi_ter": "women vs men in higher ed",
        "u5mr": "children dying before 5", "gdppc_log": "income per person",
        "flfp": "women in the labour force", "urban": "cities",
        "electricity": "homes with electricity"}
KEY = list(NAME)


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


V = {k: load(k) for k in KEY + ["fertility"]}
F = V["fertility"]
meta = json.load(open(os.path.join(DATA, "meta.json")))
real = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
for k in V:
    V[k] = {kk: vv for kk, vv in V[k].items() if kk[0] in real}

# ---------------- BMA machinery ----------------
def bma(Y, X, names, g=None):
    """exact BMA with Zellner g-prior, g = n (unit information); uniform model prior"""
    n = len(Y)
    g = n if g is None else g
    yc = Y - Y.mean()
    sst = (yc ** 2).sum()
    Z = (X - X.mean(0)) / X.std(0)
    k = X.shape[1]
    logs = []
    for r in range(k + 1):
        for S in itertools.combinations(range(k), r):
            if r == 0:
                logp = 0.0
            else:
                Zs = Z[:, S]
                beta, *_ = np.linalg.lstsq(Zs, yc, rcond=None)
                rss = ((yc - Zs @ beta) ** 2).sum()
                R2 = max(1e-12, 1 - rss / sst)
                logp = ((n - 1 - r) / 2) * np.log(1 + g) - ((n - 1) / 2) * np.log((1 + g) * (1 - R2))
                # (constant terms cancel across models)
            logs.append((logp, S))
    mx = max(l for l, _ in logs)
    w = np.array([np.exp(l - mx) for l, _ in logs])
    w = w / w.sum()
    pip = np.zeros(k)
    for wt, (_, S) in zip(w, logs):
        for j in S:
            pip[j] += wt
    order = np.argsort(-pip)
    print("   inclusion probability (how often the model wants it):")
    for j in order:
        bar = "#" * int(round(pip[j] * 40))
        print(f"     {NAME[names[j]]:34s} {pip[j]:.2f} {bar}")
    # best model
    bi = int(np.argmax(w))
    best = logs[bi][1]
    print("   most probable single model: " + (", ".join(NAME[names[j]] for j in best) if best else "(nothing)"))
    return pip


# ---------------- BMA 1: onset year ----------------
print("=" * 76)
print("BAYES 1   WHEN DOES THE FERTILITY FALL BEGIN?")
print("          outcome: the year a country first drops below 5 children per woman")
print("          predictors measured 20 years earlier")
print("=" * 76)
onsets = {}
for iso in {i for (i, y) in F}:
    for y in sorted(y for (i, y) in F if i == iso):
        if F[(iso, y)] < 5.0:
            if 1950 <= y <= 2020:
                onsets[iso] = y
            break
rows = []
for iso, y0 in onsets.items():
    rec = {}
    for c in ["lsc","sec","ter","gpi_ter","urban","gdppc_log","u5mr"]:
        for back in range(0, 11):
            if (iso, y0 - 20 - back) in V[c]:
                rec[c] = V[c][(iso, y0 - 20 - back)]
                break
    if len(rec) >= 7:
        rows.append((y0, rec))
print(f"  {len(rows)} countries with every predictor available")
if len(rows) >= 30:
    Y = np.array([r[0] for r in rows], float)
    K1 = ["lsc","sec","ter","gpi_ter","urban","gdppc_log","u5mr"]
    X = np.array([[r[1][c] for c in K1] for r in rows], float)
    bma(Y, X, K1)

# ---------------- BMA 2: 10-year change, within country ----------------
print()
print("=" * 76)
print("BAYES 2   WHAT TRACKS THE 10-YEAR FALL IN BIRTHS, COUNTRY BY COUNTRY?")
print("=" * 76)
rows = []
for (i, t), v in F.items():
    if (i, t + 10) not in F:
        continue
    if all((i, t) in V[c] for c in KEY):
        rows.append((i, F[(i, t + 10)] - v, [V[c][(i, t)] for c in KEY]))
print(f"  {len(rows)} country-decades, {len({r[0] for r in rows})} countries")
if len(rows) > 200:
    iso = [r[0] for r in rows]
    Y = np.array([r[1] for r in rows], float)
    X = np.array([r[2] for r in rows], float)
    # remove country means
    uq = {c: n for n, c in enumerate(sorted(set(iso)))}
    g = np.array([uq[c] for c in iso])
    def dm(a):
        if a.ndim == 1:
            return a - (np.bincount(g, weights=a) / np.bincount(g))[g]
        cnt = np.bincount(g)
        M = np.vstack([np.bincount(g, weights=a[:, j]) for j in range(a.shape[1])]).T / cnt[:, None]
        return a - M[g]
    Yd, Xd = dm(Y), dm(X)
    bma(Yd, Xd, KEY)

# ---------------- HB: hierarchical, country random intercepts ----------------
print()
print("=" * 76)
print("BAYES 3   HIERARCHICAL MODEL — each country gets its own baseline")
print("          10-yr change in births, country random intercepts, Gibbs sampler")
print("=" * 76)
if len(rows) > 200:
    n = len(Yd)
    Z = (Xd - Xd.mean(0)) / Xd.std(0)
    k = Z.shape[1]
    nj = int(g.max()) + 1
    Zx = np.column_stack([np.ones(n), Z])
    XtX = Zx.T @ Zx
    cnt = np.bincount(g, minlength=nj).astype(float)
    beta = np.zeros(k + 1)
    u = np.zeros(nj)
    sig2, tau2 = float(Yd.var()), float(Yd.var()) / 4
    keep = []
    for it in range(8000):
        adj = Yd - u[g]
        Vb = np.linalg.inv(XtX / sig2 + np.eye(k + 1) * 1e-8)
        mb = Vb @ (Zx.T @ adj / sig2)
        beta = rng.multivariate_normal(mb, Vb)
        r = Yd - Zx @ beta
        rj = np.bincount(g, weights=r, minlength=nj)
        prec = cnt / sig2 + 1.0 / tau2
        u = rng.normal(rj / sig2 / prec, 1.0 / np.sqrt(prec))
        rss = float(((r - u[g]) ** 2).sum())
        sig2 = 1.0 / rng.gamma(1.5 + n / 2.0, 1.0 / (1.0 + rss / 2.0))
        tau2 = 1.0 / rng.gamma(1.5 + nj / 2.0, 1.0 / (1.0 + float((u ** 2).sum()) / 2.0))
        if it >= 3000:
            keep.append(beta.copy())
    K = np.array(keep)
    print("   coefficient, 95% credible interval, probability the effect is positive")
    for j in range(k):
        s = K[:, j + 1]
        lo, hi = np.percentile(s, [2.5, 97.5])
        p = float(np.mean(s > 0))
        flag = "***" if (lo > 0 or hi < 0) else ""
        print(f"     {NAME[KEY[j]]:34s} {s.mean():+6.3f}  [{lo:+6.3f}, {hi:+6.3f}]  P(>0)={p:.2f} {flag}")
print("\ndone.")
