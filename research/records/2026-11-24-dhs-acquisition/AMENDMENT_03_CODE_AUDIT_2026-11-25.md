# AMENDMENT 03 — code audit fixes to `ir_pipeline.py` (2026-11-25), before any DHS microdata

**Status:** code + documentation only. **No DHS microdata has been seen** (the box holds none: no file >10 MB;
`/root/work/dhs_ir` does not exist). Nothing in this file is a result. All processing language is associational.

**Code change:** Neon's audited `ir_pipeline.py` patch applied to
[`scripts/ir_pipeline.py`](scripts/ir_pipeline.py) on branch `research/dhs-ir-pipeline-neon-2026-11-25`
(base `f4a7f65` = head of `research/dhs-acquisition-2026-11-24`). The patch is additive (no deletions, no
push). Post-image blob hash `44da8a32…`; file sha256 `68cccaa1…`.

**Audit citation.** Patch submitted by Neon as `~/neon-boot/patches/dhs_ir_pipeline_neon.diff`; independent
verifier verdict: **APPLIES** with `git apply --recount` (plain apply fails "corrupt at line 179" because the
pasted patch drops its final context line; post-image blob equals Neon's `44da8a3`, content identical) and
**11/11 claims re-derived**. This amendment adds an independent 8/8 re-derivation on synthetic fixtures
(method below) and records the code-test values that differ from the base commit.

---

## 1. What the patch changes, and the measured base-vs-patched behaviour

Synthetic fixtures only: hand-made numpy/pandas rows to exercise the estimator; they imitate no DHS record
and say nothing about the research question.

| # | Area | Base `f4a7f65` behaviour | Patched behaviour (measured) | Prereg status |
|---|---|---|---|---|
| 1 | `filter_manifest()` (new) | `--countries` filtered ISO3 only; all 92 manifest rows requested if files supplied | strict `survey_type == "DHS"`: **92 → 72** rows; drops **20** (13 MIS + 7 AIS); keeps **14/14** countries | **aligns** with §2 "standard-DHS IR rounds only in the main analysis — 72 files" |
| 2 | survey weights (`woman_frame`) | `v005/1e6` raw; pooled sum = raw total (fixture: 120.0) | normalised **per survey**, each survey sums to **1.000000** (fixture: 1.0; 1.0); non-positive/non-finite → NaN | **aligns** with §4.1 "renormalised so each survey round has equal total weight" |
| 3 | M2 wealth `v190` | out-of-range/NaN compared with `==` → **False = 0 = reference (Q1)**, row kept (fixture M2 n=300) | NaN stays **NaN** and the row drops from M2 (fixture **n=270/300**); beta identical to a pre-filtered fit (**max abs Δβ = 0.0**) | clarification: v190 NaN is now listwise-dropped in M2, never silently coded Q1 |
| 4 | fieldwork CMC check | `y*12+m` (2020-06 → 24246) → **100.0% outside window** on a correct file | `(y−1900)*12+m` → **1446**; 0 in-window warnings; 1 out-of-window warning when one row is 5 months early (2.5%) | bug fix |
| 5 | region FE | `country_region` (fixture: 3 levels `ZZ_1..ZZ_3`) | **round_region**, 6 levels `S1_1..S1_3,S2_1..S2_3`, zero country_region | **aligns** with §4.1 `φ_{r,region}` (region × round). The base code was finer than the prereg |
| 6 | cluster SEs | per-cluster loop; **no CR1** factor | vectorised CR1; equals a reference loop to **max abs ΔSE = 1.4e-17**; SE ratio to base = √(G/(G−1)) exactly | implementation detail of "cluster-robust SEs" |
| 7 | CONSTRUCT block | stacked z(O1)/z(O2); **cluster on woman**; no region FE; `mean/std` | adds **round_region FE**, clusters on **PSU**; `nanmean/nanstd`; 8 terms equal an independently built round_region-FE + PSU-clustered fit to **max abs Δb = 0.0, ΔSE = 0.0**; note string "cluster = psu; rows = 2x women" | **DEVIATION — see §2** |
| 8 | `--selftest` | passes (`51 coefficient rows`) | passes (`estimator ran: 51 coefficient rows`; `SELFTEST OK`) | code test only, never evidence |

Reproduction: harness `~/neon-boot/dhs-verify/claims_2026-11-25/verify_claims.py` (8/8 checks reproduced);
the machine-readable result is committed at [`data/ir_pipeline_claims_audit_2026-11-25.json`](data/ir_pipeline_claims_audit_2026-11-25.json). It loads the patched file and the base file
(`git show f4a7f65:…/ir_pipeline.py`) and compares them on the fixtures above.

---

## 2. Pre-registration deviation: CONSTRUCT clustering, woman → PSU

**What the pre-registration says.** `PRE_REGISTRATION.md` §4.3: the construct test stacks O1/O2 (two rows per
woman) and is estimated "with cluster-robust SEs **on the woman** (the two rows are the same person)".

**What the patched code does.** `run_models()` now calls
`wls_absorbed(y, X, fe, w, ps)` with `ps` = the **PSU** id (`survey_id_v021`) repeated for both rows, not the
woman index. The note written into `estimates.csv` is `"cluster = psu; rows = 2x women"`.

**Why PSU is defensible (stated, not assumed).**
1. **It nests the woman pairing.** Both rows of a woman are in the same PSU, so PSU clustering does not discard
   the within-woman dependence that §4.3 was protecting — it retains it *and* adds the within-PSU dependence
   that woman-clustering ignores.
2. **It matches the rest of the pre-registered ladder.** §4.1 already specifies "clustered on `v021` (PSU)" for
   M0–M4; using woman-level clustering only inside CONSTRUCT was an internal inconsistency, not a prereg
   design feature.
3. **DHS design-based inference is PSU-level.** Women are sampled within PSU; ignoring that nests the SEs too
   small relative to the survey design (the same reason `svyset` takes `v021`).

**It is nevertheless a deviation from §4.3 as written** — defensible ≠ silently fine. Consequences and
planned reporting:
- PSU-clustered SEs will generally be **larger** than the §4.3 woman-clustered SEs; the construct decision
  (sign and CI of the standardised β3) is unchanged in point estimate but may change in width.
- When IR data arrive, report the 8 CONSTRUCT terms **both** PSU-clustered (primary, consistent with M0–M4)
  **and** woman-clustered (§4.3 exactly as written, sensitivity), declared **before** the data are opened and
  never chosen after seeing results. If the two disagree on the construct verdict, that disagreement is the
  finding and both are reported.
- Nothing is retro-fitted: this log is written **before** any microdata exists.

**Related less-interpretive deviations, for completeness.** (i) `v190` NaN rows are dropped from M2 rather
than coded Q1 (clarification). (ii) CR1 uses the standard `G/(G−1)` finite-sample factor, unspecified by the
prereg (implementation detail). Neither changes the preregistered model list M0–M4.

---

## 3. Stale-record reconciliation (what contradicts the patched code)

There is **no `results/` directory and no `REPORT.md` in this record**, so no committed estimate, table or
reported number depends on the old code. `data/ceb_education_cells.csv` is a public-DHS-API cell extract
(source log in `data/source_log.txt`), not pipeline output, and is unaffected.

Two descriptive rows *did* describe the old implementation and are corrected here (code descriptions, not
pre-registration text):
- [`EXECUTION_READY.md`](EXECUTION_READY.md) §4 mapping row "Region × round FE … adds `country_region`" →
  `round_region`; row "Construct test … cluster by **woman**" → cluster by **PSU**, pointing at this file.
- [`ACQUISITION_PLAN.md`](ACQUISITION_PLAN.md) §4.3 "with the woman as the clustering unit" → annotated with
  the 2026-11-25 code amendment.

Everything else checked and **consistent** with the patched code: the manifest's 72 standard-DHS / 20 MIS-AIS
split (README, §2), the `v005/1e6` weight convention, the region × round FE definition, and the M0–M4 ladder.

**Pre-registered M4 note (other record).** The `SurveyType == "DHS"` robustness model is pre-registered in
`research/records/2026-11-24-dhs-api-ecological/PRE_REGISTRATION.md` (line 147), not in this IR record. It was
not previously computed explicitly; the patched re-run recipe makes it explicit and records
`results/m4_surveytype_check.json`. Pointer:
`research/records/2026-11-24-dhs-api-ecological/M4_SURVEYTYPE_CHECK_2026-11-25.md`.

---

## 4. Reproducibility and boundaries

- Patch: `git apply --recount ~/neon-boot/patches/dhs_ir_pipeline_neon.diff` on top of `f4a7f65`; blob
  post-image `44da8a32…`. Never edited to make a test pass.
- Claims re-derived on synthetic fixtures (8/8); the full claim list and measured values are in §1.
- The only use of hand-made rows is code testing ("CODE TEST ONLY — NOT EVIDENCE"); they are not a simulation
  of the research question and must never be reported as a result.
- No microdata was read, copied or synthesised. No causal claim is made or supported by anything here.
