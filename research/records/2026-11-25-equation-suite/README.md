# Master Equation Inventory experiment suite (task-40)

**Record:** `research/records/2026-11-25-equation-suite/` · branch `research/equation-suite-2026-11-25`.
**Pre-registration:** `PRE_REGISTRATION.md` (committed before code: `dabc458`), plus Amendments 01–03 (system-map
alignment, final massification scope, MASSENG v5 boundary labels) committed before any run.
**Status:** synthetic-equation demonstration suite. **No causal claims. No invented citations. Not MASSENG v5
output.**

## What this is

Ten self-contained experiments, one per part of the massification system, built around the chain
**family affordability (incl. forgone earnings) → learning (school + tutoring) → limited-place selection gate →
credential→jobs**, with migration, inequality/dashboard, growth and a test bench as the wider system. Tutoring
is exactly one module (the exams-shadow part). Each script varies defensible equation choices (multiverse) and
reports the range and sign-robustness, rather than one specification.

## Mapping table (system part × connected piece × multiverse × data)

| # | Script | System part (Codex map) | Piece | Multiverse specs (equation choices) | Data tier | In MASSENG v5? |
|---|---|---|---|---|---|---|
| S1 | `eq01_family_demand.py` | families: budgets, demand, forgone earnings, credit | 1 affordability | income-only budget; forgone-earnings budget; credit-constrained; zero-signal control | SYNTHETIC | affordability yes; **borrowing no** |
| S2 | `eq02_supply_finance.py` | schools-state, finance, dashboard | 1 affordability / state supply | universal vs means-tested vs quota; supply response; discount 5%/8% | SYNTHETIC | affordability/capacity yes |
| S3 | `eq03_learning_quality.py` | learning, schools-state | 2 learning | linear interaction (no ability); with ability; CES ρ grid; Cobb-Douglas | SYNTHETIC | **learning production no** |
| S4 | `eq04_transitions_gates.py` | stage transitions and gates at all levels | 3 gate | score bar; reserved quota; contest effort; stage progression | SYNTHETIC | progression/capacity yes; **exam bar/quota no** |
| S5 | `eq05_returns_credentials.py` | jobs-credentials | 4 credential→jobs | OLS; 2SLS; experience profile; exact-percentage premium | SYNTHETIC | **labour market/earnings no** |
| S6 | `eq06_migration_rural_urban.py` | wider economy / families | cross-cutting | probit vs logit; with/without network; with/without remittances | SYNTHETIC | **rural-urban no** |
| S7 | `eq07_inequality_dashboard.py` | inequality, dashboard | 4 / distribution | Gini; Theil; IGE; rank-rank; Oaxaca; dashboard panel check | SYNTHETIC + OBSERVED/RECONSTRUCTED dashboard check | **no** |
| S8 | `eq08_growth.py` | wider economy | 4 / macro | convergence with/without H; with/without initial income; Nelson-Phelps; descriptive real cross-section | SYNTHETIC + OBSERVED aggregate cross-section | **no** |
| S9 | `eq09_identification.py` | test bench | cross-cutting evaluation | TWFE; CS-style; OLS vs 2SLS; local-linear RD; synthetic control | SYNTHETIC | n/a |
| S10 | `eq10_tutoring_shadow.py` | exams-shadow (single tutoring module) | 2 learning / gate pressure | Tobit; two-part hurdle; OLS participants; CES ρ {0.3,0.5,0.7}; ban retention {0.5,0.7,0.9} | SYNTHETIC + LITERATURE_TARGETS (Bray check) | **no** |

## How to run

```bash
python scripts/run_all.py --smoke-only --workers 2     # local smoke
OMP_NUM_THREADS=1 python scripts/run_all.py --workers 16   # full run (server)
```

Outputs: `results/<script>.json`, `results/<script>.csv`, `results/run_all.json`,
`results/run_all_manifest.csv` (statuses, wall times, sha256 of every script and output).

## Honest limits

- Every coefficient here is a property of a stipulated DGP or a descriptive association; none is an identified
  causal effect, a country estimate, or a MASSENG v5 output.
- S7/S8 use committed observed/reconstructed panels only for **descriptive** checks, labelled as such.
- S10's Bray targets are a literature reality check; the model is not fitted to them and does not claim to
  reproduce them.
