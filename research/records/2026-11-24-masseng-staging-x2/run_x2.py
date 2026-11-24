#!/usr/bin/env python3
"""X2 driver — gate/quota × tutoring inequality factorial on the EXISTING eduengine.

Pre-registration: PRE_REGISTRATION_masseng_staging_x2_x4.md (committed before this code).
SIMULATION ONLY — toy worlds; no causal/empirical claim; rural migration not simulated.
Outputs use exclusive creation (never overwrite).
"""
import os

for _k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"

import argparse
import hashlib
import json
import multiprocessing as mp
import socket
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "SIMULATION ONLY — stipulated eduengine toy worlds; not empirical; no causal claims"


def resolve_engine_root(explicit):
    cands = []
    if explicit:
        cands.append(os.path.abspath(explicit))
    if os.environ.get("MASSENG_ENGINE_ROOT"):
        cands.append(os.path.abspath(os.environ["MASSENG_ENGINE_ROOT"]))
    cands.append(os.path.join(HERE, "engine"))
    cands.append(os.path.abspath(os.path.join(HERE, "..", "..", "..", "engine")))
    for c in cands:
        if os.path.exists(os.path.join(c, "worlds.py")):
            return c
    raise FileNotFoundError(f"engine/worlds.py not found in candidates: {cands}")


SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper"]
ARRAYS = ["tut_by_grade", "tut_by_q", "completion_lower_q", "completion_upper_q", "completion_tertiary_q",
          "tut_own_by_grade", "tut_firm_by_grade"]
EXTRA_SCALARS = ["own_share", "firm_price"]

GATES_BAR = [dict(kind="bar", bar=x) for x in (3.0, 5.5, 8.0, 11.5)]
GATES_QUOTA = [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
               dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)]
GATES = {"bar": GATES_BAR, "quota": GATES_QUOTA}
ACCESS = (0.2, 0.4, 0.8)
BANS = (0.0, 1.0)


def clean(v):
    if isinstance(v, dict):
        return {str(k): clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, np.ndarray)):
        return [clean(x) for x in v]
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return float(v) if np.isfinite(v) else None
    if isinstance(v, (str, bool)) or v is None:
        return v
    return str(v)


_G = {}


def init_engine(engine_root):
    sys.path.insert(0, engine_root)
    import worlds
    _G["worlds"] = worlds


def one(task):
    worlds = _G["worlds"]
    gate, access, ban, seed = task
    engine = worlds.make("formal_loop", seed=int(seed), N=400, T=70, measure_from=35,
                         job_elasticity=0.0, gates=GATES[gate], events=[],
                         rural_firm_access=float(access), own_ban=float(ban))
    result = engine.run()
    row = {"gate": gate, "rural_firm_access": float(access), "own_ban": float(ban), "seed": int(seed),
           "metrics": {k: clean(result.get(k)) for k in SCALARS + EXTRA_SCALARS + ARRAYS},
           "annual": {k: clean(engine.R.get(k)) for k in ("year", "formal_share_gdp", "edu_budget", "q_pub", "tut_rate")}}
    return row


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--out", required=True)
    ap.add_argument("--engine-root", default=None)
    ap.add_argument("--seeds", type=int, default=20)
    a = ap.parse_args()
    out_path = os.path.abspath(a.out)
    if os.path.exists(out_path):
        raise FileExistsError(out_path)
    if not (1 <= a.workers <= 20):
        raise ValueError("declared bound 1..20 workers")
    engine_root = resolve_engine_root(a.engine_root)
    seeds = tuple(range(a.seeds))
    tasks = [(gate, access, ban, s) for gate in ("bar", "quota") for access in ACCESS
             for ban in BANS for s in seeds]
    t0 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=1)
    elapsed = time.time() - t0
    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for f in fs if f.endswith(".py")])
    data = {"label": LABEL, "experiment": "x2",
            "config": {"design": "gate/quota x tutoring access x own-teacher ban factorial",
                       "GATES": {"bar": "bar 3.0,5.5,8.0,11.5", "quota": "bar3.0,quota .55 cut0 7.0,quota .45 cut0 10.0,bar11.5"},
                       "rural_firm_access": list(ACCESS), "own_ban": list(BANS), "seeds": list(seeds),
                       "cohort_N": 400, "years": 70, "measure_from": 35, "job_elasticity": 0.0,
                       "events": [], "workers": a.workers, "runs": len(rows),
                       "gate_adjacent_grades_1based": [6, 9, 12], "non_gate_grades_1based": [4, 7, 10, 13],
                       "migration": "NOT SIMULATED (rural = attribute + rural_cost + lower tutoring-firm access)"},
            "rows": rows, "elapsed_s": round(elapsed, 3),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
            "engine_root": engine_root,
            "code_sha256": {**{os.path.relpath(p, engine_root): sha256(p) for p in engine_files},
                            "run_x2.py": sha256(os.path.abspath(__file__))}}
    with open(out_path, "x") as f:
        json.dump(data, f)
    print(json.dumps({"experiment": "x2", "runs": len(rows), "workers": a.workers,
                      "elapsed_s": data["elapsed_s"], "out": out_path}))


if __name__ == "__main__":
    main()
