#!/usr/bin/env python3
"""E1: does fertility respond to the LEVEL of child mortality or to its VOLATILITY?

Design (pre-registered in research/records/2026-11-23-mechanisms/EXPERIMENTS.md, E1):
for every country and every year t, decompose under-five mortality into a local linear
trend (the slow LEVEL) and the residual dispersion around it (VOLATILITY), using only
information available up to t (trailing 10-year window; no look-ahead). Then run the
project's within-country lead-lag estimator: ten-year change in births per woman on the
starting level of the mortality measure, with country effects, decade effects, income
logged, urbanisation controlled, country-clustered errors, with and without a
country-specific straight-line trend.

Specifications: level only; volatility only; both; plus (secondary) the recent shock and
a relative-volatility version. Falsifiers: circular-shift permutation within country,
country placebo for the volatility series, observed-rows-only (we use the observed panel
only), and a minimum detectable effect for every coefficient.

Outputs out/level_vol.json and printed tables.
"""
import json, os
import numpy as np

DATA = "/root/work/data"
OUT = "/root/work/level_vol/out"
meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i for i, m in meta.items()
       if len(i) == 3 and m.get("region", "").strip() != "Aggregates"}


def load(name):
    d = {(r[0], int(r[1])): float(r[2]) for r in
         json.load(open(os.path.join(DATA, name + ".json"))) if r[2] is not None}
    return {k: v for k, v in d.items() if k[0] in REG}


U5 = load("u5mr")
TFR = load("fertility")
GDP = {k: float(np.log(max(v, 1.0))) for k, v in load("gdppc_log").items()}
URB = load("urban")
print(f"series: u5mr {len(U5)}, fertility {len(TFR)}, income {len(GDP)}, urban {len(URB)}")

WINDOW = 10          # trailing years used to estimate trend and volatility
HORIZON = 10         # ten-year change in fertility (as in the matrix)
MIN_T, MAX_T = 1969, 2014   # need t-9>=1960 and t+10<=2024

LEVEL, VOL, SHOCK, VOLREL = {}, {}, {}, {}
byc = {}
for (i, t) in U5:
    byc.setdefault(i, []).append((t, U5[(i, t)]))
for i, lst in byc.items():
    lst.sort()
    years = [t for t, _ in lst]
    vals = [v for _, v in lst]
    for k, t in enumerate(years):
        if t < MIN_T or t > MAX_T:
            continue
        win = [(years[j], vals[j]) for j in range(k + 1) if years[j] >= t - WINDOW + 1]
        if len(win) < 8:
            continue
        xs = np.array([w[0] - t for w in win], float)   # years relative to t: -9..0
        ys = np.array([w[1] for w in win], float)
        b, a = np.polyfit(xs, ys, 1)
        res = ys - (a + b * xs)
        lvl = float(a)                       # fitted level at t (x=0)
        vol = float(np.std(res, ddof=1)) if len(res) > 2 else None
        if lvl <= 0 or vol is None:
            continue
        LEVEL[(i, t)] = lvl
        VOL[(i, t)] = vol
        SHOCK[(i, t)] = float(vals[k] - lvl)
        VOLREL[(i, t)] = vol / lvl
print(f"derived: level {len(LEVEL)}, volatility {len(VOL)}")

# ---- rows for the estimator ----
CTR = ["income", "urban"]


def build(xnames):
    rows = []
    for (i, t), yt in TFR.items():
        if t < MIN_T or t > MAX_T or (i, t + HORIZON) not in TFR:
            continue
        xs = []
        for xn in xnames:
            src = {"level": LEVEL, "vol": VOL, "shock": SHOCK, "volrel": VOLREL}[xn]
            if (i, t) not in src:
                xs = None
                break
            xs.append(src[(i, t)])
        if xs is None:
            continue
        if (i, t) not in GDP or (i, t) not in URB:
            continue
        row = [i, t, TFR[(i, t + HORIZON)] - yt, yt] + xs + [GDP[(i, t)], URB[(i, t)]]
        rows.append(row)
    return rows


def dm(a, g):
    s = np.bincount(g, weights=a)
    c = np.bincount(g)
    return a - (s / np.maximum(c, 1))[g]


def fit_multi(rows, k, trend):
    """rows: [iso, t, dy, y_level, x1..xk, ctrls]. Returns b, se per x plus n/nc."""
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
    cols = [np.array([r[4 + j] for r in rows], float) for j in range(k)]
    cols.append(np.array([r[3] for r in rows], float))          # starting level of y
    nctrl = len(rows[0]) - 4 - k
    cols += [np.array([r[4 + k + j] for r in rows], float) for j in range(nctrl)]
    if trend:
        for j in range(len(ui)):
            cols.append(((gi == j) * yr).astype(float))
    X = np.column_stack([np.ones(len(yv))] + cols)
    X = np.column_stack([dm(X[:, c], gi) for c in range(X.shape[1])])
    X = np.column_stack([dm(X[:, c], gy) for c in range(X.shape[1])])
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
    se = np.sqrt(np.maximum(np.diag(Vb)[1:1 + k], 0))
    return dict(b=[float(x) for x in b[1:1 + k]], se=[float(x) for x in se],
                n=len(yv), nc=len(ui), n_decades=int(len(set(gy))))


SPECS = {
    "level_only": ["level"],
    "vol_only": ["vol"],
    "both": ["level", "vol"],
    "shock_only": ["shock"],
    "volrel_only": ["volrel"],
}


def run_specs(rows_by_spec):
    out = {}
    for name, xnames in SPECS.items():
        rows = rows_by_spec[name]
        for trend in (False, True):
            r = fit_multi(rows, len(xnames), trend)
            out[f"{name}|{'trend' if trend else 'fe'}"] = r
            if r:
                parts = " ".join(f"{xn}={bb:+.5f} (se {ss:.5f})"
                                 for xn, bb, ss in zip(xnames, r["b"], r["se"]))
                print(f"{name:12s} {'trend' if trend else 'FE   ':6s} {parts} "
                      f"n={r['n']} countries={r['nc']} decades={r['n_decades']}")
    return out


if __name__ == "__main__":
    print("\n=== main specifications (10-year change in births per woman) ===")
    rows_by_spec = {name: build(xn) for name, xn in SPECS.items()}
    out = {}
    out["main"] = run_specs(rows_by_spec)

    # multicollinearity diagnostics for the joint specification
    rows = rows_by_spec["both"]
    lv = np.array([r[4] for r in rows], float)
    vo = np.array([r[5] for r in rows], float)
    print(f"\ncorr(level, volatility) raw = {np.corrcoef(lv, vo)[0, 1]:.3f}")
    out["corr_level_vol"] = float(np.corrcoef(lv, vo)[0, 1])

    # ---- falsifier 1: circular-shift permutation within country ----
    def circ_shift(src):
        byc = {}
        for (i, t), v in src.items():
            byc.setdefault(i, []).append((t, v))
        outd = {}
        for i, lst in byc.items():
            lst.sort()
            vals = [v for _, v in lst]
            if len(vals) > 1:
                k = int(np.random.default_rng().integers(1, len(vals)))
                vals = list(np.roll(np.array(vals), k))
            for (t, _), v in zip(lst, vals):
                outd[(i, t)] = float(v)
        return outd

    rng = np.random.default_rng(20261123)
    perm = {}
    for target in ("level", "vol"):
        base = out["main"]["both|trend"]
        idx = 0 if target == "level" else 1
        coeff = base["b"][idx]
        orig = dict(LEVEL if target == "level" else VOL)
        target_dict = LEVEL if target == "level" else VOL
        null = []
        for _ in range(200):
            target_dict.clear()
            target_dict.update(circ_shift(orig))
            try:
                r = fit_multi(build(["level", "vol"]), 2, True)
            finally:
                target_dict.clear()
                target_dict.update(orig)
            if r:
                null.append(abs(r["b"][idx]))
        null = np.array(null)
        perm[target] = dict(actual=abs(coeff), p=float((null >= abs(coeff)).mean()),
                            q95=float(np.percentile(null, 95)), draws=len(null))
        print(f"circular-shift permutation {target}: |b|={abs(coeff):.5f} "
              f"p={perm[target]['p']:.3f} null q95={perm[target]['q95']:.5f} "
              f"({perm[target]['draws']} draws)")
    out["permutation"] = perm

    # ---- falsifier 2: country placebo for volatility ----
    years_with_vol = {}
    for (i, t) in VOL:
        years_with_vol.setdefault(t, []).append(i)
    base = out["main"]["both|trend"]
    actual = abs(base["b"][1])
    orig_vol = dict(VOL)
    null = []
    for _ in range(200):
        placebo = {}
        for t, isos in years_with_vol.items():
            vals = [VOL[(i, t)] for i in isos]
            perm_isos = rng.permutation(isos)
            for i, v in zip(perm_isos, vals):
                placebo[(i, t)] = v
        VOL.clear(); VOL.update(placebo)
        try:
            r = fit_multi(build(["level", "vol"]), 2, True)
        finally:
            VOL.clear(); VOL.update(orig_vol)
        if r:
            null.append(abs(r["b"][1]))
    null = np.array(null)
    out["country_placebo"] = dict(actual=actual, p=float((null >= actual).mean()),
                                  q95=float(np.percentile(null, 95)), draws=len(null))
    print(f"country placebo (volatility): |b|={actual:.5f} "
          f"p={out['country_placebo']['p']:.3f} null q95={out['country_placebo']['q95']:.5f}")

    # ---- MDE = 2.802 * se for every coefficient ----
    mde = {}
    for key, r in out["main"].items():
        if r:
            mde[key] = [round(2.802 * s, 5) for s in r["se"]]
    out["mde_80_95"] = mde
    print("\nMDE (80% power, 95% two-sided = 2.802 x se):")
    for k, v in mde.items():
        print(f"  {k:20s} {v}")

    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "level_vol.json"), "w"), indent=1)
    print(f"\nwrote {OUT}/level_vol.json")
