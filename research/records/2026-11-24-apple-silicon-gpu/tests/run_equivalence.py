#!/usr/bin/env python3
"""Equivalence tests: NumPy reference vs Apple (MLX) backend, fixed seed, same transcribed kernel.

1. Kernel-level: run kernel_probe.py on both backends; compare integer states (must be exact) and
   continuous outputs (max abs <=1e-5, max rel <=1e-4; float32 reduction-order noise).
2. End-to-end smoke: run exp1 --smoke through the shim on both backends; compare JSON rows.
3. exp3 small run (draws 20, batch 2000) if the World Bank API is reachable; compare candidate outputs.
Writes results/equivalence.json.
"""
import json, os, subprocess, sys
import numpy as np

RECORD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUITE = os.path.join(RECORD, "suite", "unified_gpu_suite")
RESULTS = os.path.join(RECORD, "results")
PY = os.environ.get("APPLE_PY", sys.executable)
ENV = dict(os.environ)
ENV["PYTHONPATH"] = os.pathsep.join([RECORD, os.path.join(RECORD, "shim"), os.path.join(SUITE, "scripts")])
ENV.setdefault("https_proxy", "http://127.0.0.1:7890")
ENV.setdefault("http_proxy", "http://127.0.0.1:7890")
os.makedirs(RESULTS, exist_ok=True)


def run(cmd, backend, log):
    e = dict(ENV); e["APPLE_GPU_BACKEND"] = backend
    p = subprocess.run(cmd, cwd=SUITE, env=e, capture_output=True, text=True)
    open(os.path.join(RESULTS, log), "w").write(p.stdout + "\n---STDERR---\n" + p.stderr)
    return p


out = {"tolerance": {"state_mismatches_max": 0, "cont_max_abs": 1e-5, "cont_max_rel": 1e-4}}

# 1. kernel-level
probes = {}
for b in ("numpy", "mlx"):
    f = os.path.join(RESULTS, f"kernel_probe_{b}.npz")
    p = run([PY, os.path.join(RECORD, "tests", "kernel_probe.py"), "--backend", b, "--out", f], b,
            f"kernel_probe_{b}.log")
    probes[b] = np.load(f) if os.path.exists(f) else None
    out[f"probe_{b}_ok"] = probes[b] is not None
if probes["numpy"] is not None and probes["mlx"] is not None:
    res = {}
    for k in ("state", "tutor", "learn", "work", "y_hh"):
        a, b = probes["numpy"][k], probes["mlx"][k]
        diff = np.abs(a.astype(np.float64) - b.astype(np.float64))
        rel = diff / np.maximum(np.abs(a.astype(np.float64)), 1e-12)
        res[k] = dict(dtype=str(a.dtype), max_abs=float(diff.max()), max_rel=float(rel.max()),
                      n_diff=int(np.sum(diff > 0)))
    res["state_mismatches"] = int(np.sum(probes["numpy"]["state"] != probes["mlx"]["state"]))
    res["tutor_mismatches"] = int(np.sum(probes["numpy"]["tutor"] != probes["mlx"]["tutor"]))
    res["equivalent"] = bool(res["state_mismatches"] == 0 and res["tutor_mismatches"] == 0
                             and res["learn"]["max_abs"] <= 1e-5 and res["work"]["max_abs"] <= 1e-5
                             and res["y_hh"]["max_abs"] <= 1e-5)
    out["kernel_level"] = res

# 2. exp1 smoke end-to-end
ej = {}
for b in ("numpy", "mlx"):
    f = os.path.join(RESULTS, f"smoke_exp1_{b}.json")
    p = run([PY, "scripts/exp1_unified_gpu_abm.py", "--smoke", "--out", f], b, f"smoke_exp1_{b}.log")
    ej[b] = json.load(open(f)) if os.path.exists(f) else None
if ej.get("numpy") is not None and ej.get("mlx") is not None:
    rows_a, rows_b = ej["numpy"], ej["mlx"]
    assert len(rows_a) == len(rows_b)
    int_keys = ("ger", "study_work", "work_only", "hidden_work", "cl_total", "tutoring")
    cont_keys = ("enrolled_work_hrs_p90", "tutor_income_corr", "mean_learn", "q_pub")
    e2e = {"n_rows": len(rows_a), "int_metrics_exact": {}, "cont_metrics": {}}
    for k in int_keys:
        e2e["int_metrics_exact"][k] = bool(all(a[k] == b[k] for a, b in zip(rows_a, rows_b)))
    for k in cont_keys:
        d = [abs(a[k] - b[k]) for a, b in zip(rows_a, rows_b)]
        e2e["cont_metrics"][k] = dict(max_abs=float(max(d)), median_abs=float(np.median(d)))
    e2e["equivalent"] = bool(all(e2e["int_metrics_exact"].values())
                             and all(v["max_abs"] <= 1e-5 for v in e2e["cont_metrics"].values()))
    out["exp1_smoke"] = e2e

# 3. exp3 small run (may need network)
e3 = {}
for b in ("numpy", "mlx"):
    f = os.path.join(RESULTS, f"smoke_exp3_{b}.json")
    p = run([PY, "scripts/exp3_rejection_abc_realdata.py", "--draws", "20", "--batch-n", "2000",
             "--out", f], b, f"smoke_exp3_{b}.log")
    e3[b] = (json.load(open(f)) if os.path.exists(f) else None, p.returncode)
if e3.get("numpy", (None,))[0] is not None and e3.get("mlx", (None,))[0] is not None:
    a, b = e3["numpy"][0], e3["mlx"][0]
    d = {}
    for k in a["identifiability"]:
        d[k] = dict(width_ratio_abs_diff=abs(a["identifiability"][k]["width_ratio"] -
                                             b["identifiability"][k]["width_ratio"]),
                    identified_same=bool(a["identifiability"][k]["identified"] ==
                                         b["identifiability"][k]["identified"]))
    out["exp3_smoke"] = dict(equivalent=bool(all(v["width_ratio_abs_diff"] <= 1e-6
                                                and v["identified_same"] for v in d.values())),
                             detail=d)
else:
    out["exp3_smoke"] = dict(equivalent=False,
                             note="exp3 smoke not comparable (network/World Bank API or run failure); "
                                  "see smoke_exp3_*.log")
json.dump(out, open(os.path.join(RESULTS, "equivalence.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
