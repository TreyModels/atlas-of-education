"""Run the Cluster B toy battery: exp4, exp5, exp6.

Usage:
    python3 code/run_all.py            # full run, writes RESULTS.csv + RUN_MANIFEST.json
    python3 code/run_all.py --smoke    # 3 seeds, structural checks only

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
Every arm in every seed shares the same latent draw. Seeds are SEED_BASE + rep.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import toy_common as tc
import exp4_visibility as e4
import exp5_queue as e5
import exp6_eligibility as e6
import verdicts as vd

HERE = os.path.dirname(os.path.abspath(__file__))
CLUSTER = os.path.dirname(HERE)
ARCHIVE = os.path.dirname(os.path.dirname(CLUSTER))
SPEC = os.path.join(ARCHIVE, "codex_2026-11-20", "COUNCIL_TOY_SPECS_015.md")
BASE_MODEL_DIR = "/tmp/codex_unpack/codex-massification-5eec11470690/workspace"

PARAMETERS = {
    "common": {
        "population": tc.POPULATION,
        "jobs": tc.JOBS,
        "public_seats": tc.PUBLIC_SEATS,
        "public_fee": tc.PUBLIC_FEE,
        "private_capacity": tc.PRIVATE_CAPACITY,
        "private_fixed_cost": tc.PRIVATE_FIXED_COST,
        "private_seat_cost": tc.PRIVATE_SEAT_COST,
        "tuition": tc.TUITION,
        "gross_premium": tc.GROSS_PREMIUM,
        "opportunity_cost_scale": tc.COST_SCALE,
        "budgets": "1.5 / 4.0 alternating, not shuffled (as model.py)",
        "seed_base": tc.SEED_BASE,
        "seeds_per_cell": tc.REPS,
        "pairing": "identical latent draws (skill, costs, lottery) across all arms of a seed",
    },
    "exp4": {
        "mechanisms": list(e4.MECHANISMS),
        "visibility_levels": list(e4.VISIBILITIES),
        "hc_skill_increment": 1.0,
        "signaling_premium": "4.0 * (1 - visibility)",
        "hc_premium": "4.0 (constant in visibility)",
        "employer_score": "visibility*true_skill + (1-visibility)*credential",
        "hires": 40,
        "metrics": e4.METRICS,
    },
    "exp5": {
        "older_diploma_group": "indices 0..19 (20 people, fixed membership)",
        "treated_group": "indices 20..39 (20 young people, fixed, paired across arms)",
        "young_group": "indices 20..99 (80 people)",
        "jobs_fixed": "J0 ~ Uniform{35,36,37,38,39,40}, one draw per seed shared by fixed arms",
        "jobs_responsive": "J = 100 (full absorption; the pool responds to the queue)",
        "skill_upgrade": "+1.0 true skill on treated group only",
        "rank_upgrade": "treated group hired first (lottery order), then other young by skill, then older group by skill; no skill change",
        "reference": "no treatment; hire by true skill",
        "metrics": e5.METRICS,
    },
    "exp6": {
        "offers": e6.J_OFFERS,
        "population": tc.POPULATION,
        "credential_shares": list(e6.CRED_SHARES),
        "credential_skill_correlation": 0.0,
        "gate_retained": "only credentialed applicants eligible",
        "gate_repealed": "all applicants eligible",
        "ranking_visible": "credentialed first, then true skill",
        "ranking_blind": "true skill only",
        "metrics": e6.METRICS,
    },
}

ARMS = {"exp4": [a[2] for a in e4.arms()],
        "exp5": [a[2] for a in e5.arms()],
        "exp6": [a[3] for a in e6.arms()]}

THRESHOLD_IDS = {
    "exp4": ["T4.1", "T4.2", "T4.3", "F4"],
    "exp5": ["T5.1", "T5.2", "T5.3", "T5.4", "D5.5", "D5.6"],
    "exp6": ["T6.1", "T6.2", "T6.3", "T6.4", "F6"],
}


def sha256_16(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def validate(seed):
    """Structural invariants only (counts/accounting); no outcome-based tuning."""
    # exp4: market accounting, and exact reproduction of model.py at seed 41, v=0.
    for mech in e4.MECHANISMS:
        for vis in e4.VISIBILITIES:
            r = e4.cell(mech, vis, seed)
            assert r["public_admissions"] + r["private_admissions"] == r["admissions"]
            assert r["admissions"] <= r["applications"]
            assert r["graduate_hires"] <= min(tc.JOBS, r["admissions"])
            assert r["rejected_count"] == r["applications"] - r["applicant_hires"]
            assert 0 <= r["applicant_hires"] <= min(tc.JOBS, r["applications"])
    ref = e4.cell("signaling", 0.0, 41)
    assert ref["applications"] == 89 and ref["public_admissions"] == 30
    assert ref["private_admissions"] == 15 and ref["admissions"] == 45
    assert ref["graduate_hires"] == 40, ref
    hc1 = e4.cell("human_capital", 1.0, 41)
    assert hc1["admissions"] == 45 and hc1["graduate_hires"] == 40
    assert e4.cell("signaling", 1.0, 41)["applications"] == 0
    # exp4: at v=0 the two mechanisms are identical in the market, not just in means.
    for s in (seed, seed + 1, seed + 2):
        a, b = e4.cell("human_capital", 0.0, s), e4.cell("signaling", 0.0, s)
        for k in ("applications", "admissions", "graduate_hires", "rejected_count"):
            assert a[k] == b[k], (k, a[k], b[k])

    # exp5: hires are bounded by the job count; responsive absorbs everyone.
    for treatment in ("skill_upgrade", "rank_upgrade", "reference"):
        for regime in ("fixed_jobs", "responsive_jobs"):
            r = e5.cell(treatment, regime, seed)
            assert r["total_hires"] <= tc.POPULATION
            assert 0 <= r["older_group_hires"] <= len(e5.OLDER)
            if regime == "responsive_jobs":
                assert r["total_hires"] == tc.POPULATION
            else:
                assert 35 <= r["total_hires"] <= 40, r
    # exp5 paired starting conditions: no treatment means identical skills.
    b1 = e5.cell("reference", "fixed_jobs", seed)
    b2 = e5.cell("rank_upgrade", "fixed_jobs", seed)
    assert b1["population_mean_skill"] == b2["population_mean_skill"]

    # exp6: staged screening accounting.
    for c in e6.CRED_SHARES:
        for vis in (True, False):
            for gate in (True, False):
                r = e6.cell(c, vis, gate, seed)
                assert r["total_offers"] == min(e6.J_OFFERS, r["eligible_count"])
                assert r["uncred_offers"] + r["cred_offers"] == r["total_offers"]
                assert r["vacancies"] == e6.J_OFFERS - r["total_offers"]
                if not gate:      # gate retained: uncredentialed are screened out
                    assert r["uncred_offers"] == 0
                    assert r["eligible_count"] == c
                else:             # gate repealed: everyone eligible
                    assert r["eligible_count"] == tc.POPULATION


def run_full(seeds):
    rows = []
    rows += e4.run(seeds)
    rows += e5.run(seeds)
    rows += e6.run(seeds)
    return rows


def write_manifest(summary, rows, results_path, seeds):
    verdicts, failures = {}, []
    for exp, payload in summary.items():
        for v in payload.get("verdicts", []) + payload.get("diagnostics", []):
            verdicts[v["id"]] = v["status"]
            if v["status"] == "NOT MET":
                failures.append({"id": v["id"], "statement": v["statement"]})
        f = payload.get("falsifier")
        if f:
            verdicts.setdefault("falsifier", f["status"])
    code_files = {}
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".py"):
            code_files[name] = {"sha256_16": sha256_16(os.path.join(HERE, name))}
    payload = {
        "label": tc.LABEL,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy_used": False,
        "spec": {"path": SPEC, "sha256_16": sha256_16(SPEC)},
        "base_model": {
            "model_py": {"path": os.path.join(BASE_MODEL_DIR, "model.py"),
                         "sha256_16": sha256_16(os.path.join(BASE_MODEL_DIR, "model.py"))},
            "experiments_py": {"path": os.path.join(BASE_MODEL_DIR, "experiments.py"),
                               "sha256_16": sha256_16(os.path.join(BASE_MODEL_DIR, "experiments.py"))},
        },
        "predeclarations": {"path": os.path.join(CLUSTER, "PRE_DECLARATIONS.md"),
                            "sha256_16": sha256_16(os.path.join(CLUSTER, "PRE_DECLARATIONS.md"))},
        "protocol": {
            "seeds_per_cell": len(seeds),
            "seed_base": seeds[0],
            "seed_list": "SEED_BASE + rep for rep in range(N)",
            "pairing": "identical latent draws across arms within a seed",
            "one_factor": "only the named arm factor changes between cells",
            "all_cells_reported": True,
            "reproduce": "python3 code/run_all.py  (stdlib Python only; deterministic)",
        },
        "parameters": PARAMETERS,
        "arms": ARMS,
        "threshold_ids": THRESHOLD_IDS,
        "verdict_summary": verdicts,
        "failures": failures,
        "results_csv": {"path": results_path, "rows": len(rows),
                        "sha256_16": sha256_16(results_path),
                        "schema": ["experiment", "arm", "seed", "metric", "value"],
                        "line_1": "# " + tc.LABEL},
        "code": code_files,
    }
    path = os.path.join(CLUSTER, "RUN_MANIFEST.json")
    tc.write_json(path, payload)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        for s in tc.seeds(3):
            validate(s)
        print("smoke: structural invariants OK (counts/accounting only, no means printed)")
        return
    seeds = tc.seeds()
    for seed in seeds[:5] + [41]:
        validate(seed)
    rows = run_full(seeds)
    results_path = os.path.join(CLUSTER, "RESULTS.csv")
    tc.write_results(results_path, rows)
    summary = vd.evaluate(rows, seeds)
    tc.write_json(os.path.join(HERE, "summary.json"), summary)
    manifest = write_manifest(summary, rows, results_path, seeds)
    print(f"wrote {results_path} ({len(rows)} rows)")
    print(f"wrote {os.path.join(HERE, 'summary.json')}")
    print(f"wrote {manifest}")
    for exp, payload in summary.items():
        print(f"\n== {exp}  [{payload['label']}]")
        for v in payload.get("verdicts", []) + payload.get("diagnostics", []):
            print(f"  {v['id']}: {v['status']} — {v['statement']}")
        if payload.get("falsifier"):
            print(f"  falsifier: {payload['falsifier']['status']}")


if __name__ == "__main__":
    main()
