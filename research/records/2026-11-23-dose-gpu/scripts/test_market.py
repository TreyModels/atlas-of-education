"""How big is the marriage-market approximation, and does it go away?

The GPU engine replaces the original's serial random-permutation market with a priority claim, twice
(or more) per year.  That is an approximation, so the right question is whether it converges to the
serial market as the number of claim rounds grows.  This script holds the parameter vector and the
host-side schooling imputation fixed, runs 200 seeds of the original CPU model and 200 seeds of the
GPU engine at 1-4 rounds, and reports the marriage-age gap with a confidence interval.

It also reports total fertility and share married by 18 so a reader can see the bias is specific to
the marriage-market channel rather than a general shift in the simulation.
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
RES = os.environ.get("RESULTS", "../results"); os.makedirs(RES, exist_ok=True)
import dosecore as dc
from engine import GPUDose, targets_array, make_spec
import model as M

PAN = json.load(open(next(c for c in ["../data/panel.json", "data/panel.json"] if os.path.exists(c))))
ISO = ["PHL", "CHN", "EGY"]
NSEED = 200
SCEN = 0
TR = json.load(open(next(c for c in ["../data/truth_A.json", "data/truth_A.json"] if os.path.exists(c))))
P = np.array(TR["theta"])
FC = 0.0
YEARS = list(range(1980, 2011, 5))

# ---- CPU: the ORIGINAL serial model, 200 seeds per country
cpu = {iso: {g: [] for g in ("tfr", "smam", "m18", "asfr")} for iso in ISO}
preps = {}
t0 = time.time()
for iso in ISO:
    pc = PAN["countries"][iso]
    PW, PM, wcell, gdp, Zc, dosen = M.prepare(pc, P, np.random.default_rng(4242), SCEN)
    preps[iso] = dict(PW=PW, PM=PM, wcell=wcell, gdp=gdp, Zc=Zc, dosen=dosen, pc=pc)
    for s in range(NSEED):
        S = M.summaries(M.simulate(pc, P, SCEN, 70_000 + s, FC, nW=12, tmax=2012))
        for g in cpu[iso]: cpu[iso][g].append([S[g][y] for y in YEARS])
print("cpu done %.1fs" % (time.time() - t0), flush=True)

# ---- GPU: same prepared inputs, one seed per run, several round counts
seeds = np.arange(70_000, 70_000 + NSEED, dtype=np.uint64)
out = {}
for rounds in (1, 2, 3, 4):
    eng = GPUDose(nW=12, seed=1, max_runs=len(ISO) * NSEED, tmax=2012)
    eng.rounds = rounds
    specs, order = [], []
    for iso in ISO:
        for s in range(NSEED):
            specs.append(dict(prep=preps[iso], P=P, fc=FC, gap=preps[iso]["pc"]["age_gap"]))
            order.append((iso, s))
    eng.load(specs)
    sv = np.concatenate([seeds for _ in ISO])
    acc = eng.run(SCEN, seeds=sv)
    S = targets_array(acc)
    gpu = {iso: {g: [] for g in ("tfr", "smam", "m18", "asfr")} for iso in ISO}
    for k, (iso, s) in enumerate(order):
        for g, key in (("tfr", "tfr"), ("smam", "smam"), ("m18", "m18"), ("asfr", "asfr1519")):
            gpu[iso][g].append([S[key][y][k] for y in YEARS])
    r = {}
    for iso in ISO:
        for g in ("tfr", "smam", "m18", "asfr"):
            c = np.array(cpu[iso][g]); q = np.array(gpu[iso][g])
            cm, qm = np.nanmean(c, 0), np.nanmean(q, 0)
            se = np.sqrt(np.nanvar(c, 0) / NSEED + np.nanvar(q, 0) / NSEED)
            d = qm - cm
            r[f"{iso}_{g}"] = dict(diff=d.round(4).tolist(), t=(d / se).round(2).tolist(),
                                   mean_abs=float(np.nanmean(np.abs(d))),
                                   max_abs=float(np.nanmax(np.abs(d))),
                                   ci95=float(1.96 * np.nanmean(se)),
                                   t_avg=float(np.nanmean(d / se)))
        # pooled over the three countries, the headline number
    for g in ("tfr", "smam", "m18", "asfr"):
        ds = np.concatenate([r[f"{iso}_{g}"]["diff"] for iso in ISO])
        ts = np.concatenate([r[f"{iso}_{g}"]["t"] for iso in ISO])
        r[f"pooled_{g}"] = dict(diff=float(np.nanmean(ds)), t=float(np.nanmean(ts)),
                                max_abs=float(np.nanmax(np.abs(ds))))
    out[str(rounds)] = r
    print("rounds=%d pooled: " % rounds + " ".join(
        f"{g} {r['pooled_' + g]['diff']:+.4f} (t={r['pooled_' + g]['t']:+.2f})" for g in ("tfr", "smam", "m18", "asfr")),
        flush=True)

json.dump(dict(nseed=NSEED, countries=ISO, years=YEARS, scen="A", fc=FC, params=P.tolist(),
               result=out), open(os.path.join(RES, "market_bias.json"), "w"), indent=1)
print("wrote", os.path.join(RES, "market_bias.json"))
