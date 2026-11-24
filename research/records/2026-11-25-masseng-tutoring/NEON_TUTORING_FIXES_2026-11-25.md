# NEON TUTORING FIXES — 2026-11-25

**Branch:** `research/masseng-tutoring-neon-2026-11-25` (additive; created off the base below, base not rewritten)
**Base:** `b9d68c1` (head of `research/masseng-tutoring-2026-11-25`)
**Worktree:** `~/neon-boot/wt3/tut` — clean clone `/Users/treymenefee/neon-boot/repos/atlas` (no sparse-checkout)
**Code+tests commit:** `8dd85b5` (this record commit follows; branch head is the last commit in `git log -1`)
**Host-only:** no box, no GPU, no server, no power/shutdown commands, no push.

Everything here is **SIMULATION** of a declared, illustrative coupled model. No empirical or causal claim.
No committed result was edited or regenerated to make a test pass; pre-fix artifacts are preserved and flagged below.

## 1. Fixes (Neon's three named defects)

### 1.1 `_record()` spend double-count when `spend_feedback=False` — **FIXED**
File: `research/masseng-v6/model/masseng/tutoring.py`, `TutoringModel5._record` (now lines 388–448; old code
`spend_d = spend_d + spend_tut_d` was the single unconditional line at old line 333).

Before: household education spending was always reported as *fitted direct-cost schedule + tutoring outlay*, in both
arms. The fitted `c_scale` schedule was matched to FIES **total** household education spending, which already
contains shadow-education outlays (the warning is in `MASSENG_TUTORING_COUPLING.md` §3.1). In the learning-only arm
(`spend_feedback=False`) that means the same household spending is counted twice: the schedule is read as all-in and
the outlay is added on top again.

After: two declared flows, each counted exactly once —
`spend_school_d` (fitted direct-cost schedule × enrolled persons) and `spend_tut_d` (declared tutoring outlay),
`spend_incl_d = spend_school_d + spend_tut_d`. The reported total `spend_d` is the inclusive total in the financing
arm (`spend_feedback=True`, outlay declared **additional**) and the schedule only in the learning-only arm
(`spend_feedback=False`, schedule read as all-in); the outlay is still reported separately. New outputs expose the
decomposition: `spend_school_share_gdp`, `spend_total_share_gdp`, `spend_incl_share_gdp`,
`edu_share_hh_incl_tut`; `tut_spend_share_hh_edu` now uses the inclusive total as denominator.

Before/after (uncalibrated anchor, identical fit, 2010 / 2024; `edu_share_hh` in % of household consumption):

| arm | before 2010 | after 2010 | before 2024 | after 2024 |
|---|---|---|---|---|
| learning-only (`spend_feedback=False`) | 6.0430 | **4.9709** | 7.8440 | **6.6252** |
| `edu_share_hh_incl_tut` (new; both arms) | — (not available) | 6.0430 | — | 7.8440 |
| financing (`spend_feedback=True`) | 4.6867 | 4.6867 (unchanged) | 6.8512 | 6.8512 (unchanged) |

Difference in the learning-only arm equals exactly the outlay share of consumption (0.7719/0.72 = 1.0721 pp at 2010;
0.8775/0.72 = 1.2188 pp at 2024) — i.e. the removed second count, not a behaviour change. The financing arm and the
smoke run's default arm are numerically unchanged.

### 1.2 MNL price/option mismatch vs Bray — **LEFT OPEN, now declared and measurable** (chosen deliberately)
Files: `research/masseng-v6/model/masseng/tutoring.py` (`BRAY_CHECK_MAPPING`/`PORT_MAPPING` lines 95/102,
`bray_mapping_gap()` line 181, new module-docstring section); reference
`research/records/2026-11-25-masseng-tutoring/ported/bray_reality_check.py:87-93`.

The `bray_8k` parameter vector was fitted under the standalone **three-option** mapping
`none/own/other`, with the other-teacher option entering as `-0.5·price_fee` and **no** commercial option. The port
(`_level_utilities`) is **four-option** `none/own/other/commercial`, charged at `-price_own·fee` and
`-price_other·fee` (`price_other = 0.8`), with a commercial option absent from the fit.

Why left OPEN rather than "aligned": aligning the coefficient alone (`0.8 → 0.5`) still cannot reproduce the fitted
object because the option set differs (4 vs 3, plus the commercial option), and changing the option set would change
the pre-registered four-option claim text. Per instruction the claim text is **not** silently rewritten; instead the
two mappings are declared in code and `bray_mapping_gap()` measures the gap (own: 0; other: **−0.30 logit** at
`fee = 1.0`, scaling with fee; commercial option: fit False / port True). Default behaviour is unchanged. A re-fit of
the vector in the port specification (or an explicit claim amendment) is required to close this; that is an owner
decision, not a code-only fix.

### 1.3 `1940–2024` label error — **FIXED (label corrected and stated)**
Files: `research/records/2026-11-25-masseng-tutoring/MASSENG_TUTORING_COUPLING.md` (§1 and §6.1);
`research/masseng-v6/model/masseng/tutoring.py` (module-docstring "Window labels" section and
`SIMULATED_WINDOW`/`OBSERVED_DATA_WINDOW`/`FIT_WINDOWS`, lines 87–89).

Before: the record said the model is "of the Philippine school system (1940–2024), fitted to PHL targets", which
reads as the **data** window. After: the record states the model **simulates** 1940–2024 (85 years), with 1940–1959
back-cast from the 1960 WDI levels using the configured pre-data growth and **not observed data**; the observed data
window used by the fit is **1960–2024** for the macro series (education enrolment/private series start **1971**;
Gini 1985–2023); the fit windows are **train 1971–1995, test 1996–2024** (`countries/PHL/config.json`).
`§6.1` now reads "simulated window 1940–2024 (85 years; observed data 1960–2024, 1940–1959 back-cast)".

Generated artifacts (`results/tables.md`, `results/summary.json`, committed result JSON) were **not** edited or
regenerated; they predate the label and accounting fixes and carry the old label/numbers (see §4).

## 2. Test evidence (fail on base, pass on branch)

New self-contained test file: `research/records/2026-11-25-masseng-tutoring/tests/test_tutoring_fixes.py`
(the model package imports scipy through `masseng.data`, so run it with a scipy-enabled Python — this session used
`/Users/treymenefee/neon-boot/venv/bin/python`, Python 3.10, numpy 2.2.6, scipy 1.15.3).

```
cd research/records/2026-11-25-masseng-tutoring
<scipy-python> tests/test_tutoring_fixes.py                     # branch: 3/3 PASS, exit 0
<scipy-python> tests/test_tutoring_fixes.py \
    --model-dir <base b9d68c1 checkout>/research/masseng-v6/model  # base: 0/3 PASS, exit 1
```

- **S1 spend single-count** (base FAIL / branch PASS): runs the coupled model for `spend_feedback=True` and `False`
  and asserts, at 2010 and 2024, that `spend_incl_share_gdp == spend_school_share_gdp + tut_spend_share_gdp`
  (once each), that the reported total is the inclusive total in the financing arm and the schedule only in the
  learning-only arm, that `edu_share_hh == reported_total / household-consumption share`, and that
  `edu_share_hh_incl_tut == inclusive_total / household-consumption share`. Base lacks the decomposition outputs
  (`spend_school_share_gdp`, `spend_incl_share_gdp`, `spend_total_share_gdp`, `edu_share_hh_incl_tut`) → FAIL.
- **S2 MNL vs Bray explicit OPEN deviation** (base FAIL / branch PASS): asserts the declared mappings
  (check = 3 options, other coefficient 0.5, no commercial; port = 4 options, `price_other` 0.8, commercial) and that
  `bray_mapping_gap()` reports `own_gap = 0`, `other_gap = −0.30` at fee = 1 and `−0.60` at fee = 2.
  Base has no declared mapping objects → FAIL (ImportError).
- **S3 window labels** (base FAIL / branch PASS): asserts `SIMULATED_WINDOW ==
  (config v5.years.simulate_from, simulate_to)`, `FIT_WINDOWS == config years.train/test`, that the observed macro
  series actually start in 1960 and education series in 1971 and the raw series extend to 2025, and that the record
  text says "simulates 1940 …" / "observed data window" and does **not** call 1940–2024 the fitted data window.
  Base has no declared label objects → FAIL (ImportError).

Base-count: **0/3 PASS, exit 1** (3/3 FAIL); branch: **3/3 PASS, exit 0**.

Existing module checks on the fixed tree (host-only):

- `scripts/smoke_coupling.py` — exit 0; calibrated anchor `b0` unchanged; default (financing) arm numbers identical
  to the pre-fix run: `edu_share_hh` 4.895 / 5.121 / 7.150 (2010/2018/2024), `tut_spend_share_gdp` 0.422 / 0.518 /
  0.608, `tut_participation` 0.524 / 0.609 / 0.667; fee grid and ban-own demand responses unchanged.
- `scripts/verify_switch_off.py` — **IDENTICAL**: full run 85 years, **318 comparisons**, all byte-identical;
  short run 25 years, **138 comparisons**, all byte-identical. (The script writes `results/switch_off_identity.json`;
  that generated change was **restored**, not committed, to avoid touching committed artifacts.)

## 3. What was deliberately left OPEN (and why)

1. **MNL price/option mismatch vs Bray** — OPEN (§1.2). Ambiguous: the shared-option price coefficient can be
   aligned, but the fitted object was 3-option and the port is 4-option with a commercial option, so an "alignment"
   would require re-fitting the vector in the port specification or changing the declared/claimed model. Per
   instruction the claim text was not touched; the mismatch is made explicit in code, in this record, and by a
   regression test that measures it. Any future closure must re-fit and update the claim with a declared deviation.
2. **Financing-arm outlay** remains declared *additional* to the FIES-all-in-calibrated schedule
   (`spend_feedback=True`). This is the declared arm, not an accounting bug; it is documented in
   `MASSENG_TUTORING_COUPLING.md` §3.1 and unchanged here.
3. The gate-jobs v6 items (Tullock invariance, v6 wiring, etc.) are not on this branch — they were handled on
   `research/masseng-gate-jobs-neon-2026-11-25`.

## 4. Preserved failures / artifacts (not edited)

- `results/summary.json`, `results/channel_decomposition.json`, `results/tables.md`, `results/MANIFEST.sha256`,
  `RUN_REPORT.md` and the `MASSENG_TUTORING_COUPLING.md` result tables were **not regenerated**. Consequences:
  the committed learning-only `edu_share_hh` numbers (e.g. §6.2 / `tables.md` arm rows) are the old
  schedule+outlay figure (6.043 / 7.844 at 2010 / 2024 in the uncalibrated-anchor probe), i.e. they equal the new
  `edu_share_hh_incl_tut`; the arm-consistent post-fix learning-only figure is 4.971 / 6.625. Any future run
  regenerates them consistently. They are preserved here as pre-fix artifacts rather than silently rewritten.
- No failure of the fixed tests or of the two module checks was observed; base-code failures are kept in the
  fail-on-base comparison, not tuned away.

## 5. Reproduction notes

- Base comparison tree: base `b9d68c1` model package (contents identical to the verifier's untouched snapshot);
  tests are parameterised with `--model-dir` / `MASSENG_MODEL_DIR` for exactly this purpose.
- Environment: host-only `venv` Python 3.10 / numpy 2.2.6 / scipy 1.15.3. The model's `masseng.data` requires scipy;
  system Python lacks it. No package was installed into any environment for this fix (the venv already had scipy).
- Rule compliance: additive commits on a new branch off the stated base, explicit paths, base never rewritten,
  no push, no server/box, no power commands, no result edited to pass a test.
