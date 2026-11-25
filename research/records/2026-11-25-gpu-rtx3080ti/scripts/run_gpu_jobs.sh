#!/bin/bash
set -u
cd /root/work/gpu
mkdir -p logs results_rtx3080ti
PY=/root/miniconda3/bin/python
echo "===== ENV ====="
date -u +%Y-%m-%dT%H:%M:%SZ
$PY -c "import torch;print('torch',torch.__version__);print('cuda_available',torch.cuda.is_available());print('cuda_version',torch.version.cuda);print('gpu',torch.cuda.get_device_name(0))"
$PY -c "import pandas,numpy;print('pandas',pandas.__version__,'numpy',numpy.__version__)"
run() {
  local name="$1"; shift
  local t0=$(date +%s.%N)
  "$@" 2>&1 | tee "logs/${name}.log"
  local rc=${PIPESTATUS[0]}
  local t1=$(date +%s.%N)
  echo "JOB ${name} EXIT ${rc} WALL_SEC $(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.2f", b-a}')"
}
run job2_bray_abc $PY gpu_bray_abc_and_contest_surface.py --n-abc 200000 --out-dir ./results_rtx3080ti/bray_and_contest
run job1_e1_q3_selftest $PY gpu_e1_q3_wild_cluster_ri.py --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest
CUDA_VISIBLE_DEVICES="" run job1_e1_q3_cpu_ref $PY gpu_e1_q3_wild_cluster_ri.py --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest_cpu_ref
echo "===== DONE ====="
date -u +%Y-%m-%dT%H:%M:%SZ
