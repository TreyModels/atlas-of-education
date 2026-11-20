<!-- PHASE WRITE-UP — authored, not executed. Writer Wu (lit author), 2026-11-21, under D168's frozen order
W-1…W-6 and the frozen gate A-1…A-8 (D166). NO model run, NO re-run, NO re-score, NO new number, NO new cell.
Every number below is lifted from a delivered file and cited by path + column (or by its VERIFICATION_026.csv id).
Every claim is one permitted sentence carrying a label, a class tag where a model number is quoted, an object
(EXP-21 row) where a level number is quoted, a window where κ is quoted, and a status. Banned sentences appear
ONLY inside the quoted-and-barred register (Appendix F). Supersedes PHASE_WRITEUP_SHELL.md (status SUPERSEDED).
Gate self-check: PHASE_WRITEUP_GATE.md. -->

# PHASE WRITE-UP — massification and universalization of education

**Two objects, one record.** (a) A **bounded negative on income-scaling**; (b) an **equivalence / identification map**
with **one unreproduced upper-secondary asymmetry** — plus the four delivered registers as citation appendices and
the HELD/banned apparatus as limits.

| field | value |
|---|---|
| document | `10_massification/lit/PHASE_WRITEUP.md` (canonical; D168) |
| status | **`LIVE`** — document of record. It **supersedes** [`PHASE_WRITEUP_SHELL.md`](PHASE_WRITEUP_SHELL.md), whose status is **`SUPERSEDED`** (its headline predates the closed line: 0 occurrences of `v1.5`/`v1.6`/`v1.7`/`bimodal`/`κ`/`WINDOW-ONLY`, V68) |
| phase verdict | **`CLOSED` at `PARTIAL / DESCRIPTIVE / EQUIVALENT`** (D76/D77, untouched by this document) |
| experiment programme | **`CLOSED` — 0 new cells** (D167). This write-up is the only open item (D168) |
| gate | **A-1…A-8** (D166); the Lead checks it, the Council issued **no** `SPINE-REPLACED` verdict. Self-check: [`PHASE_WRITEUP_GATE.md`](PHASE_WRITEUP_GATE.md) |
| write discipline | authorship only: no model run, no re-run, no re-score, no new number, no new cell; no causal claim; no direction claim; no external message |

*Table caption (A-1):* `DECLARED` document metadata; object: this document; no κ window; status `LIVE`. Permitted sentence: C-36.

**Label vocabulary (binding, D166/A-1).** `OBS` observed value from a cited delivered series · `SIM` value from a
committed run with its class tag · `DERIVED` arithmetic on `OBS`/`SIM` values, formula stated · `DECLARED` a
convention, threshold, assumption or theory statement · `HELD` an object that is not on disk · `REQUIRED-STATE` a
required-state object (none is used in this document; the D63 "required" values are `DERIVED` inversions, C-21).
**Status vocabulary:** `LIVE` (usable now) · `CLOSED` (an artifact or verdict that is final) · `SUPERSEDED` (replaced
by this document).

**Claim form.** Each claim is tagged `[C-nn · label · class/object · window · status]` and is followed by **exactly
one** permitted sentence. Tables carry the same fields in their captions. The claim index — id, label, class/object,
window, status, sentence — is reproduced as A-1 evidence in the gate file.

**Where the two objects sit.** Object (a), the bounded negative, is carried by W-1.3 (C-04, C-05) and W-2.6 (the
constant-conversion sentence). Object (b), the equivalence/identification map with the unreproduced asymmetry, is
carried by W-1.4 (C-06, C-07), W-2.7 (C-14, C-15) and W-3–W-5. W-6 carries the limits and the apparatus.

---

# W-1. The headline block and the two-class spine

## W-1.1 The headline block (two objects, one sentence each)

> **PHASE OBJECT — A1 anchor class (12 arms), pre-close. Status `CLOSED` (D76: `PARTIAL / DESCRIPTIVE / EQUIVALENT`).**
> Conditional **level** reproduction — fit MAE **1.047492271754753–3.2916863270693772** across the 12 arms, holdout
> **4.014780434743067–6.122199101442962**, losing to the **4.35 pp** linear-trend benchmark
> (`4.352883341604888`) — plus observational equivalence and one unreproduced upper-secondary asymmetry; **placement**
> (`v1.2` / `v1.3 A00`, status `CLOSED`): **9/33**, and a placement is not a reproduction.
>
> **POST-CLOSE OBJECT — `v1.7 (A17)`, within the closed `v1.5`–`v1.7` family. Status `CLOSED` (D150, D153(viii)).**
> Representation-only: upper-secondary unfilled **15/15**, both-level queue **30/30**, strict both-level coexistence
> **0/15**; **0/33** on the observed path against the **≥17/33** bar; crossings **1/3**; **D63** stays
> `UNABLE as to cause`, with the residual split **58.6008 / 41.3992** at the declared t−3 pair (`DERIVED`).

*Provenance for the block — no number in it is new.* 12-arm range **V69** ([`anchor_table.csv`](../model/anchor_out/anchor_table.csv)
columns `fit_mae`, `hold_mae`); 4.35 pp **V75** ([`calibration_table.csv`](../model/calib/calibration_table.csv) column
`naive_trend`, `iso = PHL`, stored `4.352883341604888`); 9/33 **V75**
([`observed_path_A17.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/observed_path_A17.csv)
column `within_5pp_A00`); 0/33, ≥17/33 and 1/3 ([`v1_7_checks.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/v1_7_checks.csv)
rows S1, S2, columns `synthetic_value`, `threshold`, `legs_passed`); 15/15, 30/30, 0/15 (same file row S3, and
[`representation_cells.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/representation_cells.csv)
columns `unfilled`, `queue_ratio`, `coexists`); the split **V58**
([`D63_BOUNDS_RESULTS.csv`](../extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv) rows S8, S9, column
`value_num`).

`[C-01 · SIM · A1 anchor class (12 arms), the phase's level object O-1 · — · CLOSED]` The phase's level statement is
conditional level reproduction at fit MAE 1.047492271754753–3.2916863270693772 and holdout 4.014780434743067–6.122199101442962
across the 12 arms, losing to the 4.35 pp linear-trend benchmark, with placement 9/33 recorded separately as a
placement and not as a reproduction.

`[C-02 · SIM · v1.7 (A17), within the closed v1.5–v1.7 family, the post-close object O-3 · — · CLOSED]` The post-close
class is representation-only — upper-secondary unfilled 15/15, both-level queue 30/30, strict both-level coexistence
0/15, 0/33 on the observed path against the ≥17/33 bar, crossings 1/3 — and it does not face the observed path.

**The untagged headline is barred as a post-close sentence.** The shell's single unclassed line is barred by
**B-21** in Appendix F; it may not appear in this document as a sentence, and D77 is
**applied, not amended** — the block above says *less* about *narrower* objects, each with its class tag and its
statistic, which is what a rule against overstatement permits (D168).

## W-1.2 The two-class spine — three objects that are not interchangeable

`[C-03 · DERIVED (labels) · O-1 / O-2 / O-3 · — · CLOSED]` The record carries three model/observed objects that may
not be substituted for one another: the A1 anchor class (12 arms) as the level object, the `v1.2` / `v1.3 A00`
placement label (9/33) as a placement instrument, and the closed `v1.5`–`v1.7` two-tier class as representation-only
(0/33), with D63 `UNABLE as to cause` attached to the residual.

| object | class tag | value on disk | register line | what may be said | status |
|---|---|---|---|---|---|
| **O-1** the A1 anchor model, 12 arms | `A1 anchor class (12 arms)` | fit MAE **1.047492271754753–3.2916863270693772**; holdout **4.014780434743067–6.122199101442962** (V69) | `anchor_table.csv` `fit_mae`, `hold_mae` | the phase's level statement, **and** that it loses to the 4.35 pp linear trend; placement is a different object | CLOSED |
| **O-2** the placement / comparator | `v1.2` / `v1.3 A00` | **9/33** | `observed_path_A17.csv` `within_5pp_A00` (V75) | a **placement** label (crossing/endpoint), never a reproduction | CLOSED |
| **O-3** the post-close two-tier class | `v1.6` / `v1.7 (A17)` | **0/33** vs the ≥17/33 bar; crossings 1/3; single-tier representation | `v1_7_checks.csv` rows S1–S3 (V75) | representation-only; does not face the observed path | CLOSED |

*Table caption (A-1):* `DERIVED`; class tags as printed; objects O-1/O-2/O-3 (not EXP-21 rows); no κ window; status
`CLOSED`. Permitted sentence: C-03.

## W-1.3 Object (a) — the bounded negative on income-scaling

`[C-04 · SIM · A1 anchor class (12 arms) · — · CLOSED]` On this record the cohort-flow class does not generate the
positive income-scaling sign — all 12 arms carry the standing scaling verdict `FAIL` in
[`anchor_table.csv`](../model/anchor_out/anchor_table.csv) column `scaling_verdict` ("generated exps wrong-sign/outside
A3 range") and lose on holdout to the 4.35 pp linear-trend benchmark — so the negative is **specification-bounded**
(the A3 specification with one repair cell, not a proof about all cohort-flow models), **record-bounded** (the
declared panels, not a global test), **sign-bounded** (it locates where the class must be extended — an exogenous
supply channel — not where the world must be), and **benchmark-bounded** (the decisive comparator is the linear trend,
stored `4.352883341604888` in [`calibration_table.csv`](../model/calib/calibration_table.csv) column `naive_trend` at
`iso = PHL`, with persistence stored `8.599852941176476` in column `naive_persistence`).

`[C-05 · SIM · the one-cell repair cell of the A1 anchor class · — · CLOSED]` The licensed one-cell repair failed —
[`repair_table.csv`](../model/calib/repair_table.csv) shows `n_contained` = 0 for all three rivals,
`signs_ok` = 1, and PHL fit MAE 7.432552602310797 / 6.474471009905646 / 6.162719844916801 (columns `PHL_fit_mae`,
`n_contained`, `signs_ok`) against the declared 5 pp fit gate, with the repaired exponents still wrong-signed in
[`repair_scaling.csv`](../model/calib/repair_scaling.csv) columns `generated` (−2.733722425389776 /
−2.526712979736413 / −1.0343696359734724 at secondary) against the required `A1_value` +0.286 (± `A1_se` 0.045).

*Table W-1.1 — the 12 arms (`SIM`; `A1 anchor class (12 arms)`; object O-1; status `CLOSED`; no κ window).* Source:
[`anchor_table.csv`](../model/anchor_out/anchor_table.csv), columns as printed. Permitted sentence: C-04.

| rival | arm | `fit_mae` | `hold_mae` | `scaling_verdict` |
|---|---|---:|---:|---|
| demand_led | law_only | 2.03256440424153 | 4.419372307607801 | FAIL |
| demand_led | capacity_gated | 1.8546607892456848 | 4.514717646782828 | FAIL |
| demand_led | capacity_only | 3.2916863270693772 | 4.546970438807209 | FAIL |
| demand_led | none | 1.047492271754753 | 6.111754907690532 | FAIL |
| education_led | law_only | 2.1581646858248105 | 5.190641911665736 | FAIL |
| education_led | capacity_gated | 2.0525346242409244 | 5.256464756267308 | FAIL |
| education_led | capacity_only | 3.0238001930597282 | 6.122199101442962 | FAIL |
| education_led | none | 1.371270727493839 | 5.875474290798293 | FAIL |
| complementary | law_only | 2.1718223656032265 | 4.565579948487351 | FAIL |
| complementary | capacity_gated | 1.9732647435235702 | 4.014780434743067 | FAIL |
| complementary | capacity_only | 2.4683916625376967 | 5.943703661626381 | FAIL |
| complementary | none | 1.318865482339633 | 5.938227008289883 | FAIL |

**The arm set, stated with the range (D-1 correction, A-7).** The 12 arms are
**demand_led / education_led / complementary × {`law_only`, `capacity_gated`, `capacity_only`, `none`}** — the twelve
rows above; the range **1.047492271754753–3.2916863270693772** (fit) and **4.014780434743067–6.122199101442962**
(holdout) is the min–max **over those twelve rows**. The earlier phase sentence that joined a six-arm fit range to a
twelve-arm holdout range is corrected (D165(x), D-1); if the six-arm subset is quoted anywhere, the six arms must be
named: **demand_led·`law_only`, demand_led·`capacity_only`, education_led·`law_only`, education_led·`capacity_only`,
complementary·`law_only`, complementary·`capacity_only`**. The three `none` arms fit best (1.047492271754753,
1.318865482339633, 1.371270727493839) and hold worst (5.875474290798293, 5.938227008289883, 6.111754907690532) — the
overfit story that is the honest version of the phase's level claim. The `PARTIAL` verdict does not depend on
the range.

## W-1.4 Object (b) — the equivalence / identification map

`[C-06 · SIM + DECLARED · A1 anchor class (12 arms) · — · CLOSED]` The capacity-timing claim is not credited
(`capacity_gated` ties `law_only` on the crossings in 2 of 3 rivals, is better on holdout in 1 of 3 —
complementary 4.014780434743067 vs 4.565579948487351 — and worse in 2 of 3, all in `anchor_table.csv` column
`hold_mae` and `M2`/`M3`), and the cross-country push–pull **direction is not identifiable** on these moments, so the
map is reported as an equivalence set and **no direction claim is made anywhere in this document**.

`[C-07 · OBS + SIM · observed anchor signature (PHL) vs the 12 arms · — · CLOSED]` The observed signature is primary
completion ≥90 first in **2017** (`91.91800689697266`), lower-secondary ≥90 in **2024** (`92.4139633178711`), and
upper-secondary **never** ≥90 by 2024 (maximum `76.43295288085938`, in 2017) — all
[`UNIVERSALIZATION_SERIES.csv`](../data/UNIVERSALIZATION_SERIES.csv) column `value`, `iso3 = PHL`,
`indicator = completion_primary / completion_lower_secondary / completion_upper_secondary`, `status = observed`
(V48, V49) — and no arm on disk reproduces M2 in tolerance (0/12 clean) while M3 is 12/12 in-window with two
post-window overshoots.

---

# W-2. The level sentences

## W-2.1 The conversion register — which object may carry which level statement

`[C-08 · DERIVED from OBS · EXP-21 rows (system × level) · — · LIVE]` Completion and GER are one scale in 4 of the 12
frozen system × level cells and no scale at all in the other 8 (6 `NOT-INTERCHANGEABLE`, 2 unmeasured), and all four
`INTERCHANGEABLE` cells still cross parity — so every level sentence below names its object pair and its register row.

*Table W-2.1 — the 12 frozen cells (`DERIVED`; object rows as printed; status `LIVE`; no κ window).* Source:
[`CONV_REG.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG.csv), columns `n_pairs`, `T_min`, `T_max`,
`in_band_share`, `n_in_band`, `crossing_year`, `verdict`; values `T = completion / GER` on same-year pairs (V39–V46).
Permitted sentence: C-08.

| system | level | n pairs | `T_min`–`T_max` | `in_band_share` (n) | crossing 1.0 | verdict |
|---|---|---:|---|---:|---|---|
| PHL | primary | 9 | 0.802546–1.073853 | 0.555556 (5/9) | 2021 | `NOT-INTERCHANGEABLE` |
| PHL | lower_secondary | 4 | 0.746209–0.900968 | 0.250000 (1/4) | none | `NOT-INTERCHANGEABLE` |
| PHL | upper_secondary | 6 | 0.898892–1.093971 | 1.000000 (6/6) | 2017 | `INTERCHANGEABLE` |
| KOR | primary | 1 | 0.988654 | 1.000000 (1/1) | `UNABLE` | **`THIN`** |
| KOR | lower_secondary | 16 | 0.952004–1.035805 | 1.000000 (16/16) | 2010; 2017 | `INTERCHANGEABLE` |
| KOR | upper_secondary | 19 | 0.903371–1.079097 | 1.000000 (19/19) | 2006; 2007; 2008; 2009; 2016 | `INTERCHANGEABLE` |
| KHM | primary | 14 | 0.334070–0.790452 | 0.000000 (0/14) | none | `NOT-INTERCHANGEABLE` |
| KHM | lower_secondary | 6 | 0.525134–0.770959 | 0.000000 (0/6) | none | `NOT-INTERCHANGEABLE` |
| KHM | upper_secondary | 3 | 0.370991–1.173614 | 0.000000 (0/3) | 2001; 2008 | `NOT-INTERCHANGEABLE` |
| CHN | primary | 6 | 0.904041–1.004089 | 1.000000 (6/6) | 2014; 2016; 2020 | `INTERCHANGEABLE` |
| CHN | lower_secondary | 1 | 0.846909 | 0.000000 (0/1) | `UNABLE` | **`THIN`** |
| CHN | upper_secondary | 5 | 0.572200–0.946374 | 0.200000 (1/5) | none | `NOT-INTERCHANGEABLE` |

HKG and JPN carry `NO-COMPLETION-SERIES` in all six of their cells (`n_pairs` = 0): no completion-based level
sentence exists for them, and the blank is printed rather than omitted.

## W-2.2 The three headline numbers and their licences

`[C-09 · OBS · PHL primary, lower_secondary, upper_secondary at 2024 · — · LIVE]` The three 2024 PHL completion
values are completion objects only — `98.30461883544922` (primary, register row PHL/primary, `NOT-INTERCHANGEABLE`,
T = 1.045426), `92.4139633178711` (lower, **no same-year level GER**) and `75.02525329589844` (upper, **no same-year
level GER**) (V48) — and none may be converted, compared to GER, or fused with the model's `completion_uis`.

| number | object | system / year | register row | may be used as | may **not** be used as | label | status |
|---|---|---|---|---|---|---|---|
| **98.30461883544922** | `completion_primary` | PHL / 2024 | PHL/primary `NOT-INTERCHANGEABLE` | a completion value with system + year + register row | "completion" unqualified; a conversion; a comparison with `completion_uis` | `OBS` | LIVE |
| **92.4139633178711** | `completion_lower_secondary` | PHL / 2024 | PHL/lower_secondary `NOT-INTERCHANGEABLE` | a completion value with system + year | a ratio, a GER comparison, or a fusion with the model — **no same-year level GER** (series ends 2018) | `OBS` | LIVE |
| **75.02525329589844** | `completion_upper_secondary` | PHL / 2024 | PHL/upper_secondary `INTERCHANGEABLE` | a completion value with system + year | the same, and any substitution of `ger_secondary` 2024 as its denominator | `OBS` | LIVE |

*Table caption (A-1):* `OBS`; objects as printed (EXP-21 rows); status `LIVE`. Permitted sentence: C-09.

## W-2.3 The `ger_secondary` trap

`[C-10 · OBS + DECLARED · ger_secondary 2024 vs ger_upper_secondary / ger_lower_secondary · — · LIVE]`
`ger_secondary` in 2024 is `85.2945085684493`
([`UNIVERSALIZATION_SERIES.csv`](../data/UNIVERSALIZATION_SERIES.csv) column `value`, `indicator = ger_secondary`,
`iso3 = PHL`, `status = observed`; V51) and the level-specific GER series **end in 2018** (V50) — so `ger_secondary`
may never stand in for `ger_upper_secondary` or `ger_lower_secondary`: the pairing is `NOT-COMPARABLE` under D158(2),
not a number, and no 2024 level denominator exists on this disk.

## W-2.4 `T` and completion share digits — separate columns, separate units

`[C-11 · DERIVED · EXP-21 row PHL/primary at 2017 · — · LIVE]` PHL primary completion in 2017 is `91.91800689697266`
**percent** and the conversion `T` for the same cell is **0.925039** **ratio**
([`CONV_REG_DETAIL.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG_DETAIL.csv) columns `completion_value`,
`T`; V49) — two different quantities whose mantissas are cousins, which is why every table here keeps them in separate
columns with units and no sentence carries both without their labels.

## W-2.5 `THIN` is unmeasured, not clean

`[C-12 · DERIVED · EXP-21 rows KOR/primary and CHN/lower_secondary · — · LIVE]` KOR/primary and CHN/lower_secondary
rest on exactly one same-year pair each (`n_pairs` = 1 in
[`CONV_REG.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG.csv)) and are therefore printed as **unmeasured**
— they receive neither `INTERCHANGEABLE` nor `NOT-INTERCHANGEABLE` and support no sentence in either direction — and
PHL/lower_secondary clears the declared `< 3` pair gate with 4 pairs but is thin in substance, with no GER counterpart
for its 2024 value.

## W-2.6 The constant-conversion sentence

`[C-13 · DECLARED + SIM · A17, v1.3, v1.2 panels · — · CLOSED]` `m = 1.10` is a `DECLARED` point convention on a
**synthetic** panel — the identity `completion_uis / completion_cohort` is `CONSTANT` on A17 at `8.8395202269e-10`
and `NOT-CONSTANT` on v1.3 and v1.2 at `4.7043695535e-02`, because **35 of 6,720** cells in each of those two panels
cap `completion_uis` at 1.0 exactly where `1.10 × completion_cohort > 1`
([`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv), columns `panel_path`,
`completion_uis_column`, `completion_cohort_column`; V47) — and it is **not** a level convention for the observed
record.

## W-2.7 The asymmetry, stated exactly

`[C-14 · OBS · PHL three-level signature · — · LIVE]` The observed order is primary (`91.91800689697266`, 2017) then
lower-secondary (`92.4139633178711`, 2024) then tertiary, with upper-secondary never reaching 90 by 2024 (maximum
`76.43295288085938`), and that ordering — floor and middle yes, ceiling no — is the anchor criterion the equivalence
map is measured against (A6/R23; `MASSIFICATION_CLOSEOUT.md` §2).

`[C-15 · SIM · the 12 arms against the M-vector · — · CLOSED]` No arm reproduces M2 and M3: M2 is missing, 2025, 2028
or 2038 against an observed 2024 — **0/12 clean in tolerance** — and M3 is missing or post-window (2027, 2031) against
a series that never reaches 90, in
[`anchor_table.csv`](../model/anchor_out/anchor_table.csv) columns `M2`, `M3` (`MASSIFICATION_CLOSEOUT.md` §2 records
the R29 flags on the 2025/2028 and 2027/2031 cells).

**Two disclosures that travel with this section.** (i) The **C8 reporting gap**: the asymmetry's first element — the
primary ≥90 crossing in 2017 — was never recorded in the committed A1 outputs (per-arm fitted series were not
persisted), so the asymmetry was tested with its first element missing; no re-fit was performed, and this is a
reporting gap of A1, not evidence for or against any mechanism (`MASSIFICATION_CLOSEOUT.md` §2; the shell's §b.7).
(ii) **M4 is not discriminable**: simulated tertiary GER ≥50 occurs in 1960 in all 12 arms including no-push (an
initialisation artefact, `anchor_table.csv` column `M4`), so it is excluded from PASS/FAIL and recorded as untested.

---

# W-3. The participation margin

`[C-16 · DERIVED from OBS pairs · PHL primary / lower_secondary / upper_secondary · — · LIVE]` The observed
participation margin is a same-year gross − net enrolment gap that spans levels steeply — primary **n = 30**,
**2.196578–14.627307 pp** (median **10.086482**), lower-secondary **n = 4**, **17.412040–29.239540 pp** (median
**28.518155**), upper-secondary **n = 2**, **46.062110–51.704530 pp** (`THIN`, median **48.883320**) — and no single
cross-level margin exists in this record.

*Table W-3.1 — the three spans (`DERIVED`; object: PHL `ger_<level> − ner_<level>`, same year, both `observed`;
status `LIVE`; no κ window).* Source: [`PART_MARGIN_DESC.csv`](../extensions/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv),
columns `n_pairs`, `pair_year_min`, `pair_year_max`, `span_min_pp`, `span_min_year`, `span_max_pp`, `span_max_year`,
`span_median_pp`, `thin` (V52). Permitted sentence: C-16.

| level | pairs | window | span min (year) | span max (year) | median | `THIN` | identity | placement | `comparison_performed` |
|---|---:|---|---|---|---:|---|---|---|---|
| primary | 30 | 1976–2017 | 2.196578 (1976) | 14.627307 (1999) | 10.086482 | no | `NO-REGISTERED-COUNTERPART` | **`WITHHELD-NO-IDENTITY`** | `FALSE` |
| lower_secondary | 4 | 2014–2017 | 17.412040 (2017) | 29.239540 (2016) | 28.518155 | no | `NO-REGISTERED-COUNTERPART` | **`WITHHELD-NO-IDENTITY`** | `FALSE` |
| upper_secondary | 2 | 2014–2015 | 46.062110 (2014) | 51.704530 (2015) | 48.883320 | **yes** | `NO-REGISTERED-COUNTERPART` | **`WITHHELD-NO-IDENTITY`** | `FALSE` |

`[C-17 · DERIVED · the identity test over the audited candidate set · — · LIVE]` The identity test fails at all three
levels — EXP-21's register carries one line per PHL level and **0** lines matching the model object's
numerator/denominator, and none of the audited candidate objects shares the model's convention
([`OBJECT_IDENTITY_AUDIT.csv`](../extensions/part_margin_desc_2026-11-20/results/OBJECT_IDENTITY_AUDIT.csv);
`PART_MARGIN_DESC.csv` columns `identity_test`, `n_register_lines`, `n_matching_lines`; V54) — so the verdict is
`NO-OBSERVED-COUNTERPART`, the placement is `WITHHELD-NO-IDENTITY`, and `comparison_performed = FALSE`.

`[C-18 · DERIVED · the historical window vs the model year · — · LIVE]` The pairs end in **2017** (primary, lower) and
**2015** (upper) while the model shares sit at 2024, so any sentence placing a 2024 model share against an observed
span is barred as a cross-year comparison, independently of the identity test.

**Reading rule (permanent).** `WITHHELD-NO-IDENTITY` is never rendered as "close" or "far": no observed range exists
for the model's object, so no distance exists to render. The model's shares may be printed beside the spans **for
orientation only**, with `comparison_performed = FALSE` in the same table — printing is not a comparison, and the six
class-tagged shares (V55) are not a placement. The negative statement this permits is scoped, and stays scoped:
**no object among the audited candidates / no register line** shares the model's convention — never that no such
object exists.

---

# W-4. The D63 residual

`[C-19 · DERIVED · D63 residual, upper-secondary 2024 against the declared 90 pp level · — · LIVE]` The residual is
**14.974746704101562 pp** (stored `value_num`, row S1 of
[`D63_BOUNDS_RESULTS.csv`](../extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv); displayed
14.974747), and it splits at the declared one-stage pair (upper 2024 against lower 2021) into **58.6008386858443 %
pipeline level / 41.3991613141558 % transition ratio** (rows S8, S9; G = 0.18198490285627197 = P 0.1066446793553944
+ Q 0.07534022350087775, identity residual 1.942890293094024e-16 — an accounting identity with zero free parameters;
V57, V58).

> **The t−3 sentence, which every citation of 58.6008 % must carry:** the split is a statement **about the declared
> one-stage pair**, not a lag-free property of the residual — at the contemporaneous lower value the pipeline share is
> **−0.14544291665697634** and the ratio share **1.145442916656977** (row X1/X2, `used_in_verdict = FALSE`; V62),
> because the 2024 lower value already sits above the 90 pp level.

`[C-20 · DERIVED · the three bounds · — · LIVE]` Of the three declared bounds, **B1 is `OUTSIDE`** — the lower
completion required at the 2024 ratio is **97.0425841315231** against the record maximum
**92.4139633178711** (excess **4.628621 pp**) — and **B2** (required ratio **0.9738788032543533** inside the observed
eight-pair range **[0.8891573087274445, 1.0724421619315192]**) and **B3** (implied upper interval
**[82.170551, 99.108631]**, which contains 90) are **`INSIDE`** (rows B1–B3, columns `value_num`, `outcome`;
V59–V61).

| id | required / implied | record envelope | outcome | label |
|---|---|---|---|---|
| **B1** | lower completion needed at the 2024 ratio: **97.0425841315231** pp | highest observed lower completion: **92.4139633178711** (2024) | **`OUTSIDE`** (+4.628621 pp) | `DERIVED` |
| **B2** | ratio needed at the record's 2024 lower completion: **0.9738788032543533** | observed eight-pair range: **0.8891573087274445–1.0724421619315192** | **`INSIDE`** | `DERIVED` |
| **B3** | upper completion implied at that ratio: **82.170551–99.108631** pp | the declared 90 pp level | **`INSIDE`** (interval contains 90) | `DERIVED` |

*Table caption (A-1):* `DERIVED`; object: the D63 upper-only leg; status `LIVE`. Permitted sentence: C-20. The two
"required" values are `DERIVED` inversions of the identity, **not** `REQUIRED-STATE` objects (D158(7), C-21): they
are not targets, not a policy level, and not the EXP-17 required coverage.

`[C-21 · DERIVED · the bounds verdict · — · LIVE]` `BOUNDS-EDGE` means **1 of 3 outside** and nothing else — there is
no tolerance, epsilon or margin anywhere in the three tests, so "edge" is not a proximity label — and the record
therefore neither contains the required path nor rules it out.

`[C-22 · DECLARED · D63, as ruled · — · LIVE]` **D63 stays `UNABLE as to cause`**: the split names two accounting
channels and does not say what produced either, no structural sentence about the upper-secondary ceiling may be
written in **either** direction (B-3 and B-15 in Appendix F), B2/B3 are arithmetic combined across different years
(the joint combination was never observed, no counterfactual is claimed), and this is an **upper-only** leg that may
not be cited about the lower level or about any two-level object (D158(4)).

---

# W-5. The κ register

The four fixed sentences, **verbatim**, each with its window, from
[`KAPPA_WRITE_REGISTER.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv) column
`admissible_sentence` and [`FINDINGS.md`](../extensions/kappa_write_2026-11-20/FINDINGS.md) §5 (V64):

`[C-23 · DERIVED · PHL κ (transition ratio) · window 2003–2024 (full), 2003–2017 (pre-2021) · LIVE]` The PHL sentence, verbatim: "within-window; slope flat but half-shift 2.1348 pp > 2.0, so not stationary in level" (κ = `0.949135`, `kappa_full`; slope `−0.000704`, half-shift `2.1348`, hold-out 2/2).

`[C-24 · DERIVED · KOR κ · window 2005–2023 (full), 2005–2020 (pre-2021) · LIVE]` The KOR sentence, verbatim: "slope flat and shift 0.6354 pp, yet 0/3 hold-out cells — κ-STABLE is never written forward-usable" (κ = `0.989758`, slope `+0.002875`, half-shift `0.6354`, hold-out `0/3`).

`[C-25 · DERIVED · KHM κ · window 2000–2023 (full), 2000–2017 (pre-2021) · LIVE]` "trending, shift 7.4361 pp"
(κ = `0.594984`, slope `+0.017318`, half-shift `7.4361`, hold-out 1/2).

`[C-26 · DERIVED · CHN κ · window 2012–2020 · LIVE]` "reported only; non-stationary; not a forward constraint"
(κ = `0.722222`, slope `+0.041728`, half-shift `25.6573`, 0 hold-out cells).

`[C-27 · DERIVED · KOR as the counter-example · window 2005–2023 · LIVE]` The KOR counter-example ships with the
register: **KOR is the counter-example that bars "κ-STABLE is forward-usable": slope +0.002875/yr and half-shift
0.6354 pp both clear their bars, yet 0/3 hold-out cells (excess +0.6824, +0.6506, +0.5917 pp)**
([`FINDINGS.md`](../extensions/kappa_write_2026-11-20/FINDINGS.md) §2;
[`KAPPA_WRITE_REGISTER.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv) columns
`holdout_within`, `holdout_violation_years`).

`[C-28 · DERIVED · the κ use count and its universe · — · LIVE]` Of **309** enumerated uses, **299** are applied,
**233** are in-window (**77.9264 %** of applied), **64** sit below and **4** above the window (**68** barred, not a
partition — the 64 projections and 44 `NOT-COMPARABLE` rows are subsets), **132** are observed-pair descriptive uses
in-window, and **0** live verdicts rest on any barred use — over a universe of **17** adjudicated files, of the
**193** files on disk that contain a κ token
([`KAPPA_WRITE_SUMMARY.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_SUMMARY.csv) rows `n_uses`,
`n_applied`, `n_in_window`, `pct_in_window_of_applied`, `n_out_below`, `n_out_above`, `n_barred`,
`n_observed_descriptive_in_window`, `live_verdict_load_bearing_uses`, `universe_files`,
`corpus_files_with_kappa_token`; V63).

`[C-29 · DECLARED · the two κ symbols · — · LIVE]` Two different objects are written κ in this programme — the
per-system transition ratio registered here and the model's congestion elasticity `G(C) = C^κ`, `κ ∈ [0.5, 1.0]`,
excluded by declaration D9 and counted as 2 lines, never merged into the register — and every κ sentence in this
document names which κ it is.

`[C-30 · DECLARED · the barred κ families · — · LIVE]` Two sentence families are barred from this write-up: any
citation of the κ-link as validation (it is a projection over **53** synthetic model years with **31** outside the
window, applied to a model-generated lower series; the 62 uses sit in the closed EXP-7 object), and the stated
future-value sentence computed from κ for 2027 (D133; `STATUS.md`) — and **no table may be lifted from column 15**
(`exp11_forward_constraint`) of the register, whose stale value is a label hazard (D-2, D165(viii)) and whose only
forward-field label that may ship is `WINDOW-ONLY`.

**What this register does not license.** κ is a citation, not a parameter, constraint, calibration target or forecast
input; no cross-system or cross-level κ sentence; no projection past 2024/2023/2020; no causal or direction claim; no
adoption. A κ value from a file outside the 17 adjudicated files has no register line and is `UNVERIFIED`.

---

# W-6. Limits, apparatus and what this document does not claim

## W-6.1 The HELD ledger and the HKG re-entry condition

`[C-31 · HELD · 14 HELD objects + the HKG re-entry condition · — · LIVE]` Fourteen objects are `HELD` — none is
fabricated, user approval is required for any of them, and no cell is issued against any of them (D157; V74) — and
`DEFER-HKG` stands until **both** parts of the HKG condition hold **and** a new Council decision authorises re-entry.

Full table: **Appendix E** (the Council's Appendix B, carried verbatim; 14 rows).

## W-6.2 The 12-arm range and its arm set

`[C-32 · SIM · A1 anchor class (12 arms) · — · CLOSED]` The phase's fit range is
**1.047492271754753–3.2916863270693772** and its holdout range **4.014780434743067–6.122199101442962**, taken over
the **twelve** arms demand_led / education_led / complementary × {`law_only`, `capacity_gated`, `capacity_only`,
`none`} of [`anchor_table.csv`](../model/anchor_out/anchor_table.csv) columns `fit_mae`, `hold_mae` (V69; A-7), and
any quotation of the six `law_only` + `capacity_only` arms must name those six arms (W-1.3; B-26).

## W-6.3 The read order (D-4 correction)

`[C-33 · DECLARED · the external read order · — · LIVE]` Three paths in the programme's external read order do not
resolve — `06_report/AGENT_PROTOCOL.md`, `LEAD_HANDOFF.md` and `06_report/MASSIFICATION_CLOSEOUT.md` (the first and
third live at the programme root and the second is absent; V71) — so the corrected order below is the one that
resolves, and it adds the four registers and this write-up.

| # | file | what it is |
|---:|---|---|
| 1 | [`10_massification/README.md`](../README.md) | the current first-order question |
| 2 | [`AGENT_PROTOCOL.md`](../../AGENT_PROTOCOL.md) | bridge grammar and authority (root; the `06_report/` path was dead) |
| 3 | [`08_council/BIG_PICTURE_RULE.md`](../../08_council/BIG_PICTURE_RULE.md) | the mandatory step-back |
| 4 | [`08_council/DECISIONS.md`](../../08_council/DECISIONS.md) | D1–D169; D76/D77, D150, D152–D169 govern this document |
| 5 | [`MASSIFICATION_CLOSEOUT.md`](../../MASSIFICATION_CLOSEOUT.md) | phase closeout (root; the `06_report/` path was dead) |
| 6 | [`10_massification/HANDOFF_expert-council.md`](../HANDOFF_expert-council.md) | the nearest object to the absent `LEAD_HANDOFF.md` |
| 7 | [`10_massification/STATUS.md`](../STATUS.md) | live task/artifact state (§3w–§3ag) |
| 8 | [`PHASE_WRITEUP.md`](PHASE_WRITEUP.md) | this document |
| 9 | [`conv_reg_2026-11-20/FINDINGS.md`](../extensions/conv_reg_2026-11-20/FINDINGS.md) | register 1 — conversion (EXP-21) |
| 10 | [`part_margin_desc_2026-11-20/FINDINGS.md`](../extensions/part_margin_desc_2026-11-20/FINDINGS.md) | register 2 — participation margin (EXP-22) |
| 11 | [`d63_bounds_2026-11-20/FINDINGS.md`](../extensions/d63_bounds_2026-11-20/FINDINGS.md) | register 3 — D63 bound split (EXP-23) |
| 12 | [`kappa_write_2026-11-20/FINDINGS.md`](../extensions/kappa_write_2026-11-20/FINDINGS.md) | register 4 — κ use register (EXP-24) |
| 13 | [`SYNTHESIS_026.md`](../../08_council/brief_026/SYNTHESIS_026.md) | the write-up order W-1…W-6 and the gate A-1…A-8 |
| 14 | [`PHASE_WRITEUP_GATE.md`](PHASE_WRITEUP_GATE.md) | the A-1…A-8 self-check with per-item evidence |

*Table caption (A-1):* `DECLARED`; object: the external read order; status `LIVE`. Permitted sentence: C-33. Every
link in this table, and every inline link in this document, resolves on disk (A-8; checked in
[`PHASE_WRITEUP_GATE.md`](PHASE_WRITEUP_GATE.md)).

## W-6.4 The frame this programme carries as theory, never as evidence

`[C-34 · DECLARED · the user's structural frame · — · LIVE (as theory only)]` The programme carries the user's
structural insight as `DECLARED-THEORY` — the system is **bimodal within the same system** (low-cost seats going
untaken at the same time as extreme competition at the rationed gates) and the path is a **one-way ratchet** (shocks
set back levels, they do not reverse the configuration) — and it is never evidence: no synthetic PASS may be read as
confirmation, no causal or direction claim is licensed, and the illustrative examples are not to be modelled
literally ([`THEORY_FRAME.md`](../extensions/synthetic_2026-11-20/THEORY_FRAME.md) §1–§2, §5;
[`MODEL_ARCHITECTURE.md`](../extensions/synthetic_2026-11-20/MODEL_ARCHITECTURE.md)).

## W-6.5 Parks, verdicts and the things this document does not do

`[C-35 · DECLARED · parks and verdicts · — · CLOSED]` The parks stand — A3 `KILLED`, the exit-cost/induction layer
`PARKED` (D101, D104), HKG `DEFER-HKG`, D63 `UNABLE as to cause`, C1–C4 closed — and the phase verdict is
`CLOSED` at `PARTIAL / DESCRIPTIVE / EQUIVALENT` with D76/D77 **untouched**: nothing in this write-up amends the
label, strengthens the phase's claim, or reopens a closed claim.

`[C-36 · DECLARED · the status of this document · — · LIVE]` This document is authorship, not an experiment — no
model was run, no cell was re-run or re-scored, no number was computed, and no external message or request was made —
so it is a *statement of the record*, and its acceptance is the A-1…A-8 gate checked by the Lead rather than a
Council verdict.

**Explicit "does not claim" box.** (1) Not that income-scaling is false in the world — only that this model class,
at these specifications and on this record, does not generate the sign without an exogenous supply channel. (2) Not
that any rival is better — all are equivalent or fail. (3) Not a direction of push–pull. (4) Not a causal effect of
any PHL event. (5) Not that capacity has no effect — only that capacity timing is not credited on the crossings and
that the de jure enforcement gate is contaminated by a double count in `law × G(C)`. (6) Not that the 2017 primary
milestone was reproduced — it was not recorded (C8 gap). (7) Not a word from a blocked source: PSA/ILOSTAT/OECD and
the Enterprise Surveys credential module are blocked, so the human-capital and signalling rivals are **design-only**
and are never called equivalent.

---

# Appendix A — Register 1: the conversion register (EXP-21)

**What it is.** A per-system × level register of `T = completion / GER` on same-year pairs, with a band test
(`INTERCHANGEABLE` iff T ∈ [0.85, 1.15] in ≥ 80 % of paired cells and range ≤ 0.30), a crossing record and a
`THIN` floor (`n_pairs < 3`). Verdict `REGISTER-BINDING` (`ACCEPT`, clean; D160, D164). No model, no NER, no
adoption. Predeclaration `1dd86bd1…`, enforced pre-input and pre-verdict; deterministic 6/6; 21/21 SHA.

*Table A-1 (A-1 caption): `DERIVED`/`OBS`/`SIM` as printed; object: EXP-21 register rows and the three 2024 completion cells; no κ window; status `LIVE`. Permitted sentence: C-08.*

| read-out | value | source (file + column) | label |
|---|---|---|---|
| cells `INTERCHANGEABLE` / `NOT-INTERCHANGEABLE` / `THIN` | 4 / 6 / 2 of 12 | [`CONV_REG.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG.csv) `verdict` | `DERIVED` |
| the 12 cells | see Table W-2.1 | same, `n_pairs`, `T_min`, `T_max`, `in_band_share`, `n_in_band`, `crossing_year` | `DERIVED` |
| interchangeable cells that still cross parity | 4 of 4 | same, `verdict`, `crossing_year` | `DERIVED` |
| HKG / JPN cells | 6 × `NO-COMPLETION-SERIES` | same, `verdict` (rows HKG/JPN) | `OBS` (absence) |
| `m`-constancy | A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02 | [`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv) | `SIM` |
| capped cells | 35 of 6,720 per panel | same, `completion_uis`/`completion_cohort` columns | `DERIVED` |
| three 2024 completion values | 98.30461883544922 / 92.4139633178711 / 75.02525329589844 | [`UNIVERSALIZATION_SERIES.csv`](../data/UNIVERSALIZATION_SERIES.csv) `value` (V48) | `OBS` |
| level GER end years | 2018 (lower, upper) | same, `indicator`, `year` (V50) | `OBS` |
| `ger_secondary` 2024 | 85.2945085684493 | same, `value` (V51) | `OBS` |

**Conditions that travel with it.** `CONSTANT` is A17-only and may never appear without the panel; `THIN` is
unmeasured, not clean; it is a conversion register only (no NER statistic, no demand object); a crossing is descriptive,
not a trend (KOR/upper crosses five times; PHL primary's crossing lies *between* 2017 and 2021, not in 2021); two of
the three headline numbers are unpaired; the block's authoring defect (asserting its own result) is recorded and not
verdict-bearing.

---

# Appendix B — Register 2: the participation margin (EXP-22)

**What it is.** The observed same-year gross − net enrolment gap per level, with an identity test run **before** the
observed series was opened. Verdict `NO-OBSERVED-COUNTERPART` (`ACCEPT-WITH-CONDITIONS`; D161, D164). Predeclaration
`8f47aa21…`, enforced pre-input and pre-verdict; deterministic 6/6; 22/22 SHA; count-blind `PASS`.

*Table B-1 (A-1 caption): `DERIVED`/`SIM` as printed; object: PHL gross − net spans and the model placement subject; no κ window; status `LIVE`. Permitted sentence: C-16.*

| read-out | value | source (file + column) | label |
|---|---|---|---|
| primary span | n=30, 2.196578 (1976) – 14.627307 (1999), median 10.086482 | [`PART_MARGIN_DESC.csv`](../extensions/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv) `n_pairs`, `span_min_pp`, `span_max_pp`, `span_median_pp`, `pair_year_min`, `pair_year_max` | `DERIVED` |
| lower span | n=4, 17.412040 (2017) – 29.239540 (2016), median 28.518155, not `THIN` | same | `DERIVED` |
| upper span | n=2, 46.062110 (2014) – 51.704530 (2015), median 48.883320, `THIN` | same, `thin` | `DERIVED` |
| identity | `NO-REGISTERED-COUNTERPART` at 3 of 3 levels; 1 register line per level, 0 matching | same, `identity_test`, `n_register_lines`, `n_matching_lines` (V54) | `DERIVED` |
| placement | `WITHHELD-NO-IDENTITY`; `comparison_performed = FALSE` | same, `placement`, `comparison_performed` (V54) | `DERIVED` |
| audited candidates | every candidate object, and the model object | [`OBJECT_IDENTITY_AUDIT.csv`](../extensions/part_margin_desc_2026-11-20/results/OBJECT_IDENTITY_AUDIT.csv) | `DERIVED` |
| model shares, orientation only | v1.6 0.900000 / 0.900000 / 0.820000; v1.7 0.9956438554 / 0.9534771716 / 0.8003108482 (2024) | `PART_MARGIN_DESC.csv` `model_share_v1_6_2024`, `model_share_v1_7_2024` (V55) | `SIM` |

**Conditions that travel with it.** The record correction (V35b's `THIN` note for a 4-pair level) is recorded and the
`< 3` rule governs (D165(vii)); the negative is scoped to the register's universe and the audited candidate set; the
placement hazard is permanent; the pairs end 2017/2015, so no 2024 comparison exists; the block's label set omitted
its positive branch (authoring defect, not verdict-bearing).

---

# Appendix C — Register 3: the D63 bound split (EXP-23)

**What it is.** The log-gap decomposition of the upper-secondary residual at the declared one-stage pair, plus three
bound comparisons against the observed envelope. Verdicts `RESIDUAL-SPLIT` / `BOUNDS-EDGE`
(`ACCEPT-WITH-CONDITIONS`; D162, D164). Predeclaration `dc714963…`, enforced at verdict time; deterministic; 14/14
SHA; 11/11 stated numbers reproduce.

*Table C-1 (A-1 caption): `DERIVED`/`DECLARED` as printed; object: the D63 upper-only leg; no κ window; status `LIVE`. Permitted sentence: C-19.*

| read-out | value | source (file + column) | label |
|---|---|---|---|
| gap | 14.974746704101562 pp (90 − upper 2024) | [`D63_BOUNDS_RESULTS.csv`](../extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv) row S1 `value_num` | `DERIVED` |
| G / P / Q | 0.18198490285627197 / 0.1066446793553944 / 0.07534022350087775 | rows S2–S4 `value_num` | `DERIVED` |
| identity residual | 1.942890293094024e-16 | row S5 `value_num` | `DERIVED` |
| split | 58.6008386858443 % / 41.3991613141558 % | rows S8, S9 `value_num` (V58) | `DERIVED` |
| B1 | 97.0425841315231 vs record max 92.4139633178711 → `OUTSIDE` | row B1 `value_num`, `outcome` (V59) | `DERIVED` |
| B2 | 0.9738788032543533 in [0.8891573087274445, 1.0724421619315192] → `INSIDE` | row B2 `value_num`, `comparison`, `outcome` (V60) | `DERIVED` |
| B3 | [82.170551, 99.108631] contains 90 → `INSIDE` | row B3 `value_num`, `value_display`, `outcome` (V61) | `DERIVED` |
| contemporaneous sensitivity | pipeline −0.14544291665697634; ratio 1.145442916656977; ratio 0.8118389321518255 | rows X1–X3 `value_num`, `used_in_verdict = FALSE` (V62) | `DERIVED` |
| verdicts | `RESIDUAL-SPLIT`; `BOUNDS-EDGE`; D63 `UNABLE as to cause` | rows V1–V3 `value_display` | `DECLARED` |

**Conditions that travel with it.** The t−3 sentence is mandatory with every citation of the split; B3 is cross-year
arithmetic and is not evidence that 90 was reachable; `BOUNDS-EDGE` = 1 of 3 outside; quote the ratio range at full
precision where 0.9738788032543533 is the comparator; the leg is upper-only; the "required" values are `DERIVED`
inversions, not `REQUIRED-STATE` objects.

---

# Appendix D — Register 4: the κ use register (EXP-24)

**What it is.** A static register of the per-system transition ratio κ and of every κ use in a declared 17-file
universe, with windows, stationarity statistics, hold-out cells and four admissible sentences. Verdict
`REGISTER-NARROWED` (block label `USE-OUTSIDE-WINDOW`; `ACCEPT-WITH-CONDITIONS`; D163, D164). Predeclaration
`db20d123…`, enforced at verdict time; deterministic 4/4; 14/14 SHA.

| system | κ (full) | window (pre-2021 / full) | slope /yr | half-shift | hold-out | admissible use | sentence |
|---|---:|---|---:|---:|---|---|---|
| PHL | 0.949135 | 2003–2017 / 2003–2024 | −0.000704 | **2.1348 pp** | 2/2 | `SENTENCE-ONLY` | C-23 |
| KOR | 0.989758 | 2005–2020 / 2005–2023 | +0.002875 | 0.6354 pp | **0/3** | `SENTENCE-ONLY` | C-24 |
| KHM | 0.594984 | 2000–2017 / 2000–2023 | +0.017318 | **7.4361 pp** | 1/2 | `SENTENCE-ONLY` | C-25 |
| CHN | 0.722222 | 2012–2020 | +0.041728 | **25.6573 pp** | 0 cells | `REPORTED-ONLY` | C-26 |
| HKG / JPN | — | empty | — | — | — | **`NONE`** (non-entrant) | — |

*Table caption (A-1):* `DERIVED`; object: the transition-ratio κ per system; windows as printed; status `LIVE`.
Permitted sentence: C-28. Source: [`KAPPA_WRITE_REGISTER.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv)
columns `kappa_full`, `window_pre2021_upper`, `window_full_upper`, `slope_ratio_per_year`, `half_median_shift_pp`,
`holdout_within`, `admissible_use`, `admissible_sentence` (V64).

*Table D-2 (A-1 caption): `DERIVED`; object: the κ use register and its universe; windows as printed above; status `LIVE`. Permitted sentence: C-28.*

| read-out | value | source |
|---|---|---|
| uses enumerated / applied / in-window | 309 / 299 / 233 (77.9264 %) | [`KAPPA_WRITE_SUMMARY.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_SUMMARY.csv) rows `n_uses`, `n_applied`, `n_in_window`, `pct_in_window_of_applied` |
| below / above / barred | 64 / 4 / 68 | same, `n_out_below`, `n_out_above`, `n_barred` |
| projections / `NOT-COMPARABLE` (subsets of the 68, not additions) | 64 / 44 | same, `n_projection`, `n_not_comparable` |
| observed-pair descriptive uses in-window | 132 | same, `n_observed_descriptive_in_window` |
| live verdicts resting on a barred use | 0 | same, `live_verdict_load_bearing_uses` |
| universe / corpus files with a κ token | 17 / 193 | same, `universe_files`, `corpus_files_with_kappa_token` |
| the seven barred objects | `KAPPA_LINK.csv` (62 uses, 31 of 53 years outside the window) plus the v1.5 guard/audit files, the v1.6 audit/panel files, and the two 2027 prose sentences | same, `barred_files`; [`FINDINGS.md`](../extensions/kappa_write_2026-11-20/FINDINGS.md) §3 (V67) |
| the two κ symbols | transition ratio (registered) vs `G(C) = C^κ` (excluded, D9; 2 lines) | `FINDINGS.md` §3 |

**Limits that travel with it.** The universe is 17 of 193 files — the register certifies the 17 and **does not
certify the corpus**; the projection count is a floor, not a ceiling (prose projections are detected by language);
text extraction is a reading, not a measurement (three declared pre-run amendments, verdict invariant); the
κ-conditioned objects are aggregated at file-span granularity; and the 100 % bar was not met — that is the finding,
and nothing was repaired to make it pass.

---

# Appendix E — The HELD ledger (14 items) and the HKG re-entry condition

Carried verbatim from the Council's Appendix B (D164/D165(ix); V74). Every item is `HELD`, none is fabricated, **user
approval is required for any of them** (D157), and **no cell is issued against any item**.

| # | HELD object | what it would change | cell that would consume it |
|---:|---|---|---|
| H1 | measured places / PTR series (DepEd/CHED seats vs enrolment) | the `places` object and any place-based capacity test | none issued; would re-open EXP-19's identification gate |
| H2 | capacity utilisation | the V_O validation and the ceiling object | none |
| H3 | private/public shares of enrolment and provision | the A5 two-tier sorting object | none |
| H4 | SHS voucher take-up | the `v1.7` Tier-O take-up margin | none |
| H5 | upper-secondary completion for additional systems | the 43-pair κ/CEIL register (the only route beyond 43) | none |
| H6 | single-age HKG population 1971–1996 | HKG re-entry, part 2 | none |
| H7 | HKG senior-secondary queue / places | HKG re-entry | none |
| H8 | PSA microdata | returns by education; the human-capital/signalling rivals (design-only) | none |
| H9 | WB Enterprise Surveys | the credential module / rung-4 | none |
| H10 | real per-pupil spending | the spending channel (A2d) | none |
| H11 | annual capacity / enforcement | **D76's C4 re-opener** — the only authorised re-opener that could reopen the phase | none |
| H12 | measured credential-queue (rung-4) series | the upper-secondary ceiling / D63 | none |
| H13 | PHL/KHM/CHN/JPN shadow participation | the closed shadow-education claims (do not reopen without a new test) | none |
| H14 | measured remittance→schooling coefficient | the push–pull direction (R13) | none |

*Table caption (A-1):* `HELD`; object: the 14-item ledger; no κ window; status `LIVE` (the asks stand). Permitted
sentence: C-31.

**HKG re-entry condition — two parts, both required, plus the standing gate.** `DEFER-HKG` stands until **(i)** a
stock-NER object passes D120's **N2** construct test on the systems that have completion, **and (ii)** the **HELD
single-age HKG population 1971–1996** (H6) is on disk — **and**, those two parts once satisfied, **(iii)** a **new
Council decision** authorises re-entry (D120, D133, D156 EXP-24 item 5(iii), D157). Until then the frozen stock-NER
design is preserved unrun and no HKG sentence may appear in this write-up: the six HKG cells are
`NO-COMPLETION-SERIES` (Appendix A), and the two-part condition is stated here rather than executed.

---

# Appendix F — Banned-sentence register (quoted only to bar)

<!-- BANNED-REGISTER-START -->

**None of the phrasings in this appendix is a sentence of this document.** They are reproduced here **only to bar
them** (D158(6), A-3): a caption, table cell or claim that uses one is returned. Copied from
`SYNTHESIS_026.md` Appendix A (B1–B26), with B-27 and B-28 added by EXP-24's own sentence constraints.

| # | barred phrasing (quoted only to bar) | source | why |
|---:|---|---|---|
| B-1 | "demand falsified" | D124/D158(6) | the A3-D result is a specification failure, not demand evidence |
| B-2 | "the participation margin is duplicated" (as a cell-level sentence) | D152 C-1 | the per-level split is mandatory |
| B-3 | "the upper-secondary ceiling is structural" | D153(xiii)/D158(6) | EXP-23 removes it; the mirror image is also barred |
| B-4 | "survival loses 50.7 %" | D140/D153(iii) | the split is unidentified |
| B-5 | "fix survival only" | D140 | s\* > surv_max |
| B-6 | "A17 0/33 vs A00 9/33" without its sentence | D158(6) | the difference is two declarations, not behaviour |
| B-7 | "behaviourally N pp wrong" | D158(6) | not decomposable to behaviour |
| B-8 | "the model is 13.4 pp low at primary" | EXP-21 §5 | the same claim in plain clothes; fuses two objects |
| B-9 | "completion rose to 98.3 %" | D155/EXP-21 | the object must be named; no unqualified "completion" |
| B-10 | "completion and GER are one scale" | EXP-21 | true in 4/12 cells, false in 8 |
| B-11 | "the model's measurement factor matches the observed ratio" | EXP-21 §5 | the observed ratio is not constant; `m` is capped where the ceiling binds |
| B-12 | "the participation share is too low (0.900 vs 0.996)" | EXP-22 §5 | compares two synthetic classes and implies an unobserved benchmark |
| B-13 | "58.6 % of the residual is the pipeline" without the t−3 sentence | EXP-23 §7 | the contemporaneous share is −0.145443 (sign flip) |
| B-14 | "90 is reachable / the record contains the required path" | EXP-23 §5 | B3 is a cross-year arithmetic combination, not a counterfactual |
| B-15 | "the upper-secondary ceiling is not structural" | EXP-23 §5 | the mirror image is barred too |
| B-16 | "κ ≈ 0.95 for the Philippines"; "κ is stable across systems"; "κ-STABLE is forward-usable"; "κ predicts upper completion"; "the κ-link validates the model path"; "CHN is a forward constraint"; "the register is clean" | EXP-24 §5 | the register's own banned examples |
| B-17 | the stale forward-field value carried by `KAPPA_WRITE_REGISTER.csv` column 15 (`exp11_forward_constraint`) on the PHL and KOR rows; "κ is eligible as a forward constraint" | EXP-24 D-2; V65 | a stale EXP-11 field contradicted by column 16's `WINDOW-ONLY`; **the literal string is not reproduced here and may not ship** — relabel or drop (D165(viii)) |
| B-18 | "every κ use on disk is in-window" | EXP-24; V63 | 77.93 % of 299 applied uses in 17 adjudicated files |
| B-19 | "the proxy is consistent with the required coverage" | D152/D157 | `PROXY-SILENT` = `NOT-IDENTIFIED` |
| B-20 | "the representation capability holds at both levels" | D153(ix) | single-tier: strict both-level coexistence 0/15 |
| B-21 | "conditional level reproduction" untagged; "the model reproduces the PHL level path" | D77/§5.1 | the class tag, the statistic and the date are mandatory; the shell's unclassed one-line headline is barred as a post-close sentence |
| B-22 | "v1.2 passes" | `SYNTHESIS_025.md` §8 | 9/33 is a placement label, not a pass |
| B-23 | "the repair made the model worse" | `SYNTHESIS_025.md` §8 | the 0/33 vs 9/33 difference is two declarations |
| B-24 | "EXP-25 ran"; a `SPINE-REPLACED` verdict | D166 | EXP-25 did not run; the spine is a write-up act, and the Council issued no such verdict |
| B-25 | "no observed counterpart exists" (unqualified) | EXP-22 C-3 | say "no object among the audited candidates / no register line" |
| B-26 | "the 12-arm fit MAE is 2.03–3.29 pp" | D165(x) | that is the six `law_only` + `capacity_only` range; the 12-arm range is 1.047492271754753–3.2916863270693772 |
| B-27 | any κ-implied value for a future year, including the 2027 upper-completion sentence in D133 and `STATUS.md` | EXP-24 §5 | a stated future value computed from κ; barred in both places; D63 `UNABLE` is unaffected |
| B-28 | any citation of the κ-link as validation of the model path | EXP-24 §3 object 1 | a projection over 53 model years, 31 outside the window, applied to a model-generated lower series |

<!-- BANNED-REGISTER-END -->

*Table F-1 (A-1 caption):* quoted-and-barred register, `DECLARED`; object: the barred phrasings B-1…B-28; no κ window; status `LIVE`. No row of this table is a permitted sentence — the only permitted sentence it attaches to is C-36, and every row is present **only to be barred**.

**Negated form only.** The verdict token barred by B-24 appears in this document exactly once outside this register, in
the status table at the top, inside the negation "the Council issued **no** … verdict"; the barred assertion of B-24
appears only here.

---

# Appendix G — Provenance index and read-order resolution

**Every number in this document traces to one of the following.** `V`-ids are rows of
[`VERIFICATION_026.csv`](../../08_council/brief_026/VERIFICATION_026.csv) (columns `id`, `source_path`,
`source_column`, `derivation`).

*Table G-1 (A-1 caption): `DERIVED` index over `OBS`/`SIM` values; object: every number group used in this document; no κ window; status `LIVE`. Permitted sentence: C-36.*

| # | number(s) used here | file | column / row | V-id |
|---:|---|---|---|---|
| 1 | 12-arm fit and holdout ranges; per-arm fit/hold MAE; `M0`–`M4` | [`anchor_table.csv`](../model/anchor_out/anchor_table.csv) | `fit_mae`, `hold_mae`, `M0`–`M4`, `scaling_verdict` | V69 |
| 2 | 4.35 pp trend; 8.60 pp persistence | [`calibration_table.csv`](../model/calib/calibration_table.csv) | `naive_trend`, `naive_persistence` (`iso = PHL`) | V75 |
| 3 | repair-cell fit MAE; `n_contained`; `signs_ok` | [`repair_table.csv`](../model/calib/repair_table.csv) | `PHL_fit_mae`, `n_contained`, `signs_ok` | — (closeout §2) |
| 4 | repaired exponents and required values | [`repair_scaling.csv`](../model/calib/repair_scaling.csv) | `generated`, `A1_value`, `A1_se`, `A3_lo`, `A3_hi` | — |
| 5 | 9/33 and 0/33 with per-level splits | [`observed_path_A17.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/observed_path_A17.csv) | `within_5pp_A00`, `within_5pp_A17` | V75 |
| 6 | 0/33 vs ≥17/33; crossings 1/3; 15/15, 30/30, 0/15 | [`v1_7_checks.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/v1_7_checks.csv) | rows S1–S3, `synthetic_value`, `threshold`, `legs_passed` | V75 |
| 7 | representation cells | [`representation_cells.csv`](../extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/representation_cells.csv) | `unfilled`, `queue_ratio`, `coexists` | V75 |
| 8 | the 12 conversion cells | [`CONV_REG.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG.csv) | `n_pairs`, `T_min`, `T_max`, `in_band_share`, `n_in_band`, `crossing_year`, `verdict` | V39–V46 |
| 9 | 2017 `T` and completion (digit hazard) | [`CONV_REG_DETAIL.csv`](../extensions/conv_reg_2026-11-20/results/CONV_REG_DETAIL.csv) | `T`, `completion_value`, `ger_value` | V49 |
| 10 | `m`-constancy and the 35 capped cells | [`M_CONSTANCY.csv`](../extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv) | `panel_path`, `completion_uis`, `completion_cohort` | V47 |
| 11 | the three 2024 completion values; GER end years; `ger_secondary` 2024; the three completion maxima | [`UNIVERSALIZATION_SERIES.csv`](../data/UNIVERSALIZATION_SERIES.csv) | `value` at `indicator`, `iso3 = PHL`, `status = observed` | V48, V50, V51 |
| 12 | three spans, identity, placement, `comparison_performed`, model shares | [`PART_MARGIN_DESC.csv`](../extensions/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv) | `n_pairs`, `span_*`, `identity_test`, `n_register_lines`, `n_matching_lines`, `placement`, `comparison_performed`, `model_share_*` | V52–V55 |
| 13 | the 21 audited candidate objects | [`OBJECT_IDENTITY_AUDIT.csv`](../extensions/part_margin_desc_2026-11-20/results/OBJECT_IDENTITY_AUDIT.csv) | all rows | V54 |
| 14 | gap, G, P, Q, split, B1–B3, sensitivity, verdicts | [`D63_BOUNDS_RESULTS.csv`](../extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv) | `value_num`, `value_display`, `comparison`, `outcome`, `used_in_verdict` | V57–V62 |
| 15 | κ values, windows, slopes, shifts, hold-outs, sentences | [`KAPPA_WRITE_REGISTER.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv) | `kappa_full`, `window_*`, `slope_ratio_per_year`, `half_median_shift_pp`, `holdout_within`, `admissible_sentence` | V64, V67 |
| 16 | κ counts and the 17-of-193 universe | [`KAPPA_WRITE_SUMMARY.csv`](../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_SUMMARY.csv) | `metric`, `value` | V63 |
| 17 | the KOR counter-example sentence | [`FINDINGS.md`](../extensions/kappa_write_2026-11-20/FINDINGS.md) | §2 | V67 |
| 18 | the HELD ledger (14) and the HKG condition | [`DECISIONS.md`](../../08_council/DECISIONS.md) | rows D157, D133, D156 | V74 |
| 19 | D76/D77 and the phase verdict | [`DECISIONS.md`](../../08_council/DECISIONS.md) | rows D76, D77 | V72 |
| 20 | the read-order defect | [`EXTERNAL_CHECKIN.md`](../../EXTERNAL_CHECKIN.md) | read-order items 2, 5, 7 | V71 |
| 21 | the shell's stale headline and vocabulary | [`PHASE_WRITEUP_SHELL.md`](PHASE_WRITEUP_SHELL.md) | whole file, line 15 | V68 |

**Read-order resolution (A-8).** All fourteen links of the corrected order in W-6.3 resolve, and every inline link
above resolves to an existing file; the resolution check and its output are recorded in
[`PHASE_WRITEUP_GATE.md`](PHASE_WRITEUP_GATE.md) (A-8). Two links are deliberately **not** present anywhere in this
document because their targets do not exist: `06_report/AGENT_PROTOCOL.md` and `06_report/MASSIFICATION_CLOSEOUT.md`
(the root copies are used instead), and `LEAD_HANDOFF.md` is replaced by
[`HANDOFF_expert-council.md`](../HANDOFF_expert-council.md).
