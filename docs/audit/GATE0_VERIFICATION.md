# GATE 0 VERIFICATION — Commander independent sign-off

**Owner:** `atlas-commander` (execution owner). **Status: SIGNED OFF — GATE 0 PASS (2026-11-25T14:40 CST).**
**Date:** 2026-11-25 ~14:33 CST. **Branch:** `research/contest-audit-v2-2026-11-25`.

This is the Commander's *independent* check of Gate 0, as required by the Directive. I did not rely on
audit-runner's comparison outputs for the headline numbers: I re-ran the 540-job myself from a clean
`git archive HEAD` extraction on the host, and I re-invoked the comparator myself on the box artifacts
(over SSH), parsing the results here.

Evidence: **REPRODUCED SIMULATION** (engine/simulation reproduction), not empirical.

---

## 1. Artifacts verified

| artifact | sha256 | size |
|---|---|---|
| pristine engine `engine/eduengine/core.py` @ 1c3417c/7356c97 | `618bd6ddce27691243111bae138a8d7aede6d59d25d2d9faa2caed24bd67fb4f` | 21,825 B |
| pristine `engine/eduengine/modules/tutoring.py` @ 1c3417c/7356c97 | `b2d213b65318fddd0c9555cd25f27714d46609036167079393bcb289c9d64308` | 10,647 B |
| legacy runner `papers/.../code/run_hk_korea_comparative.py` | `dd0b1d8d1a17e4639e45c1ae085d4efe5be613fde509c62f7a8345170786bcec` | 10,468 B |
| supplied bundle reference output | `851bb1dfb6acd67aea6025a11941fa50105a3c41261d566821b730ab3d0fe41b` | 431,901 B |
| **Commander independent host run** | `722c370bfc00a339174bf3135f12389dbc53d87a7f607639814ebf43056eaf54` | 431,902 B |
| audit-runner host run | `de46b91ac9fa28f987760f7daed205e6e9500d071a3527929fab4de6291e185e` | 431,902 B |
| audit-runner box run, 8 workers | `2e1bcb01c790dbc4f8229b605925e3190bd40fce6c2ad8d948472dfc377d217f` | 431,903 B |
| audit-runner box run, 56 workers | `7620a983cd8cebcd6838efc5654d31cf792e198626876142bd884965f67b7b43` | 431,903 B |

`git diff 1c3417c HEAD -- engine/` is empty, so the 7356c97 engine is the directive start engine.
The commit `7356c97` is `1c3417c` + one doc commit (`REVIEW_RESPONSE_2026-11-25.md`).

## 2. Commander independent host reproduction (from clean `git archive HEAD`)

```
rm -rf /tmp/cmd-verify && mkdir -p /tmp/cmd-verify
cd /Users/treymenefee/neon-boot/wt4/auditv2
git archive HEAD engine \
  papers/shadow-education-contest/code/run_hk_korea_comparative.py \
  papers/shadow-education-contest/code/compare_cf4_reference.py \
  papers/shadow-education-contest/code/results/reference | tar -x -C /tmp/cmd-verify
cd /tmp/cmd-verify
PYTHONPATH="$PWD/engine" OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /Users/treymenefee/neon-boot/venv/bin/python \
  papers/shadow-education-contest/code/run_hk_korea_comparative.py
```

Result: exit 0, 540/540, wall **100.79 s** (user 9 m 9.7 s), 8 workers. Output preserved as
`results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json`.

Comparison against the committed reference (re-run myself with `compare_cf4_reference.py`, full per-field
report preserved as `results/audit/commander/compare_commander_vs_reference.json`):

| comparison | differs / compared | max abs | max rel |
|---|---|---|---|
| seed-level numeric values | **6 / 9,180** (rows 130/311/379: `q5_q1_spend_ratio`, `k12_spend_by_q[0]`) | `3.553e-15` | `2.094e-16` |
| summary numeric values | **4 / 846** (`KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio` mean/sd/ci95_lo/ci95_hi) | `4.441e-16` | `2.486e-16` |
| stored 2-d.p. `total_spend_index` | 0 differ (all equal) | — | — |
| other stored numbers | only `metadata.elapsed_seconds` | — | — |

→ **11 stored numbers differ out of 10,026 numeric values compared**, all of them `elapsed_seconds` or last-bit
floating-point rounding (≤4.5e-16 relative in summary, ≤3.6e-15 absolute in seed rows). Verdict:
REPRODUCED SIMULATION — identical up to floating-point rounding; no substantive discrepancy.

**Cross-lane check:** the Commander run and audit-runner's host run differ in **exactly one stored field**
(`metadata.elapsed_seconds`: 100.79 vs 118.36); all other 10,025 numeric values are identical. Whole-file hashes
differ because each run embeds its own wall time — Gate 0 must be judged on the value diff, not whole-file hashes.

## 3. Box environment-independence re-run — independently re-verified

Box: `autodl-container-wjb02xe512-3c3a2b3b`, 80 vCPU Xeon Gold 6248, 251 GiB RAM, overlay 27 G free,
`/root/miniconda3/bin/python` 3.10.8, **numpy 1.24.1**, scipy 1.13.1 (host: py 3.10.2, **numpy 2.2.6**, scipy 1.15.3).
So the box differs in Python patch level, NumPy major.minor, BLAS, CPU architecture, core count — a genuine
environment-independence test.

Deployment was read-only from a committed SHA into `/root/work/gate0`; the box run wrote only inside that dir.
I independently re-invoked `compare_cf4_reference.py` **on the box** for the three comparisons and parsed the JSON
here:

| comparison | seed exact / compared | seed max abs | seed max rel | summary exact / compared | summary max abs | summary max rel | spend indices |
|---|---|---|---|---|---|---|---|
| **box 8w vs bundle reference** | 9,164 / 9,180 (16 differ) | `7.105e-15` | `3.961e-16` | 831 / 846 (15 differ) | `1.776e-15` | `4.971e-16` | all 2-d.p. equal |
| **box 56w vs bundle reference** | 9,164 / 9,180 (16 differ) | `7.105e-15` | `3.961e-16` | 831 / 846 (15 differ) | `1.776e-15` | `4.971e-16` | all 2-d.p. equal |
| **box 56w vs box 8w** | **9,180 / 9,180 exactly equal** | `0.0` | `0.0` | **846 / 846 exactly equal** | `0.0` | — | all equal |

Box-vs-reference differing rows (each 2 fields, always `q5_q1_spend_ratio` and `k12_spend_by_q[0]`):
`(118, HK, CF2a, 28)`, `(130, HK, CF2b, 10)`, `(282, KR, Baseline, 12)`, `(319, KR, CF1a, 19)`,
`(365, KR, CF2a, 5)`, `(367, KR, CF2a, 7)`, `(379, KR, CF2a, 19)`, `(463, KR, CF3b, 13)`.

**Conclusions.**
1. **Environment independence:** an independent machine/OS/Python/NumPy/BLAS reproduces the reference to ≤`7.1e-15`
   absolute (`≤5.0e-16` relative); **every reported 2-d.p. figure is identical**, and the CF4 arm verdicts
   (`win_win_both_jurisdictions`: only CF1b True) are identical. The residual is last-bit libm/BLAS rounding, not a
   model discrepancy.
2. **Worker-count invariance:** 56 workers vs 8 workers on the box produce **bit-identical** outputs (all 9,180 seed
   values and all 846 summary values exactly equal). Parallel execution does not perturb results.
3. The 56-worker box run used a transparent runner variant: `results/audit/box56w_runner_variant.diff` is a
   **one-line diff** (`workers = min(os.cpu_count() or 2, 8)` → `workers = 56`) and nothing else; the algorithmic
   code path is unchanged. This is acceptable for the environment/worker test and is recorded, not hidden.

## 4. Artifact registry verification (independent)

`docs/audit/ARTIFACT_REGISTRY.csv` has **87 rows** (≥40 required) with evidence taxonomies:
REPRODUCED SIMULATION 50, AUTHOR-REPORTED 27, UNRESOLVED 7, VERIFIED EMPIRICAL 3.

I re-hashed every row that exists in the frozen `7356c97` snapshot or the working tree myself:

* **71 / 87 rows verified exactly** (sha256 and byte count) against the frozen snapshot — including all engine,
  runner, result, manuscript and GPU-script artifacts in the audit branch.
* **1 row is self-referential churn:** `docs/audit/system_box.txt` was registered at 9,065 B then extended to
  9,468 B later in Gate 0; the registry entry is stale for that manifest only (benign, but should be re-hashed
  before final packaging).
* **15 rows are Gate-0 outputs produced after the snapshot** (host/box run JSONs, comparison/per-field diff files,
  manifests) — they are absent from `7356c97` by construction and are committed separately by audit-runner.
* The archive-branch bundle contents are inventoried separately in `docs/audit/ARCHIVE_BRANCH_INVENTORY.csv`
  (1,123 entries) with sha256; I did **not** independently re-derive those 1,123 hashes — flagged as an
  audit-runner-verified (not Commander-verified) claim.
* 3 "VERIFIED EMPIRICAL" rows are environment manifests and the archive inventory — that label is correct for
  captured environment facts, but it must **not** be read as empirical research evidence anywhere.

## 5. Discrepancy audit and caveats (preserved, not explained away)

* The supplied bundle reference **records no Python/NumPy versions** (`metadata` has only repo/branch/base_commit/
  counts/elapsed/history_api), so "bit-identical to the reference" cannot mean byte-identical; it means value-identical
  to the last bit. That is what we observe (≤4.5e-16 relative), on two independent environments and two worker counts.
* The 420-run generation (`verified_results_2026_11_25.json`, Paper B tables) remains **AUTHOR-REPORTED** and is
  **not reproducible** against the committed engine (its runner targets an older `Engine(cfg, modules=…)` API).
  Gate 0 does not and cannot validate it.
* The CF4 inconvenient result is **reproduced, not repaired**: only CF1b (cap −50 %) is Win-Win in both
  jurisdictions; CF4a fails HK equity (48.64 % vs 46.36 % baseline); CF4b fails spend (HK 90.88, KR 88.04 ≥ 80).
  This stays reported in every downstream document.
* Box 8w/56w outputs have a different file size (431,903 B) from the reference (431,901 B) because the box runner
  variant writes its metadata/wall time; value comparison is the meaningful test.

## 6. Gate 0 verdict

**Commander verdict: GATE 0 PASS (pending sign-off on audit-runner's `GATE0_REPORT.md`).**
Environment manifests exist for host and box; the artifact registry covers 87 artifacts with real hashes (71/87
independently re-hashed by me, 1 stale self-referential row, 15 post-snapshot Gate-0 outputs, archive inventory
separately recorded); the legacy 540-run reproduction is value-identical to the committed reference on the host
(6/9,180 seed values at ≤3.6e-15, 4/846 summary values at ≤4.5e-16, all 2-d.p. figures identical); the box
environment-independence re-run reproduces it at ≤7.1e-15 with all reported figures identical; 56-vs-8-worker
outputs are bit-identical. **Gate 0 does not validate any research claim; it validates that the Gate-0 baseline
code and artifact are reproducible.**

**Conditions carried forward:** (i) re-hash `system_box.txt` in the registry before final packaging; (ii) archive
inventory hashes are audit-runner-verified, not Commander-verified; (iii) the 420 generation stays AUTHOR-REPORTED.

*Formal sign-off line to be completed when `docs/audit/GATE0_REPORT.md` is delivered: the report's verdict, hashes
and mismatch table must match §2–§3 above; any divergence is to be recorded here before Gate 0 is declared closed.*

---

## 7. Sign-off on `docs/audit/GATE0_REPORT.md` (accepted as the Gate-0 record)

**Sign-off: GATE 0 PASS.** `docs/audit/GATE0_REPORT.md` (audit-runner, commit `9536870`) is accepted as the
Gate-0 record; it is **not** overwritten by this file. I independently reproduced its three headline claims:

| claim in GATE0_REPORT | Commander independent check | match |
|---|---|---|
| host repro output is textually identical to the committed 540 JSON `c1fa0926…` **except** `metadata.elapsed_seconds` (178.65 → 118.36) | re-flattened both JSONs: exactly **1** differing stored field (`metadata.elapsed_seconds`); 9,180 seed + 846 summary numerics identical | ✅ |
| host vs supplied reference: 9,174/9,180 seed + 842/846 summary exact; max abs `3.553e-15` / `4.441e-16`; max rel `2.094e-16` / `2.486e-16` | my own clean-`git archive HEAD` run + my own comparator invocation: same counts, same maxima, same 3 changed rows (130/311/379) | ✅ |
| box (NumPy 1.24.1) vs reference: 9,164/9,180 + 831/846 exact; max abs `7.105e-15`; max rel `4.971e-16`; 0 diffs at 2 d.p. | my own comparator invocation **on the box** over SSH: same counts/maxima; all 18×2 `total_spend_index` values identical; CF4 verdict identical | ✅ |
| box 56-worker vs box 8-worker: all 9,180 + 846 numerics bit-identical | same, re-invoked by me: 9,180/9,180 and 846/846 exactly equal, max abs 0.0 | ✅ |
| artifact registry 87 rows with real sha256 | **after the `25fd953` correction** I re-derived **87/87 rows from immutable snapshot blobs myself** (15 archive rows at `46950ab` with the `research/atlas-all-work-2026-11-25/` prefix stripped, 72 rows at `9536870`/`7356c97`/`1c3417c`) → **0 mismatches**. Phase-B files (`rng.py`, `contest_math.py`) are correctly absent from the Gate-0 registry. | ✅ |

**(a) The one-field difference.** audit-runner's host reproduction of the 540-run job is *bit-identical* to the
committed 540-run JSON apart from `metadata.elapsed_seconds`; against the author-supplied reference it differs by
last-bit floating-point rounding only (6/9,180 seed values ≤3.553e-15; 4/846 summary values ≤4.441e-16). The
`elapsed_seconds` field is machine wall time and is excluded from every "identical" claim. Whole-file sha256s of
reproduction outputs therefore differ run-to-run by design; Gate 0 is judged on value diffs.

**(b) Box NumPy caveat (recorded; remediation decided).** The box runs NumPy **1.24.1** (py 3.10.8) while
`engine/requirements.txt` declares `numpy>=1.26` (`research/requirements.txt`: `numpy>=1.26,<3`; host: 2.2.6).
The box re-run is therefore an **independent-environment stress test, not a certified in-range environment** — and
it still reproduces every reported figure. Decision (Lead directive, recorded): create `/root/work/venv-declared` on
the box (python3 -m venv) with the declared stack (`engine/requirements.txt` + `pytest pandas pyarrow psutil`),
record its `pip freeze` in `docs/audit/system_box_venv.txt`, and use it for **all future box CPU work** (Gate 2/3
calibration). Status at sign-off: venv created (`/root/work/venv-declared`, py 3.10.8), declared-stack install
running detached (`nice -n 10`, log `/root/work/venv-declared/install.log`); it does not block Gate 1.

**(c) What remains AUTHOR-REPORTED / UNRESOLVED (carried verbatim into Gate 1+).**
* **420-run generation** (`verified_results_2026_11_25.json`; Paper B docx tables: HK elite Q5 30.0 %, KR 24.6 %) —
  **AUTHOR-REPORTED**, not reproducible: no 420-era runner/engine generation exists in the tree. The Paper B tables
  must not be presented as Gate-0-reproduced.
* **Paper A Exp 1/3/4/5 simulations and the identifiability result** — **UNRESOLVED** (runners and raw outputs absent;
  `code/MISSING_ARTIFACTS.md` confirmed still accurate).
* **GPU (RTX 3080 Ti) outputs** — **UNRESOLVED**: nothing supplied, nothing run; the review-confirmed estimator
  defects (unused `theta[:,5]`, panel `X=[1,x]` drops controls/FE) stand. Torch/cu118 now installs on the box but
  GPU work remains parked for wave 2.
* **All Gate-0 reproduction claims are SIMULATION evidence** (REPRODUCED SIMULATION), never empirical.

**Conditions carried into final packaging:** (i) `GATE0_REPORT.md` is the immutable Gate-0 record — do not
overwrite; (ii) registry rows are frozen from commit snapshots, never from the live worktree (the `25fd953`
correction fixes the one row that violated this); (iii) the full 1,123-entry archive-branch inventory hashes are
audit-runner-verified (MANIFEST 13/13 OK), not independently re-derived by the Commander (the 15 registry-covered
archive rows *are* Commander-verified); (iv) 420-run/Paper A/GPU statuses above stay AUTHOR-REPORTED / UNRESOLVED.

**GATE 0 CLOSED (PASS, WITHIN TOLERANCE).**
