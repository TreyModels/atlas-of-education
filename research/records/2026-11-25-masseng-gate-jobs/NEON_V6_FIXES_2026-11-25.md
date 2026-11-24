# NEON V6 / GATE-JOBS FIXES — 2026-11-25

**Branch:** `research/masseng-gate-jobs-neon-2026-11-25` (additive, local only, **not pushed**)
**Base:** `6728494` (WIP snapshot for external code review; head of `research/masseng-gate-jobs-2026-11-25`)
**Worktree:** `~/neon-boot/wt2/v6` (clean clone `/Users/treymenefee/neon-boot/repos/atlas`, no sparse-checkout)

Commits in this branch (each logical fix separate, explicit paths only, no `git add -A`):

| commit | fix |
|---|---|
| `3799152` | `labour.py`: fractional-mass vacancy clearing (audit item: fractional-mass vacancy / 4× over-hiring) |
| `bb46e3a` | `education/gate.py`: quota rejection channels no longer double-count below-bar mass (audit item: quota double-count) |
| `6b80c25` | `scripts/dashboard.py`: keep fractional formal share (measurement-layer follow-on; no re-binarisation) |
| `70f13b0` | `scripts/run_swaps.py`: T1b NaN handling, T5 swap arms, strict-JSON nan-safe dump |
| `c21bf3b` | record: this file (before/after numbers, tests, OPEN defects) |
| `fc2504d` | tests: restore labour test SUMMARY/non-zero exit after the file split (no production change) |

Branch head at handoff is the last commit in `git log -1` on the branch (reported to the Lead); this record-update commit follows the fixes.

Everything below is **SIMULATION** of a declared, illustrative toy model. No empirical calibration, no causal claim.
No result was edited to make a test pass; failures are preserved and reported (see §5).

## 1. What changed

### 1.1 `research/masseng-v6/masseng_v6/labour.py` — fractional-mass vacancy clearing
The old clearing called `ranked_admit` (mass-aware, admits a boundary cell partially) but then divided by mass,
turned the fraction into a boolean (`newly = (frac > 0) & mask`), marked the **whole cell** formally employed and
counted the whole cell's mass at the formal wage. With two 50-mass cells and 25 vacancies the formal share was
`1.0` — exactly **4×** the 25-mass vacancy stock.

Fixed behaviour:
- `ranked_admit` returns **admitted mass**; a cell can be hired partially. `LabourOutcome.formal` is now the
  expected share of each cell in formal work in `[0, 1]`; `income` is the expected annual income of one person.
- Both the queue and the competitive clearings are fractional; the vacancy stock cannot hire more mass than it holds.
- Queue status-year income is accumulated over the declared vacancy rounds (formal from the hire round on,
  informal from the informal round on, waiting support while queuing).
- `p_hire` is the declared belief "chance a queuer of credential c is hired this year": it is updated from the hires
  observed among the **previous round's waiters** (not from all eligible mass), kept in `[0, 1]`, asserted in code,
  and exposed on `LabourOutcome.p_hire` so the bound is auditable.
- The waiting decision is the **pre-registered deterministic threshold** (`PRE_REGISTRATION_GATE_JOBS.md`, declared
  model: "wait if expected formal-minus-informal gain over the horizon exceeds informal income"). The old code used
  an undeclared logit draw; with fractional mass the draw let early informal exits starve later vacancy rounds and
  the declared 25-vacancy stock did not clear. This is a behavioural change beyond arithmetic and is disclosed here
  rather than buried: no base result is claimed comparable to fixed-branch output.

### 1.2 `masseng_v6/education/gate.py` — quota double-count (FIXED)
In the quota branch, `cap_reject` was computed over **all** eligible cells although below-quota-threshold mass was
already recorded in `below_bar`. Probe: eligible 1000, admitted 300, rejected 700, `below_bar` 575 / old
`capacity_rejection` 700 → old channels sum **1275** (and 470+700=1170 in the 100-cell probe). Now `cap_reject` is
restricted to threshold-passers, so `below_bar + capacity_rejection + exam_fail == rejected_eligible` for all five
gate kinds.

### 1.3 `scripts/dashboard.py` — fractional formal share (FIXED)
`formal = np.asarray(d["formal"], bool)` re-binarised the expected-mass array, erasing a partial hire. Now read as
float; `formal_share`, per-credential and per-quintile read-outs stay fractional.

### 1.4 `scripts/run_swaps.py` — T1b NaN handling, T5 swap arms (FIXED)
- **T1b** correlated ability among admitted cells with their own all-ones admission indicator: zero variance, so the
  control returned `NaN` on every seed and could never fail. Now the point-biserial correlation
  `corr(ability, admitted)` over the gate-2 eligible (in-school) pool; degenerate pools (none admitted / all
  admitted / constant ability) return a declared `0.0` with counts recorded, never `NaN`.
- **T5** structural multiverse rebuilt as four pairwise-distinct, name↔params-matched arms. Old dict: `multi_bar_concave` was
  verbatim `multi_prep_concave` (duplicate) and `multi_quota_tullock` set no non-default field (no tullock rule,
  `prep_form="linear"` is the default) — a no-op. New declared arms (prep-return form × tertiary gate rule):
  `multi_bar_concave` (bar, concave), `multi_quota_concave` (quota, concave), `multi_tullock_linear` (tullock,
  linear), `multi_tullock_concave` (tullock, concave); base cell (bar, linear) is the reference and is already the
  baseline run.
- ABC truth moments are nan-safe; every non-finite float is written as JSON `null` (`allow_nan=False`), so
  `swaps_raw.json` has zero `NaN`/`Infinity` literals.

## 2. Test evidence (self-contained, numpy only, no pytest)

Tests live in `tests/`. Base comparison runs the same files against an untouched base-6728494 checkout
(model dir = base `research/masseng-v6`, scripts dir = base `scripts/`).

```
cd research/records/2026-11-25-masseng-gate-jobs
python3 tests/test_labour_fixes.py       # fixed 8/8   | base 1/8  (base formal_share 1.0)
python3 tests/test_gate_fixes.py         # fixed 4/4   | base 2/4  (base channels 1170 vs 700)
python3 tests/test_dashboard_fixes.py    # fixed 3/3   | base 2/3  (base 0.5 input -> 1.0)
python3 tests/test_run_swaps_fixes.py    # fixed 7/7   | base 3/7  (base T1b NaN, T5 duplicate, no strict JSON)
```

Base-comparison invocation:
`python3 tests/<file>.py --model-dir <BASE>/research/masseng-v6` and, for the runner/dashboard files,
`GJ_SCRIPTS_DIR=<BASE>/scripts MASSENG_MODEL_DIR=<BASE>/research/masseng-v6 python3 tests/<file>.py`.

Key before/after numbers:

| check | base (6728494) | fixed |
|---|---|---|
| queue: 25 vacancies / two 50-mass cells (`cred=[3,3]`) | `formal_share = 1.0`, allocated mass 100 (4×) | `0.25`, allocated mass 25 |
| competitive: same case | `1.0`, 100 (4×) | `0.25`, 25 |
| over-hiring across 80 configs (queue+competitive, 4 credentials × 5 vacancy rates × 2 mass splits) | violations (up to 100 mass on ≤60 vacancy stock) | 0 violations |
| quota channels vs `rejected_eligible` | 1170 vs 700 | 700 vs 700 |
| all gate kinds: channels reconcile | quota fails | all pass |
| dashboard on a synthetic 0.5 fractional formal input | 1.0 (re-binarised) | 0.5 |
| full model through dashboard | `formal_share = 0.25` | `0.25` |
| T1b ability-admission corr (seeds 0/1/2) | `NaN, NaN, NaN` | full `0.368, 0.366, 0.374`; zero-selection `−0.0055, −0.0057, 0.0061`; prep 0 |
| T5 arms | 2 duplicates + 1 no-op/name mismatch | 4 distinct, name↔params matched |
| `swaps_raw.json` | no sanitiser (NaN literals) | 0 `NaN`/`Infinity` literals |

`p_hire ∈ [0,1]` is asserted in `labour.py` and checked from `LabourOutcome.p_hire` (test T3).

Existing tests in the model tree (no existing tests in this record directory): `pytest` is not installed system-wide,
so it was installed to a temporary `/tmp/pytestlib` for the run only (no repo change).
`tests/test_accounting.py` + `tests/test_admissions.py`: **24 passed**. Two files fail collection for a pre-existing
reason unrelated to this branch — `tests/test_array_admissions.py` and `tests/test_engine5_array.py` import
`masseng.data`, which is absent from this tree. **Preserved failure, not caused by these fixes.**

## 3. End-to-end runner smoke (SIMULATION, not a result)

Copied the fixed scripts to `/tmp/swaptest` (so the record directory is not polluted) and ran:

```
MASSENG_MODEL_DIR=<repo>/research/masseng-v6 /Users/treymenefee/neon-boot/venv/bin/python run_swaps.py \
    --workers 8 --abc-draws 40 --out /tmp/swaptest/results/swaps_raw.json
```

Result: **310/310 model runs returned, `errors=0`**, wall 175.57 s, 8 workers, Python 3.10 / numpy 2.2.6,
output 1.36 MB; **0 `NaN` and 0 `Infinity` literals**, strict `json.loads(..., parse_constant=raise)` passes;
31 arms × 10 seeds; T5 contributes 40 runs with finite headline moments; `T1a max diff = 0.0`;
`T1b corr full/zero = (0.368,−0.006), (0.366,−0.006), (0.374,0.006)`.
Output file is in `/tmp` only; **no results are claimed** from this WIP prototype.

## 4. OPEN defects (not fixed here; file:line)

1. **`_record()` spend double-count when `spend_feedback=False` — OPEN.**
   `research/masseng-v6/model/masseng/tutoring.py:311` (`_record`), especially `:326` (`spend_tut_d`) and
   `:333` (`spend_d = spend_d + spend_tut_d`); contrast `_v` at `:288-299`, which adds tutoring outlay to the
   household burden **only** when `spend_feedback=True`. With `spend_feedback=False` the model's cost excludes the
   outlay, yet reported `edu_share_hh`/`edu_share_bottom30`/… add it on top of the fitted `c_scale` schedule that
   was calibrated to FIES *total* household education spending — the double count is documented as a warning in
   `research/records/2026-11-25-masseng-tutoring/MASSENG_TUTORING_COUPLING.md:90-99`. Fixing means deciding whether
   `c_scale` is all-in (then report-only, no addition) or additional (financing arm) — a definition/claim change,
   so it is **not** silently rewritten.
2. **MNL price/option mismatch vs Bray — OPEN.**
   The port (`research/masseng-v6/model/masseng/tutoring.py:17-21` spec; implementation `:230-235`, spending `:252-254`)
   uses **four** options and a **full** `price_other·fee` on the other-teacher option (plus a commercial option and a
   spending sum). The fitted Bray reality check it claims to port (`research/records/2026-11-25-masseng-tutoring/ported/bray_reality_check.py:87-93`)
   uses **three** options with the other-teacher utility entering `−0.5·price_fee` and no commercial utility. The
   "closest-to-Bray" defaults (`tutoring.py:74-83`) were fit under the standalone specification, so the port's demand
   mix is not the object that was validated against the seven published Bray patterns. Claim text unchanged; needs a
   re-fit in the port specification or an explicit caveat amendment (owner decision).
3. **Quota double-count — FIXED** (`gate.py`, commit `bb46e3a`).
4. **Tullock invariance — OPEN / unadjudicable (no declared invariance property).**
   `research/masseng-v6/masseng_v6/education/gate.py:142-162` implements
   `P_i = sigmoid((score_i − threshold)/scale)` with proportional allocation capped by cell mass. Probes (tests
   `G3/G4`): invariant to `(mass, capacity)` scaling (max rel diff `5.5e-16`) and to cell splitting (`0.0`); **not**
   invariant to a common score translation with the fixed absolute threshold (max cell diff `0.50`). A softmax form
   would be translation-invariant but that is a change of the **declared functional form**, i.e. a claim change, so
   it is reported here instead of changed. Also cosmetic: `scripts/model_blocks.py:219-220` folds tullock
   rejections into reject-reason 1 ("capacity"); not relabelled.
5. **v6 not wired to the runner — OPEN by design.**
   `research/masseng-v6/masseng_v6/core/runner.py:20-46` (`run_admissions_year`) implements only annual admissions
   transitions and imports neither `education.gate` nor `labour`; the prototype is driven by the record script
   `research/records/2026-11-25-masseng-gate-jobs/scripts/model_blocks.py:22-23,196-244`. The pre-registration
   declares the v6 skeleton untouched; wiring gate/labour into `core/runner.py` would be a scope and accounting
   change, not a code-bug fix. OPEN.

## 5. Preserved failures / top risk

- Preserved: the two pytest collection errors above (pre-existing missing `masseng.data` in this tree); base-code
  failures in every test file are kept in the base comparison, not tuned away.
- **Top risk:** the queue waiting decision and `p_hire` belief update are behavioural changes, not just arithmetic.
  They were required for the pre-registered 25-vacancy clearing invariant to hold with fractional mass (the
  declared deterministic waiting rule could not be implemented on the old whole-cell status arrays), but it means
  base vs fixed queue output (`queue_share`, pay mixture, formal shares beyond the invariant) is **not comparable**,
  and no base v6 number should be carried forward. The default wait horizon/support parameters are still declared,
  unestimated, and now more visible in the output.
