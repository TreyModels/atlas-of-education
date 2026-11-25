# PAPER A — REPRODUCTION ATTEMPT (Phase 2)

**Adjudicator:** `paper-adjudicator` (independent). **Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`.
**Order:** Lead Phase-2 directive — do a genuine reproduction attempt, search everywhere first, run what is computable,
and record exact gaps for what is not. **Do not reconstruct missing artefacts from memory.**

## 0. Bottom line

**Paper A's Exp 1, Exp 3, Exp 4 (Paper A's own model) and Exp 5 are NOT reproducible in this environment.** No
author runner, seed list, raw data or result file exists for any of them in the bundles, archive branch, research
branches, worktrees or pulled directories. The only artefacts are summary numbers inside the author-supplied
`verified_results_2026_11_25.json` (7,224 B), which is a self-report, not a run. **Paper B's 420 design is likewise
not reproducible**; the Paper B **540** design is fully reproduced and is handled in
`docs/audit/PAPER_B_TABLE_REGENERATION.md`.

**What was actually computable was re-executed and confirmed.** The independent ABC identification audit (the
audit's own code, not Paper A's) was re-run by me on the host; its output JSON is **bit-identical** to the committed
host output recorded by `contest-math` (`66bb2648…15808`), and it confirms the numbers my verdict cites. The
bootstrap and DGP audit harnesses were started on the host (see §4); their committed results are unchanged
regardless.

**No value was reconstructed, interpolated or invented.** Where the mathematics cannot be rerun, this document
records a precise **UNRESOLVED verification task** — never an affirmative or negative result.

---

## 1. Rule used: what counts as "reproducible"

A claim is **reproducible** here only if (a) the author's own code and data are present, with a runnable entry point
and seeds, and (b) the run can be executed and compared to the reported numbers. A **reconstruction** — writing a
new runner from the manuscript's prose and running it on the repaired engine — is **not a reproduction** of the
author's run; it is a new experiment. The Lead's instruction forbids reconstructing from memory, and the audit's
own rules (`SCIENTIFIC_CLAIM_LEDGER.md`) require a missing artifact to be recorded as `UNRESOLVED`. This document
therefore **does not** contain a reconstructed Exp 3/Exp 5. It records what exists, what was re-executed, and the
exact gaps.

---

## 2. Search register (every location searched, with method and result)

| # | location | method | result |
|---|---|---|---|
| 1 | `~/neon-boot/pulled/gemini-bundles/` (95 files) | `ls`, `shasum -a 256`, `unzip -l` on every research bundle, `MANIFEST.sha256` | Research bundles found: `ALL_ATLAS_WORK_2026_11_25.zip` sha256 **`f602ede3cb6ef147c9211b56f82b4806d065f5bd15c6d30c7de6ff2dc7814f74`** (12 files — patched engine+runner+540 output, 2 GPU scripts, both `.docx`, `verified_results_2026_11_25.json`); `hk_korea_exact_bundle.zip` **`e9cc02c2…be4e`** (runner `dd0b1d8d…`, `core.py 618bd6dd…`, `tutoring.py b2d213b6…`, patch); `hk_korea_contest_code_bundle.zip` **`da5cd1ee…e47f`** (same + 540 reference `851bb1df…`); `rtx3080ti_gpu_scripts_bundle.zip` **`bb481b87…5550`**. **No Paper A Exp 1/3/4/5 code or result JSON in any bundle.** No 420-era runner. |
| 2 | archive branch `origin/research/atlas-all-work-2026-11-25` @ `46950ab` | `git ls-tree -r --name-only`, grep for `exp1|exp3|exp4|exp5|bulge|identif|bray|jacobian|fee_event|e8|shadow_equation|masseng`; `research/` tree listing | Only the same 12-file all-in-one bundle; no `research/records/2026-11-25-*`; no Paper A experiment code/results. |
| 3 | all `research/*` branches (local + origin), incl. `e6e8-sequencing`, `e8-fisher-ri`, `gender-split-e6e8`, `bulge-arrival`, `shadow-equations*`, `masseng-*`, `gpu-rtx3080ti`, `model-revision` | `git ls-tree -r --name-only` per branch + grep; `git show` of candidate records | E8 empirical records exist (`e8_event_SE.PRM.ENRR_verified8.csv`, Fisher-RI, gender); bulge record exists only as pre-registration + `BULGE_ARRIVAL_STATUS.md` (NOT-ESTIMABLE); shadow-equations branches have no Paper A Exp 4 runner; `model-revision` has the legacy 420-port HK/KR runner + calibration sweep (Paper B-related, not Paper A). **No Paper A Exp1/3/4/5.** |
| 4 | `~/neon-boot/wt2/*`, `~/neon-boot/wt3/*` (incl. `wt3/allwork`, `wt3/shadow`, `wt3/e8`, `wt3/gender`, `wt3/gpu`, `wt3/model`, `wt3/tut`), `~/neon-boot/wt5/*` | `find` by filename pattern; grep for Exp-4 signatures | Only repo snapshots + the all-in-one bundle; no Paper A experiment artefacts. |
| 5 | `~/neon-boot/{paper2,analysis,papers,patched,pulled/eqsuite,pulled/binding-gate,pulled/rtx3080ti,pulled/testbench}` | `find`, `grep -ril` for `spend_feedback|own_premium|grade9_bonus|posterior_corr_cond|masseng-tutoring|bray_abc_7param`, file reads | `paper2/` has `PREREGISTRATION_BULGE_ARRIVAL.md` + `BULGE_ARRIVAL_STATUS.md` (Exp 1 gate failed: `L_primary` 0/8, outcomes absent). `pulled/eqsuite` is a different paper's equation suite (MASSENG; `eq09` DID/IV demo, `eq10` tutoring synthetic), not Paper A's Exp 4. `pulled/binding-gate` is phase-sweep output, not the 1,640 gate matrix. `pulled/rtx3080ti` is the GPU bundle (quarantined). |
| 6 | `~/massification_live` (read-only) | `ls`, `find` | Repo snapshot only; no Paper A experiments. |
| 7 | iCloud Downloads (`~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek`) | filename sweep (`*bulge*`, `*exp1..5*`, `*identif*`, `*bray*`, `*shadow*`, `*contest*`, `*e8*fee*`) | `tutoring_run/tutoring_abm/experiments/exp1_evidence_mc.py`, `exp3_prior_discrimination.py`, `exp4_policy_seed.py`, `exp5_page_ensemble.py` — these are the **tutoring ABM** experiments (different project; no 1,640 gate matrix, no 7,290-obs bulge test, no 10-param Bray Jacobian). `papers/2026-11-21_identification/` — not the Paper A Exp 4 model. No Paper A artefacts. |
| 8 | audit tree `docs/audit/`, `results/audit/`, `docs/audit/harvest/` | `ls`, `grep`, file reads | `harvest/` has the legacy model-revision and GPU records (labelled AUTHOR-REPORTED/PRE-REPAIR); no Paper A Exp runners. `research/records/2026-11-25-masseng-edsystem/` (on the origin audit tip) is a **different** 1,440-run full-system multiverse (`N=400`, `T=70`, 144 equation-choice combos × 10 seeds) — related engine substrate but **not** the 1,640 gate matrix and **not** the fee shock; it cannot substitute. |

**Conclusion of the sweep:** the Paper A Exp 1/3/4/5 code/data are **absent everywhere**. The only Paper A material
in existence is the `.docx` manuscript, the self-reported summary JSON, and the `paper2/` Exp-1 pre-registration
(which records the data gate as failed).

---

## 3. Artefact-by-artefact adjudication of the reproduction attempt

### 3.1 Exp 1 — delayed secondary-bulge `t*` (live-WDI, 7,290 obs, 2,500 permutations)

| item | detail |
|---|---|
| What the paper claims | 7,290 non-null country-year observations; 5 WDI indicators; CS event studies centred on `t* = t_ab + L_primary`; 2,500 Fisher permutations/scheme; honest null (SE.PRM.REPT.ZS T0 = +1.061, p_date = .141, p_country = .279) |
| What code/data is needed | the 5 WDI series (SE.PRM.DURS, SE.PRM.REPT.ZS, SE.SEC.PROG.ZS, SE.SEC.ENRR, SE.SEC.ENRL.TC.ZS) with vintage/hashes; `L_primary` by country-year; the event-study/Fisher runner; the result JSON |
| Where searched | bundles (§2.1), archive branch (§2.2), all research branches (§2.3), worktrees (§2.4), `paper2/` (§2.5), iCloud (§2.7) |
| What was found | `paper2/PREREGISTRATION_BULGE_ARRIVAL.md` + `paper2/BULGE_ARRIVAL_STATUS.md`; committed `e8_primary_ger_panel.csv` (SE.PRM.ENRR only); `wdi_region_map.csv`; `acquire_wdi.py`. **No `L_primary`, no repetition/progression/PTR series, no runner, no result JSON.** |
| Reproducible? | **NO — UNRESOLVED verification task.** The committed bulge record registers `t*` **NOT-ESTIMABLE** (`L_primary` sourced 0/8) and `BULGE_ARRIVAL_STATUS.md` §B records a 2-blocker gate failure (no treatment date; outcome series absent). |
| What would be needed to make it computable | commit a year-varying `L_primary` source (UNESCO/ISCED mapping), at least one repetition and one progression series with annual SSA coverage ~1990–2016, the raw E8 outcome inputs + a download script, the runner, the seed list and the result JSON. This is a **data-acquisition** task plus a small compute task; not runnable now. |
| Note | the self-reported JSON's numbers cannot be checked; a live-WDI pull *could* in principle make `t*` estimable, but the value 7,290 and the p-values remain unverified until deposited. The R²/null conclusion is **not** a result. |

### 3.2 Exp 3 — 1,640-run gate-architecture / H2 experiment

| item | detail |
|---|---|
| What the paper claims | 1,640 matched runs; gate kinds bar, bar_high, quota, contest; S ∈ {.25,.35,.45,.55,.70}; fee ∈ {0,.19}; vac0 ∈ {.02,.08,.25,.50}; 20–25 seeds/cell; `N=400`, `T=70`; H2 = Δcut(S=.25) − Δcut(S=.70) = +0.1086 (contest), −0.0145 (quota) |
| What code/data is needed | the author's gate-matrix runner, the country/household parameterisation (beyond the grid), the pre-registration hash, the seeds, and the result JSON |
| Where searched | as §3.1, plus `pulled/binding-gate` (phase-sweep outputs — different design), `analysis/{phase_sweep_binding,dense_boundary}`, `research/records/2026-11-25-masseng-edsystem` |
| What was found | **Nothing for Exp 3.** The engine has `contest`/`fixed_bar`/`quota`/`open` gate kinds after the Gate-1 repair and `GATE_SPECS`, but there is **no SSA `countries/` config** in the engine (`engine/countries/` = cambodia, china, philippines only), and no Exp-3 runner/seed list/result. The `masseng-edsystem` 1,440-run multiverse is a different experiment (equation-choice grid, 144×10 runs, no S×fee×vac0 matrix, no H2 estimator). |
| Reproducible? | **NO — UNRESOLVED verification task.** The self-reported JSON's `base_commit 68da16e` did not contain a runnable `contest` gate (RECONCILIATION; MISSING_ARTIFACTS), so its provenance is internally inconsistent even before the missing files. |
| Could it be reconstructed? | Only by **inventing** the SSA/household parameterisation not stated in the manuscript. That is a new experiment, not a reproduction, and is prohibited here. If the operator wants the repaired-engine H2 test, it must be commissioned explicitly as a **new pre-registered experiment** with a frozen config; cost ≈ 2× the 540 per-run (N=400/T=70) ⇒ ~14–30 CPU-h for 1,640 runs. |

### 3.3 Exp 4 — tutoring identifiability / Jacobian ("theorem")

| item | detail |
|---|---|
| What the paper claims | `masseng-tutoring` 3-option MNL; 10-parameter calibration against Bray's 7 aggregate targets; 3 exact collinearities; 7-parameter bijection; 5-parameter core; Jacobian ranks 5/10 → 5/7 → 5/5, 6/7, 7/7; condition numbers 3.48e12 / 1.09e13 / 14.41 / 3435.49 / 43.81; acceptance 0.0063 %→0.0192 %; 100 fresh seeds 1000–1099; posterior corr cond 447.16→23.97→8.05 |
| What code/data is needed | the `masseng-tutoring` module patch, the 10-parameter model specification, the Bray target vector, the ABC/rank runner, the seed list, the result JSON |
| Where searched | bundles, archive, all research branches (incl. all `shadow-equations*` branches), worktrees, `pulled/eqsuite`, iCloud `papers/2026-11-21_identification` |
| What was found | **No Paper A Exp-4 code/spec/result.** The `shadow-equations` branches exist but carry no 10-param MNL Jacobian runner. `pulled/eqsuite` is a different paper's synthetic equation suite (`eq09` DID/IV demo, `eq10` tutoring demand/production; `bray_targets.json` is a literature reality check with different target values 0.819/0.747/0.898/0.026/0.577/0.409/0.54). The **only** independent identifiability computation is the audit's ABC audit on the **GPU bundle's frozen 6-active-parameter design**, which is **not Paper A's 10-parameter masseng model**. |
| Reproducible? | **Paper A's Exp 4: NO — UNRESOLVED verification task.** Its own Jacobian must be computed from its own model; that model is not deposited. |
| What WAS computable | the independent ABC audit — **re-executed by me** (§4.1) and bit-identical to the committed host output. It confirms: the advertised 5-moment Jacobian has rank **4/5** at 1,000/1,000 prior-box points; **2-dimensional null space**; δ = **−0.7537718023763802** analytic; cell targets 0.823333/0.516667/0.85; reduced 3-moment/5-parameter rank **3** (null dim 2); one income + one within-grade quality moment → **local rank 5/5** (6/6 unsubstituted). This **contradicts the cited evidence base** but cannot verify Paper A's own 7/7 claim. |
| Independent target-algebra check (my computation) | The paper's "two algebraic identities" (participation = weighted avg of G9/G12; other = 1 − own) reduce 7 targets to at most **5** independent moments — consistent with the paper's count *if the identities hold exactly*. But the literature target values in `paper2`-era `bray_targets.json` **violate both identities**: participation − (⅔·G9 + ⅓·G12) = **+0.0217**, own + other − 1 = **−0.0140**. The archived ABC design's targets satisfy the participation identity exactly (residual 0.0) but that reduces the 5 advertised moments to **4** independent, not 5. So the paper's "five independent aggregate moments" is a **definitional count on a different (idealised) target set**, not a property established from its own quoted targets. |

### 3.4 Exp 5 — E8 fee-abolition shock / forecast

| item | detail |
|---|---|
| What the paper claims | `fee_public = .150` calibrated to pre-abolition GER 74.88 % (10 seeds), zero post fitting; 40 paired seeds; 7 horizons; three gate regimes (open_bar bars [3.0,5.5,8.0,11.5]; tight_sec_quota G6 S=.55, G9 S=.45; mv_quota); RMSE 5.13/4.68 vs persistence 23.93; on-impact +11.60/+13.48 |
| What code/data is needed | the SSA country/engine config, the calibrated run script, the seed pairs, the raw output JSON, and the E8 panel |
| Where searched | as above; plus `results/audit/`, `engine/`, `experiments/` |
| What was found | **No Exp-5 runner or output.** The E8 empirical panel is committed (`e8_primary_ger_panel.csv`, SE.PRM.ENRR) but the Exp-5 simulator needs the other indicators only for the empirical comparison; the engine has no SSA config and the fee calibration is not in any committed script. The 74.88 % figure appears only in the self-reported JSON. |
| Reproducible? | **NO — UNRESOLVED verification task.** Reconstructing it would require inventing the SSA parameterisation and the gate/cohort config; not a reproduction. |
| What is verifiable | the **empirical** column of Table 1 (E8 ATTs) is verified against the committed record (see `PAPER_A_VERIFICATION.md` A-01/A-02). The **simulation** column is author-reported and cannot be tested. |

### 3.5 Paper B — the 420 design

| item | detail |
|---|---|
| What is needed | the 420-era runner (`Engine(cfg, modules=…)`/`e.history` API), the 14-arm config, the 30-seed list, the raw output |
| Where searched | bundles, archive, all research branches, worktrees; legacy `model-revision` branch |
| What was found | only the **summary numbers** in `verified_results_2026_11_25.json`; no runner, no raw output. The legacy `model-revision` branch has a **different** 420-port runner (`run_hk_korea_canonical.py`, V1/V2/V3 variants) whose calibration **failed** (untuned 66.27 %/80.77 pp/5.32×; best grid 91.63 %/37.11 pp/1.59× vs 76.5/32.1/3.4) — it is not the docx's generator and cannot reproduce its numbers. |
| Reproducible? | **420 design: NO — AUTHOR-REPORTED/UNRESOLVED.** The **540 design IS reproducible** and is regenerated in `PAPER_B_TABLE_REGENERATION.md`. |
| Note | this is exactly the Lead/Commander correction: Paper B's 540 scripts/data are in hand and reproduced; only the 420-generation design and Paper A Exp1/3/4/5 are genuinely missing. |

---

## 4. What was re-executed (and what it shows)

### 4.1 ABC identification audit — **COMPLETED, independent re-execution**

```bash
cd /Users/treymenefee/neon-boot/wt4/auditv2
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/abc_identification_audit.py
```
Output `/tmp/abc_identification.json`, sha256 **`66bb2648e8957ced627972219e3ae4f6dc54f797988651be921bc07210215808`** —
**identical to the committed host JSON hash recorded in `ABC_IDENTIFICATION_AUDIT.md` §6** (`66bb2648…15808`);
tables sha256 `06f31983…9a23`. Exit 0. The re-execution reproduces:

| quantity | value |
|---|---|
| 5-moment × 6-parameter Jacobian rank | **4** at 1,000/1,000 prior-box points |
| 6 active parameters − rank | **2-dimensional null space** |
| analytic provider-choice δ | **−0.7537718023763802** (own share 0.68 exact) |
| implied cell means (A urban G9, B rural G9, C rural G12) | 0.823333, 0.516667, 0.850000 |
| reduced 3-moment × 5-parameter cell Jacobian | rank **3**, null dim **2** |
| one income + one within-grade quality micro-moment | **local rank 5/5** (6/6 unsubstituted) — local only |

This is a **re-execution of the audit's own deterministic harness**, not a reproduction of Paper A's Exp 4. It
confirms the evidence my verdict uses; it does **not** verify Paper A's own rank 5/7→7/7 numbers (whose model is
absent).

### 4.2 Bootstrap size/power + invalid permutation — re-execution started

```bash
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/bootstrap_factorial.py \
  --out /tmp/adjud/repro --workers 3 --n-datasets 2000 --seed 20261125
```
Status at the time of writing: **running on the host** (host load average >20 from other lanes; the box run of the
same harness took 70.2 s). The committed record (`BOOTSTRAP_REPORT.md`, `results/audit/boostrap_factorial_summary.json`)
is unchanged; my re-execution is an independence check only. Expected reproductions: pooled size 0.996–1.000 under
the zero-effect null, country-FE size 0.052–0.062, permutation within-invariance 6.66e-16, replacement WCR
0.025–0.042, cluster bootstrap 0.033–0.050 (coverage 0.95–0.97). If it does not finish on the host, the committed
result stands and is labelled as the audit's, not mine.

### 4.3 Corrected synthetic DGP — re-execution started

```bash
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/dgp_validation.py \
  --out-dir /tmp/adjud/repro/dgp --workers 3 --n-pop 100 --n-draws 20000 --seed 20261125
```
Status: **running on the host** (the box run was 464 s with 3 workers; host load makes this slower). Committed
record (`results/audit/dgp_validation_summary.json`, parquets) is unchanged. Expected: corrected crossed design
rank **5/5** in 400/400 crossed populations, legacy **3/5**, recovery RMSE 0.04–0.13 vs legacy 0.58–0.64.

### 4.4 Paper B table regeneration — **COMPLETED** (host)

All Paper B HK/Korea-dependent tables were regenerated from the repaired 540 (`455649da…`); see
`docs/audit/PAPER_B_TABLE_REGENERATION.md` and `results/audit/paper_b_540_regenerated_tables.csv`
(sha256 `da40a2ee…c5c1`). This is the only **genuine reproduction** work in Phase 2: the 540 scripts/data exist and
were reproduced in Gate 0/Gate 1.

---

## 5. Paper-number vs recomputed-number

| paper number | recomputed / verified? | verdict |
|---|---|---|
| E8 ATT +12.44 / +25.26 / event path / RI p / gender D (Paper A empirics) | **yes** — against committed records (`bd782be`, `fb8b67e`, `b4eb680`), reproduction gates passed | **MATCH** (see `PAPER_A_VERIFICATION.md`) |
| Exp 1: 7,290 obs, 2,500 perms, T0 = +1.061, p = .141/.279 | no — no series/runner/result; `t*` NOT-ESTIMABLE in committed record | **NOT RECOMPUTABLE** |
| Exp 3: 1,640 runs; H2 +0.1086 / −0.0145; H1 +0.3430 | no — no runner/config/pre-registration/result; declared base commit lacked the contest gate | **NOT RECOMPUTABLE** |
| Exp 4: ranks 5/7, 6/7, 7/7; cond 1.09e13/3435/43.81; acceptance 0.0063→0.0192 % | no — no Paper A model/code/result. The **affiliated archived design** recomputes to **rank 4/5, 2-dim null, local 5/5 after two moments** | **NOT RECOMPUTABLE (Paper A)**; **MISMATCH (affiliated evidence)** |
| Exp 5: RMSE 5.13/4.68 vs 23.93; impact +11.60/+13.48; 74.88 % calibration | no — no runner/config/seeds/raw output | **NOT RECOMPUTABLE** |
| Paper B 420 tables | no — no runner/raw output; docx == self-reported JSON | **NOT RECOMPUTABLE (AUTHOR-REPORTED)** |
| Paper B 540 tables | yes — reproduced 540 (`455649da…`); pre-repair (`722c370b…`) | **RECOMPUTED; tables regenerated** |
| GPU/ABC 7-param calibration, 100 % paradox, E1/Q3 selftest | audit harnesses exist and re-execute (ABC done); results contradict the claims | **MISMATCH — CONTRADICTED** |

---

## 6. Exact gap list (UNRESOLVED verification tasks — not results)

| # | missing file/artefact | expected content | needed access / action | blocks |
|---|---|---|---|---|
| 1 | `results/exp1_bulge_arrival_summary.json` (author runner absent too) | per-indicator CS event estimates on `t*`, Fisher-RI p-values, 2,500 permutations/scheme, 7,290-obs sample | author deposit; plus a year-varying `L_primary` source and repetition/progression series | Exp 1 (A-07, A-08) |
| 2 | `results/exp3_contest_h1_h2_summary.json` + the gate-matrix runner + seed list + pre-registration hash | 1,640-run results, H1/H2 cells, contest/quota comparison | author deposit; declare the **patched** engine commit (not `68da16e`) | Exp 3 (A-09…A-12) |
| 3 | Paper A Exp-4 `masseng-tutoring` model spec + rank/ABC runner + seeds + result JSON | 10-parameter model, 7 Bray targets, Jacobian ranks/conditions, 100-seed stability | author deposit (shadow-equations branch is quarantined; no runner found) | Exp 4 (A-13…A-19) |
| 4 | Paper A Exp-5 fee-shock runner + SSA engine config + seed pairs + raw output | 40 paired seeds, 3 gate regimes, 7-horizon RMSE | author deposit; the SSA country config does not exist in the engine | Exp 5 (A-21…A-25) |
| 5 | Paper B 420-era runner + config + raw output | 14 arms × 30 seeds, `N=400`, `T=70`; exact `Engine(cfg, modules=…)` API generation | author deposit; the legacy `model-revision` 420-port is a different run | Paper B Tables 2–4 / Figs 1–4 (B-01…B-13) |
| 6 | E8 raw outcome inputs / `download_data.sh` | the WDI zips and a download script (the record's `REPORT.md` cites a `scripts/download_data.sh` that does not exist at `bd782be`) | author/data deposit | full E8 reproduction (note: the committed CS/RI/gender outputs and their gate already reproduce the **numbers**) |
| 7 | Paper B "published benchmark" sources | primary KEDI 2024/2025 and HK 2011/12 surveys with population/denominator | operator/source supply (G2-A gate: **all four moments DROPPED/UNRESOLVED**; `G2A_CITATION_VERIFICATION.md`) | any calibration (B-05…B-10) |

**Nothing in this list was reconstructed.** Each row is a concrete, bounded task with an owner/action; none is an
affirmative or negative scientific result.

---

## 7. What this means for the verdict

* The **verdict stands**: Paper A's E8 empirical block is VERIFIED EMPIRICAL; its simulation/identifiability claims
  are `UNRESOLVED` (no artifact) or `CONTRADICTED` where the affiliated archived evidence is independently
  recomputed (rank 4/5, 2-dim null, local 5/5).
* The **reproduction attempt did not rescue any Paper A claim**; it confirmed that the strongest independent
  computation available (the ABC audit) contradicts the paper's cited evidence base, and that everything else is
  missing.
* **Paper B's 540 is the only fully reproducible simulation in the programme**, and its tables have been
  regenerated (`PAPER_B_TABLE_REGENERATION.md`). Its 420 tables remain AUTHOR-REPORTED.
* A **box campaign cannot fix the Paper A gap** — there is nothing to run. The blocker is authorship/data deposit,
  not compute. Any "reconstruction" on the repaired engine would be a **new experiment** and must be commissioned
  and pre-registered as such (estimated cost: Exp 3 ≈ 14–30 CPU-h; Exp 5 ≈ 1–3 CPU-h; both at `N≈400`, `T≈70`).
