# Statistical tests of the full-system multiverse (SIMULATION)

Source: `results_multiverse.json` — 1,440 eduengine runs (144 design cells × 10 seeds, N=400,
T=70, measure from year 35). Toy worlds, illustrative parameters; **no causal or empirical claims**.
Script: `test_full_system.py`. Output: `full_system_tests.json`.

## Method
For each design-axis contrast and outcome: OLS with all main effects + seed fixed effects,
**cluster-robust SEs by design cell** (144 clusters), 95% CI, **Holm correction across 9 outcomes**,
and a **stratum check** (does the sign hold in every level of every other axis?). An effect is called
supported only if Holm p < 0.05 **and** the sign is consistent across all strata. Nulls are reported as
not supported, not hidden.

## Supported effects (all Holm p < 0.05 and sign-consistent across strata)

**Family credit (vs cash only)** — the biggest access lever:
| outcome | credit_constant | credit_poverty |
|---|---|---|
| primary completion | +13.2 pp [12.6, 13.9] | +11.3 pp [10.6, 12.0] |
| lower completion | +3.5 pp [2.0, 5.1] | +2.6 pp [0.9, 4.2] |
| upper completion | +3.8 pp [2.2, 5.4] | +3.0 pp [1.4, 4.5] |
| tertiary completion | +6.6 pp [5.6, 7.7] | +13.2 pp [12.1, 14.4] |
| wealth parity (lower) | +12.7 pp [11.3, 14.1] | +8.0 pp [6.6, 9.4] |
| skill premium | −0.22 [−0.25, −0.19] | −0.39 [−0.42, −0.35] |
| tutoring rate | ns | −2.0 pp [−3.6, −0.4] |

**Gates: quota vs bar** — pushes out and pushes prep up:
lower completion **−17.0 pp** [−18.4, −15.7]; upper **−16.0 pp**; tertiary **−9.9 pp**;
tutoring **+22.6 pp** [21.3, 23.9]; wealth parity **−1.4 pp**; skill premium **+0.324**;
public quality **+0.024**.

**Jobs: competitive vs queue-with-floors**:
formal share **+33.4 pp** [32.4, 34.4]; primary completion +5.4 pp; lower +3.9 pp;
wealth parity +6.4 pp; public quality +0.105.

**Rural: high vs low penalty** — compounds disadvantage:
primary −3.2 pp; lower −5.0 pp; upper −4.4 pp; tertiary −5.3 pp; tutoring −6.8 pp;
formal share −2.1 pp; wealth parity **−14.6 pp**; skill premium +0.16.

**Learning: private/tutoring vs public only** (smaller than the structural axes):
primary completion +1.6 pp (+private) / +3.5 pp (+private+tutoring); tertiary +3.3 pp (tutoring);
formal share +4.7 pp; skill premium −0.089; public quality +0.04.

**Supply: fiscal loop vs fixed budget**: only public quality is supported (+0.132 [0.115, 0.149]);
completion effects are not supported.

## What this means
In this toy full system, the structural axes — **credit access, gate design, jobs/credential regime,
rural penalty** — dominate attainment and distribution. Tutoring is a real but second-order channel
(+3.5 pp primary completion, −0.09 skill premium), and it reacts strongly to gates (+22.6 pp under quota).
The "shadow education" story is a small corner of a system whose main levers are affordability, gate
design, jobs, and rural disadvantage.

## Limits
Toy eduengine, illustrative parameters; no migration, rural–urban sorting, remittances, country
calibration; p-values describe regularities of the simulated design, not the world. No causal claims.
