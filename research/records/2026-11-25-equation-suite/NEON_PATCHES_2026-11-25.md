# NEON PATCHES — equation suite: what changed, before/after (2026-11-25)

**Branch:** `research/equation-suite-neon-fixes-2026-11-25` (local only, not pushed).
**Base:** `a7fcfb9` = head of `research/equation-suite-2026-11-25`. **Worktree:** `~/neon-boot/wt2/eq`.
**Environment of the re-recorded run:** local Mac (`Treys-MacBook-Air.local`), Python 3.10.2, NumPy 2.2.6,
`nproc 8`, `run_all.py --workers 6`, wall **224.33 s** (the old numbers came from the 192-core server,
Python 3.10.8 / NumPy 1.24.1 — the environment is therefore NOT byte-comparable; every changed number is
re-derived here, not copied).
**Command:** `OMP_NUM_THREADS=1 python scripts/run_all.py --workers 6` → exit code **1** (three decision-rule
failures, listed below; execution failures `[]`).

This file is the before/after record the Lead asked for. Old values are **superseded, not silently overwritten**:
they remain in git at `a7fcfb9` and are quoted in the table. All scripts are SIMULATION / known-truth
demonstrations; no causal claim; not MASSENG v5 output.

## 1. Part A — Neon's verified diff (applied with `git apply --recount`)

Neon's pasted transcription loses the final context line, so plain `git apply` reports "corrupt patch";
`--recount` is required. Post-image blob hashes match Neon's own index hashes:

| file | Neon index hash | post-image hash in this branch | fixes |
|---|---|---|---|
| `eq_common.py` | `26bda9c` | `26bda9c` | probit Newton step (clipped index, score), Tobit-EM inverse-Mills tail + conditional variance + convergence + σ² SEs |
| `eq03_learning_quality.py` | `f96f855` | `f96f855` | CES fit: 2-D (ρ, ω) grid evaluated as normalised CES on the A-scale, scale concentrated out |
| `eq04_transitions_gates.py` | `67e3f2f` | `67e3f2f` | `q` loop-variable shadowing (quota_share gaps were NaN); `mechanism_in_masseng_v5` True→False |
| `eq05_returns_credentials.py` | `a476e12` | `a476e12` | 2SLS gains an intercept and the slope is returned; σ² uses n−k |

Verification: `py_compile` OK on all four; `git hash-object` equals the hashes above.

## 2. Part B — implemented specs (Neon's direct specs, no diff provided)

| file | change | audit item |
|---|---|---|
| `eq09_identification.py` | TWFE unit dummy `np.repeat`, time dummy `np.tile` (they were transposed for the row-major `i*T+t` layout); 2SLS SEs from residuals in **actual D**, not `Dhat`, σ² with n−k | handoff quarantine #4 / Neon line audit: eq09 TWFE transpose, eq09 2SLS residuals |
| `eq07_inequality_dashboard.py` | Gini/Theil/within-between on **exp(child log income)** = level income, strictly positive; domain enforced; Oaxaca stays on log income; `data_tier` includes the observed dashboard check | Theil/Gini domains; audit §4 tier label |
| `eq10_tutoring_shadow.py` | Tobit estimated on **log1p(T)** (left-censored at 0) so its coefficient is the same semi-elasticity as the 0.8 truth; level-scale fit reported separately and never compared to 0.8. Gini on **exp(achievement index)**, strictly positive domain | Tobit vs ground-truth scale; Gini domain |
| `run_all.py` | PASS/FAIL is the script's own `decision_rule.PASS` plus sub-test flags (e.g. S10 Tobit), not `returncode == 0`; statuses PASS / RULE_FAIL / NO_RULE / FAIL(execution); exit code non-zero on any rule failure | `run_all.py` decision-rule parsing |
| `eq_common.py` | `write_result` maps non-finite floats to `null` and dumps with `allow_nan=False` (invalid JSON literal can no longer be committed) | QA: eq04 had 12 literal `NaN`s |
| `eq04` / `eq06` | plain summaries rewritten to say what the output says (S4 quota "flips" → does not flip and the pre-declared rule FAILS; S6 "networks increase" → networks slightly reduce and the ad-hoc criterion FAILS); eq04 MASSENG note split (progression/capacity in v5; exam bar/quota out) | audit §6.3, §6.4, §4 |

## 3. Before → after, every number claimed to change

| script | claim | before (`a7fcfb9`) | after (this branch) | how checked |
|---|---|---|---|---|
| eq03 | decision_rule.PASS | False | **True** | own JSON; full run |
| eq03 | median ρ̂, CES world (truth 0.5) | 0.2 | **0.6** | own JSON; 2-D grid on the A-scale |
| eq03 | share of ρ̂ within 0.10, CES world | 0.0 | **1.00** | own JSON |
| eq03 | CES RMSE, CES world (vs CD 0.5578) | 0.3762 | **0.2910** | own JSON |
| eq03 | median ρ̂, linear world (truth 1.0 = CD) | 0.2 | **1.00** (share within 0.10 = 0.69) | own JSON |
| eq04 | quota_share_{0.4,0.5,0.6} gaps | NaN | **0.2593 / 0.0906 / −0.0912** | own JSON; 12 NaN literals removed |
| eq04 | multiverse range | [0.5472, 0.7614] | **[−0.0912, 0.7614]** | own JSON |
| eq04 | `mechanism_in_masseng_v5` | True | **False** (+ note split) | own JSON |
| eq04 | decision_rule.PASS (pre-declared) | False | **False (unchanged)** | quota gap +0.0906 does not flip |
| eq05 | 2SLS coefficient | 0.0836 | **0.0897** | own JSON |
| eq05 | mean 2SLS bias under ability bias | −0.0064 | **−0.0003** | own JSON |
| eq05 | exact-percentage mean | 8.76 | **9.39** | own JSON |
| eq06 | probit no-network marginal effect | 0.01402 | **0.01404** | probit patch side-effect; own JSON |
| eq06 | decision_rule.PASS (ad hoc) | False | **False (unchanged)** | network 0.00892 < 0.01404 |
| eq07 | Theil within, null / persistent | NaN / NaN | **0.5042 / 0.6141** | own JSON; strict JSON parse |
| eq07 | Gini of child income, null / persistent | 0.2024 / 0.2402 | **0.5224 / 0.6006** | level income |
| eq07 | Theil between, persistent | 0.0128 | **0.0951** | level income |
| eq07 | top-level data_tier | SYNTHETIC | **SYNTHETIC + OBSERVED/RECONSTRUCTED descriptive** | own JSON |
| eq09 | TWFE mean | 0.785 | **0.138** | independent within-transformation check to 2e-14 |
| eq09 | TWFE bias (true ATT 1.284) | −0.499 | **−1.146** | own JSON |
| eq09 | null-world TWFE mean | −0.023 | **0.003** | own JSON |
| eq09 | IV SE mean | 0.082 | **0.045** | own JSON |
| eq10 | Tobit η̂, single / different (level scale) | 7.499 / 7.631 | level-scale 8.612 / 8.781 **reported but not compared to 0.8** | own JSON |
| eq10 | Tobit η̂ on the truth's scale (log1p) | — (not on this scale before) | **1.441 / 1.370** | own JSON |
| eq10 | two-part η̂, single / different | 0.802 / 0.733 | 0.802 / 0.733 (unchanged) | own JSON |
| eq10 | ΔGini(ban) range over 9 CES/retention specs | 0.0247 … 0.3721 | **−0.0642 … −0.0406** | own JSON; sign robust to a common additive shift too |
| eq10 | decision_rule.PASS | True | **False** | ban_raises_gini_in_all_specs = False |
| run_all | PASS criterion | `returncode == 0` (all ten "PASS") | **decision_rule.PASS**: 7 PASS, 3 RULE_FAIL (eq04, eq06, eq10), 0 execution failures | full run; exit code 1 |
| JSON | NaN/Infinity literals | eq04 12, eq07 3 | **0** (11/11 files strict-parse; 0 non-finite→null substitutions) | `json.loads(..., parse_constant=raise)` |

**Scripts no fix touched (S1/S2/S8).** S1 and S8 reproduce their committed JSON values exactly (only
`generated_utc` differs; CSVs unchanged). S2's CSV differs on one last digit for replication 16
(0.3355 → 0.3354) — floating-point/environment difference between the old server (NumPy 1.24.1) and this
re-record (NumPy 2.2.6), not a code change. S6 shifts at the 4th decimal because it uses the patched
`eq_common.probit` (0.01402 → 0.01404).

## 4. Verdict accounting — corrected framing

It is **not** "3 pre-declared FAILs". 10/10 scripts executed; **3 decision-rule failures**, of which:

- **S4 / eq04 — pre-declared FAIL.** The old S5 rule ("quota flips the admission gap") is applied exactly.
  Bar gap +0.5472 > 0, quota gap **+0.0906** (not < 0), contest +0.7614 → FAIL. The old plain summary said
  the quota "flips the gap (0.091)", which contradicted its own number; corrected.
- **S6 / eq06 — post-hoc FAIL.** Migration is a new script created by Amendment 02; the pre-registration lists
  its multiverse choices only, with no decision rule. The implemented rule ("education positive in every spec"
  AND "network effect larger than no-network") is ad hoc: network 0.00892 < no-network 0.01404 → FAIL. It is
  reported as a post-hoc criterion, not a pre-declared one.
- **S10 / eq10 — FAIL, and also fails a dropped pre-registered rule.** The implemented rule fails on
  `ban_raises_gini_in_all_specs` (see §3). Independently, the old S3 tutoring-demand rule required, in the
  SINGLE-process world, **both** estimates within 0.15 of 0.8; on the aligned scale the Tobit is 1.441
  (`tobit_within_0.15_share = 0.0`) → the dropped pre-registered sub-rule still fails. Reported explicitly
  instead of hidden behind the old 7.499-vs-0.8 scale artefact.
- **S3 / eq03 currently PASSES**, but note its `rho_recovered_within_0.10` criterion is itself post-hoc
  (the pre-registered S2 rule is "recovered ρ closer than Cobb–Douglas implies", which also passes: 0.6 vs
  truth 0.5 vs CD 1.0). This is logged as a deviation in `SUITE_REPORT.md`.
- Failure count by criterion is therefore **1 pre-declared (S4) + 1 post-hoc (S6) + 1 post-hoc/dropped-rule
  (S10)**; it is not a count of pre-declared failures.

## 5. Pre-registration deviations that must be logged (QA demand 2)

**(a) eq03 CES estimator: 2-D (ρ, ω) grid vs the pre-registration's 1-D grid over ρ.** The pre-registration
(S2 learning production) says "CES fit by 1-D grid over ρ with linear coefficients concentrated out". Neon's
Part A patch made it a 2-D grid over (ρ, ω). This is a deviation and it is undisclosed in the old record. Does a
1-D-grid PASS exist? Experiment on the same seeds/reps (150 × n=4000, CES world ρ=0.5, fixed normalised-CES
objective, ω fixed at the DGP's ω=0.6):

| 1-D grid, fixed ω | median ρ̂ | share within 0.10 |
|---|---|---|
| ω = 0.4 | 1.00 | 0.00 |
| ω = 0.5 | 0.90 | 0.00 |
| **ω = 0.6 = DGP ω** | **0.60** | **1.00** |
| ω = 0.7 | 0.30 | 0.00 |
| 2-D (ρ, ω) grid (Part A) | 0.60 | 1.00 |

So a 1-D-grid PASS **does** exist, but only if ω is pinned at its DGP value (an oracle choice); with any other
fixed ω it fails. The 2-D grid makes the PASS independent of knowing ω. The PASS flip itself is caused by the
**corrected normalised-CES objective on the A-scale** (the old estimator regressed A^ρ on (1, S^ρ, T^ρ) and
returned ρ̂=0.2 in both worlds); the ρ grid being 2-D is a deviation that removes the oracle dependence.

**(b) `ir_pipeline` CONSTRUCT clustering change** (woman → PSU) belongs to the DHS branch, not to this record;
nothing under `research/records/2026-11-25-equation-suite/` implements it and it is not changed here. Flagged
for the Lead / DHS owner.

## 6. eq04 `q` shadowing — what changed and why the new range is the correct one (QA demand 3)

The loop `for q, adm_q in quotas.items(): ... gq = adm_q[q >= 0.8].mean() - adm_q[q <= 0.2].mean()` reused the
name `q` for the quota-share float (0.4 / 0.5 / 0.6). `q >= 0.8` then evaluated a **scalar** boolean, so
`adm_q[False]` selected an empty slice and both means were `np.nan`: all three quota_share gaps (and their
CIs) were NaN, and `min()` over the multiverse estimates collapsed to the non-NaN subset, making the recorded
range [0.5472, 0.7614] look clean. Renaming the loop variable to `qs` lets the real gaps through:

- quota_share 0.4 → **+0.2593** [0.2424, 0.2771]: too few reserved seats to offset the score bar;
- quota_share 0.5 → **+0.0906** [0.0733, 0.1063]: identical to the default `quota` spec (same construction);
- quota_share 0.6 → **−0.0912** [−0.1097, −0.0779]: a 60% reserve is large enough to tip the top–bottom gap
  negative.

The new range **[−0.0912, 0.7614]** is correct because it contains all five declared specs, and the sign of
the quota gap genuinely depends on the quota share (`spec_robust: False`). The multiverse range cannot include
a NaN; the old range silently excluded three of the five specs. The decision rule still fails: it uses the
default `quota` spec (0.5 share), gap **+0.0906**, which does not flip.

## 7. What still fails (preserved, not massaged)

- S4 pre-declared FAIL (quota gap +0.0906 not negative).
- S6 ad-hoc FAIL (network marginal effect smaller than no-network).
- S10 FAIL: `ban_raises_gini_in_all_specs=False` (ΔGini negative in all 9 specs) and the dropped pre-registered
  S3 single-world Tobit rule fails on the aligned scale.
- Smoke pass disagrees with full pass for eq08 (`clean_lambda_near_truth=False` in smoke, `True` in full):
  both statuses are recorded in `run_all.json`; the full run is the reported one.
- `run_all.py` now exits **1** on this suite. That is the honest verdict, not a broken run: execution failures
  are `[]`.

## 8. Reproduce

```sh
cd research/records/2026-11-25-equation-suite
OMP_NUM_THREADS=1 /Users/treymenefee/neon-boot/venv/bin/python scripts/run_all.py --workers 6   # exit 1
python - <<'PY'
import json, glob
for f in glob.glob("results/*.json"):
    json.loads(open(f).read(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
print("strict JSON OK")
PY
```
