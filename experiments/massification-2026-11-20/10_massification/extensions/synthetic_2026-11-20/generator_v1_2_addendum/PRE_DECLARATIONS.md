# PRE-DECLARATIONS — v1.2 NER output addendum (interface object, no model change)

**Worker W4, 2026-11-20 (Asia/Shanghai). FROZEN BEFORE THE ADDENDUM RUN.**
**Scope:** `10_massification/extensions/synthetic_2026-11-20/generator_v1_2_addendum/` only.
**Parent object:** the frozen v1.2 generator at `../generator_v1_2/` (read-only here).
**LABEL: SYNTHETIC. The NER columns are DERIVED from model output. Nothing here is observed, estimated, fitted, forecast, or evidence about any country. No causal or direction claim.**

---

## 1. Why this addendum exists

The frozen v1.2 generator emits `ger`, `completion_cohort`, `completion_uis`, `survival`, `enrolment`,
`admitted_official`, `admitted_overage`, `out_of_school`, and related objects — but **no NER object**
(`generator_v1_2/PARAMS.md` §10: "No NER object"). The HKG transfer (worker W3) is therefore
`BLOCKED-MEASURE(SR-1)`: D75's timing target is a **primary NER** crossing (≥90 in 1974; ≥95 in 1979),
and a GER or completion crossing is not a permitted substitute.

This addendum adds an **NER output object at the panel interface**. It does **not** change the model:
it reads the already-delivered v1.2 panel and appends columns. No v1.2 parameter, equation, seed, or
input is touched, and no v1.2 file is edited. It is the kind of predeclared interface amendment described
in `HKG_INVENTORY.md` §9 option (a), **not** the in-run NER patch that `SR-1`/`SR-8` forbid.

---

## 2. NER definition and derivation (declared before the run)

For every panel row (country `c`, year `t`, level `L`):

```
ner_L(c,t) = 100 * admitted_official_L(c,t) / cohort_L(c,t)
```

where, in the frozen v1.2 quantities:

- `cohort_L(c,t)` is the model's **annual official-age cohort** for level `L`, i.e. the same `C_L(t)`
  used in the model's denominator for GER (`code/sim_v1_2.py:436`,
  `C = band_share * S / dur`; `PARAMS.md` §3). The generator writes it to the panel column `cohort`.
- `admitted_official_L(c,t)` is the model's **official-age admission** flow for level `L`
  (`code/sim_v1_2.py:588`, `adm_off = min(D_off, phys)`) and is written to the panel column
  `admitted_official`.
- `admitted_overage_L(c,t)` (`adm_oa`) is the separate over-age component and is **excluded** from
  the numerator. The model's rationing rule admits official-age children first and over-age children
  only from residual capacity (`code/sim_v1_2.py:588–589`); `oa_rate` is the declared over-age
  applicant rate per cohort (`PARAMS.md` §4.1).

Thus the object is **not** "GER times an invented constant share". It is the model's own age split:
official-age admissions divided by the official-age cohort. Equivalently, in the model's own algebra,

```
GER = (admitted_official + admitted_overage) / cohort
NER = GER * admitted_official / (admitted_official + admitted_overage)
```

so the ratio `NER/GER` is the model-computed official-age share of admissions, not a declared constant.

### 2.1 Declared limitation: this is a cohort-flow NER, not the UIS stock NER

v1.2 is a one-year cohort-flow simulator. It carries an annual admission flow and an annual cohort, not
a multi-grade enrolment stock. The object above is therefore a **cohort-flow NER analogue**, internally
consistent with the model's own `ger` column (both have the same denominator). It is **not** the UIS
stock-based NER (`NER.1.cp`: enrolled children of official age across all grades ÷ official-age
population), because v1.2 does not carry that stock.

This limitation is declared here, before the run, and is not hidden: the addendum makes an NER object
**exist at the model interface**; it does not claim that the object is the UIS measure, and it does not
authorise the HKG transfer by itself. Any HKG run must separately declare whether this model-interface
NER is an admissible realisation of its TC-1/TC-2 measure; that is a Council/HKG-predeclaration question,
not one this addendum answers.

### 2.2 What was rejected

- **Not** `ner_declared = declared-share × GER`. The age composition *is* modelled (`demand_official` /
  `demand_overage`, `admitted_official` / `admitted_overage`, `oa_rate`), so a declared constant share
  would discard real model information and would be less honest.
- **Not** a GER or completion relabel. Those are the substitutions `SR-1`/`SR-8` bar.
- **Not** a stock reconstruction from admissions and survival. That would add a new model object, not
  just read the frozen panel, and would require undeclared progression assumptions.
- **Not** an edit to `sim_v1_2.py`, its parameters, or its results.

---

## 3. Exact panel columns used and output schema

### 3.1 Input

`../generator_v1_2/results/synthetic_panel_v1_2.csv` (frozen; 6 720 data rows + header; 67 columns).
Columns **read** by the addendum:

| column | use |
|---|---|
| `country`, `country_id`, `year`, `level` | row identity / smoke-test selection; copied unchanged |
| `cohort` | NER denominator (official-age annual cohort) |
| `admitted_official` | NER numerator (official-age admission) |
| `admitted_overage` | diagnostic only: confirms the age split; **not** in the numerator |
| `enrolment`, `ger` | consistency diagnostic: `NER ≤ GER` and `enrolment = admitted_official + admitted_overage` |
| `label` | must be `SYNTHETIC`; copied unchanged |

All 67 pre-existing columns are copied through **byte-for-byte, in the same order, with the same values**.
The addendum does not sort, filter, re-index, re-round, or rewrite them.

### 3.2 Output

`results/synthetic_panel_v1_2_ner.csv` — same 6 720 rows and 67 columns, plus:

| new column | content |
|---|---|
| `ner` | row-level NER in percent, `%.10g`, for the row's own level |
| `ner_basis` | `derived-from-age-structure` on every row |
| `ner_primary` | the row's NER if `level == primary`, else empty |
| `ner_lower_secondary` | the row's NER if `level == lower_secondary`, else empty |
| `ner_upper_secondary` | the row's NER if `level == upper_secondary`, else empty |
| `ner_tertiary` | the row's NER if `level == tertiary`, else empty |
| `ner_primary_basis` | `derived-from-age-structure` on primary rows, else empty |
| `ner_lower_secondary_basis` | same, lower-secondary rows |
| `ner_upper_secondary_basis` | same, upper-secondary rows |
| `ner_tertiary_basis` | same, tertiary rows |

Because the panel is long (one row per country-year-level), the level-named columns are populated only on
rows of that level; `ner` is the non-sparse row-level object. This preserves the input's row count and
long-panel structure exactly.

Formatting: all new numeric values are written at `%.10g` (the v1.2 float convention); empty means "not
applicable for this row's level", never zero. No `NaN`/`inf` strings are emitted; a non-positive
denominator would be an error (the frozen panel has none) and the addendum refuses to write in that case.

---

## 4. Declared assumptions

1. **A1 — `cohort` is the official-age annual cohort for the row's level.** This is the frozen v1.2
   definition (`PARAMS.md` §3, `C_L(t) = band_share_L · S(t) / dur_L`); `band_population = cohort × dur`
   is the multi-year official-age band. The model's own GER uses `cohort` in the denominator.
2. **A2 — `admitted_official` counts only official-age admissions.** The model computes official-age
   demand `D_off` and over-age demand `D_oa` separately, then fills official-age first
   (`code/sim_v1_2.py:567–568, 588–589`). `admitted_overage` is not included in the NER numerator.
3. **A3 — the flow is the model's "enrolment" for the level-year.** In v1.2, `enrolment =
   admitted_official + admitted_overage`; there is no separate stock. The NER object is therefore a
   cohort-flow object (see §2.1).
4. **A4 — no re-scaling, no cap.** NER is emitted as computed. In particular, tertiary NER can exceed
   100 because the tertiary pool can exceed the current annual cohort (`D_off` is bounded by
   `1.05 × C` at `code/sim_v1_2.py:575`); this is disclosed, not clipped. Primary/lower/upper NER are
   bounded above by 100 by construction because `D_off = demand_share × elig × C ≤ C`.
5. **A5 — no new randomness, no new parameters.** The addendum uses only arithmetic on frozen columns.
   It does not re-fit, re-calibrate, re-seed, or re-run the model.
6. **A6 — the frozen panel is the only input.** No observed NER, no external data, no web, no HKG series
   enters the computation. The object is DERIVED from the synthetic model, not observed.

---

## 5. Invariance requirement (must be demonstrated, not asserted)

Adding the output must not change the model's dynamics or the frozen v1.2 artifacts. Three checks:

**(a) Frozen generator reruns.** `python code/sim_v1_2.py` is run twice from `../generator_v1_2/`, each
time into a **separate output directory inside this addendum**, with `--manifest` also inside this
addendum. All three result CSVs from each run are compared **byte-for-byte (`cmp`)** with the delivered
`generator_v1_2/results/*.csv`, and the two reruns are compared with each other. The frozen generator
directory is not written to. `PYTHONDONTWRITEBYTECODE=1` / `-B` is used so no `__pycache__` is created
there.

**(b) Panel pass-through.** After `add_ner.py`, the output has exactly the same number of rows (6 720)
and the same row order; every one of the 67 pre-existing columns is identical string-for-string to the
input; only the appended columns differ. A machine-readable record is written to
`results/INVARIANCE_CHECKS.json`.

**(c) Addendum determinism.** Two runs of `add_ner.py` produce **byte-identical** output CSVs
(`sha256` equality, not merely equal values). The output contains no timestamp, hostname, path, process
id, elapsed time, or dict-order dependence.

If any check fails, the addendum reports the failure and does not claim an NER object.

---

## 6. HKG-readiness smoke test (predeclared rule; diagnostic only)

After the object exists, a small smoke test is run and written to `results/NER_SMOKE.csv`:

- **Country:** `SYN00_PHL_LIKE`. **Level:** `primary`. **Series:** `ner_primary` (equivalently `ner` on
  primary rows). **Years:** 1970–2025. **Label:** `SYNTHETIC`. **Provenance:** `DERIVED`.
- **Thresholds:** 90 and 95 (percent).
- **First-at-above:** the first year with `ner >= threshold`.
- **First-sustained crossing:** the first year `y` such that every year `y … y+4` has `ner >= threshold`
  (five consecutive years at or above), mirroring the on-disk crossing rule cited by the HKG
  predeclaration (`relations/data/UNIVERSALIZATION_TIMING.csv`: "observed first-sustained crossing
  (>=5 consecutive years above)"). If no such year exists by 2025, report `none_by_2025`.
- **Also reported:** number and percentage of years at or above the threshold; series minimum/maximum
  and their years; count of non-decreasing year steps; and a monotonicity note.

This is a **smoke test that an NER object now exists and that crossings are computable**, not a test of
HKG and not a verdict. There is **no comparison to HKG**, no use of the 1974/1979 targets, no tolerance,
no `TRANSFER-HOLDS`/`TRANSFER-FAILS` token, and no claim about any real country.

---

## 7. What this addendum does and does not license

**Does:**
- Make an NER-named object available at the v1.2 panel interface.
- State exactly how it is derived from the model's own age split, so a reader can audit it.
- Make a primary-NER crossing computable for the synthetic PHL-like country (smoke test).
- Preserve the frozen v1.2 dynamics and artifacts, demonstrated by the three invariance checks.

**Does not:**
- Change any v1.2 check, verdict, parameter, result, or file.
- Pass, fail, or pre-judge the HKG transfer; no HKG comparison is made.
- Turn the synthetic NER into an observed NER or evidence about the Philippines, Hong Kong, or any country.
- Establish that the model-interface cohort-flow NER is the UIS stock NER; §2.1 declares that it is not.
- Authorise an HKG run; `SR-1` is cleared only at the interface, and `SR-2`/`SR-9` remain outside this
  addendum's scope.

---

## 8. Freeze, hashes, determinism

- This file is frozen **before** `add_ner.py` is first run. Its sha256 is recorded in
  `RUN_MANIFEST.json` as `predeclaration_sha256`.
- `code/add_ner.py` and the input panel's sha256 are also recorded.
- All result files produced by the addendum are hashed in `RUN_MANIFEST.json`.
- Two runs must be byte-identical; the sha256 of each result file is recorded.
- The addendum refuses to run if the input panel's row count/schema is not the expected frozen schema
  (6 720 rows; 67 named columns; every `label == SYNTHETIC`), and it refuses if any pre-existing column
  would change.

---

## 9. No-causality / no-direction statement

Every output carries: **SYNTHETIC / DERIVED — not observed, not an estimate, not a forecast, not
evidence about any country; no causal or direction claim; no policy claim.** The NER object is a
deterministic transformation of a declared-assumption simulator's own output. It is reported because the
HKG interface lacks an NER object, not because any number in it describes the world.
