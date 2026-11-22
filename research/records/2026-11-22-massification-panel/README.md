# Massification panel and MASSENG runs, 22 November 2026 (record)

**Status: record, not an active research model.** This folder archives one day's work so it can be reproduced and challenged. It does not take one of the two active research slots in `research/GATE.md`.

Every number lives in a result file listed below. Following the house rule, this README restates none of them; each section names the file that holds the result.

**Testing status.**
- Every test here is retrospective and inspected, not blind.
- Associations from the panel sweeps are not causal estimates.
- Protocols were written before each run, and each amendment is dated inside its protocol.

## What was done

### 1. Philippine cohort model (MASSENG)
- **v6_phl, a pre-registered demand experiment.** Six nested demand specifications, with constrained and unconstrained sign tests, were scored against persistence and trend.
  - The record also holds Amendment A1 (a nesting fix and optimiser restarts) and diagnostic A2 (household-spending rows removed).
  - Files: `protocols/PROTOCOL_v6_phl.md`, `notes/RESULTS_v6_phl.md`, `results/masseng_PHL/v6_phl/`.
- **kiss_phl, enrolment-only.** Several simple models were compared: income + cost, + positional pull, + returns, and a logistic S-curve, plus an equal-weight ensemble ("Page") and a blend of persistence and the ensemble ("Silver"). Ten optimiser starts per spec; parameter Monte Carlo bands.
  - Files: `protocols/PROTOCOL_kiss_phl.md`, `results/masseng_PHL/kiss/scores.json`, `results/masseng_PHL/kiss/mc_K0.json`.

### 2. Triad (households, employers, state) in three countries
- **The same cohort engine on the Philippines, Cambodia and Hong Kong**, with measured employer drivers (non-agricultural employment share) and state drivers (education spending).
  - Files: `protocols/PROTOCOL_triad.md`, `results/triad/logs/scores.log`, `results/triad/outputs/`.
  - The identification Monte Carlo was stopped part-way as the wrong test for the boot-up claim. Its partial files are archived but not interpreted.
- **Global sensitivity of the agent-based Triad simulation**: 2,000 Latin-hypercube parameter draws, each followed by single-actor knockouts.
  - Files: `scripts/triad_gsa.py`, `results/triad/triad_abm/results/gsa/findings.txt`.
  - The simulation code itself belongs to the authors' unpublished project and is not included.

### 3. Cross-national panel (World Bank WDI, UIS and ILO-modelled series, plus OEC economic complexity)
- **Takeoff test.** Does tertiary GER crossing 15% (Trow) require household means, employer demand (ECI) and state capacity jointly? Discrete-time hazard models, 10-fold country cross-validation, a 2,000-draw cluster bootstrap and a 1,000-draw threshold Monte Carlo.
  - Files: `protocols/PROTOCOL_takeoff.md`, `results/takeoff/findings.txt`, `results/takeoff/results.json`.
- **Wide sweep.** Extreme-bounds (Sala-i-Martin) robustness for three schooling outcomes, with a discovery/confirmation split of countries, country groupings (Asia, massifier timing, complexity mismatch, resource states) and lead-lag tests.
  - Files: `scripts/sweep.py`, `results/sweep/findings.txt`, `results/sweep/robust_table.csv`.
- **Every-variable sweep.** Each of 58 variables in turn as the outcome, giving a directed "who leads whom" map.
  - Files: `scripts/sweep_all.py`, `results/sweep_all/findings.txt`, `results/sweep_all/matrix.csv`, `results/sweep_all/leads.csv`.

### 4. Tighter tests (run after the sweeps; design fixed in the script header before running)
- **Within-country lead-lag.** Country fixed effects with a split-panel jackknife correction, plus a cluster-bootstrap test of whether X→Y is stronger than Y→X.
- **Split stability.** 200 random country splits instead of one.
- **Takeoff functional form.** Smooth, threshold, count and hybrid hazard models compared by cross-validation across 20 fold seeds.
- Files: `scripts/tight_tests.py`, `results/tight/findings.txt`, `results/tight/results.json`.
- Reading note: within-country coefficients on levels pick up floor and ceiling dynamics. Some signs are implausible (for example, income "leading" rising child mortality), so read them as noisy.

## Source data
- `sources/wdi_takeoff/` and `sources/wdi_sweep/` hold every series downloaded from the World Bank API (WDI, which includes UIS and ILO-modelled indicators), the OEC economic-complexity ranks via Our World in Data, the Harvard Growth Lab complexity rankings file, and the hand-collected triad driver data.
  - Each WDI file is a JSON list of `[iso3, year, value]` rows. Files over 200 KB are gzipped (`.json.gz`); the scripts expect them unzipped in `data/` (takeoff) and `data_sweep/` (sweeps).
  - The driver data are `triad_drivers.json` and `triad_drivers.md`. They list sources, read status and gaps.
- The four World Governance Indicator series failed to download (API source parameter). They are absent from the sweeps.

## Literature and next tests
`notes/sweep_litreview.md` covers three things:
- prior work, including Schofer & Meyer 2005, Clemens 2004, Yu & Delaney 2016 and Acemoglu et al. 2005;
- the main weakness of the sweeps: no country fixed effects;
- tighter designs: split-panel-corrected fixed-effects Granger tests with a direct asymmetry test, BMA or double ML with false-discovery-rate control, and event studies around fee abolitions.

Items marked [M] in that note are unverified.

## Reproduce
- **Panel:** `python scripts/takeoff.py fetch && python scripts/takeoff.py run`, then `python scripts/sweep.py fetch && python scripts/sweep.py run`, then `python scripts/sweep_all.py`.
- **Cohort runs:** `scripts/triad.py` and `scripts/kiss_ensemble.py` run from the `masseng_snapshot/` package root (`PYTHONPATH=.`).
- `masseng_snapshot/` is a copy of the MASSENG lab package used for these runs. It is not an Atlas engine, and nothing in `engine/` was edited.
- Runs used Python 3.10 (AutoDL server, 21 workers) and Python 3.13 (Linux workspace).
