#!/usr/bin/env bash
# Reproduces the ARCHAIVED runner's execution-integrity defect (P0-07 item 1).
#
# This is a faithful reduction of gpu_abc_bundle/run_gpu_jobs.sh's run() function:
#   * `set -u` only (no -e, no pipefail)
#   * the job's rc is captured from PIPESTATUS[0] but only ECHOED
#   * the script continues to the next job and prints DONE regardless
#
# It is run here with one deliberately failing job (exit 7). Expected (defective)
# behaviour: overall exit 0 and "JOB job_fail EXIT 7" + "===== DONE =====" printed.
# The corrected harness must instead abort with rc 7 (see dry_run_failure_propagation.sh).
set -u
PY=${PYTHON:-python3}

LOG_DIR=${1:-./archived_demo_logs}
mkdir -p "$LOG_DIR"

run() {
  local name="$1"; shift
  "$@" 2>&1 | tee "$LOG_DIR/${name}.log"
  local rc=${PIPESTATUS[0]}
  echo "JOB ${name} EXIT ${rc} WALL_SEC 0.00"
}

run job_ok "$PY" -c 'print("job_ok ran")'
run job_fail "$PY" -c 'import sys; print("intentional failure", file=sys.stderr); sys.exit(7)'
echo "===== DONE ====="
