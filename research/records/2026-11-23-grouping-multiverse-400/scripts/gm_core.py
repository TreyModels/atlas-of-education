#!/usr/bin/env python3
"""Grouping multiverse: core. Panel, groupings, fast version of the full-matrix estimator.

The estimator reproduces full_matrix_trends.py (10-year-ahead change, own starting level,
controls log GDP per head and urban, country fixed effects, decade fixed effects, clustered SEs,
with or without a linear trend per country). Country-level terms (mean, trend) are removed once
per edge on the full panel; only the decade demeaning and the fit are redone per country subset.
gdppc_log.json holds LEVELS: we take the log.
"""
import json, os, gzip
import numpy as np

DATA = os.environ.get("GM_DATA", "/root/work/data")
VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp", "gdppc_log",
        "urban", "tax", "agri_va", "emp_agri", "flfp", "life_exp", "u5mr",
        "gpi_sec", "gpi_ter", "fertility"]
CTRL = ["gdppc_log", "urban"]
Y0, Y1 = 1940, 2025
T = Y1 - Y0 + 1


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
ISOS = sorted(REG)
CI = {i: n for n, i in enumerate(ISOS)}
C = len(ISOS)

A = {}
for v in VARS:
    a = np.full((C, T), np.nan)
    for (i, t), val in load(v).items():
        if i in CI and Y0 <= t <= Y1:
            if v == "gdppc_log":
                val = np.log(val) if val > 0 else np.nan
            a[CI[i], t - Y0] = val
    A[v] = a

# ---------------- continent (meta has none) ----------------
NAF = {"DZA", "EGY", "LBY", "MAR", "TUN", "DJI"}
CASIA = {"ARM", "AZE", "GEO", "KAZ", "KGZ", "TJK", "TKM", "UZB", "TUR"}
OCE = {"AUS", "NZL", "FJI", "PNG", "SLB", "VUT", "WSM", "TON", "KIR", "FSM", "MHL", "PLW", "NRU",
       "TUV", "ASM", "GUM", "MNP", "PYF", "NCL"}


def continent(i):
    r = REG[i]
    if r.startswith("Sub-Saharan"): return "Africa"
    if r.startswith("Latin") or r == "North America": return "Americas"
    if r.startswith("Middle East"): return "Africa" if i in NAF else "Asia"
    if r.startswith("Europe"): return "Asia" if i in CASIA else "Europe"
    if r.startswith("East Asia"): return "Oceania" if i in OCE else "Asia"
    return "Asia"


# ---------------- edges ----------------
def build_edge(x, y, trend):
    ctrls = [c for c in CTRL if c not in (x, y)]
    ay = A[y]
    y0 = ay[:, :-10]; dy = ay[:, 10:] - y0
    cols = [A[x][:, :-10], y0] + [A[c][:, :-10] for c in ctrls]
    ok = np.isfinite(dy) & np.isfinite(y0)
    for c in cols:
        ok &= np.isfinite(c)
    ci, ti = np.nonzero(ok)
    yr = (ti + Y0).astype(float)
    if trend:
        cnt = np.bincount(ci, minlength=C)
        keep = cnt[ci] >= 4
        ci, ti, yr = ci[keep], ti[keep], yr[keep]
    M = np.column_stack([c[ci, ti] for c in cols] + [dy[ci, ti]])

    def dm(a):
        n = np.bincount(ci, minlength=C)
        return a - (np.bincount(ci, weights=a, minlength=C) / np.maximum(n, 1))[ci]
    yrc = dm(yr)
    den = np.bincount(ci, weights=yrc ** 2, minlength=C)
    out = np.empty_like(M)
    for k in range(M.shape[1]):
        v = dm(M[:, k])
        if trend:
            sl = np.bincount(ci, weights=yrc * v, minlength=C) / np.maximum(den, 1e-12)
            v = v - sl[ci] * yrc
        out[:, k] = v
    gy = ((yr // 10) * 10).astype(int)
    gy = gy - gy.min()
    return dict(ci=ci, gy=gy, X=out[:, :-1].copy(), Y=out[:, -1].copy())


PAIRS = [(x, y) for x in VARS for y in VARS if x != y]
SPECS = [(x, y, t) for (x, y) in PAIRS for t in (0, 1)]
EDGES = [build_edge(x, y, t) for (x, y, t) in SPECS]
NE = len(SPECS)


def fit_edge(E, mem):
    sel = mem[E["ci"]]
    n = int(sel.sum())
    if n < 150:
        return None
    ci = E["ci"][sel]
    if np.count_nonzero(np.bincount(ci, minlength=C)) < 10:
        return None
    gy = E["gy"][sel]
    X = E["X"][sel]; Y = E["Y"][sel]
    ng = gy.max() + 1
    cnt = np.maximum(np.bincount(gy, minlength=ng), 1)
    X = X - (np.stack([np.bincount(gy, weights=X[:, k], minlength=ng) for k in range(X.shape[1])], 1) / cnt[:, None])[gy]
    Y = Y - (np.bincount(gy, weights=Y, minlength=ng) / cnt)[gy]
    XtX = X.T @ X
    P = np.linalg.pinv(XtX)
    b = P @ (X.T @ Y)
    u = Y - X @ b
    S = np.stack([np.bincount(ci, weights=X[:, k] * u, minlength=C) for k in range(X.shape[1])], 1)
    V = P @ (S.T @ S) @ P
    se = float(np.sqrt(max(V[0, 0], 0)))
    nc = int(np.count_nonzero(np.bincount(ci, minlength=C)))
    return float(b[0]), se, n, nc


def fit_cell(mem):
    """returns arrays b, se, n, nc of length NE (nan if not estimable) and the count of fits."""
    b = np.full(NE, np.nan); se = np.full(NE, np.nan)
    n = np.zeros(NE, int); nc = np.zeros(NE, int); k = 0
    for j, E in enumerate(EDGES):
        r = fit_edge(E, mem)
        if r is not None:
            b[j], se[j], n[j], nc[j] = r
            k += 1
    return b, se, n, nc, k


# ---------------- baseline country characteristics ----------------
def base(v, yr=1990, win=7):
    a = A[v]; out = np.full(C, np.nan)
    for c in range(C):
        ys = np.nonzero(np.isfinite(a[c]))[0] + Y0
        if len(ys):
            j = np.argmin(np.abs(ys - yr))
            if abs(ys[j] - yr) <= win:
                out[c] = a[c, ys[j] - Y0]
    return out


BASE = {v: base(v) for v in ["fertility", "gdppc_log", "sec", "lsc", "urban", "agri_va", "emp_agri",
                             "tax", "u5mr", "life_exp", "electricity"]}


def crossing_year(thr=2.1):
    f = A["fertility"]; out = np.full(C, np.nan)
    for c in range(C):
        ys = np.nonzero(np.isfinite(f[c]))[0]
        if len(ys) < 10: continue
        below = ys[f[c, ys] < thr]
        out[c] = (below[0] + Y0) if len(below) else 9999
    return out


CROSS = crossing_year()


def kmeans(Xm, k, rng, restarts=20):
    best = None
    for _ in range(restarts):
        cen = [Xm[rng.integers(len(Xm))]]
        for _ in range(k - 1):
            d = np.min([((Xm - c) ** 2).sum(1) for c in cen], 0)
            cen.append(Xm[rng.choice(len(Xm), p=d / d.sum())] if d.sum() > 0 else Xm[rng.integers(len(Xm))])
        cen = np.array(cen)
        for _ in range(100):
            lab = ((Xm[:, None] - cen[None]) ** 2).sum(2).argmin(1)
            new = np.array([Xm[lab == j].mean(0) if (lab == j).any() else cen[j] for j in range(k)])
            if np.allclose(new, cen): break
            cen = new
        inert = ((Xm - cen[lab]) ** 2).sum()
        if best is None or inert < best[0]: best = (inert, lab)
    return best[1]


def gfe(Z, G, rng, restarts=30):
    """Grouped fixed effects (Bonhomme-Manresa): group-specific time profiles, masked Lloyd."""
    M = np.isfinite(Z); Z0 = np.where(M, Z, 0.0); best = None
    for _ in range(restarts):
        lab = rng.integers(G, size=len(Z))
        for _ in range(100):
            th = np.zeros((G, Z.shape[1]))
            for g in range(G):
                m = lab == g
                if m.any():
                    th[g] = Z0[m].sum(0) / np.maximum(M[m].sum(0), 1)
            cost = np.stack([(M * (Z0 - th[g]) ** 2).sum(1) for g in range(G)], 1)
            new = cost.argmin(1)
            if (new == lab).all(): break
            lab = new
        tot = cost[np.arange(len(Z)), lab].sum()
        if best is None or tot < best[0]: best = (tot, lab)
    return best[1]


def make_groupings():
    """list of dict(name, family, key, ordinal, groups=[(label, tag, member_idx array)])."""
    G = []
    ids = np.arange(C)

    def add(name, family, key, ordinal, labels, tags, members):
        G.append(dict(name=name, family=family, key=key, ordinal=ordinal,
                      groups=[(l, t, np.array(m, int)) for l, t, m in zip(labels, tags, members)]))

    def cat(name, family, vals):
        labs = sorted({v for v in vals if v is not None})
        add(name, family, name, False, labs, [f"{name}={l}" for l in labs],
            [[c for c in ids if vals[c] == l] for l in labs])

    cat("World Bank region", "geography", [REG[i] for i in ISOS])
    cat("Continent", "geography", [continent(i) for i in ISOS])
    cat("World Bank income group", "geography", [meta[i]["income"] for i in ISOS])

    def ordtag(var, k, K):
        if K == 2: return f"{var}:{'low' if k == 0 else 'high'}"
        return f"{var}:{'low' if k == 0 else 'high' if k == K - 1 else 'mid'}"

    def quant(var, family, vals, Ks, key=None):
        ok = ids[np.isfinite(vals)]
        order = ok[np.argsort(vals[ok], kind="stable")]
        for K in Ks:
            parts = np.array_split(order, K)
            add(f"{var} x{K}", family, key or var, True, [f"{var} group {k+1}/{K}" for k in range(K)],
                [ordtag(var, k, K) for k in range(K)], parts)

    quant("log income 1990", "income", BASE["gdppc_log"], [2, 3, 4, 5])
    quant("fertility 1990", "demography", BASE["fertility"], [2, 3, 4, 5])
    quant("child mortality 1990", "demography", BASE["u5mr"], [2, 3, 4])
    quant("life expectancy 1990", "demography", BASE["life_exp"], [3])
    # timing of crossing replacement
    for name, cuts in [("replacement crossing x3", [1990, 2010]), ("replacement crossing x4", [1975, 1990, 2010])]:
        ok = ids[np.isfinite(CROSS)]
        bins = np.digitize(CROSS[ok], cuts, right=True)
        K = len(cuts) + 1
        add(name, "demography", "crossing", True, [f"crossing bin {k+1}/{K}" for k in range(K)],
            [ordtag("crossing time(early=low)", k, K) for k in range(K)], [ok[bins == k] for k in range(K)])
    quant("secondary completion 1990", "schooling", BASE["sec"], [2, 3, 4, 5])
    quant("lower-secondary completion 1990", "schooling", BASE["lsc"], [2, 3, 4])
    quant("agriculture share of output 1990", "economy", BASE["agri_va"], [2, 3, 4])
    quant("urban share 1990", "economy", BASE["urban"], [2, 3, 4])
    quant("agricultural employment share 1990", "economy", BASE["emp_agri"], [3])
    quant("electricity access 1990", "economy", BASE["electricity"], [3])
    quant("tax share 1990", "institutions", BASE["tax"], [2, 3, 4])

    # k-means on baseline profile
    prof = np.column_stack([BASE[v] for v in ["fertility", "gdppc_log", "urban", "sec", "u5mr", "life_exp"]])
    ok = ids[np.isfinite(prof[:, [0, 1, 2, 4, 5]]).all(1)]
    P = prof[ok].copy()
    med = np.nanmedian(P, 0)
    P = np.where(np.isfinite(P), P, med)
    P = (P - P.mean(0)) / P.std(0)
    rng = np.random.default_rng(1)
    fert = BASE["fertility"]
    for k in range(2, 7):
        lab = kmeans(P, k, rng)
        order = sorted(range(k), key=lambda j: np.nanmean(fert[ok[lab == j]]))
        add(f"k-means k={k}", "kmeans", f"kmeans{k}", False,
            [f"cluster {r+1}/{k} (by fertility)" for r in range(k)],
            [ordtag("kmeans-fertility-order", r, k) for r in range(k)], [ok[lab == j] for j in order])
    # GFE on fertility and on log income trajectories
    for var, a, y0_, y1_ in [("fertility", A["fertility"], 1960, 2020), ("log income", A["gdppc_log"], 1990, 2020)]:
        Z = a[:, y0_ - Y0:y1_ - Y0 + 1]
        ok = ids[np.isfinite(Z).sum(1) >= (y1_ - y0_) * 0.6]
        for g in range(2, 7):
            lab = gfe(Z[ok], g, np.random.default_rng(2))
            order = sorted(range(g), key=lambda j: np.nanmean(Z[ok[lab == j]]))
            add(f"GFE {var} G={g}", "gfe", f"gfe-{var}-{g}", False,
                [f"GFE class {r+1}/{g} (by {var})" for r in range(g)],
                [ordtag(f"gfe-{var}-order", r, g) for r in range(g)], [ok[lab == j] for j in order])
    return G


def mask(members):
    m = np.zeros(C, bool); m[members] = True
    return m


def random_version(G, rng):
    """Random partition per grouping with the same group sizes (and same covered countries).
    Groupings sharing a key (different cuts of one variable) share the random ordering."""
    keys = {}
    out = []
    for g in G:
        cov = np.concatenate([m for _, _, m in g["groups"]])
        ck = g["key"] + "|" + str(len(cov))
        if ck not in keys:
            keys[ck] = rng.permutation(cov)
        perm = keys[ck]
        if not g["ordinal"]:
            perm = rng.permutation(cov)
        sizes = [len(m) for _, _, m in g["groups"]]
        cut = np.cumsum([0] + sizes)
        out.append([perm[cut[k]:cut[k + 1]] for k in range(len(sizes))])
    return out
