# PRE-REGISTRATION — rural–urban migration/sorting extension (eduengine full-system multiverse)

**Committed BEFORE code and BEFORE any run.** SIMULATION ONLY on `eduengine` toy worlds; all
parameters illustrative; no causal or empirical claims. Extends the committed full-system multiverse
(`research/masseng-edsystem-2026-11-25` @ `b7108da`) with the declared-missing rural–urban
migration/sorting channel, behind a switch.

## 1. Mechanism (declared, not calibrated)

A new `Migration` module in `engine/eduengine/modules/migration.py` acts at the start of each year,
before household continuation decisions. For each **rural child still in the system** (`urban=False`,
`reason<0`, age between entry age and 18), the annual probability of the household moving to an urban
area is

`Pr(move) = sigmoid(b0 − friction + b_cred·cred + b_ability·ability + b_income·log(y/y_median) + b_home·(home−0.5))`

with declared, illustrative coefficients `b_cred=0.35, b_ability=0.45, b_income=0.30,
b_home=0.30`; `friction` = 2.2 (low-friction axis) or 4.0 (high-friction axis); `closed` = no
module at all. On moving: `urban←True`, household income multiplied by `urban_income` (engine
default 1.6), and household school-quality draw shifted upward by the engine's declared urban
quality premium (+0.05, clipped) so urban access/quality and tutoring non-price costs apply.
**No remittances** (not modelled), no urban→rural moves, no spatial job access, no country
calibration. The module is a declared sorting channel (ability/education/income-weighted), not an
estimate.

**Switch-off identity (binding test before the grid):** the `closed` axis level builds exactly the
pre-extension module list (no Migration instance, no migration parameter). For the baseline design
cell and seeds 0–2 the run outputs must be **bit-identical** to the corresponding rows of the
committed `results_multiverse.json` (hash/equality check). If not, stop and report.

## 2. Design axis and grid

Migration axis added to the committed 144-cell multiverse: **closed / low-friction / high-friction**
(each level of the 6 existing axes crossed with the 3 migration levels) × **8 seeds (0–7)** =
**432 design cells × 8 = 3,456 runs** (inside the declared 2,880–4,320 range), N=400, T=70,
measure_from=35, base world `formal_loop`, 12 workers on `ssh -p 45973` (key only; server stays up).
All other settings unchanged from the committed multiverse: affordability (cash-only, credit-constant,
credit-poverty), supply/funding (fixed budget, fiscal loop), learning/supply configuration (public
only, +private, +private+tutoring), gates (bar, quota), jobs (queue floors, competitive), rural
structure (low/high penalty).

## 3. Outcomes

Completion primary/lower/upper/tertiary; wealth parity (lower); tutoring rate; formal share of GDP;
skill premium; public quality. Also the engine's own migration summary (share of rural children who
move) for description.

## 4. Statistical tests (same protocol as `research/edsystem-tests-2026-11-25` @ `aadbbb4`)

For each design-axis contrast and outcome: OLS with **all main effects + seed fixed effects**,
**cluster-robust SEs by design cell** (432 clusters), 95 % CI, **Holm correction across outcomes**,
and **stratum sign consistency** (does the sign hold in every level of every other axis?). An effect
is called supported only if Holm p < 0.05 **and** the sign is consistent across all strata; nulls
are reported as not supported.

Additionally (same estimator/SE/SE-cluster and Holm across outcomes): **interaction terms** for
`migration × gates`, `migration × affordability`, `migration × jobs` (the task requires reporting
migration's interaction with these axes). Interactions use dummy products with the reference levels
used in the main-effect coding; they are reported with 95 % CIs and Holm-adjusted p-values, and are
labelled as regularities of the simulated design.

## 5. Reporting and limits

Report: switch-off identity result; run count/wall time/hashes; migration main effects on completion
by level, wealth parity, tutoring, formal share, skill premium, public quality, with CIs and Holm
status; robust vs not-robust/interaction findings; what remains missing — **remittances, spatial job
access, internal migration flows/age composition, country calibration**; observed vs assumed
unchanged from the committed report (task-41 data map). Every result is a toy-world simulation, not a
causal or empirical claim. Stop/report on switch-off failure, engine error, >2 % non-finite metrics,
or wall >40 min.

## Deviations log
- (to be filled before any affected run)
