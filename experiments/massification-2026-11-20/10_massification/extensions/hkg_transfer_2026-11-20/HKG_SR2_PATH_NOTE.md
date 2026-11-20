# HKG SR-2 PATH STATUS NOTE (Lead, cycle 13, D110/D111)
<!-- Status note only. The frozen predeclaration HKG_TRANSFER_PRE_DECLARATIONS.md (sha256 99be01d7...) is NOT edited. -->

## SR-2 path correction

`HKG_CHECKLIST.md` §0 tests the v1.2 precondition by looking in `synthetic_2026-11-20/v1_2/`, which holds only
`PRE_DECLARATIONS.md`. The **delivered** v1.2 artifacts are in **`synthetic_2026-11-20/generator_v1_2/`**:
`code/sim_v1_2.py`, `PARAMS.md`, `results/reproduction_checks_v1_2.csv` (+ detail, FINDINGS, TUNE_LOG, RUN_MANIFEST).
The NER object required by SR-1 is delivered by `synthetic_2026-11-20/generator_v1_2_addendum/` (W4; predecl sha256
`aa756f8b…`): `ner_L = 100 × admitted_official_L / cohort_L`, a **cohort-flow NER analogue**, not the UIS stock NER.

## SR-2 status: PASS-CONDITIONAL (D110/D111 H3)

v1.2 checks **A–E PASS CONDITIONAL** — `m = 1.10` is a declared convention with an admissible window ≈ 1.09–1.11
(m = 1.05 → primary 2022 FAIL; m = 1.12 → upper 78.03 FAIL); parameters calibrated in the design phase; the
upper-secondary ceiling is demand/quality-driven (flat-cohort 2024 = 73.2, never ≥ 90). **No HKG file may say "v1.2
passes".**

## SR-9 status: AUTHORISE-WITH-CONDITIONS (D111 H1–H6)

Execution is gated on **H1 construct equivalence** (EXP-3 M1-NER: |stock − flow| ≤ 2.0 pp in every year where the
analogue ∈ [85,95], and implied first-sustained 5-year crossing years differing by ≤ 1 y). Until H1 clears, the HKG
run is `BLOCKED-MEASURE(SR-1)` and this authorisation is void for that object. H2 requires the v1.2.1 addendum to be a
delivered artifact with SHA256SUMS; H4 requires declared D7–D9 values pre-tabulated (sources or DECLARED rationales,
not referencing 1974/1979) and hashed before the run; H5–H6 restate the D75 constraints, the scaling-FAIL banner and the
closed verdict set (`TRANSFER-HOLDS` / `TRANSFER-FAILS` / `FAIL-RE-FIT` / `BLOCKED-*`; never PASS; DIAGNOSTIC-TRANSFER
only).
