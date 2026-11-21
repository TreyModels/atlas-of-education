#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEBUG DRIVER -- run the repaired v1.2 / v1.3 generator copies and emit the repaired panel.

LABEL: DEBUG. This driver executes the copy in this directory (one named defect repaired:
the `completion_uis` 1.0 ceiling -> one-sided floor). It imports the copy as a module, runs
the same simulation call the delivered generator's `main()` makes, and writes the panel.
No parameter, seed, threshold, draw order or input changes. No clock in outputs.

The copy resolves every frozen INPUT from the original generator directory
(`synthetic_2026-11-20/generator_v1_{2,3}/`); only the CAP-01 expression differs.

Usage:
  python run_repaired.py --generator v1_3 --out DIR
  python run_repaired.py --generator v1_2 --out DIR
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXDIR = HERE.parent
LABEL = "DEBUG"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def guard_v13(m):
    m.guard_hashes()
    return {
        "prerdecl_v1_2_sha256": m.EXPECTED_PREDECL_SHA,
        "shadow_predecl_sha256": m.EXPECTED_SHADOW_PREDECL_SHA,
        "shadow_s1_sha256": m.EXPECTED_SHADOW_S1_SHA,
        "params_md_sha256": m.EXPECTED_PARAMS_SHA,
    }


def run_v13(m, outdir):
    inputs = m.shadow_inputs_named()
    # shadow-OFF run: host mapping rule is declared on the v1.2 (shadow-off) state
    res_off, *_ = m.run_all(shadow=False)
    hosts, _gdp = m.resolve_hosts(res_off)
    # scored (shadow ON) run: byte-identical call to the delivered generator's main()
    res, ptr_obs, spend_obs, S_phl, P_phl = m.run_all(
        beh=m.SHADOW_BEHAV, shadow=True, inputs=inputs, hosts=hosts)
    rows = m.build_panel_v13(res, hosts, inputs)
    path = outdir / "synthetic_panel_v1_3_repaired.csv"
    m.write_panel_v13(rows, path)
    return path, rows, hosts


def run_v12(m, outdir):
    # same frozen-predeclaration enforcement the delivered main() performs
    if not m.PREDECL.exists():
        raise SystemExit("REFUSING TO RUN: v1.2 predeclaration not found")
    got = sha256_file(m.PREDECL)
    if got != m.EXPECTED_PREDECL_SHA:
        raise SystemExit("REFUSING TO RUN: v1_2/PRE_DECLARATIONS.md sha256 changed")
    res, ptr_obs, spend_obs, S_phl, P_phl = m.run_all()
    rows = m.build_panel(res)
    path = outdir / "synthetic_panel_v1_2_repaired.csv"
    m.write_panel(rows, path)
    return path, rows, {"frozen_predeclaration_sha256": got}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--generator", choices=("v1_2", "v1_3"), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.generator == "v1_3":
        m = load("sim_v1_3_fix", "sim_v1_3_fix.py")
        guard = guard_v13(m)
        path, rows, hosts = run_v13(m, outdir)
        meta = {
            "label": LABEL,
            "generator": "sim_v1_3_fix.py (copy of generator_v1_3/code/sim_v1_3.py)",
            "seed": int(m.SEED),
            "n_rows": len(rows),
            "panel_sha256": sha256_file(path),
            "host_mapping": hosts,
            "frozen_hashes_enforced": guard,
            "fix": "out[\"comp_uis\"][L, t] = max(0.0, P[\"meas_completion_factor\"] * comp_coh)"
                   "  # was clip(..., 0.0, 1.0)",
            "no_clock_in_outputs": True,
            "no_rng_change": True,
        }
    else:
        m = load("sim_v1_2_fix", "sim_v1_2_fix.py")
        path, rows, guard = run_v12(m, outdir)
        meta = {
            "label": LABEL,
            "generator": "sim_v1_2_fix.py (copy of generator_v1_2/code/sim_v1_2.py)",
            "seed": int(m.SEED),
            "n_rows": len(rows),
            "panel_sha256": sha256_file(path),
            "frozen_hashes_enforced": guard,
            "fix": "out[\"comp_uis\"][L, t] = max(0.0, P[\"meas_completion_factor\"] * comp_coh)"
                   "  # was clip(..., 0.0, 1.0)",
            "no_clock_in_outputs": True,
            "no_rng_change": True,
        }
    meta["panel_file"] = path.name
    (outdir / "RUN_META.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("[%s] %s -> %s (%d rows) sha256=%s" % (
        LABEL, args.generator, path, len(rows), meta["panel_sha256"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
