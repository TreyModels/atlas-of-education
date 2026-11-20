# DRY-RUN PLAN — STOCK-NER-D construct test: the exact protocol, **not executed**

> `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

**Worker SN, 2026-11-21 (Asia/Shanghai). RUN-READY. NOTHING IN THIS FILE HAS BEEN EXECUTED.**

**Read first:** `PRE_DECLARATIONS.md` (frozen; sha256 below) and `STOCK_NER_DESIGN.md`. This plan
**implements** them; where they conflict, **the predeclaration wins**.

**FROZEN PREDECLARATION sha256:**

```
6f5d3c169487f4b6e296e4bf1673ec0755e04499cf5d291c9ccd88089c73bb3e  PRE_DECLARATIONS.md
```

If `shasum -a 256` on that file differs, **STOP** — do not run against an unknown spec, and report
`BLOCKED-PRECONDITION`. The same value is in `RUN_MANIFEST.json → predeclaration_sha256` and in
`SHA256SUMS.txt`.

**Status: `NOT-RUN-NOT-AUTHORISED`.** D120 authorises the **design** only. Execution of anything in §3–§8 is a
**further controller action** that requires (a) a new Council decision, (b) the HKG gate's own preconditions,
and (c) the hash verification of §2 below. **No command in this file has been run**; the construct test does
not exist as an artifact.

**Label.** The test objects are **SYNTHETIC**; the comparator is **DERIVED**. No observed series is read.
No HKG result exists until one is produced; nothing here licenses a portability, capacity-timing, or
phase-verdict claim. `BLOCKED-*` is terminal.

---

## 0. Gates — all must clear before any command in §3 is executed

| gate | condition | current state |
|---|---|---|
| **A — Council authority** | a **new** Council decision authorising the construct test (D120: "execution NOT authorised … further controller action after freeze") | ❌ **NOT GRANTED** |
| **B — freeze integrity** | `PRE_DECLARATIONS.md` sha256 = `7d67b4fa…` | ✅ recorded at freeze; must be re-verified at run time |
| **C — checklist §2** | the frozen HKG spec and its inputs verify (§2.2 below) | ✅ expected to pass (11/11 hashes match as of freeze) |
| **D — input integrity** | this experiment's cited inputs match `RUN_MANIFEST.json → inputs` (§2.1) | ✅ expected to pass |
| **E — no prior run** | `results/` and `_determinism/run2/` do not exist | ✅ **neither exists** (verified at freeze: the directory holds three spec files, this plan, the manifest and the sums — and no `results/`) |

**If any gate is unclear: STOP. Record `BLOCKED-PRECONDITION` (A/B), `BLOCKED-INPUT` (C/D) or `BLOCKED-STATE`
(E). Do not run. Do not substitute an object, a level, a country, a bar, or a tolerance.**

---

## 1. What the run may write — and nothing else

The run may create **only** inside `10_massification/extensions/hkg_stock_ner_2026-11-20/`:

```
code/stock_ner_d.py                 the runnable module (transcribed from Appendix A)
results/                            run 1 outputs (5 files, §5)
_determinism/run2/                  run 2 outputs, byte-compared to results/
run_log.txt                         optional; must contain no timestamp-bearing field in any computed column
```

It **must not** write to `synthetic_2026-11-20/`, `m1_ner_2026-11-20/`, `hkg_transfer_2026-11-20/`,
`10_massification/data/`, `08_council/`, or any other path. The panel is opened **read-only**. No
`__pycache__` is created in any other directory (`PYTHONDONTWRITEBYTECODE=1` / `python -B`).

**Run-once rule.** The module **refuses** if its output directory already exists. A re-run is a *new*
directory, never an overwrite; a silent overwrite voids the determinism evidence.

---

## 2. Pre-run verification (read-only; safe)

### 2.1 This experiment's own freeze and inputs

```bash
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20
D=10_massification/extensions/hkg_stock_ner_2026-11-20

# 2.1.1 frozen spec hash — must print 6f5d3c169487f4b6e296e4bf1673ec0755e04499cf5d291c9ccd88089c73bb3e
shasum -a 256 "$D/PRE_DECLARATIONS.md"

# 2.1.2 every cited input against this experiment's manifest; abort on any mismatch
python - <<'PY'
import hashlib, json, sys
D = "10_massification/extensions/hkg_stock_ner_2026-11-20"
man = json.load(open(D + "/RUN_MANIFEST.json"))
bad = []
if hashlib.sha256(open(D + "/PRE_DECLARATIONS.md", "rb").read()).hexdigest() != man["predeclaration_sha256"]:
    bad.append(("PRE_DECLARATIONS.md", "predecl hash", "mismatch"))
for rel, want in man["inputs"].items():
    got = hashlib.sha256(open(rel, "rb").read()).hexdigest()
    if got != want:
        bad.append((rel, want[:12], got[:12]))
for rel, want in man["spec_files"].items():
    if rel.endswith("PRE_DECLARATIONS.md"):
        continue
    got = hashlib.sha256(open(rel, "rb").read()).hexdigest()
    if got != want:
        bad.append((rel, want[:12], got[:12]))
print("ALL HASHES MATCH" if not bad else bad)
sys.exit(1 if bad else 0)
PY

# 2.1.3 both directories must be absent
test -e "$D/results" && echo "BLOCKED-STATE: results/ exists" || echo "ok: no results/"
test -e "$D/_determinism/run2" && echo "BLOCKED-STATE: run2 exists" || echo "ok: no run2/"
```

**Expected:** 2.1.1 prints `7d67b4fa…`; 2.1.2 prints `ALL HASHES MATCH`; 2.1.3 prints both `ok:` lines. **Any
deviation ⇒ abort.**

### 2.2 HKG checklist §2 — the frozen transfer spec this object was designed against

The object is only meaningful against the **frozen** HKG specification. Execute `HKG_CHECKLIST.md` §2
**verbatim** (it is read-only and may be run any time), from the programme root. Expected results:

| step | expected |
|---|---|
| §2.1 (HKG `RUN_MANIFEST.json → inputs`) | **`ALL INPUTS MATCH`** — 11/11; verified at this freeze: 0 mismatches |
| §2.2 (`shasum` of `HKG_TRANSFER_PRE_DECLARATIONS.md`) | `99be01d78abee2fa797c02a68a05330a4d53ad43c30960508039708edc98fb5f` |
| §2.3 (the two recorded TC-1/TC-2 rows unchanged) | the two rows read exactly as the frozen predeclaration records them; this is a read-only check of the **frozen transfer spec** and is **not** executed by, or passed to, the object module |
| §2.4 (`10_massification/data/SHA256SUMS.txt`) | **ten `OK` and exactly one `FAILED`**, for `DATA_NOTES_MASSIFICATION.md` (known drift, `HKG_INVENTORY.md` §11.2) |

**Any other failure in §2.4 ⇒ abort.** If §2.3 shows a changed target row, abort — the frozen transfer would
have moved underneath the object.

> **Known stale entry, disclosed.** `HKG_CHECKLIST.md` §1b's **table** lists `08_council/DECISIONS.md` at
> `7bfba877…`; the file's actual hash at this freeze is `b214171f82538580e615c68ccde73d94a22dec84f4a71449754141089ce62cd8`
> because D131 was appended after the checklist was written. **The operative §2.1 check iterates the HKG
> manifest's `inputs` map, which does not include `DECISIONS.md`** — so §2.1 is unaffected, and this is a
> documentation staleness in a frozen file (which this worker does not edit), not an input drift. It is
> recorded here so that a future reader does not mistake it for a failure.

### 2.3 Static guards before any computation

Run the module's `--check` mode (Appendix A, `check_guards()`), which exercises **G4** (operand allow-list)
and **G6** (target isolation). **Expected:** `GUARDS OK`. A G6 hit is `FAIL-RE-FIT` — the design falsifier —
and the run **is not dispatched**.

---

## 3. Build the object (algorithm, exact)

Transcribe Appendix A into `code/stock_ner_d.py`, then:

```bash
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20
D=10_massification/extensions/hkg_stock_ner_2026-11-20
PYTHONDONTWRITEBYTECODE=1 "/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" -B \
  "$D/code/stock_ner_d.py" --check
```

For each test type `(T1, SYN00_PHL_LIKE)`, `(T2, SYN28)`, level `primary`, `d = 6`, years 1970–2025:

1. **Index** the panel by `(country, year, level)`; assert 6 720 rows, 67 columns, `label = SYNTHETIC` on
   every row (**G3**).
2. **For each year `t` with `t − d + 1 ≥ 1970`** (primary: `t ≥ 1975`):
   - `s = survival[c, t, primary]`;
   - `N = Σ_{k=0..d−1} admitted_official[c, t−k, primary] · s**(k/d)`;
   - `B = Σ_{k=0..d−1} cohort[c, t−k, primary]`;
   - `STOCK[t] = 100 · N / B`; assert both sums finite and `B > 0` (**G5**).
3. **`FLOW[t] = 100 · admitted_official[c,t,primary] / cohort[c,t,primary]`**; cross-check against the
   addendum panel's `ner` column at `%.10g` display precision; abort on mismatch.
4. **No other column is read** (**G4**): not `ner*` (except the §5 cross-check), not `band_population`, not
   `admitted_overage`, not `enrolment`, not `ger`, not `rationed_official`.
5. **No smoothing, no imputation, no interpolation, no partial window.**

---

## 4. Score the construct test (exact)

1. **Band set** for each series: `{ t : t ∈ STOCK and 85.0 ≤ FLOW[t] ≤ 95.0 }`. Empty ⇒ that series'
   Condition B is `UNDETERMINED`.
2. **Condition B** `MET` iff `|STOCK[t] − FLOW[t]| ≤ 2.0 + 1e-9` for **every** band year; otherwise
   `NOT_MET`.
3. **Condition C**, for `T ∈ {90.0, 95.0}`: `first_sustained(x, T)` = first `y` with `x[y..y+4]` all `≥ T`
   (five consecutive years), evaluated on the series' full computable range (`FLOW` 1970–2025,
   `STOCK` 1975–2025); `first_at_or_above` reported alongside but **not** verdict-bearing.
   - both defined → `delta = |STOCK_year − FLOW_year|`; `MET` iff `delta ≤ 1`, else `NOT MET`;
   - exactly one defined → `NOT MET`;
   - neither defined → `MET`, recorded explicitly.
4. **Condition C per series** `MET` iff both thresholds are `MET`.
5. **Verdict** (closed set, `PRE_DECLARATIONS.md` §6.5):

```
CONSTRUCT-EQUIVALENT          iff B(T1), B(T2), C(T1), C(T2) all MET
BLOCKED-MEASURE(N2-EMPTY)     iff any band set is empty
BLOCKED-MEASURE(N2-BOTH)      iff a band NOT_MET and a crossing NOT_MET
BLOCKED-MEASURE(N2-BAND)      iff a band NOT_MET only
BLOCKED-MEASURE(N2-CROSSING)  iff a crossing NOT_MET only
```

6. **Descriptive sensitivity (§6.6)** is computed last, written to its own file, and **must not** be consulted
   before the verdict token is written.

---

## 5. Expected outputs (exact schemas; **none exists at freeze time**)

| file | columns / content |
|---|---|
| `results/STOCK_NER_RESULTS.csv` | `object_definition_id,test_type,country,level,condition,statistic,value,threshold,component_result,verdict_bearing,label` — one row per condition/statistic: band max abs diff, band-year count, band years over bar, both crossing years and deltas per threshold, per-series aggregate, overall verdict |
| `results/STOCK_NER_COMPARISON.csv` | `country,year,stock,flow,diff,abs_diff,band_member,bar_met,stock_window_complete,role,label` — every year 1970–2025 for T1 and T2; `role ∈ {VERDICT, DESCRIPTIVE-SENSITIVITY}`; `bar_met ∈ {TRUE,FALSE,NA}` |
| `results/STOCK_NER_CROSSINGS.csv` | `test_type,threshold,series,first_at_or_above,first_sustained,defined,delta_years,le_1y,component_result,label` |
| `results/STOCK_NER_SENSITIVITY.csv` | `country,level,years_in_band,max_abs_diff,band_years_over_bar,role,component_result,label`, one row per (country, level), `role = DESCRIPTIVE-SENSITIVITY`, `label = SYNTHETIC` |
| `results/STOCK_NER_VERDICT.txt` | the single token from §4.5, the banner line, and the two label sentences of `PRE_DECLARATIONS.md` §11.2 |

Formatting: `%.6f` for all numeric report fields; years as integers; `none_by_2025` a string, never a number;
no timestamp, hostname, path, process id, or float-repr instability in any computed field. Component results
are written `MET` / `NOT_MET` / `UNDETERMINED` — **never** `PASS` / `FAIL`.

---

## 6. Guards — ids, rule, abort behaviour

| id | guard | rule | on violation |
|---|---|---|---|
| **G1** | freeze integrity | `PRE_DECLARATIONS.md` sha256 == `7d67b4fa…` | abort, `BLOCKED-PRECONDITION` |
| **G2** | input integrity | every `RUN_MANIFEST.json → inputs` hash matches on disk | abort, `BLOCKED-INPUT` |
| **G3** | panel schema | 6 720 rows, 67 named columns, every `label = SYNTHETIC`, both test types present for all 56 years | abort, `BLOCKED-INPUT` |
| **G4** | operand allow-list | the module reads exactly `{country, year, level, admitted_official, cohort, survival, label}` (plus `ner` in the §5 cross-check only) | abort, `FAIL-RE-FIT` (an operand was added) |
| **G5** | no imputation / left edge | every operand of every computed row exists; no `None`/`NaN`/`inf`; no partial window; `B > 0` | abort, `BLOCKED-INPUT` |
| **G6** | target isolation | AST scan of the module: **no** integer constant equal to (1900+74) or (1900+79), and **no** string constant containing them. *The guard builds the forbidden values arithmetically so that its own AST never carries the literals it forbids.* | `FAIL-RE-FIT` — the design falsifier; **not dispatched** |
| **G7** | forbidden strings + banner | the run's banner carrier `results/STOCK_NER_VERDICT.txt` contains the banner `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`; every CSV contains `SYNTHETIC` on its rows; no output contains `PASS`, `SUPPORTED`, `VALIDATED`, `REPRODUCED`, `PORTABLE`, `CONFIRMED`, or bare `HOLDS` | run **void**, no verdict |
| **G8** | determinism | run 1 and run 2 outputs byte-identical (sha256) | run **invalid**, no verdict (`SR-7` analogue) |

G1–G6 run **before** any arithmetic. G7–G8 run **after** outputs are written and **before** any verdict is
reported.

---

## 7. Determinism

```bash
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20
D=10_massification/extensions/hkg_stock_ner_2026-11-20
PY="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"

PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$D/code/stock_ner_d.py" --out "$D/results"
PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$D/code/stock_ner_d.py" --out "$D/_determinism/run2"

for f in STOCK_NER_RESULTS.csv STOCK_NER_COMPARISON.csv STOCK_NER_CROSSINGS.csv \
         STOCK_NER_SENSITIVITY.csv STOCK_NER_VERDICT.txt; do
  a=$(shasum -a 256 "$D/results/$f"         | cut -d' ' -f1)
  b=$(shasum -a 256 "$D/_determinism/run2/$f" | cut -d' ' -f1)
  [ "$a" = "$b" ] && echo "OK   $f  $a" || echo "DIFF $f  -> BLOCKED-DETERMINISM (no verdict)"
done
```

**Expected:** five `OK` lines with identical hashes. One `DIFF` ⇒ `BLOCKED-DETERMINISM`; the run produces no
verdict and no finding.

There is no RNG, no seed, no clock, no network, no locale dependence and no dict-ordering dependence in the
module. The seed is irrelevant to this object; the model is **not** re-run — the frozen panel is read.

---

## 8. Reporting the outcome — and what may never be reported

1. **Write the token to `results/STOCK_NER_VERDICT.txt` first**, then to `RUN_MANIFEST.json`, then (and only
   then) write a FINDINGS file.
2. **`CONSTRUCT-EQUIVALENT`** licenses only the measure-side statement of `STOCK_NER_DESIGN.md` §12.1. It
   **does not** authorise the HKG transfer, does not clear SR-1/SR-2/SR-9, and does not license any HKG,
   portability, capacity-timing, or phase-verdict claim.
3. **`BLOCKED-MEASURE(N2-*)`** is **terminal**. It is recorded as a terminal state, in the same class as
   `BLOCKED-MEASURE(SR-1)`. It is **never** reported as a result, a model failure, or a country finding, and
   **no** alternative object/weighting/denominator/level/country/window/bar is tried.
4. **`FAIL-RE-FIT`** voids the run and names the moved parameter or the target-year reference.
5. **Forbidden in every output:** `PASS`, `SUPPORTED`, `NOT SUPPORTED`, `REPRODUCED`, `VALIDATED`,
   `CONFIRMED`, `PORTABLE`, bare `HOLDS`; any sentence of the form "HKG universalized because …"; any
   comparison of a model number to an observed HKG number in the same column; any level claim; any capacity
   claim; any causal or direction claim.

---

## 9. Post-run records (only under a further decision)

`RUN_MANIFEST.json` (this directory) gains a `runs` array with: run 1/run 2 output hashes, the code hash, the
verdict token, the guard log, and the python version. The pre-existing `predeclaration_sha256` and `inputs`
blocks are **not** edited. `FINDINGS.md` is written **after** the run and must state the banner, the labels,
the no-causality paragraph, and — if the verdict is terminal — that no diagnostic was produced.

---

## Appendix A — reference implementation (listing only; **not shipped, never executed**)

> **This listing is a specification, not an artifact.** It has **not** been executed, it is **not** shipped as
> a `.py` file, and no result exists. Its **syntax** was checked by parsing it in memory (`compile()` only; no
> execution, no import, no file written). A future authorised run transcribes it verbatim into
> `code/stock_ner_d.py`, records that file's sha256 in the run manifest, and verifies the transcription
> line-by-line against this appendix. If the transcription differs, the run is void.

```python
#!/usr/bin/env python3
"""STOCK-NER-D: frozen stock-style NER object and its construct test (EXP-10).

Implements PRE_DECLARATIONS.md sections 3-6. Deterministic; stdlib only.
No RNG, no clock, no network, no environment dependence, no target-year operand.
"""
import argparse
import ast
import csv
import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EXT, "..", "..", ".."))
PANEL_REL = ("10_massification/extensions/synthetic_2026-11-20/"
             "generator_v1_2/results/synthetic_panel_v1_2.csv")
NER_PANEL_REL = ("10_massification/extensions/synthetic_2026-11-20/"
                 "generator_v1_2_addendum/results/synthetic_panel_v1_2_ner.csv")

DUR = {"primary": 6, "lower_secondary": 3, "upper_secondary": 3, "tertiary": 4}
YEARS = tuple(range(1970, 2026))
TEST_TYPES = (("T1", "SYN00_PHL_LIKE"), ("T2", "SYN28"))
THRESHOLDS = (90.0, 95.0)
BAND_LO, BAND_HI = 85.0, 95.0
BAR_PP = 2.0
BAR_Y = 1
EPS = 1e-9
OBJ_ID = "STOCK-NER-D/v1"
BANNER = ("SCALING: FAIL (standing, A12/B02) - "
          "DIAGNOSTIC-TRANSFER ONLY - NOT EVIDENCE")
LABELS = ("SYNTHETIC/DERIVED. No HKG result exists until one is produced; "
          "nothing here licenses a portability, capacity-timing, or "
          "phase-verdict claim.")
FORBIDDEN = ("PASS", "SUPPORTED", "VALIDATED", "REPRODUCED", "PORTABLE",
             "CONFIRMED", "HOLDS")


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def guard_target_isolation():
    """G6: the module must contain no literal for the two forbidden years.

    The forbidden values are assembled arithmetically so that this guard's own
    source never carries the literals it forbids.
    """
    forbidden = tuple(1900 + x for x in (74, 79))
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and not isinstance(node.value, bool):
            val = node.value
            if isinstance(val, int) and val in forbidden:
                hits.append(repr(val))
            elif isinstance(val, str) and any(str(y) in val for y in forbidden):
                hits.append(val[:40])
    return hits


def guard_manifest():
    """G1/G2: frozen spec and every cited input must match the manifest."""
    man = load_json(os.path.join(EXT, "RUN_MANIFEST.json"))
    if sha256_file(os.path.join(EXT, "PRE_DECLARATIONS.md")) != man["predeclaration_sha256"]:
        sys.exit("G1 FAILED: predeclaration hash mismatch -> BLOCKED-PRECONDITION")
    for rel, want in man["inputs"].items():
        if sha256_file(os.path.join(ROOT, rel)) != want:
            sys.exit("G2 FAILED: %s -> BLOCKED-INPUT" % rel)
    return man


def load_panel():
    """G3: schema guard, then index by (country, year, level)."""
    path = os.path.join(ROOT, PANEL_REL)
    rows = {}
    with open(path, "r", encoding="utf-8", newline="") as fh:
        rdr = csv.DictReader(fh)
        cols = rdr.fieldnames or []
        if len(cols) != 67:
            sys.exit("G3 FAILED: %d columns -> BLOCKED-INPUT" % len(cols))
        n = 0
        for rec in rdr:
            if rec["label"] != "SYNTHETIC":
                sys.exit("G3 FAILED: non-SYNTHETIC row -> BLOCKED-INPUT")
            rows[(rec["country"], int(rec["year"]), rec["level"])] = rec
            n += 1
    if n != 6720:
        sys.exit("G3 FAILED: %d rows -> BLOCKED-INPUT" % n)
    for _, c in TEST_TYPES:
        for t in YEARS:
            if (c, t, "primary") not in rows:
                sys.exit("G3 FAILED: missing %s %d -> BLOCKED-INPUT" % (c, t))
    return rows, path


def stock(rows, country, level, year):
    """The object (PRE_DECLARATIONS.md section 3.1). None on an incomplete window."""
    d = DUR[level]
    if year - d + 1 < YEARS[0]:
        return None
    s = float(rows[(country, year, level)]["survival"])
    num = 0.0
    den = 0.0
    for k in range(d):
        rec = rows[(country, year - k, level)]
        num += float(rec["admitted_official"]) * (s ** (k / float(d)))
        den += float(rec["cohort"])
    if not (math.isfinite(num) and math.isfinite(den)) or den <= 0.0:
        sys.exit("G5 FAILED: non-finite operand -> BLOCKED-INPUT")
    return 100.0 * num / den


def flow(rows, country, level, year):
    rec = rows[(country, year, level)]
    return 100.0 * float(rec["admitted_official"]) / float(rec["cohort"])


def series_for(rows, country, level):
    st, fl = {}, {}
    for t in YEARS:
        fl[t] = flow(rows, country, level, t)
        val = stock(rows, country, level, t)
        if val is not None:
            st[t] = val
    return st, fl


def first_sustained(ser, thr):
    ys = sorted(ser)
    for i in range(len(ys) - 4):
        if all(ser[ys[i + j]] >= thr for j in range(5)):
            return ys[i]
    return None


def first_at(ser, thr):
    for y in sorted(ser):
        if ser[y] >= thr:
            return y
    return None


def band_eval(st, fl):
    years = [t for t in sorted(fl) if t in st and BAND_LO <= fl[t] <= BAND_HI]
    if not years:
        return "UNDETERMINED", []
    out = []
    met = True
    for t in years:
        diff = st[t] - fl[t]
        ok = abs(diff) <= BAR_PP + EPS
        met = met and ok
        out.append((t, st[t], fl[t], diff, ok))
    return ("MET" if met else "NOT_MET"), out


def cross_eval(st, fl):
    detail = {}
    met_all = True
    for thr in THRESHOLDS:
        ys, yf = first_sustained(st, thr), first_sustained(fl, thr)
        if ys is None and yf is None:
            met, delta = True, None
        elif ys is None or yf is None:
            met, delta = False, None
        else:
            delta = abs(ys - yf)
            met = delta <= BAR_Y
        met_all = met_all and met
        detail[thr] = {"stock": ys, "flow": yf, "delta": delta,
                       "first_at_stock": first_at(st, thr),
                       "first_at_flow": first_at(fl, thr),
                       "result": "MET" if met else "NOT_MET"}
    return ("MET" if met_all else "NOT_MET"), detail


def decide(b1, b2, c1, c2):
    if "UNDETERMINED" in (b1, b2):
        return "BLOCKED-MEASURE(N2-EMPTY)"
    band_bad = "NOT_MET" in (b1, b2)
    cross_bad = "NOT_MET" in (c1, c2)
    if band_bad and cross_bad:
        return "BLOCKED-MEASURE(N2-BOTH)"
    if band_bad:
        return "BLOCKED-MEASURE(N2-BAND)"
    if cross_bad:
        return "BLOCKED-MEASURE(N2-CROSSING)"
    return "CONSTRUCT-EQUIVALENT"


def fmt(x):
    return "NA" if x is None else ("%.6f" % x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    hits = guard_target_isolation()
    if hits:
        sys.exit("G6 FAILED: %r -> FAIL-RE-FIT (not dispatched)" % (hits[:3],))
    if args.check:
        print("GUARDS OK")
        return
    if not args.out:
        sys.exit("usage: stock_ner_d.py --out DIR | --check")
    if os.path.exists(args.out):
        sys.exit("BLOCKED-STATE: output directory exists; refusing to overwrite")
    guard_manifest()
    rows, _ = load_panel()
    os.makedirs(args.out)
    results, comp, cross, verdicts = [], [], [], {}
    for tag, country in TEST_TYPES:
        st, fl = series_for(rows, country, "primary")
        b, band_rows = band_eval(st, fl)
        c, detail = cross_eval(st, fl)
        verdicts[tag] = (b, c)
        for t, sv, fv, dv, ok in band_rows:
            comp.append((country, t, fmt(sv), fmt(fv), fmt(dv), fmt(abs(dv)),
                         "TRUE", "TRUE" if ok else "FALSE", "TRUE", "VERDICT"))
        mx = max((abs(sv - fv) for _, sv, fv, _, _ in band_rows), default=None)
        results.append((tag, country, "primary", "B", "band_years",
                        "%d" % len(band_rows), "2.0", b, "Y", "SYNTHETIC"))
        results.append((tag, country, "primary", "B", "max_abs_diff",
                        fmt(mx), "2.0", b, "Y", "SYNTHETIC"))
        for thr in THRESHOLDS:
            d = detail[thr]
            results.append((tag, country, "primary", "C", "delta_years_%g" % thr,
                            "NA" if d["delta"] is None else "%d" % d["delta"],
                            "1", d["result"], "Y", "SYNTHETIC"))
            for name, yy in (("stock", d["stock"]), ("flow", d["flow"]),
                             ("first_at_stock", d["first_at_stock"]),
                             ("first_at_flow", d["first_at_flow"])):
                cross.append((tag, thr, name,
                              "none_by_2025" if yy is None else "%d" % yy,
                              "none_by_2025" if d[name] is None else "%d" % d[name],
                              "TRUE" if yy is not None else "FALSE",
                              "NA" if d["delta"] is None else "%d" % d["delta"],
                              "NA" if d["delta"] is None else ("TRUE" if d["delta"] <= BAR_Y else "FALSE"),
                              d["result"]))
        results.append((tag, country, "primary", "C", "crossing_aggregate",
                        "NA", "1", c, "Y", "SYNTHETIC"))
    verdict = decide(verdicts["T1"][0], verdicts["T2"][0],
                     verdicts["T1"][1], verdicts["T2"][1])
    results.append(("ALL", "ALL", "primary", "OVERALL", "verdict",
                    "NA", "NA", verdict, "Y", "SYNTHETIC"))
    with open(os.path.join(args.out, "STOCK_NER_RESULTS.csv"), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["object_definition_id", "test_type", "country", "level",
                    "condition", "statistic", "value", "threshold",
                    "component_result", "verdict_bearing", "label"])
        for row in results:
            w.writerow((OBJ_ID,) + row)
    with open(os.path.join(args.out, "STOCK_NER_COMPARISON.csv"), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["country", "year", "stock", "flow", "diff", "abs_diff",
                    "band_member", "bar_met", "stock_window_complete", "role",
                    "label"])
        for row in sorted(comp, key=lambda r: (r[0], r[1])):
            w.writerow(row + ("SYNTHETIC",))
    with open(os.path.join(args.out, "STOCK_NER_CROSSINGS.csv"), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test_type", "threshold", "series", "first_at_or_above",
                    "first_sustained", "defined", "delta_years", "le_1y",
                    "component_result", "label"])
        for row in cross:
            w.writerow(row + ("SYNTHETIC",))
    sens = []
    for country in sorted({key[0] for key in rows}):
        for level in ("primary", "lower_secondary", "upper_secondary", "tertiary"):
            s2, f2 = series_for(rows, country, level)
            b2, br2 = band_eval(s2, f2)
            if b2 == "UNDETERMINED":
                continue
            sens.append((country, level, len(br2),
                         fmt(max(abs(a - b) for _, a, b, _, _ in br2)),
                         sum(0 if ok else 1 for _, _, _, _, ok in br2),
                         "DESCRIPTIVE-SENSITIVITY", b2, "SYNTHETIC"))
    with open(os.path.join(args.out, "STOCK_NER_SENSITIVITY.csv"), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["country", "level", "years_in_band", "max_abs_diff",
                    "band_years_over_bar", "role", "component_result", "label"])
        for row in sens:
            w.writerow(row)
    with open(os.path.join(args.out, "STOCK_NER_VERDICT.txt"), "w",
              encoding="utf-8") as fh:
        fh.write(BANNER + "\n" + verdict + "\n" + LABELS + "\n")
    carrier = os.path.join(args.out, "STOCK_NER_VERDICT.txt")
    if BANNER not in open(carrier, encoding="utf-8").read():
        sys.exit("G7 FAILED: banner missing in the carrier file")
    for name in sorted(os.listdir(args.out)):
        text = open(os.path.join(args.out, name), encoding="utf-8").read()
        if name.endswith(".csv") and "SYNTHETIC" not in text:
            sys.exit("G7 FAILED: no SYNTHETIC label in %s" % name)
        for bad in FORBIDDEN:
            if bad in text.replace("TRANSFER-HOLDS", ""):
                sys.exit("G7 FAILED: forbidden string %r in %s" % (bad, name))
    print(verdict)


if __name__ == "__main__":
    main()
```

**Notes on the listing (all deliberate):**

1. **No `band_population`, no `admitted_overage`, no `ner*`** in the object path — the operand allow-list of
   `PRE_DECLARATIONS.md` §4.1 is the whole input.
2. **`--check` runs only G6** and prints `GUARDS OK`; it reads no data.
3. **The output directory must not pre-exist**; the run refuses to overwrite.
4. **G7 strips `TRANSFER-HOLDS` before the forbidden-string scan** because that token is part of the allowed
   `DIAGNOSTIC-TRANSFER` vocabulary and this run emits no transfer verdict at all.
5. **`results/STOCK_NER_SENSITIVITY.csv`** is written **after** the verdict token is fixed, over all 30
   countries × 4 levels, and its `component_result` is **display-only**: it must never be consulted before the
   token is written, and a run that lets it influence the token is void (§4.6 of the plan, §6.6 of the
   predeclaration).
6. The listing writes **no timestamp** anywhere, so two runs are byte-identical by construction (G8).

---

## Appendix B — full command sequence (copy-pasteable LATER; **not executed now**)

```bash
# 0. STOP unless a new Council decision authorises the construct test and gates A-E of §0 clear.
cd /Users/treymenefee/massification_live/experiments/massification-2026-11-20
D=10_massification/extensions/hkg_stock_ner_2026-11-20
PY="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"

# 1. freeze + input verification (section 2.1)
shasum -a 256 "$D/PRE_DECLARATIONS.md"
#   expect 6f5d3c169487f4b6e296e4bf1673ec0755e04499cf5d291c9ccd88089c73bb3e

# 2. HKG checklist section 2 (read-only, verbatim) -- expect ALL INPUTS MATCH,
#    99be01d7..., the two TC rows unchanged, and 10 OK + 1 known FAILED

# 3. transcribe Appendix A into code/stock_ner_d.py, then static guards
PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$D/code/stock_ner_d.py" --check
#   expect GUARDS OK

# 4. two runs (section 7), then byte-compare; expect five OK lines
PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$D/code/stock_ner_d.py" --out "$D/results"
PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$D/code/stock_ner_d.py" --out "$D/_determinism/run2"

# 5. read the token -- never edit a rule in response to it
cat "$D/results/STOCK_NER_VERDICT.txt"
```

**Nothing above has been executed. `results/` does not exist. No token has been produced.**
