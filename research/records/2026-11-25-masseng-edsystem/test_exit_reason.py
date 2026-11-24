#!/usr/bin/env python3
"""Regression test for the exit-reason read (Neon audit, 2026-11-25).

THE BUG THIS GUARDS AGAINST
    engine/eduengine/core.py compacts exited children out of the state at the end of every step
    (``keep = k['reason'] < 0; self.kids = {kk: v[keep] ...}``) and stores them in ``e.exits``.
    So after ``e.run()``, ``e.kids['reason']`` is all -1. A driver that reads ``e.kids['reason']``
    therefore reports liquidity == choice == never == 0 and started_share == 1.0 for every run --
    a silent, universal false negative, not an engine bug. The first version of
    ``run_edsystem_multiverse.py`` did exactly that; this test pins the correct read.

Run (needs numpy + scipy):
    python3 test_exit_reason.py [--engine-root PATH]

Exit code 0 = all assertions pass. No server compute, no data files.
"""
import argparse
import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVER = os.path.join(HERE, "run_edsystem_multiverse.py")
AXES = None


def load_driver():
    spec = importlib.util.spec_from_file_location("drv_under_test", DRIVER)
    drv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(drv)
    return drv


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print("ok  -", msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine-root", default=os.path.abspath(os.path.join(HERE, "..", "..", "..", "engine")))
    ap.add_argument("--N", type=int, default=120)
    ap.add_argument("--T", type=int, default=45)
    a = ap.parse_args()

    sys.path.insert(0, a.engine_root)
    import worlds  # noqa: F401  (engine must import cleanly)

    drv = load_driver()
    drv.init_engine(a.engine_root)   # the driver imports the engine lazily
    combos = [tuple(c) for c in __import__("itertools").product(*drv.AXES.values())]
    check(len(combos) == 144, "declared multiverse still has 144 combos")

    for ci in (0, len(combos) - 1):
        combo = combos[ci]
        mods, over = drv.combo_params(combo, 0)
        over.update(N=a.N, T=a.T, measure_from=min(20, a.T - 10), seed=0)
        e = worlds.make("formal_loop", mods=mods, **over)
        o = e.run()

        # (1) The invariant that caused the bug: the engine's remaining state has no exits.
        live_reason = np.asarray(e.kids["reason"], int)
        check(len(live_reason) > 0, f"combo {ci}: survivors still in e.kids")
        check(np.all(live_reason == -1),
              f"combo {ci}: e.kids['reason'] is all -1 (exits are compacted out) -- "
              f"reads of e.kids alone are structurally blind to exits")

        # (2) aggregate_exits rebuilds the full population.
        pop = drv.aggregate_exits(e)
        n_exited = sum(len(np.asarray(b["reason"])) for b in (e.exits or []))
        check(len(pop["reason"]) == len(live_reason) + n_exited,
              f"combo {ci}: population size = survivors + exits ({len(pop['reason'])} rows)")
        check(n_exited > 0, f"combo {ci}: engine recorded exited children ({n_exited})")

        # (3) Reasons are a partition of the population and liquidity is present.
        r = np.asarray(pop["reason"], int)
        check(set(np.unique(r)).issubset({-1, 0, 1, 2, 3, 4, 5, 6}),
              f"combo {ci}: every row has a known reason code")
        check(int(np.sum(r == 1)) > 0,
              f"combo {ci}: liquidity exits exist ({int(np.sum(r == 1))} rows)")
        check(int(np.sum(r == 0)) > 0, f"combo {ci}: choice exits exist ({int(np.sum(r == 0))} rows)")

        # (4) The decomposition the driver reports uses that population and partitions it.
        rec = drv.one((ci, combo, 0))
        g = rec["groups"]
        check(g["n_population"] > g["n_censored"], f"combo {ci}: driver reports exits, not 1.0 survived")
        check(g["n_exits"] > 0, f"combo {ci}: driver n_exits > 0 ({g['n_exits']})")
        for q in ("q1", "q3", "q5", "urban", "rural"):
            d = g[q]
            check(d is not None, f"combo {ci}: group {q} present")
            parts = d["liquidity"] + d["choice"] + d["never"] + d["censored"] + d["other_terminal"]
            check(abs(parts - 1.0) < 1e-9,
                  f"combo {ci}/{q}: categories partition the group (sum={parts:.4f})")
        # liquidity need not appear in every cell (the top quintile can pay in every combo),
        # but it must appear overall and in the poorest quintile.
        check(g["started_liquidity_share"] is not None and g["started_liquidity_share"] > 0.0,
              f"combo {ci}: started-children liquidity share > 0 ({g['started_liquidity_share']:.3f})")
        check(g["q1"]["liquidity"] > 0.0,
              f"combo {ci}/q1: liquidity share > 0 ({g['q1']['liquidity']:.3f})")

    print("\nALL PASS - exit-reason read is correct; the old all-zero result cannot recur silently.")


if __name__ == "__main__":
    main()
