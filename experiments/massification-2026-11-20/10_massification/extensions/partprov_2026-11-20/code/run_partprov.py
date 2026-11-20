#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUN_PARTPROV -- EXP-16 PARTPROV: the count-blind provenance diagnostic.

Three diagnostic arms (P0 as built, P1 with the frozen v1.3 block's declared outside-option
primitives substituted unchanged, P2 nested inside the frozen block's school-going mass,
reported never adopted) on the byte-identical frozen v1.6 code.

Everything emitted is SYNTHETIC. No observed file is opened, no observed value is compared,
no 33-cell count is computed or reported. The count-blind guard refuses the run if the
observed series is opened (exit 42, VOID CONTAMINATED-BY-DESIGN).

Run:  python code/run_partprov.py [--out DIR] [--no-determinism]
"""
from __future__ import annotations

import argparse
import builtins
import csv
import hashlib
import io
import json
import os
import pathlib
import sys
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parent
CELL = CODE.parent
EXT = CELL.parent
MASS = EXT.parent
PROG = MASS.parent
SYNTH = EXT / "synthetic_2026-11-20"
V16_DIR = SYNTH / "generator_v1_6_repair"
V13_DIR = SYNTH / "generator_v1_3"
FROZEN = CODE / "frozen"

PREDECL = CELL / "PRE_DECLARATIONS.md"
PREDECL_SHA = "d7c81309e8f21ab5e338fafe10adf34691445876ec99b98f3458a2ad7ade49cf"
# ^ embedded at freeze time (2026-11-21), before any arm of this cell was run.

V16_SIM = V16_DIR / "code" / "sim_v1_6_repair.py"
V13_SIM = V13_DIR / "code" / "sim_v1_3.py"
V13_PANEL = V13_DIR / "results" / "synthetic_panel_v1_3.csv"
A10_PANEL = V16_DIR / "results" / "panel_A10_repaired.csv"
V16_PREDECL = V16_DIR / "PRE_DECLARATIONS.md"
OBSERVED = MASS / "data" / "UNIVERSALIZATION_SERIES.csv"

ANCHOR = "SYN00_PHL_LIKE"
YEARS = list(range(2010, 2025))
LEVELS = ("primary", "lower_secondary", "upper_secondary")
ENGINE = dict(bimodal=True, kappa_link=False, tier_surv=False, tier_cfg=None,
              inject_upper=None, w_child_mult=1.0, phys_cap=1.15)
ARMS = ("P0", "P1", "P2")

TOL_DUP_PP = 1.0
MIN_YEARS_WITHIN = 15
TOL_STRUCT_PP = 0.5
MIN_YEARS_MOVED = 15
S_IDENT_TOL_REL = 1e-8
VOID_EXIT = 42

LABEL = "SYNTHETIC"


# ======================================================================================
# count-blind runtime guard
# ======================================================================================
class ObservedFileAccess(RuntimeError):
    pass


class AuditGuard:
    """Wraps every file-open entry point for the whole scored path.

    An attempt to open the forbidden basename raises BEFORE the OS call: nothing is read.
    Every attempt is logged with a normalised path so two runs are byte-identical.
    """

    def __init__(self, forbidden_basename, outdir, prog, log):
        self.forbidden = forbidden_basename.lower()
        self.outdir = os.path.abspath(str(outdir))
        self.prog = os.path.abspath(str(prog))
        self.log = log
        self.blocked = 0
        self._saved = None

    def norm(self, p):
        try:
            ap = os.path.abspath(str(p))
        except Exception:
            return str(p)
        if ap.startswith(self.outdir + os.sep) or ap == self.outdir:
            return "<OUT>/" + os.path.relpath(ap, self.outdir)
        if ap.startswith(self.prog + os.sep):
            return "<PROG>/" + os.path.relpath(ap, self.prog)
        return ap

    def _check(self, p, op):
        base = os.path.basename(str(p)).lower()
        if base == self.forbidden:
            self.blocked += 1
            self.log.append({"path": self.norm(p), "op": op, "allowed": False})
            raise ObservedFileAccess("GUARD: refused to open the observed series (%s)" % (self.norm(p),))
        self.log.append({"path": self.norm(p), "op": op, "allowed": True})
        return p

    def __enter__(self):
        self._bopen, self._iopen, self._osopen = builtins.open, io.open, os.open
        guard = self

        def bopen(file, *a, **kw):
            guard._check(file, "open:" + str(a[0] if a else kw.get("mode", "r")))
            return guard._bopen(file, *a, **kw)

        def iopen(file, *a, **kw):
            guard._check(file, "io.open:" + str(a[0] if a else kw.get("mode", "r")))
            return guard._iopen(file, *a, **kw)

        def osopen(path, *a, **kw):
            guard._check(path, "os.open")
            return guard._osopen(path, *a, **kw)

        builtins.open, io.open, os.open = bopen, iopen, osopen
        return self

    def __exit__(self, *exc):
        builtins.open, io.open, os.open = self._bopen, self._iopen, self._osopen
        return False


# ======================================================================================
# helpers
# ======================================================================================
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fnum(x, spec="%.10g"):
    if x is None:
        return ""
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        return "nan"
    return spec % float(x)


def pp(x):
    return "%.6f" % float(x)


def write_rows(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def declared_block(path):
    txt = Path(path).read_text()
    i = txt.index("```json\n")
    j = txt.index("\n```", i)
    return json.loads(txt[i + len("```json\n"):j])


def verify_predecl_scalars(d):
    """The declared JSON must equal this driver's own constants, else REFUSE."""
    checks = {
        "anchor": (d["anchor"], ANCHOR),
        "levels": (list(d["levels"]), list(LEVELS)),
        "year_start": (int(d["year_start"]), YEARS[0]),
        "year_end": (int(d["year_end"]), YEARS[-1]),
        "n_anchor_years": (int(d["n_anchor_years"]), len(YEARS)),
        "tol_dup_pp": (float(d["tol_dup_pp"]), TOL_DUP_PP),
        "min_years_within_1pp": (int(d["min_years_within_1pp"]), MIN_YEARS_WITHIN),
        "tol_struct_pp": (float(d["tol_struct_pp"]), TOL_STRUCT_PP),
        "min_years_moved_le_0.5pp": (int(d["min_years_moved_le_0.5pp"]), MIN_YEARS_MOVED),
        "forbidden_basename": (d["forbidden_basename"], OBSERVED.name),
        "void_exit_code": (int(d["void_exit_code"]), VOID_EXIT),
        "s_ident_tol_rel": (float(d["s_ident_tol_rel"]), S_IDENT_TOL_REL),
        "frozen_sim_v16_sha256": (d["frozen_sim_v16_sha256"], sha256_file(FROZEN / "sim_v1_6_repair.py")),
        "frozen_sim_v13_sha256": (d["frozen_sim_v13_sha256"], sha256_file(FROZEN / "sim_v1_3.py")),
        "frozen_v13_panel_sha256": (d["frozen_v13_panel_sha256"], sha256_file(V13_PANEL)),
        "frozen_a10_panel_sha256": (d["frozen_a10_panel_sha256"], sha256_file(A10_PANEL)),
        "frozen_v16_predecl_sha256": (d["frozen_v16_predecl_sha256"], sha256_file(V16_PREDECL)),
        "engine_arm": (dict(d["engine_arm"]), dict(ENGINE)),
    }
    bad = {k: v for k, v in checks.items() if v[0] != v[1]}
    if bad:
        raise SystemExit("REFUSED: declared block != code constants: %r" % (bad,))
    return len(checks)


def read_v13_targets():
    """The frozen block's own demand objects (SYNTHETIC panel). The only panel read."""
    out = {}
    with open(V13_PANEL, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != ANCHOR:
                continue
            y = int(float(r["year"]))
            if y not in YEARS or r["level"] not in LEVELS:
                continue
            out[(r["level"], y)] = dict(
                demand_official=float(r["demand_official"]),
                cohort=float(r["cohort"]),
                demand_share=float(r["demand_share"]),
            )
    miss = [(lv, y) for lv in LEVELS for y in YEARS if (lv, y) not in out]
    if miss:
        raise SystemExit("REFUSED: frozen v1.3 panel missing target cells: %r" % (miss[:5],))
    return out


def read_a10_identity():
    """P0's frozen output, for the S-IDENT guard (synthetic identity only)."""
    cols = ("demand_official", "cohort", "admitted_official", "seats", "survival",
            "completion_uis", "demand_share")
    out = {}
    with open(A10_PANEL, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["country"] != ANCHOR:
                continue
            y = int(float(r["year"]))
            if y not in YEARS or r["level"] not in LEVELS:
                continue
            out[(r["level"], y)] = {c: float(r[c]) for c in cols}
    return out


def result_field(res, col, L, t):
    name = {"demand_official": "demand_off", "admitted_official": "intake_off",
            "seats": "seats", "survival": "surv", "completion_uis": "comp_uis",
            "demand_share": "demand_share", "cohort": "C"}[col]
    return float(res[name][L, t])


# ======================================================================================
# the pipeline
# ======================================================================================
def run_pipeline(outdir, log, guard_meta):
    import arms as A                     # local module (declared import set)
    sys.path.insert(0, str(FROZEN))
    import sim_v1_6_repair as S
    import sim_v1_3 as V13

    # mount the frozen module's path constants at their canonical locations (no read)
    S.ROOT = V16_DIR
    S.SYNTH = SYNTH
    S.MASS = MASS
    S.DATA = MASS / "data"
    S.V12_DIR = SYNTH / "generator_v1_2"
    S.V15_DIR = SYNTH / "generator_v1_5_bimodal"
    S.SHADOW_DIR = SYNTH / "shadow_module"
    S.PARAMS_MD = V16_DIR / "PARAMS.md"

    # ---- frozen predeclaration integrity: the object under test is the declared one -----
    pre16 = S.verify_predecl(path=V16_PREDECL,
                             expected_sha="6a554dc033828835431f65be2e5e218833fcdb56220baad8fbe53c3324e78991")
    if sha256_file(V16_PREDECL) != pre16["sha256"]:
        raise SystemExit("REFUSED: frozen v1.6 predeclaration hash mismatch")

    # ---- declared demographic input, reconstructed with no observed read ----------------
    S_path, Pop_path, n_band = A.declared_demographic_path(
        V13_PANEL, S.YEARS, S.P["band_share"][0])

    def demographic_stub():
        """Replaces the frozen load_observed_phl_paths BEFORE any arm runs (declared in
        PRE_DECLARATIONS.md sec.6). Returns no observed object at all."""
        return S_path, Pop_path, {}, {}, {}

    S.load_observed_phl_paths = demographic_stub

    # ---- capability lint ---------------------------------------------------------------
    arm_fns = A.make_arms(S, V13)
    if set(arm_fns) != set(ARMS):
        raise SystemExit("REFUSED: CAPABILITY-LINT (arm set)")

    records = {}
    for arm in ARMS:
        cells_fn, alloc_fn = arm_fns[arm]
        S.tier_cells, S.tier_allocate = cells_fn, alloc_fn
        res, hosts = S.run_arm_full(**ENGINE)
        if hosts.get("SYN_PHL_LIKE") != ANCHOR:
            raise SystemExit("REFUSED: anchor is not the declared PHL-like host")
        i = [j for j, r in enumerate(res) if r["cp"]["name"] == ANCHOR][0]
        records[arm] = res[i]
    # restore the frozen lookups (P0 is the built arm)
    S.tier_cells, S.tier_allocate = arm_fns["P0"]

    # ---- comparison objects are read ONLY after every arm has finished (copy-blind) ----
    targets = read_v13_targets()
    a10 = read_a10_identity()

    # ---- S-IDENT: P0 must reproduce the frozen A10 panel -------------------------------
    ident = {"tol_rel": S_IDENT_TOL_REL, "max_rel": 0.0, "worst": None, "n_cells_compared": 0}
    for lv in LEVELS:
        L = LEVELS.index(lv)
        for y in YEARS:
            t = y - S.YEAR_START
            ref = a10[(lv, y)]
            for col in ref:
                got = result_field(records["P0"], col, L, t)
                want = ref[col]
                rel = abs(got - want) / max(abs(want), 1e-12)
                ident["n_cells_compared"] += 1
                if rel > ident["max_rel"]:
                    ident["max_rel"] = rel
                    ident["worst"] = {"level": lv, "year": y, "column": col,
                                      "frozen": fnum(want), "run": fnum(got)}
    ident["passes"] = bool(ident["max_rel"] <= S_IDENT_TOL_REL)
    if not ident["passes"]:
        raise SystemExit("REFUSED: DEMOGRAPHIC-INPUT-IDENTITY (max_rel %.3e)" % ident["max_rel"])

    # ---- metrics -----------------------------------------------------------------------
    detail = []
    per_level = {}
    for arm in ARMS:
        r = records[arm]
        for lv in LEVELS:
            L = LEVELS.index(lv)
            g, m, rows = [], [], []
            for y in YEARS:
                t = y - S.YEAR_START
                tg = targets[(lv, y)]
                dem = float(r["demand_off"][L, t])
                coh = float(r["C"][L, t])
                dc = dem / coh
                tgt_dc = tg["demand_official"] / tg["cohort"]
                ds = float(r["demand_share"][L, t])
                v13_ds = tg["demand_share"]
                p0 = records["P0"]
                p0_dc = float(p0["demand_off"][L, t]) / float(p0["C"][L, t])
                gap = abs(dc - tgt_dc) * 100.0
                move = abs(dc - p0_dc) * 100.0
                sec_gap = abs(ds - v13_ds) * 100.0
                K_O = float(r["tier_K_O"][L, t])
                V_O = float(r["tier_V_O"][L, t])
                g.append(gap)
                m.append(move)
                rows.append(dict(
                    arm=arm, level=lv, year=y,
                    demand_official=dem, cohort=coh, dc=dc,
                    v13_demand_official=tg["demand_official"], v13_cohort=tg["cohort"],
                    v13_dc=tgt_dc, gap_pp=gap, p0_dc=p0_dc, move_pp=move,
                    ds=ds, v13_ds=v13_ds, secondary_gap_pp=sec_gap,
                    eligible_share=float(r["elig"][L, t]),
                    seats_over_cohort=float(r["seats"][L, t]) / coh,
                    K_H_over_cohort=float(r["tier_K_H"][L, t]) / coh,
                    K_O_over_cohort=K_O / coh,
                    admitted_H_over_cohort=float(r["tier_adm_H"][L, t]) / coh,
                    T_O_over_cohort=float(r["tier_T_O"][L, t]) / coh,
                    V_O_over_cohort=V_O / coh,
                    unfilled_share=(V_O / K_O) if K_O > 1e-12 else 0.0,
                    admitted_official_over_cohort=float(r["intake_off"][L, t]) / coh,
                    queue_H_over_cohort=float(r["tier_queue_H"][L, t]) / coh,
                ))
                detail.append(rows[-1])
            within = sum(1 for x in g if x <= TOL_DUP_PP + 1e-12)
            moved = sum(1 for x in m if x <= TOL_STRUCT_PP + 1e-12)
            moved_reported = moved if arm != "P0" else None   # P0 vs P0 is not a movement
            dup = within >= MIN_YEARS_WITHIN
            struct = moved >= MIN_YEARS_MOVED
            label = ("DUPLICATED-PRIMITIVES" if dup
                     else ("STRUCTURAL-MENU" if struct else "MIXED"))
            unf = [x["unfilled_share"] for x in rows]
            per_level[(arm, lv)] = {
                "arm": arm, "level": lv, "n_years": len(YEARS),
                "years_within_1pp": within, "years_moved_le_0.5pp": moved_reported,
                "mean_gap_pp": float(np.mean(g)), "max_gap_pp": float(np.max(g)),
                "mean_move_pp": float(np.mean(m)), "max_move_pp": float(np.max(m)),
                "label": label, "both_applicable": int(dup and struct),
                "mean_dc": float(np.mean([x["dc"] for x in rows])),
                "mean_target_dc": float(np.mean([x["v13_dc"] for x in rows])),
                "mean_secondary_gap_pp": float(np.mean([x["secondary_gap_pp"] for x in rows])),
                "max_secondary_gap_pp": float(np.max([x["secondary_gap_pp"] for x in rows])),
                "years_unfilled_zero": sum(1 for x in unf if x <= 1e-12),
                "years_unfilled_ge_0_10": sum(1 for x in unf if x >= 0.10 - 1e-12),
                "unfilled_share_min": float(np.min(unf)), "unfilled_share_max": float(np.max(unf)),
            }

    # ---- verdict (P1 only; P0/P2 are report-only) --------------------------------------
    labels = [per_level[("P1", lv)]["label"] for lv in LEVELS]
    if all(x == "DUPLICATED-PRIMITIVES" for x in labels):
        agg = "DUPLICATED-PRIMITIVES"
    elif all(x == "STRUCTURAL-MENU" for x in labels):
        agg = "STRUCTURAL-MENU"
    else:
        agg = "MIXED"
    verdict = {"aggregate": agg, "per_level": {lv: per_level[("P1", lv)]["label"] for lv in LEVELS},
               "aggregation_rule": "unanimous_else_MIXED"}

    # ---- write -------------------------------------------------------------------------
    write_outputs(outdir, per_level, detail, ident, pre16, verdict)
    return {"verdict": verdict, "ident": ident, "per_level": per_level,
            "n_detail": len(detail), "n_checked": pre16["n_checked"], "n_band": n_band}


def write_outputs(outdir, per_level, detail, ident, pre16, verdict):
    outdir = Path(outdir)
    rows = []
    agg_note = {
        "P0": "comparator, as built; movement is a self-comparison",
        "P1": "aggregate = unanimous_else_MIXED; per-level: " + ", ".join(
            "%s=%s" % (lv, verdict["per_level"][lv]) for lv in LEVELS),
        "P2": "report-only, never adopted (nesting diagnostic for the unfilled object)",
    }
    for arm in ARMS:
        for lv in LEVELS:
            p = per_level[(arm, lv)]
            rows.append([arm, lv, "YES" if arm in ("P1",) else "NO", p["n_years"],
                         p["years_within_1pp"],
                         "" if p["years_moved_le_0.5pp"] is None else p["years_moved_le_0.5pp"],
                         pp(p["mean_gap_pp"]), pp(p["max_gap_pp"]),
                         pp(p["mean_move_pp"]), pp(p["max_move_pp"]),
                         fnum(p["mean_dc"]), fnum(p["mean_target_dc"]),
                         pp(p["mean_secondary_gap_pp"]), pp(p["max_secondary_gap_pp"]),
                         p["years_unfilled_zero"], p["years_unfilled_ge_0_10"],
                         fnum(p["unfilled_share_min"]), fnum(p["unfilled_share_max"]),
                         p["label"] if arm == "P1" else "", p["both_applicable"],
                         "verdict-bearing" if arm == "P1" else
                         ("comparator (as built)" if arm == "P0" else "report-only, never adopted")])
        agg = verdict["aggregate"] if arm == "P1" else ""
        rows.append([arm, "ALL", "YES" if arm == "P1" else "NO", len(YEARS), "", "", "", "", "", "",
                     "", "", "", "", "", "", "", "", agg, "", agg_note[arm]])
    write_rows(outdir / "PARTPROV_RESULTS.csv",
               ["arm", "level", "verdict_bearing", "n_years", "years_within_1pp",
                "years_moved_le_0.5pp", "mean_gap_pp", "max_gap_pp", "mean_move_pp",
                "max_move_pp", "mean_demand_over_cohort", "mean_target_demand_over_cohort",
                "mean_secondary_gap_pp", "max_secondary_gap_pp", "years_unfilled_zero",
                "years_unfilled_ge_0.10", "unfilled_share_min", "unfilled_share_max",
                "verdict", "both_applicable", "note"], rows)

    drows = []
    for d in detail:
        drows.append([d["arm"], d["level"], d["year"],
                      fnum(d["demand_official"]), fnum(d["cohort"]), fnum(d["dc"]),
                      fnum(d["v13_demand_official"]), fnum(d["v13_cohort"]), fnum(d["v13_dc"]),
                      pp(d["gap_pp"]), fnum(d["p0_dc"]), pp(d["move_pp"]),
                      fnum(d["ds"]), fnum(d["v13_ds"]), pp(d["secondary_gap_pp"]),
                      fnum(d["eligible_share"]), fnum(d["seats_over_cohort"]),
                      fnum(d["K_H_over_cohort"]), fnum(d["K_O_over_cohort"]),
                      fnum(d["admitted_H_over_cohort"]), fnum(d["T_O_over_cohort"]),
                      fnum(d["V_O_over_cohort"]), fnum(d["unfilled_share"]),
                      fnum(d["admitted_official_over_cohort"]), fnum(d["queue_H_over_cohort"])])
    write_rows(outdir / "PARTPROV_DETAIL.csv",
               ["arm", "level", "year", "demand_official", "cohort", "demand_official_over_cohort",
                "v13_demand_official", "v13_cohort", "v13_demand_official_over_cohort", "gap_pp",
                "p0_demand_official_over_cohort", "move_vs_p0_pp", "demand_share_ds",
                "v13_demand_share_ds", "secondary_gap_pp", "eligible_share", "seats_over_cohort",
                "K_H_over_cohort", "K_O_over_cohort", "admitted_H_over_cohort",
                "T_O_over_cohort", "V_O_over_cohort", "unfilled_share",
                "admitted_official_over_cohort", "queue_H_over_cohort"], drows)


def write_audit(outdir, audit):
    with open(Path(outdir) / "COUNT_BLIND_AUDIT.json", "w") as fh:
        json.dump(audit, fh, indent=2, sort_keys=True)
        fh.write("\n")


def build_audit(log, guard_meta, ident, pre16, verdict, n_band):
    opens = {}
    for e in log:
        k = (e["path"], e["op"], e["allowed"])
        opens[k] = opens.get(k, 0) + 1
    files_opened = [{"path": k[0], "op": k[1], "count": v}
                    for k, v in sorted(opens.items()) if k[2]]
    blocked_detail = [{"path": k[0], "op": k[1], "count": v}
                      for k, v in sorted(opens.items()) if not k[2]]
    return {
        "cell": "EXP-16-PARTPROV",
        "label": LABEL,
        "predeclaration": {"sha256": sha256_file(PREDECL),
                           "frozen_sha256_declared": PREDECL_SHA,
                           "verified": sha256_file(PREDECL) == PREDECL_SHA},
        "guard": {
            "forbidden_basename": OBSERVED.name,
            "observed_path_resolved": guard_meta["norm"](OBSERVED),
            "observed_file_opened": guard_meta["observed_opened"],
            "observed_bytes_read": 0,
            "blocked_attempts": guard_meta["blocked"],
            "guard_selftest": guard_meta["selftest"],
            "void": False,
        },
        "count_blind": {
            "count_computed": False,
            "observed_values_in_outputs": 0,
            "n_33cell_counts_emitted": 0,
            "n_observed_files_referenced_in_code": 0,
        },
        "ast_scan": guard_meta["ast"],
        "own_code_rule": guard_meta.get("own_code_rule", {}),
        "frozen_forbidden_literal_functions": guard_meta.get("frozen_hits", []),
        "frozen_loader_shadowed": "S.load_observed_phl_paths replaced by arms.declared_demographic_path "
                                  "stub before any arm (PRE_DECLARATIONS.md sec.6)",
        "reachability_lint": guard_meta["reach"],
        "static_refusals": guard_meta["refusals"],
        "imports": guard_meta["imports"],
        "capability_lint": "PASS",
        "s_ident_p0_vs_frozen_a10": ident,
        "frozen_v16_predecl": {"sha256": pre16["sha256"], "n_parameters_checked": pre16["n_checked"]},
        "demographic_input": {"source": "<PROG>/10_massification/extensions/synthetic_2026-11-20/"
                                        "generator_v1_3/results/synthetic_panel_v1_3.csv",
                              "reconstruction": "S_path = band_population(primary,t)/band_share[0]; "
                                                "Pop_path = population(t)",
                              "n_band_rows": n_band,
                              "observed_file_used": False},
        "verdict": verdict["aggregate"],
        "verdict_per_level": verdict["per_level"],
        "files_opened": files_opened,
        "blocked_attempts_detail": blocked_detail,
        "target_read_order": "both comparison objects (frozen v1.3 panel, frozen A10 panel) are "
                             "read only AFTER all three arms have finished; no target value is "
                             "passed to any arm",
        "determinism": guard_meta.get("determinism", "PENDING"),
    }


def emit_void(outdir, reason, guard_meta, log):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    audit = {
        "cell": "EXP-16-PARTPROV", "label": LABEL,
        "guard": {"forbidden_basename": OBSERVED.name,
                  "observed_path_resolved": guard_meta["norm"](OBSERVED),
                  "observed_file_opened": guard_meta["observed_opened"],
                  "blocked_attempts": guard_meta["blocked"],
                  "guard_selftest": guard_meta["selftest"], "void": True,
                  "reason": reason},
        "count_blind": {"count_computed": False, "observed_values_in_outputs": 0},
        "ast_scan": guard_meta.get("ast", []),
        "files_opened": log,
        "verdict": "VOID (CONTAMINATED-BY-DESIGN)",
    }
    with open(outdir / "COUNT_BLIND_AUDIT.json", "w") as fh:
        json.dump(audit, fh, indent=2, sort_keys=True)
        fh.write("\n")
    write_rows(outdir / "PARTPROV_RESULTS.csv",
               ["arm", "level", "verdict_bearing", "n_years", "years_within_1pp",
                "years_moved_le_0.5pp", "mean_gap_pp", "max_gap_pp", "mean_move_pp",
                "max_move_pp", "mean_demand_over_cohort", "mean_target_demand_over_cohort",
                "mean_secondary_gap_pp", "max_secondary_gap_pp", "years_unfilled_zero",
                "years_unfilled_ge_0.10", "unfilled_share_min", "unfilled_share_max",
                "verdict", "both_applicable", "note"],
               [["P0/P1/P2", "ALL", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                 "", "", "VOID (CONTAMINATED-BY-DESIGN)", "", reason]])
    write_rows(outdir / "PARTPROV_DETAIL.csv", ["arm", "level", "year"], [])


def static_checks(guard_meta, A):
    # ---- static (AST) scan of every source this cell executes or imports -----------
    src = [CODE / "run_partprov.py", CODE / "arms.py",
           FROZEN / "sim_v1_6_repair.py", FROZEN / "sim_v1_3.py"]
    guard_meta["ast"] = A.ast_scan_files(src, OBSERVED.name)
    own = [s for s in guard_meta["ast"] if s["file"] in ("run_partprov.py", "arms.py")]
    rule = A.own_code_rule([CODE / "run_partprov.py", CODE / "arms.py"], OBSERVED.name)
    guard_meta["own_code_rule"] = rule
    if rule["verdict"] != "PASS":
        guard_meta["refusals"].append({"rule": "AST-OWN-CODE-CLEAN", "failed": rule})
        raise SystemExit("REFUSED: AST-OWN-CODE-CLEAN %r" % (rule,))
    if not own or any(not s["sha256"] for s in own):
        raise SystemExit("REFUSED: AST scan did not cover the cell's own sources")
    frozen_hits = [{"file": s["file"], "n": len(s["forbidden_literal_hits"]),
                    "functions": sorted({h["enclosing_function"] for h in s["forbidden_literal_hits"]})}
                   for s in guard_meta["ast"]
                   if s["file"] in ("sim_v1_6_repair.py", "sim_v1_3.py")]
    guard_meta["frozen_hits"] = frozen_hits

    called = A.ast_called_names([CODE / "run_partprov.py", CODE / "arms.py"],
                                {"S", "V13", "A"})
    allow = {"S": A.CALL_ALLOWLIST, "V13": A.V13_ALLOWLIST, "A": A.ARMS_ALLOWLIST}
    unknown = {k: sorted(n for n in v if n not in allow.get(k, frozenset()))
               for k, v in called.items()}
    unknown = {k: v for k, v in unknown.items() if v}
    if unknown:
        guard_meta["refusals"].append({"rule": "REACHABILITY-LINT", "failed": unknown})
        raise SystemExit("REFUSED: REACHABILITY-LINT %r" % (unknown,))
    guard_meta["reach"] = called



def guard_selftest(outdir, guard_meta, guard, log):
    """Positive control: the observed open MUST be blocked before the OS call.

    Exactly one definition site; both run passes call it. A successful open here means the
    guard is dead, so the cell is VOID and nothing is scored.
    """
    guard_meta["norm"] = guard.norm
    try:
        open(OBSERVED, "rb")
    except ObservedFileAccess:
        guard_meta["selftest"] = "BLOCKED-AS-REQUIRED"
        guard_meta["observed_opened"] = False
        guard_meta["blocked"] = guard.blocked
        return
    guard_meta["selftest"] = "FAILED-OPEN-SUCCEEDED"
    guard_meta["observed_opened"] = True
    guard_meta["blocked"] = guard.blocked
    emit_void(outdir, "GUARD-SELFTEST-FAILED", guard_meta, log)
    print("VOID (CONTAMINATED-BY-DESIGN): guard self-test failed")
    sys.exit(VOID_EXIT)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(CELL / "results"))
    ap.add_argument("--no-determinism", action="store_true")
    args = ap.parse_args(argv)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    log = []
    guard_meta = {"ast": [], "reach": {}, "refusals": [], "imports": {},
                  "blocked": 0, "observed_opened": False, "selftest": "NOT-RUN"}

    # ---- freeze integrity (before anything else) ---------------------------------------
    got = sha256_file(PREDECL)
    if got != PREDECL_SHA:
        raise SystemExit("REFUSING: PRE_DECLARATIONS.md sha256 %s != frozen %s" % (got, PREDECL_SHA))
    d = declared_block(PREDECL)
    n_scalars = verify_predecl_scalars(d)

    with AuditGuard(OBSERVED.name, outdir, PROG, log) as guard:
        guard_meta["norm"] = guard.norm

        import arms as A

        # ---- static (AST) scan + reachability lint ------------------------------------
        static_checks(guard_meta, A)

        # ---- guard self-test: the observed open MUST be blocked -----------------------
        guard_selftest(outdir, guard_meta, guard, log)

        body = run_pipeline(outdir, log, guard_meta)

        # ---- module provenance ---------------------------------------------------------
        imported = {}
        for name, mod in list(sys.modules.items()):
            f = getattr(mod, "__file__", None)
            if not f:
                continue
            rp = os.path.abspath(f)
            if rp.startswith(str(CELL)) or rp.startswith(str(SYNTH)):
                imported[name] = guard.norm(rp)
        guard_meta["imports"] = dict(sorted(imported.items()))
        declared_imports = {"arms", "run_partprov", "__main__", "sim_v1_6_repair", "sim_v1_3"}
        extra = sorted(set(imported) - declared_imports)
        if extra:
            raise SystemExit("REFUSED: IMPORT-SET %r" % (extra,))

        body["audit"] = build_audit(log, guard_meta, body["ident"],
                                    {"sha256": sha256_file(V16_PREDECL),
                                     "n_checked": body["n_checked"]},
                                    body["verdict"], body["n_band"])
        write_audit(outdir, body["audit"])

    # ---- determinism ---------------------------------------------------------------------
    if not args.no_determinism:
        det_dir = outdir / "determinism_run2"
        det_dir.mkdir(parents=True, exist_ok=True)
        log2 = []
        gm2 = {"ast": [], "reach": {}, "refusals": [], "imports": {},
               "blocked": 0, "observed_opened": False, "selftest": "NOT-RUN"}
        with AuditGuard(OBSERVED.name, det_dir, PROG, log2) as g2:
            static_checks(gm2, A)
            guard_selftest(det_dir, gm2, g2, log2)
            body2 = run_pipeline(det_dir, log2, gm2)
            body2["audit"] = build_audit(log2, gm2, body2["ident"],
                                         {"sha256": sha256_file(V16_PREDECL),
                                          "n_checked": body2["n_checked"]},
                                         body2["verdict"], body2["n_band"])
            write_audit(det_dir, body2["audit"])
        names = ["PARTPROV_RESULTS.csv", "PARTPROV_DETAIL.csv", "COUNT_BLIND_AUDIT.json"]
        same = []
        for n in names:
            same.append(sha256_file(outdir / n) == sha256_file(det_dir / n))
        det = {"status": "BYTE-IDENTICAL" if all(same) else "NOT-IDENTICAL",
               "files": names, "n": len(names), "n_identical": sum(same)}
        if not all(same):
            print("UNDETERMINED: two runs are not byte-identical; no verdict issued")
            sys.exit(1)
        # stamp the determinism line into both audits (identical string in both files)
        for od in (outdir, det_dir):
            p = od / "COUNT_BLIND_AUDIT.json"
            a = json.loads(p.read_text())
            a["determinism"] = det["status"]
            with open(p, "w") as fh:
                json.dump(a, fh, indent=2, sort_keys=True)
                fh.write("\n")
    else:
        det = {"status": "DETERMINISM-NOT-RUN", "files": [], "n": 0, "n_identical": 0}

    # ---- manifest + sums ---------------------------------------------------------------
    files = []
    for root, _dirs, names in os.walk(outdir):
        for n in sorted(names):
            p = Path(root) / n
            rel = os.path.relpath(p, CELL)
            if rel in ("RUN_MANIFEST.json", "SHA256SUMS.txt"):
                continue
            files.append(rel)
    files.sort()
    manifest = {
        "cell": "EXP-16-PARTPROV",
        "label": LABEL,
        "date": "2026-11-21",
        "question": "is the participation margin a duplicated parameterisation or a structural "
                    "consequence of the declared tier menu?",
        "predeclaration": {"file": "PRE_DECLARATIONS.md", "sha256": sha256_file(PREDECL),
                           "n_declared_scalars_checked": n_scalars},
        "frozen_inputs": {
            "sim_v1_6_repair.py": sha256_file(V16_SIM),
            "sim_v1_3.py": sha256_file(V13_SIM),
            "copied_sim_v1_6_repair.py": sha256_file(FROZEN / "sim_v1_6_repair.py"),
            "copied_sim_v1_3.py": sha256_file(FROZEN / "sim_v1_3.py"),
            "panel_A10_repaired.csv": sha256_file(A10_PANEL),
            "synthetic_panel_v1_3.csv": sha256_file(V13_PANEL),
            "v16_PRE_DECLARATIONS.md": sha256_file(V16_PREDECL),
        },
        "code": {"run_partprov.py": sha256_file(CODE / "run_partprov.py"),
                 "arms.py": sha256_file(CODE / "arms.py")},
        "verdict": body["verdict"],
        "count_blind": {"observed_file_opened": False, "count_computed": False,
                        "guard_selftest": guard_meta["selftest"],
                        "blocked_attempts": guard_meta["blocked"]},
        "determinism": det,
        "p2_status": "reported, never adopted",
        "files": files,
    }
    with open(CELL / "RUN_MANIFEST.json", "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    sums = []
    for rel in files + ["RUN_MANIFEST.json"]:
        p = CELL / rel
        if p.exists():
            sums.append("%s  %s" % (sha256_file(p), rel))
    sums.append("%s  %s" % (sha256_file(CELL / "PRE_DECLARATIONS.md"), "PRE_DECLARATIONS.md"))
    with open(CELL / "SHA256SUMS.txt", "w") as fh:
        fh.write("\n".join(sorted(sums)) + "\n")

    print("verdict: %s  per-level: %r" % (body["verdict"]["aggregate"], body["verdict"]["per_level"]))
    print("determinism: %s (%d/%d)" % (det["status"], det["n_identical"], det["n"]))
    print("count-blind: observed_opened=%s selftest=%s blocked=%d"
          % (guard_meta["observed_opened"], guard_meta["selftest"], guard_meta["blocked"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
