# Rigor experiments: identification, falsification and external checks

Added 16 November 2026, on top of the research workbench (`research/README.md`, `research/lab.py`). Same runner, same
hashing, same rules: a plan is frozen, failures stay visible, and a new plan is needed whenever source or inputs change.

The workbench's factorial probes ask *what each model does under declared assumptions*. These six families ask
the questions a referee in computational sociology would ask next:

1. **Could the data tell the explanations apart at all?** Model-recovery studies (Wilson & Collins 2019): simulate
   data from each structure, add realistic measurement error, and see whether the analysis recovers the structure
   that generated it. If it cannot, no fit or evidence value on real data can rank the explanations
   (Robert et al. 2011 on ABC model choice). The same tables show which *new* observation would make them separable.
   This is the step that turns "the models can't be distinguished" into a fieldwork design.
2. **Does an interpretation survive a placebo?** Moving the China step to months where no policy happened
   (Abadie et al. 2010 placebo logic).
3. **Does the model forecast better than a naive rule, with a proper test?** Rolling origins inside one measurement
   definition, Diebold–Mariano with the HLN small-sample correction (Diebold & Mariano 1995; Harvey et al. 1997;
   Hyndman & Koehler 2006).
4. **Is a correlation stronger than trending alone?** Spurious-regression benchmarks (Granger & Newbold 1974).
5. **Does a policy response match the one experiment that measured it?** The Cambodia cash lever against the CESSP
   scholarship regression discontinuity (Filmer & Schady 2011).

The pass/fail thresholds are in `protocols_rigor.json` and were written before any run. `analyze.py` applies them
mechanically. All empirical targets had already been seen, so none of this is a prospective test.

## The families

| Family | Model | What it tests | Verdicts it can return |
|---|---|---|---|
| `credential_recovery` | credential floor + new `engine/relfloor_gate.py` | Whether HC / POS / REL / GATE are recoverable from (D0) today's wealth profiles, (D1) plus a premium shock, (D2) plus a change in an eligibility rule, (D3) all | DISCRIMINATES / PARTIAL / DOES NOT DISCRIMINATE, per design, over the prior and near the data |
| `shadow_recovery` | tutoring ABM | Whether thin / diversion / favour are recoverable from the seven published patterns, and which field observation (classroom instruction by teacher status, purchases by teacher status, coverage by wealth, response to a ban or to more class time) would separate them | same |
| `youth_placebo` | China youth | Whether August 2021 fits better than 24 placebo step months | AUG-2021 SINGLED OUT / NOT SINGLED OUT / MIXED |
| `youth_rolling` | China youth | Rolling-origin forecasts 2020-06 to 2022-12 → June 2023, against random walk, seasonal naive and lake null | model better / worse / no detectable difference (DM-HLN, 5%) |
| `fertility_placebo` | fertility page | Levels R² against independent random walks with the same drift and volatility, and against other places' covariates | stronger than trending / NOT DISTINGUISHABLE FROM TRENDING |
| `camchild_validation` | Cambodia child labour | Cash-lever effect on attendance of poor 12–13-year-olds at US$45 and US$60, at the calibrated baseline and at era-matched baselines | CONSISTENT / LEVEL TOO LARGE / LEVEL TOO SMALL / DOSE RESPONSE TOO STEEP |

`analyze.py` also reads the workbench's `schools` family. It adds Diebold–Mariano tests against the flat benchmark
and marks series with fewer than 10 forecasts as anecdotal.

### The eligibility gate (credential floor)

In the current model the relational value is an additive constant `b_rel`. `M_GATE` replaces it with an
institutional mechanism. A share G_t of desirable jobs screens on the certificate (Collins 1979; Bills 2003). The
certificate is necessary but not sufficient: access also needs connections, which rise with household income. The
household values completion by `b_gate × G_t × access(income)`. That gives the relational account two observable
implications the constant lacks. Completion responds to a change in the screening rule, and the response has a
wealth gradient. With `b_gate = 0` the new simulator reproduces `relfloor_countries.sim` draw for draw (tested).
Every gate parameter is an assumed range. Breen & Goldthorpe's (1997) relative-risk-aversion model is the obvious
next rival structure to add; it is cited in the protocol but not implemented.

## Run

Verification first (seconds):

```bash
python -m unittest research.tests.test_rigor -v        # from the repo root; or: python -m unittest discover -s research/tests
python research/lab.py plan --profile smoke --families credential_recovery shadow_recovery youth_placebo youth_rolling fertility_placebo camchild_validation --draws 2 --replicates 1 --out research/runs/rigor-smoke
python research/lab.py run --out research/runs/rigor-smoke --jobs 4 --timeout 900
python research/rigor/analyze.py --run research/runs/rigor-smoke
```

Smoke numbers mean nothing. A first substantive batch, budgeted for an 8-core laptop (times are rough, from a
2-core preview):

```bash
# fast (minutes)
python research/lab.py plan --profile main --families fertility_placebo camchild_validation --draws 32 --replicates 2 --out research/runs/rigor-fast
python research/lab.py run --out research/runs/rigor-fast --jobs 6 --timeout 1800
# recovery tables (about 1-2 h); raise --draws until each structure has >= 100 simulations within 15 points of the profiles
python research/lab.py plan --profile main --families credential_recovery --draws 32 --out research/runs/rigor-credential
python research/lab.py run --out research/runs/rigor-credential --jobs 6 --timeout 7200
python research/lab.py plan --profile main --families shadow_recovery --draws 64 --out research/runs/rigor-shadow
python research/lab.py run --out research/runs/rigor-shadow --jobs 6 --timeout 7200
# China (about 1-3 h; draws = optimiser restarts per cell, the first warm-started from the headline fit)
python research/lab.py plan --profile main --families youth_placebo youth_rolling --draws 3 --out research/runs/rigor-youth
python research/lab.py run --out research/runs/rigor-youth --jobs 6 --timeout 7200
# analysis across runs, including the earlier workbench pilots for the schools table
python research/rigor/analyze.py --run research/runs/rigor-credential --run research/runs/rigor-shadow --run research/runs/rigor-youth --run research/runs/rigor-fast --run research/runs/mechanism-pilot
```

Do not edit anything under `engine/`, `experiments/`, `inputs/` or `research/` while a batch runs: the runner
re-hashes them at the end and rejects the batch if they changed.

## Before citing any verdict

- **Cambodia:** copy the Filmer & Schady (2011) point estimates and intervals into
  `protocols_rigor.json → criteria.camchild_filmer_schady`, with table and page. Do the same for the
  comparison-group attendance used to choose the era-matched baselines. The current band (0.15–0.35, dose difference
  ≤ 0.05) is a placeholder built from the paper's headline. The adult wage range W (US$350–700) is unsourced; CSES
  2004 or 2007 wage tables would fix it.
- **Recovery studies** answer "could this design tell the structures apart *if one of them were true*?" They do
  not say which is true. The observation-error SDs are declared assumptions; rerun with your own if you know the
  survey design.
- **Placebo LR** uses an iid Gaussian approximation; residual autocorrelation makes "singled out" verdicts weaker
  than they look.
- **Forecast DM tests** pool overlapping horizons from six origins. Small n; treat p near 0.05 as indicative.

## How to contribute

Each verdict names the assumption that would overturn it: a noise SD, a prior range, a benchmark, a target band.
Challenge one by opening a model-challenge issue (`.github/ISSUE_TEMPLATE/model-challenge.yml`). Change the declared
value in a dated amendment, then rerun into a new directory. A result that flips under a defensible alternative is a
finding about the model.
