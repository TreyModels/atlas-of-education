# Atlas handoff — start here (final state, 24 Nov 2026)

Read this file top to bottom before touching anything. It is the seam between the Codex wave / 24 Nov fleet
session and the next session. It replaces the earlier handoff text; the previous version is in git history.

## 1. What this project is

Dr. Trey Menefee's Atlas of Education. Two questions:
1. **Fertility:** is schooling a "dose" of individuation, and is "more schooling, fewer births" real?
2. **Massification:** what drove schooling for everyone — state supply, labour demand, or general development?

The empirical position after the Codex wave: **the aggregate evidence cannot separate the competing
mechanisms.** Five of 272 links travel; "robust everywhere" mislabels 87% of minority-effect worlds; MSE/BIC
fail the zero-signal control; effective fertility and TFR flip lead/lag; the 7% labour-demand figure was a
data-start artefact. That is the "macro regression wall". The wave's conclusion is **not** that the wall is
demonstrated by simulation: see §8 — the suite that was supposed to simulate it does not implement its own
tests, and the redesigned suite separates the mechanisms instead of collapsing them.

## 2. Where things are

- Repo: `TreyModels/atlas-of-education` (public). Clone and `git fetch origin 'refs/heads/*:refs/remotes/origin/*'`.
- **Dashboard (one-screen report):** `research/records/2026-11-23-dashboard/README.md` — branch
  `research/dashboard-2026-11-23` @ `8fd2ec7` at write time (may advance).
- **Verification ledger (every verified number + source):** `research/records/2026-11-24-handoff/codex_wave_ledger.md`
  on this branch.
- **Apple Silicon port:** `research/apple-silicon-gpu-2026-11-24` @ `52d74ec` — `REPORT.md`,
  `ADDENDUM_2026-11-24_env.md`, `APPLESILICON.md`, `cuda_reference/`, `results/`.
- **Suite audit:** `research/suite-lit-review-2026-11-24` @ `4649cae` (`AUDIT.md` — the ten claims to withdraw).
- **Redesign (honest H1/H4):** `research/suite-redesign-2026-11-24` @ `1de7d33` (`PRE_REGISTRATION.md`,
  `ANALYSIS.md`, `results/h1_macro_wall.json`, `results/h4_tiebreakers.json`).
- **DHS access route:** `research/dhs-acquisition-2026-11-24` @ `77a2285` (`ACQUISITION_PLAN.md`, per-individual
  test pre-registration; **no data yet**). Public-API ecological sprint may land as
  `research/dhs-api-ecological-2026-11-24` (task-16, in flight at write time).
- **Atlas bridge:** CLI at `…/DeepSeek/atlas-bridge-tools/bridge.mjs`; `ATLAS_PARTY=deepseek node "$B" status|list|read|post`.
- **AutoDL T4:** **OFF.** Powered on no later than 13:14 local, `shutdown -h now` at 18:03:06 local (关机, not
  release), SSH + MCP verified unreachable. Billing window ≤ 4 h 49 m; exact charge not visible from the
  instance and not recorded. Do not restart it for this programme — the port runs on the M1.

## 3. Final verified heads (24 Nov 2026 ~18:55 local; `git ls-remote` is authoritative)

| Item | Branch | Head | Status / content |
|---|---|---|---|
| Handoff | `research/handoff-2026-11-24` | this commit | ✓ final state + STATUS |
| Port (CUDA→Apple) | `research/apple-silicon-gpu-2026-11-24` | `52d74ec` | ✓ kernel verified vs 10 real CUDA launches |
| Q1 mechanisms | `research/q1-mechanisms-2026-11-25` | `9b0cabe` | ✓ |
| Q2 pathways | `research/q2-pathways-2026-11-25` | `9a4f586` | ✓ errata (yardstick) |
| Q3 calibration | `research/q3-multiverse-calibration-2026-11-25` | `db7814d` | ✓ |
| E1 multiverse R=1200 | `research/e1-multiverse-1200-2026-11-25` | `6a452a4` | ✓ errata (136-parity) |
| E6/E8 sequencing | `research/e6e8-sequencing-2026-11-25` | `bd782be` | ✓ errata (data unchanged) |
| E11 fertility audit | `research/e11-fertility-audit-2026-11-25` | `e926575` | ✓ |
| Source verification | `research/codex-source-verification-2026-11-25` | `ea6bc61` | ✓ metadata erratum |
| Methods paper | `research/methods-multiverse-paper-2026-11-23` | `d7e8f9f` | ✓ |
| Paper F | `research/paper-fertility-2026-11-25` | `23928e0` | ✓ −0.227 rounding applied |
| Paper M revision | `research/paper-massification-2026-11-25` | `fb9f419` | ✓ E6/E8 integrated, 7% retracted |
| Paper N1 revision | `research/paper-sequencing-novel-2026-11-25` | `62c27a3` | ✓ |
| Suite audit | `research/suite-lit-review-2026-11-24` | `4649cae` | ✓ |
| Tie-breaker prereg | `research/suite-tiebreakers-2026-11-24` | `e526c94` | ✓ design only |
| Suite redesign | `research/suite-redesign-2026-11-24` | `1de7d33` | ✓ H1 separable; H4 cannot test |
| Prose-data audit | `research/prose-data-audit-2026-11-24` | `ff390fe` | ✓ |
| Synthesis | `research/codex-wave-synthesis-2026-11-24` | `f23f239` | ✓ latest |
| Dashboard | `research/dashboard-2026-11-23` | `8fd2ec7` | ✓ latest |
| DHS access | `research/dhs-acquisition-2026-11-24` | `77a2285` | ⏳ waiting on human (no microdata) |
| DHS public API | `research/dhs-api-ecological-2026-11-24` | not pushed at write time | ⏳ task-16 in flight |

## 4. Non-negotiable rules

1. **Never rewrite, force-push or delete an existing branch.** New branch per job: `research/<topic>-YYYY-MM-DD`.
   No PRs unless Trey asks.
2. **PRE_REGISTRATION.md first**, committed before any run. Do not change the rule after seeing results; if you
   must, say so (a dated amendment committed before the confirmatory run is acceptable; see the redesign).
3. **Recompute before quoting.** Every number must be reproduced from a committed file or labelled UNVERIFIED.
4. **No secrets** in the repo, logs or chat.
5. **No causal language** unless an event study with checked pre-trends; then "consistent with".
6. **Label data tiers**: observed / reconstructed / model-imputed. Never call effective fertility (surviving
   children) "TFR".
7. **GPU runs must pin and log batch layout**; no bit-identity claims across architectures without testing.
8. **Report everything** — nulls, failures, discarded runs; record commit, hashes, seeds, wall time.
9. **Simulation is not history.** A model winner is not a cause; a counterfactual is model-conditional.
10. **Shut the rented instance down** when a job finishes (关机, not release).

## 5. Things that must never reappear (retracted / settled / annotated)

- **"7%" labour-demand figure** — a 1991+ data-start artefact. E6 replacement: demand-first 10.0% (GGDC), 15.4%
  (urban), 24.1% (industry), 18.8% (agri), bounds 6.7–53.0%, ties/censoring 21–43% → "schooling and structural
  change move together".
- **Effective fertility called "TFR"** — different constructs (median |diff| 0.3042, max 4.2677; lead/lag 0.541
  vs 1.555).
- **68.75% / 69% schooling-before-fertility** — tie-counting artefact; strict ordering 37.5% (24/64, CI
  26.6–50.0), simultaneous 31.25%, fertility-first 31.25% (`subsistence-v2 @ 8caaeac`).
- **"Robust everywhere" as a homogeneity certificate** — mislabels 87% of minority-effect worlds (Q3).
- **"BY certifies zero" as universal** — draw-budget statement: 0 at R ≤ 800; at R=1200 BY certifies 32
  heterogeneity links (272-link convention).
- **"400 draws can certify nothing"** — wrong; BH step-up certifies a floor cluster (35 up at 400; 41 at 1200).
- **E1 136-parity sentence** — corrected at `6a452a4`: up/down/flip certify **25/15/0** and BY heterogeneity
  certifies **39** at R=1200 (not "0/0/0").
- **Q2 yardstick** — corrected at `9a4f586`: matched-pair medians **0.620 (schooling) / 0.2375 (TFR)**;
  shares **96.1% / 100.0%** (not 52.4% / 50.3%). The all-pairs 0.82 / 0.7715 comparison must not be quoted as
  the matched-pair statistic. Direction of Q2's honest null survives.
- **E6 errata** — `bd782be`: "18–33% strict schooling-first" → **21.5–46.3% of identifiable countries**; N3
  "56–84% weak forward-or-tie" stale; controls **28–30** (not 25–30); mean post **12.3–26.2** (not 18–29),
  placebo −0.39.
- **Source-verification metadata** — `ea6bc61`: 24 prior-art works checked = 21 verified / 2 unverified / 1
  wrong metadata; quote the corrected statuses, not the earlier counts.
- **Paper F rounding** — `−0.228` → **−0.227** (coefficient −0.227458; SE 0.042, n 1,394, 144 countries
  unchanged); applied at `23928e0`. Do not cite the old head `4f8a61c`.
- **The suite's own H1/H2/H4 claims** — see §8 and `AUDIT.md` §9.

## 6. Fleet state / open work

All 24 Nov tasks closed except DHS-dependent work. Key results:
- **Port**: kernel transcription verified against the real CUDA kernel (10 launches; 0 int mismatches; max abs
  3.815e-6). Data-stream CUDA equivalence **not** claimed (CuPy 13.6 has no Philox `default_rng.normal`; the
  upstream scripts fail as shipped — failure preserved).
- **Redesign**: H1 = **separable** (slopes −0.155 / −0.027 / −0.270; joint p = 4.8e-25; no CI overlap);
  H4 = **cannot test (F3)** (all four measurement-layer tie-breakers rejected as transforms of the weights,
  R² 0.974–0.991; s=0 and algebraic-equivalence placebos exactly at chance). See §8.
- **DHS**: access route + per-individual pre-registration only; **no microdata**. Public-API ecological sprint
  in flight (task-16).
- **Papers M/N1** revised; **Paper F** rounding fixed; synthesis/dashboard folded in the audit + errata.

## 7. Next moves

1. **DHS**: submit the second African project request; complete the DUA; download IR files; run the
   pre-registered individual schooling→children-ever-born test (cohorts; EFR/TFR construct split). This is the
   only route to a real micro tie-breaker — do not substitute model proxies.
2. **Downstream errata**: correct anything still quoting the values in §5 before publication; re-read
   `research/prose-data-audit-2026-11-24` @ `ff390fe`.
3. **If the suite is revived**, it needs a different model and different observables (redesign `ANALYSIS.md` §4),
   not another port or another run of the shipped code. Do not analyse the old PORT-PRODUCTION exp2/exp3
   outputs as evidence.

## 8. What not to believe

- **The ten claims in `AUDIT.md` §9** must not be published in their original form: (1) "the macro wall is
  demonstrated / DGPs collapse to identical macro slopes"; (2) "binary bans backfire"; (3) "protective capacity
  reduces child labour while fee abolition does not"; (4) "a micro tie-breaker passes the Q1 zero-signal
  control"; (5) "rejection-ABC calibrates the model / identifies weights"; (6) "fee abolition reduces child
  employment"; (7) "learning-per-grade slope tested"; (8) "the 3/4-DGP structure maps faithfully to the cited
  mechanisms"; (9) "hidden work is measured"; (10) "the mixed DGP is a mixed-mechanism world". Safer forms are
  in the audit.
- **Six dashboard overclaims** corrected during the wave (documented in the dashboard README "Corrections made
  during the wave" and the synthesis corrections): the 68.75% tie artefact; "400 draws can certify nothing";
  four wrong world-polity / book-as-article DOIs in Paper M; wrong-title references in Paper F; a Paper F
  commit-message overclaim; and the Q2 yardstick (52.4%/50.3% must not be quoted). Do not reuse pre-correction
  dashboard text.
- **The macro wall and the micro tie-breaker are UNTESTED by simulation.** The old suite cannot test them
  (audit). The redesign's honest verdicts: H1 separable (the wall does **not** follow from separable mechanisms
  in this model), H4 cannot test (model observables are construction-implied). Neither verdict is evidence about
  real economies; both must be labelled SIMULATION.
- **The old PORT-PRODUCTION exp2/exp3 numbers** (macro accuracy 0.767 / micro 1.000; exp3 width ratios) are
  construction-implied artefacts, not an H1/H4 test — do not quote them as findings.

## 9. Human blockers

- **DHS registration / data-use agreement approval** (Trey must complete; then IR downloads).
- **Second African project request** still to be submitted (the current application is pending).
- **Microdata cannot enter the public repo** — analyses stay local/controlled; only derived, non-disclosive
  outputs may be committed.
- **T4 billing**: exact charge unknown (window ≤ 4 h 49 m); instance is off, not released.

## 10. Verification checklist (run 24 Nov ~18:50 local; results recorded in `research/records/2026-11-24-final-status/STATUS.md`)

- `git ls-remote` heads match §3 (fetched same session).
- All fleet worktrees clean (0 dirty entries each).
- Ancestry: 5 branches fork at `94b612d4` (a main commit); the rest descend from `55732f4`; no rewrite/force-push
  evidence in local records (remote reflogs are not public — stated limit).
- No secrets found in `research/` paths of any fleet head (private-key/token/password pattern scan).
- **Nine ledger headlines recompute** from committed source files: all eight recompute groups byte-identical to
  the synthesis record's `results/recompute.json`.
- Labels: `PORT-*` for the port, `SIMULATION` for the redesign, `OBSERVED` for observed-data records.

## 11. Quick sanity checks

```bash
git fetch origin 'refs/heads/*:refs/remotes/origin/*'
git log origin/research/suite-redesign-2026-11-24 --oneline -1        # expect 1de7d33
git log origin/research/apple-silicon-gpu-2026-11-24 --oneline -1     # expect 52d74ec
git log origin/research/paper-fertility-2026-11-25 --oneline -1       # expect 23928e0 (not 4f8a61c)
git show origin/research/suite-redesign-2026-11-24:research/records/2026-11-24-suite-redesign/ANALYSIS.md | grep -E 'H1:|H4:'
ssh autodl3 'echo up' 2>&1                                            # expect connection failure (T4 is off)
```

## 12. Addendum — post-handoff work pushed 24 Nov 2026 ~19:35 local

New origin heads beyond §3:

- **DHS public-API ecological sprint** — `research/dhs-api-ecological-2026-11-24` @ **`708e34a`**: OBSERVED/ECOLOGICAL published cells, no microdata. Prior attempt reproduced (−0.554 / −1.608 / −2.520; 1,291 cells, 86 countries); gradient across **346 surveys: 98.8% negative, median −1.90** children; robust to country+period FE, country×survey FE, country trends; period-TFR vs completed-CEB ratio **1.017 [0.944, 1.102]**; surviving-children ≠ TFR; the individual Recode test remains blocked on DHS approval and is not substituted.
- **Synthetic loop Phase A** — `research/synthetic-loop-2026-11-24` @ **`394fb32`**: four literature worlds calibrated non-degenerately; H1 **separable**, H4 **cannot test (F3)**; construct-correct ABC pre-audit (w_push / w_tutor identified; div / w_pov unidentified); pre-registered DHS day-one micro signature.
- **Synthetic matrix v1 and v2** — `research/synthetic-matrix-2026-11-24` @ **`ff42c4b`**: v1 (`be7e499`) 55.6% cross-world indistinguishable; v2 (`52dfcb7`) **26.1%** (dose ladder 22.5 / 25.4 / 30.4%), with a misspecified Pritchett world (Rm) not collapsing the worlds; synthetic robust-across-groupings 70–85% vs E1's 1.8%. v2b pre-registration + parallel driver (`ef5541c`), runner scripts committed (`ff42c4b`); v2b run in flight on region-42.
- **Synthetic loop Phase B (scripts)** — `research/synthetic-phaseb-2026-11-24` @ **`81112ab`**: birth-history layer + dynamic tie-breaker scripts committed; server run in flight, results to follow.

**Compute site:** region-42 (96 cores, 375 GB RAM, RTX 2080 Ti) is the compute site; AutoDL T4 remains **off**. GPU currently idle pending a fixed-seed NumPy-vs-CUDA equivalence (no CuPy kernel backend yet); the NumPy CPU pool is the workhorse. Mac has no project compute.

**In flight at this push:** v2b matrix run, Phase B verdict, GPU equivalence probe. No new secrets.
