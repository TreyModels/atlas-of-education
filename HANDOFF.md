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

## 13. Evening update (24–25 Nov 2026): staging falsified, shadow equations do not fit Bray

**Read this before the next session.** Everything in §13 is **SIMULATION or aggregate-exploratory** — no causal, historical or country claim. The compute site is **region-42** (96 cores); the T4 is **off**. §3 remains the 18:55 snapshot; §13 adds the evening heads and results.

### New origin heads

| Item | Branch | Head | Record file |
|---|---|---|---|
| Staging audit (confounds + five bounded experiments) | `research/masseng-timing-audit-2026-11-24` | `ff84e75` | `STAGING_AUDIT_AND_MASSENG_INVENTORY.md` |
| X1 exposure-matched sequencing + X3 feedback surface | `research/masseng-staging-x1-2026-11-24` | `fef7428` | `RUN_REPORT.md` |
| X2 gate/quota × tutoring inequality + X4 honest-split aggregate test | `research/masseng-staging-x2-2026-11-24` | `f592bae` | `RUN_REPORT.md` |
| X5 Bayesian screen validation + synthetic recovery | `research/masseng-bayes-audit-2026-11-24` | `0ecd4be` | `AUDIT.md` addendum |
| Shadow equations first pass + Bray reality check | `research/shadow-equations-2026-11-25` | `fdc8da0` | `RESULTS_FIRST_PASS.md`, `bray_reality_check*.json` |

### What happened, in plain words

**The staging audit removed the old sequencing claim's support.** The audited staging experiment reproduced exactly (160 runs, N=400, T=70, 10 seeds, 16.5 s), but its arms were not exposure-matched: school-first carried +1.8 more education-share-years and jobs-first +1.2 more vacancy-years; the fiscal loop gave jobs-first a 9.5% higher cumulative education budget; a one-year fiscal lag makes "simultaneous" not simultaneous; quota/ban effects are partly gate arithmetic; completion rankings change across seeds; and migration is not simulated. Time order in that experiment is not causal evidence.

**X1 (the confound fixed): the sequencing falsifier fired.** With cumulative exposure equalised (18.36 education-share-years / 9.44 vacancy-years for every matched arm), the unmatched "school-first beats jobs-first" formal-share gap of −5.4…−4.8 pp (0 positive / 20 negative seeds) **collapses to −0.13…+0.56 pp, i.e. 2–12% of its size**; completion/equity shows no material effect before or after matching (<0.5 pp). A +10-year calendar placebo moves the unmatched contrast to −6.2…−7.6 pp (outside the unmatched CI), so calendar position was also doing work. The pre-declared strict A/≈0 rule is met in only 2/4 conditions (feedback=0), so the label is "inconsistent" by the ≥3/4 rule, reported as such; the pre-declared magnitude criterion confirms the falsifier (88–98% of the gap removed). The model-internal fiscal-timing and tutoring responses are toy dynamics, not sequencing evidence. X1 run 1 was invalid (matched arms not actually exposure-matched), is preserved, and is not interpreted.

**X3 (feedback robustness): no reversals, but no rescue.** 800 runs across job_elasticity {0, .25, .5, .75, 1}; **zero sign reversals**. The sequencing contrast is NULL on 9–11 of 13 metrics; the only robust sequencing difference is the mechanically exposed formal share (−5.4…−4.8 pp), exactly what X1 removes. The both-early-vs-neither contrast is robust on 10–13/13 metrics. The feedback assumption changes magnitudes, not conclusions.

**X2 (gate/tutoring): the falsifier was NOT confirmed — the claim is worse than neutral.** Quota gates raise gate-prep tutoring by +17.6…+21.1 pp overall (+23.8…+28.9 pp at gate-adjacent grades; 3/3 access levels) and **widen the top-vs-bottom tutoring gap by +13.0…+14.5 pp**; the gate-specificity DiD is +9.0…+9.6 pp. The own-teacher ban cuts tutoring −11.0…−22.6 pp. A pre-declared secondary hypothesis was falsified in the opposite direction: raising rural tutoring access did **not** narrow the wealth gap — it widened it (+7.9 pp bar, +9.4 pp quota). Quota vs bar caps completion (lower −11.7…−12.3 pp, upper −13.5…−14.5 pp) and narrows the wealth completion gap. 240 runs, 24.5 s. Toy worlds only.

**X4 (aggregate observed data): FAIL_NO_EVIDENCE.** Honest 40-train/21-validation split, frozen before the run. The model-implied ordering score has point-estimate MAE 8.81 vs persistence 11.30 and pooled trend 9.48, but the paired country-level differences are −2.49 [−5.76, +0.77] and −0.67 [−2.04, +0.66] (90% CIs include 0), and its coefficient is −2.05 [−4.44, +0.87] — not positive. All four robustness specs likewise FAIL_NO_EVIDENCE; no window or split hunting; two code failures are preserved with no results. Binding caveat: the aggregates contain only attainment/enrolment — no child-work, tutoring or learning — a thin observable implication, not the full model.

**X5 (Bayesian screens): not usable as posterior-style inference.** Real-data importance screens have ESS 1.7–2.3% and max weight 2.3–10.6%; a σ-grid moves the weighted means materially (no σ selected), so inference is prior/scale-dominated. Synthetic recovery is **MIXED**: median ESS 12.79%, coverage 91.67%, median error 12.76% of the prior range, but error ≤15% in only 56.25% of cases (<60% criterion) and confusion diagonal 50% (<60%; S3/S4 near non-identified). The true-model ESS improvement says the real-data degeneracy is largely model misspecification/prior conflict, but recovery is only partial: **no real-data posterior or mechanism claims**.

**Shadow equations (first pass + Bray reality check): they do not fit Bray.** The first-pass illustrative model (20k pupils, 10 seeds, 7 scenarios, 1.3 s) gives baseline tutoring participation 36.8%, own-teacher share 20.3%, learning Gini 0.568, admission gap +15.6 pp; a ban cuts participation 15.6 pp and **raises** the learning Gini 9.6 pp; a hard quota flips the admission gap to −29.2 pp but leaves learning Gini unchanged; cash transfers and rural access are weak. Against Bray's six-school targets, rejection ABC **found 0 fits in 200,000 draws** (best max-z 1.168). The provider-share denominator bug was fixed (shares must be among tutored pupils, as Bray reports), giving best max-z 1.14 at 8,000 draws; a 300,000-draw run is in progress on the new server. **The first-pass shadow equations do not reproduce Bray's patterns**; treat the scenarios as illustrative simulation awaiting the literature-fit check.

### What not to believe

- **Not causal, not historical, not a country claim.** X1–X3 and the shadow simulations are stipulated toy worlds; X4 is aggregate-exploratory; X5 is a diagnostic on a screening method. None identifies a mechanism.
- **Do not quote the audited staging experiment's order contrasts as sequencing.** They mix cumulative exposure, the fiscal loop and calendar position; X1 removes most of the apparent effect.
- **Do not quote X1 run 1.** It was not exposure-matched and is preserved as invalid.
- **Do not call the Bayesian importances a posterior.** ESS/max-weight diagnostics fail and synthetic recovery is partial.
- **Do not quote the first-pass shadow scenarios as evidence.** They are illustrative; the Bray check found no fit at 200k draws.
- **Missing channels:** rural migration, urbanisation, remittances, spatial job access and composition change are not simulated. No comparison with E1's 1.8% or observed country history.

### In flight and next moves

1. **region-42 is running a 2M-draw parallel check and a MASSENG coupling run** at write time; nothing is committed. Interpret only after the results are committed with hashes and labels.
2. **Shadow equations:** finish the 300k-draw Bray check; add the separate "other/grade-9" channels flagged by the run; relabel anything that does not survive the literature check.
3. **Staging:** do not revive the old order claim. The fiscal-timing and tutoring responses are model-internal dynamics and need a separate pre-registered test if pursued.
4. **X4:** the aggregate route gives no support at this honest split; the only real upgrade remains DHS individual microdata (application pending).
5. **Housekeeping:** keep SIMULATION / OBSERVED labels attached to every number in this section; T4 off; region-42 is the compute site.


## 14. DHS correction (25 Nov 2026)

**Read before quoting any DHS number.** The first public-API DHS estimates were biased by a fixed-effect parameterisation bug: `scripts/estimate.py` dropped each categorical FE's reference level without an intercept, adding roughly **+0.015–0.019 children** to every FE model (toward zero). Fixed and independently verified (weighted within-transform second implementation; prior within-transform record reproduced); pre-registration/sample/decision rules unchanged. **Old biased numbers remain only at git commit `708e34a` — never quote them.** Bugfix: `BUGFIX_FE_PARAMETERISATION.md`; corrected heads `fe762b9` (dhs-api) and `f4a7f65` (acquisition). All numbers are **OBSERVED / ECOLOGICAL** published DHS cells, not women; no causal claim.

- **Corrected full sample (87 countries), M1:** primary **−0.5541 (0.0588)**, secondary **−1.5837 (0.1667)**, higher **−2.5382 (0.2419)**. **Q2a ratio 1.0029 [0.932, 1.077]**; 2-group ratio 0.9582 [0.915, 0.998] (just excludes 1). **Q2b1 wanted-vs-actual −0.0775 (p=0.0004)** (D4 confirmed). **Cohort 2-group +0.2438 (p=0.016) → D6 now attenuation** (was indeterminate). The individual Recode test remains decisive and is not substituted.
- **African 11-country extension (T1 coverage tier; NOT the pre-registered 14-country main test; D1 not applied):** completed fertility on education, country×survey FE: primary **−0.707**, secondary **−2.163 (0.179)**, higher **−3.198 (0.135)**; **98.6%** of surveys negative, median **−2.00**; window ratio **1.178 [1.027, 1.356]**; cohort **steepening** primary −0.278 (p=0.013), secondary −0.186 (p=0.014) — flagged regional divergence. Source `AFRICA11_EXTENSION.md` @ `fe762b9`.
- **Next action (Trey):** submit the **second (African 11-country) DHS request** with exact title/abstract/country list, **no GPS/HIV ticks**; record both statuses; review window **Wed 25–Fri 27**; if no decision, email **`archive@dhsprogram.com`** on **Mon 30 Nov** with the template; on approval download **Tier 1 (69 IR ZIPs, 493.6 MB)**, record sha256, run pipeline. Asian request pending. **Individual test blocked on approval only** — no ecological/model proxies as substitutes. Record: `research/dhs-acquisition-2026-11-24` @ `f4a7f65`.
