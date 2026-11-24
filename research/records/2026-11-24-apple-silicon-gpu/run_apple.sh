#!/usr/bin/env bash
# Apple Silicon runner for the unified GPU suite, through the CuPy import shim.
# Usage: APPLE_PY=/path/to/python APPLE_GPU_BACKEND=mlx ./run_apple.sh smoke
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SUITE="$ROOT/suite/unified_gpu_suite"
PY="${APPLE_PY:-python3}"
BACKEND="${APPLE_GPU_BACKEND:-mlx}"
export APPLE_GPU_BACKEND="$BACKEND"
export PYTHONPATH="$ROOT:$ROOT/shim:$SUITE/scripts:${PYTHONPATH:-}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
mkdir -p "$ROOT/results"
cd "$SUITE"
echo "[run_apple] backend=$BACKEND python=$PY"
case "${1:-smoke}" in
  smoke)
    t0=$(date +%s)
    "$PY" scripts/exp1_unified_gpu_abm.py --smoke --out "$ROOT/results/smoke_exp1_${BACKEND}.json"
    "$PY" scripts/exp3_rejection_abc_realdata.py --draws 20 --batch-n 2000 --out "$ROOT/results/smoke_exp3_${BACKEND}.json"
    t1=$(date +%s); echo "[run_apple] smoke wall $((t1-t0)) s"
    ;;
  production)
    # Full upstream production configuration (time-bounded on Apple Silicon per results/projection.json).
    t0=$(date +%s)
    "$PY" scripts/exp1_unified_gpu_abm.py --seeds 20 --out "$ROOT/results/exp1_abm_${BACKEND}.json"
    "$PY" scripts/exp2_macro_wall_and_tiebreaker.py --inp "$ROOT/results/exp1_abm_${BACKEND}.json" --out "$ROOT/results/exp2_macro_wall_${BACKEND}.csv"
    "$PY" scripts/exp3_rejection_abc_realdata.py --draws 5000 --batch-n 50000 --out "$ROOT/results/exp3_abc_posterior_${BACKEND}.json"
    t1=$(date +%s); echo "[run_apple] production wall $((t1-t0)) s" | tee "$ROOT/results/production_wall_${BACKEND}.txt"
    ;;
  cpu)
    "$PY" scripts/exp2_macro_wall_and_tiebreaker.py --inp "$ROOT/results/smoke_exp1_${BACKEND}.json" --out "$ROOT/results/smoke_exp2_${BACKEND}.csv"
    ;;
  *) echo "usage: run_apple.sh [smoke|cpu]" >&2; exit 2;;
esac
