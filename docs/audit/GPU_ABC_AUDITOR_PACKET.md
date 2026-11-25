# GPU scripts (RTX 3080 Ti lane) — auditor packet

> **POST-AUDIT STATUS (2026-11-25): QUARANTINED.** An external audit of commit `045a63e` found two structural
> defects: the five advertised ABC moments have **rank 4** (overall participation ≡ ⅔·G9 + ⅓·G12, so it is
> redundant), giving ≥2 unidentified directions; and the country-block permutation is algebraically invariant
> under country fixed effects, so it cannot test the within-country estimand. The provider-choice parameter is
> analytic: δ = ln(0.32/0.68) = −0.7537718. Full record + dispositions:
> `docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md`. Nothing here is `VALIDATED`; GPU/CPU agreement validates
> arithmetic only.



**Date:** 2026-11-25 · **Purpose:** give an external auditor everything needed to judge the three GPU
scripts, what they were trying to do, what they actually produced, and what must **not** be claimed from them.
**Status labels (use verbatim):** `AUTHOR-REPORTED` · `PRE-REPAIR` · `UNRESOLVED`. None of the outputs here is
`VERIFIED EMPIRICAL`, `REPRODUCED SIMULATION` or `VALIDATED SIMULATION`.

Source of these scripts: the prior Gemini/Neon research context, handed to the fresh window as
`rtx3080ti_gpu_scripts_bundle.zip` (sha256 `bb481b87a8ae1bac63d33ca3a4424ef7195fd29baaae9c3432d7e92ee7785550`).
They were run once on an AutoDL RTX 3080 Ti by the legacy `gpu-rtx3080ti` lane on 2026-11-25; the fresh window
harvested them read-only. The lane handed over control at 14:38 CST and started nothing new.

---

## 1. Where the files are on GitHub

Repo: `https://github.com/TreyModels/atlas-of-education` (public). All links below are **commit-pinned**.

| artifact | branch @ commit | path | sha256 |
|---|---|---|---|
| **Job 2 script, as-shipped (7-param)** | `research/gpu-rtx3080ti-2026-11-25` @ `9f7dfa9` | `research/records/2026-11-25-gpu-rtx3080ti/scripts/gpu_bray_abc_and_contest_surface.py` | `0709032c043372cafd79d1df4c62dd352403e881afc1fc395cb5956a19a15d2e` |
| same file, earlier deposit | `research/shadow-education-contest-2026-11-25` @ `7356c97` | `papers/shadow-education-contest/code/rtx3080ti_gpu_scripts/gpu_bray_abc_and_contest_surface.py` | same hash |
| **Job 2b script, corrective 6-param** | `research/gpu-rtx3080ti-2026-11-25` @ `9f7dfa9` | `research/records/2026-11-25-gpu-rtx3080ti/scripts/gpu_bray_abc_and_contest_surface_6param.py` | `012b14bb93ef9e668c1a578f7f98273fed3a41d9f7cf404a6ed26fa2e9c1623f` |
| **Job 1 script (E1/Q3 + selftest)** | same @ `9f7dfa9` | `research/records/2026-11-25-gpu-rtx3080ti/scripts/gpu_e1_q3_wild_cluster_ri.py` | `3bbbc19ac42020b64a6d88c57118d75702c42dabddc0038f8ea087a6b2caf6c9` |
| runner | same @ `9f7dfa9` | `.../scripts/run_gpu_jobs.sh` | — |
| **outputs** | same @ `9f7dfa9` | `.../results/bray_and_contest/bray_abc_and_contest_surface.json` | — |
| | | `.../results/bray_and_contest_6param/bray_abc_and_contest_surface.json` | — |
| | | `.../results/e1_q3_selftest/wild_cluster_ri_results.json` | — |
| | | `.../results/e1_q3_selftest_cpu_ref/wild_cluster_ri_results.json` | — |
| run record | same @ `9f7dfa9` | `.../RUN_REPORT.md`, `.../MANIFEST.sha256`, `.../env_lock_rtx3080ti.txt`, `.../logs/*` | — |
| harvest + reuse verdict | `research/contest-audit-v2-2026-11-25` @ `1b7d472` (and later) | `docs/audit/harvest/gpu_rtx3080ti/` | `HARVEST_MANIFEST.csv` |

Direct URLs (replace with the paths above):
`https://github.com/TreyModels/atlas-of-education/blob/9f7dfa97a61359a5e432eb9c44a9e632de07fc92/research/records/2026-11-25-gpu-rtx3080ti/scripts/<file>`

---

## 2. Job 2 Part A — what the 7-parameter "Bray ABC" is trying to do

**Goal (as the script's own docstring puts it):** a GPU-batched **de-collinearized 7-parameter Bray ABC** for a
three-option (none / own tutoring / other tutoring) multinomial-logit model, fitted to **Bray's Cambodia/Asia
aggregate benchmark moments**, plus a 100-fresh-seed stability bank.

**The model, as implemented** (`run_gpu_bray_7param_abc`):

- Fixed **synthetic** population: 630 pupils = 6 schools × {G9, G12} → 420 G9 + 210 G12, 210 urban + 420 rural.
  Covariates are synthetic draws: `log_y ~ N(0,1)`, `school_gap ~ U(0,1)`.
- Parameter vector (7): `theta = [b0_eff, b_income, b_school_gap, delta_g12, urban_demand, teacher_threshold, delta_other]`.
- Utilities: `V0 = 0`;
  `base = θ0 + θ1·log_y + θ2·school_gap + θ3·is_g12 + θ4·is_urban`;
  `V1 = base` (own), `V2 = base + θ6` (other). **`θ5` never appears.**
- Moments actually computed (5): mean participation `0.73` (tol 0.05), G9 participation `0.67` (0.05),
  G12 participation `0.85` (0.05), urban−rural gap `0.14` (0.04), own share `0.68` (0.06).
  The docstring also lists `other_share = 0.32` and `teacher_tut = 0.55` — **neither is computed**.
- Acceptance: a draw is accepted if `max_j |M_j − target_j| / tol_j ≤ 1`. 200,000 draws, batches of 20,000,
  seed `20261125`.

**Results actually produced:**

| run | accepted | accept rate | best `max_z` | posterior condition number |
|---|---|---|---|---|
| as-shipped 7-param | 92 / 200,000 | 0.046 % | 0.4550 | 25.96 (`posterior_corr_cond_6active`) |
| corrective 6-param | 77 / 200,000 | 0.0385 % | 0.4075 | 21.03 |

**The defect the auditor should focus on (confirmed by this inspection and by the external review §5):**

1. `θ5 = teacher_threshold` is **dead** — it enters neither the utilities nor any moment. A 7-parameter ABC cannot
   identify it; **`best_theta_7param`'s 6th coordinate (θ5, 0-indexed 5) is meaningless** — the unused parameter is the sixth of the seven, not the seventh.
2. Even after dropping `θ5`, the corrective run has **6 active parameters against only 4 independent moments** — the five advertised moments have rank 4 because overall participation is identically ⅔·G9 + ⅓·G12 (420 G9 / 210 G12; 0.73 = ⅔·0.67 + ⅓·0.85).
   The posterior is therefore **not point-identified from the moments**; the uniform prior bounds do the
   identifying. The condition numbers (25.96 → 21.03) confirm the remaining parameters are strongly correlated.
3. The declared 7 moments are not used: only 5 are computed, and `teacher_tut`/`other_share` are absent. Any claim
   of "7-moment fit" is unsupported.
4. The population is **synthetic**, not the Bray survey micro-data; the targets are aggregate constants typed into
   the script. This is a self-test of a computation, not an empirical calibration.

**Correct labelling:** the 7-param output is `AUTHOR-REPORTED` + **BROKEN for identification**; the 6-param output
is the honest corrective, still `AUTHOR-REPORTED` and approximate. Neither is a calibration of the Atlas engine.

---

## 3. Job 2 Part B — what the "contest sensitivity surface" is trying to do

**Goal:** a 20 × 20 × 5 = 2,000-point GPU surface over `contest_r ∈ [0.8, 2.5]`, `contest_price ∈ [0.05, 0.30]`,
and seat share `S ∈ {0.12, 0.16, 0.23, 0.35, 0.50}`, mapping where the **Seat-Expansion Paradox**
(`dSpend/dS > 0`) holds, and the 2024 Korea seat-expansion paradox.

**What it actually computes:** 1,000 lognormal households (`y = exp(0.65·N(0,1))`), fixed elite log-wage prize
`delta_v = 1`, and a **30-iteration damped fixed point** on mean effort:

```
A   = (1/S − 1) · (x0 + ē)                  # rival mass; x0 = 2
e_i = sqrt(max(r · delta_v · A · y_i / p, 0)) − A − x0
e_i = clamp(e_i, 0, 4.5)                     # annual effort cap
ē   = 0.5·ē + 0.5·mean_i(e_i)
```

Then `spend = mean(p·e_i)`, `participation = mean(e_i > 0.25)`, and the "paradox share" is the fraction of the
400 (r, price) cells where raising S increases mean spend.

**Results:** `paradox_share(S 0.12→0.16) = 1.0`, `paradox_share(S 0.12→0.50) = 1.0`,
`mean participation jump = 0.3709`.

**Caveats for the auditor:** (i) this is an **approximate symmetric Tullock best response** solved by a damped
fixed point — it is *not* the engine's realized Gumbel-max Plackett–Luce contest; (ii) the "paradox" is defined on
**aggregate mean spend**, not per household, and a share of exactly 1.0 across all 400 cells is suspiciously clean;
(iii) the docstring itself labels Part B an approximate sensitivity exercise. It must not be cited as a boundary
map of the model's contest mechanism.

---

## 4. Job 1 — what the E1/Q3 script tries to do, and why it is not a reconstruction

**Goal:** GPU batched **wild-cluster bootstrap** (Rademacher, CR1 standard errors) and **country-block permutation**
for Paper #1's E1 and Q3 estimators ("referee armor" for a "zero universal laws, 32 regimes" claim).

**Two modes:**
- `--panel-csv <file>` → panel mode. As shipped, panel mode builds `X = [1, x]` **only**, dropping controls and
  fixed effects. That is not the E1/Q3 regression specification, so it cannot be described as a reconstruction.
- no CSV → built-in **selftest** `selftest_minority_effect_15pct` on synthetic data, to validate the GPU CR1 /
  wild-cluster maths against a CPU reference.

**What was actually run:** the **selftest only** (`B = 2000` wild cluster bootstrap; `B = min(B,1000)` block
permutation). GPU and CPU-forced runs agree on every deterministic quantity to **max abs diff 8.9e-15**;
p-values sit at the resolution floors (wild cluster `p = 0.000499750 = 1/2001`; block permutation
`p = 0.000999 = 1/1001`). RNG-dependent bootstrap percentiles differ because CUDA and CPU RNG streams differ for
the same seed.

**Panel mode was not run — the E1/Q3 panel CSV is MISSING.** Full E1/Q3 reconstruction status: **UNRESOLVED**.

---

## 5. Audit checklist (concrete)

1. Confirm `θ5` is unused: grep the as-shipped script for `th[:, 5]` / `theta[5]` — it never enters `V0/V1/V2`
   or any moment. Reject any "7-parameter calibration" claim.
2. Count active parameters vs independent moments: 6 vs 5 in the corrective run. Ask whether a 6-param posterior
   with a 5-moment loss can be point-identified; check whether the `max_z ≤ 1` acceptance region is a credible
   posterior approximation or a prior-bounded box.
3. Confirm the targets (`0.73, 0.67, 0.85, 0.14, 0.68`) are constants in the script and the population is
   synthetic; verify they trace to Bray (Cambodia/Asia) or flag as unsourced.
4. Reproduce the accept rates from seed `20261125`, `n = 200,000` on any CUDA 11.8 GPU (≈ 3 s wall).
5. Confirm the contest surface uses the approximate Tulloch fixed point, not the engine's PL gate.
6. Check whether the "paradox share = 1.0" is an artefact of the aggregate definition and the effort cap.
7. For E1/Q3: confirm `X = [1, x]` in panel mode and that no panel CSV exists; treat as `UNRESOLVED`.
8. Verify the GPU-vs-CPU selftest diff (8.9e-15) and that p-values are at the `1/(B+1)` floors, i.e. the selftest
   validates numerics only.
9. Verify the environment: torch `2.7.1+cu118`, CUDA available, RTX 3080 Ti, cap 8.6, py 3.10.8, numpy 1.24.1
   (`env_lock_rtx3080ti.txt` is a 152-package `pip freeze`).
10. Treat all four JSONs as `AUTHOR-REPORTED` / `PRE-REPAIR`; none may enter a calibration table or a Gate-1
    report without independent re-derivation.

## 6. Reproduction

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118   # see note on mirror below
pip install numpy pandas scipy
python3 gpu_bray_abc_and_contest_surface.py --n-abc 200000 --seed 20261125 \
        --out-dir ./results_rtx3080ti/bray_and_contest
python3 gpu_bray_abc_and_contest_surface_6param.py --n-abc 200000 --seed 20261125 \
        --out-dir ./results_rtx3080ti/bray_and_contest_6param
python3 gpu_e1_q3_wild_cluster_ri.py --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest
CUDA_VISIBLE_DEVICES="" python3 gpu_e1_q3_wild_cluster_ri.py --B 2000 \
        --out-dir ./results_rtx3080ti/e1_q3_selftest_cpu_ref
```

**Install note (auditor-relevant):** the official `download-r2.pytorch.org` path served this instance at
**27 KB/s** (905 MB ≈ 9 h), so the wheel was fetched from the Aliyun pytorch-wheels mirror in 16 parallel ranges
and its sha256 verified (`89433c62…`). This is an environment-workaround, not a numerical change; the same torch
`2.7.1+cu118` was used for the outputs.

## 7. Verdicts

| artifact | verdict |
|---|---|
| `bray_and_contest/…json` (7-param) | `AUTHOR-REPORTED`; **BROKEN for identification** — do not report as a 7-parameter calibration |
| `bray_and_contest_6param/…json` | `AUTHOR-REPORTED`; corrective but still **prior-dominated / not point-identified**, approximate |
| contest surface (both JSONs) | `AUTHOR-REPORTED`; **APPROXIMATE** sensitivity, not the engine's contest mechanism |
| `e1_q3_selftest/…` + `_cpu_ref/…` | `AUTHOR-REPORTED`; **GPU-numerics validation only**, not an E1/Q3 reconstruction; panel mode `MISSING` |
| E1/Q3 reconstruction | `UNRESOLVED` |

Related internal docs: `docs/audit/harvest/gpu_rtx3080ti/README.md` (harvest provenance),
`docs/audit/GATE0_REPORT.md` (Gate 0), `papers/shadow-education-contest/REVIEW_RESPONSE_2026-11-25.md` §5.
