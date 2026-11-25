# Missing artifacts — status after the canonical bundle (update 2026-11-25 14:05 CST)

**Bottom line:** the canonical all-in-one bundle (`/tmp/ALL_ATLAS_WORK_2026_11_25.zip`, sha256
`f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74`) arrived and was integrated. The two engine
files and the tested runner were verified byte-identical to it, applied additively on this branch, and the
540-run HK/Korea CF4 job was reproduced against the supplied reference (SIMULATION). The Paper A manuscript
`.docx` and three GPU job scripts also arrived. Still missing: the five individual result JSONs / runners for
Exp 1/3/4/5, so those numbers remain author-reported, and Paper A's simulations were **not** run here.

| # | artifact | status | needed for |
|---|---|---|---|
| 1 | Paper A `.docx` (Google Doc `1NFXSjzRaAXR2nhM6iZVTlhJKcE5puj7PI43ZZkP2cns`) | **RECEIVED (draft)** — `paper_a_general_mechanism/When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`, 369,246 bytes, sha256 `39092abb…0c91`; deposited as received, its simulations **not** reproduced here | Paper A text |
| 2 | `engine/eduengine/core.py` **patched file/diff** (Tullock `contest` gate) | **RECEIVED & APPLIED** — exact bundle file, sha256 `618bd6dd…fb4f`; `git diff` equals `code/contest_gate.patch` | Exp 3, 5, Paper B |
| 3 | `engine/eduengine/modules/tutoring.py` **patched file/diff** | **RECEIVED & APPLIED** — exact bundle file, sha256 `b2d213b6…4308` | Exp 3, 5, Paper B |
| 4 | `run_hk_korea_comparative.py` | **RECEIVED & RAN** — tested bundle runner, sha256 `dd0b1d8d…bcec`; 540/540 runs, exit 0; see `RUNNER_STATUS.md` | Paper B |
| 5 | `results/exp1_bulge_arrival_summary.json` | bundled inside `results/verified_results_2026_11_25.json` (self-reported only; **not** re-run) | Paper A Exp 1 |
| 6 | `results/exp3_contest_h1_h2_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported only; **not** re-run — only Paper B's runner was supplied) | Paper A Exp 3 |
| 7 | `results/exp4_tutoring_identifiability_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported only; **not** re-run) | Paper A Exp 4 |
| 8 | `results/exp5_e8_shock_summary.json` | bundled inside `verified_results_2026_11_25.json` (self-reported only; **not** re-run) | Paper A Exp 5 |
| 9 | `results/hk_korea_comparative.json` | **RECEIVED FROM RUN (18-arm design)** — `code/results/hk_korea_comparative_with_cf4.json`, sha256 `c1fa0926…2e99`; reproduces the bundle reference to last-bit float; note this is the runner's 18-arm / 540-run / `N=300` / `T=46` design, **not** the draft's author-reported 14-arm / 420-run / `N=400` / `T=70` design | Paper B |
| 10 | Exact patched engine commit / pre-registration hashes | **PARTLY RECEIVED** — exact files + patch + bundle-reference hashes are committed (`code/REPRODUCTION_CF4_2026-11-25.md`, `code/results/reference/`); still **no** pre-registration/hash record for the original 420-run Paper B design | reproduction of all simulation claims |

## Why this matters

- The committed `eduengine` (pre-patch) had **only `bar` and `quota`** gate kinds; the dispatch is
  `if kind == 'bar' … else: # quota`, so an unknown kind would be silently treated as quota. The exact patch
  is now committed on this branch, so gate kind `contest` is real code here — but only for this branch, and
  only as SIMULATION evidence.
- **CF4a/CF4b (Exp 7) did not meet the pre-stated Win-Win criterion.** CF4a fails in Hong Kong on elite
  capture (+2.28 pp above baseline; Korea passes); CF4b fails in both jurisdictions on spend (90.88 / 88.04
  vs the < 80 cutoff) even though elite share falls. The only arm meeting the criterion is the single
  effort-cap arm CF1b. See `REPRODUCTION_CF4_2026-11-25.md`. Do not cite the draft's "wage compression
  reaches the Win-Win Zone" reading as reproduced.
- The committed bulge-arrival record says `t*` is **NOT-ESTIMABLE** in-repo (`L_primary` sourced 0/8). Exp 1
  claims a live-WDI series (7,290 observations); that data and its hashes must be committed to make the
  claim auditable — still missing.
- The shadow-equations identifiability work is currently **quarantined** (`research/shadow-equations-review-2026-11-25`
  @ `264c059`); Exp 4 must be reconciled with that record before citation — still missing.
- The Paper B manuscript's own calibration/counterfactual table (14 arms) is still **author-reported**; the
  reproduced run is a different design.

## How to deposit

Attach the files to the bridge (the `send_file`/attachment path used for Paper B) or push them to this branch.
For replication, re-run:

```
cd /Users/treymenefee/neon-boot/wt3/shadow
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/run_hk_korea_comparative.py
/Users/treymenefee/neon-boot/venv/bin/python \
    papers/shadow-education-contest/code/compare_cf4_reference.py \
    papers/shadow-education-contest/code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json \
    papers/shadow-education-contest/code/results/hk_korea_comparative_with_cf4.json
```
