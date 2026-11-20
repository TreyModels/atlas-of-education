<!-- Worker W3, 2026-11-20. RUN-READY CHECKLIST. Nothing in this file has been executed.
     Every command below is written to be copy-pasteable LATER, after the preconditions in §0 clear.
     DO NOT RUN any command in §5 until SR-1, SR-2 and SR-9 are all clear. -->

# HKG CHECKLIST — run-ready, not run

**Banner for every output this checklist produces:**
`SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

**Read first:** `HKG_TRANSFER_PRE_DECLARATIONS.md` (frozen) and `HKG_INVENTORY.md`. This checklist **implements** them; where they conflict, the predeclaration wins.

**FROZEN PREDECLARATION sha256:**
```
99be01d78abee2fa797c02a68a05330a4d53ad43c30960508039708edc98fb5f  HKG_TRANSFER_PRE_DECLARATIONS.md
```
Verify with `shasum -a 256 HKG_TRANSFER_PRE_DECLARATIONS.md`; if it differs, **STOP** — do not run against an unknown spec.

**Current status: `BLOCKED` — do not run.** See §0.

---

## 0. Gate — all three must be clear before any command in §5 is executed

| gate | condition | current state | how to confirm |
|---|---|---|---|
| **SR-1 NER interface** | the model emits a declared **NER** object | ❌ **NOT CLEAR** — `generator_v1` has no NER object (`PARAMS.md:59,252`; no `ner` column in `results/synthetic_panel_v1.csv`) | `grep -c ',ner,' <panel>.csv` → must be ≥1; and a declared age-appropriate definition must exist |
| **SR-2 PHL precondition** | **v1.2 passes its PHL checks (a)–(e)** (W1's job) | ❌ **NOT CLEAR** — `v1_2/` holds only `PRE_DECLARATIONS.md`; no code/results | `ls synthetic_2026-11-20/v1_2/` must show `code/sim_v1_2.py`, `PARAMS.md`, `results/reproduction_checks_v1_2.csv` with all checks PASS |
| **SR-9 Council authority** | a **new Council decision** authorising the HKG run | ❌ **NOT GRANTED** — slate PARKED-ARMED (D75; `STATUS.md:441`) | `grep -n "HKG" 08_council/DECISIONS.md` must show a decision **after** D75 authorising the run |

**If any gate is unclear: STOP. Record `BLOCKED-*(SR-n)`. Do not run. Do not substitute a measure.**

---

## 1. Inputs — with sha256 (verify before every run)

All hashes below were computed on disk 2026-11-20 for this checklist and are also in `RUN_MANIFEST.json`. **Run the verification in §2 first; abort on any mismatch.**

### 1a. Observed / derived inputs cited by the predeclaration

| role | path (relative to programme root) | sha256 | note |
|---|---|---|---|
| **NER/ANER/GER/PTR series (C01)** | `data/gmr_observed_6countries_1970_2024.csv` | `794a67c11ca052412edb2935c33c3c6e635cbd2e81ca5b9e44345ef9f5326e41` | **the source of TC-1/TC-2** |
| **Crossing table (C03, 128 rows)** | `10_massification/data/UNIVERSALIZATION_TIMING.csv` | `6e067ffd76b2c57c7c0363387735750cb9e6f68bc4dfd242b3d0f9c80786f892` | targets 1974/1979 |
| Crossing table (A01, 63 rows, first-**sustained**) | `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv` | `6223b75a4d4808c29426aa67fdf52e5155b53bf77e701cf804c0e062c3d11525` | method + `pct_years_above` |
| Policy dates | `10_massification/data/POLICY_TIMELINE.csv` | `a068b5bf92cee52e442231ef8de63e1b3814d1e42cd61b02969ccf1f3fb3353e` | 1971/1978/2008/2012 |
| Capacity | `10_massification/data/STATE_CAPACITY.csv` | `704efacad00f0ba7ddf579459a930d064fdb0f4b882cffbbf44a6cbecd585044` | PTR 1996–2018 |
| School expansion | `10_massification/data/SCHOOL_EXPANSION.csv` | `c218e6c9bd784e135e089ebecefec21112a09e6bf2c778599a33bc81b78c8ea3` | **PHL-only — 0 HKG rows** |
| Series store | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | `85bc869396ebfcb39e3e1a21a31af219e75a07326c738a51d2bfdbe536737ddb` | cohorts 1995–2024 |
| Economy panel | `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` | `aaaab2744803989ff0f347e27d5824c9b0086b967914d96d21ecd354329787d3` | 1995+ |
| ECI panel | `09_relations/data/economic_complexity_panel.csv` | `27403fce9556239ed058bf981749a856946a96ada38f52920d77c13362d44958` | 1995–2024 |
| Event windows | `10_massification/relations/data/event_windows.csv` | `7bac26b3ff143b97443988db822457b2c5fa63f13c41fad8c8247ca6a0d52ffb` | 1971/1978/2012 UNABLE |
| Measurement defs | `10_massification/data/DATA_NOTES_MASSIFICATION.md` | **`5e51c5d0a6d620125f0f8ef902ed8942cf3bed96af762cd213f71b7613a8c244`** | ⚠ **hash drift vs `SHA256SUMS.txt`** (`e2cfcdb2…`); explained at `STATUS.md:639` — record the actual hash, flag the drift |

### 1b. Model inputs (the frozen parameterisation that would be ported)

| role | path | sha256 |
|---|---|---|
| Architecture (A1/A2/A3) | `10_massification/extensions/synthetic_2026-11-20/MODEL_ARCHITECTURE.md` | `862b5b8bd4360da243dcaca5a239f3ff97ff243dee1f01ab94afccc1b15dad55` |
| **v1.2 predeclaration (the PHL model)** | `…/synthetic_2026-11-20/v1_2/PRE_DECLARATIONS.md` | `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` |
| v1 PARAMS (parameter list source) | `…/synthetic_2026-11-20/generator_v1/PARAMS.md` | `9052e85bb0a2b010c2c300a2f728e2a99f277a2bcea6d08f193d25b8a7f026fe` |
| v1 code | `…/synthetic_2026-11-20/generator_v1/code/sim_v1.py` | `a03fa0cb05a879020e254207dcd4add540883d0920b7d4457d3b157f7400a8d8` |
| **Y5 data-completeness audit** | `…/lab_2026-11-20_c/Y5_portability_audit/results/transfer_checklist.csv` | `2a512622a68c11649a66dd5f255462787cee94068fef8e80906eeed0892760eb` |
| Y5 findings | `…/lab_2026-11-20_c/FINDINGS.md` | `8c2a675b8913d1f1bd2fde5765589585072ba0cdcde8d091cb8a6b8c3dc761b5` |
| Audit register | `…/audit_2026-11-20/a_regressions/REGRESSION_INVENTORY.csv` | `b4effcc4f194d093b796a92e655625b5e715209e1feae67167cd3ed3a8414c0a` |
| Decision record | `08_council/DECISIONS.md` | `7bfba8776f6c08e85c02b2ac183b099f08abe2d79dfd72e0c3e273cebddde6ff` |
| Status | `10_massification/STATUS.md` | `2056ab94148c60f2ccbe26c581dc135d42bd5b59be53934d39bbd167e24ffc99` |
| State-capacity lit | `10_massification/lit/STATE_CAPACITY.md` | `093e03dc5d9cf4f8eeb076b26c6ac56afb15b24d154555f69cb9e18b0b1ab56a` |
| Timelines lit | `10_massification/lit/UNIVERSALIZATION_TIMELINES_JPN_KOR_HKG.md` | `80fd254cff94a40d84ff6c8a59bdf38367f617818d3f00e66cd5a5248e69e9e4` |
| Timing lit | `10_massification/lit/UNIVERSALIZATION_TIMING.md` | `fbb5198ccd6b08cdc9c7ab14b8ab552c1d7a58d9fb4aeecae5d523e775efc68f` |
| Rival lit | `10_massification/lit/RIVAL_MODELS_ANCHOR.md` | `ee99e05cabfd167f716bb7d62ce1794c5e3eb74eba616da7f9f6960e0c145fba` |
| Labour lit | `10_massification/lit/LABOUR_MARKET_REPORTS.md` | `683940287830a76e66dfa89fc14c1c4e4dea7441697d40d4673ffa0257fdec32` |
| HKG country card | `02_lit/COUNTRY_CARDS/HKG.md` | `d8c0c6a213fb6d8de24b808925a37f4f84ca7d2b9f27e72382d29bd07d77c769` |
| Shadow targets | `02_lit/SHADOW_TARGETS.csv` | `3c613137d82830f3108e3c610922b8af57d3a8155d9baf7c96ec89994a8dc06f` |
| Data ledger | `DATA_LEDGER.md` | `a93f3cd69d4d7e374412f48542e1f75e533636d3284601251a665ba989a97bfe` |

### 1c. Spec files in this directory (frozen)

| path | role |
|---|---|
| `HKG_TRANSFER_PRE_DECLARATIONS.md` | **the frozen spec** — hash in `RUN_MANIFEST.json` |
| `HKG_INVENTORY.md` | evidence record |
| `DATA_INVENTORY.csv` | per-object data register |
| `HKG_CHECKLIST.md` | this file |

---

## 2. Pre-run verification (safe — read-only; may be run any time)

```bash
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20

# 2.1 verify every input hash in §1 against disk; abort on any mismatch
python - <<'PY'
import hashlib, json, sys
man = json.load(open("10_massification/extensions/hkg_transfer_2026-11-20/RUN_MANIFEST.json"))
bad = []
for rel, want in man["inputs"].items():
    got = hashlib.sha256(open(rel, "rb").read()).hexdigest()
    if got != want:
        bad.append((rel, want, got))
for rel, want, got in bad:
    print(f"MISMATCH {rel}\n  manifest {want}\n  actual   {got}")
print("ALL INPUTS MATCH" if not bad else f"{len(bad)} MISMATCH(ES) -> ABORT")
sys.exit(1 if bad else 0)
PY

# 2.2 verify the frozen predeclaration hash matches the manifest (PA-1 precondition)
shasum -a 256 10_massification/extensions/hkg_transfer_2026-11-20/HKG_TRANSFER_PRE_DECLARATIONS.md

# 2.3 confirm the on-disk targets are unchanged (TC-1/TC-2 integrity)
grep -n "HKG.*primary,90,NER\|HKG.*primary,95,NER" 10_massification/data/UNIVERSALIZATION_TIMING.csv
#   expect: ,primary,90,NER,1974,1973,1974,none,observed,high
#   expect: ,primary,95,NER,1979,1978,1979,none,observed,high

# 2.4 confirm the data SHA256SUMS state (expect 1 known FAIL on DATA_NOTES_MASSIFICATION.md)
cd 10_massification/data && shasum -a 256 -c SHA256SUMS.txt; cd - >/dev/null
```

**Expected 2.4 output:** ten `OK` lines and exactly one `FAILED` for `DATA_NOTES_MASSIFICATION.md` (known drift, `HKG_INVENTORY.md` §11.2). **Any other failure ⇒ abort.**

---

## 3. Gate check (safe — read-only)

```bash
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20

# SR-1: does the runnable model emit NER? (currently: NO -> BLOCKED)
ls 10_massification/extensions/synthetic_2026-11-20/v1_2/
grep -rn "ner" 10_massification/extensions/synthetic_2026-11-20/v1_2/code/sim_v1_2.py 2>/dev/null || echo "SR-1 OPEN: no v1.2 code"

# SR-2: has v1.2 passed its PHL checks (a)-(e)?
cat 10_massification/extensions/synthetic_2026-11-20/v1_2/results/reproduction_checks_v1_2.csv 2>/dev/null \
  || echo "SR-2 OPEN: no v1.2 results"

# SR-9: is there a Council decision authorising an HKG run after D75?
grep -n "HKG" 08_council/DECISIONS.md | awk -F'|' '{print $2, $3}'
```

**All three must print a clear pass. As of 2026-11-20 all three are open ⇒ `BLOCKED`.**

---

## 4. Parameter-freeze list (copy into the run; verify with PA-1/PA-2)

**FIXED — assert `run_value == frozen_value` for every one; any delta ≠ 0 aborts the run** (full list and sources in the predeclaration §5a, `PARAMS.md:77–186`, `v1_2/PRE_DECLARATIONS.md:73–81`):

```
lf_share_of_pop 0.52          age_share_base 0.160        age_share_tfr_slope 0.045
age_share_min 0.130           age_share_max 0.420         band_share (0.42,0.21,0.20,0.17)
x_income_coef 0.55            x_urban_coef 0.55           x_urban_ref 0.40
x_min 0.0                     x_max 1.80                  takeoff_lit 0.60
takeoff_income 1500.0         div_x 0.95                  div_income 6000.0
lit_learn 0.05                lit_lag 12                  sec_ag_base 0.500
sec_ag_x -0.450               sec_inf_base 0.240          sec_inf_x -0.080
sec_man_base 0.130            sec_man_x 0.090             sec_floors (0.02,0.05,0.03,0.05)
rung_a (0.90,0.40,-0.30,-1.30)      rung_b (-0.65,0.20,1.00,2.20)
x_open (0.00,0.08,0.26,0.48)  office_u_coef (0,0.35,0,-0.20)
mfg_u_coef (0,-0.10,0.30,0.10)      phi_formal 0.82
sep (0.10,0.07,0.05,0.04)     seek (0.15,0.35,0.60,0.80)
queue_retain 0.50             queue_max_lf 0.20           rank_gain 0.20
rung_mult (2.20,3.20,4.60,6.40)     cred_prem 0.10
psi_pre 0.02  psi_ind 0.22  psi_div 0.12        rank_factor rung1 == 1.0 exactly
gp (0.012,0.008,0.030,0.022)  accel_ind (1.0,1.0,1.6,1.3) accel_div (1.0,1.0,1.3,1.5)
comp_step (0.10,0.18,0.32,0.50)     lit_ag_growth 0.010
g_floor 0.0   g_cap 0.090     g_noise_sd 0.006
dur (6,3,3,4) ger_cap 105.0   overage_cap 1.05
star_c1 (0.30,1.60,1.45,0.90) star_c3 (0.25,1.10,1.10,0.70)
adj_speed (0.50,0.50,0.35,0.35)     surv_min (0.62,0.55,0.60,0.70)
seat_lo (1.02,0.28,0.14,0.05)       seat_hi (1.05,0.985,0.80,0.78)
ter_pool_retain 0.35          ter_trans_cap 0.65          meas_completion_factor (1,1,1,1)
gamma >=0 (quality) capacity_response_coef + lag (v1.2 PARAMS)
household: y_med w_child farm compat v0 decay cost neither girl_care haz  (v1.2 PARAMS)
seed 20261120
```

**DECLARED HKG INPUTS — may be re-set, must be tabulated first** (predeclaration §5b): D1 cohorts · D2 economy · D3 policy dates (1971/1978/2008/2012) · D4 capacity · D5 gate mapping · D6 measurement defs · **D7 initial conditions** · **D8 sector offsets / office–mfg bias** · **D9 delivery pace** · D10 push markers · D11 NER↔ANER substitution.

**D7/D8/D9 are the tuning risk** — value + rationale + hash must be recorded in `results/hkg_declared_inputs.csv` **before** the run; a post-output change is `FAIL-RE-FIT`.

**FORBIDDEN (auto-void):** re-fit any FIXED · change threshold/target/tolerance · splice or mix measures · impute completion · add a free parameter · per-country override · use the 2016/2014 lower-secondary crossing · in-run NER patch (predeclaration §5c).

---

## 5. The exact commands that WILL be run (DO NOT RUN UNTIL §0 CLEARS)

Written to be copy-pasteable later. `PY` is the programme venv:

```bash
PY="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
ROOT="/Users/treymenefee/massification_live/experiments/massification-2026-11-20"
OUT="$ROOT/10_massification/extensions/hkg_transfer_2026-11-20"
cd "$ROOT"
```

### 5.1 Run 1 of 2 — the scored run

```bash
"$PY" "$OUT/code/run_hkg_transfer.py" \
    --model   "10_massification/extensions/synthetic_2026-11-20/v1_2/code/sim_v1_2.py" \
    --params  "10_massification/extensions/synthetic_2026-11-20/v1_2/PARAMS.md" \
    --inputs  "10_massification/data/UNIVERSALIZATION_SERIES.csv" \
              "10_massification/data/JOBS_AND_MARKETS_PANEL.csv" \
              "10_massification/data/POLICY_TIMELINE.csv" \
              "10_massification/data/STATE_CAPACITY.csv" \
              "10_massification/data/UNIVERSALIZATION_TIMING.csv" \
              "data/gmr_observed_6countries_1970_2024.csv" \
    --country HKG --seed 20261120 \
    --targets primary:NER:90:1974:1973:1974 primary:NER:95:1979:1978:1979 \
    --tolerance-years 5 \
    --predecl "10_massification/extensions/hkg_transfer_2026-11-20/HKG_TRANSFER_PRE_DECLARATIONS.md" \
    --out "$OUT/results/run1"
```

### 5.2 Run 2 of 2 — the determinism replicate (identical args, different output dir)

```bash
"$PY" "$OUT/code/run_hkg_transfer.py" \
    --model   "10_massification/extensions/synthetic_2026-11-20/v1_2/code/sim_v1_2.py" \
    --params  "10_massification/extensions/synthetic_2026-11-20/v1_2/PARAMS.md" \
    --inputs  "10_massification/data/UNIVERSALIZATION_SERIES.csv" \
              "10_massification/data/JOBS_AND_MARKETS_PANEL.csv" \
              "10_massification/data/POLICY_TIMELINE.csv" \
              "10_massification/data/STATE_CAPACITY.csv" \
              "10_massification/data/UNIVERSALIZATION_TIMING.csv" \
              "data/gmr_observed_6countries_1970_2024.csv" \
    --country HKG --seed 20261120 \
    --targets primary:NER:90:1974:1973:1974 primary:NER:95:1979:1978:1979 \
    --tolerance-years 5 \
    --predecl "10_massification/extensions/hkg_transfer_2026-11-20/HKG_TRANSFER_PRE_DECLARATIONS.md" \
    --out "$OUT/results/run2"
```

### 5.3 Determinism gate — two runs must be byte-identical (SR-7)

```bash
diff -r "$OUT/results/run1" "$OUT/results/run2" && echo "DETERMINISM OK" \
  || { echo "SR-7 FIRED: runs differ -> NO VERDICT"; exit 1; }
```

### 5.4 Audits §6 of the predeclaration (must all pass)

```bash
"$PY" "$OUT/code/audit_parameter_freeze.py" --run "$OUT/results/run1" --predecl \
      "$OUT/HKG_TRANSFER_PRE_DECLARATIONS.md" --strict   # PA-1, PA-2, PA-3
"$PY" "$OUT/code/audit_measure_integrity.py" --run "$OUT/results/run1"  # PA-4
grep -rniE "PASS|SUPPORTED|NOT SUPPORTED|REPRODUCED|VALIDATED|PORTABLE|HOLDS" "$OUT/results/run1" \
  && { echo "PA-5 FIRED: forbidden verdict string"; exit 1; } || echo "PA-5 OK"
grep -rc "SCALING: FAIL" "$OUT/results/run1"    # PA-6: every file, count >= 1
```

### 5.5 Emit outputs and manifest

```bash
cp -R "$OUT/results/run1/." "$OUT/results/"
"$PY" "$OUT/code/build_manifest.py" --results "$OUT/results" --out "$OUT/RUN_MANIFEST_run.json"
shasum -a 256 "$OUT"/results/* > "$OUT/SHA256SUMS_results.txt"
```

> **`code/run_hkg_transfer.py`, `code/audit_parameter_freeze.py`, `code/audit_measure_integrity.py`, `code/build_manifest.py` DO NOT EXIST YET and must NOT be written until §0 clears** — writing them now would be building a harness for a run that is blocked, and would risk encoding the answer. They are specified in §7 so they can be written against a frozen spec.

---

## 6. Checks to be run (summary of the frozen spec)

| id | check | measure | target | tolerance | in verdict? |
|---|---|---|---|---|---|
| **TC-1** | primary NER ≥90 crossing | NER (`NER.1.cp`) | **1974** (band 1973–1974) | ±5 y → [1969,1979] | **YES** |
| **TC-2** | primary NER ≥95 crossing | NER | **1979** (band 1978–1979) | ±5 y → [1974,1984] | **YES** |
| **DISCLOSURE** | 1977 = 95.10725 first-at-above; 1978 = 94.6876 dip; `pct_years_above` 45.8; later dips 1995/96/2012–15 | — | — | printed in every table | no (mandatory print) |
| **LC-1** | primary NER level at 1974 & 1979 | NER | 91.10855 / 95.07646 | ±5 pp | **NO — check-only** |
| PA-1…PA-6 | freeze / extra-param / anchor-array / measure / forbidden-string / banner audits | — | — | zero tolerance | **gate** |

**Verdict tokens (closed set):** `DIAGNOSTIC-TRANSFER: TRANSFER-HOLDS` · `…: TRANSFER-FAILS` · `…: FAIL-RE-FIT` · `BLOCKED-*(SR-n)` (terminal, **not** a verdict). **`PASS` is forbidden.**

---

## 7. Required output files (post-run)

| file | must contain |
|---|---|
| `results/hkg_transfer_checks.csv` | TC-1, TC-2, LC-1 rows + the 1977 disclosure row |
| `results/hkg_crossings_model.csv` | model crossings by level × threshold × measure; **both** first-sustained and first-at-above rules; `pct_years_above` |
| `results/hkg_levels_checkonly.csv` | levels 1974/1979, header `LEVELS: CHECK-ONLY — NOT A VERDICT COMPONENT` |
| `results/hkg_parameter_freeze_audit.csv` | PA-1…PA-4, `delta` all zero for FIXED |
| `results/hkg_declared_inputs.csv` | D1–D11 values, `source_or_DECLARED`, hash — **including the pre-1995 declared paths** |
| `results/hkg_run_meta.json` | seed, model/params hashes, v1.2 precondition status, timestamps, byte counts |
| `RUN_MANIFEST_run.json` | post-run hashes + verdict token + stop-rule id if any |
| `SHA256SUMS_results.txt` | hash of every result file |
| `FINDINGS.md` | **written only after** the run; FAILs and BLOCKEDs included; no-causality statement present |

Every file carries: `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

---

## 8. Determinism requirement

- seed **20261120**, one `PCG64` stream, no wall-clock/OS entropy, floats `%.10g`.
- **Two clean runs byte-identical** — verified by the stored `diff -r` in §5.3, recorded in the manifest. **Not** an assertion in prose.
- Any difference ⇒ **SR-7**, run invalid, **no verdict emitted**.

---

## 9. Reporting format

1. **Header, every artifact:** the banner + the no-causality statement from predeclaration §9, verbatim.
2. **Verdict line, first line of `FINDINGS.md`:** exactly one token from the closed set, plus `err_1`/`err_2` in years. No adjectives.
3. **One table per check**, columns in the order fixed in predeclaration §10. Observed and model numbers **never in the same column**.
4. **Disclosure block** (1977 / 1978 dip / `pct_years_above` / later dips) printed before the verdict table, not in a footnote.
5. **BLOCKED reporting:** state the stop-rule id, the failing precondition, and what would clear it. **Never** report a `BLOCKED` state as a result, and **never** describe it as a failure of the model or of HKG.
6. **No causal, direction, push–pull, portability, capacity or policy sentence anywhere** (R13/R22/D61/D77). No "HKG universalized because…".
7. **Failures reported, not rescued** (`v1_2/PRE_DECLARATIONS.md:113–115`).

---

## 10. Sign-off block (to be completed only if §0 cleared and the run completed)

```
Predeclaration sha256 : 99be01d78abee2fa797c02a68a05330a4d53ad43c30960508039708edc98fb5f
Run 1 / Run 2 identical: <yes/no>
PA-1..PA-6             : <pass/fail each>
v1.2 PHL checks (a)-(e): <pass/fail each>
Council authorisation  : <decision id + date>
TC-1 err (years)       : <n>
TC-2 err (years)       : <n>
LC-1 (check-only)      : <n pp MAE>
VERDICT                : <one token from the closed set>
```
