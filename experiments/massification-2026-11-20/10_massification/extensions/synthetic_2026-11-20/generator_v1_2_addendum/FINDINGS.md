# FINDINGS — v1.2 NER output addendum (interface object; no model change)

**LABEL: SYNTHETIC / DERIVED. Every number below is produced by a declared-assumption simulator and is a deterministic transformation of its output. Nothing here is observed, estimated, fitted, forecast, or evidence about any country. No causal or direction claim. No policy claim. No HKG comparison and no transfer verdict is made.**

Files: [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md) · [`code/add_ner.py`](code/add_ner.py) ·
[`results/synthetic_panel_v1_2_ner.csv`](results/synthetic_panel_v1_2_ner.csv) ·
[`results/NER_SMOKE.csv`](results/NER_SMOKE.csv) · [`results/INVARIANCE_CHECKS.json`](results/INVARIANCE_CHECKS.json) ·
[`results/INVARIANCE_RERUNS.json`](results/INVARIANCE_RERUNS.json) · [`RUN_MANIFEST.json`](RUN_MANIFEST.json)

---

## 1. What was added

The frozen v1.2 generator has no NER object (`generator_v1_2/PARAMS.md` §10: "No NER object"), so
the HKG transfer is `BLOCKED-MEASURE(SR-1)` at the model interface. This addendum reads the frozen
v1.2 panel and appends an NER object:

- 6 720 rows, unchanged; 67 pre-existing columns, unchanged and in the same order.
- 10 appended columns: `ner`, `ner_basis`, `ner_primary`, `ner_lower_secondary`,
  `ner_upper_secondary`, `ner_tertiary`, and `ner_primary_basis`, `ner_lower_secondary_basis`,
  `ner_upper_secondary_basis`, `ner_tertiary_basis`.
- Row-level `ner` is the NER for the row's own level; the level-named columns are populated only on
  rows of that level (the panel is long by country-year-level, so this keeps the row count and
  long-panel structure identical).
- `label` remains `SYNTHETIC` on every row; `ner_basis` is `derived-from-age-structure`.

**This is an output-interface addendum, not a model change.** No v1.2 parameter, equation, seed, input,
check, or result file was edited. The v1.2 directory was never written to.

---

## 2. Derivation (and why this derivation)

For every panel row (country `c`, year `t`, level `L`):

```
ner_L(c,t) = 100 * admitted_official_L(c,t) / cohort_L(c,t)
```

The two inputs are the model's own age-split quantities:

- `cohort` is the model's **annual official-age cohort** for the level, `C_L(t) = band_share_L · S(t) /
  dur_L` (`code/sim_v1_2.py:436`; `PARAMS.md` §3). It is the same denominator the model uses for `ger`.
- `admitted_official` is the model's **official-age admission** flow (`code/sim_v1_2.py:588`,
  `adm_off = min(D_off, phys)`). The model computes official-age demand and over-age demand separately
  (`code/sim_v1_2.py:567–568, 588–589`) and admits official-age children first. `admitted_overage` is
  **excluded** from the numerator.

Equivalently, in the model's algebra:

```
GER = (admitted_official + admitted_overage) / cohort
NER = GER * admitted_official / (admitted_official + admitted_overage)
```

The official share is computed by the model's age split, **not** a declared constant. This is why the
"declared-share × GER" fallback was not used: the model carries the age composition, so discarding it
would be less honest.

**Declared limitation (from `PRE_DECLARATIONS.md` §2.1).** v1.2 is a one-year cohort-flow simulator.
It carries an annual admission flow and an annual cohort, not a multi-grade enrolment stock. This is a
**cohort-flow NER analogue**, internally consistent with the model's `ger`, not the UIS stock-based NER
(`NER.1.cp`). It makes an NER object exist at the model interface; it does not by itself establish that
the object is the UIS measure or that an HKG run is admissible.

---

## 3. Invariance evidence (all three checks)

### (a) Frozen v1.2 generator reruns — PASS

`sim_v1_2.py` was run twice from `generator_v1_2/` into two separate directories inside this addendum,
with `PYTHONDONTWRITEBYTECODE=1` and `-B` so the frozen directory was not written. All three result CSVs
from each run were compared with `cmp` against the delivered `generator_v1_2/results/` files and with
each other.

| file | delivered sha256 | rerun A | rerun B | byte comparison |
|---|---|---|---|---|
| `synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` | same | same | **IDENTICAL** (delivered=A=B) |
| `reproduction_checks_v1_2.csv` | `72a17fb6dcf59db671bbbcdb04111560d1d1aee59791009111dc3861b3f0fba8` | same | same | **IDENTICAL** (delivered=A=B) |
| `reproduction_checks_detail_v1_2.csv` | `0597bafb8f8b90ad03a0164e9c2137cdaaff2186f1d7d0c5e5476462b285706b` | same | same | **IDENTICAL** (delivered=A=B) |

**Environment disclosure.** The delivered v1.2 manifest records Python 3.11.17 / NumPy 2.4.6. The
reruns available in this environment used Python 3.12.14 / NumPy 2.3.5. The three result CSVs are
nevertheless **byte-identical** to the delivered files; the rerun manifests differ from the delivered
manifest only in the recorded `python` and `numpy` fields. This is recorded in
`results/INVARIANCE_RERUNS.json`; no exact-version Python 3.11.17/NumPy 2.4.6 environment was available
to this worker.

### (b) Panel pass-through — PASS

`add_ner.py` re-reads its own output and checks, independently of the write:

- 6 720 rows in, 6 720 rows out; same row order and same `(country, country_id, year, level)` keys.
- All 67 pre-existing columns identical string-for-string; only the appended columns differ.
- Every row still has `label = SYNTHETIC`.
- `enrolment = admitted_official + admitted_overage` within `1e-6` relative display rounding; 0
  violations.
- `ner <= ger + 1e-6` (display rounding); 0 violations.
- No non-positive cohort, no negative admission, no `ner < 0`.
- Each row carries `ner` plus exactly one populated level-named NER column (the same value); the other level-named columns are empty.

The machine-readable record is `results/INVARIANCE_CHECKS.json`. Input panel sha256:
`14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac`; output panel sha256:
`c6d1f9b059b5a48cbd5a4aaf7e1c4611cad781819b74987988897e8d35e40294`.

### (c) Addendum determinism — PASS

Two clean runs of `add_ner.py` produced **byte-identical** files:

| file | sha256 (run 1 = run 2) |
|---|---|
| `synthetic_panel_v1_2_ner.csv` | `c6d1f9b059b5a48cbd5a4aaf7e1c4611cad781819b74987988897e8d35e40294` |
| `NER_SMOKE.csv` | `987f9200c5218f9417b6850e8f2b561e216e2665280bb7fc87826c3be5f803e4` |
| `INVARIANCE_CHECKS.json` | `ca41790cf4f6a4b3b8f8f7ae4a3a077b94f730c8e4c448f33b9d7a58b79eecb5` |

The output contains no timestamp, hostname, path, process id, elapsed time, or dict-order dependence.
The transient rerun directories were compared byte-for-byte and then removed to avoid duplicating the
frozen artifacts; the hashes above and in `results/INVARIANCE_RERUNS.json` are the record.

---

## 4. SYNTHETIC smoke test — primary NER crossings for `SYN00_PHL_LIKE`

**This is a smoke test only.** It checks that an NER object now exists and that a crossing is
computable. There is **no comparison to HKG**, no use of the HKG 1974/1979 targets, no tolerance, no
verdict, and no claim about any real country. The series is the row-level `ner` on primary rows
(equivalently `ner_primary`).

Crossing rule (predeclared): **first-at-above** = first year with NER ≥ threshold; **first-sustained** =
first year `y` such that every year `y … y+4` is at or above the threshold (five consecutive years),
mirroring the on-disk "first-sustained" convention. The table is reproduced from `results/NER_SMOKE.csv`.

| threshold | first-at-above | first-sustained (≥5 y) | years ≥ threshold | % of 56 years | note |
|---|---|---|---|---|---|
| **90** | **1970** | **2007** | 20 | 35.71 | 1970 is an isolated above-threshold year; not sustained |
| **95** | **2016** | **2016** | 10 | 17.86 | first-at-above and first-sustained coincide |

Series diagnostics (same table): minimum **75.14471392** in **1978**; maximum **99.57100547** in
**2023**; **44 of 55** year steps are non-decreasing; **11** are decreases, so the series is **not
monotone** (`is_monotone_non_decreasing = false`). The decreases are concentrated in 1971–1978 (the
boom trough) plus three tiny post-2019 movements. The object is therefore computable and crossable,
but **not monotone**; no smoothness or monotonicity is claimed.

The 1970 value is above 90 because the model starts near-universal primary and the boom then drives the
series down to the 1978 trough before recovery. That is a property of this declared synthetic world,
not a historical statement.

---

## 5. What the new object does and does NOT license

**Does:**

- Make an object named `ner` / `ner_primary` available at the v1.2 panel interface, derived from the
  model's own official-age split.
- Make a primary-NER crossing computable for the synthetic PHL-like country (the smoke test above).
- Preserve the frozen v1.2 dynamics and artifacts, with all three invariance checks recorded.

**Does NOT:**

- Change any v1.2 check, parameter, result, or file. The v1.2 A–E verdicts are untouched.
- Pass, fail, or pre-judge the HKG transfer. No HKG series, target year, tolerance, or verdict is used
  here.
- Turn the synthetic NER into an observed NER, an estimate, or evidence about the Philippines, Hong
  Kong, or any country.
- Establish that the cohort-flow NER analogue is the UIS stock NER. That mapping is a separate
  declaration for the HKG predeclaration/Council, not something this addendum decides.
- Clear `SR-2` (v1.2 PHL precondition) or `SR-9` (Council authority). It addresses only the interface
  side of `SR-1`.

---

## 6. Disclosure: where NER equals GER, and other limits

- **NER equals GER where no over-age pupil is admitted.** The model admits official-age children first;
  if official demand fills capacity, `admitted_overage = 0` and the NER equals GER up to the panel's
  `%.10g` display rounding. For primary this holds for 1970–2018; from 2019 onward small over-age
  admissions appear and NER falls below GER (2025: NER **99.56814916**, GER **105.0**, a **5.43 pp**
  gap). This is the model's rationing rule, not a relabelling: the NER numerator is always the
  official-age component.
- **Display rounding.** Recomputing `100 * admitted_official / cohort` from the printed 10-significant-
  digit columns can differ from the printed `ger` by up to **6.0e-08** when `admitted_overage = 0`. This
  is display rounding, not a numerical inconsistency; the `ner <= ger` check uses a `1e-6` tolerance.
- **Tertiary.** Tertiary `admitted_overage` is positive in all 1 680 tertiary rows (the pool can exceed
  the current annual cohort), so tertiary NER is materially below tertiary GER. No NER value exceeds 100
  in this run (tertiary max **73.08**).
- **Level ranges (SYNTHETIC, DERIVED).** Primary 66.24–99.74; lower-secondary 47.35–96.92;
  upper-secondary 2.93–93.51; tertiary 0.66–73.08. These are descriptive ranges of the synthetic
  panel, not targets.
- **No HKG use.** The HKG predeclaration's TC-1/TC-2 need a measure decision about this object; this
  addendum deliberately does not make it.

---

## 7. File list and hashes

| file | sha256 |
|---|---|
| `PRE_DECLARATIONS.md` | `aa756f8b463e557eaf72601c23da150e76968ca249e0cc74c1ff30792533eb88` |
| `code/add_ner.py` | `e4eedc3fa33620f5dfaacdcab6778072e5a778e8c3f8a88dafcee9ebe04a1753` |
| `results/synthetic_panel_v1_2_ner.csv` | `c6d1f9b059b5a48cbd5a4aaf7e1c4611cad781819b74987988897e8d35e40294` |
| `results/NER_SMOKE.csv` | `987f9200c5218f9417b6850e8f2b561e216e2665280bb7fc87826c3be5f803e4` |
| `results/INVARIANCE_CHECKS.json` | `ca41790cf4f6a4b3b8f8f7ae4a3a077b94f730c8e4c448f33b9d7a58b79eecb5` |
| `results/INVARIANCE_RERUNS.json` | `7a8a83317701d720bb682baa556a357ebac0f554193cfe013f35d111ce28eb18` |

Frozen inputs (read-only; not modified):

| object | sha256 |
|---|---|
| `generator_v1_2/results/synthetic_panel_v1_2.csv` | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| `v1_2/PRE_DECLARATIONS.md` | `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` |
| `generator_v1_2/code/sim_v1_2.py` | `61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c` |
| `generator_v1_2/PARAMS.md` | `0d619781c4e059f54cf771fb385475f5f939dceced5036e8a21b6e07a2b315e3` |
| `generator_v1_2/RUN_MANIFEST.json` | `36c40ff95470893a6d6fda21d9afe341ec0f374073a7af56cdf9c55c9b75b876` |
| `generator_v1_2/results/reproduction_checks_v1_2.csv` | `72a17fb6dcf59db671bbbcdb04111560d1d1aee59791009111dc3861b3f0fba8` |
| `generator_v1_2/results/reproduction_checks_detail_v1_2.csv` | `0597bafb8f8b90ad03a0164e9c2137cdaaff2186f1d7d0c5e5476462b285706b` |

The authoritative, machine-readable record is [`RUN_MANIFEST.json`](RUN_MANIFEST.json).

---

## 8. No-causality / no-direction statement

**SYNTHETIC / DERIVED — not observed, not an estimate, not a forecast, not evidence about any country;
no causal or direction claim; no policy claim.** The NER object is a deterministic transformation of a
declared-assumption simulator's own output, created because the HKG interface lacked an NER object. No
number in this addendum describes the world.
