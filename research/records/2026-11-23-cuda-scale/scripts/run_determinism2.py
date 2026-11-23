"""Determinism audit, v2: separate true determinism from atomic-summation noise and from
batch-composition dependence.

The v1 test asked for bitwise-identical aggregate arrays across batch sizes.  That fails for a
benign reason (double atomicAdd sums in a scheduling-dependent order) and for a real one (the RNG
stream includes the *within-launch* run index, so splitting a population into different batch
sizes changes which random numbers each run receives).  This script measures both.
"""
import os, sys, time, gc
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupy as cp
from benchlib import (log, gpu_stat, free_pool, dump, compare, PAN, FIT, NW, WPR, TMAX,
                      array_digest, GPUDose, make_spec)
import dosecore as dc
import abm_dose

out = dict(job="cuda-scale determinism audit v2", gpu=gpu_stat(), nW=NW, women_per_run=WPR,
           questions=[])

rng = np.random.default_rng(0)
theta = dc.LO + rng.random((3, dc.D_)) * (dc.HI - dc.LO)
countries = FIT[:4]
nruns = theta.shape[0] * len(countries)
specs = []
for i in range(theta.shape[0]):
    for k, iso in enumerate(countries):
        pc = PAN["countries"][iso]
        specs.append(make_spec(pc, theta[i], 0, 0.0, pc["age_gap"], 7, i * len(countries) + k))


def state_run(spec_list, max_runs, seed=7, graph=True):
    eng = GPUDose(nW=NW, seed=seed, max_runs=max_runs, tmax=TMAX)
    eng.load(spec_list)
    acc = eng.run(0, use_graph=graph, state=True)
    st = acc["state"]
    del eng; gc.collect(); free_pool()
    return st, acc


# ---- Q1 true determinism: two identical fresh engines, same batch -------------------------
st_a, acc_a = state_run(specs, nruns)
st_b, acc_b = state_run(specs, nruns)
q1 = dict(question="same seed, same batch, two independent engine instances: repeatable?",
          per_woman_state={k: compare(st_a[k], st_b[k]) for k in st_a},
          device_aggregates={k: compare(acc_a[k], acc_b[k])
                             for k in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d", "coh")})
q1["per_woman_state_all_identical"] = all(v["bitwise_identical"] for v in q1["per_woman_state"].values())
q1["aggregates_max_abs_diff"] = max(v["max_abs_diff"] for v in q1["device_aggregates"].values())
out["questions"].append(q1)
log("Q1 same-batch repeat: per-woman state identical =", q1["per_woman_state_all_identical"],
    "max aggregate diff =", q1["aggregates_max_abs_diff"])

# ---- Q2 launch configuration: CUDA graph vs plain launches -------------------------------
st_g, acc_g = state_run(specs, nruns, graph=True)
st_p, acc_p = state_run(specs, nruns, graph=False)
q2 = dict(question="same seed/batch: CUDA-graph replay vs plain kernel launches",
          per_woman_state={k: compare(st_g[k], st_p[k]) for k in st_g},
          device_aggregates={k: compare(acc_g[k], acc_p[k])
                             for k in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d", "coh")})
q2["per_woman_state_all_identical"] = all(v["bitwise_identical"] for v in q2["per_woman_state"].values())
q2["aggregates_max_abs_diff"] = max(v["max_abs_diff"] for v in q2["device_aggregates"].values())
out["questions"].append(q2)
log("Q2 graph vs plain: per-woman state identical =", q2["per_woman_state_all_identical"],
    "max aggregate diff =", q2["aggregates_max_abs_diff"])

# ---- Q3 batch composition: same 12 runs split as one launch vs 12 single-run launches -----
st_full, acc_full = state_run(specs, nruns)          # one launch, local run index 0..11
q3 = dict(question="same 12 runs in one batch vs each run alone in its own launch "
                   "(RNG stream contains the within-launch run index)", per_run=[])
for i in range(nruns):
    st_i, acc_i = state_run([specs[i]], 1)
    st_full_i = {k: v[i:i + 1] for k, v in st_full.items()}
    rec = dict(run=i,
               state_identical={k: compare(st_full_i[k], st_i[k]) for k in st_i},
               births=compare(acc_full["births"][i:i + 1], acc_i["births"]))
    rec["state_all_identical"] = all(v["bitwise_identical"] for v in rec["state_identical"].values())
    if i >= 2:
        rec["state"] = "not repeated for every run (see run 0/1 for the pattern)"
    q3["per_run"].append(rec)
q3["summary"] = dict(
    run0_state_identical=q3["per_run"][0]["state_all_identical"],
    run1_state_identical=q3["per_run"][1]["state_all_identical"],
    runs_identical=[r["run"] for r in q3["per_run"] if r["state_all_identical"]],
    note="run 0 is at the same stream position (local index 0) in both layouts; every other "
         "run moves stream position and its draws change")
out["questions"].append(q3)
log("Q3 batch composition:", q3["summary"])

# ---- Q4 end-to-end simulate(batch=...) on the documented callable interface ---------------
variants = {}
for b in (1, 5, 7, 12):
    variants[b] = abm_dose.simulate(theta, countries, scen=0, nW=NW, seed=7, batch=b)
q4 = dict(question="documented callable simulate(batch=...) on 12 runs: how much do answers move?",
          comparisons=[])
for b in (5, 7, 12):
    rec = dict(batch=b)
    for g in ("tfr", "asfr1519", "smam", "m18", "afb", "coh"):
        rec[g] = compare(variants[1][g], variants[b][g])
    # per-run: does only run 0 agree?
    rec["tfr_run0_identical"] = compare(variants[1]["tfr"][0], variants[b]["tfr"][0])["bitwise_identical"]
    rec["tfr_rows_identical"] = [bool(np.array_equal(variants[1]["tfr"][i], variants[b]["tfr"][i],
                                                     equal_nan=True)) for i in range(12)]
    q4["comparisons"].append(rec)
out["questions"].append(q4)
log("Q4 simulate batch sensitivity:", [(c["batch"], c["tfr"]["max_abs_diff"]) for c in q4["comparisons"]])

out["gpu_after"] = gpu_stat()
dump("determinism_v2.json", out)
log("DONE determinism v2")
