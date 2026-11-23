# No-off-switch and alternatives-foreclosure tests, 23 Nov 2026

**Pre-registration.** `PRE_REGISTRATION.md` was committed and pushed as the first commit on
branch `research/policy-foreclosure-2026-11-23` (7ad44d5) **before any analysis code or
result**. This report follows that plan; the two deviations are flagged at the end.

**Bottom line.**
1. **No off-switch is falsified in its strong form, supported in its weak form.** Nine of the
   38 pronatalist introductions in countries already below 1.6 were followed by runs of 3 to
   10 consecutive years above 1.6 — the pre-registered falsifier fires. The longest is
   Bulgaria, above 1.6 every year 2014-2023 and still 1.81 in 2023. But no country came near
   replacement (highest TFR reached after any introduction: 1.83), most crossings reversed,
   and the average post-introduction shift is only +0.035 births (SE 0.025), with the design
   able to detect +0.07. So: policy introductions are not followed by a return toward
   replacement, but the ~1.6 line is not a hard ceiling, especially in post-socialist EU.
2. **Alternatives foreclosure is not supported: a clean null.** The interaction between
   pipeline coverage and farm employment is essentially zero (−0.01 births per 10-point
   increase in each, SE 0.02), survives income and urbanisation rivals as a null, and the
   high-versus-low farm gradient is not beyond a 400-random-split null. Where it is
   non-zero (the stricter sample) it has the *opposite* sign to the prediction,
   −0.32 (SE 0.20) per 10 points. The sample is thin (two decades), so this is "no evidence
   for the gradient", not proof of no gradient.

## Data availability
| variable | source used | coverage | note |
|---|---|---|---|
| TFR | project panel `/root/work/data/fertility.json` (WPP/World Bank) | 217 countries, 1960-2023 | observed series |
| income, urbanisation, farm employment, secondary/tertiary completion | project panel (same directory) | 1990s/2000s onward for completion and farm employment | income stored in levels, logged |
| net migration | World Bank API, pulled on box2 (`SM.POP.NETM`, `SP.POP.TOTL`) | 1960-2023 | used as a rival in the no-off-switch test |
| pronatalist policy dates | hand-coded `data/events.json` (38 introductions, 25 countries) from public national records/OECD conventions | 1994-2021 | dates approximate to the year; **not re-verified online this pass** (budget) — the single biggest data caveat |
| prior-project local files | `/root/work/local_data/10_massification/` | 6-7 case countries | inspected. `POLICY_TIMELINE.csv` has 18 rows of *education* policy for 6 countries and **no pronatalist events**, so it cannot cross-check the event list (no conflict to resolve, but no independent confirmation either). `UNIVERSALIZATION_TIMING/SERIES`, `JOBS_AND_MARKETS_PANEL`, `STATE_CAPACITY` are case-study scale (6-7 countries), so they could not replace the global panel. |
| housing costs | not available | — | stated limitation for the no-off-switch rivals |

## (1) Fertility — the no-off-switch test
**Sample:** 38 documented pronatalist introductions (cash, leave, childcare, population-policy
reversal) in 25 countries, every one with TFR below 1.6 at introduction. TFR panel
1960-2023; post-window 10 years.

**The bound test.** 34 of 396 country-years in the ten years after introduction are above
1.6 = **8.6% (one-sided 95% upper bound 11.3%)**; the pre-registered prediction was "below
10%", so the point estimate passes and the confidence bound does not. Ten of 38 events have
at least one year above 1.6 within ten years, and **five of 38 have 3+ consecutive years
above 1.6 — the pre-registered falsifier fires**: Russia 2007 and 2011 (6 years, max 1.78),
Czechia 2008 (3 years, max 1.71), Estonia 2004 (5 years, max 1.72), Belarus 2007 (5 years,
max 1.73).

**The longer view (beyond the pre-registered 10-year window).** Nine of 38 events ever have
a run of 3+ consecutive years above 1.6 after introduction. The longest:
Bulgaria 2005 introduction — 1.37 at introduction, 10 consecutive years above 1.6 (2014-2023),
still 1.81 in 2023; Romania — 8 years (1.30 to 1.81, back to 1.54 by 2023); Czechia — 7 years
(1.15 to 1.83, back to 1.46); Russia — 6 years (1.42 to 1.78, back to 1.41); Estonia 5,
Belarus 5, Latvia 4. **The highest TFR reached anywhere after an introduction is 1.83**; no
country approached replacement.

**The average effect.** Event study with country and calendar-year fixed effects, first
saturated introduction per country (467 country-years, 25 countries): average
post-introduction TFR shift **+0.035 (SE 0.025; 95% CI −0.014 to +0.083)**. Power: the design
detects +0.070 at 80% power, so it can rule out a sustained *average* recovery larger than
about +0.07 births — it cannot rule out smaller ones, and it cannot speak for individual
countries (see Bulgaria).
**Rivals:** without controls +0.028 (SE 0.028); with the income cycle, urbanisation and net
migration controlled +0.028 (SE 0.028); with country-specific trends +0.017 (SE 0.010). The
small positive shift is not an income/urbanisation/migration artefact.
**Pre/post descriptive:** the maximum TFR in the ten years after an introduction exceeds the
five-year pre-mean by a median of +0.15 births (mean +0.18).
**Thailand (case study, not saturated at the reversal):** TFR 1.84 in 1997 → 1.73 (2000) →
1.56 (2010) → 1.21 (2023); the 1997 policy reversal was followed by continued decline, no
recovery.
**What would refute the weak claim:** a country sustaining TFR near or above 2.1 for a
decade after policy. Nothing close occurs. **What would refute the strong claim (and does):**
a country holding above 1.6 for several years — Bulgaria, Romania, Czechia, Russia, Estonia,
Belarus, Latvia. **Provisional:** the event dates are hand-coded and approximate; Bulgaria's
rise is as likely to reflect delayed births, EU accession income growth and emigration
selection as policy — we test the average, not the attribution.

## (2) Massification — the alternatives-foreclosure test
**Sample:** 10-year-change windows, outcome = change in TFR; coverage = secondary completion
at window start (robustness: tertiary); foreclosure = farm employment share (robustness:
urbanisation, sign reversed); controls income and urbanisation; country and decade fixed
effects; errors clustered by country. Data availability limits this to the **2000 and 2010
decades** (completion and farm-employment series start in the 1990s), giving 237 windows in
153 countries (strict complete-case sample: 175 windows, 127 countries).
**Primary result:** the coverage effect per 10 percentage points is +0.09 births (SE 0.11) and
the pre-registered interaction with farm employment is **−0.01 (SE 0.02; 95% CI −0.06 to
+0.04) per 10 points of each** — a precise-ish zero. The pre-registered sign was positive
(weaker coverage effect where farming survives); observed sign is negative.
**Rivals:** with income and urbanisation controls the interaction is −0.01 (SE 0.03); adding
coverage × income and coverage × urbanisation, the farm interaction stays −0.01 (SE 0.04),
coverage × income is −0.02 (SE 0.07) and coverage × urbanisation +0.00 (SE 0.00). The
masquerade does not arise because there is nothing to masquerade.
**Gradient and random-split null:** the coverage effect in high-farm minus low-farm countries
is −0.08 (SE 0.15) in the expanded sample and −0.32 (SE 0.20) in the strict sample — the
opposite of the predicted positive gradient. Against 400 random splits of the same sizes, the
real gradient sits at the 9.8th percentile of the null (null mean 0.00, sd 0.06): no
detectable gradient.
**Power:** the interaction minimum detectable effect is about 0.06 per 10 points of coverage
and farm share; the gradient MDE is about 0.4 births. With only two decades and modest
within-country variation in completion, a small true gradient would be missed. The honest
statement is **no support for the foreclosure gradient in this sample**, not a demonstrated
absence.
**Falsifiers:** (i) interaction zero or negative — fires (both samples); (ii) interaction
vanishes under income/urbanisation rivals — it starts at zero, so this test is vacuous;
(iii) gradient not beyond the random-split null — fires.

## Deviations from the pre-registration
1. The event list was planned to be cross-checked against OECD Family Database indicators and
   the prior-project `POLICY_TIMELINE.csv`. Neither was possible: `POLICY_TIMELINE.csv`
   contains only education policy for 6 countries, and the OECD indicator API was not pulled
   within budget. The event dates are therefore hand-coded and approximate, as stated above.
2. The foreclosure sample was planned 1960-2023; data availability restricted usable windows
   to 2000 and 2010. This is reported as a limitation, and the expanded/strict samples are
   both shown.
Both deviations are data-availability constraints, not changes to the tests or their
falsifiers.

## Files
- `PRE_REGISTRATION.md` — the frozen pre-registration (commit 7ad44d5).
- `data/events.json` — the 38-event pronatalist list and the Thailand case study.
- `scripts/pf_common.py` — panel builder; `scripts/analysis_a.py` — no-off-switch tests;
  `scripts/analysis_b.py`, `scripts/analysis_b2.py` — foreclosure tests.
- `results/A_results.txt`, `A_event_trajectories.csv`, `A2_longrun.json` — no-off-switch
  estimates, per-event trajectories and the longer-run crossing table.
- `results/B_results.txt`, `B2_results.txt`, `B_windows.csv` — foreclosure estimates.
- `results/net_migration.csv` — the rival series pulled from the World Bank on box2.
- Work ran on box2 in `/root/work/policy_foreclosure` with 2 single-threaded workers.
