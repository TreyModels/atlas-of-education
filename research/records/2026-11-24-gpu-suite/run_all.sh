#!/usr/bin/env bash
set -euo pipefail
mkdir -p results
export PYTHONPATH="$(pwd)/scripts:${PYTHONPATH:-}"
python3 scripts/exp1_unified_gpu_abm.py --smoke --out results/smoke_exp1.json
python3 scripts/exp1_unified_gpu_abm.py --seeds 20 --out results/exp1_abm.json
python3 scripts/exp2_macro_wall_and_tiebreaker.py --inp results/exp1_abm.json --out results/exp2_macro_wall.csv
python3 scripts/exp3_rejection_abc_realdata.py --draws 5000 --batch-n 50000 --out results/exp3_abc_posterior.json
python3 scripts/exp4_fee_abolition_child_labor.py --out results/exp4_fee_child_labor.csv
sha256sum results/* > results/SHA256SUMS.txt
echo "SUITE COMPLETE"
