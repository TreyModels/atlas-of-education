# SCIENTIFIC CLAIM LEDGER — GPU bundle + Paper A/B (P0-07)

**Programme:** Atlas contest audit v2 · **Task:** `task-11` (P0-07 execution half) · **Owner:** `audit-runner`
**Date:** 2026-11-25 · **Audit branch:** `research/contest-audit-v2-2026-11-25`
**Companion machine-readable record:** [`CORRECTED_GPU_EXPERIMENT_MANIFEST.json`](CORRECTED_GPU_EXPERIMENT_MANIFEST.json)
**Audit authority:** [`EXTERNAL_AUDIT_GPU_2026-11-25.md`](EXTERNAL_AUDIT_GPU_2026-11-25.md) — **GPU-bundle scientific
conclusions are QUARANTINED**. P0-07 list is binding.

## Rules used in this ledger

1. **Every claim below has exactly one status** from the programme taxonomy:
   `VERIFIED EMPIRICAL` · `REPRODUCED SIMULATION` · `VALIDATED SIMULATION` · `AUTHOR-REPORTED` · `CONTRADICTED` ·
   `UNRESOLVED` (see `LEAD_GROUND_TRUTH.md` §6).
2. **Arithmetic validation ≠ scientific validation.** GPU-vs-CPU float64 agreement (8.88e-15) validates
   **arithmetic only**; it does **not** promote any scientific claim to `VALIDATED`.
3. A claim backed only by an artifact that this audit did **not** execute or independently re-derive is at best
   `AUTHOR-REPORTED`; if the artifact is missing it is `UNRESOLVED`; if verified code/algebra contradicts it, it is
   `CONTRADICTED`.
4. **No GPU-bundle output may be cited** as a calibration, a contest boundary map, or an E1/Q3 reconstruction
   (external audit §2). The entries below exist so the quarantine is explicit and per-claim, not a blanket.
5. Bundle integrity (separate from scientific claims): canonical `MANIFEST.sha256` **12/12 entries OK** on host
   (`shasum -a 256 -c`) and box (`sha256sum -c`); bundle directory digest
   `8d58e6ff…f3cfbf` unchanged before/after every harness run. That is an **integrity fact**, not a scientific
   claim (recorded in the manifest deliverable).

---

## A. GPU bundle claims (`docs/audit/gpu_abc_bundle/` @ `045a63e`)

| ID | claim | artifact(s) | status | basis |
|---|---|---|---|---|
| G-01 | The 7-coordinate Bray ABC is a **7-parameter calibration** | `gpu_bray_abc_and_contest_surface.py`; `results_bray_abc_7param.json` | **CONTRADICTED** | `θ5` (teacher_threshold) never enters utilities or moments; not identifiable (external audit P0-01/P0-02; P0-07 defect list) |
| G-02 | The ABC has **5 independent moments** (or "5 moments vs 6 parameters" is tight) | same script L52, L82-90; `results_bray_abc_7param.json` | **CONTRADICTED** | overall participation ≡ ⅔·G9 + ⅓·G12 (420 G9 / 210 G12), and the targets satisfy it exactly (0.73 = ⅔·0.67+⅓·0.85) ⇒ **4 independent moments** (audit P0-01) |
| G-03 | The **posterior correlation condition number** (25.96 → 21.03) measures/improves identification | `results_bray_abc_7param.json` (`posterior_corr_cond_6active`); `results_bray_abc_6param.json` | **CONTRADICTED** | it is the eigenvalue ratio of the accepted-draw correlation matrix, not the moment-Jacobian; must not be cited as identification evidence (audit P0-01) |
| G-04 | The ABC identifies the provider-choice parameter (archived δ = −0.8241 7-param; −0.6682 6-param against own-share target 0.68) | `results_bray_abc_7param.json`; `results_bray_abc_6param.json` | **CONTRADICTED** | δ is analytic: `P(own|tutoring)=1/(1+e^δ)` ⇒ δ = ln(0.32/0.68) = **−0.7537718** exactly; the archived estimates imply 69.51 % / 66.11 % own share, both off the exact target (audit P0-02) |
| G-05 | The ABC posterior is a credible calibration rather than a prior-bounded accepted region | `results_bray_abc_7param.json`; `results_bray_abc_6param.json` | **CONTRADICTED** | 6 active parameters vs 4 independent moments ⇒ ≥2 locally unidentified directions; the uniform priors do the identifying (audit P0-01/P0-02) |
| G-06 | The ABC fits **7 benchmark moments** (`other_share`, `teacher_tut` included) | `gpu_bray_abc_and_contest_surface.py` docstring L39-41 vs code L52, L82-90 | **CONTRADICTED** | only 5 moments are computed; `other_share` and `teacher_tut` are never computed |
| G-07 | The synthetic population supports urban/rural and school-level claims | `gpu_bray_abc_and_contest_surface_6param.py` L50-54 | **CONTRADICTED** | population is degenerate: every G12 pupil is rural (zero urban G12), no school identifiers; `school_gap ~ U(0,1)` per pupil (audit P0-03) |
| G-08 | Accepted draws are retained for posterior/predictive diagnostics | `gpu_bray_abc_and_contest_surface.py` L103-120 | **CONTRADICTED** | accepted draws are discarded; only aggregates returned (audit P0-07) |
| G-09 | A **“100-Fresh-Seed Stability Bank”** was run | script docstring L4-8 | **CONTRADICTED** | advertised but not implemented anywhere; no output artifact (audit P0-07) |
| G-10 | The 2,000-point contest surface maps the exact H2 boundary / the engine's contest mechanism | `results_bray_abc_{7,6}param.json` `part_b_*`; script L124-174 | **CONTRADICTED** | approximate symmetric Tullock fixed point, not the engine's Gumbel-max Plackett–Luce gate (audit P0-06; bundle README §3) |
| G-11 | The **seat-expansion “paradox”** (`dSpend/dS > 0`; share of cells = **1.0**) is a model result | `results_bray_abc_{7,6}param.json` (`share_cells_paradox_*=1.0`) | **CONTRADICTED** | solver is the **r = 1** first-order condition with r inserted as a multiplier (`e = sqrt(r·ΔV·A·y/p) − A − x0`), so r rescales incentives rather than the discrimination exponent; no capacity clearing / convergence diagnostics; seat shares stop at 50 %. **Toy-model result, quarantined** (audit P0-06) |
| G-12 | The E1/Q3 selftest demonstrates **minority-effect leakage** | `results_e1_q3_selftest.json`; `gpu_e1_q3_wild_cluster_ri.py` L172-185 | **CONTRADICTED** | DGP puts the country effect in both regressor and outcome; pooled regression has omitted-variable bias; auditor negative control (true effect 0) found β=0.3054, t=4.975, p=0.0005 (audit P0-04) |
| G-13 | Wild-cluster bootstrap p-values provide valid inference for the published E1/Q3 estimators | `results_e1_q3_selftest.json`; `results_gpu_vs_cpu_diff.json` | **CONTRADICTED** | selftest p-values sit at the 1/(B+1) resolution floors (0.00049975, 0.000999) on a confounded DGP; the selftest is GPU-numerics validation only (audit P0-04) |
| G-14 | The country-block permutation tests the within-country (FE) estimand | `gpu_e1_q3_wild_cluster_ri.py` L144-160; `results_e1_q3_selftest.json` `block_perm` | **CONTRADICTED** | `x*_it − x̄*_i ≡ x_it − x̄_i` for every permutation ⇒ the within regressor is invariant; adding FE cannot repair it (audit P0-05) |
| G-15 | The bundle is an **E1/Q3 reconstruction** | `gpu_e1_q3_wild_cluster_ri.py` panel mode; `RUN_REPORT.md` | **UNRESOLVED** | panel CSV missing (panel mode never run); even with a CSV, `X=[1,x]` drops controls/FE, so it is not the estimator |
| G-16 | GPU and CPU agree numerically on the selftest | `results_gpu_vs_cpu_diff.json` | **VALIDATED SIMULATION** *(arithmetic only)* | deterministic quantities max abs diff 8.88e-15; p-values identical; RNG-dependent bootstrap moments differ by design (scope-limited: no scientific claim validated) |
| G-17 | Reported pooled regression values (β = 0.4447407388610457, SE = 0.08291358451449403, t = 5.363906788800103) | `results_e1_q3_selftest.json` | **AUTHOR-REPORTED** | consistent with committed code and independently reproduced arithmetically by the external auditor; **inference** from these numbers is invalidated separately (G-12/G-13) |
| G-18 | Environment: torch 2.7.1+cu118, CUDA 11.8, RTX 3080 Ti 12 GB, 152-package env lock | `env_lock_rtx3080ti.txt`; `RUN_REPORT.md` | **AUTHOR-REPORTED** | environment lock deposited; not re-verified in this audit (no GPU campaign; torch parked) |
| G-19 | The archived runner executed all jobs successfully (`EXIT 0` per job, `DONE`) | `run_gpu_jobs.sh`; `RUN_REPORT.md` | **AUTHOR-REPORTED** | P0-07: the archived runner cannot detect failure (rc only echoed), so its `DONE` is not evidence of success. Corrected harness proof: archived pattern exits 0 with a failing job; corrected harness exits 7 (see `fixed_harness/evidence/`) |
| G-20 | The GPU bundle's ABC/contest/E1-Q3 outputs are citable scientific evidence | this bundle (all outputs) | **UNRESOLVED** | quarantined by external audit §2 until P0-01…P0-07 corrections are implemented and the corrected experiments are re-run; no GPU campaign authorised |

**GPU ledger summary:** 0 `VERIFIED EMPIRICAL`, 0 `REPRODUCED SIMULATION`, 1 `VALIDATED SIMULATION` (arithmetic
scope only: G-16), 3 `AUTHOR-REPORTED` (G-17…G-19), **14 `CONTRADICTED`** (G-01…G-14), 2 `UNRESOLVED` (G-15, G-20).
The only thing that survives without caveat is **arithmetic agreement**, and even that validates no claim.

---

## B. Paper A headline claims (`papers/shadow-education-contest/paper_a_general_mechanism/`)

| ID | claim | artifact(s) | status | basis |
|---|---|---|---|---|
| A-01 | Empirical E8 effect: abolition-year GER jump **+12.44 pp** (committed 12.4436), mean post-abolition **+25.26 pp** (25.2607), event range **+22.12…+28.56 pp** | `When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`; `RECONCILIATION.md` (committed E8 record `bd782be`) | **AUTHOR-REPORTED** | manuscript cites a committed E8 record on another branch; not re-derived in this audit. Internal consistency checked in `RECONCILIATION.md` |
| A-02 | **Exp 1** live-WDI `t*` bulge-arrival test: 7,290 observations, 2,500 Fisher permutations, honest null | manuscript; `MISSING_ARTIFACTS.md` | **UNRESOLVED** | no series/code/result JSON committed; the in-repo bulge record says `t*` **NOT-ESTIMABLE** (`L_primary` sourced 0/8). Cannot be cited until the series + hashes are committed |
| A-03 | **Exp 3** Tullock `contest` gate: 1,640 matched runs, H2 fee×scarcity `+0.1086` (p = 1.9e-11), H1 `+0.3430` (Spearman −1.00) | manuscript; `MISSING_ARTIFACTS.md` | **UNRESOLVED** | no runner/results/seeds committed; the committed base engine has no `contest` gate (dispatch is bar/quota only), and the reproduction record notes the patch lineage separately |
| A-04 | **Exp 4** identifiability: rank 5/7 (cond 1.09e13) → 7/7 (43.81) via micro-moments | manuscript; `MISSING_ARTIFACTS.md` | **UNRESOLVED** | no committed code/results; the shadow-equations record is quarantined. External audit P0-01/P0-02 require the rank to be **recomputed** — the GPU bundle cannot support this theorem |
| A-05 | **Exp 5** E8 out-of-sample shock: 7-horizon RMSE 5.13/4.68 pp vs persistence 23.93 pp; calibrated to 74.88 % pre-abolition GER; predicted on-impact +11.60/+13.48 pp | manuscript; `MISSING_ARTIFACTS.md` | **AUTHOR-REPORTED** | simulation code/results not supplied; empirical +12.44 is the committed E8 value (A-01). Draft numbers, not reproduced |
| A-06 | Paper A's **Jacobian / micro-identifiability theorem** (7-moment identification claim) | manuscript; GPU ABC bundle (declared evidence) | **UNRESOLVED** | external audit §2: the existing GPU ABC outputs must **not** be used to support the manuscript's Jacobian theorem; the claim requires an independent rank audit (`ABC_IDENTIFICATION_AUDIT.md`, contest-math) |

**Paper A ledger summary:** 0 `VERIFIED EMPIRICAL`, 0 `REPRODUCED SIMULATION`, 0 `VALIDATED SIMULATION`,
2 `AUTHOR-REPORTED`, 0 `CONTRADICTED`, 4 `UNRESOLVED`. Paper A remains a **draft**: its empirical E8 block is
author-reported-consistent with a committed record; its four simulation/identification claims are unresolved.

---

## C. Paper B headline claims (`papers/shadow-education-contest/paper_b_hk_korea/`)

| ID | claim | artifact(s) | status | basis |
|---|---|---|---|---|
| B-01 | **420-run calibration** (HK G9 53.8 %; HK G12 71.6 % vs 71.8 %; KR K–12 76.5 %; KR Q5−Q1 gap 34.1 pp vs 32.1; KR Q5/Q1 spend 3.19× vs 3.4×) | `Shadow_Education_Arms_Race_HK_Korea_APA.docx`; `results/verified_results_2026_11_25.json` (`paperB_hk_korea_comparative`) | **AUTHOR-REPORTED** | 14-arm / 420-run / N=400 / T=70 design; no runnable 420-era runner was supplied, so the table is not reproduced (this audit reproduced the **540**-run generation only) |
| B-02 | **420-run counterfactual table** (baseline/CF1a/CF1b/CF2a/CF2b/CF3a/CF3b spend + elite Q5 shares) | same docx + 420 record | **AUTHOR-REPORTED** | author-reported generation; differs from the reproduced 540 design (e.g. HK baseline elite Q5 30.0 % vs 46.36 %). Not reproduced |
| B-03 | Paper's reading: “only **wage compression paired with effort caps/seat expansion** reaches the win-win frontier” | docx; `NEXT_EXPERIMENTS.md` (Exp 7 criterion) | **CONTRADICTED** | reproduced 540 run: **CF4a fails HK equity** (48.64 % > 46.36 %), **CF4b fails spend in both** (90.88 / 88.04 ≥ 80); the only passing arm is single-lever **CF1b**. Pre-stated falsifier not met |
| B-04 | Tax +50 % raises total spend and top-quintile elite capture | docx; 420 record; 540 reproduction | **REPRODUCED SIMULATION** | direction holds in the reproduced 540 run (HK spend 107.42, elite Q5 52.43 %; KR 106.46, 41.75 % vs baselines 46.36/36.12 %). Magnitudes are generation-specific |
| B-05 | Elite-seat expansion raises Grade-12 participation and spend (the 2024 Korean medical-seat shock reading) | docx; 420 record; 540 reproduction | **REPRODUCED SIMULATION** *(direction only)* | 540 run: CF2b spend 149.30 HK / 128.00 KR (both ↑), G12 **85.65 % / 95.58 %** (baselines 72.37 / 73.69 %). The §6 manuscript episode (proposed 2,000 → finalized ~1,500 seats; KRW 29.2 tn 2024 / ~27.5 tn 2025) stays **AUTHOR-REPORTED** empirical context with its own limitations |
| B-06 | The **540-run bundle job** reproduces the supplied reference and is the canonical simulation evidence | `code/REPRODUCTION_CF4_2026-11-25.md`; `GATE0_REPORT.md`; `results/audit/*` | **REPRODUCED SIMULATION** | Gate 0: host output bit-identical to the committed 540 JSON modulo `elapsed_seconds`; box (numpy 1.24.1) matches reference to ≤7.1e-15; every 2-d.p. figure identical; independent worker-count invariance |
| B-07 | 540-run headline numbers: HK/KR baseline elite Q5 **46.36 % / 36.12 %**; CF4a HK 48.64 %; CF4b spend 90.88/88.04; CF1b 67.39/41.96 % and 76.42/26.39 % | `results/hk_korea_comparative_with_cf4.json`; `GATE0_REPORT.md` | **REPRODUCED SIMULATION** | reproduced from the exact committed engine+runner (Gate 0; this audit reran the harness integrity) |
| B-08 | The **540 design is calibrated** (recovers the Korean benchmarks) | `REVIEW_RESPONSE_2026-11-25.md` §4; reproduced 540 baseline | **CONTRADICTED** | 540 baseline Q5−Q1 participation gap 68.36 pp vs 32.1 target; Q5/Q1 spend ratio 18.01× vs 3.4× target; K–12 participation field differs from the 76.5 % benchmark |
| B-09 | Four embedded charts match the handoff numbers | `paper_b_hk_korea/figures/fig1…fig4.png` | **AUTHOR-REPORTED** | extracted and visually checked, not regenerated from a reproduced generation |
| B-10 | Cited empirical benchmarks: HK Grade 9 **53.8 %** / Grade 12 **71.8 %** (2011/12 survey); Korea private-education participation **80.0 % (2024)** / **75.7 % (2025)** — used as calibration targets | docx; `README.md`; programme benchmark list | **AUTHOR-REPORTED** | citations exist in the programme record; population/survey-year/denominator must accompany every use; not re-derived from raw survey microdata in this audit |

**Paper B ledger summary:** 0 `VERIFIED EMPIRICAL`, **4 `REPRODUCED SIMULATION`** (B-04, B-05, B-06, B-07),
**4 `AUTHOR-REPORTED`** (B-01, B-02, B-09, B-10), **2 `CONTRADICTED`** (B-03, B-08), 0 `UNRESOLVED`.
The reproduced result is the **540**-run generation; the manuscript tables are the **420**-run generation and are
not reproduced. (B-05's empirical Korean seat-expansion episode remains AUTHOR-REPORTED context inside that row.)

---

## D. What must not be cited (explicit quarantine, after this ledger)

1. **No GPU-bundle output** may be cited as a calibration, a 7-parameter identification, a contest boundary map, an
   E1/Q3 reconstruction, or evidence for a “100 % seat-expansion paradox”. (G-01…G-14, G-20)
2. **Paper A's** Exp 1/3/4/5 and the Jacobian theorem remain unresolved; the GPU ABC bundle **cannot** support the
   Jacobian theorem. (A-02…A-06)
3. **Paper B's** 420-run tables and the “wage-compression win-win” reading are not reproduced; the win-win reading
   is **contradicted** by the reproduced 540-run evaluation. (B-01…B-03)
4. **GPU-vs-CPU agreement is arithmetic validation only** and must never be quoted as scientific validation. (G-16)
5. The corrected harness demonstrates **execution integrity**; it does **not** by itself validate any experiment.
   The real-mode matrix is defined but was **not executed** (CPU-only audit; torch parked; no GPU campaign).

---

## P0 ANNEX — Commander record of task-6 / task-9 / task-12 / task-7 / task-8 outcomes

**Appended by `atlas-commander` 2026-11-25 ~16:00 (Lead-directed). The ledger body above is audit-runner's task-11
record; this annex adds the later P0 findings. All GPU conclusions remain QUARANTINED; nothing here is a Gate-1
result or an empirical claim.**

| # | claim previously in play | status now | exact artifact / evidence |
|---|---|---|---|
| A1 | "7-parameter ABC is identifiable / 5 moments pin 6 active params" | **CONTRADICTED** (already listed; confirmed quantitatively) | task-6 `79bc919` / `ABC_IDENTIFICATION_AUDIT.md`: 5 advertised moments **rank 4/5** at 1000/1000 prior-box points; 6 active params ⇒ 2-dim null space; **44 distinct θ** inside the prior reproduce the same 5 moments (null motion |Δθ|=0.266, residual 1e-16); analytic Jacobian vs FD 4.3e-6; δ = −0.7537718023763802 exact |
| A2 | "Archived 7/6-param ABC deltas validate the model" | **UNVALIDATED/INSIDE-TOLERANCE ONLY** | task-6: archived deltas 69.51 %/66.11 % inside the 6 pp own-tolerance, i.e. the tolerance masked an exactly solvable parameter; reduced 5-param/3-moment rank 3 ⇒ exactly two further independent moments required |
| A3 | "Paper A micro-moments are identified" | **LOCAL ONLY** (not global) | task-6: rank 5/5 substituted, 6/6 unsubstituted local; Paper A's Jacobian must be independently computed; must NOT cite archived ABC outputs |
| A4 | "Urban–rural participation gap is 0.14" | **COMPOSITION ARTEFACT** | task-6: empty G12×urban cell implies a 30.7 pp within-grade G9 gap (A−B) behind the 0.14 aggregate |
| A5 | "100 % seat-expansion paradox" | **CONTRADICTED** | task-9 `66abc13`/`0f56621`: archived S-grid truncated at 0.50 (rising arm only); corrected 72-cell exact-PL surface is an **inverted-U ending at 0** at universal admission (positive-gradient share falls to 52 % as S→1) |
| A6 | "Tullock structural map = 3-D surface" | **CONTRADICTED** | task-9: archived solver depends only on r·ΔV/p ((0.8,0.10) and (1.6,0.20) give identical effort, |diff|=0); the 20×20 (r,p) grid is a 1-D r/p sweep × S (rank 2); core/context for A4 |
| A7 | "Archived Tullock solver is a valid general-r mirror" | **UNVALIDATED** | task-9: archived r=1-with-multiplier formula's fixed point is accidentally right (matches analytic x*=rV(n−1)/(n²c)), but its individual response is wrong by up to 0.87 (r=1.5)/2.68 (r=2.5) effort units under heterogeneity (utility loss up to 0.162/child); for r>1 a corner e=0 is the global best response in 5/24 anchors |
| A8 | "2–5× engine speed-up is available for Gate 2/3" | **UNPROVEN** | task-12 `d1acdf3`/`1b34d36`: KEEP-MEMO-ONLY shipped (bit-identical outputs, 68/68 tests), end-to-end **1.113×** (controller 1.196× on superseded build); 2–5× unproven because 93.6 % of runtime is 405 float32 DP calls that cannot be re-associated within ≤1e-12. Levers: prep grid 9→5 ⇒ ~1.7×, 9→4 ⇒ ~2.0×; compiled kernel 5–10× (violates pure-NumPy) |
| A9 | "Shipped E1/Q3 pooled selftest can separate OVB from minority-effect leakage" | **CONTRADICTED** | task-8 `ffed664`/`01cb4d3`: FE size 0.052–0.062 vs pooled size **0.996–1.000** under zero-effect null (bias +0.23/+0.39/+0.49; coverage 0.02/0/0); permutation within-invariance 6.66e-16; replacements WCR size 0.025–0.042, cluster bootstrap 0.033–0.050 / coverage 0.95–0.97 |
| A10 | "Legacy symmetric DGP design is usable" | **CONTRADICTED** | task-7 `01cb4d3`/`9e04236`/`47b342a`: legacy 3/5 rank with min singular value exactly 0; corrected crossed design rank **5/5 in 500/500** populations, recovery RMSE 0.04–0.13 vs legacy 0.58–0.64; 182,212 accepted + 106,902 posterior-predictive draws retained |

**Gate-1 impact: none.** These are P0 annex items; Gate-1 evidence (invariants/checks/540 migration) is unaffected and
the task-12 patch is bit-identical (Gate-1 540 used the pre-task-12 `98baf6b` engine). Any future citation of these
items must carry the artifact/commit and status above.

---

## ADJUDICATOR ADDENDUM — Paper B NEW GENERATION (2026-11-25)

**Appended by `paper-adjudicator` (independent). The ledger body and the commander's P0 annex above are unchanged;
this addendum records the 100-seed Paper B new-generation result and its provenance.** Corrected artifacts at commit
`a4b0808`, re-aggregated from intact checkpoints (HK aggregation bug fixed; **no simulation rerun**):
`results/newgen/paperB_new_generation_TRACKED.json` **sha256 `cf801af8e07f9ebf615d075c42ec742f00d5a98a19a0e938005a3632e28836d3`**
(HK+KR; `total_runs=1,800`); `paperB_new_generation_SINGLE_KR.json`
**`2b69fa08ea521c664bda59da4d6fce0d9b48d494d5cee793b69987795bef0330`** (`total_runs=900`); provenance
**`8f08164d08006d5c0225cd2115352270560806fe4055294ff16f453dd62e3301`** (campaign 2,700; wall 11,234.49 s; 8
workers). **Engine `98baf6b`** (pre-re-pin; 118-series numerics unchanged vs `846c9e0`); spec content `c5f9e2de…`;
100 matched seeds; frozen parameters ⇒ **zero calibrated-parameter uncertainty**, seed-MC only. The earlier defective
artifacts (`14fc2a31…`, `697e7ca9…`, `cba8ee0f…`) are **SUPERSEDED — do not cite**. Independent cross-check: the
adjudicator re-aggregated the raw HK checkpoints (9×100) and the KR checkpoints; the result matches the corrected
JSON **exactly** (max |mean diff| 0.0; all spend indices identical).

| # | claim now in play | status | exact artifact / evidence |
|---|---|---|---|
| NB-01 | **CF4a meets the pre-stated both-jurisdiction Win-Win** under the new generation | **REPRODUCED SIMULATION** (new generation; frozen spec; seed-MC only) | HK 70.59 spend / elite 23.21 vs baseline 24.82; KR-TRACKED 73.13 / 22.16 vs 23.90; KR-SINGLE 75.43 / 22.04 vs 24.08. CF4 reversal vs pre-repair 540 (which failed HK 48.64 > 46.36); repaired 540 legacy-gate-list also passed (70.58/23.44; 72.48/21.47). Robust across two repaired specs and 30 vs 100 seeds. |
| NB-02 | CF4b fails; CF1b fails; **CF3b (single lever) passes both** ⇒ the paper's "only pairing compression with caps/seats works" is false | **REPRODUCED SIMULATION** for the pass/fail pattern; the paper's "only pairing" claim **CONTRADICTED** | CF4b 89.99 / 109.70 / 117.74 spend; CF1b 97.25 / 99.19 / 98.99; CF3b 70.88/23.43 (HK), 73.21/22.21 (KR-TRACKED), 75.53/22.09 (KR-SINGLE). |
| NB-03 | **Substantial participation reduction under CF4a** (~13 pp K–12); **welfare interpretation unresolved** | **REPRODUCED SIMULATION — first-class caveat** | HK K–12 61.93 → 48.60 (−13.33 pp), G12 49.37 → 39.14 (−10.23); KR-TRACKED 55.79 → 42.81 (−12.98), G12 36.25 → 30.56 (−5.69); CF3b similar (48.56 / 42.80). The pre-stated criterion is spend + elite share only. Phrase "meets the pre-stated spend/elite criterion while reducing participation by ~13 pp", never "win-win" unqualified. **A participation fall is not automatically a welfare cost**: it could be lost support, substituted school provision, or reduced low-value purchase; telling them apart needs learning/access/teacher-workload/student-time outcomes not measured here. Paper B's spec (`own_ban=0.95`, `mode=positional`) suppressed the engine's withholding/own-teacher/positional-vs-learning mechanisms; the emergence question is **Paper C**, not Paper B. |
| NB-04 | Earlier new-gen artifacts had an **empty HK summary** due to an aggregator key bug (`TRACKED` vs `PRIMARY`) | **PROVENANCE CORRECTION — not a model defect** | Corrected at `a4b0808` by re-aggregating the intact `ckpt_HK_*_PRIMARY.jsonl` (9×100) and KR checkpoints; no rerun. Engine label corrected to `98baf6b`; TRACKED `total_runs=1,800`; campaign total 2,700. |

**Status changes to earlier Paper B rows in this ledger:** B-03/B-04/B-05 remain REPRODUCED SIMULATION for the
pre-repair direction but the manuscript's readings are now decisively **CONTRADICTED** by the new generation — "tax
backfires on spending" (new-gen CF1a 96.47/97.12 < 100), "wage compression is regressive" (new-gen CF3b elite
23.43/22.21 below baseline), and "only pairing" (CF3b single lever passes) do not survive. The pre-repair CF4 failure
(B-35) and the repaired-540 pass (B-36) both remain reported; the new generation **confirms the reversal**. Paper B
now has a citable **methods/negative-paper core**, but is still **not calibrated** (Gate-2 not run) and must not use
"win-win" without the participation-cost caveat.

**Still open:** X-27 / item (c) gate-architecture grid (5,632 runs, launched 19:46) — adjudicate against Amendment A3
when its result JSON lands.
