#!/usr/bin/env bash
# =============================================================================
# Proof that the corrected harness propagates job failure (P0-07 acceptance test)
# =============================================================================
# Runs two CPU-only dry-runs (tiny n, no CUDA, no torch):
#   1. control: two stub jobs that succeed                  -> overall exit 0
#   2. failure: success, then deliberate exit-7 job, then a
#      sentinel job that must never run                     -> overall exit 7
# It also runs a faithful reduction of the ARCHIVED runner pattern with the same
# failing job, showing that the old harness exits 0 and prints DONE anyway.
#
# Evidence is written to evidence/dry_run_evidence.json (atomic) and the script
# exits 0 only if every assertion passes.
# =============================================================================
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PYTHON=${PYTHON:-python3}
EVID="$HERE/evidence"
RUNS="$EVID/dry_runs"
HARNESS="$HERE/run_gpu_jobs_fixed.sh"
TS=$(date -u +%Y%m%dT%H%M%SZ)
CONTROL_ID="dryrun-control-$TS"
FAILURE_ID="dryrun-failure-$TS"
DEMO_DIR="$EVID/archived_demo-$TS"

mkdir -p "$EVID" "$RUNS" "$DEMO_DIR"
log() { printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*"; }

log "case 1/3: archived-pattern defect demonstration (expect overall rc 0 + DONE)"
set +e
PYTHON="$PYTHON" bash "$HERE/tools/archived_pattern_demo.sh" "$DEMO_DIR" > "$DEMO_DIR/stdout.log" 2>&1
DEMO_RC=$?
set -e
DEMO_SAW_EXIT7=$(grep -c 'JOB job_fail EXIT 7' "$DEMO_DIR/stdout.log" || true)
DEMO_SAW_DONE=$(grep -c '===== DONE =====' "$DEMO_DIR/stdout.log" || true)
log "  archived-pattern rc=$DEMO_RC (defect: 0 despite failing job; EXIT7 lines=$DEMO_SAW_EXIT7)"

log "case 2/3: corrected harness, all-succeed control (expect rc 0)"
set +e
"$HARNESS" --mode dry-run --jobs control --run-id "$CONTROL_ID" --runs-dir "$RUNS" --python "$PYTHON" \
  > "$EVID/control_stdout.log" 2>&1
CONTROL_RC=$?
set -e
log "  control rc=$CONTROL_RC"

log "case 3/3: corrected harness with deliberate failure (expect rc 7)"
set +e
"$HARNESS" --mode dry-run --jobs failure --run-id "$FAILURE_ID" --runs-dir "$RUNS" --python "$PYTHON" \
  > "$EVID/failure_stdout.log" 2>&1
FAILURE_RC=$?
set -e
log "  failure rc=$FAILURE_RC"

CTRL_DIR="$RUNS/$CONTROL_ID"
FAIL_DIR="$RUNS/$FAILURE_ID"

# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------
"$PYTHON" - "$HERE" "$EVID" "$CTRL_DIR" "$FAIL_DIR" "$CONTROL_RC" "$FAILURE_RC" \
  "$DEMO_DIR" "$DEMO_RC" "$DEMO_SAW_EXIT7" "$DEMO_SAW_DONE" "$CONTROL_ID" "$FAILURE_ID" "$PYTHON" <<'PY'
import hashlib, json, os, subprocess, sys, time

(here, evid, ctrl_dir, fail_dir, control_rc, failure_rc, demo_dir, demo_rc,
 demo_exit7, demo_done, control_id, failure_id, python) = sys.argv[1:]
control_rc, failure_rc, demo_rc = int(control_rc), int(failure_rc), int(demo_rc)
demo_exit7, demo_done = int(demo_exit7), int(demo_done)

def jload(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

ctrl_manifest_p = os.path.join(ctrl_dir, "manifest.json")
fail_manifest_p = os.path.join(fail_dir, "manifest.json")
fail_marker_p = os.path.join(fail_dir, "run_failure.json")
fail_job_dir = os.path.join(fail_dir, "jobs", "dryrun_stub_fail")
sentinel_dir = os.path.join(fail_dir, "jobs", "dryrun_stub_ok_b_must_not_run")

ctrl_manifest = jload(ctrl_manifest_p) if os.path.isfile(ctrl_manifest_p) else None
fail_marker = jload(fail_marker_p) if os.path.isfile(fail_marker_p) else None

ctrl_outputs = {}
if ctrl_manifest:
    for j in ctrl_manifest.get("jobs", []):
        p = os.path.join(ctrl_dir, "jobs", j["job_id"], j["output"])
        ctrl_outputs[j["job_id"]] = {
            "exists": os.path.isfile(p),
            "sha256": sha(p) if os.path.isfile(p) else None,
            "manifest_sha256": j.get("output_sha256"),
        }

fail_partials = []
for root, dirs, files in os.walk(fail_job_dir):
    for f in files:
        if f.endswith(".tmp") or ".tmp." in f or f.endswith(".partial"):
            fail_partials.append(os.path.join(root, f))

A = {
    # --- defect reproduced on the archived pattern ---
    "archived_pattern_overall_exit_is_0_despite_failing_job": demo_rc == 0,
    "archived_pattern_echoes_exit_7": demo_exit7 >= 1,
    "archived_pattern_prints_DONE_anyway": demo_done >= 1,
    # --- corrected harness: control ---
    "control_exit_0": control_rc == 0,
    "control_manifest_assembled": ctrl_manifest is not None and ctrl_manifest.get("status") == "ok",
    "control_all_jobs_exit_0": bool(ctrl_manifest) and ctrl_manifest.get("jobs_failed") == 0 and ctrl_manifest.get("jobs_attempted") == 2,
    "control_outputs_exist_and_match_manifest": all(
        v["exists"] and v["sha256"] == v["manifest_sha256"] for v in ctrl_outputs.values()
    ) and len(ctrl_outputs) == 2,
    "control_bundle_unchanged": bool(ctrl_manifest) and ctrl_manifest.get("bundle_unchanged_during_run") is True,
    # --- corrected harness: failure propagation ---
    "failure_overall_exit_nonzero": failure_rc != 0,
    "failure_overall_exit_equals_failing_job_rc_7": failure_rc == 7,
    "failure_marker_written": fail_marker is not None,
    "failure_marker_records_job_and_rc": bool(fail_marker) and fail_marker.get("failed_job") == "dryrun_stub_fail" and fail_marker.get("exit_code") == 7,
    "no_manifest_assembled_on_failure": not os.path.isfile(fail_manifest_p),
    "failing_job_left_no_result_json": not os.path.isfile(os.path.join(fail_job_dir, "result.json")),
    "failing_job_staging_removed": not os.path.isdir(os.path.join(fail_job_dir, ".staging")),
    "failing_job_no_partial_files_remain": len(fail_partials) == 0,
    "sentinel_job_never_ran": not os.path.isdir(sentinel_dir),
    "sentinel_job_has_no_manifest_record": not os.path.isfile(os.path.join(fail_dir, "manifest.jsonl")) or (
        "dryrun_stub_ok_b_must_not_run" not in open(os.path.join(fail_dir, "manifest.jsonl"), encoding="utf-8").read()
    ),
}

payload = {
    "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "purpose": "P0-07 acceptance: a failing job aborts the corrected harness with a non-zero overall exit; the archived pattern does not.",
    "python": python,
    "cases": {
        "archived_pattern_demo": {
            "run_dir": os.path.abspath(demo_dir),
            "overall_exit_code": demo_rc,
            "stdout_log": os.path.abspath(os.path.join(demo_dir, "stdout.log")),
        },
        "control": {
            "run_id": control_id,
            "run_dir": os.path.abspath(ctrl_dir),
            "overall_exit_code": control_rc,
            "manifest": os.path.abspath(ctrl_manifest_p),
            "manifest_sha256": sha(ctrl_manifest_p) if os.path.isfile(ctrl_manifest_p) else None,
        },
        "failure": {
            "run_id": failure_id,
            "run_dir": os.path.abspath(fail_dir),
            "overall_exit_code": failure_rc,
            "run_failure": os.path.abspath(fail_marker_p),
            "run_failure_sha256": sha(fail_marker_p) if os.path.isfile(fail_marker_p) else None,
        },
    },
    "assertions": A,
    "passed": all(A.values()),
    "failed_assertions": sorted(k for k, v in A.items() if not v),
}
out = os.path.join(evid, "dry_run_evidence.json")
tmp = f"{out}.tmp.{os.getpid()}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, sort_keys=True); f.write("\n"); f.flush(); os.fsync(f.fileno())
os.replace(tmp, out)

print("\n=== ASSERTIONS ===")
for k in sorted(A):
    print(f"  [{'PASS' if A[k] else 'FAIL'}] {k}")
print(f"\nEvidence: {out}")
if not payload["passed"]:
    print("RESULT: FAIL", file=sys.stderr)
    sys.exit(1)
print("RESULT: PASS — corrected harness aborts with rc 7; archived pattern exits 0 and prints DONE ")
PY
