# PAPER A — VERIFICATION AND ADJUDICATION

**Manuscript:** *When Fee Abolition Meets Rationed Gates: Shadow Education, Strategic Contests, and
Micro-Identifiability in Massifying Education Systems* (Trey Menefee, Atlas of Education Research Program).
File `papers/shadow-education-contest/paper_a_general_mechanism/When_Fee_Abolition_Meets_Rationed_Gates_APA.docx`,
369,246 B, sha256 `39092abb071f0f50552bfd920f16503c8280ecf585a7703b333657d099820c91`.
**Adjudicator:** `paper-adjudicator` (independent; did not write the engine repairs, the audit, or the manuscript).
**Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`. **Mode:** read-only synthesis; no experiments run.
**Taxonomy (verbatim, one status per claim):** `VERIFIED EMPIRICAL` · `REPRODUCED SIMULATION` ·
`VALIDATED SIMULATION` · `AUTHOR-REPORTED` · `CONTRADICTED` · `UNRESOLVED`.

## 0. Bottom line

Paper A is **two different papers stapled together**, and only one of them currently stands up.

* **The E8 empirical block is real and verified.** The point estimates, event path, Fisher-RI p-values and
  gender differential quoted in the manuscript reproduce the committed empirical records (`research/records/
  2026-11-25-e6e8-sequencing` @ `bd782be`, `research/records/2026-11-25-e8-fisher-ri`,
  `research/records/2026-11-25-gender-split-e6e8` @ `b4eb680`) to machine precision, and those records carry
  passed reproduction gates. This is the manuscript's only citable evidence. It is **descriptive/associational**;
  the source record explicitly forbids causal language. The manuscript over-reads it in two places (pre-trends and
  the gender conclusion) — see A-05/A-06.
* **The simulation/identifiability half is not evidence.** Exp 1, Exp 3, Exp 4 and Exp 5 have **no committed
  runner, seeds, or result files** in the paper's replication package. The only result artifact is a self-reported
  JSON (`passed off` as verified), and its stated `base_commit` (`68da16e`) did not contain a runnable `contest`
  gate. The archived GPU/ABC bundle that the draft leans on is **quarantined** and, where independently
  recomputed, **contradicted** (rank 4/5 not 5/7; 2-dimensional null space; analytic δ; degenerate synthetic DGP).
* **The identifiability "theorem" is not a theorem.** No independent computation of Paper A's own Jacobian exists.
  The only independent recomputation of the affiliated design finds the advertised moments have **rank 4/5**
  (not 5), a **2-dimensional null space**, **44 distinct parameter vectors** reproducing the moments, and that the
  proposed two micro-moments restore **local rank 5/5 only** — not global identification, not rank 7/7. "Proves"
  and "theorem" must be deleted; "local" must be stated.

**Publishability verdict:** the current combined manuscript is **not publishable**. The E8 block is publishable as
a short descriptive empirical paper; the measurement proposal is publishable only as a conjecture/pre-registration
with an independently computed local-rank appendix; the Tullock H2 experiment and the fee-abolition forecast must
be removed until deposited and re-run.

## 1. Evidence rule used here

1. Only the six taxonomy labels are used, verbatim, one per claim.
2. `VERIFIED EMPIRICAL` = the quoted number reproduces the committed empirical record (data hash + estimation
   code + reproduction gate) to the stated precision, **and** the manuscript's use is consistent with that record's
   permitted reading. It is **not** a causal-identification claim.
3. `REPRODUCED SIMULATION` / `VALIDATED SIMULATION` = the audit re-executed or contract-validated the run. Arithmetic
   agreement (GPU vs CPU, host vs box) is never sufficient and is never used below to promote a claim.
4. `AUTHOR-REPORTED` = an artifact exists but this audit did not execute or re-derive it, **or** only a
   self-reported JSON is offered. `UNRESOLVED` = the artifact needed to test the claim is absent. `CONTRADICTED` =
   committed code, algebra, or a verified record refutes the claim as stated.
5. Missing data/code is recorded as an unresolved **task**, never as a supporting result.

## 2. Claim-by-claim adjudication

### 2.1 Empirical E8 fee-abolition block

| ID | Claim (manuscript location) | Supporting / refuting artifact | Status | Required change |
|---|---|---|---|---|
| A-01 | Abolition-year primary-GER ATT = **+12.44 pp** (abstract, Results ¶1, Table 1) | `research/records/2026-11-25-e6e8-sequencing/results/e8_event_SE.PRM.ENRR_verified8.csv` @ `bd782be` (e=0 ATT 12.44362392207772); reproduction gate in `research/records/2026-11-25-e8-fisher-ri/results/repro_gate.json` (ATT diff 0.0) | **VERIFIED EMPIRICAL** | Keep value; add record + branch + commit; call it an ATT association, not "the surge". |
| A-02 | Mean post-abolition ATT **+25.26 pp**; event range **+22.12 … +28.56 pp** (e=+1…+6); Table 1 empirical column | same committed event CSV: +23.8244, +25.9429, +22.1208, +25.1932, +28.5608, +25.9224; mean 25.2607 | **VERIFIED EMPIRICAL** | Keep values and full 6-row path; state `n=6–7` cohorts per event. |
| A-03 | Fisher-RI **p = .0001** (placebo-date), **p = .0003–.0006** (placebo-country); 20,000 permutations = 10,000 + 10,000 | `research/records/2026-11-25-e8-fisher-ri/results/e8_ri_results.json` (p2_date T0 = 9.999e-05; p2_country T0 = 5.999e-04; p2_country Tpost = 2.9997e-04; B=10,000/family); `REPORT.md` §5–6 | **VERIFIED EMPIRICAL** | Keep; state that .0001 is the 1/(B+1) resolution floor, not a precise tail probability; add the MCSE (1.0e-4). |
| A-04 | Gender differential **D = −3.94 pp, 95% CI [−8.72, +0.29]**; "no statistically detectable gender gap" | `research/records/2026-11-25-gender-split-e6e8/results/gender_split_results.json` (D = −3.94395; paired percentile CI [−8.7178, +0.2946]); `REPORT.md` §3.4 | **VERIFIED EMPIRICAL** | Keep point estimate/CI and the pre-registered "no detected sex difference" wording. |
| A-05 | "flat pre-trends (−0.03 and −0.13 pp) and a clean −6-year placebo (−0.39 pp)" (Results ¶1) | `e8_event_SE.PRM.ENRR_verified8.csv`: leads e=−5 **+6.389** (CI −0.08, 12.86), e=−4 **+1.345**, e=−3 −0.128, e=−2 −0.027. `e8_results.json` `sensitivity.placebo-6`: `mean_att_post = −0.3910`, `att_t0 = −0.2358` | **CONTRADICTED** | Delete "flat pre-trends (−0.03, −0.13)" and "clean −6-year placebo (−0.39)". Report the full lead vector; state the −0.39 is the **mean post-period ATT under a placebo-6 assignment** (placebo e=0 ATT −0.24), not a lead coefficient. |
| A-06 | Gender non-detection is "robust to inverse-variance weighting and leave-one-out exclusion of Mozambique" (Results ¶1); Discussion "lifting boys and girls alike" | `gender-split-e6e8` `FOLLOWUP.md` (EXPLORATORY POST-HOC): IV point −4.05 (IV CI [−5.94, −2.17], excludes 0); LOO −4.07…−3.80; drop-MOZ −3.947 [−8.32, +0.24]; **"near-boundary non-detection, not a precise zero"**; paired percentile upper endpoint +0.29 | **CONTRADICTED** (as stated) | Replace with: "point estimate stable under IV/LOO, but the pre-registered paired CI upper endpoint is +0.29; an unpaired normal framing excludes zero. Treat as a near-boundary non-detection." Delete "lifting boys and girls alike" — the CI admits a female shortfall up to 8.72 pp. |

### 2.2 Exp 1 — delayed secondary-bulge `t*` "honest null"

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-07 | Live-WDI `t*` bulge-arrival test: 7,290 country-year observations, 2,500 Fisher permutations/scheme; indicators non-estimable/sparse; `SE.PRM.REPT.ZS` T0 = +1.061, p_date = .141, p_country = .279 (abstract, Method ¶2, Results "Honest Nulls", Table none) | **None.** No WDI series, runner, hashes, or result JSON in the deposit. Self-reported `papers/.../code/results/verified_results_2026_11_25.json` (`exp1_wdi_bulge_arrival_tstar`) only. The committed bulge record `origin/research/bulge-arrival-2026-11-25` @ `1b91a71` and `e8-fisher-ri` §7 record `t*` as **NOT-ESTIMABLE** (`L_primary` sourced 0/8) | **UNRESOLVED** | Do not report Exp 1 as a result. Commit the WDI extract (5 indicators), runner, seeds, per-scheme permutations and JSON/hashes. The self-reported JSON is not evidence. A live-WDI `SE.PRM.DURS` pull *could* legitimately make `t*` estimable, but until deposited the claim cannot be cited. |
| A-08 | Conclusion: "Together, these nulls **prove** that aggregate grade-pooled WDI indicators lack the resolution to detect grade-specific exam bottlenecks" (Results "Honest Nulls"; abstract "prove too coarse") | same as A-07; committed record is NOT-ESTIMABLE for the target quantity | **UNRESOLVED** | Downgrade "prove" to "we could not detect"; a null on a partly non-estimable design cannot prove absence. Remove the claim from the abstract until the design is deposited and powered. |

### 2.3 Exp 3 — the 1,640-run gate-architecture / H2 experiment

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-09 | 1,640 matched runs; H2 fee×scarcity **+0.1086** (SE 0.0078; 95% CI [+0.0924, +0.1248]; p = 1.9e-11) on the multi-vacancy grid; quota −0.0145 [−0.0214, −0.0076] (abstract, Results ¶2, Table 2) | **None.** Only self-reported `verified_results_2026_11_25.json` (`exp3_tullock_contest_gate_h1_h2`). No runner/seeds/JSON, no pre-registration hash. | **UNRESOLVED** | Remove from abstract and Results until the runner, seed list, and result JSON are deposited with an engine commit that actually implements `contest`. |
| A-10 | Provenance: Exp 3 declared `base_commit = 68da16e` | The committed engine at `68da16e` had **no `contest` gate kind** (dispatch was `bar`/`quota` only; `RECONCILIATION.md`; `MISSING_ARTIFACTS.md`), so 1,640 contest runs cannot have come from the declared commit. The gate patch arrived later and is committed on this branch. | **UNRESOLVED** (unverifiable provenance) | Correct the declared engine commit to the patched engine hash; re-run. Until then the experiment has no verifiable provenance and the numbers are uncitable. |
| A-11 | H1 **+0.3430** (fee=0), Spearman −1.00; contest 2×2 +0.2013; contest-by-`vac0` inverted-U +0.0138 / +0.1865 / +0.2573 / −0.0232; Table 2 and Figure 2 | same self-reported JSON only | **UNRESOLVED** | Same as A-09. Note Table 2/Figure 2 cannot stand on a self-reported JSON. |
| A-12 | Central mechanism claim: fee abolition amplifies the Q5−Q1 gap **only under an endogenous Tullock contest gate**, not under quotas (abstract, intro contribution 2, Discussion) | same self-reported JSON; the archived GPU "contest surface" that this lineage drew on is **QUARANTINED** and its "100 % seat-expansion paradox" is **CONTRADICTED** (see X-05) | **UNRESOLVED** | Keep only as a pre-registered hypothesis. The repaired engine now has an exact-PL `contest` gate, so the experiment is re-runnable — but it has not been re-run, and arithmetic/lineage from the quarantined bundle cannot substitute. |

### 2.4 Exp 4 — Jacobian / micro-identifiability "theorem"

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-13 | Bray's seven aggregate targets contain two algebraic identities ⇒ **five independent aggregate moments**; 7-parameter Jacobian **rank 5/7, cond 1.09e13**; 10-parameter baseline **rank 5/10, cond 3.48e12** (Results "Structural Identifiability Theorem", Table 4) | **No code, model specification, or result JSON in the deposit.** The only related artifacts are the archived GPU ABC bundle (quarantined) and the quarantined `research/shadow-equations-review-2026-11-25` @ `264c059` | **UNRESOLVED** (specific numbers) | The specific ranks/condition numbers cannot be cited. Recompute from Paper A's own model; report rank of the actual moment map, not a condition number. |
| A-14 | The archived 10-parameter Bray ABC supports the claim (θ5 calibration; posterior spread; condition-number improvement) | `docs/audit/ABC_IDENTIFICATION_AUDIT.md`: 5 advertised moments have **rank 4/5 at 1,000/1,000 prior-box points** (left-null certificate ≤3.4e-16); 6 active parameters ⇒ **2-dimensional null space**; **44 distinct θ** reproduce the same moments (null motion 0.266, residual 1e-16); θ5 (`teacher_threshold`) never enters utilities/moments; δ is analytic = **−0.7537718023763802** | **CONTRADICTED** (as evidence) | Paper A must **not** cite the archived ABC outputs. State that the affiliated archived design is rank-deficient (4/5, 2-dim null, 44 in-box θ) and that this is exactly why an independent computation is required. |
| A-15 | Two null singular vectors "isolate `b_income` (loading −0.977) and `b_school_gap` (−0.959)" | No artifact. The independent null vectors on the affiliated 5-parameter design are `[−0.398, +0.238, +0.886, …]` (school-gap slope vs intercept) and `[−0.159, −0.967, +0.190, …]` (income slope vs intercept) — qualitatively consistent (income/school-gap slopes trade against intercepts) but the quoted loadings are not reproducible | **UNRESOLVED** | Do not quote the loadings; if retained, report the independent vectors with their model/design and note they are from a different design. |
| A-16 | Adding income micro-moments lifts rank to **6/7** (cond 3435.49); adding income + within-grade school-quality lifts to **full rank 7/7** (cond 43.81) ⇒ full identifiability | No Paper A artifact. Independent recomputation on the affiliated 6-active-parameter design: one income moment → rank 4/5 (null dim 1); **two moments → rank 5/5, null dim 0, cond ≈ 4.59 — local only**; unsubstituted 6/6. | **UNRESOLVED** (specific 6/7, 7/7) | Replace with the independent, design-specific result: two additional independent moments give **local rank 5/5** (substituted) / 6/6 (unsubstituted) for the affiliated synthetic design. Do not report 7/7 or the 43.81 condition number without Paper A's own computation. |
| A-17 | "proves a formal structural identifiability theorem" / "Achieving full structural identification" (abstract, contributions, Discussion "Two-Moment Data Blueprint") | `ABC_IDENTIFICATION_AUDIT.md` §3.6, §5: full-rank Jacobian at a point is **local** identification by the inverse-function theorem; no global injectivity is shown or claimed; the audit's recomputation is design-specific and synthetic | **CONTRADICTED** (as a status claim) | Delete "theorem", "proves", "full structural identification". Say: "a local Jacobian-rank computation on a synthetic design suggests that two additional moments would restore local rank; this is a hypothesis for survey design, not a proof." |
| A-18 | "posterior correlation condition number" 447.16 → 23.97 (7-param) → 8.05 (5-param) used as identification evidence (Results ¶1, Table 4 note) | `ABC_IDENTIFICATION_AUDIT.md` §3.1/§3.7 and ledger G-03: it is the eigenvalue ratio of the accepted-draw correlation matrix, **not** the moment-Jacobian; condition numbers change with scaling and do not change rank | **CONTRADICTED** | Delete from the identification argument. Keep only if relabelled as a descriptive MCMC/posterior diagnostic, never as identification evidence. |
| A-19 | "three exact linear collinearities" produce zero output difference; 7-parameter bijection; rejection-ABC acceptance 0.0063 % → 0.0192 %; fresh-seed failure 58/54/53 %; max\|z\| 1.1214 → 0.6091 (Results ¶1) | No artifact in the deposit (self-reported only). The collinearity/reparameterisation logic is plausible but unverified. | **UNRESOLVED** | Deposit the shadow-equations code/results (currently quarantined) or delete. Do not quote acceptance/failure rates without the runner and seeds. |
| A-20 | "structural identifiability" rests on the synthetic Bray DGP | `docs/audit/SYNTHETIC_DGP_VALIDATION.md`: the shipped population is degenerate — **G12×urban cell empty**, no school identifiers, i.i.d. `school_gap`; legacy Jacobian **rank 3/5** (min SV exactly 0). Corrected crossed design (32 schools, crossed cells, income–quality link) gives **rank 5/5 in 500/500 populations** (3 seed bands), recovery RMSE 0.04–0.13 vs legacy 0.58–0.64 | **CONTRADICTED** (legacy DGP as identification base) | Do not cite any legacy-DGP identification result. If the measurement proposal is retained, build it on a crossed grade×urban, school-identified design and say so. |

### 2.5 Exp 5 — fee-abolition simulator forecast

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-21 | Seven-horizon out-of-sample RMSE **5.13 / 4.68 pp** vs persistence **23.93 pp**; reduction **78.6 % / 80.5 %**; MAE 4.24 / 3.92 (abstract, Results, Table 1) | Only self-reported `verified_results_2026_11_25.json` (`exp5_out_of_sample_e8_shock`). No simulator code, calibration seeds, or raw outputs in the deposit. | **AUTHOR-REPORTED** | Commit the runner, seed pairs, raw output JSON, and engine commit. Re-run on the repaired engine (D2/D6 repairs change the path) before any "validation" language. |
| A-22 | On-impact predictions **+11.60 / +13.48 pp** bracket empirical +12.44; mid-horizon +21.39…+23.68 (abstract, Results, Table 1) | same self-reported JSON | **AUTHOR-REPORTED** | Same as A-21. The empirical +12.44 is verified (A-01); the bracketing is not. |
| A-23 | Calibration: `fee_public = 0.150` selected solely on pre-abolition GER **74.88 %** (10 seeds), **zero post-abolition fitting** (Method, Table 1 note) | No artifact for 74.88 %/fee calibration; the 74.88 figure appears only in the self-reported JSON. The procedure ("zero fitting") is a claim about code that is not deposited. | **AUTHOR-REPORTED** | Re-derive 74.88 % from the committed E8 panel and commit the calibration script + seeds. Until then, "strictly calibrated / zero post fitting" is an unverifiable procedure claim. |
| A-24 | Table 1 as a comparison of "Empirical E8" versus "out-of-sample mechanistic shock predictions", presented as validation | empirical column verified (A-01/A-02); simulation columns author-reported (A-21/A-22) | **AUTHOR-REPORTED** (table as a whole) | Split the table: empirical column labelled VERIFIED; simulation columns labelled AUTHOR-REPORTED / NOT REPRODUCED. Do not call the table a validation. |
| A-25 | Simulator "validates a mechanistic education-system simulator out-of-sample" (intro contribution 2, abstract) | no independent reproduction; repaired engine changes expected probabilities, seat denominators, RNG, and ledger | **CONTRADICTED** (as a status claim) | Downgrade "validates" to "illustrates under an unreproduced calibration"; the word "validate" requires a reproduction on the canonical repaired spec. |

### 2.6 Exit-reason decomposition and baseline mechanism claims

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-26 | Table 3: Q1 exit decomposition never/liquidity/choice/gate-fail; e.g. open_bar never 74.07 → 1.70, gate-fail 0.12 → 1.71; tight_sec_quota never 79.94 → 6.17, gate-fail 0.84 → 11.23 (Results, Table 3) | No runner/result artifact. Values exist only in the manuscript. | **AUTHOR-REPORTED** | Commit the 40 paired-seed run and raw `e.exits` extracts, or drop Table 3. Note the repaired engine changed exit accounting and seat denominators, so old values are not canonical. |
| A-27 | "roughly 70 % of poorest-quintile exits occur because households exhaust liquidity or never enter; fewer than 1 % from failing an examination gate" (Conceptual Framework ¶1) | No artifact | **AUTHOR-REPORTED** | Commit the baseline run; otherwise delete the specific percentages. |
| A-28 | Fee abolition collapses Q1 non-entry by 72–74 pp; tight quota gate-fail +10.39 pp (0.84 → 11.23); gap +8.82 pp vs +3.11 pp under open_bar (Results, Table 3) | No artifact | **AUTHOR-REPORTED** | Same as A-26. |
| A-29 | Engine limitation: `max_entry_age = 9`, zero repetition, GER capped near 98 % vs empirical 106.9 % (Results, Limitations) | `engine/eduengine/core.py:33` confirms `max_entry_age=9`; the 98 %/106.9 % simulation claim has no artifact | **AUTHOR-REPORTED** | Keep the parameter fact; drop or deposit the 98 % claim. |
| A-30 | Within-gate equifinality: 319,600 pairs, 176 collisions vs null mean 190.52, p = .838 (Results "Honest Nulls") | committed `research/records/2026-11-25-equifinality-phase/data/equifinality_null.json` @ `ab415f2` (`within_gate_combined`: 176, null mean 190.523, p = 0.8382; label "SIMULATION ONLY") | **AUTHOR-REPORTED** (matches committed record; not re-executed) | Cite the record and its SIMULATION-ONLY label. Do not use it to prove a general proposition about identification. |

### 2.7 Provenance and replication claims

| ID | Claim | Artifact | Status | Required change |
|---|---|---|---|---|
| A-31 | Author Note: "Open replication code, pre-registrations, and line-by-line audit logs are archived at TreyModels/atlas-of-education" | The paper's package contains the manuscript only. Exp 1/3/4/5 runners, seeds and result JSONs are **absent** (`MISSING_ARTIFACTS.md` is still accurate). The GPU bundle is quarantined; the ABC/DGP/E1-Q3 evidence is contradicted/unresolved. | **CONTRADICTED** | Either deposit the replication package or rewrite the Author Note to say what is and is not available. |
| A-32 | The archived GPU/ABC bundle can support the identifiability/micro-moment claims (declared evidence lineage) | `SCIENTIFIC_CLAIM_LEDGER.md` G-01…G-20: **14 CONTRADICTED**, 2 UNRESOLVED; only GPU-vs-CPU arithmetic is VALIDATED (G-16, arithmetic scope only). `ABC_IDENTIFICATION_AUDIT.md`; `SYNTHETIC_DGP_VALIDATION.md`. | **CONTRADICTED** | Do not cite any GPU-bundle output as calibration, 7-parameter identification, contest boundary map, or E1/Q3 reconstruction. |
| A-33 | E1/Q3 robustness inference (not present in the received manuscript but part of the declared replication bundle) | `docs/audit/BOOTSTRAP_REPORT.md`: pooled selftest size **0.996–1.000** under a zero-effect null (OVB); FE size 0.052–0.062; country-block permutation within-invariant (**6.66e-16**); replacement WCR size 0.025–0.042, cluster bootstrap 0.033–0.050 (coverage 0.95–0.97) | **CONTRADICTED** (any such claim) | The received manuscript makes no E1/Q3 claim — keep it that way. If an earlier draft cited the pooled/bootstrap selftest, it is contradicted and must be removed. |

## 3. Status summary (Paper A)

| Status | Count | Claim IDs |
|---|---|---|
| VERIFIED EMPIRICAL | 4 | A-01, A-02, A-03, A-04 |
| REPRODUCED SIMULATION | 0 | — |
| VALIDATED SIMULATION | 0 | — |
| AUTHOR-REPORTED | 9 | A-21, A-22, A-23, A-24, A-26, A-27, A-28, A-29, A-30 |
| CONTRADICTED | 10 | A-05, A-06, A-14, A-17, A-18, A-20, A-25, A-31, A-32, A-33 |
| UNRESOLVED | 10 | A-07, A-08, A-09, A-10, A-11, A-12, A-13, A-15, A-16, A-19 |

*(33 adjudicated rows: A-01 … A-33. A-33 is a quarantine note for a claim that is not in the received
manuscript but is part of the declared replication bundle; it is included so the quarantine is explicit.)*

## 4. What survives, what must be done before any resubmission

### Survives (citable)

1. **E8 descriptive empirical block**: +12.44 pp impact, +25.26 pp post mean, full event path, Fisher-RI p-values,
   and the pre-registered gender non-detection. Label it association, cite the committed record and its
   reproduction gate, and keep the causal caveat.
2. **The corrected-identifiability negative finding** (new, and useful): the archived ABC is not identified
   (rank 4/5, 2-dim null, 44 in-box θ, analytic δ), the legacy DGP is degenerate (3/5), and a corrected crossed
   design reaches 5/5 in 500/500 populations. This is an audit result, not a paper result; Paper A may cite it only
   as an independent, design-specific recomputation with its caveats.

### Must be removed or relabelled

* "theorem"/"proves"/"full structural identification" and all rank 7/7 / condition-number claims (A-13…A-19).
* The entire Exp 3 result block and Table 2/Figure 2 (A-09…A-12), until deposited and re-run.
* The Exp 1 `t*` analysis and its "prove too coarse" conclusion (A-07, A-08).
* Exp 5 RMSE/forecast numbers, Table 1 simulation columns, Table 3, and the 70 %/<1 % baseline claims
  (A-21…A-28) until the runner and seeds are committed and the run is repeated on the canonical repaired spec.
* "flat pre-trends", "clean −6-year placebo", "robust to inverse-variance weighting", "lifting boys and girls
  alike" (A-05, A-06).
* The Author Note replication claim (A-31).

### Unresolved tasks (must be completed, not asserted)

| # | Task | Owner | Blocks |
|---|---|---|---|
| 1 | Deposit Exp 3 runner + seed list + result JSON with the **patched** engine commit; re-run on the repaired engine | author/engine | A-09…A-12 |
| 2 | Deposit Exp 1 WDI extract (5 indicators), runner, hashes, per-scheme permutations | author | A-07, A-08 |
| 3 | Deposit Exp 4 code + own-model specification; recompute the Jacobian independently; never cite the archived ABC | author/contest-math | A-13…A-20 |
| 4 | Deposit Exp 5 runner + calibration script + raw outputs; re-run on the canonical repaired spec | author/engine | A-21…A-25 |
| 5 | Deposit exit-reason run/raw extracts (Table 3) | author/engine | A-26…A-28 |
| 6 | Replace the "replication package" note with an accurate inventory | author | A-31 |

## 5. Bottom-line recommendation to the programme

Paper A should be **split**:

* **Paper A1 (publishable):** the E8 fee-abolition event study with Fisher-RI and the gender analysis. Descriptive,
  association-only, with the full lead vector and the near-boundary gender caveat. This is real work.
* **Paper A2 (working paper / pre-registration, not a theorem):** the two-moment measurement proposal, presented as
  a conjecture, with the independent local-rank recomputation as a design-specific appendix and the corrected DGP
  design. Remove "theorem", "proves", "7/7", and the archived ABC provenance.
* **Delete or park** the Tullock H2 experiment and the simulator forecast until deposited and re-run.

The current combined manuscript is **not publishable** in its present form.
