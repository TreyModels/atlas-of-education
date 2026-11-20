# E13 — Graduate-supply shock with matched competitive benchmark

Command: `PYTHONPATH=<work>/massabm "$PY" exp/run_E13.py --reps 3 --N 5000 --workers 2 --out <out>`

E13 GRADUATE-SUPPLY SHOCK, matched competitive benchmark
reps=3 N=5000 wall=81s ok=18/18 failed=0
No K-12 reform; 1995 tuition shock; labour market 2010-30; paired seeds 20000+r.

  world                                    shock                           d degree   d diploma inc  d degree inc  d dip/deg  d formal|dip
  surplus model (slots, floors, ranking)   no shock                          +0.000      +0.000(0.000)        +0.000     +0.000    +0.000(0.000)
  surplus model (slots, floors, ranking)   college half price from 1995      +0.135      -0.058(0.018)        -0.333     +0.047    -0.151(0.022)
  surplus model (slots, floors, ranking)   college 80% off from 1995         +0.214      -0.039(0.015)        -0.436     +0.079    -0.164(0.019)
  competitive skill market (CES wages)     no shock                          +0.000      +0.000(0.000)        +0.000     +0.000    +0.000(0.000)
  competitive skill market (CES wages)     college half price from 1995      +0.130      +0.295(0.005)        -0.442     +0.171    +0.000(0.000)
  competitive skill market (CES wages)     college 80% off from 1995         +0.221      +0.546(0.007)        -0.657     +0.321    +0.000(0.000)

PREDECLARED DISCRIMINATION (college half price from 1995):
  surplus model (slots, floors, ranking)   Δdiploma income=-0.0583 (±0.0180)  Δformal|dip=-0.1511 (±0.0217)  Δratio=+0.0466
  competitive skill market (CES wages)     Δdiploma income=+0.2947 (±0.0046)  Δformal|dip=+0.0000 (±0.0000)  Δratio=+0.1706
  surplus predicts diploma losers (Δ<0), competitive predicts diploma gainers (Δ>0): observed sign pattern CONSISTENT -> SUPPORTS the surplus account (ratio also usable in both)
