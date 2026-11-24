# SUPERSESSION — 25 Nov 2026

**Authoritative corrected record: `research/dhs-corrected-2026-11-25` @ `22de735`**
(`CORRECTED_RUN_2026-11-25.md`, `results/`, `results/full_corrected/`, `results/africa11_corrected/`).

This branch (`research/dhs-api-ecological-2026-11-24`) is the **code chain** (estimator, `ir_pipeline`,
reduction tooling) and the original run. Its `REPORT.md` numbers predate the correction; every quoted
`−0.0775` has been annotated inline as superseded.

## What changed and why

| quantity | original (this report) | corrected (authoritative) | cause |
|---|---|---|---|
| D4 C_vs_B (wanted vs actual), secondary × construct | **−0.0775 (SE 0.0217)** | **−0.1962 (SE 0.0495)** | **interaction-set change**: `stacked()` now carries the full construct×schooling set (higher×cohort + pri/hi interactions); the original used a single secondary interaction |
| D4 A_vs_B | +0.016 (SE 0.041) | **+0.0711** | same interaction-set change |
| higher × cohort | not reported | **+0.1804 (p = 0.030)** | previously omitted term |
| Q2a / Africa-11 ratio CIs | [1.014, 1.380] (4-level) | bootstrap multiplicities corrected | **multiplicity fix = CIs only**; point estimates unchanged by it |
| Africa-11 2-group ratio CI | [1.011, 1.135] | **[0.9987, 1.1403]** (now includes 1.0) | multiplicity fix |

**A bootstrap-multiplicity fix cannot move a point estimate.** The −0.0775 → −0.1962 move is entirely
the interaction set. Neon's bootstrap-only diff applied to the DHS base gives ≈ −0.0775 with corrected
CIs, **not** −0.1962, unless the diff also carries the interaction hunk.

This was the *predicted* correction: `MIGRATION_2026-11-25.md` quarantine item 1 (on
`research/handoff-2026-11-24`) says "`stacked()` omits higher×con and pri/hi interactions; corrected D4
secondary gap ≈ −0.1962". The corrected run reproduces that prediction.

## Evidence chain
- Patched DHS re-run (Neon `ir_pipeline` post-image + `estimate.py`/`corrected_reduction.py` @ `45b974e`):
  **PASS_BYTE_IDENTICAL** — 13/13 output files byte-identical to the committed corrected run, 27/27
  numeric anchors, `ir_pipeline --selftest` 51 rows, pre-registered M4 (`SurveyType == "DHS"`) passed
  (76 non-DHS cells excluded). Artefacts: `research/box-runs-2026-11-25` @ `0fd9928`,
  `research/records/2026-11-25-box-runs/dhs-patched-verify/`.
- Independent reproduction of every quoted corrected number to ~1e-9 by the verifier lane.

## Status of uncomputed references
`FE_FRTR_W_GFR` was **never estimated** — no computed value exists (0 rows in `model_table`,
`results`, `africa11`). References were removed/marked in the 25 Nov pass. Do not cite a GFR number
from this record.

SIMULATION does not apply here: these are observational reduced-form estimates on DHS panels; no causal
language is intended beyond the stated specification.
