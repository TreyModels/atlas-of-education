"""Benchmark the GPU dose engine at scale: how many simulated women / parameter draws per second, and
how large a population one launch can carry.  Fills the "kernel as a deliverable" brief."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cupy as cp
from engine import GPUDose, targets_array, make_spec
import dosecore as dc

PAN = json.load(open(os.environ.get("DOSE_PANEL", "data/panel.json"))); FIT = PAN["FIT"]
rng = np.random.default_rng(3)
res = []
for runs in (192, 384, 768, 1536, 3000, 6000):
    draws = max(1, runs // 24)
    specs = []
    for i in range(runs):
        iso = FIT[i % len(FIT)]; pc = PAN["countries"][iso]
        th = dc.LO + rng.random(dc.D_) * (dc.HI - dc.LO)
        specs.append(make_spec(pc, th, 0, 0.0, pc["age_gap"], 7, i))
    try:
        eng = GPUDose(nW=12, seed=5, max_runs=runs, tmax=2012)
        t = time.time(); eng.load(specs); tload = time.time() - t
        eng.run(0)
        t = time.time(); reps = 3 if runs <= 1536 else 2
        for _ in range(reps): eng.run(0)
        cp.cuda.Stream.null.synchronize(); trun = (time.time() - t) / reps
        women = runs * 1680
        res.append(dict(runs=runs, param_draws=draws, women=women, load_sec=round(tload, 3),
                        run_sec=round(trun, 4), women_per_sec=int(women / trun),
                        draws_per_sec=round(draws / trun, 1),
                        mem_MB=int(sum(a.nbytes for a in [eng.births, eng.expo, eng.sing, eng.coh, eng.w_born,
                                                          eng.w_par, eng.w_afm, eng.w_ed, eng.w_wt, eng.w_ind0,
                                                          eng.m_born, eng.m_av, eng.m_key, eng.PWc, eng.PMc, eng.gdp]) / 1e6)))
        print(res[-1], flush=True)
        del eng
        cp.get_default_memory_pool().free_all_blocks()
    except Exception as e:
        res.append(dict(runs=runs, error=str(e)[:120])); print(res[-1], flush=True)
json.dump(dict(results=res, nW=12, women_per_run=1680), open(os.path.join(os.environ.get("RESULTS", "../results"), "bench_scale.json"), "w"), indent=1)
print("wrote bench_scale.json")
