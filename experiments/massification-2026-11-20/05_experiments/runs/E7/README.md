# E7 — Gate density and tutoring clustering

Command actually run:
```
PYTHONPATH=<work>/massabm MASSRUN_EXP=<work>/exp \
  "$PY" exp/run_E7.py --reps 3 --N 5000 --workers 2 --out /tmp/massrun/runs/E7
# findings regenerated from the written raw CSV by exp/post_E7.py (the first findings pass
# crashed on a formatting bug AFTER both CSVs were written; no runs were rerun or dropped).
```

E7 GATE DENSITY AND TUTORING CLUSTERING
reps=3 N=5000; seeds 3000+r; window 2000-2012 for gate rates, cohorts 1995-2012.

Baseline gate tutoring rates (share of gate-takers who tutor) and spend shares:
  basic=0.040  apex=0.443  college=0.280  board=0.933
  spend by gate: basic=756  apex=1678  college=647  board=1019
  apex share of total spend=0.409  board share=0.249

Bar sweep on the BASIC completion gate:
     bar  tut_basic  completion  college_Q1 liquidity exit
    -2.0      0.022(±0.000)       0.718       0.021         0.4011
    -1.5      0.085(±0.001)       0.709       0.018         0.3916
    -1.0      0.234(±0.005)       0.675       0.012         0.3653
    -0.5      0.463(±0.001)       0.596       0.006         0.3167
    +0.0      0.650(±0.004)       0.457       0.002         0.2461
    +0.5      0.752(±0.006)       0.287       0.003         0.2100

Tutoring ban arms (does spend disappear or reroute?):
  ban=none        total=  4100  by gate: basic=756 apex=1678 college=647 board=1019  completion=0.716  college_Q1=0.017
  ban=apex        total=  3686  by gate: basic=761 apex=1216 college=701 board=1009  completion=0.717  college_Q1=0.019
  ban=board       total=  4075  by gate: basic=779 apex=1699 college=660 board=937  completion=0.718  college_Q1=0.017
  ban=all_formal  total=  3601  by gate: basic=764 apex=1233 college=638 board=966  completion=0.717  college_Q1=0.017

Predeclared threshold: bar sweep must raise basic-gate tutoring by > 2 seed sd. Observed Δ=+0.729 vs 2*sd≈0.012 -> SUPPORTS

Read: tutoring share should be highest where the payoff is discontinuous (board/apex) and should
move to the basic gate as that gate is pushed toward the median student. The ban arms show whether
closing a gate deletes demand (spend->0) or reroutes it (spend persists at other gates / informal leak).
