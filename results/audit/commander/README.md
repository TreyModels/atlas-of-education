# Commander independent verification — legacy 540-run reproduction (Gate 0)

**Purpose:** independent re-execution of the legacy 540-run HK/Korea CF4 job, by the execution owner, from a
**clean `git archive` extraction of `HEAD`** (not from audit-runner's worktree and not from `wt4/repro`), so that
Gate 0's "bit-identical to the committed reference" claim does not rest on a single lane's run.

**Provenance of the extracted code** (`/tmp/cmd-verify`, extracted with `git archive HEAD` at commit `7356c97`,
branch `research/contest-audit-v2-2026-11-25`; `git diff --stat 1c3417c HEAD -- engine/` is empty, so the engine is
byte-identical to the directive start commit `1c3417c`):

| file | sha256 |
|---|---|
| `engine/eduengine/core.py` | `618bd6ddce27691243111bae138a8d7aede6d59d25d2d9faa2caed24bd67fb4f` |
| `engine/eduengine/modules/tutoring.py` | `b2d213b65318fddd0c9555cd25f27714d46609036167079393bcb289c9d64308` |
| `papers/.../code/run_hk_korea_comparative.py` | `dd0b1d8d1a17e4639e45c1ae085d4efe5be613fde509c62f7a8345170786bcec` |

**Command (exactly):**

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

**Result:** exit 0, `540/540` runs on 8 workers, wall **100.79 s** (user 9 m 9.7 s). Output JSON preserved here as
`hk_korea_540_commander_independent_2026-11-25.json` (431,902 bytes, sha256
`722c370bfc00a339174bf3135f12389dbc53d87a7f607639814ebf43056eaf54`).

**Comparison to the committed bundle reference**
(`papers/.../code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`, sha256
`851bb1dfb6acd67aea6025a11941fa50105a3c41261d566821b730ab3d0fe41b`):

* 9,180 seed-level numeric values: **9,174 exactly equal, 6 differ** by ≤ `3.553e-15` absolute (`2.094e-16` relative,
  one ulp) — same three rows/fields as documented before (rows 130, 311, 379; `q5_q1_spend_ratio` and
  `k12_spend_by_q[0]`).
* 846 summary numeric values: **842 exactly equal, 4 differ** by ≤ `4.441e-16` (`2.486e-16` relative) — the four
  `KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio` statistics.
* Every `total_spend_index` value (2 d.p.) identical; no non-numeric difference; the **only** other differing stored
  number is `metadata.elapsed_seconds`. In total **11 stored numbers differ out of 10,026 numeric values compared**
  (elapsed + the 10 last-bit values).
* **Interpretation:** REPRODUCED SIMULATION — identical to the reference up to last-bit floating-point rounding, no
  substantive discrepancy. `elapsed_seconds` is wall time and is expected to differ.

**Cross-lane check:** this run differs from audit-runner's host run (`results/audit/hk_korea_...repro_mac_...json`,
sha256 `de46b91a…185e`) in **exactly one stored field: `metadata.elapsed_seconds`** (100.79 vs 118.36). All 10,025
other numeric values are identical. File hashes of the two JSONs therefore differ (each embeds its own wall time);
the *values* are identical. This is why Gate 0 must be judged on the value diff, not on whole-file hashes.

**CF4 verdict reproduced (unchanged, inconvenient result preserved):** only **CF1b (cap −50 %)** passes the pre-stated
Win-Win criterion in **both** jurisdictions (HK spend index 67.39 / elite Q5 share 41.96 %; KR 76.42 / 26.39 %).
**CF4a fails HK equity** (spend 43.78, elite Q5 48.64 % > 46.36 % baseline); **CF4b fails spend** in both
(HK 90.88, KR 88.04 ≥ 80). Baselines: HK elite Q5 **46.36070853462158 %**, KR **36.123456790123456 %**. This is
REPRODUCED SIMULATION, not empirical.

**Files in this directory:** run JSON, reference comparison JSON (full per-field report from
`compare_cf4_reference.py`), stdout log, wall-time file, `SHA256SUMS`.
