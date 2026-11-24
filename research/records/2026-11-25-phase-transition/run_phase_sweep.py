#!/usr/bin/env python3
"""Full phase sweep — SIMULATION ONLY (eduengine toy worlds; no empirical/causal claims).

X  formal vacancies per cohort entrant (`vac0`), 10 levels severe->slack.
Y  primary-school fee per year as share of median income (`fee_primary`, grades 1-6 only), 10 levels
   post-E8 (0.0) -> pre-E8 (0.18).
G  exam-gate rule: bar (fixed pass threshold, tournament) vs quota (planned seats as a declared share
   of the cohort; endogenous admission cutoff). 10 x 10 x 2 = 200 cells x 5 seeds = 1,000 runs.

PRE-REGISTERED design and analysis: PREREGISTRATION_PHASE_SWEEP.md (committed BEFORE this code and
before any run). Exits are read ONLY from `e.exits` (core.step compacts exited children out of the
state, so e.kids['reason'] is all -1 by design); `aggregate_exits` rebuilds the population and keeps
censored-at-horizon as its own category.

Writes only under --out. No power/reboot commands. Deterministic seeds.
"""
import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import os
import socket
import sys
import time

sys.dont_write_bytecode = True

import numpy as np

LABEL = "SIMULATION ONLY - eduengine toy worlds; illustrative parameters; no causal/empirical claims"

X_LEVELS = [0.02, 0.03, 0.045, 0.065, 0.09, 0.13, 0.18, 0.25, 0.35, 0.50]
Y_LEVELS = [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]
GATE_LEVELS = ["bar", "quota"]
GATES = {
    "bar": [dict(kind="bar", bar=b) for b in (3.0, 5.5, 8.0, 11.5)],
    "quota": [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
              dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)],
}
EXIT_FIELDS = ("reason", "started", "urban", "y", "cohort", "cred", "inc")
SHARE_CATS = (("liq", "liquidity", 1), ("gate_fail", "gate_fail", 2), ("finished", "finished", 3),
              ("never", "never_enrolled", 4), ("no_seat", "no_seat", 5), ("not_admitted", "not_admitted", 6),
              ("choice", "choice", 0), ("censored", "censored", -1))
SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper",
           "formal_rate", "youth_unemp", "grad_unemp", "skill_premium", "floor_skilled", "floor_routine"]
ARRAYS = ["tut_by_q", "completion_primary_q", "completion_lower_q", "completion_upper_q", "completion_tertiary_q"]

_G = {}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def clean(v):
    if isinstance(v, (list, tuple, np.ndarray)):
        return [clean(x) for x in v]
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return float(v) if np.isfinite(v) else None
    return v


def init_engine(engine_root):
    sys.dont_write_bytecode = True
    sys.path.insert(0, engine_root)
    import worlds
    import eduengine as ee
    from eduengine.modules.schools import PublicSchools
    from eduengine.modules.sdg4 import SDG4
    _G.update(worlds=worlds, ee=ee, SDG4=SDG4, PublicSchools=PublicSchools)


def make_engine(engine_root, vac0, fee_primary, gate, seed, n, t, measure_from):
    worlds, ee = _G["worlds"], _G["ee"]
    SDG4, PublicSchools = _G["SDG4"], _G["PublicSchools"]

    class PrimaryFeeSchools(PublicSchools):
        """PublicSchools + a household fee charged only on grades 1-6 (the fee E8 removes)."""
        name = "public_schools"
        defaults = dict(PublicSchools.defaults, fee_primary=0.0)

        def supply(self, E, t):
            super().supply(E, t)
            p, k, y = E.p, E.kids, E.yr
            add = (k["g"] < 6) & (k["sector"] == 0)
            y["cost"] += np.where(add, p["fee_primary"], 0.0)

    params = dict(worlds.WORLDS["formal_loop"]["params"])
    params.update(dict(N=n, T=t, measure_from=measure_from, seed=seed, vac0=vac0, vac_growth=0.0,
                       fee_primary=fee_primary, gates=GATES[gate], queue_on=True))
    mods = [PrimaryFeeSchools(), ee.PrivateSchools(), ee.TutoringMarket(), ee.FiscalState(),
            ee.QueueLabour(), SDG4()]
    mods = sorted(mods, key=lambda m: ee.ORDER.index(m.name) if m.name in ee.ORDER else 50)
    return ee.Engine(mods, **params)


def aggregate_exits(e):
    blocks = list(getattr(e, "exits", None) or [])
    n_surv = len(e.kids["reason"]) if e.kids is not None else 0
    out = {}
    for f in EXIT_FIELDS:
        parts = [np.asarray(b[f]) for b in blocks if f in b]
        parts.append(np.asarray(e.kids[f]) if f in e.kids else np.full(n_surv, np.nan))
        out[f] = np.concatenate(parts)
    return out


def one(task):
    xi, yi, gi, seed = task
    e = make_engine(one.engine_root, X_LEVELS[xi], Y_LEVELS[yi], GATE_LEVELS[gi], seed,
                    one.n, one.t, one.measure_from)
    out = e.run()
    pop = aggregate_exits(e)
    mask = np.asarray(pop["cohort"]) >= one.measure_from
    reason = np.asarray(pop["reason"], int)[mask]
    y = np.asarray(pop["y"], float)[mask]
    inc = np.asarray(pop["inc"], float)[mask]
    cred = np.asarray(pop["cred"], int)[mask]
    n = int(mask.sum())
    cuts = np.quantile(y, [0.2, 0.4, 0.6, 0.8])
    q = np.searchsorted(cuts, y, side="right")
    n_meas_cohorts = max(len(np.unique(np.asarray(pop["cohort"])[mask])), 1)

    rec = {"x_index": xi, "x_vac0": X_LEVELS[xi], "y_index": yi, "fee_primary": Y_LEVELS[yi],
           "gate": GATE_LEVELS[gi], "gate_index": gi, "seed": seed,
           "metrics": {m: clean(out.get(m)) for m in SCALARS},
           "arrays": {m: clean(out.get(m)) for m in ARRAYS}, "groups": {}}

    def share(sel, code):
        return float(np.mean(reason[sel] == code)) if np.any(sel) else None

    for key, _nm, code in SHARE_CATS:
        rec["groups"][f"{key}_share"] = share(np.ones(n, bool), code)
    for qi in range(5):
        sel = q == qi
        rec["groups"][f"q{qi + 1}"] = {
            f"{k2}_share": share(sel, code) for k2, _nm, code in SHARE_CATS}
        rec["groups"][f"q{qi + 1}"]["n"] = int(sel.sum())
    # gate-pass (secondary transition) by quintile: cred>=2 = lower-secondary gate cleared
    rec["groups"]["gate_pass_q"] = [float(np.mean(cred[q == qi] >= 2)) if np.any(q == qi) else None
                                    for qi in range(5)]
    rec["groups"]["gate2_pass_q"] = [float(np.mean(cred[q == qi] >= 3)) if np.any(q == qi) else None
                                     for qi in range(5)]
    # formal hire by quintile, derived from leaver income (formal routine >= ~1.5 vs informal <= ~1.16
    # in the queue module's wage equations; 1.3 is the declared separating threshold)
    finite = np.isfinite(inc)
    rec["groups"]["formal_hire_q"] = [float(np.mean(inc[(q == qi) & finite] >= 1.3))
                                      if np.any((q == qi) & finite) else None for qi in range(5)]
    # derived inequality read-outs (declared in the pre-registration)
    tg = out.get("tut_by_q") or []
    rec["groups"]["tut_q5_q1_gap"] = float(tg[4] - tg[0]) if len(tg) == 5 else None
    for lvl in ("primary", "lower", "upper", "tertiary"):
        arr = out.get(f"completion_{lvl}_q") or []
        rec["groups"][f"completion_{lvl}_q_gap"] = float(arr[4] - arr[0]) if len(arr) == 5 else None
    gp = rec["groups"]["gate_pass_q"]
    rec["groups"]["gate_pass_q_gap"] = float(gp[4] - gp[0]) if all(v is not None for v in gp) else None
    fh = rec["groups"]["formal_hire_q"]
    rec["groups"]["formal_hire_q_gap"] = float(fh[4] - fh[0]) if all(v is not None for v in fh) else None

    # realised X normalisations
    vac_year = one.n * X_LEVELS[xi]
    rec["groups"]["x_vac_per_entrant"] = X_LEVELS[xi]
    rec["groups"]["x_vac_per_lower_complete"] = float(vac_year / max(int(np.sum(cred >= 1)) / n_meas_cohorts, 1e-9))
    rec["groups"]["x_vac_per_gate_pass"] = float(vac_year / max(int(np.sum(cred >= 2)) / n_meas_cohorts, 1e-9))
    rec["groups"]["n_pop_measured"] = n
    rec["groups"]["n_cohorts_measured"] = n_meas_cohorts
    return rec


def cell_summary(rows):
    """Per-cell seed means + seed SD of every scalar read-out (groups and metrics)."""
    s = {"n_seeds": len(rows)}
    for grp in ("metrics", "groups"):
        keys = rows[0][grp].keys()
        for k in keys:
            vals = [r[grp][k] for r in rows if not isinstance(r[grp][k], (list, dict))]
            vals = [v for v in vals if v is not None]
            s[k] = float(np.mean(vals)) if vals else None
            if len(vals) > 1:
                s[f"sd_{k}"] = float(np.std(vals, ddof=1))
        for k in keys:  # list-valued (quintile arrays) -> mean vector
            vv = [r[grp][k] for r in rows if isinstance(r[grp][k], list)]
            if vv:
                s[k] = [float(np.mean([v[j] for v in vv])) for j in range(len(vv[0]))]
    q1 = [r["groups"]["q1"] for r in rows]
    for k in q1[0]:
        vals = [x[k] for x in q1 if x[k] is not None]
        s[f"q1_{k}"] = float(np.mean(vals)) if vals else None
    return s


def main():
    ap = argparse.ArgumentParser(description="Full phase sweep (SIMULATION ONLY)")
    ap.add_argument("--engine-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--x-levels", default=None)
    ap.add_argument("--y-levels", default=None)
    ap.add_argument("--gates", default="bar,quota")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--t", type=int, default=70)
    ap.add_argument("--measure-from", type=int, default=35)
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()

    global X_LEVELS, Y_LEVELS, GATE_LEVELS
    if a.x_levels:
        X_LEVELS = [float(x) for x in a.x_levels.split(",")]
    if a.y_levels:
        Y_LEVELS = [float(x) for x in a.y_levels.split(",")]
    GATE_LEVELS = [g.strip() for g in a.gates.split(",") if g.strip()]
    assert set(GATE_LEVELS) <= {"bar", "quota"}
    if not (1 <= a.workers <= 32):
        raise SystemExit("workers bound 1..32")
    engine_root = os.path.abspath(a.engine_root)
    if not os.path.isfile(os.path.join(engine_root, "worlds.py")):
        raise SystemExit(f"--engine-root must contain worlds.py: {engine_root}")
    out_dir = os.path.abspath(a.out)
    os.makedirs(out_dir, exist_ok=True)
    paths = {k: os.path.join(out_dir, f"phase_sweep_{k}") for k in
             ("raw.json", "summary.json", "summary.csv", "run_meta.json")}
    if not a.overwrite and any(os.path.exists(p) for p in paths.values()):
        raise SystemExit(f"outputs already exist in {out_dir} (use --overwrite)")

    tasks = [(xi, yi, gi, s) for xi in range(len(X_LEVELS)) for yi in range(len(Y_LEVELS))
             for gi in range(len(GATE_LEVELS)) for s in range(a.seeds)]
    t0 = time.time()
    one.engine_root = engine_root
    one.n, one.t, one.measure_from = a.n, a.t, a.measure_from
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=4)
    elapsed = time.time() - t0

    cells = []
    for xi in range(len(X_LEVELS)):
        for yi in range(len(Y_LEVELS)):
            for gi, gate in enumerate(GATE_LEVELS):
                cr = [r for r in rows if r["x_index"] == xi and r["y_index"] == yi and r["gate_index"] == gi]
                s = cell_summary(cr)
                s.update({"x_index": xi, "x_vac0": X_LEVELS[xi], "y_index": yi,
                          "fee_primary": Y_LEVELS[yi], "gate": gate, "gate_index": gi})
                cells.append(s)

    # partition honesty check
    for r in cells:
        tot = sum((r.get(f"{k}_share") or 0.0) for k, _n, _c in SHARE_CATS)
        if abs(tot - 1.0) > 1e-6:
            raise RuntimeError(f"exit partition != 1 at x={r['x_vac0']} y={r['fee_primary']} gate={r['gate']}: {tot}")

    cols = ["gate", "x_index", "x_vac0", "x_vac_per_gate_pass", "y_index", "fee_primary", "n_seeds",
            "liq_share", "gate_fail_share", "censored_share", "choice_share", "never_share",
            "no_seat_share", "not_admitted_share", "finished_share",
            "q1_liq_share", "q1_gate_fail_share", "q1_choice_share", "q1_censored_share",
            "tut_rate", "tut_q5_q1_gap", "completion_lower", "completion_upper",
            "completion_lower_q_gap", "completion_upper_q_gap", "parity_wealth_lower",
            "formal_rate", "queue", "grad_unemp",
            "sd_liq_share", "sd_gate_fail_share", "sd_tut_rate", "sd_tut_q5_q1_gap",
            "sd_completion_lower", "sd_completion_lower_q_gap"]
    with open(paths["summary.csv"], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in cells:
            w.writerow(r)

    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, fn) for dp, _dd, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for fn in fs if fn.endswith(".py")])
    meta = {"label": LABEL, "experiment": "phase_sweep_full",
            "design": {"X_vac0_formal_vacancies_per_entrant": X_LEVELS,
                       "Y_fee_primary_share_of_median_income": Y_LEVELS,
                       "gate": GATE_LEVELS, "n_cells": len(cells), "seeds": a.seeds,
                       "runs": len(rows), "N": a.n, "T": a.t, "measure_from": a.measure_from,
                       "base_world": "formal_loop", "workers": a.workers,
                       "notes": ["primary fee grades 1-6 only; 0.0 = E8 abolition slice",
                                 "X grid = vac0; realised vacancies per gate-passing child reported",
                                 "queue_on=True", "exits from e.exits only; censored its own category"],
                       "missing_mechanisms": ["migration/emigration", "rural-urban sorting/residential choice",
                                              "remittances/kin transfers", "country-specific calibration",
                                              "informal/formal composition beyond queue vs competitive"]},
            "elapsed_s": round(elapsed, 3), "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
            "engine_root": engine_root,
            "code_sha256": {**{os.path.relpath(p, engine_root): sha256(p) for p in engine_files},
                            "run_phase_sweep.py": sha256(os.path.abspath(__file__))}}
    with open(paths["raw.json"], "w") as f:
        json.dump({"label": LABEL, "meta": meta, "rows": rows}, f)
    with open(paths["summary.json"], "w") as f:
        json.dump({"label": LABEL, "meta": meta, "cells": cells}, f)
    print(json.dumps({"runs": len(rows), "cells": len(cells), "elapsed_s": meta["elapsed_s"],
                      "workers": a.workers, "out": out_dir}))


if __name__ == "__main__":
    main()
