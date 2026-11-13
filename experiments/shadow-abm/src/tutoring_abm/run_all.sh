#!/usr/bin/env bash
# Full pipeline. "./run_all.sh quick" uses a smaller calibration for checking.
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "quick" ]]; then N=300; P=150; G=10; else N=1000; P=400; G=16; fi
python3 calibrate.py --n "$N" --out results/pilot2.csv
python3 smc.py --particles "$P" --gens "$G"
python3 analysis.py
python3 make_figures.py
echo "Done. See results/summary.json and paper/figures/."
