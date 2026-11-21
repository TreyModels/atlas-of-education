# Q-5 — the arm-vs-trend reading hazard: RESOLVED (DEBUG; record correction prepared, applied = false)

**LABEL: `DEBUG`.** Lead ruling (2026-11-21): resolve before any further record work; re-derive from
`anchor_table.csv` + `calibration_table.csv`; state whether the class-level sentence is **(i) correct for the
aggregate, (ii) wrong for some arms, or (iii) comparing different tables/objects**; if a correction is needed,
prepare it in the D-1/D-165 style (corrected sentence + gate re-run), flagged as a **correction, not a new claim**.
The gate-passed write-up is **not edited** without the user's approval.

## 1. The hazard

`10_massification/lit/PHASE_WRITEUP.md` W-1.1 (headline block) and O-1 record the A1 anchor class as
"**losing to the 4.35 pp linear-trend benchmark**" (`4.352883341604888`), while
`10_massification/model/anchor_out/anchor_table.csv` shows one arm's holdout MAE **4.014780434743067**
(`complementary · capacity_gated`) **below** that benchmark.

## 2. Re-derivation (read-only; no model run, no re-score)

**The two numbers come from different tables with different fit/holdout windows.**

| object | file | windows | holdout n | benchmark |
|---|---|---|---|---|
| 12-arm anchor class | `anchor_out/anchor_table.csv` (`hold_mae`) | fit **1999–2013**, holdout **2014–2024** (`anchor.py`) | **14** | — |
| naive trend 4.352883… | `calib/calibration_table.csv` (`naive_trend`, iso=PHL) | fit **1980–2010**, holdout **2011–2024** (`calibrate.py` `FIT_Y`/`HOLD_Y`) | **17** | 4.352883341604888 |

**Like-for-like benchmark on the anchor's own windows** — naive linear trend fitted on PHL completion **1999–2013**,
projected to **2014–2024**, MAE over the same 14 observed cells (same 3 completion series):
**`naive_trend_anchor = 5.614935464535336`** (persistence on the same windows: 9.594685714285715; the 4.352883…
and 8.599853… values reproduce exactly on the calibration windows, slope/level check: 17 holdout cells).

| arm | rival | holdout MAE | vs like-for-like trend 5.614935 | verdict on holdout |
|---|---|---:|---:|---|
| law_only | demand_led | 4.419372307607801 | −1.195563 | **beats** |
| capacity_gated | demand_led | 4.514717646782828 | −1.100218 | **beats** |
| capacity_only | demand_led | 4.546970438807209 | −1.067965 | **beats** |
| none | demand_led | 6.111754907690532 | +0.496820 | loses |
| law_only | education_led | 5.190641911665736 | −0.424294 | **beats** |
| capacity_gated | education_led | 5.256464756267308 | −0.358471 | **beats** |
| capacity_only | education_led | 6.122199101442962 | +0.507264 | loses |
| none | education_led | 5.875474290798293 | +0.260539 | loses |
| law_only | complementary | 4.565579948487351 | −1.049355 | **beats** |
| capacity_gated | complementary | **4.014780434743067** | **−1.600155** | **beats** |
| capacity_only | complementary | 5.943703661626381 | +0.328769 | loses |
| none | complementary | 5.938227008289883 | +0.323292 | loses |

**7 of 12 arms beat the like-for-like trend; 5 lose.** The class range is 4.014780434743067–6.122199101442962
against a like-for-like benchmark of 5.614935464535336.

## 3. Finding: **(iii) comparing different tables/objects — and the class claim is also not supportable as stated**

The write-up's "losing to the 4.35 pp trend" joins a 12-arm holdout range measured on **2014–2024** to a benchmark
measured on **2011–2024** and fitted on **1980–2010**; on the anchor's own windows the benchmark is **5.614935 pp**,
and **the class does not uniformly lose** (7/12 beat it). This is a **record correction**, not a new claim: no arm is
re-scored, no model is re-run, no threshold changes.

## 4. Corrected sentence (prospective; `applied = false`; requires the user's approval)

> **A1 anchor class (12 arms), pre-close; `CLOSED`.** On the anchor's own windows (fit 1999–2013, holdout 2014–2024),
> fit MAE **1.047492271754753–3.2916863270693772** and holdout MAE **4.014780434743067–6.122199101442962**; the
> **like-for-like** naive linear-trend benchmark is **5.614935464535336** pp, which **7 of the 12 arms beat** and
> **5 lose** to; the previously quoted **4.352883341604888** pp trend is the **calibration-table** benchmark
> (1980–2010 fit / 2011–2024 hold) and is **not comparable** to the 12-arm holdout range. `[label: DERIVED; evidence:
> anchor_table.csv hold_mae; naive trend recomputed on the anchor windows from TARGETS_FLOW.csv completion_series]`

The corrected sentence says **less** and names its windows; it does not strengthen any claim and changes no verdict
(the phase remains `PARTIAL / DESCRIPTIVE / EQUIVALENT`; the negative remains specification-, record-, sign- and
benchmark-bounded — with the benchmark now correctly bounded).

## 5. Gate re-run (D-1/D-165 style)

The **write-up as delivered is unchanged**: `PHASE_WRITEUP.md` byte-identical, `WRITE-UP-GATE: PASS` stands.
Re-running the gate on the **corrected sentence** as a prospective replacement (not applied):

| gate | result for the corrected sentence | evidence |
|---|---|---|
| A-1 (label · class/object · window · status · one sentence) | **PASS** | one sentence; `DERIVED`; anchor class; windows named; status `CLOSED` |
| A-2 (0 untraceable numbers) | **PASS** | all five numbers trace to `anchor_table.csv` / the recomputation in §2 |
| A-3 (0 banned sentences outside the register) | **PASS** | no banned phrase; "losing to the trend" is replaced by a windowed statement |
| A-7 (12-arm range stated with its arm set) | **PASS** | the 12 arms are the anchor class; per-arm table in §2 |
| A-4/A-5/A-6/A-8 (document-level) | **N/A while `applied = false`** | the document is not edited; its gate result stands as shipped |

**Flag:** this is a **correction**, not a new claim; it is **prospective** (`applied = false`) and needs the user's
approval before any edit. The delivered tables, panels and write-up are untouched.
