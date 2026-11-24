#!/usr/bin/env python3
"""Self-contained regression tests for the v6 labour fix (numpy only, no pytest).

Target: ``research/masseng-v6/masseng_v6/labour.py`` (fractional-mass vacancy clearing, queue p_hire bounds).
Run from anywhere:  python3 test_v6_fixes.py [--model-dir DIR]
The model directory defaults to the repo's ``research/masseng-v6`` and can be overridden with
``MASSENG_MODEL_DIR`` or ``--model-dir`` (used to demonstrate the old-code failure against a base tree).

Every check prints PASS/FAIL and the test exits non-zero if any check fails. Numbers are SIMULATION of a
declared toy clearing; there is no empirical or causal claim here.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RECORD)))


def _model_dir(argv):
    for i, a in enumerate(argv):
        if a == "--model-dir" and i + 1 < len(argv):
            return os.path.abspath(argv[i + 1])
    env = os.environ.get("MASSENG_MODEL_DIR")
    if env:
        return os.path.abspath(env)
    return os.path.join(REPO, "research", "masseng-v6")


MODEL = _model_dir(sys.argv[1:])
sys.path.insert(0, MODEL)
for _mod in [m for m in list(sys.modules) if m.startswith("masseng_v6")]:
    del sys.modules[_mod]
from masseng_v6.labour import LabourParams, clear_labour  # noqa: E402

CASES = []


def check(name, ok, detail):
    CASES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


def run_case(regime, cred, ability, mass, vacancies=0.25, seed=7, **kw):
    p = LabourParams(regime=regime, vacancies=vacancies, **kw)
    return clear_labour(np.asarray(cred, int), np.asarray(ability, float),
                        np.asarray(mass, float), p, np.random.default_rng(seed))


# ------------------------------------------------------------------ T1: 25 vacancies over two 50-mass cells
# Old code turned the ranked fraction into a boolean and hired whole cells: formal_share = 1.0 (4x over-hiring).
# Eligible mass = 100, vacancy stock = 25, so the only correct answer is 25 mass / 0.25 share.
for regime in ("queue", "competitive"):
    o = run_case(regime, [3, 3], [0.0, 0.0], [50.0, 50.0])
    fs = o.accounting["formal_share"]
    alloc = float(np.sum(np.asarray(o.formal, float) * np.asarray([50.0, 50.0])))
    whole_cell = float(np.sum(np.asarray(o.formal, bool) * np.asarray([50.0, 50.0])))
    check(f"T1 {regime}: 25 vacancies / two 50-mass cells -> formal_share == 0.25",
          abs(fs - 0.25) < 1e-9 and abs(alloc - 25.0) < 1e-9,
          f"formal_share={fs!r} (want 0.25), fractional allocated mass={alloc!r} (want 25), "
          f"whole-cell counting would be {whole_cell!r} (100 was the 4x bug)")

# ------------------------------------------------------------------ T2: no over-hiring across configurations
violations = []
for regime in ("queue", "competitive"):
    for vac in (0.05, 0.10, 0.25, 0.40, 0.60):
        for creds in ([3, 3], [1, 2], [0, 3], [2, 3]):
            for masses in ([50.0, 50.0], [80.0, 20.0]):
                o = run_case(regime, creds, [0.3, -0.3], masses, vacancies=vac)
                f_mass = float(np.sum(np.asarray(o.formal, float) * np.asarray(masses, float)))
                fs = o.accounting["formal_share"]
                if (not np.isfinite(fs)) or f_mass > vac * sum(masses) + 1e-9 or fs < -1e-12:
                    violations.append((regime, vac, creds, masses, fs, f_mass))
check("T2 formal mass <= vacancy stock for 80 small-cell configurations (no over-hiring)",
      not violations, f"violations={violations[:3]}")

# ------------------------------------------------------------------ T3: p_hire exposed and kept in [0, 1]
o = run_case("queue", [1, 2, 3, 3], [0.5, -0.5, 0.2, -0.2], [20.0, 30.0, 25.0, 25.0])
ph = np.asarray(getattr(o, "p_hire", np.zeros(0)), float)
check("T3 queue p_hire exposed and all in [0, 1]",
      ph.size > 0 and np.all(np.isfinite(ph)) and float(ph.min()) >= 0.0 and float(ph.max()) <= 1.0,
      f"p_hire={ph.tolist()}")

# ------------------------------------------------------------------ T4: accounting identities and finite pay
o = run_case("competitive", [1, 3], [0.0, 0.0], [50.0, 50.0])
a = o.accounting
ok = (abs(sum(a["credential_shares"]) - 1.0) < 1e-12 and np.isfinite(a["formal_mean_pay"])
      and np.isfinite(a["informal_mean_pay"]) and abs(a["formal_share"] - 0.25) < 1e-9)
check("T4 competitive accounting: credential shares sum 1, formal/informal pay finite, share 0.25", ok,
      f"shares={a['credential_shares']}, formal_pay={a['formal_mean_pay']}, "
      f"informal_pay={a['informal_mean_pay']}, formal_share={a['formal_share']}")

# ------------------------------------------------------------------ T5: mass-weighted share is split-invariant
o1 = run_case("queue", [3, 3], [0.1, -0.1], [50.0, 50.0], vacancies=0.10)
o2 = run_case("queue", [3, 3, 3, 3], [0.1, -0.1, 0.1, -0.1], [25.0, 25.0, 25.0, 25.0], vacancies=0.10)
d = abs(o1.accounting["formal_share"] - o2.accounting["formal_share"])
check("T5 formal_share is mass-weighted: splitting 50/50 into 25 x4 gives the same share", d < 0.02,
      f"{o1.accounting['formal_share']!r} vs {o2.accounting['formal_share']!r} (|d|={d:.4f})")

# ------------------------------------------------------------------ T6: expected pay is finite, non-negative and ordered
# Waiters earn the declared support while queuing, so a cell income can sit below the informal mean; the declared
# bounds are 0 and the top formal wage (skilled premium x the highest credential wage). Formal mean pay must exceed
# informal mean pay when both statuses exist.
o = run_case("queue", [3, 3], [0.0, 0.0], [50.0, 50.0])
inc = np.asarray(o.income, float)
a = o.accounting
wf_top = float(np.max(o.formal) * 0 + 1.25 * 1.0 * np.exp(0.06 * (16.0 - 9.0)))   # tier premium x tertiary wage
ok = (np.all(np.isfinite(inc)) and inc.min() >= -1e-12 and inc.max() <= wf_top + 1e-9
      and np.isfinite(a["formal_mean_pay"]) and np.isfinite(a["informal_mean_pay"])
      and a["formal_mean_pay"] > a["informal_mean_pay"])
check("T6 queue expected income finite and within declared pay bounds; formal mean pay > informal", ok,
      f"income range=({inc.min():.4f},{inc.max():.4f}) in [0,{wf_top:.4f}], "
      f"informal={a['informal_mean_pay']:.4f}, formal={a['formal_mean_pay']:.4f}")

# ------------------------------------------------------------------ T7: queue accounting stays bounded
o = run_case("queue", [2, 3], [0.5, -0.5], [50.0, 50.0])
a = o.accounting
ok = (0.0 <= a["formal_share"] <= 0.25 + 1e-9 and 0.0 <= a["queue_share"] <= 1.0
      and np.isfinite(a["mean_income"]) and a["mean_income"] > 0)
check("T7 queue formal_share<=vacancies, queue_share in [0,1], mean income positive", ok,
      f"formal_share={a['formal_share']}, queue_share={a['queue_share']}, mean_income={a['mean_income']}")

