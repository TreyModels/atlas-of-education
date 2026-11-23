"""Standalone callable interface to the GPU schooling-dose life-course engine.

    summaries = simulate(parameters, countries, scen=0, nW=12, seed=7, tmax=2012)

`parameters` is a [n, 31] array (uniform in [0,1] or the actual values? -> use values), `countries`
is a list of panel country codes, and the return value is a dict of numpy arrays:
  tfr[n, years], asfr1519[n, years], smam[n, years], m18[n, years], afb[n, years],
  coh[n, 14, 7, 8]  (cohort aggregates: weight, births by 30, by 35, parity, childless, married,
                     age at first birth, ever-first-birth weight)
plus 'fb' (the country-effect index that was used per country and draw).

Deterministic for a given seed and a PINNED BATCH LAYOUT.  Each woman's random stream is keyed on her
position within the launch and each man's on the number of women in the launch, so changing how a fixed set
of runs is grouped changes the random numbers each run receives: the same twelve parameter draws gave total
fertility differences of up to 1.13 births and mean marriage age differences of up to 1.74 years when
launched as one batch versus batches of 5, 7 and 12 (audited in the cuda-scale record, determinism_v2.json).
Operational rule: reproduce a run by pinning the batch size (this module's `batch` argument) and recording
it with the results.  Two instances with the same seed and the same layout are bit-identical per woman.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import GPUDose, targets_array, make_spec
import dosecore as dc

_PANEL = os.environ.get("DOSE_PANEL", "data/panel.json")


def load_panel(path=None):
    import json
    return json.load(open(path or _PANEL))


def simulate(theta, countries, scen=0, nW=12, seed=7, tmax=2012, fc=0.0, panel=None, batch=192):
    """theta: [n,31] actual parameter values; countries: list of ISO3 codes (one run each).
    fc: scalar or [n, len(countries)] country effects."""
    theta = np.atleast_2d(np.asarray(theta, float))
    n = theta.shape[0]; nc = len(countries)
    PAN = panel or load_panel()
    fc = np.asarray(fc, float)
    if fc.ndim == 0: fc = np.full((n, nc), float(fc))
    nruns = n * nc
    steps = max(1, min(batch, nruns))
    eng = GPUDose(nW=nW, seed=seed, max_runs=steps, tmax=tmax)
    out = {k: [] for k in ("tfr", "asfr1519", "smam", "m18", "afb", "coh")}
    fb = np.zeros((n, nc))
    for r0 in range(0, nruns, steps):
        idx = [(i, k) for i in range(n) for k in range(nc)][r0:r0 + steps]
        specs = []
        for (i, k) in idx:
            pc = PAN["countries"][countries[k]]
            specs.append(make_spec(pc, theta[i], scen, fc[i, k], pc["age_gap"], 7, i * nc + k))
        eng.load(specs); acc = eng.run(scen)
        S = targets_array(acc)
        for g in ("tfr", "asfr1519", "smam", "m18", "afb"):
            out[g].append(np.array([[S[g][y][j] for y in sorted(S[g])] for j in range(len(idx))]))
        out["coh"].append(acc["coh"])
        fb.flat[r0:r0 + len(idx)] = fc.reshape(-1)[r0:r0 + len(idx)]
    for g in out: out[g] = np.concatenate(out[g], 0)
    out["years"] = np.array(sorted(targets_array(eng.collect())["tfr"].keys()))
    out["fb"] = fb
    return out


if __name__ == "__main__":
    PAN = load_panel(); FIT = PAN["FIT"]
    rng = np.random.default_rng(0)
    th = dc.LO + rng.random((3, dc.D_)) * (dc.HI - dc.LO)
    r = simulate(th, FIT[:4], scen=0, nW=12, seed=7)
    print({k: (v.shape if hasattr(v, "shape") else v) for k, v in r.items()})
    print("tfr sample:", np.round(r["tfr"][0, -5:], 3), "m18:", np.round(r["m18"][0, :3], 3))
    r2 = simulate(th, FIT[:4], scen=0, seed=7)
    print("determinism (identical, nans equal):",
          bool(np.allclose(r["tfr"], r2["tfr"], equal_nan=True) and np.allclose(r["m18"], r2["m18"], equal_nan=True)))
