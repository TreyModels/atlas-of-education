# M4 — pre-registered `SurveyType == "DHS"` robustness check, now computed (2026-11-25)

**Status: computed and recorded; ADDITIVE.** This file closes a pre-declared check that had never been run.
It does **not** change any committed number, table or D3/D4 verdict in this record. Unit: country × survey ×
education published cell — **OBSERVED / ECOLOGICAL**, association only, **not causal**, **not** the individual
(IR) test. No microdata is involved.

---

## 1. What was pre-registered

- `PRE_REGISTRATION.md` line 147: **M4 = "M1 restricted to `SurveyType == "DHS"`" — survey-type robustness.**
- Lines 107–108: "**No MIS/AIS exclusion by default:** the API mixes survey types. The main specification pools
  whatever exists and a pre-declared robustness split by `SurveyType == "DHS"` is reported."

So the main Q1 models are *supposed* to pool DHS + MIS + AIS, and M4 is the *declared* DHS-only contrast.

## 2. Why it had not been computed (gap, stated plainly)

`scripts/estimate.py` pools whatever survey types the committed panels contain — by pre-registration — and has
no branch that restricts to `SurveyType == "DHS"`. The committed panels do contain non-DHS cells:

| panel | DHS | MIS | AIS | cells | non-DHS excluded by M4 |
|---|---|---|---|---|---|
| `panel_edu4_FE_FRTY_W_MNC` (Q1 completed fertility) | 784 | 72 | 4 | 860 | **76** |
| `panel_edu4_FE_FRTR_W_TFR` (period TFR) | 1,128 | 156 | 12 | 1,296 | 168 |
| `panel_survey` (survey-level panel) | 323 | 40 | 6 | 369 | 46 |

No M4 row exists in `results/results.json`, `results/model_table.csv` or `results/africa11/results.json`
(0 GFR/M4-restricted rows). The pre-declared split was therefore **not computed**, not simply missing from the
report.

## 3. How and where it was computed

- Script: `scripts/m4_surveytype_check.py` (analysis-side, imports the committed `estimate.py` estimator; does
  **not** modify it). It (a) recounts `survey_type` straight from the committed panel CSV **independently** of
  the loader, (b) asserts 8 conditions (known type values only; both DHS and non-DHS present; loader recount
  equals CSV recount; DHS-only subset exactly `DHS`; non-DHS excluded; restriction non-vacuous; model
  estimated), and (c) estimates DHS-only M1 next to the pooled M1.
- Run recipe: `/Users/treymenefee/neon-boot/patches/dhs_patched_rerun.sh` (host-side orchestrator; audited
  code, deterministic env `OMP/MKL/OPENBLAS/NUMEXPR/VECLIB=1`, `DHS_WORKERS=8`, box `python3.10.8`/`numpy 1.24.1`).
- Box path: `autodl-container-a8f742b5ee-292349c5`, `/root/work/dhs-api-patched-2026-11-25`.
- Output: **`results/m4_surveytype_check.json`** (sha256 `c6af0f8f2f059c8edc12ce1c2734305c48b9714eed2a0f341961b6bd08e67877`).
- Run verification: `results/VERIFICATION.json` → **PASS_BYTE_IDENTICAL** — all 13 committed corrected output
  files byte-identical, 27/27 numeric anchors, script hashes match. The M4 check's own `passed` = `true`,
  assertions 8/8.

## 4. Result (weighted M1; children per woman, published-cell coefficients)

**Full sample** (M1 = education + country/survey-year FE; cluster-robust by country):

| coefficient | pooled M1 (committed, n=860 cells / 215 surveys / 65 countries) | **M4 DHS-only** (n=784 / 196 / 65) | Δ (M4 − pooled) |
|---|---|---|---|
| primary vs none | −0.554089 | **−0.553734** | +0.000355 |
| secondary vs none | −1.583724 | **−1.574933** | +0.008791 |
| higher vs none | −2.538164 | **−2.524109** | +0.014055 |
| 2-group (secondary+ vs none/primary) | −1.551392 (n=692/346/80) | **−1.537931** (n=598/299/80) | +0.013461 |

**Africa-11** (same estimator, `--countries` subset):

| coefficient | pooled M1 (n=176 / 44 / 11) | **M4 DHS-only** (n=140 / 35 / 11) | Δ |
|---|---|---|---|
| primary | −0.707025 | **−0.713919** | −0.006894 |
| secondary | −2.162678 | **−2.191961** | −0.029283 |
| higher | −3.197672 | **−3.205615** | −0.007943 |
| 2-group | −1.974325 (n=144/72/11) | −1.988742 (n=110/55/11) | −0.014417 |

## 5. Reading (pre-declared robustness, not a new claim)

The DHS-only restriction moves the full-sample coefficients by **≤ 0.014 children** and the Africa-11 ones by
**≤ 0.030**; the sign, the ordering (none > primary > secondary > higher in magnitude of the negative gap) and
the headline conclusion **do not change**. Under the pre-registered M4 split, the completed-fertility education
gradient is therefore not an artefact of pooling MIS/AIS cells. Excluding MIS/AIS reduces the sample (76/860
cells, 196/215 surveys) but not the direction of the association.

Boundaries: this is a survey-type robustness contrast on published DHS API cells; it says nothing about
individual women, cannot be read causally, and does not touch the IR pre-registration. The main Q1
specification remains the pooled one, as pre-registered.
