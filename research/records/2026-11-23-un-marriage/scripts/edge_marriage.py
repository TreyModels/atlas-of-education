#!/usr/bin/env python3
"""Do the UN marriage-timing and living-arrangement series add anything to the
schooling -> fertility edge once country trends are in?

Reuses the estimator in
research/records/2026-11-23-handoff-run/scripts/full_matrix_trends.py
(edge(): 10-year change in y regressed on level of x at the start year, country
fixed effects, decade effects, income logged and urbanisation controlled,
country-clustered standard errors, optional country-specific linear trends).

Two adaptations are needed because the UN series are survey/census years, not
annual:
  grid10   : x is the sparse survey series, y is annual (fertility).  Uses the
             actual survey year t for x and the annual value of y at t and t+10.
  survey10 : y is the sparse survey series, x is annual (schooling).  Uses real
             pairs of surveys 8-13 years apart; the window is the actual survey
             gap, never an interpolated grid.

Rules being respected:
  * marriage age is on the causal path from schooling to fertility, so it is
    NEVER a control in a schooling -> fertility regression.  The marriage
    variables enter only as the x of their own edges (association / outcome).
  * no interpolation anywhere in the estimation sample.
"""
import json, os, sys
import numpy as np

PANEL = "/root/work/data"
UN = "/root/work/undata/out"
CTRL = ["gdppc_log", "urban"]
PANEL_VARS = ["electricity", "wage_emp", "lsc", "sec", "ter", "prm_cmp",
              "gdppc_log", "urban", "tax", "agri_va", "emp_agri", "flfp",
              "life_exp", "u5mr", "gpi_sec", "gpi_ter", "fertility"]
UN_VARS = ["smam_f", "smam_m", "smam_gap", "nevermar_f_4549", "nevermar_m_4549",
           "coresid_60plus", "coresid_60plus_f", "multigen_60plus", "alone_60plus"]

meta = json.load(open(os.path.join(PANEL, "meta.json")))
REG = {i for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}


def load(name):
    for base, ext in ((PANEL, ".json"), (PANEL, ".json.gz"), (UN, ".json")):
        p = os.path.join(base, name + ext)
        if os.path.exists(p):
            import gzip
            op = gzip.open(p) if ext.endswith(".gz") else open(p)
            d = {(r[0], int(r[1])): float(r[2]) for r in json.load(op)
                 if r[2] is not None}
            return {k: v for k, v in d.items() if k[0] in REG}
    return {}


S = {}
for v in PANEL_VARS + UN_VARS:
    d = load(v)
    if d:
        S[v] = d
AVAIL = sorted(S)
print("series available:", [(v, len(S[v])) for v in AVAIL], flush=True)


def dm(a, g):
    s = np.bincount(g, weights=a)
    c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit(rows, trend, xname, yname):
    """rows: [iso, t, dy, y_level, x_level, ctrl...] -> (b, se, n, ncountry)."""
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
    yv = np.array([r[2] for r in rows], float)
    xv = np.array([r[4] for r in rows], float)
    ylev = np.array([r[3] for r in rows], float)
    nctrl = len(rows[0]) - 5
    cs = [np.array([r[5 + j] for r in rows], float) for j in range(nctrl)]
    cols = [xv, ylev] + cs
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
    se = float(np.sqrt(max(Vb[1, 1], 0)))
    return dict(b=float(b[1]), se=se, n=len(yv), nc=len(ui),
                n10=int(len({int(g) for g in gy})), years=[int(yr.min()), int(yr.max())])


def build_rows(xn, yname, mode):
    """Build regression rows for one edge. Returns [] if the pair is impossible."""
    X, Y = S[xn], S[yname]
    ctrls = [c for c in CTRL if c in S and c not in (xn, yname)]
    rows = []
    if mode == "grid10":
        # x sparse (survey years); y annual. Change in y from survey year t to t+10.
        for (i, t), v in Y.items():
            if (i, t + 10) not in Y or (i, t) not in X:
                continue
            if not all((i, t) in S[c] for c in ctrls):
                continue
            rows.append([i, t, Y[(i, t + 10)] - v, v, X[(i, t)]] +
                        [S[c][(i, t)] for c in ctrls])
    else:
        # y sparse: real pairs of surveys 8-13 years apart; x level at start year.
        byc = {}
        for (i, t), v in Y.items():
            byc.setdefault(i, []).append((t, v))
        for i, lst in byc.items():
            lst.sort()
            for t1, v1 in lst:
                cand = [(abs((t2 - t1) - 10), t2, v2) for t2, v2 in lst
                        if 8 <= t2 - t1 <= 13]
                if not cand:
                    continue
                cand.sort()
                _, t2, v2 = cand[0]
                if (i, t1) not in X:
                    continue
                if not all((i, t1) in S[c] for c in ctrls):
                    continue
                rows.append([i, t1, v2 - v1, v1, X[(i, t1)]] +
                            [S[c][(i, t1)] for c in ctrls])
    return rows


def grid10(x, y, trend):
    if x not in S or y not in S:
        return None
    return fit(build_rows(x, y, "grid10"), trend, x, y)


def survey10(x, y, trend):
    if x not in S or y not in S:
        return None
    return fit(build_rows(x, y, "survey10"), trend, x, y)


def report(x, y, mode):
    out = {}
    for trend in (False, True):
        r = (grid10 if mode == "grid10" else survey10)(x, y, trend)
        out["trend" if trend else "fe"] = r
        tag = "country trends" if trend else "country FE  "
        if r is None:
            print(f"  {x:16s} -> {y:16s} [{tag}] NOT ESTIMABLE (sample too small)")
        else:
            sig = "*" if r["se"] > 0 and abs(r["b"] / r["se"]) > 1.96 else " "
            print(f"  {x:16s} -> {y:16s} [{tag}] b={r['b']:+.4f} se={r['se']:.4f} "
                  f"t={r['b']/r['se'] if r['se'] else float('nan'):+.2f}{sig} "
                  f"n={r['n']} countries={r['nc']} decades={r['n10']} "
                  f"years={r['years']}")
    return out


EDGES = [
    # (x, y, mode)  -- marriage/living arrangement as the x of its own edge
    ("smam_f", "fertility", "grid10"),
    ("smam_gap", "fertility", "grid10"),
    ("nevermar_f_4549", "fertility", "grid10"),
    ("coresid_60plus", "fertility", "grid10"),
    ("multigen_60plus", "fertility", "grid10"),
    # schooling as x, marriage as outcome (the massification direction)
    ("sec", "smam_f", "survey10"),
    ("sec", "nevermar_f_4549", "survey10"),
    ("sec", "smam_gap", "survey10"),
    ("lsc", "smam_f", "survey10"),
    ("sec", "coresid_60plus", "survey10"),
    # reference edges on the panel (no marriage data involved)
    ("sec", "fertility", "grid10"),
    ("ter", "fertility", "grid10"),
]

if __name__ == "__main__":
    print("\n=== EDGES (level of x -> 10-year change in y) ===")
    res = {}
    for x, y, mode in EDGES:
        if x not in S or y not in S:
            print(f"  {x} -> {y}: series missing, skipped")
            continue
        res[f"{x}->{y}"] = report(x, y, mode)
    json.dump(res, open("/root/work/undata/results_edges.json", "w"), indent=1)
    print("\nwrote /root/work/undata/results_edges.json")
