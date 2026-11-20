# ANCHOR CELLS A3 + A5 — initial results (PHL). Observed only except A3b SIMULATED; no direction claim.

Predeclarations: `A3_PREREG.md`, `A5_PREREG.md` (written before running). Code `code/a3_a5.py`; outputs
`runs/a3_remittances.csv`, `runs/a3b_simulated.csv`, `runs/a5_rivals.csv`, `runs/a3_a5_findings.txt`.
No direction claim (R13/EQUIVALENT); A3b is a SIMULATED design expectation (E3 replication DATA BLOCKED); A3c
DATA BLOCKED; anchor-vs-rival comparison deferred to A1 (exp1 model not built). No git writes.

## A3a — remittances → schooling (OBSERVED, national; predeclared sign/magnitude)
Log-log, Newey–West lag 2, controls log GDP pc + trend, PHL 1995–2024:
| outcome | β | se | n | lead-placebo β (|t|) |
|---|---|---|---|---|
| GER tertiary | **−0.213** | 0.070 | 27 | −0.090 (1.22) |
| GER secondary | −0.018 | 0.041 | 25 | −0.126 (3.33) |
| GER primary | +0.124 | 0.052 | 26 | +0.119 (2.11) |
**Verdict: FAIL** against the predeclared rule (tertiary β must be >0 and in [0.10,1.50]; observed **β = −0.21**).
Remittance inflows are **negatively** associated with tertiary GER in this national record (and ~null for secondary),
with a null tertiary lead-placebo; the secondary lead-placebo fails (|t|=3.3). This is an association on one country's
national record, not a causal/direction claim. Possible channels (declared as interpretation only): remittance-financed
migration/consumption vs schooling, income-control collinearity, or trend absorption.

## A3b — nurse visa 2005–06 (SIMULATED ONLY; E3 replication DATA BLOCKED)
Design expectation, labelled SIMULATED, **no claim**: nursing enrolment +19.4% at the visa expansion vs placebo
fields −4.3% / +3.3% under declared parameters (+10–30% band; placebo |effect|≤5%). This is a power/design statement
for when PRC licensure/CHED enrolment series are secured; not an estimate.

## A3c — BPO/IT regional growth: DATA BLOCKED
No regional/BPO series on disk (PSA blocked); regional exposure gradient not run, not claimed.

## A5 — rival-model comparison on the same PHL record (OBSERVED; rivals only; anchor deferred)
Five reduced-form rivals fitted on the same pre-2013 record (HAC lag 2), predicting 2013–2024 with observed
covariates. Holdout MAE and event-window change error (2012→2016/2018/2024):
| outcome | rival | OOS MAE | RMSE | event-change obs | pred | err |
|---|---|---|---|---|---|---|
| GER secondary | **labour_queue** | **2.81** | 3.57 | +2.5 | +9.2 | +6.7 |
| GER secondary | HC | 3.16 | 3.80 | +2.5 | +6.9 | +4.4 |
| GER secondary | state_building | 8.05 | 8.92 | +2.5 | +13.8 | +11.2 |
| GER secondary | sectoral_demand | 9.54 | 10.46 | +2.5 | −2.0 | −4.5 |
| GER secondary | world_culture | 33.08 | 33.19 | +2.5 | +7.7 | +5.2 |
| GER tertiary | **labour_queue** | **4.37** | 5.07 | +9.1 | +6.6 | −2.5 |
| GER tertiary | HC | 7.80 | 9.55 | +9.1 | +0.4 | −8.7 |
| GER tertiary | sectoral_demand | 8.09 | 9.70 | +9.1 | −0.3 | −9.4 |
| GER tertiary | world_culture | 18.46 | 19.62 | +9.1 | +2.9 | −6.2 |
- **No single rival dominates:** on OOS trajectory labour-queue wins both outcomes; on the **event-break** metric HC
wins GER secondary (error 4.4 vs 6.7). The predeclared EQUIVALENT rule (best/second gap ≤0.5 pp on BOTH MAE and
event-break) is **not met**: GER secondary MAE gap 0.36 but event-break gap 2.3; GER tertiary MAE gap 3.43.
- State-building and sectoral-demand models are UNABLE/weak for the long GER window (regressor coverage 1995+ only,
  declared); world culture is worst everywhere. No rival reproduces the post-2013 event break well (all errors
  ≥|2.5| pp; HC closest on secondary).
- **Anchor comparison deferred to A1;** when the anchor model exists it must beat the best rival on BOTH the
  trajectory and the event-break estimand, or A5 reports EQUIVALENT (R3).

## Stop-rule links
R13/EQUIVALENT (no direction claim), R3 (equivalence), R4 (events exogenous, never fitted), R5 (no
re-parameterisation), R12 (no fitted event effects).
