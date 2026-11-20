#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPAIR_V17 -- EXP-18 **PART-REPAIR**: the declaration-consistency repair.

ONE change to the frozen v1.6 generator, and nothing else: the **participation decision**
-- who is school-going, and how the out-of-school mass splits into work/neither -- is taken
from the **frozen v1.3 four-state block**, called unchanged (`sim_v1_3.state_shares`), instead
of from the tier block's second, undeclared outside-option parameterisation.

No new behavioural parameter, no new number, no value moved: the substituted object is a
frozen *function* over already-declared primitives (EXP-16 P1, licence `d7c81309...` /
verdict MIXED, D149). The tier menu (`h_share`, `q_O`, `cost_H_mult`, `cost_O_mult`, `H_h`,
`a_gate`, `risk_pen`, `sigma_tier`, `cell_weight`, `z_q`, `ability_grid`, ranks, clip) and the
frozen `tier_allocate` ranking / capacity split are **held exactly as built**. The O-versus-
outside refusal margin `acc: U_O > u_out` is kept, because that margin is where the menu's
declared quality discount acts (R4a).

Everything here is SYNTHETIC. This module never reads an observed file: the caller passes
paths in, and the driver's phase guard refuses an observed open during the arm phase.
"""
from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path

import numpy as np

LABEL = "SYNTHETIC"
ANCHOR = "SYN00_PHL_LIKE"

# Declared allowlist of frozen-module callables this cell may reach (D147(iii) capability
# lint) -- anything outside it REFUSES the build.
CALL_ALLOWLIST = frozenset({
    "run_arm", "run_arm_full", "build_panel_v13", "write_panel_v13", "shadow_inputs_named",
    "verify_predecl",
    "declared_block", "tier_cells", "tier_allocate", "state_shares", "sha256_file", "P",
    "YEARS", "T" , "YEAR_START", "YEAR_END", "LEVELS", "N_C", "TIER16", "DECLARED_GATES",
    "EXPECTED_V13_PANEL_SHA", "load_observed_phl_paths", "V15_RECON", "KAPPA_V16",
    "KAPPA_LAG_V16", "CHILD_WAGE_MULT", "OUT_YEARS", "NEED", "UTIL_SCALE", "GIRL_SHARE",
    "TASTE", "ABILITY", "AGE_W", "OFF", "DVEC",
})
V13_ALLOWLIST = frozenset({"state_shares", "P", "YEARS"})
REPAIR_ALLOWLIST = frozenset({
    "make_arm_functions", "load_demographic_inputs", "load_observed_cells",
    "ast_scan_files", "ast_called_names", "own_code_rule", "CapabilityLint",
    "CALL_ALLOWLIST", "V13_ALLOWLIST", "REPAIR_ALLOWLIST", "ANCHOR", "LABEL",
    "SUPPLY_COLUMNS", "UPPER_PIPELINE_COLUMNS", "UPPER_NON_REPLAY_COLUMNS",
    "SCORE_COLUMNS", "sha256_file",
    "demographic_series", "DEMOGRAPHIC_INDICATORS",
})

# The two observed indicators that are the frozen instrument's DECLARED Layer-1b demographic
# input (v1.2/v1.3/v1.6 `load_observed_phl_paths`). They are inputs, not outcomes; the
# outcome indicators (`completion_<level>`) are read only in the scoring phase.
DEMOGRAPHIC_INDICATORS = ("cohort_population_0_14", "population_total")

# Declared column sets for the two identity guards (v1.7 replaces v1.6's G2/G3, whose legs
# were true only because the kappa cap was upper-only -- scope sentence in PRE_DECLARATIONS
# sec.7 G3).
SUPPLY_COLUMNS = ("cohort", "band_population", "seats", "seat_coverage", "congestion_q",
                  "quality_q", "class_size", "measurement_factor")
# G2: the columns the frozen `inject_upper` hook DETERMINES from the injected vector. The
# hook sets the upper official admission AFTER the over-age top-up has been computed, so the
# over-age margin and everything downstream of it (enrolment, ger, teachers, ptr) is
# "not replay-determined": it is REPORTED (UPPER_NON_REPLAY_COLUMNS), never asserted.
UPPER_PIPELINE_COLUMNS = ("admitted_official", "survival", "completion_cohort",
                          "completion_uis", "graduates", "cohort", "seats", "congestion_q",
                          "quality_q", "class_size", "measurement_factor")
UPPER_NON_REPLAY_COLUMNS = ("admitted_overage", "enrolment", "ger", "teachers", "ptr")
SCORE_COLUMNS = ("completion_uis", "completion_cohort", "demand_official", "demand_share",
                 "admitted_official", "cohort", "survival", "seats")


class CapabilityLint(RuntimeError):
    """A named object cannot exist in the named arm (D147(iii))."""


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ======================================================================================
# 1. Phase A: the frozen instrument's declared Layer-1b demographic input
# ======================================================================================
def demographic_series(rows, indicator):
    d = {}
    for r in rows:
        if r.get("iso3") != "PHL" or r.get("indicator") != indicator:
            continue
        try:
            d[int(float(r["year"]))] = float(r["value"])
        except (ValueError, TypeError):
            continue
    return d


def load_demographic_inputs(path, years, t_size):
    """Read ONLY the two declared demographic indicators and build (S, Pop).

    This is the frozen v1.3/v1.6 construction, unchanged: observed cohort/population where
    present, the declared backward/forward extrapolation otherwise. Rows carrying any other
    indicator -- including every `completion_*` outcome -- are skipped on arrival: they are
    not stored, not converted into a float, and not compared.
    """
    import csv

    kept = []
    dropped = 0
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("iso3") != "PHL" or r.get("indicator") not in DEMOGRAPHIC_INDICATORS:
                dropped += 1
                continue
            kept.append(r)
    coh = demographic_series(kept, "cohort_population_0_14")
    pop = demographic_series(kept, "population_total")
    if not coh or not pop:
        raise CapabilityLint("phase A: declared demographic indicators absent from the series")
    if min(coh) > 1995 or max(coh) < 2024:
        raise CapabilityLint("phase A: demographic cohort series coverage is not the declared one")
    S = np.empty(t_size)
    for i, y in enumerate(years):
        if y in coh:
            S[i] = coh[y]
        elif y < min(coh):
            S[i] = coh[min(coh)] / (1.0245 ** (min(coh) - y))
        else:
            S[i] = coh[max(coh)] * (1.0 - 0.008) ** (y - max(coh))
    Pp = np.empty(t_size)
    for i, y in enumerate(years):
        if y in pop:
            Pp[i] = pop[y]
        elif y < min(pop):
            Pp[i] = pop[min(pop)] / (1.025 ** (min(pop) - y))
        else:
            Pp[i] = pop[max(pop)] * (1.0 + 0.010) ** (y - max(pop))
    meta = {
        "path": path,
        "indicators_retained": list(DEMOGRAPHIC_INDICATORS),
        "rows_retained": len(kept),
        "rows_skipped_on_arrival": dropped,
        "cohort_years": [min(coh), max(coh)],
        "population_years": [min(pop), max(pop)],
        "construction": ("S = cohort_population_0_14 with the declared backward (1.0245) / "
                         "forward (0.992) extrapolation; Pop = population_total with the "
                         "declared backward (1.025) / forward (1.010) extrapolation"),
        "observed_outcomes_retained": 0,
    }
    return S, Pp, meta


# ======================================================================================
# 2. Phase C: the scoring object (33 cells), read only after every arm has finished
# ======================================================================================
def load_observed_cells(path, levels, y0, y1, expected_per_level=11):
    """The 33 observed completion cells: `completion_<level>`, iso3 PHL, inside the window."""
    import csv

    obs = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("iso3") != "PHL":
                continue
            ind = r.get("indicator", "")
            if not ind.startswith("completion_"):
                continue
            lv = ind[len("completion_"):]
            if lv not in levels:
                continue
            try:
                y = int(float(r["year"]))
                v = float(r["value"])
            except (TypeError, ValueError):
                continue
            if y0 <= y <= y1:
                obs[(lv, y)] = v
    for lv in levels:
        n = sum(1 for (a, _y) in obs if a == lv)
        if n != expected_per_level:
            raise CapabilityLint("phase C: observed cell count for %s is %d, expected %d"
                                 % (lv, n, expected_per_level))
    if len(obs) != expected_per_level * len(levels):
        raise CapabilityLint("phase C: %d observed cells, expected %d"
                             % (len(obs), expected_per_level * len(levels)))
    return obs


# ======================================================================================
# 3. The repair: one substitution, at the participation decision only
# ======================================================================================
def make_arm_functions(S, V13):
    """Return {arm: (tier_cells_fn, tier_allocate_fn)} bound to the frozen modules.

    A00 : frozen `tier_cells` + frozen `tier_allocate`, bimodal OFF (the no-tier comparator;
          the tier code is never reached, and the panel must be byte-identical to the frozen
          v1.3 panel -- guard G1).
    A17 : `cells_a17` (participation mass and composition from the frozen v1.3 four-state
          block; H/O split and refusal margin from the frozen tier block, unchanged) +
          frozen `tier_allocate` via `alloc_compose` (a reporting-only pass-through).
    """
    frozen_cells = S.tier_cells
    frozen_alloc = S.tier_allocate
    state_shares = V13.state_shares

    # ---- capability lint (D147(iii)): each named object must exist in the named arm -------
    if not callable(frozen_cells) or not callable(frozen_alloc):
        raise CapabilityLint("A00/A17: frozen tier_cells/tier_allocate not callable")
    if not callable(state_shares):
        raise CapabilityLint("A17: sim_v1_3.state_shares not callable")
    need = ("cost_H_mult", "cost_O_mult", "q_O", "H_h", "a_gate", "risk_pen", "sigma_tier",
            "z_q", "cell_weight", "ability_grid", "rank_w_income", "rank_w_ability",
            "padv_clip", "h_share")
    missing = [k for k in need if k not in S.TIER16]
    if missing:
        raise CapabilityLint("A17: declared tier-menu object(s) missing: %r" % (missing,))

    def _pr13(cp, level, y_shock):
        """The frozen v1.3 four-state block, called unchanged. Returns its 4 probabilities."""
        if level >= 3:
            raise CapabilityLint("A17: the four-state participation block governs L<3 only")
        Pr = np.asarray(state_shares(cp, level, y_shock), dtype=float)
        if Pr.shape != (4,):
            raise CapabilityLint("A17: state_shares returned a non-4-vector")
        tot = float(Pr.sum())
        if not math.isfinite(tot) or abs(tot - 1.0) > 1e-9:
            raise CapabilityLint("A17: state_shares probabilities do not sum to 1: %r" % (tot,))
        if float(Pr.min()) < -1e-15:
            raise CapabilityLint("A17: state_shares returned a negative probability")
        return Pr

    def cells_a17(cp, level, y_shock, tc, padv_hat, G_H):
        """School-going mass = the frozen block's own ds13; H/O split = the tier block's own
        declared payoff comparison (frozen U_H/U_O formulas, frozen menu values)."""
        base = frozen_cells(cp, level, y_shock, tc, padv_hat, G_H)
        Pr = _pr13(cp, level, y_shock)
        ds13 = float(Pr[0] + Pr[1])
        if not (0.0 <= ds13 <= 1.0 + 1e-12):
            raise CapabilityLint("A17: ds13 outside [0,1]: %r" % (ds13,))
        cells = dict(base)
        cells["w"] = np.asarray(base["w"], dtype=float) * ds13       # the block's own mass
        # tie -> O, the frozen convention (`uh > u0` -> H else O)
        cells["first"] = np.where(np.asarray(base["U_H"]) > np.asarray(base["U_O"]),
                                  0, 1).astype(int)
        cells["_pw"] = float(Pr[2])          # the block's own out-of-school composition
        cells["_pn"] = float(Pr[3])
        cells["_ds13"] = ds13
        cells["_arm"] = "A17"
        return cells

    def alloc_compose(cells, elig, C_L, K_H, K_O, tc):
        """Frozen `tier_allocate`, plus a REPORTING-ONLY pass-through of the v1.3 block's own
        out-of-school composition (Pr_work, Pr_neither). Demand, admission, capacity, the
        refusal margin and every verdict object are the frozen ones."""
        al = frozen_alloc(cells, elig, C_L, K_H, K_O, tc)
        if "_pw" in cells:
            out = dict(al)
            out["mW"] = float(cells["_pw"])
            out["mB"] = 0.0
            out["mN"] = float(cells["_pn"])
            return out
        return al

    return {"A00": (frozen_cells, frozen_alloc),
            "A17": (cells_a17, alloc_compose)}


# ======================================================================================
# 4. Static (AST) scans: count-blind reachability and the cell's own-code rule
# ======================================================================================
def ast_scan_files(paths, forbidden_literal):
    """Static scan of the cell's own and imported sources. Returns a JSON-able report."""
    report = []
    for p in paths:
        txt = Path(p).read_text()
        tree = ast.parse(txt, filename=str(p))
        scope = {}
        for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
            for node in ast.walk(fn):
                scope.setdefault(id(node), fn.name)
        literals, opens, drefs = [], [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if forbidden_literal.lower() in node.value.lower():
                    literals.append({"lineno": node.lineno, "text": node.value[:120],
                                     "enclosing_function": scope.get(id(node), "<module>")})
            if isinstance(node, ast.Call):
                fn = node.func
                name = (fn.id if isinstance(fn, ast.Name)
                        else (fn.attr if isinstance(fn, ast.Attribute) else ""))
                if name in ("open", "read_csv", "loadtxt", "genfromtxt", "load",
                            "read_text", "read_bytes"):
                    arg, argname = "", ""
                    if node.args:
                        a0 = node.args[0]
                        if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                            arg = a0.value
                        elif isinstance(a0, ast.Name):
                            argname = a0.id
                        else:
                            arg = "<expr>"
                    opens.append({"lineno": node.lineno, "call": name, "first_arg": arg,
                                  "first_arg_name": argname,
                                  "enclosing_function": scope.get(id(node), "<module>")})
            if isinstance(node, ast.Attribute) and node.attr == "DATA":
                drefs.append({"lineno": node.lineno})
        report.append({
            "file": Path(p).name,
            "sha256": sha256_file(p),
            "n_lines": len(txt.splitlines()),
            "forbidden_literal_hits": literals,
            "open_calls": opens,
            "data_path_refs": drefs,
        })
    return report


def ast_called_names(paths, module_aliases):
    """Every `alias.name(...)` CALL on the frozen modules, for the reachability lint."""
    called = {}
    for p in paths:
        tree = ast.parse(Path(p).read_text(), filename=str(p))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                    and isinstance(node.func.value, ast.Name):
                if node.func.value.id in module_aliases:
                    called.setdefault(node.func.value.id, set()).add(node.func.attr)
    return {k: sorted(v) for k, v in called.items()}


def own_code_rule(paths, forbidden_literal, guard_open_function, phase_functions):
    """The cell's OWN code rule.

    (a) The forbidden basename may appear ONLY as one module-level constant.
    (b) The only `open()` whose first argument is that guard name is the phase-guard
        self-test, inside `guard_open_function`.
    (c) Each declared phase function contains exactly one `open()` call on its `path`
        argument -- the two and only two observed-data sites, called in the declared phases.
    No open on a literal forbidden path anywhere.
    """
    guard_names, violations, guard_opens = set(), [], []
    phase_open_counts = {fn: 0 for fn in phase_functions}
    derived_path_ok = False
    for p in paths:
        tree = ast.parse(Path(p).read_text(), filename=str(p))
        scope = {}
        for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
            for node in ast.walk(fn):
                scope.setdefault(id(node), fn.name)
        for node in tree.body:                     # module level only
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        for sub in ast.walk(node.value):
                            if (isinstance(sub, ast.Constant) and isinstance(sub.value, str)
                                    and forbidden_literal.lower() in sub.value.lower()):
                                guard_names.add(tgt.id)
                        # the ONLY other name allowed to reach the observed file must be a
                        # path constant *derived* from the guard constant
                        if tgt.id == "OBSERVED_PATH" and any(
                                isinstance(x, ast.Name) and x.id in guard_names
                                for x in ast.walk(node.value)):
                            derived_path_ok = True
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and node.args):
                continue
            fn = node.func
            name = (fn.id if isinstance(fn, ast.Name)
                    else (fn.attr if isinstance(fn, ast.Attribute) else ""))
            if name not in ("open", "read_csv", "loadtxt", "genfromtxt", "load",
                            "read_text", "read_bytes"):
                continue
            a0 = node.args[0]
            enclosing = scope.get(id(node), "<module>")
            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                if forbidden_literal.lower() in a0.value.lower():
                    violations.append({"file": Path(p).name, "lineno": node.lineno,
                                       "reason": "open on a literal forbidden path"})
            elif isinstance(a0, ast.Name) and (a0.id in guard_names
                                               or a0.id == "OBSERVED_PATH"):
                guard_opens.append({"file": Path(p).name, "lineno": node.lineno,
                                    "enclosing_function": enclosing})
            if enclosing in phase_open_counts and isinstance(a0, ast.Name) \
                    and a0.id == "path":
                phase_open_counts[enclosing] += 1
    sites = sorted({o["enclosing_function"] for o in guard_opens})
    ok = (sorted(guard_names) == ["OBSERVED_BASENAME"] and derived_path_ok
          and not violations
          and sites == [guard_open_function]
          and all(v == 1 for v in phase_open_counts.values()))
    return {"guard_names": sorted(guard_names),
            "open_calls_on_guard_name": len(guard_opens),
            "open_sites": sites,
            "declared_guard_open_site": guard_open_function,
            "observed_path_derived_from_guard_constant": derived_path_ok,
            "phase_function_open_counts": phase_open_counts,
            "violations": violations,
            "rule": ("the forbidden basename appears only as the module-level constant "
                     "OBSERVED_BASENAME; its only direct open() is the phase-guard "
                     "self-test; each of the two declared phase functions opens its `path` "
                     "argument exactly once"),
            "verdict": "PASS" if ok else "FAIL"}
