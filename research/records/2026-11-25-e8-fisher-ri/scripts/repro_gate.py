#!/usr/bin/env python3
"""E8 Fisher RI — REPRODUCTION GATE (mandatory, before any permutation run).

Gate (pre-registered in PRE_REGISTRATION.md §4):
  1. The committed panel data/e8_primary_ger_panel.csv is exactly (0.0 difference) the long panel
     parsed from the same raw WDI bulk csv by data/acquire_wdi.py::build_long_panel().
  2. The cited estimator `att_cs` (and `boot_rep` for the SE) from
     research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py @ bd782be,
     called on that panel with the E8 main-specification sample and verified-8 dates, reproduces:
       - ATT(e=0) = 12.44362392207772 within 1e-6,
       - all 11 event-time ATTs (e=-5..+6) within 1e-6 of the committed
         results/e8_event_SE.PRM.ENRR_verified8.csv @ bd782be,
       - SE_boot(e=0) = 7.550738928931049 within 1e-6 (same seeds 1000+i, i=0..499, Pool(8)).

The cited script is executed from an import of a byte-identical temporary copy (its module-level
HERE/DATA/RES then point into the temporary directory), so no file of the cited record is modified.

Exit code 0 = gate PASS; 1 = gate FAIL (the record must then stop and report the failure).

Run:  /Users/treymenefee/neon-boot/venv/bin/python scripts/repro_gate.py
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.dirname(HERE)                                   # .../2026-11-25-e8-fisher-ri
BASE = os.path.abspath(os.path.join(RECORD, "..", "2026-11-25-e6e8-sequencing"))
WORKTREE = os.path.abspath(os.path.join(RECORD, "..", "..", ".."))
CITED_COMMIT = "bd782be4d15c834f054b1ecc650e54565f6b292f"
CITED_REL = "research/records/2026-11-25-e6e8-sequencing/scripts/e8_fee_event_study.py"
OUT = os.path.join(RECORD, "results", "repro_gate.json")
TOL = 1e-6
YEARS = list(range(1990, 2016))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", WORKTREE] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def load_cited_module():
    """Import a byte-identical temp copy of the bd782be script (no writes into the cited record)."""
    src = os.path.join(WORKTREE, CITED_REL)
    tmp = tempfile.mkdtemp(prefix="e8_gate_")
    os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
    dst = os.path.join(tmp, "scripts", "e8_fee_event_study.py")
    shutil.copyfile(src, dst)
    spec = importlib.util.spec_from_file_location("e8_base_bd782be", dst)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["e8_base_bd782be"] = mod   # so the cited functions pickle by reference
    spec.loader.exec_module(mod)
    return mod, src, dst


def build_Y(panel, region):
    ssa = set(region.loc[region.Region.fillna("").str.contains("Sub-Saharan"), "iso3"])
    countries = set(panel.iso3) & ssa
    Y = {}
    for iso, g in panel.groupby("iso3"):
        if iso in countries:
            Y[iso] = dict(zip(g.year.astype(int), g.value.astype(float)))
    return Y, sorted(countries), sorted(ssa)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    res = {"gate": "E8 RI reproduction gate", "cited_commit": CITED_COMMIT,
           "cited_script_relpath": CITED_REL, "tolerance": TOL,
           "command": "/Users/treymenefee/neon-boot/venv/bin/python scripts/repro_gate.py"}
    # provenance of the cited script
    cited_path = os.path.join(WORKTREE, CITED_REL)
    res["cited_script_sha256"] = sha256_file(cited_path)
    res["cited_script_worktree_blob"] = git("hash-object", CITED_REL)
    res["cited_script_commit_blob"] = git("rev-parse", f"{CITED_COMMIT}:{CITED_REL}")
    res["cited_script_matches_cited_commit"] = (res["cited_script_worktree_blob"] == res["cited_script_commit_blob"])
    res["git_head"] = git("rev-parse", "HEAD")

    # ---- check 1: committed panel == freshly parsed raw panel ----
    sys.path.insert(0, os.path.join(RECORD, "data"))
    import acquire_wdi as acq
    panel_committed = pd.read_csv(acq.PANEL)
    panel_raw = acq.build_long_panel()
    same_shape = panel_committed.shape == panel_raw.shape
    merged = panel_committed.merge(panel_raw, on=["iso3", "year"], how="outer", suffixes=("_c", "_r"), indicator=True)
    panel_maxdiff = float(np.nanmax(np.abs(merged.value_c.values - merged.value_r.values))) if len(merged) else float("inf")
    panel_exact = bool(same_shape and (merged._merge == "both").all() and panel_maxdiff == 0.0)
    wdi_updated = acq.wdi_last_updated()
    panel_check = {"committed_rows": int(len(panel_committed)), "raw_rows": int(len(panel_raw)),
                   "countries": int(panel_committed.iso3.nunique()), "years": [int(panel_committed.year.min()),
                   int(panel_committed.year.max())], "merged_rows": int(len(merged)),
                   "max_abs_diff": panel_maxdiff, "exact_match": panel_exact,
                   "wdi_last_updated_date": wdi_updated,
                   "committed_sha256": sha256_file(acq.PANEL)}
    res["panel_check"] = panel_check

    # ---- check 2: cited estimator reproduces the committed E8 verified-8 event study ----
    reg = pd.read_csv(acq.REGION)
    Y, sample_countries, ssa = build_Y(panel_committed, reg)
    fee = pd.read_csv(os.path.join(BASE, "data", "fee_dates.csv"))
    ver = fee[fee.status == "VERIFIED"].copy()
    coh_all = dict(zip(ver.iso3, ver.preferred_year.astype(int)))
    coh = {c: g for c, g in coh_all.items() if c in Y}
    res["sample"] = {"ssa_countries_in_region_map": len(ssa), "ssa_countries_with_panel": len(sample_countries),
                     "treated_with_panel": len(coh), "treated": coh, "controls_pool_size": len(sample_countries) - len(coh)}

    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    mod, src, tmpcopy = load_cited_module()
    att_gt, ev = mod.att_cs(Y, coh, YEARS)
    ctx = mp.get_context("fork")            # fork inherits the imported cited module (macOS-safe here)
    with ctx.Pool(8) as pool:
        boots = pool.map(mod.boot_rep, [(Y, coh, YEARS, 1000 + i) for i in range(500)])
    bdf = pd.DataFrame(boots)
    ev["se_boot"] = [float(np.std(bdf[e].dropna())) if e in bdf.columns and len(bdf[e].dropna()) else np.nan
                     for e in ev.event]

    committed_event = pd.read_csv(os.path.join(BASE, "results", "e8_event_SE.PRM.ENRR_verified8.csv"))
    committed_attgt = pd.read_csv(os.path.join(BASE, "results", "e8_att_gt_SE.PRM.ENRR_verified8.csv"))
    evm = ev.merge(committed_event[["event", "att", "n", "n_treated", "n_controls", "se_boot"]],
                   on="event", how="outer", suffixes=("", "_committed"), indicator=True)
    evm = evm.sort_values("event").reset_index(drop=True)
    d_att = float(np.nanmax(np.abs(evm.att.values - evm.att_committed.values)))
    d_se = float(np.nanmax(np.abs(evm.se_boot.values - evm.se_boot_committed.values)))
    d_n = float(np.nanmax(np.abs(evm.n.values - evm.n_committed.values)))
    d_nt = float(np.nanmax(np.abs(evm.n_treated.values - evm.n_treated_committed.values)))
    d_nc = float(np.nanmax(np.abs(evm.n_controls.values - evm.n_controls_committed.values)))
    # per-(g,t) ATT(g,t) rows as a second, stricter comparison
    agm = att_gt.merge(committed_attgt[["g", "t", "att", "n_controls"]], on=["g", "t"], how="outer",
                       suffixes=("", "_committed"), indicator=True)
    ag_maxdiff = float(np.nanmax(np.abs(agm.att.values - agm.att_committed.values))) if len(agm) else float("inf")
    ag_all_matched = bool(len(agm) == len(att_gt) and (agm._merge == "both").all())
    t0 = evm.loc[evm.event == 0].iloc[0]
    e0_repro, e0_committed = float(t0.att), float(t0.att_committed)
    se0_repro, se0_committed = float(t0.se_boot), float(t0.se_boot_committed)
    res["estimator_reproduction"] = {
        "n_events_reproduced": int(len(evm)),
        "event_rows": [{"event": int(r.event), "att_reproduced": float(r.att), "att_committed": float(r.att_committed),
                        "abs_diff": float(abs(r.att - r.att_committed)),
                        "se_boot_reproduced": float(r.se_boot), "se_boot_committed": float(r.se_boot_committed),
                        "abs_diff_se": float(abs(r.se_boot - r.se_boot_committed))}
                       for _, r in evm.iterrows()],
        "att0_reproduced": e0_repro, "att0_committed": e0_committed,
        "att0_absdiff": float(abs(e0_repro - e0_committed)),
        "se_boot0_reproduced": se0_repro, "se_boot0_committed": se0_committed,
        "se_boot0_absdiff": float(abs(se0_repro - se0_committed)),
        "max_abs_diff_att_11_events": d_att,
        "max_abs_diff_se_boot_11_events": d_se,
        "max_abs_diff_n": d_n, "max_abs_diff_n_treated": d_nt, "max_abs_diff_n_controls": d_nc,
        "att_gt_max_abs_diff": ag_maxdiff, "att_gt_all_rows_matched": ag_all_matched,
        "n_treated_e0": float(t0.n_treated_committed), "n_controls_e0": float(t0.n_controls_committed),
    }
    checks = {
        "cited_script_matches_cited_commit": res["cited_script_matches_cited_commit"],
        "panel_exact_match": panel_exact,
        "att0_within_tol": abs(e0_repro - 12.44362392207772) <= TOL,
        "all_11_event_atts_within_tol": d_att <= TOL,
        "se_boot0_within_tol": abs(se0_repro - 7.550738928931049) <= TOL,
        "att_gt_rows_all_matched": ag_all_matched and ag_maxdiff <= TOL,
    }
    res["checks"] = checks
    res["gate_pass"] = bool(all(checks.values()))
    res["failure_reasons"] = [k for k, v in checks.items() if not v]
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: res[k] for k in ["gate_pass", "checks", "failure_reasons"]}, indent=1))
    print(f"ATT(0) reproduced = {e0_repro:.12f} (committed {e0_committed:.12f}); "
          f"SE_boot(0) = {se0_repro:.12f} (committed {se0_committed:.12f}); "
          f"max|dATT| 11 events = {d_att:.3e}; max|dSE| = {d_se:.3e}")
    print(f"wrote {OUT}")
    shutil.rmtree(tmpcopy.rsplit(os.sep, 2)[0], ignore_errors=True)
    if not res["gate_pass"]:
        print("REPRODUCTION GATE FAILED — STOP, no permutations.")
        return 1
    print("REPRODUCTION GATE PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
