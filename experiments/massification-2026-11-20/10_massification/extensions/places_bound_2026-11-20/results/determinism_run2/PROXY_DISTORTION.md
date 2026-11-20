# PROXY DISTORTION — EXP-19 PLACES-BOUND

**Status:** companion to `PLACES_BOUND_RESULTS.csv` and `PLACES_BOUND_DETAIL.csv`; generated deterministically by `code/run_places_bound.py`. **Adopt nothing.**

## 1. What the proxy is, and what it is not

The proxy is an **implied `seats/cohort`**, not a place count. No count of public schools, classrooms or construction completions is on disk (the delivery rows are `unable`). The proxy infers rooms from an observed **group-size divisor** and converts rooms to places at a declared norm class size:

```
F1 (class-size): coverage(n,t) = GER(t,level) * n / class_size(t,level)
F2 (PTR):        coverage(n,t) = GER(t,level) * n / PTR(t,level)   [one class per teacher]
```

`n in {40, 45, 50}` is declared; **none is adopted**. Every output is `DERIVED` from `OBSERVED` ratio/enrolment values.

## 2. Declared assumptions (each is a distortion if false)

| id | assumption | distortion if false |
|---|---|---|
| A1 | a usable classroom supplies exactly `n` student places | ignores double shifts, room-sharing, rented/anchor rooms, non-teaching rooms, decay, utilisation |
| A2 | rooms = enrolment / observed students-per-classroom ratio | the ratio is a national average of a ratio, not a room census; unused rooms are inside the average |
| A3 | GER = enrolment/cohort and is bridged to seats/cohort by A1 | GER is gross and includes overage and repeaters; it is not a seats/cohort measure |
| A4 | divisor and enrolment ratio are same-level (JHS / lower secondary) | level mismatch changes the implied coverage; elementary/SHS are reported only as sensitivities |
| A5 | divisor exact at `t`, else carried at `t+/-1`; enrolment ratio exact at `t` | a carried divisor uses a neighbouring year's class size; no interpolation is done |
| A6 | where lower-secondary GER is absent, broader `ger_secondary` is used and flagged | 2021 is converted on a broader enrolment object than 2018 |
| A7 | F2 requires one class per teacher | at secondary this is false where teachers are subject-specialised; the on-disk PTR-24 vs class-size-39/44 pair implies ~1.6–1.8 teachers per room |
| A8 | no cohort count is invented | no observed lower-secondary cohort count is on disk; GER is used because it is a ratio |

## 3. Why the proxy is not a place count

A place count would be a census of rooms (or of seats) at a date. The observed record contains **students per room** and **students per teacher**, not rooms, seats, schools or construction. Converting a ratio to a count requires the enrolment denominator, and converting rooms to adequate places requires a norm and an adequacy standard. Both are declared here, not observed. The five 2021 congested-share values (90.0, 76.8, 66.0, 60.1, 57.7%) are observed but are shares, not counts; they are not used in the verdict.

## 4. The declared intervals (DERIVED)

| norm n | I_n = [min, max] over primary F1 cells | span(I_n) | required span | classification |
|---|---|---|---|---|
| 40 | [0.780605886938, 0.95276] | 0.172154113062 | 0.113811094126 | STRADDLE |
| 45 | [0.878181622805, 1.071855] | 0.193673377195 | 0.113811094126 | OUTSIDE |
| 50 | [0.975757358672, 1.19095] | 0.215192641328 | 0.113811094126 | OUTSIDE |

The required state is `R = [0.759712104599, 0.873523198725]` (DERIVED, EXP-17). The interval is built only from the primary F1 cells; the F2, broader-GER and elementary/SHS cells are reported separately and are **not** verdict-bearing.

## 5. The identification limitation (why the verdict is SILENT)

The JHS class-size ratio is observed at 2010;2019;2021. `ger_lower_secondary` is observed through 2018. **The two year sets do not intersect** (intersection = 0 year(s)). The 2018 required year uses a 2019 class size (carried one year); the 2021 required year uses the broader `ger_secondary` (level fallback). No required year supplies a same-year, level-matched pair, so the conversion is not identified at the required object. The interval is a sensitivity, not a bound.

## 6. What would remove the distortion

A measured classroom stock (rooms by year), a measured seats series, or a year that observes both the JHS class-size ratio and `ger_lower_secondary`. None is on disk; the measured places/PTR series and capacity utilisation are **HELD** (D146) and are not fabricated here. **No external request is made; user approval is required for any HELD item.**

