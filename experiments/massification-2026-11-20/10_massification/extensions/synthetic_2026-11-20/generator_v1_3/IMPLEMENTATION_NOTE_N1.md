# IMPLEMENTATION NOTE N1 — pre-run clarifications to `IMPLEMENTATION_NOTE.md`

**LABEL: SYNTHETIC / DECLARED.** No result is in this file. It is written and hashed **before the first
v1.3 run** and it changes **no parameter and no threshold** of the frozen spec. It clarifies four
implementation details of `IMPLEMENTATION_NOTE.md` (sha256 `b367b7daa85f126f359b2c9bd2c3fff37e20361700502241402bc2bcee16153a`,
frozen 2026-11-20T23:00+08:00) that were resolved while writing the code.

## N1.1 `c5` "tutored head-count ≤ cohort at gate" — the bound actually used

`IMPLEMENTATION_NOTE.md` §3.8 said "destination-level cohort". That bound is wrong for `g3`: the tertiary
annual cohort `C[3] = band_3 · S / 4` is *smaller* than the upper-secondary graduating class from which the
gate draws (`C[3] ≈ 0.64 · C[2]` at the declared band shares and durations), so a destination-cohort bound
would fail mechanically at high `D` without any code defect. The implemented bound is therefore:

```
g1, g2, g3 :  D_g · candidates_g  <=  C[src(g), t] · (1+1e-12),   src(g) = 0, 1, 2
g4         :  D_g4 · candidates_g4 <= candidates_g4 · (1+1e-12)     (no cohort exists at the labour gate)
```

i.e. the number of tutored households at a gate cannot exceed the cohort **from which the gate draws**. This
is still an informative accounting check (it fails if the gate-state extractor pulls a candidate pool larger
than its own source cohort, or if `D > 1`), and it cannot fail for a legitimate demand level. The maximum
ratio is reported in `shadow_checks_detail_v1_3.csv`.

## N1.2 Sensitivity grid definitions (`PRE_DECLARATIONS.md` §6 ranges)

1. **`delta_g`** — the declared range is `{0.15, 0.30, 0.45}` for `g1..g4`, but the central values are
   *differentiated* (`0.30, 0.30, 0.25, 0.20`). The grid therefore has four rows: **uniform** `delta = 0.15`,
   `0.30`, `0.45` applied to all of `g1..g4` (`delta_0 = 0.02` fixed) **plus** the central per-gate vector as
   its own reference row. The central row is the scored result; the uniform rows are the pre-declared sweep.
2. **`sigma_c`** — each country has its own declared range (`C07-C09`). The three cells move all three
   countries **together** in their declared direction: `low` = (0.40, 0.60, 0.55), `central` =
   (0.55, 0.80, 0.75), `high` = (0.70, 1.00, 0.95). No cross-country re-mixing is invented.
3. **`s_PHL`, `s_KHM`** — one-at-a-time on the named country, other countries at their central values.
4. Every other parameter (`b_Z, b_V, b_D, b_y, b_F, H`) is one-at-a-time on all three countries with the
   other parameters at central values. No multi-parameter search, no optimisation, no likelihood.

## N1.3 Which year the "experiments" use

`c1(ii)` and `c2(ii)` are comparative statics **at the declared comparison year `t* = 2020`** (the year
`§8 c4a` fixes), holding everything else at its realised value: "all else fixed" means the demand equation is
re-evaluated on the *same* gate state, not re-simulated. The full 1970–2025 path of the same gap is reported
beside it as a `NOT-SCORED` diagnostic, so a reader can see whether 2020 was unrepresentative. `c1(i)`/`c2(i)`
use **every** `(c,g,t)` cell for `g1..g4`.

## N1.4 Host resolution uses the shadow-OFF run

`resolve_hosts()` reads 2020 GDP per capita from the **shadow-off** (v1.2-equivalent) run, so the mapping is a
property of the frozen v1.2 state and cannot drift with the shadow feedback. The code asserts that the
shadow-on run produces the same mapping and refuses to run otherwise. In this panel the two runs agree.

---

**Freeze.** This note and `IMPLEMENTATION_NOTE.md` are hashed into `RUN_MANIFEST.json`. They were written
after the frozen spec was read and before any v1.3 `D`, `D*`, `c1`–`c6` value existed.
