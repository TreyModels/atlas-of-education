# Reproduction — HK/Korea 18-arm contest-gate run and CF4a/CF4b evaluation

**SIMULATION.** All numbers in this file come from a stochastic simulation of `eduengine`
(18 policy arms × 30 matched seeds, 540 runs) on 2026-11-25. They are not empirical estimates of
Hong Kong / South Korean tutoring markets and must not be cited as such.

**Date:** 2026-11-25 14:00 CST · **Branch:** `research/shadow-education-contest-2026-11-25` ·
**Base commit:** `8685417` · **Worker:** `hk-contest`

## 1. What was received and what was verified

Two code bundles were supplied by the operator:

| bundle | sha256 | contents |
|---|---|---|
| `hk_korea_exact_bundle.zip` | `e9cc02c2da17906c7bdc706285b723cb1e2058dd803312cb08a41197c425be4e` | `engine/eduengine/core.py`, `engine/eduengine/modules/tutoring.py`, `run_hk_korea_comparative.py`, `contest_gate.patch` |
| `hk_korea_contest_code_bundle.zip` | `da5cd1ee4ae6d00598bf02543545491c60ee1ffc120f98eaae3acce01c74e47f` | the same four files **plus** the reference output `hk_korea_comparative_with_cf4.json` (431,901 bytes) |

Both zips were superseded later the same day by the canonical all-in-one bundle
`/tmp/ALL_ATLAS_WORK_2026_11_25.zip` (sha256
`f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74`; archived on branch
`research/atlas-all-work-2026-11-25`). Its copies of the four code files and the reference JSON are
**byte-identical** to the ones verified below (`core.py` `618bd6dd…`, `tutoring.py` `b2d213b6…`,
`run_hk_korea_comparative.py` `dd0b1d8d…`, `contest_gate.patch` `35b1480a…`, reference JSON `851bb1df…`);
it additionally provided the Paper A draft docx (`39092abb…`) and three GPU scripts, deposited elsewhere in
this directory. The verification below was done against the earlier two zips before the all-in-one arrived
and re-checked against the all-in-one.

Both zips were extracted fresh to `/tmp/hk_verify/` and `/tmp/hk_ref/`. Every worktree file was then
compared byte-for-byte against its bundle counterpart:

| file | sha256 (bundle = worktree) |
|---|---|
| `engine/eduengine/core.py` | `618bd6ddce27691243111bae138a8d7aede6d59d25d2d9faa2caed24bd67fb4f` |
| `engine/eduengine/modules/tutoring.py` | `b2d213b65318fddd0c9555cd25f27714d46609036167079393bcb289c9d64308` |
| `code/run_hk_korea_comparative.py` | `dd0b1d8d1a17e4639e45c1ae085d4efe5be613fde509c62f7a8345170786bcec` |
| `code/contest_gate.patch` | `35b1480a9a2c006d3747a7d1b34f89e78e98f1aa1851c6cbe0a2a6fec1c71f9f` |

All four matched exactly (`diff` empty, sha256 equal). The patch was also checked against the
working tree:

- `git diff -- engine/eduengine/core.py engine/eduengine/modules/tutoring.py` is **byte-identical**
  to `code/contest_gate.patch`;
- `git apply --check -R code/contest_gate.patch` succeeds → the worktree engine files are exactly
  `HEAD` + patch.

Finally the provenance chain was closed against the runner's stated base commit `68da16e`
(`research/binding-gate-2026-11-25`):

- `HEAD:engine/eduengine/core.py` and `HEAD:.../tutoring.py` are byte-identical to
  `68da16e:engine/eduengine/core.py` and `68da16e:.../tutoring.py`;
- applying `contest_gate.patch` to those `68da16e` files reproduces the bundle engine files exactly.

So the engine code that produced the reference output and the engine code in this worktree are the same
code (`68da16e` + `contest_gate.patch`). The reference output, the patch and the runner are verified
artifacts; nothing was edited or reconstructed.

## 2. Invocation and environment

The supplied runner sets `ENGINE_DIR = os.path.join(ROOT, "engine")` where `ROOT` is the script's own
directory, so it points at `papers/shadow-education-contest/code/engine`, which does not exist (the
engine lives at the repository root, `engine/`). The runner was **not edited**; the correct import path
was supplied with `PYTHONPATH`, as the brief specified:

```
cd /Users/treymenefee/neon-boot/wt3/shadow
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/run_hk_korea_comparative.py
```

The missing `ENGINE_DIR` entry in `sys.path` is harmless; `from eduengine.core import Engine` resolves
through `PYTHONPATH` to `engine/eduengine`.

**Run environment**

| fact | value |
|---|---|
| host | `MacBookAir10,1`, macOS 26.6.2 arm64, 8 logical cores (runner uses `min(cpu_count, 8)` workers) |
| Python | 3.10.2 (`/Users/treymenefee/neon-boot/venv/bin/python`, a symlink to `python3`) |
| NumPy | **2.2.6** (venv) |
| engine requirements floor | `engine/requirements.txt`: `numpy>=1.26`; `research/requirements.txt`: `numpy>=1.26,<3` — 2.2.6 is inside the declared range |

**Bundle/reference environment.** The bundle does not record the environment that produced
`hk_korea_comparative_with_cf4.json`, and the runner's `metadata` block carries no version fields
(only repo/branch/base_commit/counts/elapsed/history_api). The only recoverable environment fact is the
reference run's wall time: **165.47 s** vs **178.65 s** here (540 runs, 8 workers). The reference NumPy
version is therefore **unknown**; it cannot be pinned from the bundle. Despite that, the reproduction
below agrees to the last bit on every reported figure, so the version difference is immaterial for this
result (see §3).

**Run result**

- 540/540 runs completed, `exit code 0`, elapsed **178.65 s**, no worker failures or warnings that
  affect output (`warnings.filterwarnings("ignore")` is set in the supplied runner).
- Output written by the runner to its own script-directory path, `code/hk_korea_comparative_with_cf4.json`
  (as supplied; not edited). The committed copy of this run is
  `code/results/hk_korea_comparative_with_cf4.json` (431,902 bytes, sha256
  `c1fa09264531aa2443b6239cdac70761584a6603fe6f9eb62addecbfd22e2e99`).
- `metadata` in the output: `n_arms=18`, `n_seeds=30`, `total_runs=540`,
  `repo=https://github.com/TreyModels/atlas-of-education.git`,
  `branch=research/binding-gate-2026-11-25`, `base_commit=68da16e`.
  These two provenance strings are **hardcoded in the supplied runner** and were not edited; they
  describe the code lineage (verified in §1), not the checkout branch the run was executed from.

## 3. Comparison with the supplied reference output

Reference: the bundle's `hk_korea_comparative_with_cf4.json`
(sha256 `851bb1dfb6acd67aea6025a11941fa50105a3c41261d566821b730ab3d0fe41b`, 431,901 bytes), committed
for audit as `code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`.
Comparison tool: `code/compare_cf4_reference.py` (committed; re-runnable).

**Metadata.** All fields equal except `elapsed_seconds` (165.47 → 178.65). No other metadata field
differs.

**Seed-level rows (`seeds`, 540 rows, same order and keys).** 9,180 numeric values compared:
**9,174 exactly equal, 6 differ** (3 rows × 2 values). Max absolute difference `3.553e-15`, max relative
difference `2.094e-16` (one floating-point ulp):

| row | jurisdiction | arm | seed | differing fields | abs diff |
|---|---|---|---|---|---|
| 130 | HK | CF2b | 10 | `q5_q1_spend_ratio`, `k12_spend_by_q[0]` | 3.55e-15, 6.9e-18 |
| 311 | KR | CF1a | 11 | `q5_q1_spend_ratio`, `k12_spend_by_q[0]` | 3.55e-15, 3.5e-18 |
| 379 | KR | CF2a | 19 | `q5_q1_spend_ratio`, `k12_spend_by_q[0]` | 3.55e-15, 6.9e-18 |

Rows are aligned one-for-one (no row-key mismatches, no extra/missing keys).

**Summary block (calibration and counterfactual fields).** 846 numeric values compared:
**842 exactly equal, 4 differ** (the four `delta_vs_baseline.q5_q1_spend_ratio` statistics for
`KR.CF2a`: mean, sd, ci95_lo, ci95_hi). Max absolute difference `4.441e-16`, max relative difference
`2.486e-16`. Every `total_spend_index` value (2 d.p.) is identical, every non-numeric field is
identical, and the two files differ textually in exactly 11 stored numbers: `elapsed_seconds` plus the
6 seed-level and 4 summary last-bit values above.

**Verdict.** The reproduced run is **numerically identical to the supplied reference up to last-bit
floating-point rounding** (≤ 4.5e-16 in the summary, ≤ 3.6e-15 in the seed rows), with no difference in
any reported (2 d.p.) figure. It is *not* a byte-identical file only because `elapsed_seconds` records
our wall time and a handful of unrounded ratios differ in the final ulp. There is no substantive
discrepancy to report.

## 4. CF4a / CF4b evaluation

**Criterion (as specified in `NEXT_EXPERIMENTS.md` Exp 7):** *Win-Win* = total K-12 spend index **< 80**
(baseline = 100) **and** the elite-track Q5 admission share **below** the same jurisdiction's Baseline —
and both conditions must hold in **both Hong Kong and Korea**.

Baselines (simulated run; 30 matched seeds): HK elite Q5 share **46.36 %**, KR **36.12 %**; spend index
100.00 by construction. "Elite Q5 share" is the simulated share of elite-track admissions drawn from the
top wealth quintile; it is a model statistic, not an empirical admission statistic.

### Hong Kong

| arm | spend index | Δ spend (pts) | elite Q5 share | Δ vs baseline (pp) | spend < 80 | elite < baseline | Win-Win |
|---|---|---|---|---|---|---|---|
| Baseline | 100.00 | 0.00 | 46.36 % | 0.00 | no | no | no |
| CF1a (+50 % tax) | 107.42 | +7.42 | 52.43 % | +6.07 | no | no | no |
| CF1b (cap −50 %) | 67.39 | −32.61 | 41.96 % | −4.40 | **yes** | **yes** | **PASS** |
| CF2a (S=0.28) | 110.29 | +10.29 | 42.91 % | −3.45 | no | yes | no |
| CF2b (S=0.50) | 149.30 | +49.30 | 33.62 % | −12.74 | no | yes | no |
| CF3a (ΔV −30 %) | 76.98 | −23.02 | 51.03 % | +4.67 | yes | no | no |
| CF3b (ΔV −50 %) | 59.11 | −40.89 | 59.02 % | +12.66 | yes | no | no |
| **CF4a** (ΔV −50 % + cap −50 %) | **43.78** | −56.22 | **48.64 %** | **+2.28** | yes | **no** | **FAIL** |
| **CF4b** (ΔV −50 % + seats S=0.50) | **90.88** | −9.12 | **35.98 %** | −10.38 | **no** | yes | **FAIL** |

### South Korea

| arm | spend index | Δ spend (pts) | elite Q5 share | Δ vs baseline (pp) | spend < 80 | elite < baseline | Win-Win |
|---|---|---|---|---|---|---|---|
| Baseline | 100.00 | 0.00 | 36.12 % | 0.00 | no | no | no |
| CF1a (+50 % tax) | 106.46 | +6.46 | 41.75 % | +5.63 | no | no | no |
| CF1b (cap −50 %) | 76.42 | −23.58 | 26.39 % | −9.73 | **yes** | **yes** | **PASS** |
| CF2a (S₁₂=0.16) | 107.17 | +7.17 | 31.08 % | −5.04 | no | yes | no |
| CF2b (S₁₂=0.40) | 128.00 | +28.00 | 22.01 % | −14.11 | no | yes | no |
| CF3a (ΔV −30 %) | 76.63 | −23.37 | 41.96 % | +5.84 | yes | no | no |
| CF3b (ΔV −50 %) | 57.36 | −42.64 | 47.66 % | +11.54 | yes | no | no |
| **CF4a** (ΔV −50 % + cap −50 %) | **46.50** | −53.50 | **34.10 %** | −2.02 | yes | yes | **PASS** |
| **CF4b** (ΔV −50 % + seats S₁₂=0.40) | **88.04** | −11.96 | **26.51 %** | −9.62 | **no** | yes | **FAIL** |

### Arm-level verdict (both jurisdictions required)

| arm | HK | KR | **Win-Win in BOTH** |
|---|---|---|---|
| CF4a (ΔV −50 % + cap −50 %) | FAIL — elite Q5 share 48.64 % vs 46.36 % baseline (+2.28 pp) | PASS — 46.50 spend, 34.10 % elite (−2.02 pp) | **NO** |
| CF4b (ΔV −50 % + seats) | FAIL — spend 90.88 ≥ 80 (elite share does fall, −10.38 pp) | FAIL — spend 88.04 ≥ 80 (elite share does fall, −9.62 pp) | **NO** |
| CF1b (cap −50 %, single lever) | PASS — 67.39 spend, 41.96 % elite (−4.40 pp) | PASS — 76.42 spend, 26.39 % elite (−9.73 pp) | **YES (only arm)** |

The pre-stated falsifier in `NEXT_EXPERIMENTS.md` was: *"CF4a/CF4b land in the Win-Win Zone … in both
jurisdictions."* **That falsifier is not met by this run.** Neither composite arm clears the criterion in
both jurisdictions: CF4a fails in Hong Kong on elite capture, and CF4b fails in both on spend. The only
arm that meets the criterion is the single effort-cap arm CF1b.

### Single-lever comparison

`CF4a` = `CF3b` (wage compression ΔV −50 %) + `CF1b` (effort cap −50 %); `CF4b` = `CF3b` + `CF2b`
(large seat expansion).

| jurisdiction | combo | spend index | elite Q5 % | combo vs its levers |
|---|---|---|---|---|
| HK | **CF4a** | 43.78 | 48.64 % (FAIL elite) | CF3b 59.11 / 59.02 % (fail); CF1b 67.39 / 41.96 % (pass). Adding ΔV −50 % to the cap cuts spend (67.39 → 43.78) but **raises** HK elite Q5 share from 41.96 % to 48.64 %, undoing the cap's equity gain on this metric. |
| KR | **CF4a** | 46.50 | 34.10 % (PASS) | CF3b 57.36 / 47.66 % (fail); CF1b 76.42 / 26.39 % (pass). Combo passes both criteria here. |
| HK | **CF4b** | 90.88 | 35.98 % (FAIL spend) | CF3b 59.11 / 59.02 % (fail); CF2b 149.30 / 33.62 % (fail). Combo lowers spend and elite capture vs CF2b but spend stays ≥ 80. |
| KR | **CF4b** | 88.04 | 26.51 % (FAIL spend) | CF3b 57.36 / 47.66 % (fail); CF2b 128.00 / 22.01 % (fail). Same pattern; spend stays ≥ 80. |

Reading (SIMULATION, descriptive only): every ΔV-compression arm (CF3a, CF3b, and both CF4 combos) lowers
total spend but **raises** the elite Q5 share relative to baseline in both jurisdictions — the opposite
of what the "wage compression reaches the Win-Win Zone" reading in the Paper B draft predicts for the
elite-capture leg. The effort cap alone (CF1b) is the only arm that satisfies both stated conditions in
both jurisdictions. The mechanism behind the sign of the ΔV→elite-share effect is not diagnosed here and
needs a dedicated decomposition before any interpretation is offered.

## 5. Caveats

- **Simulation only.** These are 30 matched stochastic seeds of a structural model with a Tullock /
  Plackett-Luce contest gate; seed-to-seed uncertainty is reported in the JSON
  (`ci95_lo`/`ci95_hi` per summary statistic) and no causal or empirical claim is made.
- The runner's `N=300`, `T=46`, `measure_from=18`, 18-arm design is **not** the design described in the
  Paper B draft (author-reported 14 arms, 420 runs, `N=400`, `T=70`). The draft's calibration and
  counterfactual table is therefore *not* reproduced by this run; the run was checked against the
  supplied 18-arm reference output, not against the paper's table.
- The Q5 elite-share statistic is the simulated share of elite-track admissions from the top wealth
  quintile, not an empirical HKDSE/CSAT admission statistic.
- The `base_commit`/`branch` strings inside the output JSON are hardcoded in the supplied runner and
  describe the patch's code lineage (`68da16e` + patch, verified in §1), not the checkout branch used
  for the run.
- Reference environment (Python/NumPy) is unrecorded in the bundle; see §2.

## 6. Reproduce / re-audit

```
cd /Users/treymenefee/neon-boot/wt3/shadow
# 1. run — the supplied runner writes code/hk_korea_comparative_with_cf4.json
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/run_hk_korea_comparative.py
# 2. compare to the committed bundle reference; the committed copy of our run is under results/
/Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/compare_cf4_reference.py \
    papers/shadow-education-contest/code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json \
    papers/shadow-education-contest/code/results/hk_korea_comparative_with_cf4.json
```

## 7. Files added/changed by this deposit

| file | sha256 | note |
|---|---|---|
| `engine/eduengine/core.py` | `618bd6dd…fb4f` | exact bundle file (contest gate + elite premium), applied |
| `engine/eduengine/modules/tutoring.py` | `b2d213b6…4308` | exact bundle file (contest tutoring), applied |
| `code/contest_gate.patch` | `35b1480a…1f9f` | exact bundle patch; equals `git diff` of the two engine files |
| `code/run_hk_korea_comparative.py` | `dd0b1d8d…bcec` | tested bundle runner (replaces the earlier incompatible `da07107c…`) |
| `code/results/hk_korea_comparative_with_cf4.json` | `c1fa0926…2e99` | this run (540/540), 431,902 bytes |
| `code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json` | `851bb1df…e41b` | supplied reference output, unmodified, for audit |
| `code/compare_cf4_reference.py` | — | comparison + CF4 evaluation tool |
| `code/REPRODUCTION_CF4_2026-11-25.md` | — | this file |

Also integrated from the canonical all-in-one bundle (not part of the reproduction):

| file/dir | sha256 | note |
|---|---|---|
| `paper_a_general_mechanism/When_Fee_Abolition_Meets_Rationed_Gates_APA.docx` | `39092abb…0c91` | Paper A draft manuscript, deposited as received; its simulations not run here |
| `code/rtx3080ti_gpu_scripts/` (3 files) | `b74cd583…`, `0709032c…`, `3bbbc19a…` | GPU job scripts from the bundle; not run on this branch |

Additive change only; no force-push, no `main`. The canonical all-in-one bundle is
`/tmp/ALL_ATLAS_WORK_2026_11_25.zip`, sha256
`f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74`; its code/reference files were verified
byte-identical to the ones this reproduction used.
