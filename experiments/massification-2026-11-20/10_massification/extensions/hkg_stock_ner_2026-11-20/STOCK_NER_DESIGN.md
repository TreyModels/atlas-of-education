# STOCK-NER-DESIGN — the stock-style NER object for the HKG diagnostic transfer (EXP-10)

> `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

**Worker SN, 2026-11-21 (Asia/Shanghai). DESIGN + FROZEN SPECIFICATION. RUN-READY. NOT RUN.**

**LABELS.** Every model-derived number in this file is **SYNTHETIC** (from the frozen v1.2 panel) or
**DERIVED** (arithmetic on it). Anything observed is **OBSERVED-REFERENCE-ONLY** and is not read by the object.
**No causal claim. No direction or push–pull claim. No portability claim. No capacity-timing claim. No
phase-verdict claim.** `BLOCKED-*` is terminal.

**Companion files:** `PRE_DECLARATIONS.md` (the binding, frozen specification — where this file and that file
disagree, **the predeclaration wins**), `DRY_RUN_PLAN.md` (the run protocol, not executed),
`RUN_MANIFEST.json` / `SHA256SUMS.txt` (hashes).

**What this file is.** The full design record for the object: what it is, why it is the right analogue of the
UIS net enrolment ratio rather than another flow object, how it is computed from the model's own columns, why
it carries no free parameter, how it differs from the object M1-NER tested, what its construct test does, what
direction it is expected to move, and what it would and would not license. It contains **one inert worked
example** (§11) and **no result**.

**What this file is not.** It is not a result, not a validation, not a comparison to Hong Kong, and not an
authorisation to run anything. `PRE_DECLARATIONS.md` §8 governs: execution is **not** authorised by this
document, by the freeze, or by a `CONSTRUCT-EQUIVALENT` outcome.

---

## 1. Why an object had to be designed at all

D114 voided the SR-9 authority for the model's cohort-flow NER analogue: the analogue is **not** construct-
equivalent to a stock reconstruction under D111's H1 bars (band max **2.685005 pp**, 7/15 band years;
first-sustained crossings **3 y** at ≥90 and **2 y** at ≥95), and the HKG transfer consequently returns
`BLOCKED-MEASURE(SR-1)` — a terminal non-verdict. D114 also named the forward path: *"a new predeclaration
specifying a stock-style NER object (e.g. grade-progression stock reconstruction) with its own construct test"*.
D120 converted that into a design task with six binding conditions (N1–N6) and **no execution**.

The object below is that stock-style object. It is deliberately **not** a repair of M1-NER: M1-NER tested a
mean of annual ratios; this is a ratio of two reconstructed stocks. The bars are unchanged. If the bars fail
again, the object is `BLOCKED-MEASURE` and the HKG arm closes on the measure.

---

## 2. The measurement problem this object has to solve

**What the target measures.** The D75 HKG targets are **net enrolment ratios** in the UIS sense
(`NER.1.cp`): the v1.2.1 addendum states the definition, and this document adopts its wording —

> the UIS stock-based NER (`NER.1.cp`: enrolled children of official age across all grades ÷ official-age
> population)
> — `generator_v1_2_addendum/PRE_DECLARATIONS.md` §2.1

Three properties of that definition matter, and each is structural, not cosmetic:

1. **The numerator spans grades.** It is a count of *pupils currently in the level*, not of pupils admitted
   this year.
2. **The denominator is an age band**, not a single-year cohort: the persons of official age for the level,
   which spans `d` single-year age groups.
3. **Both are stocks at the same instant.** The ratio is pupils ÷ persons at `t`.

**What the model has.** v1.2 is a one-year cohort-flow simulator. Its `ner` column is

```
ner = 100 * admitted_official / cohort
```

— an annual **admission flow** divided by an annual **cohort**, both of the same year. The addendum declares
the limitation in its own words:

> this is a cohort-flow NER, not the UIS stock NER … v1.2 does not carry that stock
> — `generator_v1_2_addendum/PRE_DECLARATIONS.md` §2.1

**Why the two coincide only in a special case.** If (i) the population is stationary, so every single-year
age group is the same size, and (ii) every admitted pupil stays to the end of the level, then `d` annual
admission flows of `A` fill `d` grades with `d·A` pupils out of a band of `d·C`, so
`d·A / d·C = A / C`: the stock ratio **equals** the flow ratio. Under either failure of those conditions they
diverge, and both fail on this panel:

- **Attrition.** The panel's primary `survival` (a through-level rate, §5.3) is **0.7171–0.9241** for
  `SYN00_PHL_LIKE` and **0.6830–0.8232** for `SYN28` over 1975–2025. A stock counts survivors; a flow counts
  entrants. The stock is below the flow by roughly the attrition.
- **Non-stationarity.** The synthetic cohorts grow at the declared ~2.45 %/yr back-cast rate in the early decades
  (`generator_v1_2/PARAMS.md` §2), so a backward window
  of entry cohorts is systematically smaller than the current-year flow.

**This is the whole reason a stock object is not a formality.** The HKG target is a stock ratio; the model
emits a flow ratio; a stock reconstruction from the model's own objects is the only way to ask whether the
model's flow object can stand in for the target measure at all. M1-NER asked that question with an object that
contained **no attrition** and therefore could only ever fail by the window/ramp term. This object asks it with
the attrition in, which is where the substance is.

---

## 3. The object — full algebraic definition

### 3.1 Notation

For country `c`, level `L`, year `t`, duration `d = dur_L`:

| symbol | meaning | panel column |
|---|---|---|
| `A(c,L,t)` | official-age admission flow to level `L` in year `t` | `admitted_official` |
| `C(c,L,t)` | official-age annual cohort for level `L` in year `t` | `cohort` |
| `s(c,L,t)` | the level-year's declared survival (through-level rate) | `survival` |
| `d` | declared level duration in years | `DVEC` (`sim_v1_2.py:65`; `PARAMS.md` §3) |

### 3.2 Definition (frozen; identical to `PRE_DECLARATIONS.md` §3.1)

```
w_k(c,L,t)   =  s(c,L,t) ** (k / d)                                       k = 0, ..., d-1
N(c,L,t)     =  SUM_{k=0..d-1}  A(c,L,t-k) * w_k(c,L,t)                    [pupils]
B(c,L,t)     =  SUM_{k=0..d-1}  C(c,L,t-k)                                 [persons]
STOCK(c,L,t) =  100 * N(c,L,t) / B(c,L,t)                                  [percent]
FLOW(c,L,t)  =  100 * A(c,L,t) / C(c,L,t)                                  [comparator]
DIFF(c,L,t)  =  STOCK(c,L,t) - FLOW(c,L,t)                                 [pp]
```

The object is `STOCK`. `FLOW` is the comparator, and is the panel's `ner` column re-derived (§6).

### 3.3 In words

- **Grade 1** at `t` is the cohort admitted at `t`, counted at its admission flow `A(t)` with weight `1`.
- **Grade `k+1`** at `t` is the cohort admitted at `t−k`, still in the level `k` years later, carried at
  `A(t−k)·s^(k/d)` — its admission flow decayed by the constant-hazard holding weight.
- **The numerator** `N` sums those `d` surviving cohorts: it is the reconstructed **pupil stock** of the level
  at `t`.
- **The denominator** `B` sums the same `d` entry cohorts at their entry-year sizes: it is the reconstructed
  **official-age band** at `t` — `d` single-year age groups, each counted as the model recorded it when it was
  the entry-age group.
- **The ratio is the stock NER.** Percent scale, like `NER.1.cp`.

### 3.4 Durations, and why the construct test is primary-only

`d = (6, 3, 3, 4)` for (primary, lower_secondary, upper_secondary, tertiary), from the frozen factory. The
construct test is scored on **primary only** (`d = 6`), because the D75 HKG target is primary NER and H6 fixes
the scope to primary. Other levels are computed only inside the descriptive panel-wide sensitivity of
`PRE_DECLARATIONS.md` §6.6 and never carry a verdict.

For primary, `STOCK` exists from **1975** (a complete six-year window 1970–1975). Nothing is back-cast,
truncated, or imputed at the left edge.

---

## 4. How it is computed from the model's own columns — step by step

1. **Read** `synthetic_panel_v1_2.csv` (6 720 rows; 67 columns; `label = SYNTHETIC` everywhere).
2. **Index** rows by `(country, year, level)`; assert the index is complete and unique for the two test types
   over 1970–2025.
3. **For each target row** `(c, L, t)` with `t−d+1 ≥ 1970`:
   1. read `s = survival(c,L,t)`;
   2. for `k = 0..d−1`, read `A_k = admitted_official(c,L,t−k)` and `C_k = cohort(c,L,t−k)`;
   3. compute `w_k = s ** (k/d)`, accumulate `N += A_k*w_k` and `B += C_k`;
   4. write `STOCK = 100*N/B`.
4. **Compute the comparator** `FLOW = 100*A_0/C_0` and verify it against the addendum panel's `ner` column at
   `%.10g` display precision (abort on mismatch — no substitution).
5. **Band years:** `t ≥ 1975` and `85.0 ≤ FLOW(t) ≤ 95.0`.
6. **Crossings:** first-sustained 5-year crossing at 90 and 95 for both series; `first-at-or-above` reported
   alongside.
7. **Score** the two conditions of `PRE_DECLARATIONS.md` §6 and emit exactly one token from §6.5.

No step reads an observed series, a target year, a threshold-calibration quantity, or any HKG object.

### 4.1 The `SYN28` test type

`SYN28` is the **highest-2020-GDPpc** synthetic type on the frozen panel (`gdppc` 2020 = **48 270.81143**, top
of the 30 countries; next is `SYN23` at 43 321.30) and is the generator's `SYN_HKG_LIKE` host
(`generator_v1_3/TUNE_LOG.md:50`). N2 requires it as the second test type so that the object cannot be cleared
on the PHL-like anchor alone: a construct that only works on the anchor is a construct about the anchor, not
about the model class. `SYN28` is applied **the same formula with the same `d` and the same bars**; no
country-specific adjustment exists anywhere in the object.

---

## 5. Why the object is parameter-free

"Parameter-free" here means: **no number in the object was chosen, fitted, tuned, calibrated, or set by
hand.** The claim is checkable, and it rests on five facts.

### 5.1 Every number is either a panel value or a frozen constant

`A`, `C`, `s` are columns of the frozen panel; `d` is the frozen factory's declared duration. Nothing else
enters. There is no intercept, no slope, no anchor array, no per-country override, no per-level offset, no
smoothing window chosen for fit, and no constant of proportionality.

### 5.2 The exponent is implied, not chosen

`k/d` is the grade index over the declared duration. Given `d` and `k` it takes one value. There is no free
exponent to estimate and no freedom to place the decay differently across grades.

### 5.3 Both endpoints of the holding weight are given by the model

- `w_0 = 1`: the cohort admitted this year is counted before any attrition. This is not a choice — it is what
  "entry cohort" means.
- `w_d = s`: a cohort that has completed the level's declared duration retains exactly the model's own
  through-level survival. This reproduces the model's **own** completion identity,

  ```
  completion_cohort(c,L,t) = admitted_official(c,L,t-d) * survival(c,L,t)      sim_v1_2.py:606
  ```

  so the object spends the model's survival the way the model itself spends it, and adds no second survival
  notion.

A geometric (constant-hazard) schedule is the schedule with **no free shape value** between two fixed
endpoints `1` and `s`: it is the unique constant-hazard interpolation, so the object introduces **zero** new
degrees of freedom into the model. This is the one *declared* choice in the object (the shape is declared, its
value is not), and §13.2 records what was not adopted and why.

### 5.4 Nothing is estimated from data

There is no estimation step of any kind: no regression, no calibration, no anchor interpolation, no ratio
fitted to an observed series. The object is a closed-form function of the frozen panel.

### 5.5 Nothing is estimated from the target

The target years are not operands (`PRE_DECLARATIONS.md` §3.6). The construction has no country-specific
input, so it cannot be tuned toward any country's crossing. Guard **G6** asserts mechanically that the runnable
module contains no `1974`/`1979` literals at all, and **G4** asserts the operand allow-list is exactly
`{admitted_official, cohort, survival}` plus row identity.

---

## 6. The comparator, and why the object is not the `ner` column

`FLOW` is re-derived from `admitted_official` and `cohort` and cross-checked against the addendum's `ner`
column at display precision; it is used **only** to score the construct test. The object never reads `ner*`.

The object equals the comparator only in the degenerate case `s = 1` **and** stationary `A/C` (§8.1). On this
panel both conditions fail, so `STOCK ≠ FLOW` by construction — which is precisely the quantity the construct
test measures. If the object were defined to reproduce `FLOW`, the test would be vacuous.

---

## 7. Why this is not the object M1-NER tested

| property | **M1-NER's stock analogue** (tested, `9eb35a92…`) | **STOCK-NER-D** (this object) |
|---|---|---|
| formula | `100 * (1/d) * SUM_k A(t−k)/C(t−k)` — **mean of annual ratios** | `100 * SUM_k A(t−k)·w_k / SUM_k C(t−k)` — **ratio of two stock sums** |
| numerator | a mean of annual admission *flows* | a reconstructed **pupil stock** (surviving entry cohorts) |
| denominator | a mean of annual cohorts (i.e. of flows) | a reconstructed **age band** (sum of `d` cohorts) |
| units | flow ÷ flow (a period rate) | pupils ÷ persons (a stock ratio, as `NER.1.cp`) |
| survival | **not used** — no attrition in the object | used, through the declared holding weight `w_k` |
| can it fall below the flow by attrition? | no: by construction it contains no attrition | yes: the attrition term `sigma_bar` is in the object |
| failure mode it can detect | only the window/ramp lag (measured: up to 2.685 pp, 2–3 y) | the window/ramp lag **and** the stock-vs-flow attrition wedge |
| level d | primary `d = 6` | primary `d = 6` (same, unchanged) |
| bars, band rule, crossing rule | D111 H1 | **identical** (N2; `PRE_DECLARATIONS.md` §6) |

**In one sentence:** M1-NER compared the flow to a backward average of the *same* annual ratio and measured
2.7 pp; this object compares the flow to a genuine stock and therefore measures something the earlier test
could not see. That is the substantive reason D114's forward path was a stock object and not a re-weighting of
the old one.

**Where the two objects do agree:** both are lagging, backward-looking transforms of the same entry-cohort
series, so both are expected to place crossings **later** than the flow (N3). The direction is shared; the
magnitude is not, and the magnitude is where the attrition lives.

---

## 8. Properties of the object (analytic, before any computation)

### 8.1 Degenerate identity

If `A/C` is constant in `t` and `s = 1`, then `N = d·A`, `B = d·C`, so `STOCK = 100·A/C = FLOW` exactly. The
object is therefore a strict generalisation of the flow analogue, and the construct test is a test of the two
conditions under which the flow is admissible — stationarity and no attrition — rather than a test of an alien
quantity.

### 8.2 Exact decomposition

```
STOCK = FLOW_w * sigma_bar
FLOW_w    = 100 * SUM_k A(t-k) / SUM_k C(t-k)          (window-average entry rate)
sigma_bar = SUM_k A(t-k) w_k / SUM_k A(t-k)            (weighted mean holding weight)
```

This is algebra, not a measurement: it says the object is the window-average entry rate **damped by the
holding weight**. It isolates the two mechanisms the construct test can fail on.

### 8.3 Direction (pre-registered; N3)

- `sigma_bar < 1` whenever `s < 1` (weights are non-increasing, `w_0 = 1`, `w_{d−1} < 1`), so the object sits
  **below** the window-average entry rate.
- If the entry rate is rising, `FLOW_w < FLOW(t)`, so the object sits below the current flow **twice over**.
- A backward-weighted average of a rising series crosses any threshold **no earlier** than the series itself.
  Therefore `STOCK` crossings can only be **later** than `FLOW` crossings — never earlier. This is the formal
  content of N3, and it is why a `TRANSFER-FAILS` on this object is confirmatory rather than surprising.

### 8.4 Left edge and missing data

`STOCK` is defined only on complete windows (§3.4). No partial window, no imputation, no extrapolation. If an
operand row is missing the run fails closed (`BLOCKED-INPUT`) rather than skipping the year.

### 8.5 Monotone in survival (a declared property, not a fitted one)

For fixed `A` and `C`, `STOCK` is non-decreasing in `s`: a higher survival means more pupils retained, hence a
higher stock. This is what makes the object interpretable as a stock rather than as an index: its movement is
in the direction the underlying quantity moves.

---

## 9. The construct test (summary; the binding text is `PRE_DECLARATIONS.md` §6)

| element | value |
|---|---|
| test types | **T1** `SYN00_PHL_LIKE` / primary; **T2** `SYN28` / primary — **both** must pass |
| band condition | `|STOCK − FLOW| ≤ 2.0 pp` in **every** year with `85.0 ≤ FLOW ≤ 95.0` and a complete window |
| crossing condition | first-sustained (5 consecutive years ≥ `T`) crossing years differ by **≤ 1 y** at **T = 90** and **T = 95** |
| passing token | `CONSTRUCT-EQUIVALENT` (never `PASS`) |
| failing tokens | `BLOCKED-MEASURE(N2-BAND)` / `(N2-CROSSING)` / `(N2-BOTH)` / `(N2-EMPTY)` — all **terminal** |
| override | any moved parameter, changed threshold/target/tolerance, added free parameter, or target-year reference → `FAIL-RE-FIT`, run void |
| descriptive extra | panel-wide 30 countries × 4 levels band display, `DESCRIPTIVE-SENSITIVITY`, never verdict-bearing |

The test compares a **synthetic** stock to a **synthetic** flow. It is a measurement/construct test on the
simulator's own interface; it is not an HKG test and cannot become one.

---

## 10. Expected direction, and what would be surprising

**Pre-registered (N3):** a stock object can only move crossings **later**. `TRANSFER-FAILS` is the **expected
and confirmatory** outcome of any later transfer run on this object; `TRANSFER-HOLDS` would be the **more
informative** outcome because it is the harder one.

**Pre-registered for the construct test itself:** the band difference is expected to be **systematically
negative** (stock below flow) and **dominated by the holding-weight term**, because the panel's primary
survival is materially below 1 throughout the window (§2, §5.3). Since the band bar is ±2.0 pp, a
`BLOCKED-MEASURE` outcome is a **live possibility that the design accepts in advance** — N2 says a failure is
not re-specified.

**What would actually be surprising:** a `STOCK` that sits **above** `FLOW` in band years, or a `STOCK`
crossing **earlier** than `FLOW`. Either would contradict §8.2–§8.3 and would indicate an implementation
error, not a finding; the run must then be treated as void and investigated, not reported.

**What is deliberately not predicted here:** the magnitude of the wedge at any band year. It is not computed in
this file, and the single worked example in §11 is at a year that is **not** a band year on either test type,
precisely so that the illustration cannot be read as a construct-test observation.

---

## 11. Worked arithmetic example — **INERT / SYNTHETIC, NOT A RESULT**

> **This section is arithmetic on the frozen v1.2 panel, run by hand, to show exactly how the object is
> computed. It is not a construct-test observation, not a finding, and not evidence about anything. The year
> chosen is 1992, which is (i) not a band year on either test type — `FLOW` = 77.90 and 78.57, both below 85 —
> and (ii) outside the 1970–1980 window in which the HKG target years fall. Nothing here is extrapolated to a
> band year, and no conclusion is drawn from it.**

### 11.1 T1 — `SYN00_PHL_LIKE`, `primary`, `t = 1992`, `d = 6`

Inputs read from `synthetic_panel_v1_2.csv`:

```
survival(1992) = 0.7387918583            s ** (1/6) = 0.9507952793
```

| `k` | year `t−k` | `A = admitted_official` | `w_k = s^(k/6)` | `A · w_k` | `C = cohort` |
|---:|---:|---:|---:|---:|---:|
| 0 | 1992 | 1 468 909.518 | 1.0000000000 | 1 468 909.5180 | 1 885 585.284 |
| 1 | 1991 | 1 428 423.256 | 0.9507952793 | 1 358 138.0887 | 1 840 493.201 |
| 2 | 1990 | 1 389 245.011 | 0.9040116631 | 1 255 893.6929 | 1 796 479.454 |
| 3 | 1989 | 1 351 334.450 | 0.8595300218 | 1 161 512.5292 | 1 753 518.257 |
| 4 | 1988 | 1 314 651.097 | 0.8172370871 | 1 074 381.6331 | 1 711 584.438 |
| 5 | 1987 | 1 279 154.911 | 0.7770251645 | 993 935.5551 | 1 670 653.429 |
| | | **Σ A = 8 231 718.243** | | **N = 7 312 771.0170** | **B = 10 658 314.0630** |

```
STOCK = 100 * 7312771.0170 / 10658314.0630 = 68.610955 %
FLOW  = 100 * 1468909.518 / 1885585.284     = 77.902046 %
DIFF  = 68.610955 - 77.902046               = -9.291092 pp
```

Decomposition (`§8.2`):

```
sigma_bar = 7312771.0170 / 8231718.243 = 0.888365
FLOW_w    = 100 * 8231718.243 / 10658314.063 = 77.232836 %
check     : 100 * 0.888365 * 0.77232836 = 68.610955   (matches STOCK)
```

The holding weight contributes `1 − 0.888365 ≈ 0.112` of the entry rate (≈ −8.6 pp at this level), and the
window/growth term contributes `77.902046 − 77.232836 = 0.669` pp. **In this illustration the wedge is
overwhelmingly the attrition term** — which is the mechanism the M1-NER object did not contain.

### 11.2 T2 — `SYN28`, `primary`, `t = 1992`, `d = 6` (same rule, no adjustment)

```
survival(1992) = 0.7438980776            s ** (1/6) = 0.9518873881
N = 5 631 462.7033     B = 8 191 060.0660
A terms (1992..1987): 1098325.544, 1083421.249, 1067723.412, 1050308.402, 1029504.781, 1002281.913
C terms (1992..1987): 1397919.669, 1384655.862, 1371517.905, 1358504.604, 1345614.776, 1332847.250

STOCK = 68.751330 %      FLOW = 78.568574 %      DIFF = -9.817244 pp
sigma_bar = 0.889427     FLOW_w = 77.298485 %
```

### 11.3 What the example demonstrates (and does not)

It demonstrates that the object is computable from three named columns and the frozen duration, that the
arithmetic reproduces the §8.2 decomposition exactly, and that the same rule applies to both test types without
adjustment. It does **not** demonstrate a construct-test outcome: 1992 is outside the 85–95 band on both
series, the band test is defined only inside the band, and the crossing test is not evaluated here at all.

### 11.4 Declared sensitivity of the illustration to the weighting shape (declared, not adopted)

For the same T1 row, the alternative schedules of §13.2 give: linear `w_k = 1 − (k/d)(1−s)` → **65.096605**;
endpoint-only (`w_k = 1` for `k < d−1`, `w_{d−1} = s`) → **69.806730**; constant-hazard (the object) →
**68.610955**. The spread (≈4.7 pp) is recorded **only** to show the size of the declared choice. **No
alternative is part of the object, none will be substituted after a result (`PRE_DECLARATIONS.md` §3.7), and
none may be reported as the object.**

---

## 12. What the object would and would not license

### 12.1 If the construct test returned `CONSTRUCT-EQUIVALENT` (future, under a further decision)

**Would license:** the *measure-side* statement that, on the frozen synthetic panel and at the declared bars,
this stock reconstruction and the model's cohort-flow analogue agree within ±2.0 pp in the 85–95 band and at
the 90/95 first-sustained crossings, on both the PHL-like anchor and the high-capacity type — i.e. that the
model's flow object is a defensible stand-in for a stock NER **on the simulator's own interface**.

**Would not license:**

- **Not** an HKG run. Execution still requires a further Council decision and the full HKG gate
  (SR-1…SR-9), plus checklist §2 hash verification (`PRE_DECLARATIONS.md` §8).
- **Not** a validation, a portability claim (R22), an anchor upgrade, a verdict change (D76/D77), a capacity
  claim (D61/R28), a direction or causal claim (R13), or any statement about Hong Kong.
- **Not** a statement that the synthetic object *is* the UIS `NER.1.cp`. It is an analogue built from a
  one-year cohort-flow model that carries no grades, no repeaters, and no stock (§6, §13).

### 12.2 If the construct test returned `BLOCKED-MEASURE` (future, under a further decision)

**Would license:** the terminal, informative statement that the model's cohort-flow NER object **cannot stand in
for a stock NER** under the declared bars — i.e. that the measure gap is too large for a transport of the D75
timing test to be a comparison rather than a measure artefact. The HKG arm would then **close on the measure**
for this phase, and that closure is the honest end state, not a failure to be rescued.

**Would not license:** anything about Hong Kong; any "the model is wrong about HKG" statement; any re-specified
object (N2 is explicit: not re-specified, not run); any moved bar.

### 12.3 Either way

No portability, capacity-timing, phase-verdict, direction, or causal claim. `BLOCKED-*` is terminal and is
never reported as a result, a model failure, or a country finding.

---

## 13. Alternatives considered and deliberately not adopted

Recorded so that the design cannot be reconstructed after a result as "the one that would have passed". **None
of these is part of the object; none will be substituted if the construct test fails.**

### 13.1 `band_population` as the denominator (rejected)

The panel carries `band_population = d × cohort(t)`. It is the model's own column and would be the simplest
denominator. It is **rejected** because it imposes a **stationary population** on a panel whose cohorts grow at
the declared ~2.45 %/yr early back-cast: it divides a backward window of entry cohorts by `d` times the *current* cohort, which
mechanically penalises any growing system and would inflate the measured wedge by a demographic artefact that
has nothing to do with the model's measurement of NER. The adopted denominator `B = Σ_k C(t−k)` is the correct
reconstruction of the official-age band from the same window (the `d` single-year age groups as they exist at
`t`), and it makes the object's two sums refer to the same cohorts — which is what makes §8.1's degenerate
identity exact.

### 13.2 Holding-weight shape: linear, or endpoint-only (rejected as the object; reported only as §11.4)

- **Endpoint-only** (`w_k = 1` for `k < d−1`, `w_{d−1} = s`) is the most literal mirror of
  `sim_v1_2.py:606`, but it implicitly assumes **zero** dropout for `d−1` years and all of it at the exit,
  which is a stronger and less plausible assumption than constant hazard.
- **Linear** (`w_k = 1 − (k/d)(1−s)`) is admissible and differs from constant hazard by a few pp (§11.4).

Constant hazard is adopted because it is the unique schedule with no free shape value between the two fixed
endpoints (§5.3), it treats each grade-year alike (no invented concentration of dropout), and it does not
require a second declared notion of survival. The alternatives are **not** run.

### 13.3 Per-cohort survival history (rejected)

One could weight each cohort by the survival values of the years in which it actually sat in the level. That is
**look-ahead** for the younger cohorts (their completion-year survival is in the future at `t`) and it would
require inventing a cohort-specific survival path the model does not carry. The adopted rule uses the
level-year's **own** `survival` — the only value available at `t` without future information.

### 13.4 Including over-age admissions, or adding a repeater flow (rejected)

Both would move the object toward a GER-like age-agnostic admission stock, which is the substitution D75 (iii)
and `SR-8` bar, and neither has a model object behind it (no repeater state exists). Excluded and declared as a
**downward** bias (`PRE_DECLARATIONS.md` §3.4).

### 13.5 A "ratio of sums only" object with `w_k = 1` (rejected as the object)

It would be parameter-free and closer to the flow, and it would very likely narrow the wedge. It is rejected
because it **discards the model's survival column entirely** — the object would then contain no attrition, and
would be a re-parameterisation of M1-NER's idea rather than a stock reconstruction. N1 names `survival` as one
of the objects the reconstruction is built from; an object that ignores it cannot answer the question the
construct test exists to ask.

---

## 14. Provenance

| item | value |
|---|---|
| object id | `STOCK-NER-D` |
| definition | this file §3.2 = `PRE_DECLARATIONS.md` §3.1 |
| level / duration | primary, `d = 6` (`DVEC`, `generator_v1_2/code/sim_v1_2.py:65`) |
| input panel | `generator_v1_2/results/synthetic_panel_v1_2.csv`, sha256 `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| comparator cross-check panel | `generator_v1_2_addendum/results/synthetic_panel_v1_2_ner.csv`, sha256 `c6d1f9b059b5a48cbd5a4aaf7e1c4611cad781819b74987988897e8d35e40294` |
| test types | `SYN00_PHL_LIKE` (T1), `SYN28` (T2, highest 2020 GDPpc = 48 270.81143) |
| observed inputs | **none** — no observed series is read by the object or by the construct test |
| target years read by the object | **none** (`PRE_DECLARATIONS.md` §3.6; guard G6) |
| status | frozen, unrun; construct test `NOT-RUN-NOT-AUTHORISED` |
| design verdict | `PRE_DECL-FROZEN` |

**In one line:** *the object is the model's entry cohorts carried through the level's declared duration with the
model's own survival and divided by the model's own cohort band — a stock ratio of pupils to persons, computed
from three columns and one frozen constant, never from the target, and construct-tested against the flow on two
test types before any transfer may be attempted.*
