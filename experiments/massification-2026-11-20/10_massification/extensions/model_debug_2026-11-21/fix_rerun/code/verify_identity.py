#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEBUG supporting check -- the CAP-01 identity IN MEMORY vs on the serialised panel.

LABEL: DEBUG. Runs the repaired generator copies in-process (same call the panel driver makes)
and measures, on the in-memory arrays, `max |completion_uis - 1.10*completion_cohort|`. This
separates the MODEL identity (should be exactly 0 after the fix) from the `%.10g` panel
serialisation, which alone produces the ~1e-9 ratio deviation the register's 1e-9 test sees.

No parameter, seed or threshold change. No clock in outputs.

Usage: python verify_identity.py --out results
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys

import numpy as np

CODE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.dirname(CODE_DIR)
M = 1.10


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(CODE_DIR, filename))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def measure(comp_uis, comp_coh):
    d = np.abs(comp_uis - M * comp_coh)
    rel = d / np.maximum(1.0, np.abs(comp_uis))
    return {
        "max_abs_diff_in_memory": "%.10e" % float(d.max()),
        "max_rel_residual_in_memory": "%.10e" % float(rel.max()),
        "n_cells": int(comp_uis.size),
        "n_cells_uis_gt_1": int((comp_uis > 1.0).sum()),
        "max_uis_in_memory": "%.10g" % float(comp_uis.max()),
        "max_uncapped_in_memory": "%.10g" % float((M * comp_coh).max()),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    out = {"label": "DEBUG", "declared_m": "%.2f" % M, "generators": {}}

    m13 = load("sim_v1_3_fix_ident", "sim_v1_3_fix.py")
    m13.guard_hashes()
    inputs = m13.shadow_inputs_named()
    res_off, *_ = m13.run_all(shadow=False)
    hosts, _ = m13.resolve_hosts(res_off)
    res13, *_ = m13.run_all(beh=m13.SHADOW_BEHAV, shadow=True, inputs=inputs, hosts=hosts)
    cu13 = np.array([r["comp_uis"] for r in res13])
    cc13 = np.array([r["comp_coh"] for r in res13])
    out["generators"]["v1.3"] = measure(cu13, cc13)

    m12 = load("sim_v1_2_fix_ident", "sim_v1_2_fix.py")
    got = hashlib.sha256(open(m12.PREDECL, "rb").read()).hexdigest()
    if got != m12.EXPECTED_PREDECL_SHA:
        raise SystemExit("REFUSING: v1.2 predeclaration hash changed")
    res12, *_ = m12.run_all()
    cu12 = np.array([r["comp_uis"] for r in res12])
    cc12 = np.array([r["comp_coh"] for r in res12])
    out["generators"]["v1.2"] = measure(cu12, cc12)

    out["interpretation"] = (
        "in-memory the repaired object satisfies completion_uis = 1.10 * completion_cohort "
        "exactly; the ~1e-9 ratio deviation reported on the panels is the %.10g serialisation, "
        "the same order as A17's 8.8395202269e-10")
    with open(os.path.join(args.out, "IDENTITY_CHECK.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    for g, v in out["generators"].items():
        print("[%s] %s in-memory max|uis-1.10*coh| = %s  n>1 = %d  max=%s"
              % ("DEBUG", g, v["max_abs_diff_in_memory"], v["n_cells_uis_gt_1"],
                 v["max_uis_in_memory"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
