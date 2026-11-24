#!/usr/bin/env python3
"""Self-contained regression tests for the v6 gate fix + Tullock invariance audit (numpy only, no pytest).

Target: ``research/masseng-v6/masseng_v6/education/gate.py``. The quota branch used to count the below-bar mass
again inside capacity_rejection (Neon quarantine item "quota double-count"); the Tullock probes below record what
invariance the implemented contest form does and does not have (audit evidence, not a claim change).
Run:  python3 test_gate_fixes.py [--model-dir DIR]   (SIMULATION; no empirical or causal claim)
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
from masseng_v6.education.gate import Gate, apply_gate  # noqa: E402

CASES = []


def check(name, ok, detail):
    CASES.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)


# ------------------------------------------------------------------ G1: quota rejection channels do not double-count
n_q = 100
mass_q = np.full(n_q, 10.0)
scores_q = np.linspace(-2.0, 2.0, n_q)
group_q = np.tile(np.arange(10), 10)
out = apply_gate(Gate(kind="quota", capacity=300.0, threshold=0.0, quota_share=0.3,
                      quota_threshold=-0.5, quota_group_max=2), scores_q, mass_q,
                 np.ones(n_q, bool), group_q)
a = out.accounting
channels = a["below_bar"] + a["capacity_rejection"] + a["exam_fail"]
ok = (abs(channels - a["rejected_eligible"]) < 1e-9
      and abs(a["admitted"] + a["rejected_eligible"] - a["eligible"]) < 1e-9)
check("G1 quota accounting: below_bar+capacity_rejection+exam_fail == rejected_eligible (no double-count)", ok,
      f"channels={channels!r}, rejected={a['rejected_eligible']!r}, below_bar={a['below_bar']!r}, "
      f"capacity_rejection={a['capacity_rejection']!r} (the old branch gave 1170 vs 700)")

# ------------------------------------------------------------------ G2: every gate kind conserves rejection channels
violations = []
rng = np.random.default_rng(11)
for kind in ("capacity", "bar", "quota", "exam", "tullock"):
    for _ in range(20):
        n = 60
        mass = rng.uniform(0.5, 5.0, n)
        scores = rng.normal(0.0, 1.0, n)
        group = rng.integers(0, 10, n)
        g = Gate(kind=kind, capacity=float(rng.uniform(5, 100)), threshold=float(rng.uniform(-1.5, 1.5)),
                 quota_share=0.3, quota_threshold=-0.5, quota_group_max=2, pass_rate=float(rng.uniform(0.5, 1.0)))
        o = apply_gate(g, scores, mass, np.ones(n, bool), group, rng=np.random.default_rng(5))
        ch = o.accounting["below_bar"] + o.accounting["capacity_rejection"] + o.accounting["exam_fail"]
        if abs(ch - o.accounting["rejected_eligible"]) > 1e-9:
            violations.append((kind, ch, o.accounting["rejected_eligible"]))
check("G2 all gate kinds: rejection channels reconcile to rejected_eligible", not violations,
      f"violations={violations[:3]}")

# ------------------------------------------------------------------ G3-G4: Tullock invariance audit (declared evidence)
n = 40
mass = rng.uniform(1.0, 5.0, n)
scores = rng.normal(0.0, 1.0, n)
group = np.zeros(n, int)
elig = np.ones(n, bool)
g = Gate(kind="tullock", capacity=0.3 * mass.sum(), threshold=0.0, tullock_scale=0.5)
base = apply_gate(g, scores, mass, elig, group).admitted_mass
scale = 7.3
scaled = apply_gate(Gate(kind="tullock", capacity=g.capacity * scale, threshold=0.0, tullock_scale=0.5),
                    scores, mass * scale, elig, group).admitted_mass
rel = float(np.max(np.abs(scaled / scale - base)) / max(base.max(), 1e-12))
split = apply_gate(Gate(kind="tullock", capacity=g.capacity, threshold=0.0, tullock_scale=0.5),
                   np.repeat(scores, 2), np.repeat(mass / 2, 2), np.repeat(elig, 2), np.repeat(group, 2)
                   ).admitted_mass
split_err = abs(float(split.sum() - base.sum()))
check("G3 Tullock is invariant to (mass, capacity) scaling and to cell splitting",
      rel < 1e-12 and split_err < 1e-9, f"scale max rel diff={rel:.2e}, split sum diff={split_err:.2e}")

translated = apply_gate(Gate(kind="tullock", capacity=g.capacity, threshold=0.0, tullock_scale=0.5),
                        scores + 1.0, mass, elig, group).admitted_mass
trans_diff = float(np.max(np.abs(translated - base)))
check("G4 Tullock is NOT invariant to a common score translation with a fixed absolute threshold "
      "(declared sigmoid form; property absent -- reported OPEN, claim text unchanged)",
      trans_diff > 1e-6, f"max cell diff after score+1: {trans_diff:.4f}")

n_pass = sum(1 for _, ok, _ in CASES if ok)
print(f"\nSUMMARY: {n_pass}/{len(CASES)} PASS (model dir: {MODEL})")
raise SystemExit(0 if n_pass == len(CASES) else 1)
