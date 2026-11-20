# E15 — State priorities and capacity (triad state_motive)

Command: `PYTHONPATH=<work>/triad "$PY" exp/run_triad_E14_E15.py /tmp/massrun/runs/triad 3 2000 2`

STATE MOTIVE: why does the state fund schooling, and does it come out ahead?
state net = tax a taxing state collects - its school spending, discounted from year 0 over 140 years.
"vs frozen" = that minus the same for a state that never funds beyond primary. Positive = investing pays the state.
Two ledgers: income tax on formal wages only (as built), and income + consumption tax at 12% on 80% of domestic
income (formal + informal; mirrors massabm/fiscal.py). No overseas/remittance channel exists in triad, so the
consumption ledger still understates the base. Rentier arms capture no tax in either ledger.

  arm                                    years  tert funds L2/L3/L4 in year vs frozen @6% (inc only)  @6% (inc+cons)
  fiscal, whole career (as built)         11.6  0.38               20/30/40                  -4.10           -4.20
  fiscal, 10-year horizon, 10% rate       10.2  0.14               -1/-1/-1                  -0.29           -0.30
  fiscal, 25-year horizon, 4% rate        11.6  0.38               20/30/40                  -4.11           -4.21
  never invests (frozen)                  10.4  0.21               -1/-1/-1                   0.00            0.00
  rentier with budget, no motive          10.5  0.22               -1/-1/-1                  -0.14   n/a (rentier)
  rentier + order after unrest (yr 30)    10.7  0.22               41/-1/-1                  -0.69   n/a (rentier)
  rentier + keeping up with peers         10.7  0.22               34/-1/-1                  -2.22   n/a (rentier)
  fiscal + order after unrest (yr 30)     11.6  0.38               20/30/40                  -4.10           -4.20

Read: if the investing fiscal state does NOT beat the frozen state on either ledger, the state's surplus comes
from taxing credentials households paid for, not from its own investment (its subsidies mostly replace private spending).
If adding consumption tax flips the sign, the conclusion changes: then investment pays through the broad tax base.
Compare depth across motives: which motives deepen the pipeline, and which only fund it on paper?
-1 = the state never funds that level.
