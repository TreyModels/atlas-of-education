#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARMS -- EXP-16 PARTPROV (count-blind provenance diagnostic).

Every object here is SYNTHETIC. This module holds the three diagnostic arms of
PRE_DECLARATIONS.md sec.3, implemented as *replacements of one module-level function
lookup* in the byte-identical frozen v1.6 module (code/frozen/sim_v1_6_repair.py).
The frozen file is never edited; the frozen v1.3 block (code/frozen/sim_v1_3.py) is
called, never re-implemented.

Count-blind: this module opens no file except the frozen v1.3 SYNTHETIC panel, and it
contains no reference to any observed series and no 33-cell construct.
"""
from __future__ import annotations

import csv
import math

import numpy as np

ANCHOR = "SYN00_PHL_LIKE"
PRIMARY = "primary"

# Declared allowlist of frozen-module callables this cell may reach (D147(iii) capability
# lint + D147(iv) count-blind reachability guard). Anything outside it REFUSES the build.
CALL_ALLOWLIST = frozenset({
    "run_arm_full", "run_arm", "simulate_country", "verify_predecl", "declared_block",
    "outside_utilities16", "tier_cells", "tier_allocate", "apply_declared", "draw_countries",
    "cohort_path", "pop_path", "resolve_hosts", "shadow_inputs_named",
})
V13_ALLOWLIST = frozenset({"state_shares"})
ARMS_ALLOWLIST = frozenset({"declared_demographic_path", "make_arms", "ast_scan_files",
                            "ast_called_names", "own_code_rule", "CapabilityLint", "CALL_ALLOWLIST",
                            "V13_ALLOWLIST", "ARMS_ALLOWLIST", "OUTSIDE_REMOVED",
                            "ANCHOR", "PRIMARY"})

# Sentinel used by P2 to remove the outside option by construction (nesting). It is NOT a
# behavioural value: the frozen refusal test `U_O > u_out` becomes vacuously true.
OUTSIDE_REMOVED = -1.0e300


class CapabilityLint(RuntimeError):
    """A named object cannot exist in the named arm (D147(iii))."""


# ======================================================================================
# 1. The declared demographic input, reconstructed WITHOUT any observed read
# ======================================================================================
def declared_demographic_path(v13_panel, years, band_share_primary, anchor=ANCHOR):
    """Frozen block's own declared demographic path, from the frozen SYNTHETIC v1.3 panel.

    S_path[t]  = band_population(primary, t) / band_share[primary]   (C = band*S/DVEC)
    Pop_path[t]= population(t)

    Reads ONE file: the frozen v1.3 synthetic panel (sha256 47d4b082...). No observed file
    is opened anywhere in this cell (PRE_DECLARATIONS.md sec.6).
    """
    band, pop = {}, {}
    with open(v13_panel, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != anchor:
                continue
            y = int(float(r["year"]))
            pop[y] = float(r["population"])
            if r["level"] == PRIMARY:
                band[y] = float(r["band_population"])
    S = np.array([band[int(y)] / float(band_share_primary) for y in years], dtype=float)
    Pp = np.array([pop[int(y)] for y in years], dtype=float)
    if not np.all(np.isfinite(S)) or not np.all(S > 0.0):
        raise CapabilityLint("demographic reconstruction produced non-finite S_path")
    if not np.all(np.isfinite(Pp)) or not np.all(Pp > 0.0):
        raise CapabilityLint("demographic reconstruction produced non-finite Pop_path")
    return S, Pp, len(band)


# ======================================================================================
# 2. The three arms
# ======================================================================================
def make_arms(S, V13):
    """Return dict arm -> (tier_cells, tier_allocate) callables bound to the frozen modules.

    P0 : frozen tier_cells, frozen tier_allocate (the built arm).
    P1 : tier_cells_p1 (participation primitives = frozen v1.3 four-state logit; refusal
         margin kept exactly as built), tier_allocate_compose (frozen + reporting-only
         composition pass-through).
    P2 : tier_cells_p2 (same mass as P1; outside option REMOVED by construction = nesting),
         tier_allocate_compose (same reporting-only pass-through).
    """
    frozen_cells = S.tier_cells
    frozen_alloc = S.tier_allocate
    state_shares = V13.state_shares

    # ---- capability lint (D147(iii)): each named object must exist in the named arm -----
    if not callable(frozen_cells) or not callable(frozen_alloc):
        raise CapabilityLint("P0: frozen tier_cells/tier_allocate not callable")
    if not callable(state_shares):
        raise CapabilityLint("P1/P2: sim_v1_3.state_shares not callable")

    def _pr13(cp, level, y_shock):
        """The frozen v1.3 four-state block, called unchanged. Returns its 4 probabilities."""
        if level >= 3:
            raise CapabilityLint("P1/P2: the four-state participation block governs L<3 only")
        Pr = np.asarray(state_shares(cp, level, y_shock), dtype=float)
        if Pr.shape != (4,):
            raise CapabilityLint("P1/P2: state_shares returned a non-4-vector")
        tot = float(Pr.sum())
        if not math.isfinite(tot) or abs(tot - 1.0) > 1e-9:
            raise CapabilityLint("P1/P2: state_shares probabilities do not sum to 1: %r" % (tot,))
        if float(Pr.min()) < -1e-15:
            raise CapabilityLint("P1/P2: state_shares returned a negative probability")
        return Pr

    def _participation_cells(cp, level, y_shock, tc, padv_hat, G_H):
        """School-going mass = the frozen block's own ds13; H/O split = the tier block's own
        declared payoff comparison (U_H vs U_O, frozen formulas and frozen menu values)."""
        base = frozen_cells(cp, level, y_shock, tc, padv_hat, G_H)
        Pr = _pr13(cp, level, y_shock)
        ds13 = float(Pr[0] + Pr[1])
        if not (0.0 <= ds13 <= 1.0 + 1e-12):
            raise CapabilityLint("P1/P2: ds13 outside [0,1]: %r" % (ds13,))
        cells = dict(base)
        cells["w"] = np.asarray(base["w"], dtype=float) * ds13        # nested mass
        cells["first"] = np.where(np.asarray(base["U_H"]) > np.asarray(base["U_O"]), 0, 1).astype(int)
        cells["_pw"] = float(Pr[2])          # reporting-only composition (the block's own)
        cells["_pn"] = float(Pr[3])
        cells["_ds13"] = ds13
        return cells

    def cells_p1(cp, level, y_shock, tc, padv_hat, G_H):
        cells = _participation_cells(cp, level, y_shock, tc, padv_hat, G_H)
        cells["_arm"] = "P1"
        return cells                                    # u_out untouched -> refusal margin kept

    def cells_p2(cp, level, y_shock, tc, padv_hat, G_H):
        cells = _participation_cells(cp, level, y_shock, tc, padv_hat, G_H)
        cells["u_out"] = np.full_like(np.asarray(cells["u_out"], dtype=float), OUTSIDE_REMOVED)
        cells["_arm"] = "P2"
        return cells                                    # nesting: no cell can exit

    def alloc_compose(cells, elig, C_L, K_H, K_O, tc):
        """Frozen tier_allocate, plus a REPORTING-ONLY pass-through of the v1.3 block's own
        out-of-school composition (Pr_work, Pr_neither). Demand, admission, capacity, the
        refusal margin and every verdict object are untouched."""
        al = frozen_alloc(cells, elig, C_L, K_H, K_O, tc)
        if "_pw" in cells:
            out = dict(al)
            out["mW"] = float(cells["_pw"])
            out["mB"] = 0.0
            out["mN"] = float(cells["_pn"])
            return out
        return al

    return {
        "P0": (frozen_cells, frozen_alloc),
        "P1": (cells_p1, alloc_compose),
        "P2": (cells_p2, alloc_compose),
    }


# ======================================================================================
# 3. Count-blind static scan (AST) -- run by the driver BEFORE any arm
# ======================================================================================
def ast_scan_files(paths, forbidden_literal):
    """Static scan of the cell's own and imported sources. Returns a JSON-able report."""
    import ast

    report = []
    for p in paths:
        txt = p.read_text()
        tree = ast.parse(txt, filename=str(p))
        scope = {}
        for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
            for node in ast.walk(fn):
                scope.setdefault(id(node), fn.name)
        literals, opens, drefs, counts = [], [], [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if forbidden_literal.lower() in node.value.lower():
                    literals.append({"lineno": node.lineno, "text": node.value[:120],
                                     "enclosing_function": scope.get(id(node), "<module>")})
                if "33" in node.value:
                    counts.append({"lineno": node.lineno, "kind": "string-33", "text": node.value[:80]})
            if isinstance(node, ast.Call):
                fn = node.func
                name = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
                if name in ("open", "read_csv", "loadtxt", "genfromtxt", "load", "read_text", "read_bytes"):
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
            if isinstance(node, ast.Name) and node.id == "DATA":
                drefs.append({"lineno": node.lineno})
        report.append({
            "file": p.name,
            "sha256": _sha(p),
            "n_lines": len(txt.splitlines()),
            "forbidden_literal_hits": literals,
            "open_calls": opens,
            "data_path_refs": drefs,
            "count_like_literals": counts,
        })
    return report


def own_code_rule(paths, forbidden_literal):
    """The cell's OWN code rule: the forbidden basename may appear ONLY as the guard
    constant (a module-level name), and the only open() on that name must be the guard
    self-test. Any open() on a literal forbidden path is a violation -> REFUSE."""
    import ast

    guard_names, violations, self_test_opens, on_guard = set(), [], 0, 0
    for p in paths:
        tree = ast.parse(p.read_text(), filename=str(p))
        for node in tree.body:                     # module level only
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        for sub in ast.walk(node.value):
                            if (isinstance(sub, ast.Constant) and isinstance(sub.value, str)
                                    and forbidden_literal.lower() in sub.value.lower()):
                                guard_names.add(tgt.id)
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and node.args):
                continue
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
            if name not in ("open", "read_csv", "loadtxt", "genfromtxt", "load",
                            "read_text", "read_bytes"):
                continue
            a0 = node.args[0]
            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                if forbidden_literal.lower() in a0.value.lower():
                    violations.append({"file": p.name, "lineno": node.lineno,
                                       "reason": "open on a literal forbidden path"})
            elif isinstance(a0, ast.Name) and a0.id in guard_names:
                on_guard += 1
                if node.lineno:
                    self_test_opens += 1
    return {"guard_names": sorted(guard_names), "open_calls_on_guard_name": on_guard,
            "violations": violations,
            "rule": "the forbidden basename may appear only as the module-level guard "
                    "constant OBSERVED, with exactly ONE open site (the guard self-test)",
            "verdict": "PASS" if (sorted(guard_names) == ["OBSERVED"] and not violations
                                  and on_guard == 1) else "FAIL"}


def ast_called_names(paths, module_aliases):
    """Every `alias.name(...)` CALL on the frozen modules, for the reachability lint.

    Attribute *reads* and *assignments* (path constants, P, YEARS, the loader shadow) are not
    calls and cannot compute anything; only calls are linted.
    """
    import ast

    called = {}
    for p in paths:
        tree = ast.parse(p.read_text(), filename=str(p))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                    and isinstance(node.func.value, ast.Name):
                if node.func.value.id in module_aliases:
                    called.setdefault(node.func.value.id, set()).add(node.func.attr)
    return {k: sorted(v) for k, v in called.items()}


def _sha(p):
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()
