# EXECUTION_READY — the individual IR test, ready to run the day access arrives

**Purpose:** part 3 of task-36. The pre-registration exists ([`PRE_REGISTRATION.md`](PRE_REGISTRATION.md),
committed **before** any data) and the access path is being acquired in two requests
([`application/NEXT_ACTION_2026-11-24.md`](application/NEXT_ACTION_2026-11-24.md)). This file is the operational
layer: what exactly runs, on which files and variables, in what order, and what is gated. **No DHS microdata has
been seen; nothing here is a result.**
**Status:** ready. Pre-registration `PRE_REGISTRATION.md`; coverage rules
[`AMENDMENT_02_ACCESS_COVERAGE.md`](AMENDMENT_02_ACCESS_COVERAGE.md); pipeline
[`scripts/ir_pipeline.py`](scripts/ir_pipeline.py) (syntax + self-test passed on hand-made rows — a **code test
only, not evidence**).

---

## 1. What is ready, and what is not

| Component | State |
|---|---|
| Question, samples S-A…S-E, models M0–M4, construct split, D1–D3 decision rules, limits | **fixed in advance** (`PRE_REGISTRATION.md`, commit before data) |
| Coverage tiering under partial approval (T0–T4) | **fixed in advance** (`AMENDMENT_02_ACCESS_COVERAGE.md`) |
| File inventory: 92 IR Stata files, 14 countries, expected N / fieldwork / universe per file | [`data/dhs_ir_inventory_targets.csv`](data/dhs_ir_inventory_targets.csv) (public API metadata) |
| Verification gate (variables, identities, weights, CMC/age, clusters, fieldwork) | implemented in `scripts/ir_pipeline.py --check-only`; stops on failure |
| Estimator (M0–M4, dose, construct split; cohort FE + round FE, weights, PSU-clustered SEs) | implemented and code-tested |
| O3 survey-period TFR | **needs BR (Births Recode) files** — operational correction in `AMENDMENT_02` A2.4; not computed from IR alone |
| Data | **not obtained** (two requests; Asian pending, African not yet submitted) |

---

## 2. Files expected (what "access arrives" means)

Per the manifest, 92 IR Stata ZIPs (`??IR??DT.ZIP`) for the 14 countries, ~538 MB; **Tier 1 = 69 standard-DHS IR
files, 493.6 MB**. For O3 only, optionally the matching **BR** files (`??BR??DT.ZIP`) for the same rounds.
MIS/AIS IR files are Tier 3 robustness and enter only if `v133`, `v206`, `v207` are verified present.

Expected per-file checks are in the manifest (`women_unweighted`, `sample_points`, `fieldwork_start/end`,
`universe_of_women`). Example magnitudes: Malawi 2015-16 ≈ 24,562 women; Ethiopia 2016 ≈ 15,625; Kenya 2022 ≈
32,156; Eswatini 2006 ≈ 4,987; the two Vietnam rounds are **ever-married** universes (comparability flag).

---

## 3. Commands (copy-paste; run on the secure data host, never on the Mac)

```bash
# 0) environment: pandas is needed only to read .dta
python3 -m pip install --user pandas        # or use the conda env on the server

# 1) unpack the ZIPs OUTSIDE the repo (the .dta files stay in a private directory)
mkdir -p /secure/dhs_ir && cd /secure/dhs_ir && for z in /secure/dhs_zips/*.zip; do unzip -o "$z"; done

# 2) verification gate ONLY (writes verification.json and stops; no model is run)
python3 scripts/ir_pipeline.py --datadir /secure/dhs_ir \
        --outdir /secure/dhs_out --check-only

# 3) full pre-registered run (only if step 2 reports 0 failures)
python3 scripts/ir_pipeline.py --datadir /secure/dhs_ir \
        --outdir /secure/dhs_out

# 3b) coverage-restricted run, e.g. if only the 11 African countries are approved (tier T1)
python3 scripts/ir_pipeline.py --datadir /secure/dhs_ir --outdir /secure/dhs_out \
        --countries MWI,ETH,UGA,LSO,TZA,KEN,MOZ,GHA,BEN,NAM,SWZ

# 3c) optional O3: pass BR files (the pipeline currently reports O3 as "requires BR"; extend with --br-datadir)
```

Outputs (outside the repo): `verification.json`, `estimates.csv`, `summary.json`. Only **aggregate** results may
be copied into the record; microdata and any cell small enough to identify a woman must not be.

---

## 4. Mapping: pre-registration → code

| Pre-registration element | Implementation in `ir_pipeline.py` |
|---|---|
| Universe: women 40–49 (S-A), 35–49 (S-B), 25–49 (S-C) | `age >= 40 & age <= 49` (S-A); flags for the others are the same filter with wider windows |
| O1 births = `v201`; O2 surviving = `v201 − v206 − v207` | `woman_frame()` → `births`, `surviving`; **O2 never called TFR** |
| O3 period TFR | **not computed from IR**; requires BR files (AMENDMENT_02 A2.4) |
| Exposure `v106` (4 categories, ref none); dose `v133` | `design(dose=False/True)`; `M1_dose` row in `estimates.csv` |
| Cohort = 5-year birth-year bins from `v011` | `cohort5` in `woman_frame()` |
| Round FE = survey id; country FE | absorbed via alternating projections (`absorb`) |
| Region × round FE; urban control (M1) | `fe_list_for()` adds country_region; `design()` adds `v025` |
| Wealth control (M2, mediator) | `v190` quintile dummies in M2 |
| Education × cohort (M3); education × round (M4) | interaction blocks in `design()` |
| Survey weights `v005/1e6`; PSU clusters `v021` (nested in round) | `w`, `psu = survey_id_v021`; cluster-robust sandwich |
| Construct test: stack O1/O2, standardise, construct × education, cluster by **woman** | `CONSTRUCT` block in `run_models()` |
| Verification gate (ACQUISITION_PLAN §7) | `check_file()` — the checks listed there, automated |
| Decision rules D1–D3 | applied by the analyst to `estimates.csv`; thresholds are in the pre-registration, not in code (deliberate: no auto-p-hacking) |
| Heterogeneity shares, BH | per-round/ per-country tables are produced in the analysis notebook from `verify` + raw files; BH computed by hand from the recorded p-values |

**Deliberate omissions in code:** no automatic model selection, no stepwise controls, no threshold search, no
automatic "significant/not" labels. The code returns coefficients, CIs and n; the decision rules are applied in
the report, so a reader can check them.

## 5. Order of operations when approval arrives (Day 0 → Day 3)

1. **Day 0:** record approval in `application/STATUS_LOG.md`; download Tier 1 IR files per `ACQUISITION_PLAN.md`
   §3; sha256 manifest; store outside the repo.
2. **Day 0–1:** run `--check-only`. Any structural failure → re-download that file; do **not** patch. Record the
   failures in `VERIFICATION.md`.
3. **Day 1:** run the full pipeline (or the T1 subset if only one request is approved); write `REPORT.md` with
   D1–D3 verdicts, the heterogeneity shares, and the construct result.
4. **Day 2–3:** independent check of one country-round against the published DHS tables (weights/education
   distribution); confirm the construct naming in every table; submit the record; send any publication to
   `references@dhsprogram.com` when written.
5. If partial approval: run only the tier allowed by `AMENDMENT_02`; label the coverage in the same sentence as
   the headline number; never present a T1/T2 run as the pre-registered main test.

## 6. Threats already fixed in advance

- **No microdata in the repo** (public repo; DHS Terms forbid redistribution, including dashboards).
- **No synthetic substitution**: the only use of hand-made rows is the `--selftest` code check, which prints
  "CODE TEST ONLY — NOT EVIDENCE" and is never reported as a result.
- **No causal language**: the pre-registration fixes the wording ("association", "consistent with").
- **Construct discipline**: O2 is "surviving children per woman (cumulative, individual)", never "TFR"; O1 is
  "births per woman (cumulative, individual)", never a period rate; O3 (if computed) is the only rate.
- **Weights/SEs**: survey weights and PSU-clustered design-based SEs; unweighted analogues reported.
- **Cell floors**: cohort × education cells below the pre-declared floor are pooled to 10-year cohorts or
  secondary+; logged per cell, never chosen per result.
- **Coverage**: T0/T1/T2 labelling; extra Asian countries outside the pre-registration are not part of D1–D3.

## 7. What the analyst must still decide (and cannot pre-decide)

- Whether `v133` is usable in early rounds (country-specific `x`,`y` mappings; the `.DQC`/`.DCT` in each ZIP
  documents it) — the pipeline reports missing `v133` and the dose model is optional.
- Whether MIS/AIS rounds pass the variable checks (Tier 3 only).
- The exact BH family composition if a cell floor forces pooling — logged before estimation, once, for all
  countries.

## 8. Unverified / dependencies

- Access itself (pending; `application/NEXT_ACTION_2026-11-24.md`).
- `pandas` availability on the analysis host (installable; required only to read `.dta`).
- Whether the Stata IR files include `v023`/`v149` in every round (optional variables; code tolerates absence).
- The BR files' availability under the same country approval (needed only for O3).
