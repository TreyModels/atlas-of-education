# TUNE LOG — v1.3 shadow module (design phase, unflattering and complete)

**LABEL: SYNTHETIC.** This is a build record, not a result. It lists every design-phase change, every bug I
found, what I saw *before* each change, and what I did **not** change. The frozen parameters and thresholds were
never touched: they belong to `shadow_module/PRE_DECLARATIONS.md`, which this worker hashed and did not edit.

Timeline: 2026-11-20 22:56 – 23:1x (+08:00). Frozen spec verified at the start; the delivered scored run is the
last one in this log.

---

## D0 — Read the frozen spec; verified its hashes (22:56)

Read, in order: `PRE_DECLARATIONS.md`, `PRE_DECLARATIONS_S1_NOTE.md`, `SHADOW_MODULE.md`, `PARAMETERS.csv`
(42 rows), `DRY_RUN_PLAN.md`, `toy_design_check.py`, then v1.2 (`sim_v1_2.py`, `PARAMS.md`, `FINDINGS.md`,
`TUNE_LOG.md`, `RUN_MANIFEST.json`, panel), then `MODEL_ARCHITECTURE.md` A1–A4.

```
cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2  shadow_module/PRE_DECLARATIONS.md
af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb  shadow_module/PRE_DECLARATIONS_S1_NOTE.md
61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c  generator_v1_2/code/sim_v1_2.py
14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac  generator_v1_2/results/synthetic_panel_v1_2.csv
```

Both frozen hashes matched the values recorded in the module's `RUN_MANIFEST.json`. No v1.2 file was modified.

## D1 — State probe, and the first uncomfortable fact (22:57)

I printed the 2020 gate-state extents of all 30 v1.2 countries (a read-only probe, `_scratch/`), to size the
gate-state extractor. **What I saw first:** at upper-secondary entry (`g2`) every country has `Q ≈ 0.5`,
`π⁰ ≈ 0.9–0.999` and `κ ≈ 1.0`, so `R ≈ 1.15–1.43`; the tight gates are `g4` (job) and, for poor systems,
`g3` (tertiary). That made an eventual `c4a` FAIL easy to anticipate *before* the shadow equation was ever
evaluated, because the HKG anchor is measured exactly at `g2`.

I did **not** change any parameter (I have no authority to; they are frozen). I did **not** choose the host
countries on this information — see D2. This disclosure matters: the design phase was not blind to the input
state, only to the shadow outputs.

## D2 — A real spec gap: v1.2 has no HKG-like and no KHM-like country (22:58)

`PRE_DECLARATIONS.md` §2/§7 needs three country types with gate state "computed from the run", but v1.2 contains
30 synthetic countries with only one declared real-case-informed parameterisation (`SYN00_PHL_LIKE`). The spec
declares `φ, s, σ, ν` for HKG/PHL/KHM but says nothing about which v1.2 country's *gate machinery* they sit on.

**Resolution, written down and hashed before any shadow output existed:** layer the block on three designated
v1.2 countries, chosen by a **shadow-blind income rule** — PHL = `SYN00_PHL_LIKE` (v1.2's own declared
PHL-informed country); HKG = highest 2020 GDP per capita; KHM = lowest. GDP per capita is not an argument of the
demand equation. Documented in `IMPLEMENTATION_NOTE.md` §1, hashed
`b367b7daa85f126f359b2c9bd2c3fff37e20361700502241402bc2bcee16153a` at 23:00:12, before the first run.
Resolved hosts: **SYN28 / SYN00_PHL_LIKE / SYN18**. The alternative (fabricating HKG and KHM generator traits)
would have required declaring a dozen parameters not in the frozen table — that is the thing `c4c` exists to
prevent, so I did not do it.

## D3 — The serious bug: my loop variable ate v1.2's growth rate (23:02)

**What I saw first:** the first `--smoke` run printed `gdppc` values of **1.6e+38** for 2019 and **8.0e+38** for
2020 (v1.2: 48 270 and 890). Printing the growth path showed `g = [4.0, 4.0, 4.0, …]` — every year.

**Cause:** in the shadow store I wrote `for g in GATES:` inside `simulate_country`. `g` is v1.2's growth rate.
The loop left `g = 4` (the last gate index), so `out["g"][t]` was 4.0 and `Y *= (1.0 + g)` multiplied GDP by 5
every year for 56 years. Two further locals were shadowed harmlessly (`gs`, the sector growth term, and `q`,
the congestion array) and were renamed at the same time.

**Fix:** renamed the loop variables to `gg` / `qq` / `gate_gs`. No arithmetic changed; only names.

**What this did to the numbers, and what I did about it:** the bug also forced every rank factor to 1.0 (the
exploding `X` made vacancies vast, so hiring was never tight), which slightly changed `R`. Under the bug the
smoke run gave `D*(HKG−PHL) = 0.1070` (a **PASS** on c4b); after the fix it is **0.0967** (a **FAIL**). I did not
"restore" the passing number: the buggy run is not a result, and the corrected run is the scored one. The bug was
caught by a GDP sanity check **before** any check was interpreted.

## D4 — A diagnostic bug in my own check code (23:04, first scored run)

**What I saw first:** in the first full scored run, `c2_i_max_abs_numeric_minus_analytic = 0.517` — the numerical
derivative did not match the analytic one by half a unit. That is a red flag on my derivative, not on the model.

**Cause:** I perturbed `V` so that `u = ln(1+V)` shifted by `±h·u` (because `V' = exp((1±h)u) − 1`), then divided
by `2h` instead of `2h·u`. The reported derivative was therefore `u × dD/du`, and the "error" was just `u`.

**Fix:** divide by `2h·u`. The verdict never depended on it (the sign component), but the reported diagnostic was
wrong in that run and is correct now (**1.8e-09**). The superseded run is disclosed here rather than hidden; the
delivered `results/` are from the corrected code.

## D5 — c5's headcount bound was wrong at the tertiary gate (23:05, pre-run note)

**What I saw first:** while writing the identities I noticed that the *destination-level* tertiary cohort
`C[3] = band₃·S/4` is smaller than the upper-secondary graduating class `C[2]` by a factor ≈ 0.64. A bound of
"D × candidates ≤ C[destination]" would fail mechanically at high `D`, with no code defect — a false-positive
identity check.

**Fix:** bound the tutored head-count by the **source-level** cohort `C[src]` for `g1–g3`, and by the candidate
pool at the labour gate `g4` (where no cohort exists). Written into `IMPLEMENTATION_NOTE_N1.md` §N1.1 and hashed
(`fa12944f75575b5b810140247248d3eee81a4b2e0a738f1593412a5710b20df6`) **before** the scored run, rather than
silently changed after seeing a failure. Realised max ratio: 0.4652 at g1–g3, 0.9958 at g4.

## D6 — Two more implementation choices, written down pre-run (23:05)

1. **δ_g sensitivity grid.** The declared range `{0.15, 0.30, 0.45}` is uniform, but the central values are
   differentiated (`0.30, 0.30, 0.25, 0.20`). I report four rows: the uniform sweep plus the central per-gate
   vector as its own reference row. Documented in N1 §N1.2.
2. **σ_c sensitivity.** Each country has its own declared range, so the three "cells" move all three countries
   together in their declared direction (low / central / high) rather than inventing a cross-country mix
   (N1 §N1.2).

Neither is a parameter change; both are choices about *how to report the pre-declared grid*, and both are
disclosed before the run.

## D7 — c4b came out at 0.0967 against a 0.10 threshold, and I did not touch it (23:0x)

**What I saw first:** after the D3 fix, `D*(HKG) − D*(PHL) = 0.096724` — a 3.3 % shortfall. It had been 0.1070
under the bug. The temptation is obvious: `b_V = 1.5` gives 0.1766 and passes, and so do `H = 30` and
`s_PHL = 0.07`.

**What I did:** nothing. The central value is the scored result (`PRE_DECLARATIONS.md` §10.5: "the best-looking
sensitivity cell may not be substituted for the central result"). `c4b` is reported **FAIL**, and
`FINDINGS.md` §2.2 reports which sensitivity cells would pass, explicitly labelled as *not* the scored result.
The same discipline applies to `c4a`: it fails in **every** cell of the grid, so there was no cell to be tempted
by.

## D8 — Corrected my own loop metric after seeing it (23:1x)

**What I saw first:** the first diagnostics reported a maximum `Π/π⁰` of **20.7** for KHM. That number is real
but misleading: it is at **g4**, the labour gate, which has **no feedback hook** (the block may only modify the
school pipeline's advance rate). Reporting it as "the loop" would have overstated the feedback by an order of
magnitude.

**Fix:** restricted the loop metric to the hook-bearing gates `g1–g3` (max **1.878**, PHL 1.395, HKG 1.061) and
kept the g4 ratio separately, labelled "not used". No check changed.

## D9 — Post-run diagnostics, added after the scored run, never promoted (23:1x)

Added after the scored values existed, labelled `NOT-SCORED` and dated later than the predeclaration
(`PRE_DECLARATIONS.md` §10.4 permits this):

- the gate pressure `R` that would be needed to reach `D = 0.75` at HKG g2 (2.983, i.e. 2.457× realised) — it
  explains the c4a FAIL, it cannot change it;
- the saturation breakdown by type × gate (all 53 saturated cells are KHM g4);
- the block-on vs block-off comparison of the hosts' v1.2 columns (the feedback's macro size: +0.04 % GDPpc for
  HKG, +0.12 % for PHL, +0.002 % for KHM);
- the loop multiplier per type.

None of these is in `shadow_checks_v1_3.csv`, and none can be promoted into the scored set.

## D10 — Things I deliberately did not do

- Did not modify `generator_v1_2/`, `shadow_module/`, or any file outside `generator_v1_3/`.
- Did not add v1.3 columns to v1.2, did not re-fit, did not re-seed, did not change a v1.2 parameter.
- Did not invent HKG/KHM generator traits (D2), a currency conversion for fees (`S` is an income share), or a
  gate-specific fee (`PARAMETERS.csv` declares one fee share per country).
- Did not widen the c4a band, drop a country from c4b, or switch the c4b statistic to something that passes.
- Did not report the buggy run (D3) or the superseded run (D4) as results; both are documented here.

## D11 — Run inventory (for audit)

| # | what | outcome | kept? |
|---|---|---|---|
| 1 | `--smoke`, buggy code | GDPpc 8e38, `g = 4` every year | **no** — bug D3 |
| 2 | `--smoke`, post-fix | sane distributions; c6 sha match already visible | design check only |
| 3 | scored run, post-fix | c1,c2,c3,c5,c6 PASS; c4a FAIL; c4b FAIL (0.0967); c4c PASS; **c2 max-error diagnostic wrong (0.517)** | superseded by D4 fix |
| 4 | scored run, + c4a-gap & host diagnostics | same six verdicts | superseded by D9 additions |
| 5 | scored run, + saturation breakdown | same six verdicts | superseded by D8 fix |
| 6 | scored run, + sensitivity gap/loop columns | same six verdicts | superseded by D8 fix |
| 7 | **scored run A, final code** | **c1 PASS · c2 PASS · c3 PASS · c4a FAIL · c4b FAIL · c4c PASS · c4 FAIL · c5 PASS · c6 PASS** | **delivered** |
| 8 | scored run B, separate dir (determinism) | byte-identical to run 7, including the manifest | evidence |

**The six verdicts did not change across runs 3–8.** What changed was diagnostics, the c2 max-error figure, the
loop metric's scope, and two sensitivity columns. That is the honest summary: no verdict was ever "improved" by
a design change, and the one number that moved close to a threshold (c4b) moved **from a PASS to a FAIL** when a
bug was fixed.

## Freeze

`code/sim_v1_3.py` sha256 `d714a4f4eb657dd880f3800282583d6fd0983fe33ead75dc1c0fceb8ffb3daf8`;
`PARAMS.md` sha256 `2b144985aa5b53a426afec0b9df8646ff3f49d803744dc0f2ae73778f22ff84d` (recorded in the code,
which refuses to run on mismatch). Results hashes are in `RUN_MANIFEST.json` and
`results/determinism_note.md`.
