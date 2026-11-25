#!/usr/bin/env python3
"""Build docs/audit/CORRECTED_GPU_EXPERIMENT_MANIFEST.json (P0-07 deliverable).

Sources (all read-only):
  * fixed_harness/configs/jobs_real.json + per-job configs  -> experiment definitions
  * gpu_abc_bundle/MANIFEST.sha256 + bundle_verification*.json -> integrity record
  * fixed_harness/evidence/dry_run_evidence.json           -> host harness proof
  * fixed_harness/evidence/box_execution/box_run_meta.json -> box harness proof
  * archived RUN_REPORT.md facts are embedded below with their provenance.

Writes the deliverable atomically (tmp + os.replace).

Usage:
    build_corrected_manifest.py --audit-dir docs/audit --out docs/audit/CORRECTED_GPU_EXPERIMENT_MANIFEST.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
BUNDLE = os.path.join(os.path.dirname(HARNESS), "gpu_abc_bundle")

# ---- archived-run facts (from gpu_abc_bundle/RUN_REPORT.md; evidence_status AUTHOR-REPORTED) ----
ARCHIVED_EXIT_OK_NOTE = ("archived runner echoed EXIT 0 per job; it could not fail-fast, so this value is "
                         "AUTHOR-REPORTED, not execution-verified")
ARCHIVED = {
    "job2_bray_abc_7param": {
        "archived_output_file": "results_bray_abc_7param.json",
        "archived_output_sha256": "79ceddbf409934b92b29f839931a19e61f30b4ef7b42c2f9ed652e110f4979f7",
        "archived_exit_code": 0, "archived_wall_time_sec": 2.73, "worker_count": 1,
        "archived_log_line": "[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)",
    },
    "job2b_bray_abc_6param": {
        "archived_output_file": "results_bray_abc_6param.json",
        "archived_output_sha256": "3d1027b41c0ac6647eebb272961532d20e9507141006aa1c250e411a1e9c5d09",
        "archived_exit_code": 0, "archived_wall_time_sec": None,
        "archived_log_line": "[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)",
        "wall_time_note": "whole-script wall not recorded in RUN_REPORT; ABC internal elapsed 0.30 s, surface 0.036 s",
    },
    "job1_e1_q3_selftest_gpu": {
        "archived_output_file": "results_e1_q3_selftest.json",
        "archived_output_sha256": "9dc07b4493a45f67ece8c68eca864b98d51548299030fd962b337913208a158e",
        "archived_exit_code": 0, "archived_wall_time_sec": 3.59, "worker_count": 1,
        "archived_log_line": "[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)",
    },
    "job1_e1_q3_cpu_ref": {
        "archived_output_file": "results_e1_q3_selftest_cpu_ref.json",
        "archived_output_sha256": "1b325e9d36e56cd1ee5e5e3a879fe28aaaf68c96c374382d78979b05adf276ca",
        "archived_exit_code": 0, "archived_wall_time_sec": 2.41, "worker_count": 1,
        "archived_log_line": "[CPU] CUDA not available; falling back to CPU",
    },
    "job1_gpu_vs_cpu_diff": {
        "archived_output_file": "results_gpu_vs_cpu_diff.json",
        "archived_output_sha256": "08fbc5c9920ba0afe91b5c55e151eae1608152f90058f19172c7508b5dce0e7a",
        "archived_exit_code": None, "archived_wall_time_sec": None, "worker_count": None,
        "archived_log_line": None,
        "derived": True,
        "note": "derived comparison artifact, not a runner job (the archived runner has no diff step)",
    },
}

CONFIG_FILES = {
    "job2_bray_abc_7param": "job2_abc_7param.json",
    "job2b_bray_abc_6param": "job2b_abc_6param.json",
    "job1_e1_q3_selftest_gpu": "job1_e1q3_gpu.json",
    "job1_e1_q3_cpu_ref": "job1_e1q3_cpu_ref.json",
    "job1_gpu_vs_cpu_diff": "job1_gpu_vs_cpu_diff.json",
}

PART_B = [
    {"id": "job2_partB_contest_surface_7param", "parent": "job2_bray_abc_7param",
     "note": ("Part B of the same process: 2,000-point (r, price, seat-share) approximate Tullock surface. "
              "Paradox share saturates at 1.0/1.0; external audit P0-06 CONTRADICTS it as a general-r / "
              "engine-PL boundary map (solver is the r=1 FOC with r inserted as a multiplier).")},
    {"id": "job2_partB_contest_surface_6param", "parent": "job2b_bray_abc_6param",
     "note": "Part B unchanged in the 6-parameter variant; same P0-06 contradiction applies."},
]

ABSENT = [
    {"job_id": "job1_e1_q3_panel_mode", "script": "gpu_abc_bundle/gpu_e1_q3_wild_cluster_ri.py",
     "script_sha256": "3bbbc19ac42020b64a6d88c57118d75702c42dabddc0038f8ea087a6b2caf6c9",
     "config": None, "config_sha256": None, "seed": None, "command": None,
     "output": None, "output_sha256": None, "exit_code": None, "wall_time_sec": None, "worker_count": None,
     "evidence_status": "UNRESOLVED", "execution_state": "NOT_RUN",
     "notes": ("Advertised panel mode was never run: the E1/Q3 panel CSV does not exist in the repository "
               "(RUN_REPORT.md 'E1/Q3 full panel mode - MISSING'). Even with a CSV it would build X=[1,x] only, "
               "dropping controls/FE, so it is not an E1/Q3 reconstruction. Missing experiment => UNRESOLVED.")},
    {"job_id": "job2_100_fresh_seed_stability_bank", "script": "gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py",
     "script_sha256": "0709032c043372cafd79d1df4c62dd352403e881afc1fc395cb5956a19a15d2e",
     "config": "fixed_harness/configs/job2_abc_7param.json", "config_sha256": None,
     "seed": None, "command": None, "output": None, "output_sha256": None,
     "exit_code": None, "wall_time_sec": None, "worker_count": None,
     "evidence_status": "CONTRADICTED", "execution_state": "NOT_IMPLEMENTED",
     "notes": ("The as-shipped docstring advertises a '100-Fresh-Seed Stability Bank' (n_per_class in "
               "{70,300,700}); grep of the script finds no implementation and no output artifact. "
               "Claim CONTRADICTED (P0-07).")},
    {"job_id": "abc_accepted_draws_posterior", "script": "gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py",
     "script_sha256": "0709032c043372cafd79d1df4c62dd352403e881afc1fc395cb5956a19a15d2e",
     "config": "fixed_harness/configs/job2_abc_7param.json", "config_sha256": None,
     "seed": None, "command": None, "output": None, "output_sha256": None,
     "exit_code": None, "wall_time_sec": None, "worker_count": None,
     "evidence_status": "CONTRADICTED", "execution_state": "NOT_AVAILABLE",
     "notes": ("Accepted draws are discarded: only n_accepted / best_theta / posterior condition number are "
               "returned, so posterior diagnostics, predictive checks and uncertainty are impossible from the "
               "deposit (P0-07).")},
]

DEFECTS = [
    {"id": "EI-1", "finding": "Runner does not propagate job failure (no set -e / no pipefail; rc is only echoed).",
     "evidence": {"file": "gpu_abc_bundle/run_gpu_jobs.sh", "lines": "10-21"},
     "demonstrated": "evidence/archived_demo-*/stdout.log: overall exit 0 and DONE printed while a job printed EXIT 7",
     "status": "VERIFIED DEFECT", "fixed_by": "set -euo pipefail + explicit rc capture + fail-fast abort in run_gpu_jobs_fixed.sh"},
    {"id": "EI-2", "finding": "The 6-parameter run is absent from the archived runner, so the deposited 6-param output cannot be reproduced by it.",
     "evidence": {"file": "gpu_abc_bundle/run_gpu_jobs.sh", "lines": "18-20 (only 7-param ABC, GPU selftest, CPU ref)"},
     "status": "VERIFIED DEFECT", "fixed_by": "job2b_bray_abc_6param added as a first-class job"},
    {"id": "EI-3", "finding": "gpu_bray_abc_and_contest_surface_6param.py keeps the 7-param default --out-dir, so a default run overwrites the 7-param output.",
     "evidence": {"file": "gpu_abc_bundle/gpu_bray_abc_and_contest_surface_6param.py", "lines": "argparse default --out-dir ./results_rtx3080ti/bray_and_contest"},
     "status": "VERIFIED DEFECT", "fixed_by": "unique per-run/per-job directories; harness always injects --out-dir"},
    {"id": "EI-4", "finding": "Job JSON writes are non-atomic (plain open(...,'w')), so a crash can leave a truncated result.",
     "evidence": {"file": "gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py", "lines": "191-193 (and 235-237 in the E1/Q3 script)"},
     "status": "VERIFIED DEFECT", "fixed_by": "jobs write to a private staging dir; harness publishes the JSON with an atomic rename"},
    {"id": "EI-5", "finding": "Job configurations/parameters are not hashed or recorded with the outputs.",
     "evidence": {"file": "gpu_abc_bundle/run_gpu_jobs.sh", "lines": "10-21 (nothing about configs)"},
     "status": "VERIFIED DEFECT", "fixed_by": "configs/*.json hashed per job and per run (evidence/config_hashes.json + manifest)"},
    {"id": "EI-6", "finding": "A single fixed seed (20261125) is used with no provenance; validation runs are indistinguishable from replays.",
     "evidence": {"file": "gpu_abc_bundle/run_gpu_jobs.sh", "lines": "18-20 (no --seed passed; script defaults 20261125)"},
     "status": "VERIFIED DEFECT", "fixed_by": "independent OS-CSPRNG validation seeds per job, recorded + hashed; archived seed not reused"},
    {"id": "EI-7", "finding": "Accepted draws discarded and the advertised 100-Fresh-Seed Stability Bank is not implemented; no posterior/predictive diagnostics are producible from the deposit.",
     "evidence": {"file": "gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py", "lines": "103-120 (only aggregates returned), 4-8 (advertised bank)"},
     "status": "VERIFIED DEFECT", "fixed_by": "not fixable by harness alone: requires experiment-code changes; recorded as CONTRADICTED/NOT_IMPLEMENTED"},
]

RERUN = [
    {"experiment": "job2_bray_abc_7param", "precondition": "P0-01/P0-02 corrections: drop the dead theta[5]; advertise 4 independent moments; replace ABC identification claims with the analytic moment-rank audit. Do NOT report as a 7-parameter calibration."},
    {"experiment": "job2b_bray_abc_6param", "precondition": "P0-01/P0-02: 6 active parameters vs 4 independent moments is rank-deficient; needs additional micro-moments (contest-math ABC_IDENTIFICATION_AUDIT.md) before any calibration claim."},
    {"experiment": "job2_partB_contest_surface", "precondition": "P0-06: replace the r=1-FOC-with-r-multiplier solver by an independently derived general-r Tullock optimum with capacity clearing and convergence diagnostics; extend seat shares to universal admission."},
    {"experiment": "job1_e1_q3_selftest_gpu / cpu_ref / diff", "precondition": "P0-04/P0-05: replace the confounded DGP negative control with a factorial design; replace the within-invariant country-block permutation with a scheme justified for the FE estimand. The selftest remains arithmetic validation only."},
    {"experiment": "job1_e1_q3_panel_mode", "precondition": "Commit the E1/Q3 panel CSV + the actual FE/control specification; X=[1,x] is not the estimator."},
    {"experiment": "job2_100_fresh_seed_stability_bank", "precondition": "Implement it (currently contradicted), save accepted draws, add posterior/predictive outputs."},
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path, default=None):
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", default=os.path.dirname(HARNESS))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    audit_dir = os.path.abspath(args.audit_dir)

    jobs_cfg_path = os.path.join(HARNESS, "configs", "jobs_real.json")
    jobs_cfg = load_json(jobs_cfg_path)

    host_ev_path = os.path.join(HARNESS, "evidence", "dry_run_evidence.json")
    box_meta_path = os.path.join(HARNESS, "evidence", "box_execution", "box_run_meta.json")
    host_ev = load_json(host_ev_path, {})
    box_meta = load_json(box_meta_path, {})
    import glob
    _bv = sorted(glob.glob(os.path.join(HARNESS, "evidence", "dry_runs", "dryrun-control-*",
                                         "evidence", "bundle_verification_before.json")))
    bundle_ver = load_json(_bv[-1], {}) if _bv else {}
    box_manifest_lines = (box_meta or {}).get("manifest_check", [])

    experiments = []
    for job in jobs_cfg["jobs"]:
        jid = job["id"]
        cfg_name = CONFIG_FILES.get(jid)
        cfg_path = os.path.join(HARNESS, "configs", cfg_name) if cfg_name else None
        cfg_sha = sha256(cfg_path) if cfg_path and os.path.isfile(cfg_path) else None
        arch = ARCHIVED.get(jid, {})
        experiments.append({
            "job_id": jid,
            "script": job.get("script"),
            "script_sha256": job.get("script_sha256"),
            "config": ("docs/audit/fixed_harness/configs/" + cfg_name) if cfg_name else None,
            "config_sha256": cfg_sha,
            "seed": {"archived": 20261125,
                     "validation_policy": "independent OS-CSPRNG seed per run (archived seed not reused)"},
            "command": job.get("archived_command"),
            "output": arch.get("archived_output_file"),
            "output_sha256": arch.get("archived_output_sha256"),
            "exit_code": arch.get("archived_exit_code"),
            "exit_code_note": ARCHIVED_EXIT_OK_NOTE,
            "wall_time_sec": arch.get("archived_wall_time_sec"),
            "wall_time_note": arch.get("wall_time_note"),
            "worker_count": arch.get("worker_count", 1),
            "evidence_status": job.get("evidence_status"),
            "execution_state": "ARCHIVED_RUN_AUTHOR_REPORTED" if not arch.get("derived") else "DERIVED_ARTIFACT",
            "archived_log_line": arch.get("archived_log_line"),
            "known_defects": job.get("notes"),
            "corrected_harness_command": (
                "docs/audit/fixed_harness/run_gpu_jobs_fixed.sh --mode real --jobs real  "
                f"(job {jid}; unique run dir; independent seed; atomic output; fail-fast)"
            ),
            "rerun_precondition": next((r["precondition"] for r in RERUN if r["experiment"] == jid), None),
        })

    # Part B sub-experiments (same process as their parent ABC job)
    for pb in PART_B:
        parent = next(e for e in experiments if e["job_id"] == pb["parent"])
        experiments.append({
            "job_id": pb["id"],
            "script": parent["script"],
            "script_sha256": parent["script_sha256"],
            "config": parent["config"],
            "config_sha256": parent["config_sha256"],
            "seed": parent["seed"],
            "command": parent["command"],
            "output": parent["output"],
            "output_sha256": parent["output_sha256"],
            "exit_code": parent["exit_code"],
            "exit_code_note": parent["exit_code_note"],
            "wall_time_sec": 0.036,
            "wall_time_note": "internal elapsed_sec of Part B within the parent process; not a separate process",
            "worker_count": parent["worker_count"],
            "evidence_status": "AUTHOR-REPORTED",
            "execution_state": "ARCHIVED_RUN_AUTHOR_REPORTED",
            "notes": pb["note"],
            "corrected_harness_command": parent["corrected_harness_command"],
            "rerun_precondition": next(r["precondition"] for r in RERUN if r["experiment"] == "job2_partB_contest_surface"),
        })

    # fill config_sha256 for absent entries that name a config file
    for e in ABSENT:
        if e.get("config") and not e.get("config_sha256"):
            p = os.path.join(audit_dir, e["config"])
            e["config_sha256"] = sha256(p) if os.path.isfile(p) else None
    experiments.extend(ABSENT)

    manifest = {
        "deliverable": "P0-07 corrected GPU-experiment manifest",
        "task": "task-11 (Lead-rerouted P0-07 execution half)",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "generated_by": "audit-runner",
        "audit_reference": "docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md (P0-07 list is binding)",
        "audit_target": {
            "bundle_dir": "docs/audit/gpu_abc_bundle",
            "source_commit": "045a63e",
            "frozen": True,
            "manifest": "MANIFEST.sha256",
            "manifest_entries": 12,
            "manifest_verified": True,
            "manifest_verified_by": ["host (shasum -a 256 -c)", "box (sha256sum -c)"],
            "manifest_check_exit_code": 0,
            "bundle_dir_digest_sha256": "8d58e6ff750c8e512124f74474efd33ed71fe81c200f772e76c9539966f3cfbf",
            "unchanged_before_after_harness_runs": True,
            "git_status": "clean (docs/audit/gpu_abc_bundle not modified)",
            "box_manifest_check": box_manifest_lines,
        },
        "corrected_harness": {
            "dir": "docs/audit/fixed_harness",
            "main_script": "docs/audit/fixed_harness/run_gpu_jobs_fixed.sh",
            "main_script_sha256": sha256(os.path.join(HARNESS, "run_gpu_jobs_fixed.sh")),
            "acceptance_test": "docs/audit/fixed_harness/dry_run_failure_propagation.sh",
            "acceptance_test_sha256": sha256(os.path.join(HARNESS, "dry_run_failure_propagation.sh")),
            "manifest_verifier_sha256": sha256(os.path.join(HARNESS, "verify_bundle_manifest.sh")),
            "proof": {
                "host": {"evidence": "docs/audit/fixed_harness/evidence/dry_run_evidence.json",
                         "evidence_sha256": sha256(host_ev_path) if os.path.isfile(host_ev_path) else None,
                         "passed": host_ev.get("passed"),
                         "assertions_passed": sum(1 for v in host_ev.get("assertions", {}).values() if v),
                         "assertions_total": len(host_ev.get("assertions", {})),
                         "control_exit": host_ev.get("cases", {}).get("control", {}).get("overall_exit_code"),
                         "failure_exit": host_ev.get("cases", {}).get("failure", {}).get("overall_exit_code"),
                         "archived_pattern_exit": host_ev.get("cases", {}).get("archived_pattern_demo", {}).get("overall_exit_code")},
                "box": {"evidence": "docs/audit/fixed_harness/evidence/box_execution/box_run_meta.json",
                        "evidence_sha256": sha256(box_meta_path) if os.path.isfile(box_meta_path) else None,
                        "host": box_meta.get("host"), "python": box_meta.get("python"),
                        "numpy": box_meta.get("numpy"), "cgroup_cpu_max": box_meta.get("cgroup_cpu_max"),
                        "worker_allocation": box_meta.get("worker_allocation"),
                        "nice_level": box_meta.get("nice_level"),
                        "passed": (box_meta.get("evidence") or {}).get("passed"),
                        "assertions_passed": sum(1 for v in (box_meta.get("evidence") or {}).get("assertions", {}).values() if v),
                        "assertions_total": len((box_meta.get("evidence") or {}).get("assertions", {})),
                        "manifest_entries_ok": all("OK" in ln for ln in box_manifest_lines),
                        "bundle_dir_digest_sha256": box_meta.get("bundle_dir_digest_sha256")},
            },
            "real_mode_matrix_defined": True,
            "real_mode_executed": False,
            "real_mode_not_executed_reason": "CPU-only audit mandate; torch parked and no GPU campaign authorised. The harness is validated by CPU dry-run stubs, not by executing the GPU scripts.",
        },
        "execution_integrity_findings": DEFECTS,
        "experiments": experiments,
        "what_would_need_to_be_rerun": RERUN,
        "evidence_status_legend": {
            "VERIFIED EMPIRICAL": "directly observed/measured fact, not a simulation",
            "REPRODUCED SIMULATION": "simulation re-executed and reproduced in this audit",
            "VALIDATED SIMULATION": "numerically validated within a stated scope (arithmetic only for GPU-vs-CPU)",
            "AUTHOR-REPORTED": "supplied/recorded by the author; hash-verified but not re-executed",
            "CONTRADICTED": "positively contradicted by verified code/algebra/records",
            "UNRESOLVED": "evidence missing / experiment cannot be run from the deposit",
        },
        "quarantine": ("GPU bundles' scientific conclusions remain QUARANTINED (EXTERNAL_AUDIT_GPU_2026-11-25.md §2). "
                       "No manifest entry promotes a GPU claim beyond AUTHOR-REPORTED / CONTRADICTED / UNRESOLVED; "
                       "GPU-vs-CPU agreement is arithmetic validation only."),
        "sources": {
            "jobs_config": "docs/audit/fixed_harness/configs/jobs_real.json",
            "jobs_config_sha256": sha256(jobs_cfg_path),
            "bundle_manifest": "docs/audit/gpu_abc_bundle/MANIFEST.sha256",
            "bundle_manifest_sha256": sha256(os.path.join(BUNDLE, "MANIFEST.sha256")),
            "run_report": "docs/audit/gpu_abc_bundle/RUN_REPORT.md",
            "run_report_sha256": sha256(os.path.join(BUNDLE, "RUN_REPORT.md")),
        },
    }

    out = os.path.abspath(args.out)
    tmp = f"{out}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, out)
    print(f"wrote {out}: {len(experiments)} experiment entries "
          f"({len(ABSENT)} absent), {len(DEFECTS)} integrity findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
