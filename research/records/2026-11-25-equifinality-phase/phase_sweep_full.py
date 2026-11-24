#!/usr/bin/env python3
"""phase_sweep_full.py — SIMULATION ONLY (eduengine toy worlds; no empirical/causal claims).

Full equifinality phase sweep: E8-style primary-fee abolition (Y) x formal-vacancy bottleneck (X) x gate
regime, 20 x 20 x {bar,quota} x 20 seeds = 16,000 runs. Strict extension of the committed
`research/records/2026-11-25-phase-transition/phase_sweep_quick.py` (same driver-side fee subclass, same
`aggregate_exits` partition, same axes); grid, gates, seeds, per-run failure preservation and gate-binding
diagnostics are extended per `PRE_REGISTRATION.md` (commit 078cc13) in this directory.

CONTEST GATE: NOT-IMPLEMENTED and NOT proxied. The engine's `Engine.step` inlines the gate decision with
exactly two branches (`if gate['kind'] == 'bar': ... else: # quota ...`), the Module API has no gate hook to
subclass, and `grep -rn contest` over the engine tree finds one comment (`eduengine/modules/labour.py:39`);
an unknown kind would be silently treated as quota. See PRE_REGISTRATION.md §3 for the full evidence.

Axes (exact, pre-registered):
  X  20 levels of `vac0` (formal vacancies per cohort entrant), geomspace(0.01, 0.80, 20) at 4 sig digits.
  Y  20 levels of `fee_primary` (primary-school fee per year as a share of median income, grades 1-6 only),
     0.00..0.19 step 0.01; `0.00` is the E8 abolition slice.

Fixed: formal_loop world, N=400, T=70, measure_from=35, queue_on=True, vac_growth=0.0, seeds 0..19 per cell,
seeds identical across cells. Exits are read ONLY from `e.exits` via `aggregate_exits()` (core.step compacts
exited children out of the state, so `e.kids['reason']` is all -1 after run() BY DESIGN); survivors still in
the state are the `censored` category and the exit shares partition the measured population to 1.0.

Usage (box):
  /root/miniconda3/bin/python phase_sweep_full.py \
      --engine-root /root/work/edsystem/engine --out /root/work/equifinality_phase \
      --workers 12 --seeds 20 --gate all

Writes only inside --out. No power/reboot/shutdown commands. No watchers/timers. Deterministic seeds.
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

# --- pre-registered grid (PRE_REGISTRATION.md §2; must match exactly) -------------------------------------
X_LEVELS = [0.01, 0.01259, 0.01586, 0.01998, 0.02516, 0.03168, 0.0399, 0.05025, 0.06329, 0.0797,
            0.1004, 0.1264, 0.1592, 0.2005, 0.2525, 0.318, 0.4005, 0.5044, 0.6352, 0.8]   # vac0: severe -> slack
Y_LEVELS = [round(i * 0.01, 2) for i in range(20)]                                        # fee: abolition -> high
assert len(X_LEVELS) == 20 and len(Y_LEVELS) == 20
assert all(X_LEVELS[i] < X_LEVELS[i + 1] for i in range(19))
assert Y_LEVELS[0] == 0.0 and Y_LEVELS[-1] == 0.19

GATES = {
    "bar": [dict(kind="bar", bar=b) for b in (3.0, 5.5, 8.0, 11.5)],
    "quota": [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
              dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)],
}
GATE_NAMES = ["bar", "quota"]          # 'contest' deliberately absent: NOT-IMPLEMENTED (prereg §3)

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


def _r(x, nd=9):
    """Round a float for the CSV (keeps the committed file small); None passes through."""
    return None if x is None else round(float(x), nd)


def one(task):
    """One (gate, x, y, seed) run. Failures are preserved as ok=False rows, never dropped."""
    gate, xi, yi, seed = task
    try:
        return _one(gate, xi, yi, seed)
    except Exception as ex:                     # preserve the failure row (prereg §5, §9)
        import traceback
        return dict(gate=gate, x_index=xi, x_vac0=X_LEVELS[xi], y_index=yi, fee_primary=Y_LEVELS[yi],
                    seed=seed, ok=False, error=f"{type(ex).__name__}: {ex}"[:400],
                    traceback=traceback.format_exc()[-1500:])


def _one(gate, xi, yi, seed):
    vac0, fee = X_LEVELS[xi], Y_LEVELS[yi]
    e = make_engine(one.engine_root, vac0, fee, gate, seed, one.n, one.t, one.measure_from)
    out = e.run()

    pop = aggregate_exits(e)
    mask = np.asarray(pop["cohort"]) >= one.measure_from
    reason = np.asarray(pop["reason"], int)[mask]
    y = np.asarray(pop["y"], float)[mask]
    inc = np.asarray(pop["inc"], float)[mask]
    cred = np.asarray(pop["cred"], int)[mask]
    n = int(mask.sum())
    if n == 0:
        raise RuntimeError("measured population is empty")
    cuts = np.quantile(y, [0.2, 0.4, 0.6, 0.8]) if n else np.zeros(4)
    q = np.searchsorted(cuts, y, side="right")
    n_meas_cohorts = max(len(np.unique(np.asarray(pop["cohort"])[mask])), 1)

    rec = {"gate": gate, "x_index": xi, "x_vac0": vac0, "y_index": yi, "fee_primary": fee, "seed": seed}

    def cat_share(sel, code):
        return float(np.mean(reason[sel] == code)) if np.any(sel) else None

    for key, _name, code in SHARE_CATS:
        rec[f"{key}_share"] = cat_share(np.ones(n, bool), code)
    for qq in (0, 4):
        sel = q == qq
        rec[f"liq_share_q{qq + 1}"] = cat_share(sel, 1)
        rec[f"gate_fail_share_q{qq + 1}"] = cat_share(sel, 2)

    # ---- exit-partition validity check (prereg §1, §9): must sum to 1 within 1e-6
    tot = sum(rec[f"{k}_share"] or 0.0 for k, _n, _c in SHARE_CATS)
    if abs(tot - 1.0) > 1e-6:
        raise RuntimeError(f"exit partition does not sum to 1 (sum={tot})")

    # ---- PRIMARY equifinality metrics (prereg §5, §6)
    # GER_sim = 1 - never_enrolled_share: DECLARED SIMULATED participation, not an empirical GER.
    rec["ger_sim"] = (1.0 - rec["never_share"]) if rec["never_share"] is not None else None

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

    # gate-binding diagnostics (prereg §8.3): realised pass rates and final cutoffs, descriptive only
    pr = np.atleast_1d(np.asarray(getattr(e, "pass_rate", []), float))
    for j in range(min(len(pr), 4)):
        rec[f"gate_pass_rate_{j}"] = float(pr[j])
    for j in range(min(len(e.cut), 4)):
        rec[f"cut_{j}"] = float(e.cut[j])
    for j in range(min(len(e.cut_adm), 4)):
        rec[f"cut_adm_{j}"] = float(e.cut_adm[j])

    # realised X normalisations (vacancies per gate-eligible / lower-complete child)
    vac_year = one.n * vac0
    rec["x_vac_per_entrant"] = vac0
    rec["x_vac_per_lower_complete"] = float(vac_year / max(int(np.sum(cred >= 1)) / n_meas_cohorts, 1e-9))
    rec["x_vac_per_gate_pass"] = float(vac_year / max(int(np.sum(cred >= 2)) / n_meas_cohorts, 1e-9))
    rec["n_pop_measured"] = n
    rec["n_cohorts_measured"] = n_meas_cohorts
    rec["ok"] = True
    rec["error"] = ""

    # round floats for the committed CSV (shares/gaps are pp-precision statistics)
    return {k: (_r(v) if isinstance(v, float) and k not in ("x_vac0", "fee_primary") else v)
            for k, v in rec.items()}


ID_KEYS = ("gate", "x_index", "y_index", "seed", "x_vac0", "fee_primary", "ok", "error")
PRIMARY = ("ger_sim", "liq_share", "tut_rate")
SD_KEYS = ("ger_sim", "liq_share", "tut_rate", "tut_q5_q1_gap", "completion_lower", "completion_lower_q_gap",
           "gate_fail_share", "censored_share", "formal_rate", "queue", "liq_share_q1", "gate_fail_share_q1")


def summarise(cell_rows):
    """Mean over OK seeds + seed SD for the headline columns. n_seeds_ok is recorded, failures are kept."""
    ok_rows = [r for r in cell_rows if r.get("ok")]
    keys = [k for k in cell_rows[0] if k not in ID_KEYS and k not in ("traceback",)]
    out = {"n_seeds": len(cell_rows), "n_seeds_ok": len(ok_rows),
           "n_failed": len(cell_rows) - len(ok_rows)}
    for k in keys:
        if k in ID_KEYS:
            continue
        vals = np.array([r[k] for r in ok_rows if r.get(k) is not None], float)
        out[k] = float(np.mean(vals)) if len(vals) else None
        out[f"sd_{k}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else None
    return out


CELL_COLS = ["gate", "x_index", "x_vac0", "x_vac_per_entrant", "x_vac_per_lower_complete",
             "x_vac_per_gate_pass", "y_index", "fee_primary", "n_seeds", "n_seeds_ok", "n_failed",
             "ger_sim", "sd_ger_sim",
             "liq_share", "sd_liq_share", "gate_fail_share", "sd_gate_fail_share",
             "censored_share", "sd_censored_share", "choice_share", "never_share",
             "no_seat_share", "not_admitted_share", "finished_share",
             "liq_share_q1", "gate_fail_share_q1", "liq_share_q5", "gate_fail_share_q5",
             "tut_rate", "sd_tut_rate", "tut_share_q1", "tut_share_q5", "tut_q5_q1_gap", "sd_tut_q5_q1_gap",
             "completion_lower", "sd_completion_lower", "completion_upper", "completion_lower_q_gap",
             "sd_completion_lower_q_gap", "completion_upper_q_gap", "parity_wealth_lower",
             "formal_rate", "sd_formal_rate", "formal_hire_q1", "formal_hire_q5", "queue", "sd_queue",
             "grad_unemp",
             "gate_pass_rate_0", "gate_pass_rate_1", "gate_pass_rate_2", "gate_pass_rate_3",
             "cut_0", "cut_1", "cut_2", "cut_3", "cut_adm_0", "cut_adm_1", "cut_adm_2", "cut_adm_3"]

RUN_COLS = ["gate", "x_index", "x_vac0", "y_index", "fee_primary", "seed", "ok", "error",
            "ger_sim", "liq_share", "tut_rate", "tut_q5_q1_gap", "completion_lower", "completion_upper",
            "liq_share_q1", "gate_fail_share_q1", "liq_share_q5", "gate_fail_share_q5",
            "tut_share_q1", "tut_share_q5", "completion_lower_q_gap", "completion_upper_q_gap",
            "parity_wealth_lower", "formal_rate", "formal_hire_q1", "formal_hire_q5", "queue", "grad_unemp",
            "liq_share", "gate_fail_share", "censored_share", "choice_share", "never_share",
            "no_seat_share", "not_admitted_share", "finished_share",
            "gate_pass_rate_0", "gate_pass_rate_1", "gate_pass_rate_2", "gate_pass_rate_3",
            "cut_0", "cut_1", "cut_2", "cut_3", "cut_adm_0", "cut_adm_1", "cut_adm_2", "cut_adm_3",
            "x_vac_per_lower_complete", "x_vac_per_gate_pass", "n_pop_measured", "n_cohorts_measured"]
RUN_COLS = list(dict.fromkeys(RUN_COLS))   # de-duplicate (liq_share etc. appear once)


def main():
    ap = argparse.ArgumentParser(description="Full equifinality phase sweep (SIMULATION ONLY)")
    ap.add_argument("--engine-root", required=True, help="path to engine/ dir containing worlds.py")
    ap.add_argument("--out", required=True, help="output directory (created; only place written)")
    ap.add_argument("--workers", type=int, default=12, help="parallel workers (box quota <=12)")
    ap.add_argument("--seeds", type=int, default=20, help="seeds per cell (0..seeds-1)")
    ap.add_argument("--gate", default="all", choices=["bar", "quota", "all"], help="exam-gate rule(s)")
    ap.add_argument("--x-levels", default=None, help="comma list overriding X (vac0) levels (smoke tests)")
    ap.add_argument("--y-levels", default=None, help="comma list overriding Y (fee) levels (smoke tests)")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--t", type=int, default=70)
    ap.add_argument("--measure-from", type=int, default=35)
    ap.add_argument("--prefix", default="phase_sweep_full", help="output filename prefix")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()

    global X_LEVELS, Y_LEVELS
    if a.x_levels:
        X_LEVELS = [float(x) for x in a.x_levels.split(",")]
    if a.y_levels:
        Y_LEVELS = [float(x) for x in a.y_levels.split(",")]
    gates = GATE_NAMES if a.gate == "all" else [a.gate]
    for g in gates:
        assert g in GATES, g
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
    runs_csv = os.path.join(out_dir, f"{a.prefix}_runs.csv")
    csv_path = os.path.join(out_dir, f"{a.prefix}_summary.csv")
    json_path = os.path.join(out_dir, f"{a.prefix}_summary.json")
    if not a.overwrite and any(os.path.exists(p) for p in (csv_path, json_path, runs_csv)):
        raise SystemExit(f"outputs already exist in {out_dir} (use --overwrite)")

    tasks = [(g, xi, yi, s) for g in gates for xi in range(len(X_LEVELS))
             for yi in range(len(Y_LEVELS)) for s in range(a.seeds)]
    t0 = time.time()
    one.engine_root = engine_root        # set BEFORE forking so workers inherit them
    one.n, one.t, one.measure_from = a.n, a.t, a.measure_from
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=8)
    elapsed = time.time() - t0

    ok_rows = [r for r in rows if r.get("ok")]
    failed = [r for r in rows if not r.get("ok")]

    # aggregate per cell (all gates)
    cells = []
    for g in gates:
        for xi in range(len(X_LEVELS)):
            for yi in range(len(Y_LEVELS)):
                cr = [r for r in rows if r["gate"] == g and r["x_index"] == xi and r["y_index"] == yi]
                s = summarise(cr)
                s.update(dict(gate=g, x_index=xi, x_vac0=X_LEVELS[xi], y_index=yi,
                              fee_primary=Y_LEVELS[yi]))
                cells.append(s)
    cells.sort(key=lambda r: (r["gate"], r["x_index"], r["y_index"]))

    # partition check on the cell means (prereg §1, §9)
    for r in cells:
        if not r["n_seeds_ok"]:
            continue
        tot = sum(r.get(f"{k}_share") or 0.0 for k, _n, _c in SHARE_CATS)
        if abs(tot - 1.0) > 1e-6:
            raise RuntimeError(f"cell exit partition does not sum to 1 in cell gate={r['gate']} "
                               f"x={r['x_vac0']} y={r['fee_primary']}: {tot}")

    # per-run CSV (all 16,000 rows, failures preserved)
    with open(runs_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=RUN_COLS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # per-cell summary CSV
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CELL_COLS, extrasaction="ignore")
        w.writeheader()
        for r in cells:
            w.writerow(r)

    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, fn) for dp, _dd, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for fn in fs if fn.endswith(".py")])
    data = {
        "label": LABEL,
        "experiment": "equifinality_phase_sweep_full",
        "prereg": "research/records/2026-11-25-equifinality-phase/PRE_REGISTRATION.md (commit 078cc13)",
        "design": {"axes": {"X_vac0_formal_vacancies_per_entrant": X_LEVELS,
                            "Y_fee_primary_share_of_median_income": Y_LEVELS,
                            "gate": gates},
                   "n_cells": len(cells), "seeds": a.seeds, "runs": len(rows),
                   "runs_ok": len(ok_rows), "runs_failed": len(failed),
                   "N": a.n, "T": a.t, "measure_from": a.measure_from, "workers": a.workers,
                   "base_world": "formal_loop",
                   "contest_gate": "NOT-IMPLEMENTED (no engine gate hook; core.step has only bar/quota "
                                   "branches and silently treats unknown kinds as quota; grep contest = one "
                                   "labour.py comment). See PREREGISTRATION §3. Not proxied.",
                   "notes": ["primary fee applies to grades 1-6 only (E8 fee); 0.0 = abolition slice",
                             "X grid is vac0 (formal vacancies per cohort entrant); realised vacancies per "
                             "gate-passing child is x_vac_per_gate_pass",
                             "queue_on=True so the credential queue is explicit",
                             "exits read from e.exits only; censored-at-horizon is its own category",
                             "GER_sim = 1 - never_enrolled_share = DECLARED SIMULATED participation, "
                             "not an empirical GER",
                             "failures are preserved as ok=False rows and counted in n_failed"],
                   "missing_mechanisms": ["migration/emigration", "rural-urban sorting/residential choice",
                                          "remittances/kin transfers", "country-specific calibration",
                                          "informal/formal composition beyond queue vs competitive"]},
        "cells": cells,
        "failures": [{"gate": r["gate"], "x_index": r["x_index"], "y_index": r["y_index"],
                      "seed": r["seed"], "error": r.get("error")} for r in failed],
        "elapsed_s": round(elapsed, 3),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
        "engine_root": engine_root,
        "code_sha256": {**{os.path.relpath(pp, engine_root): _sha256(pp) for pp in engine_files},
                        "phase_sweep_full.py": _sha256(os.path.abspath(__file__))},
    }
    with open(json_path, "w") as f:
        json.dump(data, f)
    print(json.dumps({"label": LABEL, "runs": len(rows), "runs_ok": len(ok_rows),
                      "runs_failed": len(failed), "cells": len(cells), "seeds": a.seeds,
                      "gates": gates, "elapsed_s": data["elapsed_s"], "workers": a.workers,
                      "csv": csv_path, "json": json_path, "runs_csv": runs_csv}))


if __name__ == "__main__":
    main()
