#!/usr/bin/env python3
"""Feasibility audit: can a 'credential requirement at gate places' bind in coevolve v0?

Read-only import of the frozen model; no modification. Counts, at every gate and year, applicants and
applicants lacking the prerequisite credential. If the latter is 0 everywhere, the requested primary wiring is
INERT-BY-CONSTRUCTION (see ../PRE_DECLARATIONS.md section 2).
"""
import importlib.util, json, os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
V0DIR = os.path.dirname(os.path.dirname(HERE))  # coevolve_2026-11-21
MODEL = os.path.join(V0DIR, "code", "coevolve_v0.py")
OUT = os.path.join(os.path.dirname(HERE), "results")
LABEL = "SIMULATED"

def load_v0():
    spec = importlib.util.spec_from_file_location("coevolve_v0", MODEL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["coevolve_v0"] = mod
    spec.loader.exec_module(mod)
    return mod

# prerequisite credential for entering a level (completed previous level)
REQ_CRED = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3}

def main():
    m = load_v0()
    P = m.params_as_lists()
    counts = {"seeds": [], "selective_gate": {"applicants": 0, "lacking_credential": 0},
              "university_gate": {"applicants": 0, "lacking_credential": 0},
              "allocation": {"candidates": 0, "lacking_credential": 0},
              "per_level": {}}
    for seed in [20261121, 20261122]:
        sim = m.Sim("baseline", int(seed), P)
        # wrap gates/allocation with counters
        orig_sel = sim._selective_gate
        def sel_wrap(t, seeking_upper, _orig=orig_sel, _sim=sim):
            idx = sim.stats.get("sel_idx", None)
            _orig(t, seeking_upper)
        # simpler: run step loop manually and inspect before calls via monkeypatch of methods
        def _sel(t, seeking_upper):
            idx = int(seeking_upper.sum()) if hasattr(seeking_upper, 'sum') else 0
            counts["selective_gate"]["applicants"] += idx
            if idx:
                lack = int((sim.cred[seeking_upper] < REQ_CRED[2]).sum())
                counts["selective_gate"]["lacking_credential"] += lack
            return orig_sel(t, seeking_upper)
        def _uni(t, seeking):
            idx = int(seeking.sum()) if hasattr(seeking, 'sum') else 0
            counts["university_gate"]["applicants"] += idx
            if idx:
                lack = int((sim.cred[seeking] < REQ_CRED[4]).sum())
                counts["university_gate"]["lacking_credential"] += lack
            return orig_uni(t, seeking)
        orig_uni = sim._university_gate
        sim._selective_gate = types.MethodType(lambda self, t, s: _sel(t, s), sim)
        sim._university_gate = types.MethodType(lambda self, t, s: _uni(t, s), sim)
        orig_alloc = sim._allocate
        def _alloc(is_new, want, free, t):
            for lvl in m.LEVELS:
                cand = is_new & (want == lvl)
                n = int(cand.sum())
                if n:
                    counts["allocation"]["candidates"] += n
                    lack = int((sim.cred[cand] < REQ_CRED[lvl]).sum())
                    counts["allocation"]["lacking_credential"] += lack
                    pl = counts["per_level"].setdefault(str(lvl), {"candidates": 0, "lacking_credential": 0})
                    pl["candidates"] += n; pl["lacking_credential"] += lack
            return orig_alloc(is_new, want, free, t)
        sim._allocate = types.MethodType(lambda self, a, b, c, d: _alloc(a, b, c, d), sim)
        for t in range(sim.T0, sim.T1 + 1):
            sim.step(t)
        counts["seeds"].append(int(seed))
    counts["label"] = LABEL
    counts["model"] = MODEL
    counts["inert_by_construction"] = (counts["selective_gate"]["lacking_credential"] == 0
                                       and counts["university_gate"]["lacking_credential"] == 0
                                       and counts["allocation"]["lacking_credential"] == 0)
    counts["verdict"] = ("INERT-BY-CONSTRUCTION" if counts["inert_by_construction"]
                         else "IMPLEMENTABLE")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "CREDENTIAL_GATE_AUDIT.json"), "w") as fh:
        json.dump(counts, fh, indent=2, sort_keys=True); fh.write("\n")
    print(json.dumps(counts, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
