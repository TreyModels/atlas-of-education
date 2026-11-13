# firms/ — firm-side youth labour market with a categorical (Tilly) core

Run from `engine/`:

    python -m unittest firms.test_firms firms.test_tilly -v   # 23 tier-1/tier-2 tests, a few seconds
    python -m firms.calibrate_china             # model.py fits (2 windows x 4 sigma_A), Shapley, plots; ~60 min
    python -m firms.tilly_experiments           # the four mechanisms one at a time on the headline parameters
    python -m firms.tilly_fit                   # whole-record fit with the mechanisms on; ~20-40 min

Files
- `categorical.py` — the core. Workers are cells of (degree / none) x (insider / outsider); positions are segments
  with entry rules (secure posts, private graduate jobs, open jobs). Tilly's four mechanisms act on those boundaries:
  exploitation (wage wedge on outsiders), opportunity hoarding (secure posts filled inside the network first),
  emulation (degree requirements diffusing through open jobs), adaptation (waiting for posts outside the labour force).
  With every mechanism off it reproduces `model.py` to 1e-10 (tested).
- `model.py` — the two-type special case (search, free entry, CES, wage rigidity, NBS observation equation).
- `data_china.py` — inputs with 'v'/'m' provenance flags and sources.
- `calibrate_china.py`, `tilly_experiments.py`, `tilly_fit.py` — fits and experiments; outputs in `results/`.
