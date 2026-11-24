#!/bin/bash
# Runs ON THE BOX. Binding-gate experiment, pre-registered research/binding-gate-2026-11-25 @37cbe3d.
set -e
OUTROOT=/root/work/binding_gate
X="0.02,0.03,0.045,0.065,0.09,0.13,0.18,0.25,0.35,0.5"
Y="0.0,0.04,0.08,0.12,0.16,0.19"
mkdir -p $OUTROOT
for S in 0.25 0.35 0.45 0.55 0.70; do
  OUT=$OUTROOT/share_$S
  rm -rf $OUT; mkdir -p $OUT
  /root/miniconda3/bin/python -u /root/work/phase_sweep_binding.py \
    --engine-root /root/work/edsystem/engine --out $OUT --workers 10 --seeds 5 \
    --gate quota --quota-share $S --x-levels "$X" --y-levels "$Y" \
    > $OUTROOT/share_$S.log 2>&1 || echo "share $S FAILED rc=$?"
  echo "share $S done"
done
OUT=$OUTROOT/bar_high
rm -rf $OUT; mkdir -p $OUT
/root/miniconda3/bin/python -u /root/work/phase_sweep_binding.py \
  --engine-root /root/work/edsystem/engine --out $OUT --workers 10 --seeds 5 \
  --gate bar --bar-levels 14,15,16,17 --x-levels "$X" --y-levels "$Y" \
  > $OUTROOT/bar_high.log 2>&1 || echo "bar_high FAILED rc=$?"
echo "bar-high done"
echo BINDING_DONE
