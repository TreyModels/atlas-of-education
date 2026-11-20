# EXPERIMENTS — M2b (declared partial re-run) and M2c (E1 two-shock recovery test)

Observed vs simulated: M2b is estimation on observed panels; M2c is **SIMULATED only**. Direction claims
remain barred (R13/EQUIVALENT); no model fitting; no git push. Gate ACK: `GATE_ACK_BRIEF013.md` (verbatim
brief-013 §2–§4 + Amendments A1) registered before these runs.

## M2b — declared partial re-run against `10_massification/relations/data/`
Full resolution table and limitations in `AMENDMENT_M2b.md`. Headlines:
- **Lower-secondary completion coefficient is an estimator range, not a point:** +0.84 (M2 between-logit,
  original) → +1.36 (between-logit re-run on landed panel) → +1.97/+2.28 (year-FE log-log reimplementation)
  → scout relay **+1.174**. Resolution = estimator/transform/sample sensitivity, not a data error; exact
  scout script not executable here (path layout) — limitation disclosed.
- **Universalization:** 50 matched logistic cells, median |Δr| 0.061, median |Δt0| 11.1y; scout and model2
  both reject common slopes (country-specific timing); scout's lead-lag tests are predictive-only
  (cannot_discriminate 7/13) and model2's lead-lag was NOT IDENTIFIABLE → **agreement**.
- **What changes:** Part-1 law magnitude → estimator range; Part-2 conclusions unchanged; **task-34 data
  adoption re-run deferred** by instruction (no silent replacement).

## M2c — E1 two-shock estimator recovery (SIMULATED; pre-registered in `M2C_PREREG.md`)
DGP: 30 provinces × 10y; Y = α_i + λ_t + 0.5S + 0.3D + γ·S·D + ε; γ ∈ {−0.30, 0, +0.30}; σ ∈ {0.5, 1.0};
100 sims/cell; estimator = two-way FE OLS with unit+year dummies, CR1 cluster by unit; estimand γ.

| γ | σ | sign accuracy | median \|bias\| | 90% CI coverage | null false-positive |
|---|---|---|---|---|---|
| −0.30 | 0.5 | 0.93 | 0.55 | 0.88 | — |
| −0.30 | 1.0 | 0.74 | 1.11 | 0.88 | — |
| 0.00 | 0.5 | — | — | 0.88 | 0.08 |
| 0.00 | 1.0 | — | — | 0.88 | 0.08 |
| +0.30 | 0.5 | 0.92 | 0.55 | 0.88 | — |
| +0.30 | 1.0 | 0.68 | 1.11 | 0.88 | — |

**Predeclared sufficiency rule (σ=0.5):** sign accuracy ≥0.67 both signs, median |bias| ≤0.50, coverage ≥0.67,
null FP ≤0.10. Result: sign_ok=True, cover_ok=True, nullFP_ok=True, **bias_ok=False (0.55 > 0.50)** →
**E1 NOT SUFFICIENT as the identification gate**: it recovers the interaction *sign* (0.92–0.93) but has a
median ~55% size bias at the low-noise regime; at high noise (σ=1.0) sign accuracy falls to 0.68–0.74 and
bias doubles to 1.11. This is direct evidence for the PATRINOS "underpowered at national scale" warning and
supports requiring a power fix/stronger design before E1 is fielded. If E1 is used sign-only, that must be
predeclared and labelled as sign-identification, not size identification.

## Files
`runs/m2b_scaling.csv`, `runs/m2b_logistic_compare.csv`, `runs/m2b_findings.txt`, `runs/m2b_meta.json`,
`runs/m2c_recovery.csv`, `runs/m2c_findings.txt`, `runs/m2c_meta.json`, `M2C_PREREG.md`, `AMENDMENT_M2b.md`.
