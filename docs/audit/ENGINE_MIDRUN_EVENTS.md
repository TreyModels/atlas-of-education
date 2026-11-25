# ENGINE_MIDRUN_EVENTS — calendar `events`/`paths` audit and the "inert fee abolition" defect

Owner: `engine-core` · date 2026-11-25 · branch `research/contest-audit-v2-2026-11-25`
Trigger: Lead/Commander finding that a calendar `events` change `fee_public → 0` at year 2006 is logged but the
attendance path looks bit-identical to persistence (Forecast (e) BLOCKED). Status: **ROOT CAUSE FOUND + ENGINE
DEFECT FIXED**; the attendance/fee *channel* itself is correct.

## 1. Repro and verdict

Forecast-(e) declared world (`/tmp/forecast_holdout_v2.py` on the host: `T0=16`, `T=T0+8`, `start_year=1990`,
`N=300`, `entry_age=6`, `subsist=0.60`, `borrow=0`, `y_median=0.8`, `gates=bar(-1e9)`, `seed=0`, `fee_public=0.15`).
Primary attendance proxy = `att_by_grade[:, :6].sum(1) / (6·N) · 100`.

| run | `fee_public` at end | `event_log` | primary attendance, t = 14 … 22 |
|---|---|---|---|
| A persistence (fee 0.15, no event) | 0.15 | `[]` | **58.61, 59.44, 60.39, 61.17, 60.39, 60.67, 61.11, 60.22, 60.22** |
| B "abolition" `year=16` (the forecast script) | 0.15 | `[]` | **identical to A (bit-identical arrays)** |
| C abolition `year=2006` (calendar year) | 0.00 | `[(2006, 'fee abolition', …)]` | 58.61, 59.44, **77.00, 81.44, 82.56, 85.00, 85.50, 86.67, 85.28** |
| D static fee 0.0 | 0.00 | `[]` | 58.61, 59.44, 84.22, 85.11, 84.28, 84.89, 84.67, 85.67, 85.33 |

The quoted persistence series (58.61, 59.44, 60.39, 61.17, …) is exactly run A. **Run B never fires:** the engine
matches calendar years, and `16 ≠ 1990 + 16`. So the "bit-identical attendance" is the correct behaviour of an
event that never happened, not a broken attendance path: with the correct calendar year (C) attendance jumps from
60.4 % to 77.0 % at t=16 and approaches the static-abolition path. **The fee/attendance/continuation channel is
intact.** The engine defect was that run B passed silently (no warning, no error). A separate check with
`year=2006` fires and logs — that is the check that produced the "event is applied" observation.

## 2. Root cause, with anchors

* Forecast scripts (`/tmp/forecast_holdout.py` L33/L41/L53 and `/tmp/forecast_holdout_v2.py` L30/L37/L47):
  `T0 = 12` (v1) / `T0 = 16` (v2), `BASE … start_year=1990`,
  `p['events'] = [dict(year=T0, set=dict(fee_public=0.0), …)]`. `year=T0` is a **simulation index**, and it is
  then also used as `r[T0+e]`/`rate_at(E, T0+e)`; the event spec forgot to convert it to a calendar year.
* Engine: `Engine.apply_calendar` (`engine/eduengine/core.py:865`) computes `Y = self.year(t) = start_year + t`
  (`core.py` `year()`) and fires an event when `ev['year'] == Y` (`core.py:873` in the fixed version; previously
  `core.py` L808: `if ev['year'] == Y`). Events are documented as calendar years (see `engine/policy.py`
  L83/L88: "others are set by an event in `year`", with `year` a calendar year), but the engine never checked that
  a scheduled event can be reached: **an unreachable year was a silent no-op**. That is the defect: not the
  attendance path, but the absence of a loud failure mode for a dead calendar event.
* Why it blocked Forecast (e): the abolition arm was bit-identical to persistence by construction, so the
  "forecast" had a mechanical zero effect and was correctly flagged invalid — the arm never ran.

## 3. Engine fix (new engine hash; numerics unchanged)

Committed with this document (`core.py`):

1. `EVENT_CACHED_PARAMS` (`core.py:91`) and `Engine._validate_events` (`core.py:304`), called at the end of
   `Engine.__init__` (and again if an event itself replaces `p['events']`). It emits a `UserWarning` when:
   * an event year **falls outside the simulated calendar window** `[start_year, start_year + T - 1]`
     ("…it will never fire. Events match calendar years (start_year + t); use `year_t=<t>` for a simulation-index
     year."),
   * an event sets a **construction-cached parameter** (`EVENT_CACHED_PARAMS` = `levels`, `child_wage`, `seed`,
     `T`, `measure_from`) — `p.update` accepts it but the simulation cannot change,
   * an event sets a parameter that also has a **`paths` entry** — paths are re-applied every year, so the event
     is a one-year override only.
   Unreachable `(year, label)` pairs are also kept in **`E.unfired_events`** so runners/tests can assert
   `E.unfired_events == []`.
2. **`year_t`**: an event may specify `dict(year_t=<t>)` instead of `dict(year=<calendar year>)`
   (`apply_calendar`, `core.py:873`). Exactly one of the two is allowed; both together raise `ValueError`; neither
   warns. `year_t` and the equivalent calendar year produce **bit-identical** runs.
3. **Numerics are unchanged.** A/B run of the same 118-series signature (all `E.R` series + `E.ALL` arrays,
   real TutoringMarket, KR-TRACKED, N=60/T=20) under `core.py @ f31e176` vs the fixed `core.py`: **all 118 series
   identical (NaN-aware)**. The fix is validation + an additive event schema, not a behavioural change.
   New engine hash: `engine/eduengine/core.py` sha256 `e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71`
   (was `72cbddf7…` in `docs/audit/canonical_spec.json`); the Canonical Spec must be re-pinned to this commit by the
   Commander before Gate-2 runs consume it.
4. Warnings, not errors, by design: several short-horizon smoke configs (country packs with `T=10`) schedule
   events beyond their horizon; raising would break them. Runners that must not silently lose an arm should assert
   `E.unfired_events == []` after `run()`.

## 4. How to implement a mid-run fee abolition correctly

Any of these, in order of preference:

1. **Calendar year** (explicit): `events=[dict(year=start_year + t0, set=dict(fee_public=0.0), label='fee abolition')]`.
   For the forecast (e) scripts this is `year=int(BASE['start_year']) + T0` (1990+16 = 2006 in v2; 1990+12 = 2002 in v1).
2. **Simulation index** (new): `events=[dict(year_t=t0, set=dict(fee_public=0.0), …)]` — converted internally to
   `start_year + t0`; equivalently bit-identical to (1).
3. **If the parameter also has a `paths` entry**, an event is only a one-year override because `apply_calendar`
   re-applies the path every year before the events (`core.py:868-873`). For a *persistent* change, rewrite the
   path from `t0` on — exactly what `engine/policy.py` `apply()` does for `kind='path'` levers
   (`path = [(y,x) for y < Y] + [(Y-1, …), (Y, new)] + [(y, new transformed) for y > Y]`).

Always assert `E.unfired_events == []` for every arm after `run()`.

## 5. Audit: which other `events`/`paths` parameters are inert mid-run?

Sweep: small contest world (`N=60`, `T=18`, `start_year=0`, event at calendar year 9), signature = every `E.R`
series + every `E.ALL` array; reproduce with
`PYTHONPATH="$PWD/engine" venv/bin/python docs/audit/ENGINE_CHECKS.py --events-audit`.

| class | parameters | mid-run behaviour |
|---|---|---|
| **PROPAGATES** (as intended) | `fee_public`, `fee_tertiary`, `budget_per_child`, `pay_ratio`, `own_ban`, `firm_ban`, `p_own`, `p_firm`, `tut_effect`, `subsist`, `borrow`, `y_median`, `y_sigma`, `y_growth`, `shock_sigma`, `q0`, `beta_a`, `home_effect`, `ses_home`, `learn_noise`, `tau`, `delta`, `kappa`, `prior_logw`, `elite_logw`, `contest_r`, `contest_alpha`, `contest_price`, `contest_x0`, `contest_max_e`, `entry_age`, `promote_bar`, `exam_sd`, `rural_cost`, `belief_decay`, `need_max`, `poverty_line`, `vac0`, `vac_growth`, `skilled_share`, `w_skilled`, `theta_L`, `signal_rho`, `queue_on`, `rank_routine`, `tutor_jobs`, `gates`, `start_year`, `level_open`, `paths` | re-read every year by core/modules; a calendar event changes the path from that year |
| **INERT — cached at Engine construction** | `levels` (→ `ends`, `nlev`), `child_wage` (→ `self.cw`), `seed` (→ `EventRNG`), `T` (run loop), `measure_from` (summaries) | **now warns** (`_validate_events`); cannot be changed mid-run — build a new Engine |
| **INERT — config-dependent / measurement-only** (expected, not defects) | `monitoring` (no withholding when `own_ban=0` or `sell=0`), `max_entry_age`, `entry_share` (only the anchoring fallback uses it), `gate_retakes` (no failing gate in the test arms), `kin_support`/`street_age` (no street events in this world), `floor0` (floor adaptation not binding), `mpl_primary`/`mpl_lower` (measurement thresholds only) | propagate whenever their channel is active; e.g. `monitoring` changes withholding in `own_ban>0` worlds |
| **SAFE-BUT-DANGEROUS** | `N` mid-run | propagates into `add_cohort`/seats but breaks `pid = t*N + arange(N)` uniqueness and planned-seat denominators; do not change `N` mid-run (no warning yet, documented) |

`paths` themselves are applied every year; they propagate. Events are applied *after* the path application in the
same year (`core.py:868-878`), hence the one-year-override caveat for path-shadowed parameters.

## 6. Gate-grid / Paper A(c) fee arms: NOT affected

`papers/shadow-education-contest/code/run_gate_architecture.py` builds engines from `canonical_spec.json`
`params.KR.primary`, which has **no `start_year`**, so `start_year = 0` (CORE default) and the pre-registered
`events=[dict(year=T0=12, …)]` is a valid calendar year. Verified: for the fee-0 cells
`E.event_log == [(12, 'fee abolition', {'fee_public': 0.0})]`; for fee-0.19 cells `event_log == []`. The 5,120-run
gate-architecture fee arms do not need a rerun for this defect. (If a future canonical spec sets a non-zero
`start_year`, those arms must switch to `year_t`.)

## 7. Forecast (e) rerun recipe

1. In `forecast_holdout{,_v2}.py`: replace `dict(year=T0, …)` with `dict(year_t=T0, …)` (or
   `dict(year=int(BASE['start_year']) + T0, …)`).
2. After every `E.run()`, `assert E.unfired_events == []`; log `E.event_log` in the result JSON.
3. Re-run `calibrate()`: the first defect (v2) also blocked the pre-period calibration because the abandoned
   arms were identical; with the event fixed the engine is fee-sensitive in the declared world
   (fee 0.15 → ≈59–60 % primary attendance; fee 0.0 → ≈84–85 %; the 74.88 % author anchor is bracketed by the fee grid
   [0, 0.15] (≈59 % at 0.15, ≈84 % at 0), so it is feasible in this world — re-check the v2
   "CALIBRATION_FAILED" verdict under the corrected arm).
4. Expected abolition effect in the declared world: +17 pp at the first horizon (t=16: 60.4 → 77.0) rising to
   ≈+25 pp by e=+6; persistence = 0 by construction. Report per-horizon with the 40 matched seeds and the
   held-out horizons, as pre-registered.
5. The old forecast (e) numbers remain EXPLORATORY-INVALID / not cited; this document only removes the mechanical
   reason the arm could not run.

## 8. Residual risks

* Warnings can be ignored: a runner that neither asserts `E.unfired_events == []` nor fails on warnings can still
  lose an arm silently (the fix makes it detectable, not impossible).
* `N` changes mid-run are not warned; `paths`-shadowed event overrides last one year (warned but legal).
* The canonical spec's `engine_file_sha256['engine/eduengine/core.py']` now points at the fixed hash; all Gate-2
  result manifests must state the new engine commit once the Commander re-pins it.
* Numerics of the fix: unchanged (118-series A/B identical), so previously produced Gate-1/paper results are not
  invalidated by this commit; the forecast fix is a runner-side change plus the new hard-to-ignore warning.
