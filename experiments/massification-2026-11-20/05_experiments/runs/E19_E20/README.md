# E19 + E20 (pilot) — Descriptive gate paths and cross-country transfer

Command: `PYTHONPATH=<work>/massabm "$PY" exp/run_E19_E20.py --reps 2 --N 5000 --workers 2 --out <out>`

Status: **pilot only**. Hong Kong = data blocked. Korea transfer = model-to-model.

E19/E20 DESCRIPTIVE GATE PATHS AND CROSS-COUNTRY TRANSFER (PILOT)
reps=2 N=5000 wall=34s ok=6/6 failed=0
ALL NUMBERS ARE SIMULATED MODEL OUTPUTS, not observed country series. Hong Kong: DATA BLOCKED
(no local HK series was loaded in this budget; nothing about HK is claimed).

E19 — simulated cohort trajectories (entry cohorts, 5-year windows):
  arm                                        basic1980 basic1990 basic2005 basic2018  deg1990  deg2015
  PH baseline                                    0.730     0.740     0.662     0.674    0.198    0.152
  Korea-like preset                              0.801     0.809     0.817     0.820    0.324    0.470
  Korea + PH overseas channel (transfer)         0.806     0.806     0.819     0.818    0.259    0.402

E19 — Philippine model vs the manuscript's rough targets (default parameters, NOT calibrated):
  indicator                                                    model  target
  basic completion, entry 1990-95 (HS ~2001-05)                0.739  ~0.55-0.62
  basic completion, entry 2008-12 (SHS ~2020-24)               0.649  ~0.70-0.73
  basic completion Q1, entry 1985-90                           0.423  ~0.35-0.40
  basic completion Q5, entry 1985-90                           0.815  ~0.90+
  degree share, entry 1990-95                                  0.198  ~0.14-0.20
  basic->college transition, entry 2008-12                     0.227  ~0.70 (SHS grads)
  prof-track entry share, entry 1990-98 (nursing boom)         0.097  ~0.04-0.06
  OFW professional share of deployments, 2015-23               0.156  <~0.25 (41% elementary)
  informal share of entrants, 2010                             0.514  ~0.5-0.6
  tutoring rate at board exam, 2010                            0.933  high (review centres)
  tutoring rate at basic gate, 2010                            0.057  thin
  tertiary GPI (college entry F/M), entry 1995-2005            0.868  ~1.2-1.3

E20 — transfer pilot (PH overseas/recognition channel grafted onto a Korea-like schedule):
  This is a MODEL-TO-MODEL comparison, not a blind empirical validation of Korea.
  degree (2015-17 entry): Korea-like 0.470 -> transfer 0.402
  basic (2018 entry):     Korea-like 0.820 -> transfer 0.818
  informal share 2015-30: Korea-like 0.394 -> transfer 0.292
  DECLARED NULL (predeclared): the transfer does NOT improve the naive persistence benchmark on
  informal-share or degree-share, because the overseas channel moves a small marginal group while the
  domestic formal sector in the Korea-like schedule drives the aggregates. Reported as a null, not a win.

Status: pilot only. Hong Kong path is data blocked; Korea comparison is model-to-model.
