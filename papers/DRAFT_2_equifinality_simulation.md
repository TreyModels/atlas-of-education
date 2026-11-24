# DRAFT — Equifinality and the phase surface in a toy education system

**SIMULATION ONLY — `eduengine` toy worlds; illustrative parameters; no country calibration, no empirical
validation, no causal claims.** Working draft, 25 Nov 2026. Evidence: `research/records/2026-11-25-equifinality-phase/`
(branch `research/equifinality-phase-2026-11-25` @ `ab415f2`; pre-registration `078cc13`).

## Abstract

We ask whether a toy schooling system exhibits **equifinality**: distinct parameter cells that reach almost the
same participation while differing sharply in who is excluded and in shadow-education uptake. A 20 × 20 grid
(formal-vacancy bottleneck × liquidity slack) × {`bar`, `quota`} exam-gate regimes × 20 seeds = **16,000 runs**
(800 cells) is searched exhaustively (all 319,600 cell pairs) against a pre-registered predicate and a
1,000-permutation label null. **Result: no evidence of equifinality beyond chance** — 176 within-gate qualifying
pairs versus a null mean of 190.52 (one-sided p = 0.838). Near-identical simulated participation tends to come
with near-identical exclusion composition: the toy surface is positively coupled, not an equifinality landscape.
A cross-gate excess (4,132 pairs, p = 0.001) is almost entirely a discrete gate-regime tutoring contrast and is
reported separately, not pooled. A requested third gate arm (`contest`) is **NOT-IMPLEMENTED** and was not
proxied: the engine has only `bar`/`quota`, and an unknown kind is silently executed as `quota`.

## 1. Question and design

Equifinal pair (pre-registered): seed-mean cells with
`|ΔGER_sim| < 0.5 pp` **and** (`|Δliq_share| > 25 pp` **or** `|Δtut_rate| > 20 pp`), all in percentage points,
`GER_sim = 1 − never_enrolled_share` (a **declared simulated participation** measure, not empirical GER).

- X = `vac0`, formal vacancies per cohort entrant: 20 geometric levels 0.0100…0.8000.
- Y = `fee_primary`, primary fee as share of median income: 20 levels 0.00…0.19 (0.00 = abolition slice).
- Gates: `bar` (fixed thresholds) and `quota` (cohort-scaled seats, endogenous cutoff).
- Fixed: `formal_loop` world, N = 400, T = 70, `measure_from` = 35, `queue_on` = True; exits read only from
  `e.exits` (survivors = `censored`); seeds 0–19 identical in every cell.

**Requested vs run.** The brief asked 20 × 20 × {bar, quota, contest} × 20 = 24,000 runs. Only **16,000** were
run (bar + quota, 800 cells). `contest` is **NOT-IMPLEMENTED** for four documented reasons (prereg §3, before
the run): (i) no gate hook exists on the `Module` base (`core.py` L60–69); the gate decision is inlined in
`Engine.step`; (ii) the dispatch is `if kind == 'bar' … else: # quota`, so an unknown kind is **silently treated
as quota** (`core.py`:164, 369–371) — a silent proxy, which the brief forbids; (iii) `grep contest` over the
engine returns one comment (`labour.py`:39) and `worlds.py` defines only bar/quota; (iv) at fixed N = 400 the
quota rule is already a fixed-seat rank tournament, so an absolute-seat contest would be arithmetically
identical without editing `core.py` (prohibited). The gap is stated, not hidden.

## 2. Validity and reproducibility

- 16,000/16,000 runs completed, 0 failed; elapsed 1,100.4 s at 12 workers on the warm box.
- Exit partition sums to 1 on **every one of the 16,000 rows** (max |dev| 2.0 × 10⁻⁹, tol 1e-6).
- `ger_sim = 1 − never_share` (max diff 1.1 × 10⁻¹⁶); per-cell seed means recomputed from the raw CSV match the
  committed summary (max diff 0.0).
- **Reproducibility:** a fresh 360-run re-run of 18 cells reproduced the full run **bit-for-bit** (18,360 field
  comparisons, 0 mismatches).
- Runner and 15 engine files pinned by sha256 in the run JSON; the median seed-level SD of `GER_sim` is
  **0.236 pp**, so the 0.5 pp tolerance is ≈ 2.1 × seed noise (a real constraint, not noise).

## 3. Result

**Within-gate (primary family; bar–bar + quota–quota = 159,600 pairs).** Observed **176** qualifying pairs
(bar 161, quota 15) against a 1,000-permutation null with mean **190.52**, SD 15.73, 97.5th percentile 221,
max 247. One-sided **p = 0.838**, observed/null ratio 0.92. → **NO EVIDENCE OF EQUIFINALITY BEYOND CHANCE.**
The surface is positively coupled: where participation is near-equal, exclusion composition also tends to be
near-equal, and the count is *below* chance.

| family | observed | null mean | null SD | 97.5th pct | ratio | one-sided p |
|---|---|---|---|---|---|---|
| within-gate (primary) | 176 | 190.52 | 15.73 | 221 | 0.92 | **0.838** |
| — bar | 161 | 170.22 | 14.87 | 199 | 0.95 | 0.738 |
| — quota | 15 | 20.30 | 4.46 | 29 | 0.74 | 0.900 |
| cross-gate (secondary) | 4,132 | 3,908.13 | 60.94 | 4,030 | 1.057 | 0.001 |
| all pairs | 4,308 | 4,098.66 | 63.58 | 4,229 | 1.051 | 0.001 |

The qualifying set is **thin** and structured: 89 distinct cells; max degree 15; x-only 35, y-only 0, both 141;
via liquidity 161, via tutoring 15, both 0. The top pairs are the X-extreme contrast at the abolition end:
`bar vac0 0.0100, fee 0.00` (GER 99.11, liquidity exits 4.53 pp, tutoring 27.84 pp) vs `bar vac0 0.5044, fee 0.00`
(GER 99.54, liquidity exits 32.62 pp, tutoring 22.16 pp): ΔGER +0.43 pp, Δliq +28.1 pp. The largest within-gate
gaps just clear the thresholds (max |Δliq| 28.09 pp, max |Δtut| 20.36 pp).

**Cross-gate (secondary, not pooled).** 4,132 vs 3,908 (p = 0.001), but 97.2% are driven by `|Δtut| > 20 pp`
alone: tutoring is 22.0–30.5 pp under `bar` but 34.6–57.3 pp under `quota`. That is a discrete gate-regime effect,
not smooth equifinality, and the pre-registered primary family excludes it for exactly that reason.

**Secondary outcome.** `completion_lower`: **0** pairs at |ΔGER| < 0.5 pp and |ΔCL| > 20 pp (quota pins
completion at ~55 pp across the plane). Descriptive only.

**Phase-boundary diagnostics** (no verdict; the sibling phase-transition lane owns that rule): the sharpest grid
edge is liquidity under `bar` (J_max 28.1, sharpness 29.5); tutoring is sharpest under `quota` (J_max 18.0,
sharpness 28.3). The quota gate binds (realised pass rates ≈0.92/0.96 at the two gate indices), while the four
`bar` thresholds are near-non-binding (≈0.995–0.999) — so in these cells the gate factor is effectively
"selection vs little selection".

## 4. What this does and does not say

- It does **not** say anything about any real education system; `eduengine` is uncalibrated and illustrative.
- It does **not** estimate a causal effect of fees, vacancies or gates.
- It **does** show that, in this toy world, "same participation, different regime" appears in the catalogue
  (176 pairs) but **less often than chance**, and that the regime contrast that most separates shadow education
  is the discrete bar-vs-quota switch, not a smooth phase boundary.
- The pre-registered thresholds are strict; the null choice (independent permutation of each outcome vector
  within gate) is declared and matters. No threshold or cell was changed after seeing data.

## 5. Reproduction

`data/phase_sweep_full_runs.csv` (16,000 rows), `…_summary.csv/.json`, `data/equifinality_*.json/csv`,
`data/validity_checks.json`, `data/analysis_manifest.json`, `REPORT.md`. Runner `phase_sweep_full.py`
sha256 `e6fe8aa8…`; analysis `analyze_equifinality.py`; engine hashes in the run JSON. Lead independent
recomputation: pair counts (176/4,132/4,308) and regenerated 1,000-permutation null matched exactly.

**SIMULATION ONLY — no causal or empirical claims.**
