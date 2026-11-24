#!/usr/bin/env python3
"""Self-contained regression tests for the frozen dashboard's fractional formal-share handling (numpy only).

The dashboard is the measurement layer: it must report the expected formal-work share the behavioural core returns,
not re-binarise a fractional-mass array to a whole-cell "employed" indicator. Old line:
``formal = np.asarray(d["formal"], bool)`` -- a cell that is 50% formally employed was reported as 1.0.

Run:  python3 test_dashboard_fixes.py [--model-dir DIR] [--scripts-dir DIR]
SIMULATION only; no empirical or causal claim.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RECORD)))


def _arg(argv, flag, default):
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            return os.path.abspath(argv[i + 1])
    return default


MODEL = _arg(sys.argv[1:], "--model-dir", os.environ.get("MASSENG_MODEL_DIR") or
             os.path.join(REPO, "research", "masseng-v6"))
SCRIPTS = _arg(sys.argv[1:], "--scripts-dir", os.environ.get("GJ_SCRIPTS_DIR") or
               os.path.join(RECORD, "scripts"))
os.environ["MASSENG_MODEL_DIR"] = MODEL
sys.path.insert(0, MODEL)
sys.path.insert(0, SCRIPTS)
for _mod in [m for m in list(sys.modules) if m.startswith("masseng_v6")]:
    del sys.modules[_mod]

from model_blocks import Params, simulate  # noqa: E402
from dashboard import outcomes  # noqa: E402

CASES = []


def check(name, ok, detail):
    CASES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


raw = simulate(Params(n=8000, seed=0))

# D1: mass-carrying cells can be partially formal; the dashboard must keep the expected share, not binarise it.
raw_frac = dict(raw)
raw_frac["formal"] = np.full(raw["n"], 0.5, float)
o = outcomes(raw_frac)
check("D1 dashboard keeps a 0.5 fractional formal share (old bool cast reported 1.0)",
      np.isfinite(o["formal_share"]) and abs(o["formal_share"] - 0.5) < 1e-9,
      f"formal_share={o['formal_share']!r} (want 0.5)")

# D2: end-to-end the declared vacancy rate is what the dashboard reports for the full model.
o2 = outcomes(raw)
check("D2 full model through the dashboard reports formal_share == vacancy rate 0.25",
      np.isfinite(o2["formal_share"]) and abs(o2["formal_share"] - 0.25) < 0.01,
      f"formal_share={o2['formal_share']!r}")

# D3: derivative read-outs of formal status are also fractions, in [0, 1].
vals = np.asarray(o["formal_share_by_credential"], float)
check("D3 formal_share_by_credential stays in [0, 1] under a fractional input",
      np.all(np.isfinite(vals)) and vals.min() >= -1e-12 and vals.max() <= 1.0 + 1e-12,
      f"values={vals.tolist()}")

n_pass = sum(1 for _, ok, _ in CASES if ok)
print(f"\nSUMMARY: {n_pass}/{len(CASES)} PASS (model dir: {MODEL}; scripts dir: {SCRIPTS})")
raise SystemExit(0 if n_pass == len(CASES) else 1)
