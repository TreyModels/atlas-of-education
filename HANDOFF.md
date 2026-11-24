# Atlas handoff — start here (24 Nov 2026)

Read this file top to bottom before touching anything. It is the seam between the previous DeepSeek session (which ran the Codex wave) and the next one.

## 1. What this project is

Dr. Trey Menefee's Atlas of Education. Two questions:
1. **Fertility:** is schooling a "dose" of individuation, and is "more schooling, fewer births" real?
2. **Massification:** what drove schooling for everyone — state supply, labour demand, or general development?

The empirical position after the Codex wave: **the aggregate evidence cannot separate the competing mechanisms.** Five of 272 links travel; "robust everywhere" mislabels 87% of minority-effect worlds; MSE/BIC fail the zero-signal control; effective fertility and TFR flip lead/lag; the 7% labour-demand figure was a data-start artefact. That is the "macro regression wall", and the forward programme is **micro-simulation + micro tie-breakers**, not more aggregate regressions.

## 2. Where things are

- Repo: `TreyModels/atlas-of-education` (public). Clone and `git fetch origin 'refs/heads/*:refs/remotes/origin/*'`.
- **Dashboard (the one-screen report):** `research/records/2026-11-23-dashboard/README.md` (branch `research/dashboard-2026-11-23`; check origin for the latest head).
- **Verification ledger (every verified number + source):** `research/records/2026-11-24-handoff/codex_wave_ledger.md` on this branch.
- **GPU suite (the new forward programme):** `research/records/2026-11-24-gpu-suite/` on this branch — `METHODOLOGY.md`, `PRE_REGISTRATION.md`, `run_all.sh`, and four scripts (exp1/exp3 are CuPy; exp2/exp4 are CPU pandas).
- **Atlas bridge (shared message board with Codex/Claude):** CLI at `/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/atlas-bridge-tools/bridge.mjs`; use `ATLAS_PARTY=deepseek node "$B" status|list|read|post`. Read `codex` messages first; the latest handoff and final status are there.
- Server: AutoDL instance via `ssh autodl3` (region-9, T4, 8-core cgroup, 60GB) — **idle and should be shut down (关机, not release)** to stop billing; disk holds E1 checkpoints and the restored panel. MCP `mcp__autodl__*` points at it.

## 3. Verified heads (do not re-run; verify before quoting)

| Item | Branch | Head |
|---|---|---|
| Q1 mechanisms | research/q1-mechanisms-2026-11-25 | 9b0cabe |
| Q2 pathways | research/q2-pathways-2026-11-25 | f71b789 |
| Q3 multiverse calibration | research/q3-multiverse-calibration-2026-11-25 | db7814d |
| E1 multiverse R=1200 | research/e1-multiverse-1200-2026-11-25 | 7e6f7b5 |
| E6/E8 sequencing | research/e6e8-sequencing-2026-11-25 | 2d19da7 |
| E11 fertility audit | research/e11-fertility-audit-2026-11-25 | e926575 |
| Source verification | research/codex-source-verification-2026-11-25 | 9a0fd69 |
| Methods paper | research/methods-multiverse-paper-2026-11-23 | d7e8f9f |
| Paper F (fertility) | research/paper-fertility-2026-11-25 | ec899cc |

Older paper-wave heads are in the dashboard section "Papers produced after the dashboard". Paper M (76d929a) and N1 (7f73ff1) are being revised to integrate E6/E8 — check their branches for newer heads.

## 4. Non-negotiable rules

1. **Never rewrite, force-push or delete an existing branch.** New branch per job: `research/<topic>-YYYY-MM-DD`. No PRs unless Trey asks.
2. **PRE_REGISTRATION.md first**, committed before any run (question, data, specification, decision rule). Do not change the rule after seeing results; if you must, say so.
3. **Recompute before quoting.** Every number from a paper, a bridge message or an old record must be reproduced or labelled UNVERIFIED.
4. **No secrets** (passwords, tokens, SSH keys, connection details) in the repo, logs or chat.
5. **No causal language** unless an event study with checked pre-trends; then say "consistent with". Associations are associations.
6. **Label data tiers**: observed / reconstructed / model-imputed. Never call effective fertility (surviving children) "TFR".
7. **GPU runs must pin and log batch layout**; fixed seed alone is not determinism. No bit-identity claims across architectures without testing.
8. **Report everything** — nulls, failures, discarded runs. Preserve logs. Record commit, input hashes, seeds, wall time.
9. **Simulation is not history.** A model winner is not an established cause; a counterfactual is model-conditional.
10. **Shut the rented instance down** when a job finishes; it bills by the hour.

## 5. Things that must never reappear (retracted / settled)

- The **"7%" labour-demand figure** — a 1991+ data-start artefact; not evidence against demand. E6 replaced it: demand-first 10.0% (GGDC), 15.4% (urban), 24.1% (industry), 18.8% (agri), bounds 6.7–53.0%, ties/censoring 21–43% → the honest framing is **"schooling and structural change move together"**.
- **Effective fertility called "TFR"** — different constructs (median |diff| 0.3042, max 4.2677; lead/lag 0.541 vs 1.555).
- **68.75% / 69% schooling-before-fertility** — a tie-counting artefact; strict ordering is 37.5% (24/64, CI 26.6–50.0), 31.25% simultaneous, 31.25% fertility-first; source record annotated at `subsistence-v2 @ 8caaeac`.
- **"Robust everywhere" as a homogeneity certificate** — it mislabels 87% of minority-effect worlds (Q3).
- **"BY certifies zero" as universal** — it is a draw-budget statement: 0 at R ≤ 800; at R = 1200 BY certifies 32 heterogeneity links.
- **"400 draws can certify nothing"** — wrong; BH step-up certifies a floor cluster (35 up at 400; 41 at 1200).

## 6. Open work at the seam

Six tasks were launched in the closing session; check whether their branches have pushed before redoing them:
- **Paper M revision** (panel-matrix): integrate E6/E8, soften supply-led framing, add fee-abolition section — `research/paper-massification-2026-11-25`.
- **Paper N1 revision** (gpu-dose): same softening for the standalone sequencing paper — `research/paper-sequencing-novel-2026-11-25`.
- **Suite prior-art + mechanism audit** (novelty-review) — `research/suite-lit-review-2026-11-24`.
- **Micro tie-breaker observables** (un-data) — `research/suite-tiebreakers-2026-11-24`.
- **DHS Individual Recode acquisition attempt** (multiverse-400) — `research/dhs-acquisition-2026-11-24` (the individual test is the biggest available upgrade; files are login-gated, so this is an access-path job, not a scraper).
- **Codex-wave synthesis + dashboard update** (methods-paper) — `research/codex-wave-synthesis-2026-11-24`.
- **CUDA → Apple Silicon port** (cuda-scale) — **DONE at `fd933d9`** (`research/apple-silicon-gpu-2026-11-24`; pre-reg `3d65715`). `gpu_compat.py` reproduces the exact CuPy subset, `shim/cupy/__init__.py` lets the upstream scripts run byte-for-byte unmodified (run-lead verified all four exp scripts, `run_all.sh`, `METHODOLOGY.md` and `PRE_REGISTRATION.md` are sha256-identical to the original on this handoff branch; no upstream file is edited), `kernels_np_mlx.py` transcribes the suite's one CUDA kernel (`sim_step`) line by line in NumPy and MLX, and embedded `cp.RawModule` CUDA C is recognised by source fingerprint (arbitrary CUDA raises `PortabilityError` — tested). Backend: MLX 0.32.4 on M1; NumPy fallback verified; PyTorch/MPS not installed (documented). RNG: Philox4x32-10 transcribed and validated; **CUDA bit-equivalence not claimed**. Equivalence: kernel NumPy vs MLX **bit-identical** (0 state mismatches), exp1 smoke 450 rows exact on state metrics and max 9.5e-7 on continuous, exp3 small-run identifiability identical — PASS. Smoke wall: NumPy 4.04 s / MLX 3.86 s; full production ran in **313 s** (exp1 7,500 rows at N=250,000, exp2, exp3 5,000 draws) and is labelled PORT-PRODUCTION, not research results. See `research/records/2026-11-24-apple-silicon-gpu/REPORT.md` and `APPLESILICON.md`.

## 7. Next three moves

1. **Analyse the ported suite's production output** (`research/apple-silicon-gpu-2026-11-24` @ `fd933d9`, `results/`): do the four DGPs collapse to identical macro slopes (the wall), and does any micro tie-breaker separate them better than the aggregate criteria? Label it simulation, not evidence; the run is already labelled PORT-PRODUCTION.
2. **Run exp1/exp2 sensitivity on the ported backend** where the pre-registration allows (seeds, parameter strengths), keeping the MLX×NumPy bit-identical check per run; do not claim CUDA equivalence.
3. **DHS microdata** if obtainable: individual-level schooling→children-ever-born, cohort comparisons, and the EFR/TFR construct split as the first real micro test.

## 8. Quick sanity checks

```bash
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
git log origin/research/e1-multiverse-1200-2026-11-25 --oneline -1   # expect 7e6f7b5
git show origin/research/paper-fertility-2026-11-25:research/records/2026-11-25-paper-fertility/draft/paperF_draft.md | grep -c "development gradient, not an identified schooling effect"  # expect 0
ssh autodl3 'ps -eo pcpu,args | grep python | grep -v grep'          # expect no compute
```
