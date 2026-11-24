#!/usr/bin/env python3
"""X1 (exposure-matched sequencing) and X3 (feedback-elasticity surface) drivers.

Uses the EXISTING eduengine (`engine/worlds.py` + `engine/eduengine/`) unmodified — this file
only defines arms (event schedules), runs the engine, and records every seed-level result.
Pre-registration: PRE_REGISTRATION_masseng_staging_x1_x3.md (committed BEFORE this code).

SIMULATION ONLY — stipulated toy worlds; no causal or empirical claim. Rural migration is not
simulated. Outputs are written with exclusive creation (never overwrite).
"""
import os

for _k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"

import argparse
import hashlib
import itertools
import json
import multiprocessing as mp
import platform
import socket
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "SIMULATION ONLY — stipulated eduengine toy worlds; not empirical; no causal claims"

# ---- engine location (never edited) ------------------------------------------------
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


# ---- metric definitions (identical to the audited staging experiment) --------------
SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper"]
ARRAYS = ["tut_by_grade", "tut_by_q", "completion_lower_q", "completion_upper_q", "completion_tertiary_q"]
SERIES = ["year", "formal_share_gdp", "edu_budget", "q_pub", "tut_rate"]

GATES_BAR = [dict(kind="bar", bar=x) for x in (3.0, 5.5, 8.0, 11.5)]
GATES_QUOTA = [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
               dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)]
GATES = {"bar": GATES_BAR, "quota": GATES_QUOTA}


def ev(year, label, st):
    return {"year": int(year), "set": dict(st), "label": label}


EDU = lambda y: ev(y, "education_share", {"edu_share": 0.30})
VAC = lambda y: ev(y, "formal_vacancies", {"vac0": 0.16})

# X1 arms: exposure totals in the pre-registration (70-year sums, base .18/.08, treated .30/.16)
X1_ARMS = {
    "none": [],
    "school_first": [EDU(15), VAC(30)],
    "jobs_first": [VAC(15), EDU(30)],
    "simultaneous": [EDU(15), VAC(15)],
    # matched spells are exactly 48 treated years for EACH intervention, so totals are equal:
    # revert events at year 48 end the early spell (education back to 0.18 / vacancies back to 0.08).
    "matched_school_first": [EDU(0), VAC(22), ev(48, "education_revert", {"edu_share": 0.18})],
    "matched_jobs_first": [VAC(0), EDU(22), ev(48, "vacancy_revert", {"vac0": 0.08})],
    "matched_simultaneous": [EDU(22), VAC(22)],
    "shifted_school_first": [EDU(25), VAC(40)],
    "shifted_jobs_first": [VAC(25), EDU(40)],
}
X1_PRIMARY = ["none", "school_first", "jobs_first", "simultaneous",
              "matched_school_first", "matched_jobs_first"]
X1_SUPPLEMENTARY = ["matched_simultaneous", "shifted_school_first", "shifted_jobs_first"]

X3_SCHEDULES = {"none": [], "school_first": [EDU(15), VAC(30)],
                "jobs_first": [VAC(15), EDU(30)], "simultaneous": [EDU(15), VAC(15)]}
X3_ELASTICITIES = [0.0, 0.25, 0.5, 0.75, 1.0]


def exposure(events, treated_param, base, treat):
    """Cumulative 70-year exposure implied by an arm's events (applies step changes in year order)."""
    tot = 0.0
    val = base
    for t in range(70):
        for e in events:
            if e["year"] == t and treated_param in e["set"]:
                val = e["set"][treated_param]
        tot += val
    return tot


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
    import worlds  # noqa: E402
    _G["worlds"] = worlds


def one(task):
    worlds = _G["worlds"]
    exp, arm, elasticity, feedback, gate, seed = task
    if exp == "x1":
        events = X1_ARMS[arm]
        fb = feedback
        jel = 1.0 if feedback == 1.0 else 0.0
    else:
        events = X3_SCHEDULES[arm]
        fb = None
        jel = elasticity
    engine = worlds.make("formal_loop", seed=int(seed), N=400, T=70, measure_from=35,
                         job_elasticity=jel, gates=GATES[gate], events=events)
    result = engine.run()
    row = {"experiment": exp, "arm": arm, "seed": int(seed)}
    if exp == "x1":
        row["feedback"] = float(feedback)
    else:
        row["elasticity"] = float(elasticity)
    row["gate"] = gate
    row["events"] = clean(engine.event_log)
    row["metrics"] = {k: clean(result.get(k)) for k in SCALARS + ARRAYS}
    row["annual"] = {k: clean(engine.R.get(k)) for k in SERIES}
    return row


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", required=True, choices=["x1", "x3"])
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--out", required=True)
    ap.add_argument("--engine-root", default=None)
    ap.add_argument("--seeds", type=int, default=20)
    a = ap.parse_args()
    out_path = os.path.abspath(a.out)
    if os.path.exists(out_path):
        raise FileExistsError(f"refusing to overwrite existing output: {out_path}")
    if a.workers < 1 or a.workers > 20:
        raise ValueError("declared bound: 1 <= workers <= 20 while the Bayesian screens are active")
    engine_root = resolve_engine_root(a.engine_root)
    started = time.time()
    seeds = tuple(range(a.seeds))
    if a.experiment == "x1":
        tasks = [(a.experiment, arm, None, fb, gate, s)
                 for arm in X1_ARMS for fb in (0.0, 1.0) for gate in ("bar", "quota") for s in seeds]
    else:
        tasks = [(a.experiment, arm, jel, None, gate, s)
                 for arm in X3_SCHEDULES for jel in X3_ELASTICITIES for gate in ("bar", "quota") for s in seeds]
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=1)
    elapsed = time.time() - started
    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for f in fs if f.endswith(".py")])
    code_hashes = {os.path.relpath(p, engine_root): sha256(p) for p in engine_files}
    code_hashes["run_x1_x3.py"] = sha256(os.path.abspath(__file__))
    config = {
        "experiment": a.experiment,
        "design": ("X1 exposure-matched sequencing" if a.experiment == "x1"
                   else "X3 feedback-elasticity surface"),
        "cohort_N": 400, "years": 70, "measure_from": 35, "seeds": list(seeds),
        "feedback": [0.0, 1.0] if a.experiment == "x1" else None,
        "elasticities": X3_ELASTICITIES if a.experiment == "x3" else None,
        "gates": ["bar", "quota"], "workers": a.workers, "runs": len(rows),
        "primary_arms": X1_PRIMARY if a.experiment == "x1" else list(X3_SCHEDULES),
        "supplementary_arms": X1_SUPPLEMENTARY if a.experiment == "x1" else [],
        "arms": {k: v for k, v in (X1_ARMS if a.experiment == "x1" else X3_SCHEDULES).items()},
        "exposure_arithmetic": {
            k: {"education_share_years": exposure(v, "edu_share", 0.18, 0.30),
                "vacancy_years": exposure(v, "vac0", 0.08, 0.16)}
            for k, v in (X1_ARMS if a.experiment == "x1" else X3_SCHEDULES).items()},
        "migration": "NOT SIMULATED (rural = household attribute + rural_cost + lower tutoring-firm access)",
        "label": LABEL,
    }
    data = {"label": LABEL, "config": config, "rows": rows, "elapsed_s": round(elapsed, 3),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "host": socket.gethostname(), "python": sys.version.split()[0],
            "numpy": np.__version__, "engine_root": engine_root,
            "code_sha256": code_hashes}
    with open(out_path, "x") as f:
        json.dump(data, f)
    print(json.dumps({"experiment": a.experiment, "runs": len(rows), "seeds": len(seeds),
                      "workers": a.workers, "elapsed_s": data["elapsed_s"], "out": out_path}))


if __name__ == "__main__":
    main()
