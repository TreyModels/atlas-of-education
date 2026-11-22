#!/usr/bin/env python3
"""Global sensitivity of the Triad necessity result (Monte Carlo over parameter space).

Question: the round-2b result says removing households or employers collapses tertiary schooling and removing
the state shrinks it. Is that true across plausible parameter space, or only at the defaults?

Design (fixed before running):
  - Latin hypercube over PARAMS below, each varied from LO x default to HI x default (bounded where noted).
  - For each sample and seed: baseline + three early single-actor knockouts (from year 0, full strength).
  - End state = mean of years 110-139 of mean_years, share_tertiary, cred_hire_share, formal_share.
  - An actor is "necessary" in a sample if removing it cuts end-state tertiary share by >= 50% vs baseline.
  - Samples where baseline tertiary < 0.02 are reported separately ("no pipeline emerged").
Usage:
  python triad_gsa.py chunk K NCHUNKS [--samples 2000 --seeds 2 --N 1500]
  python triad_gsa.py summarize
"""
import argparse, json, os, sys
import numpy as np
from scipy.stats import qmc, spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from triad.model import make, run, DEFAULTS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "gsa")
# (name, lo multiplier, hi multiplier)
PARAMS = [
    ("urban_speed", 0.5, 1.5), ("kin0", 0.7, 1.1), ("formal0", 0.5, 1.5), ("formal1", 0.5, 1.5),
    ("y_sigma", 0.6, 1.4), ("subsist", 0.6, 1.4), ("borrow", 0.25, 2.0), ("crra", 0.6, 1.6), ("disc", 0.97, 1.03),
    ("theta_a", 0.5, 1.5), ("theta_s", 0.0, 3.0), ("value_mult", 0.8, 1.2), ("wage_mult", 0.8, 1.2),
    ("c_ref", 0.5, 2.0), ("trust_bonus", 0.0, 2.0), ("c_test", 0.5, 2.0), ("test_noise", 0.5, 2.0),
    ("c_read", 0.5, 2.0), ("floor_margin", 0.9, 1.3), ("tax", 0.5, 1.5), ("capacity", 0.5, 1.5),
    ("switch_p", 0.5, 1.5), ("cost_scale", 0.5, 2.0),
]
ACTORS = ["household", "employer", "state"]


def _sample_params(u):
    kw = {}
    for (name, lo, hi), x in zip(PARAMS, u):
        m = lo + (hi - lo) * x
        if name == "cost_scale":
            kw["cost"] = [c * m for c in DEFAULTS["cost"]]
        elif name == "disc":
            kw["disc"] = min(0.995, DEFAULTS["disc"] * m)
        elif name == "kin0":
            kw["kin0"] = min(0.99, DEFAULTS["kin0"] * m)
        else:
            kw[name] = DEFAULTS[name] * m
    return kw


def _end(S):
    y = np.asarray(S["year"]); k = (y >= 110) & (y <= 139)
    return {v: float(np.mean(np.asarray(S[v])[k])) for v in ("mean_years", "share_tertiary", "cred_hire_share", "formal_share")}


def chunk(k, n, samples, seeds, N):
    U = qmc.LatinHypercube(d=len(PARAMS), seed=20261122).random(samples)
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for i in range(k, samples, n):
        kw = _sample_params(U[i])
        for s in range(seeds):
            rec = dict(sample=i, seed=s, u=U[i].tolist())
            rec["baseline"] = _end(run(make(seed=1000 * i + s, N=N, **kw)))
            for a in ACTORS:
                rec[a] = _end(run(make(seed=1000 * i + s, N=N, knock={a: 0}, **kw)))
            rows.append(rec)
    with open(os.path.join(OUT, f"chunk_{k:03d}.json"), "w") as f:
        json.dump(rows, f)
    print(f"chunk {k}: {len(rows)} sample-seeds", flush=True)


def summarize():
    rows = []
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("chunk_"):
            rows += json.load(open(os.path.join(OUT, fn)))
    base = np.array([r["baseline"]["share_tertiary"] for r in rows])
    emerged = base >= 0.02
    L = [f"TRIAD GLOBAL SENSITIVITY: {len(rows)} sample-seeds ({len(set(r['sample'] for r in rows))} parameter samples).",
         f"Pipeline emerged (baseline end tertiary >= 0.02): {emerged.mean():.0%} of runs.", ""]
    out = dict(n=len(rows), emerged_share=float(emerged.mean()), actors={})
    U = np.array([r["u"] for r in rows])
    for a in ACTORS:
        kt = np.array([r[a]["share_tertiary"] for r in rows])
        ratio = np.where(base > 0, kt / np.maximum(base, 1e-9), np.nan)
        nec = (ratio <= 0.5) & emerged
        share_nec = float(nec[emerged].mean()) if emerged.any() else float("nan")
        # which parameters govern necessity: Spearman of tertiary ratio with each parameter, among emerged runs
        rho = {name: float(spearmanr(U[emerged, j], ratio[emerged]).correlation) for j, (name, *_ ) in enumerate(PARAMS)} if emerged.sum() > 10 else {}
        top = sorted(rho.items(), key=lambda kv: -abs(kv[1]))[:6]
        out["actors"][a] = dict(necessary_share_of_emerged=share_nec, median_ratio=float(np.nanmedian(ratio[emerged])),
                                q10_q90_ratio=[float(np.nanquantile(ratio[emerged], .1)), float(np.nanquantile(ratio[emerged], .9))],
                                top_drivers_spearman=top)
        L.append(f"{a:10s} necessary in {share_nec:.0%} of emerged runs; tertiary after removal / baseline: median {np.nanmedian(ratio[emerged]):.2f} "
                 f"(10-90%: {np.nanquantile(ratio[emerged], .1):.2f}-{np.nanquantile(ratio[emerged], .9):.2f})")
        L.append("           governed most by: " + ", ".join(f"{n} ({r:+.2f})" for n, r in top))
    rho_emerge = {name: float(spearmanr(U[:, j], base).correlation) for j, (name, *_) in enumerate(PARAMS)}
    out["emergence_drivers"] = sorted(rho_emerge.items(), key=lambda kv: -abs(kv[1]))[:8]
    L += ["", "Baseline tertiary share governed most by: " + ", ".join(f"{n} ({r:+.2f})" for n, r in out["emergence_drivers"]),
          "", "Read: 'necessary' = removing the actor cuts end-state tertiary by half or more. A share near 100% means the",
          "necessity result is robust across the sampled space; a low share means it depends on particular parameter values.",
          "Spearman signs: positive = higher parameter values make the knockout LESS damaging."]
    json.dump(out, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd"); ap.add_argument("k", nargs="?", type=int); ap.add_argument("n", nargs="?", type=int)
    ap.add_argument("--samples", type=int, default=2000); ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--N", type=int, default=1500)
    a = ap.parse_args()
    chunk(a.k, a.n, a.samples, a.seeds, a.N) if a.cmd == "chunk" else summarize()
