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
| NB-03 | **Substantial participation reduction under CF4a** (~13 pp K–12); **welfare interpretation unresolved** | **REPRODUCED SIMULATION — first-class caveat** | HK K–12 61.93 → 48.60 (−13.33 pp), G12 49.37 → 39.14 (−10.23); KR-TRACKED 55.79 → 42.81 (−12.98), G12 36.25 → 30.56 (−5.69); CF3b similar (48.56 / 42.80). The pre-stated criterion is spend + elite share only. Phrase "meets the pre-stated spend/elite criterion while reducing participation by ~13 pp", never "win-win" unqualified. A ~13 pp K-12 participation fall under CF4a is an **unmeasured welfare change**, not automatically a welfare cost: it could be lost useful support, substitution by school-provided preparation, or families dropping low-value tutoring purchases. Interpretation requires learning/access/teacher-workload/student-time data that the programme does not yet have. The criterion's Win-Win is therefore an **accounting statement about spend and elite-Q5, not a welfare statement**. Paper B's spec (`own_ban=0.95`, `mode=positional`) suppressed the engine's withholding/own-teacher/positional-vs-learning mechanisms; the emergence question is **Paper C**, not Paper B. |
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

---

## ADJUDICATOR ADDENDUM — Paper C / Paper D DESIGN AUDIT (2026-11-25)

**Appended by `paper-adjudicator`. Design-only artefacts; no box compute. No inventory equation is declared false.**
Artefacts: `PAPER_D_EQUATION_AUDIT.md` sha256 `b6bafd1490b0a98df021f8b6ad1caff52b6ddf1a18b5606d4982ef8e1050a49d`
(commits `02990f9`+`044f7d0`); `PAPER_C_MODEL_GAP.md` sha256
`d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc`; inventory
`refs/education-equation-inventory-20261124.txt` sha256
`0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df`.

| # | item | status | exact evidence / caveat |
|---|---|---|---|
| PC-01 | Paper C probe anchors: Paper B canonical is a **private-market regime** (withheld `0.00000`; own-teacher share 2.47 % HK / 2.82 % KR); q0 0.8→1.2 lowers K–12 tutoring **0.605→0.491** and spend **161.7→135.9**; withholding regime (`pay_ratio=.55`, `monitoring=.2`, `own_ban=0`) → `h=0.144`, own share **0.528**; +`firm_ban=.9` → own **0.978**, spend **118.1**, firm price **2.0957** | **REPRODUCED SIMULATION — PROVISIONAL ANCHORS (design-only)** | `PAPER_C_MODEL_GAP.md` §2; host probes, read-only. These are anchors, not Paper C results and not adjudicated claims. |
| PC-02 | Paper C confirmatory grid: 3 (S) × 3 (L) × 4 (supply) = **36 cells** + 4 regime anchors; N=600/T=46 screening ≈320 runs ≈**2.2 CPU-h**; N=1500 confirmatory subset ≈12 CPU-h | **UNRESOLVED — PRE-REGISTRATION REQUIRED** | No box compute until a prereg is approved; review with the four-criticism discipline (no identification overclaim; design-cell counts only; seed-MC; no permutation inference). |
| PC-03 | **Paper C confirmatory prereg draft reviewed** (commit 2e69339; sha256 `10406a33…bf7`): orthogonal 36-cell design + 4 anchors, T1–T4 primaries with predicted signs/MDE/indeterminate rules, Holm, binding assertions, contamination declarations, evidence layering, ≤7 CPU-h; Pilot-0 v3 declared EXPLORATORY and excluded | **UNRESOLVED — CONDITIONAL; NOT preregistered-final** | **8 blocking amendments:** (1) missing 36-cell appendix table/factor+seed mapping; (2) one primary per test violated in T3/T4; (3) T4 overclaims "positional not learning" though T5 is wave-2; (4) screening→confirmatory selection/winner's curse (need disjoint seeds or all-cell confirmatory); (5) four-criticism section absent from the file; (6) T1 q0 scales public+private quality → quality-bundle, not clean S substitution; (7) T2/T3 contrasts and own_share definition underspecified, market-only control near-trivial; (8) runner/analysis commit, exclusion/stop/assertion-failure rules missing. No confirmatory compute until amended + four-criticism section + Codex protocol/Kaplan. | **Re-review (Amendment A1, commit `c0f4eb6`; file sha `dd58919d…`):** the 8 original blocking items are substantively addressed in §8 A1.1–A1.8 (36-cell ids/mapping + screening seeds 0–7; one primary/test; T4 overclaim removed; disjoint confirmatory seeds 100–131 + pass rule + all-cell fallback; in-file four-criticism section; T1 quality-bundle; T2/T3 `own_share_financial` + absolute quantities; provenance/stop/exclusion/MDE/Holm/Caplan V). **Still CONDITIONAL — 4 residual fixes:** (1) body §§1–6 still pre-A1 (16 seeds; T2 `own_share`; T3 `h and own_share`; T4 positional; §6 ≤4 CPU-h/16 seeds) — add "§8 supersedes" or update; (2) T3 cell mapping inconsistent (A1.1 B=own_ban .95/own-closed but A1.7 calls B own-open; T3 B vs A cannot satisfy h>0/own_share>0.1) — remap T3 to A|P55 vs A|P12 or fix labels; (3) compute envelope inconsistent (32 seeds × N=1500 × ~5–7 min/seed ≈3.2 CPU-h/cell vs ≤4 CPU-h cap/16 seeds) — recompute/raise cap/limit passers; (4) gate kind/`contest_r` absent from 36-cell mapping — fix gate dimension fixed-gate declaration. Recommended: explicit 36-row list, "screening-confirmation on pre-declared passers" wording, launch manifest hashes. **Not cleared for preregistered-final; no compute.** |
| PD-01 | Paper D omissions **M1–M5** (school prep S; positional fixed seats; teacher withholding/rent; time budgets; supply form) | **CANDIDATE GAPS — UNRESOLVED, not errors** | `PAPER_D_EQUATION_AUDIT.md` §3; engine evidence that each can matter; **no inventory equation declared false**. | Machine-checked support (commit `e0a5662`): five omission/independence lemmas M1–M5 in `Atlas/Claims.lean`; `Atlas/Model.lean` proves gap/accounting/capacity/rank invariants and counterexamples, so the omission claim is a conditional formal statement, not empirical magnitude. |
| PD-02 | Already-recorded contradictions (KR G9 phantom prize; expected≠realised; 100 % seat paradox; Paper B pairing) | **CONTRADICTED (as already recorded)** | Kept separate from the omissions; do not conflate "inventory omission" with "equation false". |
| PD-03 | Divergence tests **D1–D9**: standard-equation prediction X vs mechanism-rich Y, cell, outcome, compute (≈300–420 runs at N=600/T=30, ≈2–3 CPU-h; D3/D7 need wave-2 extensions) | **UNRESOLVED — pre-registerable, not results** | No Paper D compute until Paper C confirmatory run + approved prereg (Commander rule). |
| PD-04 | Inventory is an **AI-generated candidate map with placeholder citations** ("UIS+2", "OECD+3", "doi.org+4", …) | **UNRESOLVED — attribution risk (binding)** | **No equation or citation may be used without primary-source verification** (Hanushek; Todd & Wolpin; Cunha & Heckman; Becker; Mincer; Dang & Rogers; Bray; Tansel & Bircan; Biswal; Jayachandran; Kim & Lee; UIS/World Bank/OECD). Equation numbers refer to inventory text, not published sources. |
| PD-05 | **Citation verification of inventory §5:** **0 of 57–86 equations verified**; every 'citation' is a placeholder (`UIS+2`, `OECD+3`, `hanushek.stanford.edu+2`, `doi.org+4` …); one **false publisher** (`RCNi Company Limited`, a nursing publisher, attached to Becker & Lewis 1973); Dang & Rogers = graphical + one naive OLS; Tansel & Bircan = Tobit expenditure; Bray = monographs no equations; Kim & Lee = demand/positional; Biswal 1999 text not retrieved | **CONTRADICTED — no inventory equation is a verified quotation** | `CITATION_VERIFICATION_SHADOW_ED.md` sha256 `020ece4f08c00c5b82325fee5d3a98671b903676a7239a2557cb0a0156d9ef45` (commit `3d8b80a`). **Nothing may be cited from the inventory without primary-source verification**; correct DOIs/pages in the report. |
| PD-06 | **Jayachandran (2014, JDE 108:190–205) published model DOES contain withholding** — school-day material `m`, achievement `s(m,t)` with `s_mt<0`, teacher effort/penalty `φ(m)`, kickbacks/coercion in an earlier version — but **inventory E57–E86 has no `m`, teacher-effort, or withholding/detection equation** | **UNRESOLVED — textual support for omission lemma M3/M1; numeric importance not shown by text alone** | Same citation-verification report (§5.2, §6). Directly backs the **M3** omission (and the M1 school-day-material gap); the D-tests are still needed for magnitude. | Machine-checked complement: the classical-demand invariance to S/positional seats/withholding/time/supply form is proved (M1–M5) and the false universal generalisations are countered (`fixed_seat_relative_rank_counterexample`, `complementarity_counterexample`, `feedback_capacity_counterexample`, `max_not_additive`); still does not establish empirical importance (EP-1/EP-2 + external data). |

**Record status:** Paper D is a **candidate new-generation finding/section** (design audit) and Paper C is a
**design-only plan**; both are pre-registerable and neither is an adjudicated result. Paper C/D wording must not claim
the standard literature is wrong or that the engine is validated.

---

## ADJUDICATOR ADDENDUM — MODEL ZOO / D1–D2 and EVIDENCE-LAYER LIMITS (2026-11-25)

**Design-only. No run has started.** `MODEL_ZOO_DISCRIMINATORS.md` sha256
`5a67fcf1db9648dda02be88c3cedace5ff0818e9ad1dd8261cbabcd1caf1f48f` (commit `6e780c2`);
`TUTORING_DATA_INVENTORY.md` current sha256 `3469c644f7112e4b8de0c635e1ec72e7598b0a0c3b7ef0fb9e905fbc6cbe2608`
(commits `f95164d`/`2c315c0`; the Lead-cited `a33fa368…` is superseded); `DHS_E1E8_MODEL_MAPPING.md` current sha256
`7e27e83c38495bd160d2f055d53c43d20942c5da7053fe90a69e757c46b2d770` (earlier `11252df2…` superseded).

| # | item | status | evidence / binding condition |
|---|---|---|---|
| MZ-01 | **EP-1 engine probe** (matched public-feedback intervention; NOT a named-theory discriminator): arms C0 / P (`school_feedback=x`, `feedback_intensity=0` no-effect negative control, must be bit-identical to C0) / T (`feedback_intensity=1`, public basic schools only, teacher marking time) / B (`q0` bundle contamination demo); seeds **100–131 confirmatory**, 0–7 exposed/exploratory; primary Δ K–12 participation T−C0 with P−C0 control; fixed-R and rank-R outcomes reported separately; **NOT RUNNABLE TODAY** (needs wave-2 public-only S lever) | **UNRESOLVED — design-ready engine probe; no run** | `MODEL_ZOO_DISCRIMINATORS.md` sha256 `bd0bf29e…2a2eeb1` (commit `9035547`, supersedes v1 `6e780c2`). Omitting S from a demand regression ≠ zero true response; `q0` shifts public+private quality; Lean omission lemma is definitional invariance. |
| MZ-02 | **EP-2 engine probe** (own access × firm constraint 2×2, seeds 100–131): E00/E01/E10/E11; fixed `own_share_financial` denominator (own/(own+firm) financial tutoring, contest-only excluded), `contest_prep_class`, **absolute** own/firm counts+spends; baseline-matched seeds; pre-registered DiD participation sign; binding assertions (withheld, count reconciliation); `firm_price` reported not mechanism; **NOT CONFIRMATORY-RUNNABLE** until additive series land | **UNRESOLVED — design-ready engine probe; no run** | Same v2 doc. Engine probe, not a test of any named model. | **Row 8 = Bryan Caplan (probable, UNCONFIRMED, tag V; likely *The Case Against Education*, 2018)** — signalling/human-capital-critique, not a straw man; primary source must be verified; protocol = both competing models on the same evidence AND complementary modules. |
| MZ-03 | **Run gate:** no run until (i) Paper C prereg residual fixes land + Codex protocol/Kaplan confirmation, (ii) the EP-1/EP-2 probe design is signed off, (iii) seeds 100–131 + engine/spec/runner hashes frozen, (iv) capacity allocated; EP-1/EP-2 not runnable today | **UNRESOLVED — process gate** | Lead/Commander/Codex instruction; `MODEL_ZOO_DISCRIMINATORS.md` §4 runnability matrix. |
| MZ-04 | **Pilot-0 provenance:** code-authoritative **128 runs / 16 cells** (supersedes earlier 96/12 docstring mention); committed v3 has 4 regimes and `pay_ratio=.55`, `monitoring=.2` (commit `fbc1991`/pilot record); the prereg must quote **code + commit**, not the docstring | **UNRESOLVED — provenance** | `PAPER_C_CONFIRMATORY_PREREG.md` Amendment A1 / commit `c0f4eb6`; Pilot-0 record corrected. |
| EV-01 | **HK-vs-PH 2019 supply-form is unobserved; SEA-PLM 2024 is a candidate route, not yet testable.** PISA 2018/2022 has participation/hours by ESCS quintile for HK/PH/CN but **no expenditure and no own-teacher-vs-firm item**; provider-type data only Korea (KOSTAT); PH/KH none. **SEA-PLM 2019 parent questionnaire has NO tutoring item (full 13 pages + 6-page codebook read) — the earlier 'KH route = SEA-PLM 2019' is REFUTED.** **SEA-PLM 2024 framework p.89 item PA18 (verified text, D): PA18A paid assistance outside school / PA18B free tutoring outside school / PA18C paid tutoring provided by the school / PA18D free tutoring provided by the school** — the 2×2 supply-form item Paper C needs; SEA-PLM 2024 results/data are released (ILSA-Gateway), so 2024 may be usable pending KH/PH coverage + parent–student linkage/codebook checks (dataset presence/linkage still V). | **UNRESOLVED — binding limitation** | `TUTORING_DATA_INVENTORY.md` §2–§3; framework p.89. The emergence prediction can be illustrated, not tested, until coverage/linkage is verified. |
| EV-02 | **Paper C's empirical leg is feasible-partial (participation/hours only)**; supply-form/withholding predictions remain **theory/simulation** until codebooks/access verified. **Blanket 'theory-only' is too strong:** SEA-PLM 2024 PA18A–D is a candidate supply-form route pending KH/PH coverage + linkage; PA18 text D, dataset/linkage V. | **UNRESOLVED — binding limitation** | Same. Papers C/D must not imply the empirical leg exists until the 2024 route is verified. |
| EV-03 | **DHS E1–E8 cannot test the model zoo:** no tutoring, learning, gate/seat, time-use, earnings or expenditure variables; they weakly constrain demand-side distributions and falsify a proxy (E8 household size ≠ kin support) only | **UNRESOLVED — binding limitation** | `DHS_E1E8_MODEL_MAPPING.md`. **No model may "win" on DHS alone**; DHS = auxiliary descriptive evidence layer. |
| EV-04 | **D/L/V convention:** `D` documented snippet, `L` located/access-route, `V` verified source — **nothing marked V may be asserted as fact** | **BINDING CONVENTION** | Remaining V items (PISA/SEA-PLM wording, expenditure/provider confirmation, CIEFR/CFPS/CEPS access) are explicitly unverified. |

**Status:** all Model Zoo and zoo/evidence claims are **pre-registerable designs or binding limits, not results**.
Paper C/D sections must not imply the empirical leg exists; the unfalsifiable list is binding.

**X-27 STATUS (gate-architecture grid, 2026-11-25): CLOSED — REPRODUCED SIMULATION.** Clean artefact
`results/audit/newgen/gate_architecture_results.json` sha256
**`bce3da363afbdcfd16052d2c661107dc8c88d082d640625ef1b0b334d8f72638`** (294,532 B; `runs 5632`, `n_cells 176`;
aggregation-only 13.5 s from the same checkpoints, **no simulation rerun**; engine `846c9e0`/core `e111397b`; spec
`e5ddef6b`; clean runner `cbdea3cd`; `year_t`; `unfired_events_asserted`). The provisional artefact was `685db398…`;
a NaN-aware semantic diff shows **only `metadata.runner_sha256` and `metadata.elapsed_seconds` changed — every result
is identical (diff 0.0)**. The earlier `builtins.np` injection note is **superseded provenance**, retained for lineage.

* **Primary H2 +5.0551 pp** [paired-bootstrap 95 % CI **2.4820, 7.9614**; MDE proxy 2.7397] → CI excludes 0, |H2| > MDE
  → **primary met**. Δcut(S=.25) +5.6170 [3.5509, 7.8840]; Δcut(S=.70) +0.5619 [−0.9924, 2.0855].
* Quota H2 +0.9915 [0.5675, 1.4893]; stop-sensitivity +5.4715 [2.2078, 8.4476]; vac0 curve +3.105/+5.055/+1.145/+0.325;
  H1 +7.9350 [6.9585, 8.9127], Spearman −1.00; bar −0.255 [−0.850, 0.325], bar_high +0.204 [−0.322, 0.763]
  exploratory only. Null rule honored (pre-repair +0.1086 = AUTHOR-REPORTED baseline, not a target). Four Codex
  positions honored.
* **Status: REPRODUCED SIMULATION** (pre-registered confirmatory new-generation; frozen spec; uncalibrated; seed-MC
  only) — **explicitly NOT VALIDATED**.
* **X-29 remains open:** realized admission rates are NaN in the raw checkpoints and cannot be recovered by
  aggregation; diagnostic-only rerun (1,280 runs ≈35 min, bar/bar_high + contest if feasible) planned after Pilot-0;
  recorded as a declared deviation, not a model failure.

**Methods lesson (citable):** this is the **third bug of this class found by reading raw artefacts rather than
summaries** — (i) fee no-op (simulation index vs calendar-year event), (ii) seed-0 hardcode, (iii) missing `np` import.
Add to the methods/negative paper: summary-level QA would have missed all three.

---

## ADJUDICATOR ADDENDUM — LEAN VERIFICATION TRACK (X-30, methods artefact)

**The engine is NOT formally verified.** Commit `4d42101`; `LEAN_VERIFICATION_SCOPE.md` sha256
`9f31108e496fdc3ac9509547ea388128d156188df9b0540c486d4406d1d3f23c`; `LEMMA_LEDGER.csv` sha256
`da956fc1e1d3a3ff18c31c98cf30f8dcd5d5c8817fab2ed55b2f0f55f5617df5`; `LEMMA_LEDGER.md` sha256
`f8be23a7da854d6b52489e63c7c765be5ccb7ed7c025c2640ccae9639d875c33`; baseline `LEMMA_LEDGER_BASELINE.json`
`b777b93f…`.

| # | item | status | evidence / boundary |
|---|---|---|---|
| X-30 | **Lean verification prototype and scope** (methods artefact; the six-status scientific taxonomy does not apply) | **METHODS ARTEFACT — recorded for traceability; NOT a scientific claim and NOT "engine verified"** | **Answer to "run everything against Lean": NO.** Tier 1 (identities, accounting, inventory omission lemmas) **recommended and prototyped**; Tier 2 (general-n Plackett–Luce) **conditional on CI Mathlib** (Mathlib not installed on this host: multi-GB, not viable); Tier 3 (float32 numerics, DID/bootstrap inference, run outputs) are **computations, not theorems**. Architecture = Lean-verified reference math + differential tests + reproducible artefacts. Prototype: Lean 4.36.0, `lake build` 16 jobs PASS, **0 `sorry`**, `#print axioms` only propext; proved budget-ledger/tax/seat/prep-recursion identities, finite PL n=2, Kind-3 `decide` lemmas for A-34/A-38/B-41/B-42 accounting cells, **five M1–M5 omission/independence lemmas** + `D02_paradox_not_universal`; LEMMA_LEDGER **132 rows** (18 declared + 114 NOT-YET) frozen to baseline `55f75eea…` (ledger `3e9dbbc1…`, `.md` `eb639671…`, baseline JSON `52dee893…`, proof-status `af6232cd…`); differential bridge **22/22** exact; CI hook PASS. Install provenance: elan→Lean 4.36.0 via GitHub mirror (default CDN 70 B/s; 608.4 MiB; ~23 min; 3.0 GiB unpacked; disk 12→8.9 GiB free); Mathlib not installed, Tier 2 CI-only. **Paper D significance:** "the classical demand equation provably ignores S / positional seats / withholding / time / supply form" is a machine-checked invariance statement, not rhetoric — supports the omission lemma M1–M5; it does **not** show the omissions are empirically important (D-tests) and carries the Tier-3 disclaimer. | QA mechanical audit FINAL PASS, re-verified at the current content-edit pin (`LEMMA_LEDGER_AUDIT.md` sha `1f3c218b…`, QA commit `c18a44f`/HEAD `92a1be6`): **R1–R8** PASS on **baseline `55f75eea…`/132 + ledger `3e9dbbc1…`/132** (ledger `.md` `eb639671…`, baseline JSON `52dee893…`, proof-status `af6232cd…`); `3ff88d39→55f75eea` is content-only (same rows/ids/statuses; ledger CSV byte-identical), no re-baseline semantics change; R8 proof-status 107/107 declarations, 46 theorems, compiled/sorry-free, axioms only ''/propext; independent lake build 16 jobs, 7 files 0 sorry, 33 axiom lines propext/none, 18/18 ids, bridge 22/22; certifies mapping + axiom hygiene only, NOT empirical truth or engine numerics; engine NOT formally verified. Prior pins (`e0a5662`/`3ff88d39…`; 130-row; `b990c99f`) preserved in history. | **Delivery refresh (commit `e0a5662`):** Luna starter `LeanStarter.lean` sha `6cfa77e7…` compiled with four documented fixes (statements unchanged, no sorry); `Atlas/Model.lean` `f6acc321…` proves gap/accounting/capacity/time/rank-invariance (`rank_invariant_under_common_shift`, explicit tie rule) and `accepted_monotone_fixed_capacity`, plus counterexamples `fixed_seat_relative_rank_counterexample`, `complementarity_counterexample`, `feedback_capacity_counterexample`, `max_not_additive`; proof-status 107 declarations/46 theorems, build 16 jobs PASS, 0 sorry, only propext, 0 prohibited deps; `LEAN_PROOF_STATUS.md` `c02b4085…`, `.csv` `1ff80fb0…`, axioms `LEAN_AXIOMS_ALL.txt` `f9c05bc4…`; bridge 22/22 (`56cdfd7b…`); ledger re-pinned to baseline `55f75eea…`/132 (ledger `3e9dbbc1…`, `.md` `eb639671…`, baseline JSON `52dee893…`, proof-status `af6232cd…`); MZ rows carry v2 EP-1/EP-2 wording and Caplan-V note. Boundary: formal statements under assumptions != engine/empirical truth; Tier 3 reproducible-artefact; no 183-equation/float claim. |

**PIN FREEZE (Lead order, 2026-11-25):** no further edits to `paper_claims.csv` until Pilot-0/X-29 close. audit-runner
re-pinned internally at `f4167fc`: baseline `55f75eea…`/132, ledger `3e9dbbc1…` unchanged, proof-status `af6232cd…`;
QA R1–R8 PASS remains valid (ids/statuses/row count unchanged). After Pilot-0/X-29, make **one batched** CSV update in a
single commit and notify audit-runner + qa-verifier with old→new sha and a row/id/status diff for a single re-pin/re-audit.

**PAPER C A2 RE-REVIEW (2026-11-25): CONDITIONALLY CLEARED — 2 textual pre-launch amendments.**
`PAPER_C_CONFIRMATORY_PREREG.md` sha256 `04532581…` (commit `bb26d49`) addresses all four A1 residual items: authority
rule (§8 supersedes §§1–6), explicit 36-row appendix with gate kind contest / `share_of='cohort'` / `contest_r` mapped
by L, T3 remapped to A|P55 vs A|P12 at same S,L, and compute recalibrated from Pilot-0 (screening ≈13.4 CPU-h;
confirmatory ≤6 passers ≈22 CPU-h; ≤36 total; screening-confirmation wording; manifest hashes). Pilot-0 record corrected
to **128/16** (`PILOT0_RECORD.md` `601e13ce…`; stale `dcd0ad9` superseded); capacity reserve **X-29 at 6 workers**.
**Required textual amendments before launch:** (1) pre-declare the >6-passer selection rule (e.g. fixed appendix-order
first 6; rest screening-only) — no post-hoc choice; (2) resolve all-cell fallback vs ≤36 CPU-h (all-36 at 32 seeds
≈132 CPU-h → separate re-approved budget, or drop). Recommended: exempt A|P12 control from h>0/own_share>0.1
assertions; state L is a gate-pressure bundle (share+contest_r) with no component-separation claim; screening is compute
and starts only after clearance + Codex. **No confirmatory compute until amendments + Codex.**

**PAPER C A3 RE-REVIEW (2026-11-25): CLEARED FOR PREREGISTRATION-FINAL.** `PAPER_C_CONFIRMATORY_PREREG.md` sha256
`0089f283…` (commit `a61ffa8`) adds the two required A2 amendments with no design change: (A3.1) >6-passer rule — first
6 in fixed appendix order confirmatory, remainder screening-only, frozen list in manifest; (A3.2) all-cell fallback
REMOVED (all-36 ≈132 CPU-h explicitly outside the ≤36 CPU-h envelope; separate re-approved budget only); (A3.3) `A|P12`
exempt from h>0/own_share>0.1, exposed arms only, failed exposed arm INVALID, L is a gate-pressure bundle with no
component-separation claim; (A3.4) screening only after prereg-final + Codex protocol/Kaplan + 1–2 slot reserve.
Manifest requirements listed. **Housekeeping (one-line, non-blocking):** top authority rule should say "§9 A3 supersedes
§8 A1 where inconsistent" because A1.4 still mentions the removed fallback; status DRAFT→FINAL on sign-off. **Final
designation/compute gated on the housekeeping edit + explicit Codex protocol/Kaplan confirmation + manifest/capacity.**

**PAPER C FINAL FREEZE (2026-11-25): PREREGISTRATION FINAL (design frozen) + LAUNCH MANIFEST FROZEN.** Final
prereg `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
`445ec423c03ffdc8521a820694a72662cabbe342331dc1c8a839023e00053a8d` (commit `e34b901`): line 7 FINAL, §8 historical
status corrected. Frozen manifest `docs/audit/PAPER_C_LAUNCH_MANIFEST.json` sha256
`6400c9db99b567faa01d9c1e62df552280170b00c062762250302daa0bb2f01a` (commit `62dc609`; FROZEN reconciled): engine 846c9e0/core
e111397b/spec e5ddef6b, runner fbeba460 (pre-launch extension note), 36 cells, seeds 0–7/100–131, N=600/1500, T=46,
measure_from=18, fail routing contest/share_of cohort/contest_r by L, unfired assertion + exposed-arm assertions (A|P12
exempt/INVALID), >6-passer rule, ≤36 CPU-h (13.4+22), 1–2 slot reserve (X-29 at 6 workers), no-compute gates.
**Provenance reconciliation — DONE:** manifest now cites final prereg `445ec423…`; `sha256_at_freeze_time=ff61f1e6…` and `superseded_by` record the §8 historical-status-only diff (no design change). Launch gated only on the 1–2 slot reserve; no screening/confirmatory compute until then.

---

**METHODS ARTEFACT X-31 — GPU Plackett–Luce port (2026-11-25).** Branch
`research/gpu-pl-port-auditv2-2026-11-25` (tip `2399aa1`); engine port commit `59fd2497765f15c108de3ec182d1febbe3d28c8a`.
Files: `contest_gpu.py` `ab08a53b…` (new, byte-identical GPU backend); `contest_math.py` `5fceb4d5…` (+169 L GPU
section/batch API; task-12 caches and `pl_realize` untouched); `__init__.py` `2c082d5c…` (+11-line optional registration);
`core.py` `5bcbc0b3…` (exactly two hunks; `_validate_events`/`EVENT_CACHED_PARAMS` intact); `modules/tutoring.py`
`b3d32cee…` (9-point batched grid + helper); `docs/gpu/port_verify.py` `6ba6013c…`; `docs/gpu/PORT_REPORT.md`
`23b7a8c1…`. **Mac evidence (flag unset):** 68/68 tests; 130-fixture digest identical; CPU batch ≡ per-row 0.0; full-run
HK Baseline seed 0 digests identical; RNG-realise digests identical; 23 boundary cases OK; torch-free default import +
graceful CPU fallback. **Boundaries (binding):** branch core `5bcbc0b3…` is NOT canonical `e111397b…` → GPU runs are
**gate-grid/sensitivity only**; must not replace CPU primary artifacts/spec hash/Gate-1 evidence; no retroactive
substitution; cross-replica batching **staged, not implemented**; **no GPU numbers claimed**. **Parity gate OPEN:** box
parity (fixtures + discrete-winner comparison + full-wall benchmark) with Commander; QA to add
`tests/test_contest_math_gpu.py` and sign off only on ≤1e-7 agreement with flips quantified. **QA tests (conditional):** branch `6c68d96`; test file sha `9ee72f9e…` (8 tests), `GPU_TESTS_QA.md` sha `7ab291f0…`, `gpu_parity_qa.json` sha `3df35bd7…`; Mac 5 passed/3 skipped; CUDA box 8/8 in 57.29 s; parity max|dP| 4.83e-8, 0/130 >1e-7, 0 seat-sum violations, 0 fixture flips. **Harness provenance defects (not engine failures): `env.backend='cpu'` (reset at port_verify.py:236 before manifest write :239), `engine_commit` empty (:113), `spec_sha256` missing — Commander fixing/re-emitting. Remaining gate: cell-level parity (2 Pilot-0 cells x seeds 100-101, per-gate-year Jaccard/sym-diff/flipped seats) + full-wall benchmark; sign off only if <=1e-7 and no unresolved flip changes a headline outcome, else CPU fallback.** Methods artefact; six-status taxonomy does not apply.

---

**X-PILOT — Paper C Pilot-0 payload (2026-11-25): EXPLORATORY / PENDING QA, not a result.**
`/root/work/paperC/results/paperC_pilot0_results.json` 69,286 B sha256
`c6e50bc1e86f8d41a8d8a332e860898445de4ce90f8f9ec7d004e438fa523f9d`; **128/128 rows**, 16 cells (4 regimes × q0
{1.0,1.2} × p_firm {.03,.08}) × 8 seeds (0–7); wall **6860.01 s ≈1 h 54 min** at 8 workers; 16 ckpts +
`MANIFEST_SHA256SUMS.txt`; QA copy `~/neon-boot/qa/incoming/paperC_results/` (`sha256sum -c` OK; bundle
`paperC_results_bundle.tar.gz` sha `ec868a57…a4fb0b`); qa-verifier notified. Manifest engine `846c9e0`/core
`e111397b…`/spec `e5ddef6b…`/runner `bc833b76…`, status EXPLORATORY with withholding/contamination notes. **QA PASS A1–A10:** `PILOT0_QA.md` sha `620375a6…` (commit `0f1013e`): 128/16, 8 seeds/cell, runtime pin `846c9e0`/core `e111397b…` + spec `e5ddef6b…` verified against git, no-op guard 12/12 non-market, A10 ckpt→summary reproduction, manifest 17/17, A9 log clean. **Caveats:** `completion_primary`/`completion_upper` all-NaN in every cell — not citable; `tut_*_by_grade_last` clean; contamination note; exploratory only; CPU-only. **Status: EXPLORATORY-VALIDATED (QA PASS A1–A10), not a confirmatory result; no Paper C claim moved.** No claims until QA sign-off
+ X-29 close; CSV frozen. **X-29 (observed):** restarted at **10 workers** (driver `46562`), 473 rows preserved (resume
confirmed), cgroup 100%, DIAGNOSTIC-ONLY `results_diag/` separate; rate/ETA to be published; operator capacity update
from the earlier 6-worker plan, no effect on X-27/primary results.

