# E21 — External enrolment benchmark vs observed UIS/WDI GER (new data from data-hunter)

Command: `PYTHONPATH=<work>/massabm "$PY" exp/run_E21.py --reps 2 --N 5000 --workers 2 --out <out>`

Data: `04_data/data/gmr_observed_6countries_1970_2024.csv` (observed cells only; imputed cells never used
as truth). Source per point is in `e21_series.csv`. Window 1980-2020. Status: completed (4 model runs, 10 s).

E21 EXTERNAL ENROLMENT BENCHMARK vs OBSERVED UIS/WDI GER (new data from data-hunter)
reps=2 N=5000 wall=10s ok=172 series-years; runs failed=0
Only OBSERVED cells used; imputed cells never used as truth. Window 1980-2020.
Model GER = model enrolment stock / (N x duration); secondary duration switches 4->6 with the model's own
K-12 reform flag (not tuned to the data). This is a flow benchmark, NOT a calibration.

  country indicator        n     years obs mean model mean    corr  MAE pp  bias pp
  PHL     ger_primary     37 1980-2020    102.1       99.7   0.309     3.4     -2.4
  PHL     ger_secondary   36 1980-2020     72.3       79.9  -0.326    12.6     +7.6
  PHL     ger_tertiary    36 1980-2020     27.3       24.6  -0.397     5.4     -2.7
  KOR     ger_primary     21 2000-2020    100.0      100.0   0.643     0.7     -0.0
  KOR     ger_secondary   21 2000-2020     97.7       88.6   0.607     9.0     -9.0
  KOR     ger_tertiary    21 2000-2020     93.7       41.0   0.156    52.7    -52.7

READ: the test is whether the uncalibrated default model reproduces the LEVEL and SHAPE of observed
enrolment. Matching the shape (corr) is weak evidence because both rise; the level (MAE, bias) is the
honest test. The Korea-like preset is a stylised schedule, not a calibrated Korea: a miss there is a
statement about the preset, not about Korea.

CAVEAT on data vintage: the observed series come from the data-hunter pull (retrieved 2026-11-20), which
harmonises UIS SDG4 2026-11, UIS EDUNONCORE Feb-2020 and WDI-via-UIS layers; source per point is in
e21_series.csv. Any years where the observed series is absent were skipped, not imputed.
