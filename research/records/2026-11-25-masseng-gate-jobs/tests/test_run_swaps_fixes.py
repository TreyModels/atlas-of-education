#!/usr/bin/env python3
"""Self-contained regression tests for the v6 gate/jobs ``run_swaps.py`` fixes (numpy only, no pytest).

Covers the T1b zero-selection statistic (was always NaN), the T5 structural-multiverse arms (two were
duplicate/no-op), strict-JSON output (no NaN literals) and the end-to-end fractional formal share through
``model_blocks`` -> ``dashboard``.

Run from anywhere:  python3 test_run_swaps_fixes.py [--model-dir DIR] [--scripts-dir DIR]
Defaults: model = repo ``research/masseng-v6``, scripts = this record's ``scripts/``. Overriding both lets the
same tests be run against the base (pre-fix) tree to show the before numbers.
Everything here is SIMULATION of a declared toy model; no empirical or causal claim.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import fields

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

import run_swaps as rs  # noqa: E402
from model_blocks import Params, simulate  # noqa: E402
from dashboard import outcomes  # noqa: E402

CASES = []


def check(name, ok, detail):
    CASES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


def _finite(x):
    try:
        return bool(np.isfinite(float(x)))
    except (TypeError, ValueError):
        return False


# ------------------------------------------------------------------ R1: T1b zero-selection statistic
rows = [rs._zero_selection(s) for s in (0, 1, 2)]
corr_full = [r["ability_admission_corr_full"] for r in rows]
corr_zero = [r["ability_admission_corr_zero"] for r in rows]
ok = (all(_finite(r) for r in corr_full + corr_zero)
      and all(r > 0.05 for r in corr_full)
      and all(abs(r) < 0.05 for r in corr_zero)
      and all(_finite(r["prep_participation_zero"]) for r in rows))
check("R1 T1b: point-biserial ability-admission corr is finite (never NaN), full>0, zero-selection ~0",
      ok, f"full={[round(r, 4) for r in corr_full]}, zero={[round(r, 4) for r in corr_zero]}, "
          f"prep_zero={[r['prep_participation_zero'] for r in rows]}")

# ------------------------------------------------------------------ R2: T5 arms are distinct and self-describing
cfgs = rs.build_configs()
t5 = {}
for c in cfgs:
    if c["arm"].startswith("multi_") and c["seed"] == 0:
        t5[c["arm"]] = c["params"]
base = Params()
base_fields = {f.name: getattr(base, f.name) for f in fields(Params)}
dupes = []
seen = {}
for arm, params in t5.items():
    eff = {f.name: getattr(Params(**params), f.name) for f in fields(Params)}
    for other, prev in seen.items():
        if eff == prev:
            dupes.append((arm, other))
    seen[arm] = eff
noop = [arm for arm, params in t5.items()
        if all(getattr(Params(**params), f.name) == base_fields[f.name] for f in fields(Params))]
naming_bad = []
for arm, params in t5.items():
    p = Params(**params)
    if "concave" in arm and p.prep_form != "concave":
        naming_bad.append((arm, "concave", p.prep_form))
    if "linear" in arm and p.prep_form != "linear":
        naming_bad.append((arm, "linear", p.prep_form))
    if "tullock" in arm and "tullock" not in p.rules:
        naming_bad.append((arm, "tullock", p.rules))
    if "quota" in arm and "quota" not in p.rules:
        naming_bad.append((arm, "quota", p.rules))
    if "bar" in arm and "tullock" not in arm and "quota" not in arm and p.rules != ("bar", "bar", "bar"):
        naming_bad.append((arm, "bar", p.rules))
check("R2 T5 arms: >=4 arms, pairwise-distinct effective Params, none a baseline no-op, name<->params match",
      len(t5) >= 4 and not dupes and not noop and not naming_bad,
      f"arms={sorted(t5)}, duplicates={dupes}, no-op={noop}, name_mismatch={naming_bad}")

# ------------------------------------------------------------------ R3: T5 arms produce finite dashboard moments
bad_moments = []
for arm, params in t5.items():
    raw = simulate(Params(n=4000, seed=0, **params))
    o = outcomes(raw)
    mom = [o["prep_participation"], o["admission_by_quintile"][2][0], o["formal_share"],
           o["pay_by_credential"][3] / o["pay_by_credential"][2], o["queue_share"]]
    if not all(_finite(v) for v in mom):
        bad_moments.append((arm, mom))
check("R3 T5 arms each yield finite dashboard moments (SIMULATION)", not bad_moments,
      f"non-finite={bad_moments}")

# ------------------------------------------------------------------ R4: strict JSON, no NaN/Infinity literals
payload = {"float_nan": float("nan"), "inf": float("inf"), "np_nan": np.float64("nan"),
           "np_int": np.int64(3), "nested": [{"x": float("-inf")}, (1.0, float("nan"))],
           "ok": 1.5}
if not hasattr(rs, "_json_safe"):
    ok, text = False, "<run_swaps has no _json_safe (base code writes NaN literals)>"
else:
    safe = rs._json_safe(payload)
    text = json.dumps(safe, allow_nan=False)
    ok = ("NaN" not in text and "Infinity" not in text and json.loads(text)["ok"] == 1.5
          and json.loads(text)["float_nan"] is None)
check("R4 strict-JSON sanitiser: no NaN/Infinity literals, undefined floats become null", ok,
      f"dumped={text}")

# ------------------------------------------------------------------ R5: T1a zero-signal identity still holds
zid = rs._compare_zero_signal(0)
check("R5 T1a zero-signal identity: complex block at strength 0 equals simple block off (array for array)",
      _finite(zid["max_abs_diff"]) and zid["max_abs_diff"] < 1e-12,
      f"max_abs_diff={zid['max_abs_diff']!r}")

# ------------------------------------------------------------------ R6: fractional formal share survives model_blocks -> dashboard
raw = simulate(Params(n=20000, seed=0))
o = outcomes(raw)
share = o["formal_share"]
check("R6a end-to-end dashboard formal_share == vacancy rate 0.25",
      _finite(share) and abs(share - 0.25) < 0.01,
      f"formal_share={share!r} (want 0.25)")

# Direct trap: a mass-carrying cell can be 50% formally employed. The dashboard must report the expected share
# 0.5, not re-binarise it to "employed" and report 1.0 (the old ``np.asarray(..., bool)`` cast).
raw_frac = dict(raw)
raw_frac["formal"] = np.full(raw["n"], 0.5, float)
o_frac = outcomes(raw_frac)
check("R6b dashboard keeps fractional formal share (0.5 expected, not re-binarised to 1.0)",
      _finite(o_frac["formal_share"]) and abs(o_frac["formal_share"] - 0.5) < 1e-9,
      f"formal_share={o_frac['formal_share']!r} (want 0.5; the old bool cast gave 1.0)")

n_pass = sum(1 for _, ok, _ in CASES if ok)
print(f"\nSUMMARY: {n_pass}/{len(CASES)} PASS (model dir: {MODEL}; scripts dir: {SCRIPTS})")
raise SystemExit(0 if n_pass == len(CASES) else 1)
