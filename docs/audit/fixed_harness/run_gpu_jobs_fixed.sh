#!/usr/bin/env bash
# =============================================================================
# Corrected GPU-experiment harness — P0-07 execution-integrity remediation
# =============================================================================
# Audit target (read-only, never modified): docs/audit/gpu_abc_bundle/ @ 045a63e
#
# Defects in the archived runner (gpu_abc_bundle/run_gpu_jobs.sh) that this
# harness fixes:
#   1. `set -u` only; run() captures PIPESTATUS[0] but only *echoes* it — a failed
#      job does not stop the sequence and the run still prints DONE.
#      FIX: `set -euo pipefail` + explicit rc capture; ANY non-zero job aborts
#      the whole run with that exact non-zero exit code (fail-fast).
#   2. The 6-parameter run is absent from the archived runner.
#      FIX: job2b_bray_abc_6param is a first-class job.
#   3. gpu_bray_abc_and_contest_surface_6param.py keeps the 7-param default
#      --out-dir, so a default run would overwrite the 7-param output.
#      FIX: every job gets its own unique run/job directory; --out-dir is always
#      injected by the harness; outputs are moved into place with an atomic
#      rename only after success.
#   4. JSON writes are not atomic; a crash can leave a truncated result.
#      FIX: jobs write into a private staging dir; the harness renames the single
#      expected JSON into its final path atomically (tmp+rename discipline).
#   5. Configs/parameters are not hashed or recorded.
#      FIX: every config file's sha256 is recorded per job and in the run
#      manifest (evidence/config_hashes.json).
#   6. Seeds are a fixed archived constant with no provenance.
#      FIX: independent validation seeds from the OS CSPRNG (tools/make_seeds.py),
#      recorded and hashed; the archived seed 20261125 is not reused.
#   7. Runner cannot detect failure => the archived "DONE" is not evidence of
#      success.
#      FIX: run manifest is assembled only after every job succeeded; a failure
#      writes run_failure.json and leaves no manifest.json.
#
# Usage:
#   run_gpu_jobs_fixed.sh --mode dry-run --jobs control|failure [--runs-dir DIR]
#   run_gpu_jobs_fixed.sh --mode real --jobs real [--python /path/to/python]
# Options: --run-id ID --seed-mode independent|derived --seed N --bundle DIR -h
# Exit: 0 iff every job succeeded; otherwise the failing job's non-zero rc.
# =============================================================================
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
AUDIT_DIR=$(cd "$HERE/.." && pwd)
PYTHON=${PYTHON:-python3}
BUNDLE_DIR=${BUNDLE_DIR:-"$AUDIT_DIR/gpu_abc_bundle"}
RUNS_DIR=${RUNS_DIR:-"$HERE/runs"}
MODE=real
JOBSET=real
RUN_ID=""
SEED_MODE=independent
EXPLICIT_SEED=""
KEEP_PARTIAL=${KEEP_PARTIAL:-0}

usage() {
  sed -n '2,45p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE=$2; shift 2 ;;
    --jobs) JOBSET=$2; shift 2 ;;
    --run-id) RUN_ID=$2; shift 2 ;;
    --runs-dir) RUNS_DIR=$2; shift 2 ;;
    --python) PYTHON=$2; shift 2 ;;
    --bundle) BUNDLE_DIR=$2; shift 2 ;;
    --seed-mode) SEED_MODE=$2; shift 2 ;;
    --seed) EXPLICIT_SEED=$2; shift 2 ;;
    -h|--help) usage 0 ;;
    *) echo "unknown argument: $1" >&2; usage 2 ;;
  esac
done

case "$MODE" in
  real)
    [ "$JOBSET" = "real" ] || { echo "ERROR: --mode real requires --jobs real" >&2; exit 2; }
    ;;
  dry-run)
    case "$JOBSET" in
      control|failure) ;;
      *) echo "ERROR: --mode dry-run requires --jobs control|failure" >&2; exit 2 ;;
    esac
    ;;
  *) echo "ERROR: --mode must be real or dry-run" >&2; exit 2 ;;
esac

now_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
now_ms() { "$PYTHON" -c 'import time; print(int(time.time() * 1000))'; }
sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}';
  else shasum -a 256 "$1" | awk '{print $1}'; fi
}
die() { echo "FATAL: $*" >&2; exit 1; }

# Audited script hashes — execution is refused unless the bytes match.
EXPECTED_7PARAM=0709032c043372cafd79d1df4c62dd352403e881afc1fc395cb5956a19a15d2e
EXPECTED_6PARAM=012b14bb93ef9e668c1a578f7f98273fed3a41d9f7cf404a6ed26fa2e9c1623f
EXPECTED_E1Q3=3bbbc19ac42020b64a6d88c57118d75702c42dabddc0038f8ea087a6b2caf6c9

# ---------------------------------------------------------------------------
# 0. Run identity: unique timestamped + hashed output directory (defect 3 fix)
# ---------------------------------------------------------------------------
RUN_STARTED=$(now_utc)
if [ -z "$RUN_ID" ]; then
  HEAD_SHORT=$(git -C "$AUDIT_DIR" rev-parse --short=8 HEAD 2>/dev/null || echo nogit)
  NONCE=$(od -An -N4 -tx1 /dev/urandom 2>/dev/null | tr -d ' \n' || date -u +%s)
  RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-${HEAD_SHORT}-${NONCE}"
fi
RUN_DIR="$RUNS_DIR/$RUN_ID"
mkdir -p "$RUNS_DIR"
[ -e "$RUN_DIR" ] && die "run directory already exists (unique-dir guard): $RUN_DIR"
mkdir -p "$RUN_DIR/jobs" "$RUN_DIR/evidence"
MANIFEST_JSONL="$RUN_DIR/manifest.jsonl"
: > "$MANIFEST_JSONL"
RUN_LOG="$RUN_DIR/run.log"
echo "RUN_ID=$RUN_ID MODE=$MODE JOBSET=$JOBSET STARTED=$RUN_STARTED HOST=$(hostname)" | tee "$RUN_LOG"
echo "PYTHON=$PYTHON ($("$PYTHON" -V 2>&1))" | tee -a "$RUN_LOG"

# ---------------------------------------------------------------------------
# 1. Frozen-bundle integrity gate (read-only; before/after witness)
# ---------------------------------------------------------------------------
echo "-- bundle manifest verification (read-only) --" | tee -a "$RUN_LOG"
VERIFY_BEFORE_OUT=$("$HERE/verify_bundle_manifest.sh" --bundle "$BUNDLE_DIR" \
  --out "$RUN_DIR/evidence/bundle_verification_before.json" --python "$PYTHON")
printf '%s\n' "$VERIFY_BEFORE_OUT" | tee -a "$RUN_LOG"
BUNDLE_DIGEST_BEFORE=$(printf '%s\n' "$VERIFY_BEFORE_OUT" | sed -n 's/^bundle_dir_digest_sha256=//p')
[ -n "$BUNDLE_DIGEST_BEFORE" ] || die "could not parse bundle digest from verification output"

# ---------------------------------------------------------------------------
# 2. Job matrix (single source of truth: configs/*.json + shell matrix, checked)
# ---------------------------------------------------------------------------
case "$JOBSET" in
  real)
    JOBS_CFG="$HERE/configs/jobs_real.json"
    JOB_IDS=(job2_bray_abc_7param job2b_bray_abc_6param job1_e1_q3_selftest_gpu job1_e1_q3_cpu_ref job1_gpu_vs_cpu_diff)
    ;;
  control)
    JOBS_CFG="$HERE/configs/jobs_dry_run_control.json"
    JOB_IDS=(dryrun_stub_ok_a dryrun_stub_ok_b)
    ;;
  failure)
    JOBS_CFG="$HERE/configs/jobs_dry_run_failure.json"
    JOB_IDS=(dryrun_stub_ok_a dryrun_stub_fail dryrun_stub_ok_b_must_not_run)
    ;;
esac
[ -f "$JOBS_CFG" ] || die "jobs config missing: $JOBS_CFG"
CFG_IDS=$("$PYTHON" - "$JOBS_CFG" <<'PY'
import json, sys
print("\n".join(sorted(j["id"] for j in json.load(open(sys.argv[1], encoding="utf-8"))["jobs"])))
PY
)
MATRIX_IDS=$(printf '%s\n' "${JOB_IDS[@]}" | LC_ALL=C sort)
[ "$CFG_IDS" = "$MATRIX_IDS" ] || die "job matrix/config drift: config=[$CFG_IDS] matrix=[$MATRIX_IDS]"

# Real mode needs torch; dry-run is torch-free CPU-only by construction.
if [ "$MODE" = "real" ]; then
  "$PYTHON" -c 'import torch, numpy' 2>/dev/null || \
    die "real mode requires a Python with torch+numpy (tried: $PYTHON). Torch is parked; use --mode dry-run for the CPU-only integrity proof."
fi

# Hash every config file involved in this run (defect 5 fix).
"$PYTHON" - "$HERE/configs" "$RUN_DIR/evidence/config_hashes.json" <<'PY'
import hashlib, json, os, sys, time

configs_dir, out = sys.argv[1], sys.argv[2]
files = {}
for name in sorted(os.listdir(configs_dir)):
    p = os.path.join(configs_dir, name)
    if not os.path.isfile(p):
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    files[name] = {"sha256": h, "bytes": os.path.getsize(p)}
payload = {"generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "config_files": files}
tmp = f"{out}.tmp.{os.getpid()}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, sort_keys=True); f.write("\n"); f.flush(); os.fsync(f.fileno())
os.replace(tmp, out)
print(f"hashed {len(files)} config files -> {out}")
PY
CONFIG_HASHES_SHA=$(sha256_of "$RUN_DIR/evidence/config_hashes.json")

# ---------------------------------------------------------------------------
# 3. Independent validation seeds (defect 6 fix) — recorded + hashed
# ---------------------------------------------------------------------------
JOBS_CSV=$(printf '%s,' "${JOB_IDS[@]}" | sed 's/,$//')
if [ "$SEED_MODE" = "independent" ]; then
  "$PYTHON" "$HERE/tools/make_seeds.py" --out "$RUN_DIR/seeds.json" --jobs "$JOBS_CSV" | tee -a "$RUN_LOG"
else
  [ -n "$EXPLICIT_SEED" ] || die "--seed-mode derived requires --seed N"
  "$PYTHON" "$HERE/tools/make_seeds.py" --out "$RUN_DIR/seeds.json" --jobs "$JOBS_CSV" --seed "$EXPLICIT_SEED" | tee -a "$RUN_LOG"
fi
SEEDS_FILE="$RUN_DIR/seeds.json"
SEEDS_SHA=$(sha256_of "$SEEDS_FILE")

seed_for() {
  "$PYTHON" - "$SEEDS_FILE" "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print(d["seeds"][sys.argv[2]])
PY
}

# ---------------------------------------------------------------------------
# 4. Job execution with fail-fast + atomic output rename
# ---------------------------------------------------------------------------
record_job() { # job_id script script_sha cfg cfg_sha seed cmd out out_sha rc wall started ended err
  JOB_RUN_ID="$RUN_ID" JOB_MODE="$MODE" JOB_ID="$1" JOB_SCRIPT="$2" JOB_SCRIPT_SHA="$3" \
  JOB_CONFIG="$4" JOB_CONFIG_SHA="$5" JOB_SEED="$6" JOB_COMMAND="$7" JOB_OUTPUT="$8" \
  JOB_OUTPUT_SHA="$9" JOB_EXIT="${10}" JOB_WALL="${11}" JOB_WORKERS=1 \
  JOB_STARTED="${12}" JOB_ENDED="${13}" JOB_ERROR="${14}" \
  "$PYTHON" "$HERE/tools/record_job.py" "$MANIFEST_JSONL"
}

run_job() { # job_id script cfg out_name seed -- <command argv...>
  local job_id=$1 script=$2 cfg=$3 out_name=$4 seed=$5
  shift 5
  local job_dir="$RUN_DIR/jobs/$job_id"
  local staging="$job_dir/.staging"
  mkdir -p "$job_dir" "$staging"
  [ -f "$script" ] || die "job script not found: $script"
  local script_sha cfg_sha
  script_sha=$(sha256_of "$script")
  case "$script" in
    "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface.py")
      [ "$script_sha" = "$EXPECTED_7PARAM" ] || die "audited-script hash mismatch (7-param): $script_sha" ;;
    "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface_6param.py")
      [ "$script_sha" = "$EXPECTED_6PARAM" ] || die "audited-script hash mismatch (6-param): $script_sha" ;;
    "$BUNDLE_DIR/gpu_e1_q3_wild_cluster_ri.py")
      [ "$script_sha" = "$EXPECTED_E1Q3" ] || die "audited-script hash mismatch (E1/Q3): $script_sha" ;;
    *) : ;;
  esac
  [ -f "$cfg" ] || die "job config not found: $cfg"
  cfg_sha=$(sha256_of "$cfg")

  local cmd_str started ended start_ms end_ms rc wall out_sha err
  cmd_str=$(printf '%q ' "$@" "--out-dir" "$staging")
  started=$(now_utc)
  start_ms=$(now_ms)
  echo "== job $job_id start=$started" | tee -a "$RUN_LOG"
  # `set -e` must not kill the harness here: capture rc explicitly, then decide.
  if ( "$@" "--out-dir" "$staging" ) >"$job_dir/stdout.log" 2>&1; then
    rc=0
  else
    rc=$?
  fi
  end_ms=$(now_ms)
  ended=$(now_utc)
  wall=$("$PYTHON" -c "print(round(($end_ms - $start_ms) / 1000.0, 3))")

  if [ "$rc" -ne 0 ]; then
    err="job exited rc=$rc; corrected harness aborts the whole run (fail-fast) instead of echoing rc and continuing"
    # Atomicity: never leave a partial JSON where a result is expected.
    [ "$KEEP_PARTIAL" = "1" ] || rm -rf "$staging"
    record_job "$job_id" "$script" "$script_sha" "$cfg" "$cfg_sha" "$seed" "$cmd_str" \
      "$out_name" "" "$rc" "$wall" "$started" "$ended" "$err"
    echo "ERROR: job $job_id FAILED rc=$rc -> aborting run $RUN_ID (fail-fast)" | tee -a "$RUN_LOG" >&2
    "$PYTHON" - "$RUN_DIR/run_failure.json" "$RUN_ID" "$MODE" "$job_id" "$rc" "$started" "$ended" <<'PY'
import json, os, sys, time
out, run_id, mode, job_id, rc, started, ended = sys.argv[1:]
payload = {"run_id": run_id, "mode": mode, "status": "failed", "failed_job": job_id,
           "exit_code": int(rc), "started_utc": started, "ended_utc": ended,
           "note": "harness aborted at the first non-zero job; no manifest.json was assembled"}
tmp = f"{out}.tmp.{os.getpid()}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, sort_keys=True); f.write("\n"); f.flush(); os.fsync(f.fileno())
os.replace(tmp, out)
PY
    exit "$rc"
  fi

  if [ ! -f "$staging/$out_name" ]; then
    err="job rc=0 but expected output '$out_name' missing from staging"
    rm -rf "$staging"
    record_job "$job_id" "$script" "$script_sha" "$cfg" "$cfg_sha" "$seed" "$cmd_str" \
      "$out_name" "" "$rc" "$wall" "$started" "$ended" "$err"
    die "$err (job $job_id)"
  fi
  # ATOMIC: a single rename publishes the result; there is no half-written file.
  mv -f "$staging/$out_name" "$job_dir/$out_name"
  rm -rf "$staging"
  out_sha=$(sha256_of "$job_dir/$out_name")
  record_job "$job_id" "$script" "$script_sha" "$cfg" "$cfg_sha" "$seed" "$cmd_str" \
    "$out_name" "$out_sha" "$rc" "$wall" "$started" "$ended" ""
  echo "== job $job_id ok rc=0 wall=${wall}s output=$job_dir/$out_name sha256=$out_sha" | tee -a "$RUN_LOG"
}

run_real_jobs() {
  local s7 s6 se sd
  s7=$(seed_for job2_bray_abc_7param)
  s6=$(seed_for job2b_bray_abc_6param)
  se=$(seed_for job1_e1_q3_selftest_gpu)
  sd=$(seed_for job1_gpu_vs_cpu_diff)
  run_job job2_bray_abc_7param "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface.py" \
    "$HERE/configs/job2_abc_7param.json" bray_abc_and_contest_surface.json "$s7" \
    "$PYTHON" "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface.py" --n-abc 200000 --seed "$s7"
  run_job job2b_bray_abc_6param "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface_6param.py" \
    "$HERE/configs/job2b_abc_6param.json" bray_abc_and_contest_surface.json "$s6" \
    "$PYTHON" "$BUNDLE_DIR/gpu_bray_abc_and_contest_surface_6param.py" --n-abc 200000 --seed "$s6"
  run_job job1_e1_q3_selftest_gpu "$BUNDLE_DIR/gpu_e1_q3_wild_cluster_ri.py" \
    "$HERE/configs/job1_e1q3_gpu.json" wild_cluster_ri_results.json "$se" \
    "$PYTHON" "$BUNDLE_DIR/gpu_e1_q3_wild_cluster_ri.py" --B 2000 --seed "$se"
  run_job job1_e1_q3_cpu_ref "$BUNDLE_DIR/gpu_e1_q3_wild_cluster_ri.py" \
    "$HERE/configs/job1_e1q3_cpu_ref.json" wild_cluster_ri_results.json "$se" \
    env CUDA_VISIBLE_DEVICES="" "$PYTHON" "$BUNDLE_DIR/gpu_e1_q3_wild_cluster_ri.py" --B 2000 --seed "$se"
  run_job job1_gpu_vs_cpu_diff "$HERE/tools/gpu_vs_cpu_diff.py" \
    "$HERE/configs/job1_gpu_vs_cpu_diff.json" results_gpu_vs_cpu_diff.json "$sd" \
    "$PYTHON" "$HERE/tools/gpu_vs_cpu_diff.py" \
      --gpu "$RUN_DIR/jobs/job1_e1_q3_selftest_gpu/wild_cluster_ri_results.json" \
      --cpu "$RUN_DIR/jobs/job1_e1_q3_cpu_ref/wild_cluster_ri_results.json"
}

run_dry_control() {
  local sa sb
  sa=$(seed_for dryrun_stub_ok_a)
  sb=$(seed_for dryrun_stub_ok_b)
  run_job dryrun_stub_ok_a "$HERE/stubs/stub_job_ok.py" "$HERE/configs/stub_ok.json" result.json "$sa" \
    "$PYTHON" "$HERE/stubs/stub_job_ok.py" --job-id dryrun_stub_ok_a --n 8 --seed "$sa"
  run_job dryrun_stub_ok_b "$HERE/stubs/stub_job_ok.py" "$HERE/configs/stub_ok.json" result.json "$sb" \
    "$PYTHON" "$HERE/stubs/stub_job_ok.py" --job-id dryrun_stub_ok_b --n 5 --seed "$sb"
}

run_dry_failure() {
  local sa sf sb
  sa=$(seed_for dryrun_stub_ok_a)
  sf=$(seed_for dryrun_stub_fail)
  sb=$(seed_for dryrun_stub_ok_b_must_not_run)
  run_job dryrun_stub_ok_a "$HERE/stubs/stub_job_ok.py" "$HERE/configs/stub_ok.json" result.json "$sa" \
    "$PYTHON" "$HERE/stubs/stub_job_ok.py" --job-id dryrun_stub_ok_a --n 8 --seed "$sa"
  # This job is designed to fail with exit code 7. The harness must abort here.
  run_job dryrun_stub_fail "$HERE/stubs/stub_job_fail.py" "$HERE/configs/stub_fail.json" result.json "$sf" \
    "$PYTHON" "$HERE/stubs/stub_job_fail.py" --job-id dryrun_stub_fail --n 8 --seed "$sf" --exit-code 7
  # Unreachable if fail-fast works — its absence is the proof.
  run_job dryrun_stub_ok_b_must_not_run "$HERE/stubs/stub_job_ok.py" "$HERE/configs/stub_ok.json" result.json "$sb" \
    "$PYTHON" "$HERE/stubs/stub_job_ok.py" --job-id dryrun_stub_ok_b_must_not_run --n 5 --seed "$sb"
}

case "$JOBSET" in
  real) run_real_jobs ;;
  control) run_dry_control ;;
  failure) run_dry_failure ;;
esac

# ---------------------------------------------------------------------------
# 5. Post-run integrity witness + manifest assembly (defect 7 fix)
# ---------------------------------------------------------------------------
RUN_ENDED=$(now_utc)
echo "-- post-run bundle verification (must equal pre-run digest) --" | tee -a "$RUN_LOG"
VERIFY_AFTER_OUT=$("$HERE/verify_bundle_manifest.sh" --bundle "$BUNDLE_DIR" \
  --out "$RUN_DIR/evidence/bundle_verification_after.json" --python "$PYTHON")
printf '%s\n' "$VERIFY_AFTER_OUT" | tee -a "$RUN_LOG"
BUNDLE_DIGEST_AFTER=$(printf '%s\n' "$VERIFY_AFTER_OUT" | sed -n 's/^bundle_dir_digest_sha256=//p')
[ -n "$BUNDLE_DIGEST_AFTER" ] || die "could not parse post-run bundle digest"
[ "$BUNDLE_DIGEST_BEFORE" = "$BUNDLE_DIGEST_AFTER" ] || \
  die "FROZEN BUNDLE CHANGED DURING RUN: before=$BUNDLE_DIGEST_BEFORE after=$BUNDLE_DIGEST_AFTER"

"$PYTHON" - "$RUN_DIR/run_meta.json" "$RUN_ID" "$MODE" "$JOBSET" "$RUN_STARTED" "$RUN_ENDED" \
  "$BUNDLE_DIGEST_BEFORE" "$BUNDLE_DIGEST_AFTER" "$SEEDS_SHA" "$CONFIG_HASHES_SHA" "$PYTHON" <<'PY'
import json, os, sys, time
out, run_id, mode, jobset, started, ended, dbefore, dafter, seeds_sha, cfg_sha, py = sys.argv[1:]
payload = {
    "run_id": run_id, "mode": mode, "jobset": jobset,
    "started_utc": started, "ended_utc": ended,
    "status": "ok",
    "bundle_digest_before": dbefore, "bundle_digest_after": dafter,
    "bundle_unchanged_during_run": dbefore == dafter,
    "seeds_file_sha256": seeds_sha,
    "config_hashes_sha256": cfg_sha,
    "python": py,
    "host": os.uname().nodename,
}
tmp = f"{out}.tmp.{os.getpid()}"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, sort_keys=True); f.write("\n"); f.flush(); os.fsync(f.fileno())
os.replace(tmp, out)
PY

"$PYTHON" "$HERE/tools/assemble_manifest.py" \
  --run-dir "$RUN_DIR" --manifest-jsonl "$MANIFEST_JSONL" \
  --config "$JOBS_CFG" --mode "$MODE" --run-id "$RUN_ID" --bundle "$BUNDLE_DIR" \
  | tee -a "$RUN_LOG"

echo "RUN COMPLETE run_id=$RUN_ID mode=$MODE jobs=${#JOB_IDS[@]} dir=$RUN_DIR" | tee -a "$RUN_LOG"
