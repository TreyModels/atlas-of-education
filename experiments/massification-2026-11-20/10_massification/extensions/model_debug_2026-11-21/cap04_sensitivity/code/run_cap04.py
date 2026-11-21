#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEBUG DRIVER -- CAP-04 sensitivity: survival floor 0.02 vs 0.0 (copies only).

LABEL: DEBUG. Two copies of the v1.3 generator (both carrying the CAP-01 one-sided-floor fix)
differ ONLY in the survival clamp floor: 0.02 (CAP-04 as delivered) vs 0.0 (sensitivity).
Same seed, draw order, inputs, shadow settings. Writes one panel per variant.
"""
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABEL = "DEBUG"

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def run(m, outdir, tag):
    m.guard_hashes()
    inputs = m.shadow_inputs_named()
    res_off, *_ = m.run_all(shadow=False)
    hosts, _gdp = m.resolve_hosts(res_off)
    res, ptr_obs, spend_obs, S_phl, P_phl = m.run_all(beh=m.SHADOW_BEHAV, shadow=True, inputs=inputs, hosts=hosts)
    rows = m.build_panel_v13(res, hosts, inputs)
    path = outdir / ("synthetic_panel_v1_3_%s.csv" % tag)
    m.write_panel_v13(rows, path)
    return path, rows

def main():
    out = HERE.parent / "results" / "panels"
    out.mkdir(parents=True, exist_ok=True)
    meta = {}
    for tag, fn in (("floor002", "sim_v1_3_floor002.py"), ("floor000", "sim_v1_3_floor000.py")):
        m = load("sim_v1_3_" + tag, fn)
        path, rows = run(m, out, tag)
        meta[tag] = {"path": str(path), "n_rows": len(rows), "seed": int(m.SEED)}
        print(tag, path, len(rows), flush=True)
    (HERE.parent / "results" / "RUNS.json").write_text(json.dumps({"label": LABEL, "runs": meta}, indent=2))

if __name__ == "__main__":
    main()
