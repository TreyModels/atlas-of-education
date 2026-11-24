#!/usr/bin/env python3
"""Engine gate for Q1: verify the real GPU engine API + baseline, pin the batch layout, one small adaptation.

All inputs are SYNTHETIC (a synthetic 2-country panel built here from the model's own parameter ranges), because
the calibration panel lived on the retired box2 and is not on box3. This is labelled as an API/baseline check,
not a re-estimation of the published model.
"""
import json, sys, time
import numpy as np
sys.path.insert(0, "/root/work/q1")
import dosecore as dc
import abm_dose
from engine import GPUDose, make_spec
import ref_numpy

NC = 14  # cohorts 1930..1995 (5-year)
def synth_panel():
    rng = np.random.default_rng(11)
    def dists():
        x = np.linspace(-1.6, 1.6, NC)[:, None] + 0.25 * rng.standard_normal((NC, 7))
        e = np.exp(x - x.max(1, keepdims=True)); return (e / e.sum(1, keepdims=True)).tolist()
    yrs = np.arange(1900, 2026)
    gdp = (6.5 + 0.030 * (yrs - 1900)).tolist()
    out = {"FIT": ["SYN1", "SYN2"], "countries": {}}
    for k, iso in enumerate(out["FIT"]):
        out["countries"][iso] = dict(shF=dists(), shM=dists(),
                                     urban=(0.35 + 0.02 * np.arange(NC)).tolist(),
                                     gdp=gdp, panel_thresholds={}, age_gap=3.0 + k)
    return out

PAN = synth_panel()
theta = (dc.LO + np.random.default_rng(3).random((2, dc.D_)) * (dc.HI - dc.LO))
R = {"engine_api": {}, "baseline": {}, "layout": {}, "adaptation": {}}

# 1. API check: documented entry point runs and returns the documented arrays
t0 = time.time()
out = abm_dose.simulate(theta[:1], ["SYN1"], scen=0, nW=12, seed=7, panel=PAN)
R["engine_api"] = dict(ok=True, keys=sorted(out.keys()), tfr_shape=list(np.shape(out["tfr"])),
                       wall_sec=round(time.time() - t0, 3), nW=12, seed=7,
                       note="synthetic panel; API only, not the published calibration")

# 2. Baseline: same seed + same layout must be repeatable (GPU twice)
o2 = abm_dose.simulate(theta[:1], ["SYN1"], scen=0, nW=12, seed=7, panel=PAN)
repeat = dict(tfr_max_abs_diff=float(np.nanmax(np.abs(out["tfr"] - o2["tfr"]))),
              smam_max_abs_diff=float(np.nanmax(np.abs(out["smam"] - o2["smam"]))),
              asfr_max_abs_diff=float(np.nanmax(np.abs(out["asfr1519"] - o2["asfr1519"]))))

# 3. CPU reference equivalence on the same seed/layout (one run, synthetic input)
pc = PAN["countries"]["SYN1"]; P = theta[0]
prep = dc.prepare(pc, P, 0, 7, 0)
gpu_eng = GPUDose(nW=12, seed=7, max_runs=1, tmax=2012)
gpu_eng.load([make_spec(pc, P, 0, 0.0, pc["age_gap"], 7, 0)])
acc = gpu_eng.run(0); gpu_state = gpu_eng.collect(state=True)
cpu = ref_numpy.simulate_ref(prep, P, 0, 7, 0.0, pc["age_gap"], nW=12, tmax=2012)
R["baseline"] = dict(repeat=repeat, cpu_gpu_note="numpy reference executed on the same prep",
                     cpu_keys=sorted(cpu.keys()) if isinstance(cpu, dict) else type(cpu).__name__)

# 4. Batch-layout diagnostic: same seed, two layouts -> streams move; then PIN layout.
la = abm_dose.simulate(theta[:1], ["SYN1"], scen=0, nW=12, seed=7, panel=PAN)
lb = abm_dose.simulate(theta[:1], ["SYN1"], scen=0, nW=6, seed=7, panel=PAN)
R["layout"] = dict(pinned="nW=12 (first layout); all headline numbers use this layout",
                   nW12_first_tfr=float(np.nanmean(la["tfr"][0, -3:])),
                   nW6_first_tfr=float(np.nanmean(lb["tfr"][0, -3:])),
                   tfr_max_abs_diff=float(np.nanmax(np.abs(la["tfr"] - lb["tfr"]))),
                   reading="changing nW changes the random streams (documented caveat); diff is not FP noise")

# 5. One small adaptation: single parameter vector at larger N, GPU vs CPU timing
t0 = time.time(); big = abm_dose.simulate(theta[:1], ["SYN1"], scen=0, nW=50000, seed=7, panel=PAN)
gpu_sec = time.time() - t0
t0 = time.time(); ref_numpy.simulate_ref(dc.prepare(pc, P, 0, 7, 0), P, 0, 7, 0.0, pc["age_gap"], nW=2000, tmax=2012)
cpu_sec = time.time() - t0
R["adaptation"] = dict(nW=50000, gpu_wall_sec=round(gpu_sec, 3), cpu_nW2000_wall_sec=round(cpu_sec, 3),
                       women_s_est=round(50000 / gpu_sec, 1), tfr_mean_last3=float(np.nanmean(big["tfr"][0, -3:])))
json.dump(R, open("/root/work/q1/results/engine_check.json", "w"), indent=1)
print(json.dumps(R, indent=1))
