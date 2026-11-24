#!/usr/bin/env python3
"""phase_sweep_quick.py — SIMULATION ONLY (eduengine toy worlds; no empirical/causal claims).

Quick phase sweep: E8-style primary-fee abolition (Y) x formal-vacancy bottleneck (X), fixed exam-gate
rule, 10 x 10 grid x 5 seeds = 500 runs, summary CSV + JSON. Runs on the warm AutoDL box with
/root/miniconda3/bin/python (numpy 1.24+), or locally.

Axes
  X  formal vacancies per cohort entrant  (`vac0`, the engine's formal-demand parameter).
     The headline dimensionless normalisation `x_vac_per_gate_pass` = annual formal vacancies /
     children passing the lower-secondary exam gate (cred>=2) is measured and written per cell.
  Y  primary-school fee per year as a share of median income (`fee_primary`, grades 1-6 only);
     `fee_primary = 0.0` is the E8 abolition slice, positive values are pre-abolition regimes.

Exits are read ONLY from `e.exits` via aggregate_exits(): core.step compacts exited children out of
the state, so `e.kids['reason']` is all -1 after run() BY DESIGN. Survivors still in the state are the
`censored` category; the exit shares partition the measured population to 1.0.

Usage (box):
  /root/miniconda3/bin/python phase_sweep_quick.py \
      --engine-root /root/work/edsystem/engine --out /root/work/phase_sweep_quick --workers 12

Writes only inside --out. No power/reboot commands. Deterministic seeds (0..seeds-1 per cell).
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

sys.dont_write_bytecode = True  # never write __pycache__ outside --out

import numpy as np

LABEL = "SIMULATION ONLY - eduengine toy worlds; illustrative parameters; no causal/empirical claims"

X_LEVELS = [0.02, 0.03, 0.045, 0.065, 0.09, 0.13, 0.18, 0.25, 0.35, 0.50]   # vac0: severe -> slack
Y_LEVELS = [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18]    # primary fee: post-E8 -> pre-E8

GATES = {
    # pre-registered gate rules
    "bar": [dict(kind="bar", bar=b) for b in (3.0, 5.5, 8.0, 11.5)],
    "quota": [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
              dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)],
    # EXPLORATORY (post-hoc diagnostic, declared as a deviation): the pre-registered "bar" arm turns out
    # non-binding (gate_fail ~0.7%), so this arm makes the two high-stakes gates actually bind (~50%).
    # calibrated on one probe run so the two high-stakes gates actually ration (gate_fail ~9%), instead of
    # the pre-registered bars which almost nobody fails (gate_fail <=1.3%).
    "bar_binding": [dict(kind="bar", bar=3.0), dict(kind="bar", bar=13.5),
                    dict(kind="bar", bar=17.5), dict(kind="bar", bar=11.5)],
}

EXIT_FIELDS = ("reason", "started", "urban", "y", "cohort", "cred", "inc")
SHARE_CATS = (("liq", "liquidity", 1), ("gate_fail", "gate_fail", 2), ("finished", "finished", 3),
              ("never", "never_enrolled", 4), ("no_seat", "no_seat", 5), ("not_admitted", "not_admitted", 6),
              ("choice", "choice", 0), ("censored", "censored", -1))

_G = {}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def init_engine(engine_root):
    sys.dont_write_bytecode = True
    sys.path.insert(0, engine_root)
    import worlds
    import eduengine as ee
    from eduengine.modules.schools import PublicSchools
    from eduengine.modules.sdg4 import SDG4
    _G["worlds"] = worlds
    _G["ee"] = ee
    _G["SDG4"] = SDG4
    _G["PublicSchools"] = PublicSchools


def make_engine(engine_root, vac0, fee_primary, gate, seed, n, t, measure_from):
    """Build the formal_loop world with a primary-only E8 fee shock and a chosen gate rule."""
    worlds = _G["worlds"]
    ee = _G["ee"]
    PublicSchools = _G["PublicSchools"]
    SDG4 = _G["SDG4"]

    class PrimaryFeeSchools(PublicSchools):
        """PublicSchools + a household fee charged only on grades 1-6 (the E8 fee the reform removes)."""
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
    """Rebuild the full child population from e.exits + survivors (censored, reason -1)."""
    blocks = list(getattr(e, "exits", None) or [])
    n_surv = len(e.kids["reason"]) if e.kids is not None else 0
    out = {}
    for f in EXIT_FIELDS:
        parts = [np.asarray(b[f]) for b in blocks if f in b]
        if f in e.kids:
            parts.append(np.asarray(e.kids[f]))
        else:
            parts.append(np.full(n_surv, np.nan))
        out[f] = np.concatenate(parts) if parts else np.array([])
    return out


def one(task):
    """One run -> per-run read-out (measured window = cohorts >= measure_from)."""
    xi, yi, seed = task
    vac0, fee = X_LEVELS[xi], Y_LEVELS[yi]
    gate = one.gate
    e = make_engine(one.engine_root, vac0, fee, gate, seed, one.n, one.t, one.measure_from)
    out = e.run()

    pop = aggregate_exits(e)
    mask = np.asarray(pop["cohort"]) >= one.measure_from
    reason = np.asarray(pop["reason"], int)[mask]
    y = np.asarray(pop["y"], float)[mask]
    inc = np.asarray(pop["inc"], float)[mask]
    cred = np.asarray(pop["cred"], int)[mask]
    n = int(mask.sum())
    cuts = np.quantile(y, [0.2, 0.4, 0.6, 0.8]) if n else np.zeros(4)
    q = np.searchsorted(cuts, y, side="right")
    n_meas_cohorts = max(len(np.unique(np.asarray(pop["cohort"])[mask])), 1)

    rec = {"x_index": xi, "x_vac0": vac0, "y_index": yi, "fee_primary": fee, "gate": gate, "seed": seed}

    def cat_share(sel, code):
        return float(np.mean(reason[sel] == code)) if np.any(sel) else None

    for key, _name, code in SHARE_CATS:
        rec[f"{key}_share"] = cat_share(np.ones(n, bool), code)
    for qq in (0, 4):
        sel = q == qq
        rec[f"liq_share_q{qq + 1}"] = cat_share(sel, 1)
        rec[f"gate_fail_share_q{qq + 1}"] = cat_share(sel, 2)

    # shadow education
    rec["tut_rate"] = out.get("tut_rate")
    tq = out.get("tut_by_q") or []
    rec["tut_share_q1"] = float(tq[0]) if len(tq) == 5 else None
    rec["tut_share_q5"] = float(tq[4]) if len(tq) == 5 else None
    rec["tut_q5_q1_gap"] = float(tq[4] - tq[0]) if len(tq) == 5 else None

    # secondary transition inequality
    rec["completion_lower"] = out.get("completion_lower")
    rec["completion_upper"] = out.get("completion_upper")
    clq = out.get("completion_lower_q") or []
    rec["completion_lower_q_gap"] = float(clq[4] - clq[0]) if len(clq) == 5 else None
    rec["parity_wealth_lower"] = out.get("parity_wealth_lower")
    rec["completion_upper_q_gap"] = (float(out["completion_upper_q"][4] - out["completion_upper_q"][0])
                                     if out.get("completion_upper_q") and len(out["completion_upper_q"]) == 5 else None)

    # formal jobs / queuing
    rec["formal_rate"] = out.get("formal_rate")
    rec["queue"] = out.get("queue")
    rec["grad_unemp"] = out.get("grad_unemp")
    rec["formal_hire_q1"] = rec["formal_hire_q5"] = None
    finite = np.isfinite(inc)
    for qq in (0, 4):
        sel = (q == qq) & finite
        rec[f"formal_hire_q{qq + 1}"] = float(np.mean(inc[sel] >= 1.3)) if np.any(sel) else None

    # realised X normalisations (vacancies per gate-eligible / lower-complete child)
    vac_year = one.n * vac0
    rec["x_vac_per_entrant"] = vac0
    rec["x_vac_per_lower_complete"] = float(vac_year / max(int(np.sum(cred >= 1)) / n_meas_cohorts, 1e-9))
    rec["x_vac_per_gate_pass"] = float(vac_year / max(int(np.sum(cred >= 2)) / n_meas_cohorts, 1e-9))
    rec["n_pop_measured"] = n
    rec["n_cohorts_measured"] = n_meas_cohorts
    return rec


def summarise(cell_rows):
    """Mean over seeds + seed SD for the headline columns."""
    keys = [k for k in cell_rows[0] if k not in ("x_index", "y_index", "seed", "gate", "x_vac0", "fee_primary")]
    out = {}
    for k in keys:
        vals = np.array([r[k] for r in cell_rows if r[k] is not None], float)
        out[k] = float(np.mean(vals)) if len(vals) else None
        if k in ("liq_share", "gate_fail_share", "censored_share", "tut_rate", "tut_q5_q1_gap",
                 "completion_lower_q_gap", "completion_lower", "formal_rate", "queue") and len(vals) > 1:
            out[f"sd_{k}"] = float(np.std(vals, ddof=1))
        elif len(vals) > 1:
            out[f"sd_{k}"] = float(np.std(vals, ddof=1))
    return out


def main():
    ap = argparse.ArgumentParser(description="Quick phase sweep (SIMULATION ONLY)")
    ap.add_argument("--engine-root", required=True, help="path to engine/ dir containing worlds.py")
    ap.add_argument("--out", required=True, help="output directory (created; only place written)")
    ap.add_argument("--workers", type=int, default=12, help="parallel workers (box quota <=12)")
    ap.add_argument("--seeds", type=int, default=5, help="seeds per cell (0..seeds-1)")
    ap.add_argument("--gate", default="bar", choices=["bar", "quota", "bar_binding"], help="exam-gate rule (bar_binding = exploratory)")
    ap.add_argument("--x-levels", default=None, help="comma list overriding X (vac0) levels")
    ap.add_argument("--y-levels", default=None, help="comma list overriding Y (fee) levels")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--t", type=int, default=70)
    ap.add_argument("--measure-from", type=int, default=35)
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()

    global X_LEVELS, Y_LEVELS
    if a.x_levels:
        X_LEVELS = [float(x) for x in a.x_levels.split(",")]
    if a.y_levels:
        Y_LEVELS = [float(x) for x in a.y_levels.split(",")]
    if not (1 <= a.workers <= 32):
        raise SystemExit("workers bound 1..32 (shared 15-core quota)")
    if a.seeds < 1 or a.seeds > 40:
        raise SystemExit("seeds bound 1..40")

    engine_root = os.path.abspath(a.engine_root)
    if not os.path.isfile(os.path.join(engine_root, "worlds.py")):
        raise SystemExit(f"--engine-root must contain worlds.py: {engine_root}")
    if not os.path.isdir(os.path.join(engine_root, "eduengine")):
        raise SystemExit(f"--engine-root must contain eduengine/: {engine_root}")
    out_dir = os.path.abspath(a.out)
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "phase_sweep_quick_summary.csv")
    json_path = os.path.join(out_dir, "phase_sweep_quick_summary.json")
    if not a.overwrite and (os.path.exists(csv_path) or os.path.exists(json_path)):
        raise SystemExit(f"outputs already exist in {out_dir} (use --overwrite)")

    tasks = [(xi, yi, s) for xi in range(len(X_LEVELS)) for yi in range(len(Y_LEVELS))
             for s in range(a.seeds)]
    t0 = time.time()
    one.engine_root, one.gate = engine_root, a.gate   # set BEFORE forking so workers inherit them
    one.n, one.t, one.measure_from = a.n, a.t, a.measure_from
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=8)
    elapsed = time.time() - t0

    # aggregate per cell
    cells = []
    for xi in range(len(X_LEVELS)):
        for yi in range(len(Y_LEVELS)):
            cr = [r for r in rows if r["x_index"] == xi and r["y_index"] == yi]
            s = summarise(cr)
            s.update(dict(x_index=xi, x_vac0=X_LEVELS[xi], y_index=yi, fee_primary=Y_LEVELS[yi],
                          gate=a.gate, n_seeds=len(cr)))
            cells.append(s)
    cells.sort(key=lambda r: (r["x_index"], r["y_index"]))

    # partition check: exit categories must sum to 1 (allow only float noise)
    for r in cells:
        tot = sum(r.get(f"{k}_share") or 0.0 for k, _n, _c in SHARE_CATS)
        if abs(tot - 1.0) > 1e-6:
            raise RuntimeError(f"exit partition does not sum to 1 in cell x={r['x_vac0']} y={r['fee_primary']}: {tot}")

    cols = ["gate", "x_index", "x_vac0", "x_vac_per_entrant", "x_vac_per_lower_complete",
            "x_vac_per_gate_pass", "y_index", "fee_primary", "n_seeds",
            "liq_share", "gate_fail_share", "censored_share", "choice_share", "never_share",
            "no_seat_share", "not_admitted_share", "finished_share",
            "liq_share_q1", "gate_fail_share_q1", "liq_share_q5", "gate_fail_share_q5",
            "tut_rate", "tut_share_q1", "tut_share_q5", "tut_q5_q1_gap",
            "completion_lower", "completion_upper", "completion_lower_q_gap", "completion_upper_q_gap",
            "parity_wealth_lower", "formal_rate", "formal_hire_q1", "formal_hire_q5", "queue", "grad_unemp",
            "sd_liq_share", "sd_gate_fail_share", "sd_censored_share", "sd_tut_rate", "sd_tut_q5_q1_gap",
            "sd_completion_lower_q_gap", "sd_completion_lower", "sd_formal_rate", "sd_queue"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in cells:
            w.writerow({k: r.get(k) for k in cols})

    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, fn) for dp, _dd, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for fn in fs if fn.endswith(".py")])
    data = {
        "label": LABEL,
        "experiment": "phase_sweep_quick",
        "design": {"axes": {"X_vac0_formal_vacancies_per_entrant": X_LEVELS,
                            "Y_fee_primary_share_of_median_income": Y_LEVELS,
                            "gate": a.gate},
                   "n_cells": len(cells), "seeds": a.seeds, "runs": len(rows),
                   "N": a.n, "T": a.t, "measure_from": a.measure_from, "workers": a.workers,
                   "base_world": "formal_loop",
                   "notes": ["primary fee applies to grades 1-6 only (E8 fee); 0.0 = abolition slice",
                             "X grid is vac0 (formal vacancies per cohort entrant); realised vacancies per "
                             "gate-passing child is x_vac_per_gate_pass",
                             "queue_on=True so the credential queue is explicit",
                             "exits read from e.exits only; censored-at-horizon is its own category"],
                   "missing_mechanisms": ["migration/emigration", "rural-urban sorting/residential choice",
                                          "remittances/kin transfers", "country-specific calibration",
                                          "informal/formal composition beyond queue vs competitive"]},
        "cells": cells,
        "elapsed_s": round(elapsed, 3),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
        "engine_root": engine_root,
        "code_sha256": {**{os.path.relpath(pp, engine_root): _sha256(pp) for pp in engine_files},
                        "phase_sweep_quick.py": _sha256(os.path.abspath(__file__))},
    }
    with open(json_path, "w") as f:
        json.dump(data, f)
    print(json.dumps({"runs": len(rows), "cells": len(cells), "seeds": a.seeds, "gate": a.gate,
                      "elapsed_s": data["elapsed_s"], "workers": a.workers,
                      "csv": csv_path, "json": json_path}))


if __name__ == "__main__":
    main()
