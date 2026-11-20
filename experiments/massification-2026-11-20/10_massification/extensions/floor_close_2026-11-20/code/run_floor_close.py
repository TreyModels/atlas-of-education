#!/usr/bin/env python3
"""EXP-12 FLOOR-CLOSE: what closes the model's floor gate — places, cohort, or the
declared phys_cap = 1.15 crowding allowance?

Read-only accounting decomposition of the frozen synthetic panel.  Every definition,
bar and threshold is frozen in PRE_DECLARATIONS.md (sha256 1db266e2...e06e44) before
this script is first executed.  No RNG, no clock, no environment-dependent ordering.

Outputs (under <experiment>/<outdir>, outdir defaults to results/):
  FLOOR_CLOSE_RESULTS.csv        closing cells with factor shares and verdict
  FLOOR_CLOSE_SHAPLEY.csv        per-cell Shapley values (log units) and shares
  FLOOR_CLOSE_DETAIL.csv         the 6 ordering x 3 factor marginal contributions
  FLOOR_CLOSE_SENSITIVITY.csv    non-verdict-bearing S1/S2 sensitivities
  FLOOR_CLOSE_PANEL.json         panel verdict, counts, anchor, exclusions
"""

import csv
import hashlib
import itertools
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXP_DIR = HERE.parent
PROGRAMME_ROOT = EXP_DIR.parents[2]

PANEL = (PROGRAMME_ROOT / "10_massification" / "extensions" / "synthetic_2026-11-20"
         / "generator_v1_2" / "results" / "synthetic_panel_v1_2.csv")
PREDECL = EXP_DIR / "PRE_DECLARATIONS.md"
OUTDIR = (EXP_DIR / sys.argv[1]) if len(sys.argv) > 1 else (EXP_DIR / "results")

# ---------------------------------------------------------------- frozen constants
# PRE_DECLARATIONS.md sections 2-3.  Changing any of these voids the predeclaration.
PANEL_SHA256 = "14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac"
PREDECL_SHA256 = "1db266e2739d09cf54d8ec5dc4f72f2b8e73d6471b4bc7a1ff99de0924e06e44"

LEVEL_ORDER = ("primary", "lower_secondary", "upper_secondary", "tertiary")
PHYS_CAP = 1.15            # DECLARED (PARAMS.md section 4)
OVERAGE_CAP = 1.05         # CONVENTION (PARAMS.md section 4)
PHYS_CAP0 = 1.0            # declared no-crowding reference for the allowance factor
MIN_BINDING_YEARS = 3      # "after >= 3 binding years"
N_MIN = 30                 # falsifier: fewer than 30 closing cells -> UNDETERMINED
SHARE_BAR = 0.5            # ">= 50 % of the log change"
CELL_BAR = 0.5             # "in >= 50 % of cells"
OPEN_EPS = 1e-12           # rounding guard on p_off = 1

ORDERINGS = tuple(itertools.permutations(("A", "P", "Q")))
FACTOR_NAME = {"A": "ALLOWANCE", "P": "PLACES", "Q": "DEMAND/COHORT"}
CELL_LABEL = {"A": "ALLOWANCE-CARRIED", "P": "CAPACITY-CARRIED",
              "Q": "DEMAND-CARRIED"}
LABEL_ORDER = ("ALLOWANCE-CARRIED", "CAPACITY-CARRIED", "DEMAND-CARRIED", "MIXED")

ANCHOR_COUNTRY = "SYN00_PHL_LIKE"
ANCHOR_LEVEL = "primary"
ANCHOR_CLOSE_YEAR = 2019
ANCHOR_SEAT_COVERAGE = 0.8722
ANCHOR_V10_CAPACITY_115 = 2432921.0

EXPERIMENT = "EXP-12 FLOOR-CLOSE"
LABEL = "SYNTHETIC"

RESULTS_HEADER = [
    "level", "country", "country_id", "year_last_binding", "year_close",
    "binding_years_before_close", "seat_coverage_close",
    "seats_bind", "cohort_bind", "demand_bind",
    "seats_close", "cohort_close", "demand_close",
    "capacity_bind_115", "capacity_close_115",
    "margin_bind_log", "margin_close_log",
    "binding_branch_close", "cohort_branch", "anchor",
    "delta_log", "share_allowance", "share_places", "share_demand", "share_sum",
    "carried_leg", "cell_label",
]
SHAPLEY_HEADER = [
    "level", "country", "country_id", "year_last_binding", "year_close",
    "f_start", "f_end", "delta_log",
    "phi_allowance", "phi_places", "phi_demand",
    "share_allowance", "share_places", "share_demand",
    "efficiency_residual", "cohort_branch", "branch_switch", "anchor", "cell_label",
]
DETAIL_HEADER = [
    "level", "country", "country_id", "year_last_binding", "year_close",
    "ordering", "step", "factor", "factor_name", "from_value", "to_value",
    "f_before", "f_after", "marginal", "phi_factor", "share_factor",
]
SENS_HEADER = [
    "level", "country", "country_id", "year_close",
    "delta_observed_s1", "s1_share_allowance", "s1_share_places", "s1_share_demand",
    "delta_capacity_s2", "s2_share_allowance", "s2_share_places", "s2_share_demand",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def num(row, key):
    raw = row[key]
    if raw is None or raw == "":
        sys.exit(f"FATAL: empty cell {key!r} in "
                 f"{row.get('country')}/{row.get('level')}/{row.get('year')}")
    try:
        val = float(raw)
    except ValueError:
        sys.exit(f"FATAL: non-numeric {key!r}={raw!r}")
    if not math.isfinite(val):
        sys.exit(f"FATAL: non-finite {key!r}={raw!r}")
    return val


def fmt(x):
    return f"{x:.12f}"


def fval(p, s, c, d):
    """Declared capacity rule / gate demand, on the binding branch of the min."""
    return math.log(min(p * s, OVERAGE_CAP * c) / d)


def branch_of(p, s, c):
    return "cohort" if OVERAGE_CAP * c < p * s else "places"


def state_f(state):
    return fval(state["A"], state["P"], state["Q"][0], state["Q"][1])


def shapley(start, end):
    """Equal-split Shapley over 3 factors; returns phi and per-ordering detail."""
    phi = {k: 0.0 for k in ("A", "P", "Q")}
    detail = []
    for order in ORDERINGS:
        state = dict(start)
        prev = state_f(state)
        for step, key in enumerate(order, start=1):
            before = state[key]
            state[key] = end[key]
            cur = state_f(state)
            marginal = cur - prev
            phi[key] += marginal
            detail.append((order, step, key, before, end[key], prev, cur, marginal))
            prev = cur
    return {k: v / 6.0 for k, v in phi.items()}, detail


def load_panel():
    if sha256(PANEL) != PANEL_SHA256:
        sys.exit("FATAL: frozen-panel hash mismatch; refusing to run on a non-frozen panel")
    if sha256(PREDECL) != PREDECL_SHA256:
        sys.exit("FATAL: PRE_DECLARATIONS.md hash mismatch; the predeclaration moved")
    with open(PANEL, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != 6720:
        sys.exit(f"FATAL: expected 6720 rows, found {len(rows)}")
    if {r["level"] for r in rows} != set(LEVEL_ORDER):
        sys.exit("FATAL: unexpected level set")
    cells = {}
    for r in rows:
        cells.setdefault((r["country"], r["level"]), []).append(r)
    for key in cells:
        cells[key].sort(key=lambda r: int(r["year"]))
        if [int(r["year"]) for r in cells[key]] != list(range(1970, 2026)):
            sys.exit(f"FATAL: cell {key} does not span 1970-2025 contiguously")
    return cells


def p_off_series(rs):
    return [min(1.0, num(r, "admitted_official") / num(r, "demand_official")) for r in rs]


def identify(cells):
    """Closure census per PRE_DECLARATIONS section 3.2."""
    closing, excluded = [], []
    for key in sorted(cells, key=lambda k: (LEVEL_ORDER.index(k[1]),
                                            int(cells[k][0]["country_id"]))):
        rs = cells[key]
        p = p_off_series(rs)
        flags = [x < 1.0 - OPEN_EPS for x in p]
        ts = next((i for i, fl in enumerate(flags)
                   if (not fl) and sum(flags[:i]) >= MIN_BINDING_YEARS), None)
        if ts is None:
            if sum(flags) >= MIN_BINDING_YEARS:
                if not flags[-1]:
                    sys.exit(f"FATAL: right-censored cell {key} is not binding in 2025")
                reason = "RIGHT_CENSORED_STILL_BINDING"
            else:
                reason = "NEVER_BOUND_3_YEARS"
            excluded.append({"level": key[1], "country": key[0],
                             "country_id": int(rs[0]["country_id"]),
                             "reason": reason, "binding_years": int(sum(flags))})
            continue
        tb = ts - 1
        if not flags[tb]:
            sys.exit(f"FATAL: last binding year not binding for {key}")
        closing.append({"key": key, "rs": rs, "ts": ts, "tb": tb,
                        "binding_years": int(sum(flags[:ts]))})
    return closing, excluded


def closure_count(cells, open_eps, consecutive):
    n = 0
    for key in cells:
        rs = cells[key]
        flags = [x < 1.0 - open_eps for x in p_off_series(rs)]
        run = 0
        for i, fl in enumerate(flags):
            if (not fl) and ((run if consecutive else sum(flags[:i])) >= MIN_BINDING_YEARS):
                n += 1
                break
            run = run + 1 if fl else 0
    return n


def main():
    cells = load_panel()
    closing, excluded = identify(cells)

    results_rows, shapley_rows, detail_rows, sens_rows = [], [], [], []
    max_eff_resid = 0.0
    s3_cells, s3_max_resid = 0, 0.0
    cohort_branch_cells, branch_switch_cells = [], []
    anchor = None

    for cell in closing:
        key, rs, ts, tb = cell["key"], cell["rs"], cell["ts"], cell["tb"]
        country, level = key
        cid = int(rs[0]["country_id"])
        rb, rsx = rs[tb], rs[ts]
        sb, cb, db = num(rb, "seats"), num(rb, "cohort"), num(rb, "demand_official")
        ss, cs, ds = num(rsx, "seats"), num(rsx, "cohort"), num(rsx, "demand_official")

        cap_b = min(PHYS_CAP * sb, OVERAGE_CAP * cb)
        cap_s = min(PHYS_CAP * ss, OVERAGE_CAP * cs)
        m_b = math.log(cap_b / db)
        m_s = math.log(cap_s / ds)
        if not (m_b < 0.0 <= m_s):
            sys.exit(f"FATAL: closure margin sign violated at "
                     f"{country}/{level} {rb['year']}->{rsx['year']}")
        if not cap_b < db:
            sys.exit(f"FATAL: last binding year has capacity >= demand at "
                     f"{country}/{level}/{rb['year']}")

        cohort_branch = branch_of(PHYS_CAP, ss, cs) == "cohort"
        if cohort_branch:
            cohort_branch_cells.append(f"{country}/{level}/{rsx['year']}")

        start = {"A": PHYS_CAP0, "P": sb, "Q": (cb, db)}
        end = {"A": PHYS_CAP, "P": ss, "Q": (cs, ds)}
        f_start, f_end = state_f(start), state_f(end)
        delta = f_end - f_start
        if not delta > 0.0:
            sys.exit(f"FATAL: non-positive decomposition target at {country}/{level}")

        phi, detail = shapley(start, end)
        eff_resid = sum(phi.values()) - delta
        max_eff_resid = max(max_eff_resid, abs(eff_resid))
        if abs(eff_resid) > 1e-9 * max(1.0, abs(delta)):
            sys.exit(f"FATAL: Shapley efficiency violated at {country}/{level}: {eff_resid}")

        sigma = {k: phi[k] / delta for k in phi}

        # Branch switching: did any visited configuration put 1.05*cohort in the min?
        switched = False
        for order in ORDERINGS:
            state = dict(start)
            if branch_of(state["A"], state["P"], state["Q"][0]) == "cohort":
                switched = True
            for factor in order:
                state[factor] = end[factor]
                if branch_of(state["A"], state["P"], state["Q"][0]) == "cohort":
                    switched = True
        if switched:
            branch_switch_cells.append(f"{country}/{level}/{rsx['year']}")

        # S3 binding-branch additive identity (PRE_DECLARATIONS section 6.3): in a cell
        # that never leaves the places branch the Shapley values are exactly
        # ln(1.15), ln(s*/s_b), -ln(d*/d_b).
        if not switched and not cohort_branch:
            s3_cells += 1
            for got, want in ((phi["A"], math.log(PHYS_CAP / PHYS_CAP0)),
                              (phi["P"], math.log(ss / sb)),
                              (phi["Q"], -math.log(ds / db))):
                s3_max_resid = max(s3_max_resid, abs(got - want))
                if abs(got - want) > 1e-9 * max(1.0, abs(want)):
                    sys.exit(f"FATAL: S3 identity violated at {country}/{level}: "
                             f"{got} vs {want}")

        # A closing configuration on the cohort branch cannot carry the allowance leg
        # (PRE_DECLARATIONS section 3.6); its allowance share is forced to zero.
        sigma_a = 0.0 if cohort_branch else sigma["A"]
        carried = [k for k, s in (("A", sigma_a), ("P", sigma["P"]), ("Q", sigma["Q"]))
                   if s >= SHARE_BAR]
        carried_leg = {"A": "ALLOWANCE", "P": "PLACES", "Q": "DEMAND"}.get(
            carried[0] if carried else "", "NONE")
        cell_label = CELL_LABEL[carried[0]] if carried else "MIXED"

        is_anchor = (country == ANCHOR_COUNTRY and level == ANCHOR_LEVEL)
        if is_anchor:
            sc = ss / cs
            if int(rsx["year"]) != ANCHOR_CLOSE_YEAR or abs(sc - ANCHOR_SEAT_COVERAGE) > 1e-4:
                sys.exit(f"FATAL: anchor cell does not match V10 ({rsx['year']}, {sc})")
            if abs(PHYS_CAP * ss - ANCHOR_V10_CAPACITY_115) > 2.0:
                sys.exit("FATAL: anchor 1.15*seats does not match V10")
            if abs(num(rsx, "seat_coverage") - sc) > 1e-9:
                sys.exit("FATAL: panel seat_coverage is not seats/cohort at the anchor")
            anchor = {
                "country": country, "level": level,
                "year_last_binding": int(rb["year"]), "year_close": int(rsx["year"]),
                "binding_years_before_close": cell["binding_years"],
                "seats_close": ss, "cohort_close": cs, "demand_close": ds,
                "capacity_close_115": cap_s,
                "capacity_close_105_cohort": OVERAGE_CAP * cs,
                "seat_coverage_close": sc,
                "margin_bind": m_b, "margin_close": m_s,
                "binding_branch_close": "cohort" if cohort_branch else "places",
                "delta_log": delta,
                "share_allowance": sigma_a, "share_places": sigma["P"],
                "share_demand": sigma["Q"], "cell_label": cell_label,
                "v10_check": "PASS",
            }

        results_rows.append({
            "level": level, "country": country, "country_id": cid,
            "year_last_binding": int(rb["year"]), "year_close": int(rsx["year"]),
            "binding_years_before_close": cell["binding_years"],
            "seat_coverage_close": fmt(ss / cs),
            "seats_bind": fmt(sb), "cohort_bind": fmt(cb), "demand_bind": fmt(db),
            "seats_close": fmt(ss), "cohort_close": fmt(cs), "demand_close": fmt(ds),
            "capacity_bind_115": fmt(cap_b), "capacity_close_115": fmt(cap_s),
            "margin_bind_log": fmt(m_b), "margin_close_log": fmt(m_s),
            "binding_branch_close": "cohort" if cohort_branch else "places",
            "cohort_branch": "TRUE" if cohort_branch else "FALSE",
            "anchor": "TRUE" if is_anchor else "FALSE",
            "delta_log": fmt(delta),
            "share_allowance": fmt(sigma_a), "share_places": fmt(sigma["P"]),
            "share_demand": fmt(sigma["Q"]),
            "share_sum": fmt(sigma_a + sigma["P"] + sigma["Q"]),
            "carried_leg": carried_leg, "cell_label": cell_label,
        })

        shapley_rows.append({
            "level": level, "country": country, "country_id": cid,
            "year_last_binding": int(rb["year"]), "year_close": int(rsx["year"]),
            "f_start": fmt(f_start), "f_end": fmt(f_end), "delta_log": fmt(delta),
            "phi_allowance": fmt(phi["A"]), "phi_places": fmt(phi["P"]),
            "phi_demand": fmt(phi["Q"]),
            "share_allowance": fmt(sigma_a), "share_places": fmt(sigma["P"]),
            "share_demand": fmt(sigma["Q"]),
            "efficiency_residual": fmt(eff_resid),
            "cohort_branch": "TRUE" if cohort_branch else "FALSE",
            "branch_switch": "TRUE" if switched else "FALSE",
            "anchor": "TRUE" if is_anchor else "FALSE",
            "cell_label": cell_label,
        })

        for order, step, factor, fv, tv, f_before, f_after, marginal in detail:
            if factor == "Q":
                fv_s = f"{fv[0]:.12f}|{fv[1]:.12f}"
                tv_s = f"{tv[0]:.12f}|{tv[1]:.12f}"
            else:
                fv_s, tv_s = fmt(fv), fmt(tv)
            detail_rows.append({
                "level": level, "country": country, "country_id": cid,
                "year_last_binding": int(rb["year"]), "year_close": int(rsx["year"]),
                "ordering": "".join(order), "step": step, "factor": factor,
                "factor_name": FACTOR_NAME[factor], "from_value": fv_s, "to_value": tv_s,
                "f_before": fmt(f_before), "f_after": fmt(f_after),
                "marginal": fmt(marginal), "phi_factor": fmt(phi[factor]),
                "share_factor": fmt(sigma[factor]),
            })

        # ---- non-verdict-bearing sensitivities (PRE_DECLARATIONS section 6)
        s1_start = {"A": PHYS_CAP, "P": sb, "Q": (cb, db)}
        s1_end = {"A": PHYS_CAP, "P": ss, "Q": (cs, ds)}
        d1 = state_f(s1_end) - state_f(s1_start)
        phi1, _ = shapley(s1_start, s1_end)
        sig1 = {k: (phi1[k] / d1 if d1 else 0.0) for k in phi1}

        s2_start = {"A": PHYS_CAP0, "P": sb, "Q": (cb, db)}
        s2_end = {"A": PHYS_CAP, "P": ss, "Q": (cs, db)}
        d2 = state_f(s2_end) - state_f(s2_start)
        phi2, _ = shapley(s2_start, s2_end)
        sig2 = {k: (phi2[k] / d2 if d2 else 0.0) for k in phi2}

        sens_rows.append({
            "level": level, "country": country, "country_id": cid,
            "year_close": int(rsx["year"]), "delta_observed_s1": fmt(d1),
            "s1_share_allowance": fmt(sig1["A"]), "s1_share_places": fmt(sig1["P"]),
            "s1_share_demand": fmt(sig1["Q"]),
            "delta_capacity_s2": fmt(d2),
            "s2_share_allowance": fmt(sig2["A"]), "s2_share_places": fmt(sig2["P"]),
            "s2_share_demand": fmt(sig2["Q"]),
        })

    if anchor is None:
        sys.exit("FATAL: anchor cell not found among closing cells")

    # ---- panel verdict (PRE_DECLARATIONS section 3.7)
    n = len(results_rows)
    label_counts = {lab: sum(1 for r in results_rows if r["cell_label"] == lab)
                    for lab in LABEL_ORDER}
    if n < N_MIN:
        verdict = "UNDETERMINED"
    elif label_counts["ALLOWANCE-CARRIED"] / n >= CELL_BAR:
        verdict = "ALLOWANCE-CARRIED"
    elif label_counts["CAPACITY-CARRIED"] / n >= CELL_BAR:
        verdict = "CAPACITY-CARRIED"
    elif label_counts["DEMAND-CARRIED"] / n >= CELL_BAR:
        verdict = "DEMAND-CARRIED"
    else:
        verdict = "MIXED"
    plurality = max(LABEL_ORDER,
                    key=lambda lab: (label_counts[lab], -LABEL_ORDER.index(lab)))

    panel = {
        "experiment": EXPERIMENT,
        "label": LABEL,
        "verdict": verdict,
        "closing_cells": n,
        "falsifier_min_cells": N_MIN,
        "cell_label_counts": label_counts,
        "plurality_label": plurality,
        "anchor": anchor,
        "exclusions": {
            "counts": {reason: sum(1 for e in excluded if e["reason"] == reason)
                       for reason in ("RIGHT_CENSORED_STILL_BINDING",
                                      "NEVER_BOUND_3_YEARS")},
            "cells": excluded,
        },
        "cohort_branch_cells": cohort_branch_cells,
        "branch_switch_cells": branch_switch_cells,
        "efficiency_max_abs_residual": max_eff_resid,
        "s3_identity_cells": s3_cells,
        "s3_identity_max_abs_residual": s3_max_resid,
        "s4_closure_definition_counts": {
            "open_bar_1e-9": closure_count(cells, 1e-9, False),
            "consecutive_3": closure_count(cells, 1e-12, True),
            "primary": n,
        },
        "inputs": {"panel_sha256": PANEL_SHA256, "predecl_sha256": PREDECL_SHA256},
    }

    OUTDIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTDIR / "FLOOR_CLOSE_RESULTS.csv", RESULTS_HEADER, results_rows)
    write_csv(OUTDIR / "FLOOR_CLOSE_SHAPLEY.csv", SHAPLEY_HEADER, shapley_rows)
    write_csv(OUTDIR / "FLOOR_CLOSE_DETAIL.csv", DETAIL_HEADER, detail_rows)
    write_csv(OUTDIR / "FLOOR_CLOSE_SENSITIVITY.csv", SENS_HEADER, sens_rows)
    with open(OUTDIR / "FLOOR_CLOSE_PANEL.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(panel, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"{EXPERIMENT}: N={n} verdict={verdict} "
          f"A/P/Q/MIXED={label_counts['ALLOWANCE-CARRIED']}/"
          f"{label_counts['CAPACITY-CARRIED']}/{label_counts['DEMAND-CARRIED']}/"
          f"{label_counts['MIXED']} max|eff_resid|={max_eff_resid:.3e}")
    print("anchor: year={year_close} seat_coverage={seat_coverage_close:.6f} "
          "shares A/P/Q={share_allowance:.4f}/{share_places:.4f}/{share_demand:.4f} "
          "label={cell_label}".format(**anchor))
    print(f"wrote {OUTDIR.relative_to(PROGRAMME_ROOT)}")


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
