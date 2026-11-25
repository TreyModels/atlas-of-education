# GATE-1 MIGRATION TABLE — old (pre-repair) vs repaired engine, unmodified 540 config

**Evidence status: REPRODUCED SIMULATION.** This is a replication of the 540-run configuration on the repaired
engine (`98baf6b`), **not a calibration and not a validated simulation**. The canonical spec is **not frozen**
(Lead decision), and no parameter was re-estimated.

## Provenance of the "new" run

| item | value |
|---|---|
| source | **box cross-env run**, because the host authoritative run failed **twice** in the ProcessPoolExecutor completion phase (see `GATE1_HANG...` → `GATE1_POOL_HANG_INCIDENT.md`); host run wrote no output, was killed; box run completed |
| engine tree | clean `git archive 98baf6b` (`f31e176` gate1a + `6bc8d61` gate1b + `1a6f3d5`/`23a0173` gate1c), deployed as `/root/work/cmd/engine` from `box540.tar.gz` |
| runner | **unmodified** legacy 540 runner except `workers = 6` (worker count only; see one-line change) |
| environment | AutoDL box, Linux x86_64, 10-CPU cgroup (`cpu.max=1000000 100000`), `/root/work/venv-declared` **py 3.10.8, numpy 2.2.6, scipy 1.15.3** (declared stack) |
| wall / exit | `Completed 540 runs in 2960.4s`, 540/540, exit 0 |
| output | `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json`, 435,872 B, sha256 **`455649daf2a1e3367820004c3338deb41236991814887c295b6e7a2bb634ec21`** |
| schema check | 540 seed rows, same seed-row keys and 18-arm summary schema as the old output; `metadata = {repo, branch, base_commit, n_arms:18, n_seeds:30, total_runs:540, elapsed_seconds:2960.41, history_api}` (branch/base strings are hard-coded in the runner) |
| repaired-engine file hashes | core.py `72cbddf7…`, rng.py `ada4a760…`, contest_math.py `23a01730…`, labour.py `0ccfb3ce…`, tutoring.py `7a6fd4c3…`, planning.py `13d91bc9…` (archive of `98baf6b`) |

**Old run** = Gate-0 reproduced pre-repair 540 output (Commander independent run):
`results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json`, sha256 `722c370b…af54` (REPRODUCED
SIMULATION vs the bundle reference, see `GATE0_VERIFICATION.md`).

## Migration table (30-seed means; index old→new)

| jur | arm | spend index | elite Q5 % | Q5−Q1 gap (pp) | Q5/Q1 spend ratio |
|---|---|---|---|---|---|
| HK | Baseline | 100.00 → 100.00 | 46.36 → **25.01** | 70.63 → **34.76** | 39.81 → **2.47** |
| HK | CF1a (+50 % tax/price) | 107.42 → 96.49 | 52.43 → 24.67 | 69.01 → 35.21 | 90.33 → 2.63 |
| HK | CF1b (cap −50 %) | 67.39 → **97.21** | 41.96 → 23.72 | 74.37 → 34.61 | 19.57 → 2.26 |
| HK | CF2a (S=0.28) | 110.29 → 109.25 | 42.91 → 24.84 | 71.97 → 32.63 | 37.03 → 2.24 |
| HK | CF2b (S=0.50) | 149.30 → 131.76 | 33.62 → 22.99 | 72.62 → 25.33 | 18.24 → 1.72 |
| HK | CF3a (ΔV −30 %) | 76.98 → 82.44 | 51.03 → 24.56 | 70.00 → 36.68 | 64.45 → 2.75 |
| HK | CF3b (ΔV −50 %) | 59.11 → 70.88 | 59.02 → 23.64 | 68.71 → 36.37 | 66.35 → 2.81 |
| HK | **CF4a** | 43.78 → **70.58** | 48.64 → **23.44** | 73.56 → 36.40 | 39.20 → 2.76 |
| HK | **CF4b** | 90.88 → 89.98 | 35.98 → 23.11 | 78.04 → 34.47 | 59.11 → 2.42 |
| KR | Baseline | 100.00 → 100.00 | 36.12 → **22.13** | 68.36 → **29.71** | 18.01 → **2.11** |
| KR | CF1a | 106.46 → 96.88 | 41.75 → 21.57 | 66.22 → 28.91 | 25.72 → 1.98 |
| KR | CF1b (cap −50 %) | 76.42 → **99.25** | 26.39 → 22.00 | 67.08 → 29.72 | 13.72 → 2.06 |
| KR | CF2a | 107.17 → 111.57 | 31.08 → 22.27 | 67.58 → 28.09 | 16.22 → 2.07 |
| KR | CF2b | 128.00 → 156.76 | 22.01 → 22.13 | 55.24 → 16.23 | 3.75 → 1.61 |
| KR | CF3a | 76.63 → 83.42 | 41.96 → 21.69 | 68.61 → 31.06 | 20.32 → 2.19 |
| KR | CF3b (ΔV −50 %) | 57.36 → 72.55 | 47.66 → 21.48 | 67.03 → 30.85 | 25.81 → 2.29 |
| KR | **CF4a** | 46.50 → **72.48** | 34.10 → **21.47** | 67.42 → 30.92 | 19.37 → 2.28 |
| KR | **CF4b** | 88.04 → 105.54 | 26.51 → 22.09 | 65.44 → 28.68 | 11.57 → 2.06 |

**Calibration benchmarks (KR):** participation target 76.5 % (unchanged 57.4→58.4 %); Q5−Q1 gap target 32.1 pp
(**68.4 → 29.7**, now 2.4 pp below target); Q5/Q1 spend ratio target 3.4× (**18.0 → 2.11**, now below target —
over-correction). HK Grade-9 53.8 % / Grade-12 71.8 % targets are not re-checked here (no grade-level participation
series in this comparison). **These are not calibration results.**

## CF4 pre-stated Win-Win verdict (spend index < 80 AND elite Q5 below same-jurisdiction Baseline, both jurisdictions)

| arm | OLD (pre-repair 540) | NEW (repaired engine, uncalibrated 540) |
|---|---|---|
| CF1b (cap −50 %) | **TRUE** (only arm) | **FALSE** (HK spend 97.21, KR 99.25 ≥ 80) |
| CF3b (ΔV −50 %) | FALSE | **TRUE** (HK 70.88 / 23.64 < 25.01; KR 72.55 / 21.48 < 22.13) |
| **CF4a (ΔV −50 % + cap)** | FALSE (HK elite 48.64 > 46.36) | **TRUE** (HK 70.58 / 23.44 < 25.01; KR 72.48 / 21.47 < 22.13) |
| CF4b (ΔV −50 % + seats) | FALSE (spend 90.88/88.04) | FALSE (HK 89.98; KR 105.54 — spend fails) |
| all others | FALSE | FALSE |

**The CF4 verdict flips with the repair** (CF4a now passes both jurisdictions; CF1b no longer does). This is a
**conditional simulation result under the uncalibrated 540 config**, not an established policy effect; it is exactly
the spec/model-dependence the canonical-spec + recalibration decisions must resolve. The old CF4 failure remains
reported; the flip must be reported, not suppressed.

## Baseline absolute decomposition (30-seed means) — why the spend index collapses

| jur | K-12 spend (wage units) | participation % | elite Q5 % | gap pp | spend ratio | contest effort mean |
|---|---|---|---|---|---|---|
| HK old → new | 1343.42 → **156.54** (−88.3 %) | 59.07 → 61.92 | 46.36 → 25.01 | 70.63 → 34.76 | 39.81 → 2.47 | 2.192 → **0.042** |
| KR old → new | 1068.11 → **135.05** (−87.4 %) | 57.44 → 58.38 | 36.12 → 22.13 | 68.36 → 29.71 | 18.01 → 2.11 | 1.711 → **0.016** |

**Decomposition:** participation is essentially unchanged; contest-prep effort collapses ~98–99 %; the spend index
collapse is therefore the **expected-probability mis-pricing**, not a change in school-tutoring demand: pre-repair
the household's expected admission probability was ~2.4× (KR G12) / ~2.0× (HK G12) the realised PL probability
(Phase-A tracer: KR 0.292 vs 0.121; HK 0.455 vs 0.232), so households over-bought positional preparation; after the
D2 repair the expected probability is exactly the PL object (per-gate expected/realised = 1.0000), so they buy far
less. Contest prep was ~92–94 % of pre-repair K-12 household spending in this config (engine-core Phase A), which is
why the index moves so much.

**Interpretation (must be quoted with its label):** a large part of the "540 design lost the Korean calibration"
finding (gap 68→30 pp; ratio 18→2.1×) is a **contest-probability-consistency artefact**, not a parameterisation
problem. The remaining gap/ratio deviations from target (29.7 vs 32.1 pp; 2.11 vs 3.4×) still need Gate-2
calibration, with the spec frozen first. **REPRODUCED SIMULATION, uncalibrated, not VALIDATED.**
