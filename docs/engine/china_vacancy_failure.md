# The China vacancy failure: an explanation, not yet a fix

To-do item B9 (6 November 2026). Done criterion from `docs/TODO_BY_LANE.md`: **the vacancy check passes, or a written
reason why not.** This note records the reason, the three tests that remain, and what a passing model would need. It is a
companion to `firms/results/demand_inversion.md` and `firms/results/stories_strict.md`; all numbers below are already in
those stored results.

## The fact the model misses

Graduate job postings, H1 2025 against H1 2024: **-22%** (Caixin, citing job boards). The model's answer depends on the
specification, and none is close:

| Specification | Modelled postings, H1 2025 y/y | Stored result |
|---|---:|---|
| Two-type model, whole-record fit | +2% | `firms/results/tilly_fit.json` (`vg_2025H1_pct`) |
| Two-type model, strict Dec 2022 information set | +9% | `firms/results/forecast_strict.md` |
| Required-demand inversion (demand solved to match unemployment) | +4% | `firms/results/demand_inversion.md` |
| Story tournament winner, strict Dec 2024 protocol | -89% | `firms/results/stories_strict.md` |

Even the specification that gets closest (-9% in the pre-refit run; -89% after the 6 November refit) does so by accident of compounding mechanisms, not by modelling the vacancy fall.

## Why the structure cannot produce it

In the model, firms post vacancies in proportion to the number of searchers (free entry). More unemployed graduates
therefore means more postings, not fewer: a demand contraction that raises youth unemployment mechanically **raises**
modelled postings. That is the whole failure in one sentence.

The required-demand inversion makes the trade-off explicit. To reproduce 2023-26 youth unemployment, graduate-job demand has
to sit 6% below the 2022 rule in 2023 and about 15% below by 2025-26. On that path the model still gives postings **+4%**
in H1 2025. No single demand series can fit both the unemployment path and the postings collapse, because within this
structure they move in the same direction.

The aggregate-demand escape route is closed. A path that cuts economy-wide demand enough to matter implies, through the
model's own adult free-entry mapping, adult unemployment rising towards 6% by 2026, against an observed overall urban rate
of 5.1-5.2%. The aggregate story is contradicted by the adult labour market.

## The three remaining tests

These are the tests named in `TODO.md` §5. Each is designed to separate "the model's vacancy concept is wrong" from "the
world changed in a way this structure does not have a parameter for".

### 1. Postings coverage versus model vacancies

**Question:** Are job-board postings the same object as the model's vacancies?

**Design:** Compare the CIER graduate vacancy-to-applicant index, MyCOS six-month employment, and platform postings
(Zhaopin/BOSS) on the same half-year window. If platform postings fell 22% while the CIER index and the vacancy-to-applicant
ratio stayed flat or rose, the -22% is a coverage/composition change (a platform shift or a decline in paid postings), not a
fall in the vacancy concept the model uses.

**Data needed:** CIER quarterly index (public summaries), platform postings by quarter, job-board market reports. The
project does not yet hold a postings series other than the single -22% figure; this is the first data gap to close.

**What would count as passing:** the -22% survives re-measurement against an independent vacancy series, so it is a real
demand fall rather than a measurement artefact.

### 2. Time-varying matching efficiency

**Question:** Did matching efficiency fall, so the same vacancies produced fewer hires?

**Design:** Estimate the matching function `hires = A_t · U^α · V^(1-α)` with a time-varying `A_t`, on the urban
unemployment and vacancy series. A fall in `A_t` of about a fifth in 2025 would reconcile -22% postings with a roughly
unchanged unemployment rate. This is a Beveridge-curve shift, and it is exactly the kind of object the model currently
assumes constant.

**What would count as passing:** estimate `A_t` from data, then either fit it as an input (which would make the vacancy
check pass) or document that the estimate is too imprecise to be used.

### 3. A participation / NEET margin

**Question:** If graduates stopped searching, measured postings could fall without vacancies falling in the model's sense.

**Design:** Add a participation margin to `engine/firms/`. Each period a graduate chooses between searching and a
non-search state (exam preparation, waiting, inactivity), with the value of non-search tied to civil-service and
postgraduate-exam calendars and odds. Only searchers count in the unemployment rate and in the model's vacancy-posting
rule. The margin has three observable handles already partly in hand:
- postgraduate-exam applicants fell 4.74m → 3.88m (2023 → 2025, -18%);
- civil-service applicants rose 2.6m → 3.7m;
- MyCOS reports a rising "slow employment" (慢就业) share.

**What would count as passing:** the margin is identified from those series under the strict protocol, and with it the model
reproduces a large postings fall at roughly constant unemployment. This is a structural change (a new state), not a
parameter, and should be tested under the same strict information-set rule as `forecast_strict.py`.

## What a passing model would need

1. **Postings as a demand decision, not a searcher count.** The current free-entry assumption makes postings a function of
   the unemployment pool. A postings equation with its own demand shifter (or a more general matching function with
   endogenous tightness) is required for postings and unemployment to move independently.
2. **A measured vacancy series.** Without a second vacancy observable, any fix is unfalsifiable.
3. **The NEET margin**, so the labour-force denominator is not treated as fixed, and
4. **A time-varying matching efficiency**, which is the simplest object that can make the same unemployment rate coexist
   with a 22% fall in postings.

None of these is implemented. The to-do list classifies B9 as L (several sessions) and `TODO.md` says the L items wait
until the paper is submitted; this note is the written reason the check does not pass today, and the design for when the
work is done. It is not a claim that the model is right about anything else: the other China failures (the strict
out-of-sample loss to naive, 1.09 vs 0.89; the seasonal shape; the wage response) are separately documented in
`firms/results/`.

## Status

- **B9 done criterion met:** failure explained in writing (this note + the two stored results above).
- **Not done:** the model fix. Three tests designed above; no data work started except the series already in
  `engine/firms/data_china.py`.
