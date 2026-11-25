# GATE 0 REPORT — environment, artifact inventory, legacy 540-run reproduction

**Programme:** Atlas contest audit v2 · **Gate:** G0 · **Lane owner:** `audit-runner`
**Date:** 2026-11-25 (CST) · **Audit branch:** `research/contest-audit-v2-2026-11-25` @ `7356c97`
**Pristine repro tree:** `/Users/treymenefee/neon-boot/wt4/repro` — `research/gate0-repro-2026-11-25` @
`1c3417c4a2a17f47f31388e0686396a1a3877757` (never edited; only the runner's own throwaway output was written there)
**Status:** COMPLETE — all five Gate-0 acceptance items delivered. **Verdict: WITHIN TOLERANCE**
(host reproduction is bit-identical to the committed 540-run output apart from `elapsed_seconds`; cross-environment
and reference differences are last-bit floating-point only; **zero** differences at any reported precision).

---

## 0. What Gate 0 establishes — one paragraph

The legacy 18-arm × 30-seed (540-run) HK/Korea contest-gate job reproduces **deterministically from the exact
committed code** on two independent machines: the host (macOS arm64 / 8-core Apple M1 / Python 3.10.2 / NumPy
**2.2.6**) and the AutoDL box (Linux x86_64 / Xeon Gold 6248 host; **10-CPU cgroup quota**, not the 80 CPUs that `nproc` reports — see §4 correction / Python 3.10.8 / NumPy **1.24.1**). The host
output is textually identical to the committed 540-run JSON `c1fa0926…` except its wall-clock field, and matches
the author-supplied reference output to **≤ 3.6e-15** absolute (host) / **≤ 7.1e-15** absolute (box) — last-bit
float noise from different libm/BLAS builds. Every reported (2 d.p.) figure — all `total_spend_index` values and
every summary statistic — is identical in all comparisons. The reproduction is **SIMULATION** evidence only; the
420-run generation used by the Paper B manuscript tables is **not** reproduced (no runnable 420-era runner exists
in the tree) and remains AUTHOR-REPORTED.

---

## 1. Environment manifests (deliverables 1)

| manifest | path | contents |
|---|---|---|
| host | [`docs/audit/system_host.txt`](system_host.txt) | `uname -a`, `sw_vers`, `hw.ncpu`=8 / `hw.memsize`=8,589,934,592 B, Python 3.10.2 (`/Users/treymenefee/neon-boot/venv/bin/python`), NumPy 2.2.6 / SciPy 1.15.3, full `pip freeze`, git HEADs of both worktrees (`repro` 1c3417c, `auditv2` 7356c97) |
| box | [`docs/audit/system_box.txt`](system_box.txt) | `nproc`=80, `free -g` (251 GiB, 213 GiB available at capture), `nvidia-smi` (RTX 3080 Ti 12 GB, 1 MiB used, 0 % util), `df -h` (overlay 30 G, 27 G free), Ubuntu 22.04, `/root/miniconda3/bin/python` 3.10.8, NumPy 1.24.1 / SciPy 1.13.1, full `pip freeze`, live load + in-flight torch install. **NOTE (post-capture): `nproc`/`lscpu` report the 80-CPU host; the container cgroup quota is 10 CPUs (`cpu.max = 1000000 100000`) — see §4 correction.** |

Host: `MacBookAir10,1`, macOS 26.6.2 arm64, 8 logical cores, 8 GiB RAM. Box: `autodl-container-wjb02xe512-3c3a2b3b`,
`root@connect.nmb2.seetacloud.com:36934`, **10-CPU cgroup quota** (host reports 80 CPUs), 251 GiB RAM, RTX 3080 Ti. Captured 2026-11-25T06:23Z.
Bare `python3` is **not** on the non-interactive ssh PATH; the absolute `/root/miniconda3/bin/python` was used
throughout, as the brief required.

**Declared dependency floor vs box reality (recorded, not fixed):** `engine/requirements.txt` declares
`numpy>=1.26` (and `research/requirements.txt` `numpy>=1.26,<3`). The box interpreter ships **NumPy 1.24.1**, i.e.
below the declared floor. The box run is therefore an *independent-environment stress test*, not a certified
in-range environment; it is recorded as such. No second Python was installed on the box (the torch 2.7.1+cu118 pip
install, pid 2515, was still downloading and was deliberately left untouched).

---

## 2. Code identity verified before running (no edits to the pristine tree)

Verified on host **and** again on the box after deploy (all three must equal the committed reproduction record):

| file | sha256 |
|---|---|
| `engine/eduengine/core.py` (contest-gate patched) | `618bd6ddce27691243111bae138a8d7aede6d59d25d2d9faa2caed24bd67fb4f` |
| `engine/eduengine/modules/tutoring.py` (contest tutoring) | `b2d213b65318fddd0c9555cd25f27714d46609036167079393bcb289c9d64308` |
| `papers/shadow-education-contest/code/run_hk_korea_comparative.py` | `dd0b1d8d1a17e4639e45c1ae085d4efe5be613fde509c62f7a8345170786bcec` |

The runner was **not** edited and `N_SEEDS = 30` was not changed for either reproduction run. Its
`ENGINE_DIR = <script dir>/engine` is a non-existent path, so the engine is supplied via `PYTHONPATH="$PWD/engine"`
(both documented in `code/RUNNER_STATUS.md` and `code/REPRODUCTION_CF4_2026-11-25.md`). The runner writes its output
to its **own script directory** (`code/hk_korea_comparative_with_cf4.json`), not to `code/results/`; the committed
copy lives at `code/results/hk_korea_comparative_with_cf4.json`.

---

## 3. Host reproduction (deliverable 3) — 540/540, exit 0, 119 s

**Exact command** (run from the pristine tree; `OPENBLAS/MKL/OMP=1` as briefed):

```
cd /Users/treymenefee/neon-boot/wt4/repro
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
  /Users/treymenefee/neon-boot/venv/bin/python \
  papers/shadow-education-contest/code/run_hk_korea_comparative.py
```

| field | value |
|---|---|
| workers | 8 (`min(os.cpu_count() or 2, 8)`) |
| completed | **540/540** (18 arms × 30 matched seeds), `exit 0` |
| wall time | **119 s** (runner-reported 118.36 s; start_epoch 1795587795 → end 1795587914) |
| output | `papers/shadow-education-contest/code/hk_korea_comparative_with_cf4.json`, 431,902 B, sha256 **`de46b91ac9fa28f987760f7daed205e6e9500d071a3527929fab4de6291e185e`** |
| copy kept | [`results/audit/hk_korea_comparative_with_cf4_repro_mac_2026-11-25.json`](../../results/audit/hk_korea_comparative_with_cf4_repro_mac_2026-11-25.json) + `.sha256` |
| stdout | [`results/audit/run_mac_stdout.log`](../../results/audit/run_mac_stdout.log), meta [`run_mac_meta.txt`](../../results/audit/run_mac_meta.txt) |
| env | macOS 26.6.2 arm64 (M1, 8 cores), Python 3.10.2, NumPy 2.2.6 |

**Cross-lane check (independent of this lane):** the execution owner (`atlas-commander`) independently re-ran the
same 540 jobs from a clean `git archive HEAD` of `7356c97` in a separate directory on the host (8 workers, exit 0,
100.79 s) and preserved the output at
[`results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json`](../../results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json)
(sha256 `722c370b…af54`). Its values differ from this lane's host output in **exactly one stored field —
`metadata.elapsed_seconds` (100.79 vs 118.36)**; all 10,025 other numeric values are identical. Gate 0 is therefore
judged on value diffs, not whole-file hashes (each JSON embeds its own wall time).

**Comparison A — host re-run vs the committed 540-run output** (`code/results/hk_korea_comparative_with_cf4.json`,
sha256 `c1fa09264531aa2443b6239cdac70761584a6603fe6f9eb62addecbfd22e2e99`): the two files differ textually in
**one stored number only** — `metadata.elapsed_seconds` (178.65 → 118.36). All 9,180 seed-level and 846 summary
numeric values are bit-identical. **This is a bit-identical reproduction modulo wall-clock.**

**Comparison B — host re-run vs author-supplied reference**
(`code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`, sha256 `851bb1df…e41b`; comparator
report [`results/audit/compare_mac_vs_reference.json`](../../results/audit/compare_mac_vs_reference.json)):

```
/Users/treymenefee/neon-boot/venv/bin/python \
  papers/shadow-education-contest/code/compare_cf4_reference.py \
  papers/shadow-education-contest/code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json \
  papers/shadow-education-contest/code/hk_korea_comparative_with_cf4.json
```

| block | values compared | exactly equal | differing | max abs diff | max rel diff |
|---|---|---|---|---|---|
| seed rows (540 rows) | 9,180 | 9,174 | **6** (3 rows × 2 fields) | **3.5527e-15** | **2.0937e-16** |
| summary block | 846 | 842 | **4** (KR.CF2a `delta_vs_baseline.q5_q1_spend_ratio` mean/sd/ci95_lo/ci95_hi) | **4.4409e-16** | **2.4856e-16** |
| **total (incl. 540 seed-id ints)** | **10,566** | **10,556** | **10** | **3.5527e-15** | **2.0937e-16** |

Metadata: every field equal except `elapsed_seconds` (165.47 → 118.36). **Reported figures: 0 differences at
2 d.p.; all 18×2 `total_spend_index` values identical.** Differing seed rows: 130 (HK/CF2b/seed 10), 311
(KR/CF1a/seed 11), 379 (KR/CF2a/seed 19), each in `q5_q1_spend_ratio` and `k12_spend_by_q[0]` — exactly the
last-ulp pattern already recorded in `REPRODUCTION_CF4_2026-11-25.md` §3.

Per-field detail: [`results/audit/per_field_diff_mac_vs_reference.md`](../../results/audit/per_field_diff_mac_vs_reference.md)
and `.csv` (largest: seed `q5_q1_spend_ratio` 3.553e-15).

---

## 4. Box independence re-run (deliverable 4) — 540/540, exit 0, 72 s

**Deployment** (read-only export from the committed pristine SHA; box work done only in the private
`/root/work/gate0` directory; no other lane's box dir touched):

```
cd /Users/treymenefee/neon-boot/wt4/repro
git archive --format=tar.gz -o /tmp/gate0_repro.tar.gz HEAD     # HEAD = 1c3417c, 47,739,781 B
/tmp/box_scp.sh /tmp/gate0_repro.tar.gz /root/work/gate0/
/tmp/box_ssh.sh 'cd /root/work/gate0 && tar -xzf gate0_repro.tar.gz'
```

Engine + runner sha256 re-verified **on the box** after extraction → identical to the three hashes in §2.
Box environment: Python 3.10.8 `/root/miniconda3/bin/python`, NumPy **1.24.1**, **10-CPU cgroup quota**,
`nice -n 10`, `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1`.

**Box CPU correction (issued 2026-11-25 after these runs, Lead-verified).** The box container is a **10-CPU
cgroup**, not 80: `cat /sys/fs/cgroup/cpu.max` = `1000000 100000`. `nproc`/`lscpu` report the 80-CPU *host* and
overstate the allocation. Consequences for the Gate-0 record: (a) the canonical box evidence is the
unmodified-runner **8-worker** run below; (b) the 56-worker variant is a **worker-count invariance check only**
(56 vs 8 workers produced bit-identical numbers) and is **not** a box-capacity result — it oversubscribed the
10-CPU quota; (c) no Gate-0 box run may be interpreted as having used more than **8 concurrent workers**, and any
future box work must respect ≤8 workers across all lanes (≤4 per lane) with `nice -n 10`.

**Run A — unmodified runner (canonical box re-run):**

```
cd /root/work/gate0
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$PWD/engine" \
  nice -n 10 /root/miniconda3/bin/python \
  papers/shadow-education-contest/code/run_hk_korea_comparative.py
```

| field | value |
|---|---|
| workers | 8 — the **unmodified** runner hard-caps itself at `min(cpu_count, 8)`; no code change was made for this canonical run |
| completed | **540/540**, `exit 0` |
| wall time | **72 s** (runner-reported 71.85 s) |
| output | 431,903 B, sha256 **`2e1bcb01c790dbc4f8229b605925e3190bd40fce6c2ad8d948472dfc377d217f`** |
| copy kept | [`results/audit/hk_korea_comparative_with_cf4_repro_box8w_2026-11-25.json`](../../results/audit/hk_korea_comparative_with_cf4_repro_box8w_2026-11-25.json) + `.sha256`, stdout [`run_box_8w.log`](../../results/audit/run_box_8w.log), meta [`run_box_8w.meta`](../../results/audit/run_box_8w.meta) |

**Run B — 56-worker parallelization-only variant** (the lane brief asked for 56 workers; the box allocation was
later corrected to a **10-CPU cgroup with ≤8 workers across all lanes / ≤4 per lane**, so Run B — already
completed — is retained only as a worker-count invariance check, and no further box jobs were run). One line
changed in a *copy* of the runner — `workers = min(os.cpu_count() or 2, 8)` → `workers = 56`; seeds, arms, tasks,
ordering and math untouched:

```
diff (exact, stored at results/audit/box56w_runner_variant.diff):
205c205
<     workers = min(os.cpu_count() or 2, 8)
---
>     workers = 56
```

Result: **540/540, exit 0, 100 s**, 431,903 B, sha256 **`7620a983cd8cebcd6838efc5654d31cf792e198626876142bd884965f67b7b43`**
(copies: [`…repro_box56w_2026-11-25.json`](../../results/audit/hk_korea_comparative_with_cf4_repro_box56w_2026-11-25.json),
[`run_hk_korea_comparative_56w_variant.py`](../../results/audit/run_hk_korea_comparative_56w_variant.py),
[`run_box_56w.log`](../../results/audit/run_box_56w.log)). **Run B vs Run A: all 9,180 seed + 846 summary numeric
values bit-identical (max abs diff 0.0); only `elapsed_seconds` differs (71.85 → 99.63).** Worker count therefore
does not affect the numbers.

### Box vs reference and box vs host (comparator reports in `results/audit/`)

| comparison | seed values | summary values | total differing | max abs | max rel | differences at 2 d.p. |
|---|---|---|---|---|---|---|
| box (numpy 1.24.1) vs **supplied reference** — `compare_box8w_vs_reference.json` | 9,164 / 9,180 exact (16 diff) | 831 / 846 exact (15 diff) | 31 | **7.1054e-15** | **4.9711e-16** | **0** |
| box vs **host Mac** (numpy 2.2.6) — `compare_box8w_vs_mac.json` | 9,166 / 9,180 exact (14 diff) | 832 / 846 exact (14 diff) | 28 | **7.1054e-15** | **3.9609e-16** (seed) / 3.2462e-16 (summary) | **0** |
| box 56-worker vs box 8-worker — `compare_box56w_vs_box8w.json` | 9,180 / 9,180 exact | 846 / 846 exact | **0** | **0.0** | **0.0** | **0** |

Per-field detail: `results/audit/per_field_diff_box_vs_reference.{md,csv}`, `per_field_diff_box_vs_mac.{md,csv}`,
`per_field_diff_box56w_vs_box8w.{md,csv}`. In every pair, all `total_spend_index` values and all summary means/sd/
CIs are identical at report precision; only `metadata.elapsed_seconds` differs among non-numeric/metadata fields.

**Box constraints honoured:** private dir `/root/work/gate0` only; `nice -n 10`; BLAS/OpenMP threads pinned to 1;
no shutdown/reboot/poweroff; no watchers/timers; the in-flight torch pip install was left alone (no second
install); load stayed well below the 60 back-off threshold (loadavg ≈ 8–16 from the pip download and other lanes).

---

## 5. Consolidated mismatch table and verdict

| comparison | exact | differing | max abs | max rel | 2-d.p. mismatches | verdict |
|---|---|---|---|---|---|---|
| host rerun vs committed 540 JSON `c1fa0926…` | all 9,180 + 846 | 1 field (`elapsed_seconds`) | 0.0 (numerics) | 0.0 | 0 | **bit-identical (modulo wall clock)** |
| host vs supplied reference `851bb1df…` | 10,556 / 10,566 | 10 | 3.5527e-15 | 2.0937e-16 | 0 | within float tolerance |
| box (np 1.24.1) vs supplied reference | 10,535 / 10,566 | 31 | 7.1054e-15 | 4.9711e-16 | 0 | within float tolerance |
| box (np 1.24.1) vs host (np 2.2.6) | 10,538 / 10,566 | 28 | 7.1054e-15 | 3.9609e-16 | 0 | within float tolerance |
| box 56-worker vs box 8-worker | 10,566 / 10,566 | 0 | 0.0 | 0.0 | 0 | bit-identical (modulo wall clock) |

**Gate-0 verdict: WITHIN TOLERANCE.** There is **no mismatch beyond declared floating-point tolerance**; the
only non-`elapsed_seconds` differences are last-bit doubles from different libm/BLAS implementations and
interpreter/NumPy versions (host NumPy 2.2.6 vs box 1.24.1; different CPU architectures). No reported figure
changes at any precision the deposit uses (2 d.p. spend indices, 1–2 d.p. shares/gaps, CI bounds printed to 2 dp).

---

## 6. The 420-run vs 540-run generation difference (author-recorded; NOT reproduced here)

The review (`REVIEW_RESPONSE_2026-11-25.md` §1) records two different model generations behind the same paper:

| | 420-run record `results/verified_results_2026_11_25.json` (`runs: 420`, 14 arms × 30 seeds) — Paper B docx tables | 540-run record `results/hk_korea_comparative_with_cf4.json` (18 arms × 30 seeds) — reproduced in Gate 0 |
|---|---|---|
| design | **N = 400, T = 70** (author-recorded; the 420-era runner is **not runnable** against the committed engine) | **N = 300, T = 46** (hardcoded in the supplied runner, `measure_from=18`) |
| y_median / subsist / borrow | 3.0 / .15 / .5 | 2.2 / 2.0 / .35 / .25 |
| contest_alpha / price | 1.2 / 1.25 · .12 / .11 | .25 · .16 |
| max_e / elite_logw | 4.0 / 4.5 · .85 / 1.15 | 6.0 · .50 / .60 |
| bar gates | 0 / 0 / 0 | 2 / 4 / 10 |
| HK baseline elite Q5 | **30.0 %** | **46.36 %** |
| KR baseline elite Q5 | **24.6 %** | **36.12 %** |
| HK / KR tax spend | 104.8 / 107.4 | 107.42 / 106.46 |
| HK / KR cap −50 % spend | 82.1 / 74.1 | 67.39 / 76.42 |
| HK / KR large-seat spend | 173.8 / 122.3 | 149.30 / 128.00 |

Evidence status of that table: **AUTHOR-REPORTED / author-recorded** — Gate 0 verified the 420 file's contents
(sha256 `b14e2816…`, 7,224 B, "COMPLETED, runs: 420, seeds_per_arm: 30") and its inclusion in the archive bundle
MANIFEST, but **not the 420 run itself**: no 420-era runner, seeds or engine generation were supplied, and the
committed runner produces the 18-arm/540-run generation. The Paper B docx tables therefore remain un-reproduced.
Consequence for downstream gates: no paper table may be treated as Gate-0-reproduced; only the 540-generation
JSON is.

---

## 7. Artifact registry and archive-branch inventory (deliverable 2)

- [`docs/audit/ARTIFACT_REGISTRY.csv`](ARTIFACT_REGISTRY.csv) — **87 rows**, columns
  `path,sha256,bytes,origin,evidence_status,notes`, all sha256 recomputed from the files on disk (no transcription).
  Coverage: `papers/shadow-education-contest/**` (27 files: docs, code, the 540 output, the supplied reference, the
  420 record, GPU scripts, both manuscripts + 4 figures), `engine/eduengine/**` + `engine/requirements.txt` +
  `research/requirements.txt` (16 files), 15 key files of the archive-branch all-in-one bundle, and all 26 Gate-0
  output/evidence files plus the 3 Gate-0 documents.
  Status distribution: **REPRODUCED SIMULATION 50 · AUTHOR-REPORTED 27 · UNRESOLVED 7 · VERIFIED EMPIRICAL 3.**
- [`docs/audit/ARCHIVE_BRANCH_INVENTORY.csv`](ARCHIVE_BRANCH_INVENTORY.csv) — full inventory of
  `research/atlas-all-work-2026-11-25` @ **`46950abfe779d8c91aaa856919d20812d80d183e`**: **1,123 entries**
  (1,122 regular files + 1 symlink `node_modules`), each with git mode, git blob sha1, byte size and computed
  sha256, from `git ls-tree -r --long` + read-only extraction to `/tmp/gate0_archive`; 0 missing, tree never
  modified.
- **Archive MANIFEST verified:** `shasum -a 256 -c` on the all-in-one bundle's `MANIFEST.sha256` → **13/13 OK,
  exit 0** (includes the paired engine files, runner, patch, reference JSON, both docx, 3 GPU scripts, 420 record,
  and the original bundle zip `f602ede3…`).
- **Documentation discrepancies found (non-blocking, for the record):** the audit-branch copy of
  `code/rtx3080ti_gpu_scripts/README_RTX3080TI.md` (`d4d0ad79`, 2,175 B) is **not** byte-identical to the
  archive-bundle copy (`b74cd583`, 1,921 B, MANIFEST-covered); `RESEARCH_AGENDA_AND_EXPERIMENTS.md` differs
  between audit branch (`285b5ea1`) and archive (`47f5b532`, earlier revision). Engine/runner/patch/reference/docx
  files are byte-identical across both. No executed artifact is affected.

---

## 8. Evidence taxonomy — what is and is not established

**Legend used in this Gate (as required):** `VERIFIED EMPIRICAL` / `REPRODUCED SIMULATION` / `AUTHOR-REPORTED` /
`UNRESOLVED` (the programme taxonomy additionally has VALIDATED SIMULATION and CONTRADICTED; neither is used for a
Gate-0 artifact). For artifacts, `REPRODUCED SIMULATION` means "this code/data/output was executed and
independently reproduced in Gate 0"; `AUTHOR-REPORTED` means "supplied by the author/bundle and hash-verified but
not executed here"; `UNRESOLVED` means "the evidence does not exist in the tree / cannot be executed".

**Established (REPRODUCED SIMULATION):**
1. The exact committed engine (`68da16e` + `contest_gate.patch`, sha `618bd6dd`/`b2d213b6`) and the unmodified
   supplied runner (`dd0b1d8d`) produce the committed 540-run JSON bit-for-bit (modulo `elapsed_seconds`) on the
   host, and within last-bit float tolerance on a different OS/CPU/NumPy on the box.
2. The 540-run result is **environment-robust**: every reported 2 d.p. figure is unchanged across macOS ARM/NumPy
   2.2.6 and Linux x86_64/NumPy 1.24.1; worker count (8 vs 56) is numerically irrelevant.
3. The CF4a/CF4b evaluation re-run from the reproduced JSON confirms the recorded negative result: under the
   pre-stated criterion, only the single-lever **CF1b** passes in both jurisdictions; **CF4a fails HK elite share
   (48.64 % vs 46.36 % baseline, +2.28 pp)** and **CF4b fails spend in both (90.88 HK / 88.04 KR ≥ 80)**. The
   Exp-7 "wage-compression win-win" falsifier is **not met**. (SIMULATION, descriptive.)
4. Artifact provenance is closed: 87 registry rows hash-verified; archive-branch tree fully inventoried and its
   MANIFEST checks out 13/13.

**Not established (must stay AUTHOR-REPORTED / UNRESOLVED):**
1. **The 420-run generation** (Paper B docx tables: HK elite Q5 30.0 %, KR 24.6 %, etc.) — author-recorded only;
   no runnable 420-era runner/engine generation was supplied, so it cannot be reproduced or tested against the
   committed engine.
2. **Paper A Exp 1/3/4/5 simulations and the identifiability result** — no runners or raw result files; the
   `MISSING_ARTIFACTS.md` list is confirmed still missing. Paper A's empirical E8 numbers are **AUTHOR-REPORTED**
   (consistent with a committed E8 record outside this Gate's scope, not re-derived here).
3. **GPU (RTX 3080 Ti) results** — no outputs supplied and nothing run in Gate 0; the review-confirmed estimator
   flaws stand (7-parameter ABC not identified — `theta[:,5]` unused; panel `X=[1,x]` drops controls/FE).
4. **Any empirical/calibration claim** — no empirical dataset in this Gate's scope was re-derived from source;
   therefore no registry row is `VERIFIED EMPIRICAL` except the environment manifests and the computed archive
   inventory (directly observed facts, not research evidence).
5. **The original 420-run environment / pre-registration** — unrecorded in the bundle; cannot be pinned.

**Caveats on the reproduced record itself (unchanged from the prior deposit, re-confirmed):** the 540 output's
`metadata.branch`/`base_commit` strings are hardcoded in the supplied runner and describe the patch's code lineage
(`research/binding-gate-2026-11-25` / `68da16e`), not the checkout branch the run was executed from; the output
records no Python/NumPy version. `elapsed_seconds` is intrinsically machine-dependent and is excluded from every
"identical" claim.

---

## 9. Deliverables and exact paths

| # | deliverable | path |
|---|---|---|
| 1 | host env manifest | [`docs/audit/system_host.txt`](system_host.txt) |
| 1 | box env manifest | [`docs/audit/system_box.txt`](system_box.txt) |
| 2 | artifact registry (87 rows) | [`docs/audit/ARTIFACT_REGISTRY.csv`](ARTIFACT_REGISTRY.csv) |
| 2 | archive-branch inventory (1,123 entries) | [`docs/audit/ARCHIVE_BRANCH_INVENTORY.csv`](ARCHIVE_BRANCH_INVENTORY.csv) |
| 3 | host reproduction output (+ sha256) | [`results/audit/hk_korea_comparative_with_cf4_repro_mac_2026-11-25.json`](../../results/audit/hk_korea_comparative_with_cf4_repro_mac_2026-11-25.json) |
| 3 | host vs reference comparator report | [`results/audit/compare_mac_vs_reference.json`](../../results/audit/compare_mac_vs_reference.json) |
| 4 | box reproduction output, unmodified runner (+ sha256) | [`results/audit/hk_korea_comparative_with_cf4_repro_box8w_2026-11-25.json`](../../results/audit/hk_korea_comparative_with_cf4_repro_box8w_2026-11-25.json) |
| 4 | box vs reference / box vs host / 56w-vs-8w reports | `results/audit/compare_box8w_vs_reference.json`, `compare_box8w_vs_mac.json`, `compare_box56w_vs_box8w.json` |
| 4 | per-field diff tables (4 pairs, md+csv) | `results/audit/per_field_diff_*.{md,csv}` |
| 5 | this report | `docs/audit/GATE0_REPORT.md` |

Reproduction commit: `[gate0] …` on `research/contest-audit-v2-2026-11-25` (audit branch only; not pushed; no
other lane's files touched; the pristine `wt4/repro` engine/runner hashes are unchanged).

## 10. Acceptance checklist

- [x] Host + box environment manifests written with exact tools/versions/hashes.
- [x] `ARTIFACT_REGISTRY.csv` ≥ 40 artifacts (87) with real sha256 for every row; archive branch fully inventoried.
- [x] Legacy 540-run reproduction: exact command, 119 s wall, exit 0, output sha256, comparator report, per-field
      max abs/rel diffs.
- [x] Independent box re-run: exit 0, 72 s, separate output file + sha256 (host artifact not overwritten), max
      abs/rel diffs reported, every 2-d.p. figure matches; box numpy floor deviation recorded.
- [x] `GATE0_REPORT.md` with verdict (WITHIN TOLERANCE), commands, timings, hashes, mismatch table, the
      author-recorded 420-vs-540 generation difference, and the evidence taxonomy of what is/is not established.
