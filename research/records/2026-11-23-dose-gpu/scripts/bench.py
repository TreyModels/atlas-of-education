"""Throughput sweep for the GPU engine: how many simulated life-course runs per second, by batch size."""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dosecore as dc
from engine import GPUDose, targets_array, make_spec

PAN = json.load(open(next(c for c in ["../data/panel.json", "data/panel.json"] if os.path.exists(c))))
import model as M
P = M.LO + np.random.default_rng(3).random(len(M.PN)) * (M.HI - M.LO)
FIT = PAN["FIT"]
N = 384
specs = []
for i in range(N):
    pc = PAN["countries"][FIT[i % len(FIT)]]
    specs.append(make_spec(pc, P, 0, 0.0, pc["age_gap"], 7, i))
res = []
for R in (24, 48, 96, 192, 384):
    eng = GPUDose(nW=12, seed=5, max_runs=R, tmax=2012)
    eng.load(specs[:R]); eng.run(0)
    t = time.time(); reps = max(2, int(200 / R))
    for _ in range(reps): eng.run(0)
    dt = (time.time() - t) / reps
    t = time.time()
    for _ in range(reps): eng.load(specs[:R]); eng.run(0)
    dt2 = (time.time() - t) / reps
    out = eng.run(0); S = targets_array(out)
    t = time.time(); eng.load(specs[:R]); eng.run(0); S = targets_array(eng.collect()); dl_load = time.time() - t
    res.append(dict(R=R, run_sec=round(dt, 5), load_run_sec=round(dt2, 5), runs_per_sec=round(R / dt, 1),
                    sec_per_draw_24runs=round(dt / R * 24, 5), nWtot=R * 1680))
    print(res[-1], flush=True)
# also time scaling with tmax at the best R
eng = GPUDose(nW=12, seed=5, max_runs=192, tmax=2012)
eng.load(specs[:192])
for tm in (1960, 1985, 2012, 2050):
    eng.tmax = tm
    eng.run(0, tm)
    t = time.time(); eng.run(0, tm); dt = time.time() - t
    res.append(dict(tmax=tm, R=192, run_sec=round(dt, 5), runs_per_sec=round(192 / dt, 1)))
    print(res[-1], flush=True)
# CPU baseline, single process, uncontended-ish (3 repeats, take the min)
pc = PAN["countries"][FIT[0]]
M.simulate(pc, P, 0, 1, 0.0, nW=12)
ts = []
for i in range(6):
    t = time.time(); M.simulate(PAN["countries"][FIT[i % len(FIT)]], P, 0, 1 + i, 0.0, nW=12); ts.append(time.time() - t)
cpu = min(ts)
print(json.dumps(dict(cpu_sec_per_run_min=cpu, cpu_all=ts)), flush=True)
out = dict(sweep=res, cpu_sec_per_run_min=cpu)
json.dump(out, open(os.path.join(os.environ.get("RESULTS", "../results"), "bench.json"), "w"), indent=1)
print("wrote bench.json")
