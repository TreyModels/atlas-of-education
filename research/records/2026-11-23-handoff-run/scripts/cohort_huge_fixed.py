#!/usr/bin/env python3
"""HUGE version: schooling-as-individualisation, tested properly.

Components
  1. Coverage   : impute schooling within country so ~150+ countries survive
  2. Comparison : M0 (markets only) vs M1 (markets + schooling), fitted per country
  3. Validation : fit on all but the last two cohorts, predict them. Out of sample.
  4. Uncertainty: 500 bootstrap resamples over countries
  5. Power      : 400 simulated worlds per true alpha, to check the test can
                  detect a real schooling effect at all

If the design cannot detect a known alpha, a null on real data means nothing.
"""
import json, os, gzip, sys
import numpy as np
from multiprocessing import Pool

DATA = "/root/work/data"
STEP, Y0, Y1 = 5, 1965, 2015
GAMMA, THETA, PSI, ETA = 1.0, 0.55, 0.9, 0.55
GRID_A = [0.0, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
GRID_B = [0.0, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0]
NBOOT = 500
NSIM = 400


def load(n):
    p = os.path.join(DATA, n + ".json")
    if os.path.exists(p):
        return {(r[0], int(r[1])): float(r[2]) for r in json.load(open(p))}
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(gzip.open(p + ".gz"))}


def build():
    meta = json.load(open(os.path.join(DATA, "meta.json")))
    reg = {i: m["region"].strip() for i, m in meta.items()
           if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
    raw = {}
    for k in ("lsc", "urban", "fertility", "gdppc_log"):
        d = load(k)
        raw[k] = {kk: vv for kk, vv in d.items() if kk[0] in reg}
    return reg, raw


def paths(raw, reg):
    """per country: list of (lsc, urban, ly, fert), imputing schooling gaps"""
    out = {}
    years = list(range(Y0, Y1 + 1, STEP))
    for iso in sorted(reg):
        L = [(y, raw["lsc"][(iso, y)]) for y in years if (iso, y) in raw["lsc"]]
        if len(L) < 2:
            continue
        ly_ = [y for y, v in L]
        lv = [v for y, v in L]
        path = []
        for y in years:
            u = raw["urban"].get((iso, y))
            f = raw["fertility"].get((iso, y))
            g = raw["gdppc_log"].get((iso, y))
            if u is None or f is None or g is None:
                continue
            e = float(np.interp(y, ly_, lv))
            path.append((e, u, g, f))
        if len(path) >= 5:
            out[iso] = (reg[iso], path)
    return out


def run(path, alpha, beta):
    n0, y0 = path[0][3], path[0][2]
    I, prev_u, preds = 0.0, path[0][1], []
    for k, (e, u, ly, f) in enumerate(path):
        if k > 0:
            phi = 1 - np.exp(-e / 15.0)
            I += alpha * phi * (1 - I) + beta * (u - prev_u) / 100.0
            I = min(max(I, 0.0), 0.98)
        prev_u = u
        preds.append(max(n0 * np.exp(-GAMMA * I) ** THETA *
                         (1 + PSI * I) ** (-1) * (ly / y0) ** (-ETA), 0.2))
    return np.array(preds)


def fit_oos(iso, P):
    region, path = P[iso]
    obs = np.array([p[3] for p in path])
    k = len(path)
    if k < 6:
        return None
    tr, te = path[:-2], path[-2:]
    obs_tr = obs[:-2]
    o0 = np.array([p[3] for p in te])
    best = {}
    for sc, alphas in (("M0", [0.0]), ("M1", GRID_A)):
        b = (np.inf, 0.0, 0.0)
        for a in alphas:
            for bt in GRID_B:
                s = float(((run(tr, a, bt) - obs_tr) ** 2).mean())
                if s < b[0]:
                    b = (s, a, bt)
        pred = run(path, b[1], b[2])[-2:]
        best[sc] = (b[1], b[2], float(((pred - o0) ** 2).mean()))
    return dict(iso=iso, region=region, n=k,
                a1=best["M1"][0], b1=best["M1"][1],
                oos0=best["M0"][2], oos1=best["M1"][2])


PG = None


def fit_wrapper(k):
    return fit_oos(k, PG)


def sim_wrapper(x):
    return sim_world(x[0], x[1], PG)


def bootstrap(args):
    rng, idx, keys, res = args
    pick = [keys[i] for i in rng.integers(0, len(keys), len(keys))]
    o0 = np.array([res[k]["oos0"] for k in pick])
    o1 = np.array([res[k]["oos1"] for k in pick])
    return float(np.mean((o0 - o1) / np.maximum(o0, 1e-9)))


def sim_world(seed, alpha_true, P):
    """one synthetic panel with a known schooling effect, then the same test"""
    rng = np.random.default_rng(seed)
    keys = sorted(P)
    picks = list(rng.choice(keys, size=min(90, len(keys)), replace=False))
    fake = {}
    for k in picks:
        region, path = P[k]
        n0 = rng.uniform(3.0, 7.0); y0 = path[0][2]
        I, prev_u, pr = 0.0, path[0][1], []
        beta = rng.uniform(0.3, 1.2); alpha = alpha_true
        for j, (e, u, ly, f) in enumerate(path):
            if j > 0:
                phi = 1 - np.exp(-e / 15.0)
                I += alpha * phi * (1 - I) + beta * (u - prev_u) / 100.0
                I = min(max(I, 0.0), 0.98)
            prev_u = u
            n = n0 * np.exp(-GAMMA * I) ** THETA * (1 + PSI * I) ** (-1) * (ly / y0) ** (-ETA)
            pr.append((e, u, ly, max(n * np.exp(rng.normal(0, 0.12)), 0.2)))
        fake[k] = (region, pr)
    rr = [fit_oos(k, fake) for k in fake]
    rr = [r for r in rr if r]
    if not rr:
        return alpha_true, 0.0
    o0 = np.array([r["oos0"] for r in rr]); o1 = np.array([r["oos1"] for r in rr])
    return alpha_true, float(np.mean((o0 - o1) / np.maximum(o0, 1e-9)))


if __name__ == "__main__":
    reg, raw = build()
    P = paths(raw, reg)
    PG = P
    print(f"countries with usable cohort paths: {len(P)}", flush=True)

    with Pool(28) as p:
        res = [r for r in p.map(fit_wrapper, sorted(P), chunksize=4) if r]
    res = {r["iso"]: r for r in res}
    keys = sorted(res)
    print(f"countries fitted with out-of-sample test: {len(keys)}", flush=True)

    g = np.array([(res[k]["oos0"] - res[k]["oos1"]) / max(res[k]["oos0"], 1e-9) for k in keys])
    print("\n" + "=" * 82)
    print("OUT-OF-SAMPLE: DOES SCHOOLING IMPROVE PREDICTION OF THE LAST TWO COHORTS?")
    print("=" * 82)
    print(f"  median gain            : {100*np.median(g):+6.1f}%")
    print(f"  countries helped (>0)  : {100*np.mean(g>0.0):5.1f}%")
    print(f"  helped by >20%         : {100*np.mean(g>0.2):5.1f}%")
    print(f"  made worse (<0)        : {100*np.mean(g<0.0):5.1f}%")

    regs = {}
    for k in keys:
        regs.setdefault(res[k]["region"], []).append((res[k]["oos0"] - res[k]["oos1"]) / max(res[k]["oos0"], 1e-9))
    print("\n  by region (median out-of-sample gain):")
    for rg, v in sorted(regs.items(), key=lambda kv: -np.median(kv[1])):
        print(f"    {rg[:38]:40s} n={len(v):3d}  {100*np.median(v):+6.1f}%")

    print("\nbootstrapping over countries ({} draws):".format(NBOOT), flush=True)
    rng = np.random.default_rng(7)
    jobs = [(np.random.default_rng(7000 + b), None, keys, res) for b in range(NBOOT)]
    with Pool(28) as p:
        bs = p.map(bootstrap, jobs, chunksize=10)
    bs = np.array(bs)
    print(f"  mean gain {100*bs.mean():+.1f}%   95% CI [{100*np.percentile(bs,2.5):+.1f}%, "
          f"{100*np.percentile(bs,97.5):+.1f}%]")
    print(f"  P(the schooling channel helps) = {100*np.mean(bs>0):.1f}%")

    print(f"\nrecovery / power study: {NSIM} worlds per true alpha", flush=True)
    jobs = [(9000 + 10000 * ai + s, a, P) for ai, a in enumerate((0.0, 0.05, 0.15, 0.4)) for s in range(NSIM)]
    with Pool(28) as p:
        sims = p.map(sim_wrapper, jobs, chunksize=8)
    print(f"{'true alpha':>12s}{'median gain':>14s}{'share >0':>11s}{'share >10%':>12s}")
    for a in (0.0, 0.05, 0.15, 0.4):
        v = np.array([x[1] for x in sims if x[0] == a])
        print(f"{a:>12.2f}{100*np.median(v):>13.1f}%{100*np.mean(v>0):>10.0f}%{100*np.mean(v>0.1):>11.0f}%")
    json.dump({k: res[k] for k in keys}, open("/root/work/cohort_huge.json", "w"))
