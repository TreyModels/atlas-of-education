#!/usr/bin/env python3
"""Full-system behavioural prototype + multiverse over equation choices on the existing eduengine.

Wires the four connected pieces already present in engine/eduengine (family affordability including
forgone child earnings and borrowing; learning/quality via public/private/tutoring supply; limited-
place bar/quota gates; credential->labour queue vs competitive) and varies the equation/mechanism
choices across a bounded multiverse.

PRE-REGISTRATION: PRE_REGISTRATION_masseng_edsystem.md (committed before this code and before runs).
SIMULATION ONLY — toy worlds; illustrative parameters; no causal or empirical claims.
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
LABEL = "SIMULATION ONLY — eduengine toy worlds; illustrative parameters; no causal/empirical claims"

SCALARS = ["completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
           "tut_rate", "mpl_primary", "q_pub", "formal_share_gdp", "edu_gdp",
           "parity_location_lower", "parity_wealth_lower", "parity_location_upper", "parity_wealth_upper"]
ARRAYS = ["tut_by_grade", "tut_by_q", "completion_lower_q", "completion_upper_q", "completion_tertiary_q"]
EXTRA = ["formal_rate", "youth_unemp", "grad_unemp", "skill_premium", "floor_skilled", "floor_routine"]

GATES_BAR = [dict(kind="bar", bar=x) for x in (3.0, 5.5, 8.0, 11.5)]
GATES_QUOTA = [dict(kind="bar", bar=3.0), dict(kind="quota", share=0.55, cut0=7.0),
               dict(kind="quota", share=0.45, cut0=10.0), dict(kind="bar", bar=11.5)]

# axes: each variant is a defensible equation/mechanism choice (illustrative levels)
AXES = {
    "afford": ["cash_only", "credit_constant", "credit_poverty"],
    "supply": ["fixed_budget", "fiscal_loop"],
    "learning": ["public_only", "plus_private", "plus_private_tutoring"],
    "gates": ["bar", "quota"],
    "jobs": ["queue_floors", "competitive"],
    "rural": ["low_penalty", "high_penalty"],
}


def variant(axis, name):
    """Return (module overrides, parameter overrides) for one equation/mechanism choice."""
    if axis == "afford":
        if name == "cash_only":
            return {}, dict(borrow=0.0, need_mode="constant", need_share=0.5)
        if name == "credit_constant":
            return {}, dict(borrow=0.20, need_mode="constant", need_share=0.5)
        return {}, dict(borrow=0.30, need_mode="luxury", need_max=1.0, poverty_line=1.0, need_width=0.35)
    if axis == "supply":
        if name == "fixed_budget":
            return dict(fiscal=False), dict(budget_per_child=0.06)
        return dict(fiscal=True), dict(edu_share=0.18, tax_formal=0.15)
    if axis == "learning":
        if name == "public_only":
            return dict(private=False, tutoring=False), {}
        if name == "plus_private":
            return dict(private=True, tutoring=False), {}
        return dict(private=True, tutoring=True), {}
    if axis == "gates":
        return {}, dict(gates=GATES_BAR if name == "bar" else GATES_QUOTA)
    if axis == "jobs":
        return dict(labour="queue" if name == "queue_floors" else "competitive"), {}
    if axis == "rural":
        if name == "low_penalty":
            return {}, dict(rural_cost=0.01, urban_share=0.60)
        return {}, dict(rural_cost=0.06, urban_share=0.25)
    raise ValueError(axis)


def combo_params(combo, seed):
    mods, over = {}, {}
    for axis, name in zip(AXES, combo):
        m, o = variant(axis, name)
        mods.update(m); over.update(o)
    over.update(N=400, T=70, measure_from=35, seed=seed)
    return mods, over


def clean(v):
    if isinstance(v, (list, tuple, np.ndarray)):
        return [clean(x) for x in v]
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return float(v) if np.isfinite(v) else None
    return v


_G = {}

EXIT_FIELDS = ("reason", "started", "urban", "y", "cohort", "cred")


def aggregate_exits(e):
    """Rebuild the full child population: exit record + survivors still in the state.

    WHY THIS IS NEEDED (Neon line audit, 2026-11-25). ``core.step`` compacts exited children OUT of
    the state every step: it appends their rows to ``e.exits`` and then runs
    ``keep = k['reason'] < 0; self.kids = {kk: v[keep] for kk, v in k.items()}``
    (engine/eduengine/core.py, end of step). Therefore ``e.kids['reason']`` is ALL -1 after
    ``e.run()`` -- reading it (as the first version of this driver did) structurally reports zero
    exits, zero liquidity, zero choice and started_share == 1.0. The exits are not lost: they are in
    ``e.exits``, a list with one dict of arrays per cohort-year in which at least one child exited.

    Survivors still in ``e.kids`` keep reason -1 = censored at the horizon (still inside the system,
    not yet exited). They are concatenated too so that the reported shares sum to 1, and are exposed
    as their own ``censored`` category.
    """
    blocks = list(getattr(e, "exits", None) or [])
    out = {}
    for f in EXIT_FIELDS:
        parts = [np.asarray(b[f]) for b in blocks if f in b]
        if f in e.kids:
            parts.append(np.asarray(e.kids[f]))
        out[f] = np.concatenate(parts) if parts else np.array([])
    return out


def init_engine(engine_root):
    sys.path.insert(0, engine_root)
    import worlds
    _G["worlds"] = worlds


def one(task):
    ci, combo, seed = task
    worlds = _G["worlds"]
    mods, over = combo_params(combo, seed)
    e = worlds.make("formal_loop", mods=mods, **over)
    out = e.run()
    k = aggregate_exits(e)   # NOT e.kids: the engine compacts exits out of the state (see helper)
    y = np.asarray(k["y"], float)
    cuts = np.quantile(y, [0.2, 0.4, 0.6, 0.8])
    qb = np.searchsorted(cuts, y, side="right")
    started = np.asarray(k["started"], bool)
    reason = np.asarray(k["reason"], int)
    urban = np.asarray(k["urban"], bool)
    rec = {"combo_index": ci, "combo": list(combo), "seed": seed,
           "metrics": {m: clean(out.get(m)) for m in SCALARS + EXTRA},
           "arrays": {m: clean(out.get(m)) for m in ARRAYS},
           "groups": {}}
    # push-out decomposition by wealth quintile and rural/urban (liquidity vs choice vs never)
    def dec(mask):
        n = int(mask.sum())
        if n == 0:
            return None
        return {"n": n,
                "liquidity": float(np.mean((reason[mask] == 1))),
                "choice": float(np.mean((reason[mask] == 0))),
                "never": float(np.mean((reason[mask] == 4))),
                "censored": float(np.mean((reason[mask] == -1))),
                "other_terminal": float(np.mean(np.isin(reason[mask], (2, 3, 5, 6)))),
                "started_share": float(np.mean(started[mask]))}
    for qi in range(5):
        rec["groups"][f"q{qi+1}"] = dec(qb == qi)
    rec["groups"]["urban"] = dec(urban)
    rec["groups"]["rural"] = dec(~urban)
    rec["groups"]["n_population"] = int(len(reason))
    rec["groups"]["n_exits"] = int(np.sum(reason >= 0))
    rec["groups"]["n_censored"] = int(np.sum(reason == -1))
    started_exited = started & (reason >= 0)
    rec["groups"]["started_liquidity_share"] = (float(np.mean(reason[started_exited] == 1))
                                                if started_exited.any() else None)
    rec["groups"]["started_choice_share"] = (float(np.mean(reason[started_exited] == 0))
                                             if started_exited.any() else None)
    tg = np.asarray(out.get("tut_by_grade") or [], float)
    if tg.size >= 16:
        gate_adj = float(np.mean(tg[[5, 8, 11]]))
        non_gate = float(np.mean(tg[[3, 6, 9, 12]]))
        levels = {"primary": float(np.sum(tg[0:6])), "lower": float(np.sum(tg[6:9])),
                  "upper": float(np.sum(tg[9:12])), "tertiary": float(np.sum(tg[12:16]))}
        tot = max(sum(levels.values()), 1e-9)
        rec["groups"]["tut_gate_adjacent"] = gate_adj
        rec["groups"]["tut_non_gate"] = non_gate
        rec["groups"]["tut_level_share"] = {k2: v / tot for k2, v in levels.items()}
        rec["groups"]["tut_gate_mass_share"] = float(np.sum(tg[[5, 8, 11]]) / max(np.sum(tg), 1e-9))
    tq = np.asarray(out.get("tut_by_q") or [], float)
    if tq.size == 5:
        rec["groups"]["tut_q_gap_q5_q1"] = float(tq[4] - tq[0])
        rec["groups"]["tut_by_q"] = [float(x) for x in tq]
    for lvl in ("lower", "upper", "tertiary"):
        arr = np.asarray(out.get(f"completion_{lvl}_q") or [], float)
        if arr.size == 5:
            rec["groups"][f"completion_{lvl}_q_gap"] = float(arr[4] - arr[0])
    return rec


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine-root", default=None)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    engine_root = os.path.abspath(a.engine_root or os.path.join(HERE, "..", "..", "..", "engine"))
    if not os.path.exists(os.path.join(engine_root, "worlds.py")):
        raise FileNotFoundError(engine_root)
    if not (1 <= a.workers <= 32):
        raise ValueError("workers bound 1..32 (shared 15-core quota; declared <=12)")
    out_path = os.path.abspath(a.out)
    if os.path.exists(out_path):
        raise FileExistsError(out_path)
    combos = [tuple(c) for c in __import__("itertools").product(*AXES.values())]
    tasks = [(i, combo, seed) for i, combo in enumerate(combos) for seed in range(a.seeds)]
    t0 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(a.workers, initializer=init_engine, initargs=(engine_root,)) as pool:
        rows = pool.map(one, tasks, chunksize=8)
    elapsed = time.time() - t0
    engine_files = sorted([os.path.join(engine_root, "worlds.py")] +
                          [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(engine_root, "eduengine"))
                           for f in fs if f.endswith(".py")])
    data = {"label": LABEL, "experiment": "masseng_edsystem_multiverse",
            "design": {"axes": {k: list(v) for k, v in AXES.items()},
                       "n_combos": len(combos), "seeds": a.seeds, "runs": len(rows),
                       "N": 400, "T": 70, "measure_from": 35, "workers": a.workers,
                       "base_world": "formal_loop",
                       "missing_mechanisms": ["migration/emigration", "rural-urban sorting/residential choice",
                                               "remittances/kin transfers", "country-specific calibration",
                                               "informal/formal employment composition beyond queue vs competitive"]},
            "rows": rows, "elapsed_s": round(elapsed, 3),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "host": socket.gethostname(), "python": sys.version.split()[0], "numpy": np.__version__,
            "engine_root": engine_root,
            "code_sha256": {**{os.path.relpath(p, engine_root): sha256(p) for p in engine_files},
                            "run_edsystem_multiverse.py": sha256(os.path.abspath(__file__))}}
    with open(out_path, "x") as f:
        json.dump(data, f)
    print(json.dumps({"runs": len(rows), "elapsed_s": data["elapsed_s"], "workers": a.workers,
                      "out": out_path}))


if __name__ == "__main__":
    main()
