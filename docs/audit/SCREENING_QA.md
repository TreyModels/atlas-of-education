# PAPER C — SCREENING QA (PASS)

**Owner:** qa-verifier · **date:** 2026-11-26 ~07:30 · **mode:** host-only (box powered off; no compute)
**Artefact:** `~/neon-boot/qa/incoming/paperC_screening/` (36 `ckpt_*.jsonl` + `paperC_screening.json` + byte-identical `paperC_screening_results.json` + 2 `.sha256` sidecars) and queue markers `~/neon-boot/qa/incoming/paperC_screening_queue/` (`STATUS`, `RESULTS_DONE`, `SHA256SUMS`, `finalize.log`).
**Payload:** `paperC_screening.json` sha256 **`6bcc29a50d41dc2c63a5959c0b023eb203c5bf1bd0cd04ffaee908a5ebb5b6d4`**, **1,337,854 B**; `n_runs=288`, `n_cells=36`, `invalid_cells=[]`, `wall_seconds=1879.17`; duplicate `_results` byte-identical.
**Verdict: PASS (S1–S11 all PASS) for screening artefact integrity.** SCREENING-ONLY — not confirmatory; no Paper C claims are made or moved. P12=pay_gap is recorded and requires the A4/prereg clarification before any confirmatory use.

## 1. Checks (`docs/audit/screening_qa.py` → `docs/audit/results/screening_qa.json`)

| id | check | result |
|---|---|---|
| S1 | payload present; `paperC_screening.json` ≡ `paperC_screening_results.json`; `.sha256` sidecars match; 36 ckpts | **PASS** |
| S2 | queue `SHA256SUMS` (40 entries) all verify; `checkpoint_sha256` map (36/36) matches ckpt bytes | **PASS** |
| S3 | pins: engine `846c9e0`, core `e111397b…`, spec `e5ddef6b…`, runner `d2d25c1c…` (matches the repo runner file `papers/shadow-education-contest/code/run_paperC_screening.py`), prereg sha `445ec423…` = launch-manifest prereg sha; launch-manifest engine pins match | **PASS** |
| S4 | exact **36-cell grid in fixed appendix order**: S{0.85,1.00,1.15} × L{0.25,0.45} × settings{P55,P12} × arms{A,B,C}; ckpt cells = manifest cells = appendix order | **PASS** |
| S5 | 288 rows; **8 seeds 0–7 per cell**, no duplicates; N=600/T=46/measure_from=18 on every row | **PASS** |
| S6 | per-row params: supply A own_ban0/firm_ban0, B own_ban.95, C own_ban0/firm_ban.9; settings P55 pay_ratio .55/monitoring .2/pay_gap, P12 pay_ratio 1.2/monitoring .5/pay_gap; q0 = S; gate G6→G9 contest, share_of cohort, r = 1.2 at L=.25 / 1.6 at L=.45, fail stop; row engine pins; `unfired_events == []` every run | **PASS** |
| S7 | binding assertions: **exposed = A/C AND P55** — all withheld>1e-3 and own_share>0.1; B and A\|P12 exempt (actual enforcement correct) | **PASS** (metadata defect D-S1) |
| S8 | **no `completion_*` fields** (by design → no NaN there); no NaN/inf in summary means or per-seed rows | **PASS** |
| S9 | summary key set: 36 cells × 18 metrics, each with mean/sd/ci95_lo/ci95_hi and `n=8` | **PASS** |
| S10 | ckpt rows reproduce summary mean/sd (ddof=1)/n **exactly** (abs tol 1e-12), all 36×18 | **PASS** |
| S11 | label/status: `SCREENING-ONLY`, label says screening/NOT confirmatory; `p12_mode=pay_gap` with the settings-note prereg caveat; `invalid_cells=[]`; queue `STATUS=OK …`, `RESULTS_DONE` present, `finalize.log` shows verified (history: earlier FAIL → finalizer v2 OK); wall>0 | **PASS** |

## 2. Defects / notes

| id | severity | finding |
|---|---|---|
| **D-S1** | **low (fix before confirmatory)** | Runner metadata defect: per-row `assertions.exposed = (supply in (A,C))` and the per-row rule text says only "B exempt" (`run_paperC_screening.py:207`), so **A\|P12 is mislabelled exposed** (96 row flags = 12 cells × 8 seeds). The **actual binding check** (`run_paperC_screening.py:154`) correctly applies only to `A/C AND P55`; A\|P12 has h=0 and was not asserted; `invalid_cells=[]` and S7 enforcement passes. **No effect on screening results**, but the metadata/rule text contradicts prereg A3.3 — fix the flag/rule text before confirmatory and re-emit if a confirmatory bundle is generated. |
| D-S0 | info | Launch manifest records the *pre-launch* runner sha `fbeba460…` while the executed runner is `d2d25c1c…` (documented "screening runner extended before launch; launch sha recorded in run manifest"). The actual runner file matches the run manifest sha exactly; reconciled, no action. |
| D-S2 | info | Row `params.contest_r` is the static engine default 1.5, while the G6→G9 gate override sets `gate.r` by L (1.2/1.6) and the engine uses the gate override (`core.py`: `r = p["contest_r"] if r is None else r`). `gate.r` is authoritative; harmless but potentially confusing for downstream readers. |

## 3. Scope caveats (do not over-read)

* **Screening only.** Seeds 0–7 are exposed/exploratory; no confirmatory inference, multiplicity-adjusted claim, causal statement, or welfare claim. The confirmatory block (seeds 100–131) is a separate frozen-passer run.
* **P12 = pay_gap** is recorded in the manifest. The settings note flags that if `incentive` was actually intended, the prereg needs an explicit amendment before confirmatory; A3.3 exempts A\|P12 because h=0 under pay_gap. **A4 clarification required before confirmatory** (lead's condition), and the frozen passer list must be written into the launch manifest before any confirmatory run.
* **>6-passer rule (A3.1)** applies downstream: first 6 passers in appendix order run confirmatory; remaining passers are screening-only. This QA does not select passers.
* **No `completion_*` fields** exist in this design (so the Pilot-0 all-NaN completion caveat is N/A here); `own_share_financial_proxy`, absolute counts/spends are declared **PROXIES** (contest-prep contamination noted in every row's `proxy_flags`).
* Queue history: an early finalizer wrote FAIL (row/cell verification), the v2 finalizer re-verified the same artefact and wrote OK at 17:15:58Z; the Mac-side re-verification here (S1/S2/S10) is independent and clean.
* Grid order, counts, and hashes are verified; numbers in the summary are **not** interpreted or cited as findings here.

**Sign-off:** screening artefact **PASS** for the 36-cell/288-run bundle at payload `6bcc29a5…`; confirmatory remains **not authorised** pending the A4/prereg clarification, frozen passer list, and (if run) the separate confirmatory QA.
