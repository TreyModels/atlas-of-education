# PAPER C — PILOT-0 QA (PASS)

**Owner:** qa-verifier · **date:** 2026-11-25 ~23:05 · **mode:** host-only; CPU-only campaign
**Campaign:** Paper C Pilot-0 v3 emergence campaign (NEW GENERATION), runner `papers/shadow-education-contest/code/run_paperC_pilot0.py`, engine pin **`846c9e0`** (`core.py` sha `e111397b…8e71`), spec file from re-pin `46c080d` sha `e5ddef6b…b755`.
**Payload:** `~/neon-boot/qa/incoming/paperC_results/paperC_pilot0_results.json` sha256 **`c6e50bc1e86f8d41a8d8a332e860898445de4ce90f8f9ec7d004e438fa523f9d`** (69,286 B) + 16 `ckpt_*.jsonl` + `MANIFEST_SHA256SUMS.txt` + `pilot_v3_8w.log`.
**Verdict: PASS (A1–A10 all PASS) — valid as EXPLORATORY / hypothesis-generating evidence from the pinned CPU engine. Not confirmatory; no causal claims.**

## 0. Live-run facts (independently checked)

| item | value |
|---|---|
| design | **4 regimes** (`market_only`, `own_open_gap`, `own_open_incentive`, `own_open_gap_firm_ban`) × q0 {1.0,1.2} × p_firm {0.03,0.08} × **8 seeds 0–7** = **16 cells / 128 runs** |
| regime params | own_ban/pay_ratio/monitoring/withhold_mode/firm_ban match the declared design (pay_ratio .55 except incentive 1.2; monitoring .2; firm_ban .9) |
| runtime | box process 40058 + 8 workers, `nice 10`, declared BLAS=1; **wall 6860.01 s ≈ 1 h 54 min**, completed 22:58 |
| engine pin | payload `engine_commit=846c9e0`, `engine_core_sha256=e111397b…`; **verified against git** (`846c9e0` resolves; `engine/eduengine/core.py` at that commit hashes to `e111397b…`); box core file also matched |
| spec provenance | payload `spec_sha256=e5ddef6b…` = canonical spec **file at re-pin `46c080d`**; the `846c9e0` git tree's in-tree spec (`35576f…`) is expected old content (lead-confirmed provenance, not a defect) |
| runner | `runner_sha256=bc833b76…` = the live box runner (v3, 4-regime code; the old 96-run v2 docstring is superseded). **Design-record correction:** any earlier "96 runs / 12 cells" note is wrong for this campaign. |
| manifest | `MANIFEST_SHA256SUMS.txt` verified here: **17/17 files OK** (payload + 16 ckpts); `MANIFEST.txt` sha256 `81e6d6db…` states the same pins/design/guards and is consistent with the payload |
| canonical bundle | `~/neon-boot/qa/incoming/paperC_results_bundle.tar.gz` sha256 **`ec868a57af2ad2a5e33a9b028baadad64e4caab18218b53e7d5e237129a4fb0b`** (33,095 B), extracts to `results/` with 18 files (payload + 16 ckpts + `MANIFEST_SHA256SUMS.txt`); **all 18 hashes equal the validated extracted directory** (only `MANIFEST.txt` is directory-only, added outside the bundle). The Commander's `14567f66…ac06` tar is an **independent re-gzip of the identical directory** — recorded as informal re-compression, **not** a second bundle; validation from the extracted directory stands. |

## 1. Mechanical checks (`docs/audit/pilot0_qa.py`, run against the copied bundle)

| id | check | result |
|---|---|---|
| A1 | payload present + schema | **PASS** |
| A2 | runtime engine pin + core/spec sha (verified against git, not just the hard-coded label) | **PASS** — `846c9e0`, `e111397b…`, `e5ddef6b…` |
| A3 | design 4 regimes × 2 q0 × 2 p_firm × 8 seeds = 16 cells / 128 runs; seeds 0–7 | **PASS** |
| A4 | recorded parameters match declared design (incl. withhold_mode strings) | **PASS** |
| A5 | seed completeness: all 16 `ckpt_*.jsonl` × 8 unique seeds; row regime/q0/p_firm match the cell | **PASS** |
| A6 | summary keys: 16 cell keys, all 23 metrics each, `n=8` | **PASS** |
| A7 | no-op guard fired: **12/12 non-market cells** have mean withheld > 1e-3 **and** own_share > 0.1 | **PASS** |
| A8 | EXPLORATORY label, no confirmatory/causal claim | **PASS** |
| A9 | driver log shows no `unfired events` / `RuntimeError` / `Traceback` (runner raises on non-empty `unfired_events`) | **PASS** (log is short/minimal — see caveat C1) |
| A10 | per-seed ckpt rows reproduce the published summary means/n, and the raw-row no-op guard holds (not just summary means) | **PASS** — all 16 cells |

## 2. Caveats / findings (do not over-read)

* **C1 — driver log is minimal** (587 B: only the final write line plus two numpy "Mean of empty slice" warnings). A9 therefore evidences *absence of failure strings*, not a full per-run `unfired_events` audit trail; the runner raises on non-empty `unfired_events`, and a completed 128/128 payload implies no run aborted. For future campaigns, keep the full driver log.
* **C2 — exactly two metrics are all-NaN:** `completion_primary` and `completion_upper` are NaN in **all 16 cells / all 8 seeds** (32 summary entries; the raw ckpt rows are NaN too). The keys and `n` are present and internally consistent (A10 passes); **do not cite these two metrics**. The runner's `RuntimeWarning: Mean of empty slice` comes from summarising those empty fields. **Correction to the hand-off note:** `tut_own_by_grade_last` / `tut_firm_by_grade_last` are **clean (non-NaN)** in this payload — all other 21 of 23 metrics are clean. This is a reporting-field artefact, not a run failure.
* **C3 — contamination note stands:** `own_share` / `tut_firm_by_grade` mix contest-prep with firm tutoring (runner's documented contamination note); report as recorded, do not relabel.
* **C4 — exploratory only:** hypothesis-generating; no confirmatory, multiplicity-adjusted, causal or welfare claims. `withheld`/`own_share` are engine constructs, not estimated policy effects.
* **C5 — GPU separation (lead instruction):** **Pilot-0 is a CPU-only campaign on the canonical engine pin.** The GPU PL port (`research/gpu-pl-port-auditv2-2026-11-25`) is a *separate artefact* for gate-grid/sensitivity runs only; GPU runs must not replace CPU primary artefacts or the canonical spec hash, and are not part of this Pilot-0 record.

## 3. What is signed off

Pilot-0's **mechanical execution integrity**: design/parameters as declared, 128/128 runs and 8 seeds/cell recoverable from checkpoints, runtime engine/spec pin genuine, summary keys complete and internally consistent with raw per-seed rows, and the binding no-op guard fired in all 12 non-market cells. Scope is exploratory descriptive evidence only; empirical claims from Paper C remain hypotheses, not validated effects.
