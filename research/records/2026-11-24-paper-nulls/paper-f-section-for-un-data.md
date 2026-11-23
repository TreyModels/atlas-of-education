# Paper F section (for un-data): care work, policy bounds, and tipping points

*Draft for the consolidated Fertility paper. 1,650 words. Every number carries its record path
(branch @ commit → file → field); full map in `SOURCE_MAP.md`. Pre-registrations were the first
commit on each record branch. Not softened: the verdict table is the point.*

## 1. Three questions the framework makes falsifiable

The morphological-governance framework treats fertility decline as a by-product of a credential
pipeline. Three predictions follow that are sharp enough to kill.

**Q1, the care-work loop.** Fertility decline should be amplified by paid care work: a rising care
share of female employment lowers fertility further, and the schooling–fertility link should steepen
where care work is common.

**Q2, no off-switch.** Pipeline-compatible pronatalist policy — cash, leave, childcare subsidies —
should not restore *sustained* fertility above roughly 1.6. The mechanism, not the budget, sets the
ceiling.

**Q3, terminal enclosure as a tipping point.** Before the enclosure, fertility should show the
textbook early-warning signature (rising variance, rising lag-one autocorrelation); after it, the
schooling–fertility link should ratchet — diminishing returns.

## 2. Data and design

*Care loop:* ILO sectoral employment (education, health/social work) for 656 country-years, 148
countries, 2010–2023, merged with World Bank fertility, female tertiary attainment, log GDP and
urbanisation. The outcome tests use 140–141 countries. [care-credential @ e626cb8 →
`PREREGISTRATION.md`, `scripts/build_care_cred.py`, `results/results_care_cred.json`]

*Policy bound:* 38 hand-coded pronatalist introductions (cash, leave, childcare, reversal) in 25
countries, each with fertility below 1.6 in the introduction year, on the 1960–2023 country-year
panel (217 countries). [policy-foreclosure @ 63691a2 → `data/events.json`,
`results/A_results.txt`, `results/A2_longrun.json`]

*Tipping point:* the pre-registered event rule (first year of the fastest sustained ten-year fall of
at least 1.0 birth) gives 184 transition events; 80 have the full 15-year pre-event window. Each is
compared with 200 pseudo-event dates from its own series (never within ten years of the real
event). Surrogate null: first differences reshuffled and re-integrated 16,000 times. [early-warning
@ 7e64f61 → `results/ews_results.json`]

## 3. Q1 — the care-work loop: income and urbanisation do the work

The raw gradient is exactly what the framework wants: mean care share of female employment is
**8.1% in the bottom attainment tercile, 19.0% in the middle, 28.4% at the top** (n = 47 each, 148
countries; care share overall 18.3%, sd 12.1, range 1.2–52.1). [results_care_cred.json, A1 terciles]

It disappears with controls. With log GDP per head in the model the attainment coefficient is
**+0.009 (t = +0.17, n = 140)**, log GDP **+0.242 (t = 2.47)**, and with urbanisation added urban
**+0.42 (t = 3.38)**. The pre-registered "fully explained by income/urbanisation" falsifier fires.
[results_care_cred.json, A1 controls]

The amplification test flips sign: interaction of attainment with care share **−0.131 (t = −1.38,
n = 141)** without controls, **+0.128 (t = +1.53)** with GDP and urbanisation. Unstable, so failed.
[A3]

The placebos are decisive. Replacing women's care work with **men's** care work gives **+0.179
(t = 2.10)**; replacing it with **manufacturing** gives **−0.189 (t = −3.47)** — the unrelated-sector
placebo produces a larger "effect" in the predicted direction than care work itself. [A3 placebos]

The dynamic test has the wrong sign: across 119 country pairs, fertility change on the early care
share is **+0.199 (t = 2.14)** without controls (higher care share, *less* decline) and **−0.045
(t = −0.41)** with log GDP. [A2] Across 36 pre-registered specifications the care coefficient takes
both signs, about −0.57 to +0.27, and significance tracks the fixed effects, not the care measure.
[spec curve]

**Verdict: null.** Not that care work is irrelevant — the gradient is real — but the framework's
care loop is not separable from income and urbanisation, and its placebos behave like the treatment.

## 4. Q2 — no off-switch: strong form falsified, weak form supported

Bound test: **34 of 396 post-introduction country-years above 1.6 = 8.6%** (one-sided 95% upper
bound **11.3%**). The pre-registered prediction was below 10%: the point estimate passes, the
confidence bound does not. Ten of 38 events cross above 1.6 within ten years. [A_results.txt,
BOUND TEST]

The persistence falsifier fires. **Five of 38** events have 3+ consecutive years above 1.6 within
ten years: Russia 2007/2011 (6 years, max 1.78), Czechia 2008 (3, max 1.71), Estonia 2004 (5, max
1.72), Belarus 2007 (5, max 1.73). Beyond the pre-registered window, **9 of 38** events ever have
such a run: **Bulgaria 10 consecutive years 2014–2023, still 1.81 in 2023**; Romania 8, Czechia 7,
Russia 6, Estonia 5, Belarus 5, Latvia 4. The highest fertility reached after any introduction is
**1.83**, and most crossings reverse. [A_results.txt; A2_longrun.json]

The average effect is small and not an artefact: event study with country and calendar-year fixed
effects, first saturated introduction per country, **+0.035 (SE 0.025; 95% CI −0.014 to +0.083)** on
467 country-years and 25 countries. Power: the minimum detectable effect is **+0.070** at 80% power.
Rivals leave it: **+0.028 (SE 0.028)** without controls; **+0.028 (SE 0.028)** with income,
urbanisation and net migration; **+0.017 (SE 0.010)** with country-specific trends. [A_results.txt,
EVENT STUDY / POWER / RIVALS]

Descriptive: the maximum fertility in the ten years after an introduction exceeds the five-year
pre-mean by a median **+0.15 births** (mean +0.18). Thailand's 1997 reversal (outside the saturated
set) was followed by 1.84 → 1.73 (2000) → 1.56 (2010) → **1.21** (2023). [A_results.txt, PRE/POST and
THAILAND]

**Verdict: the strong form is falsified; the weak form is supported.** Sustained fertility above
~1.6 is not impossible — nine introductions were followed by multi-year runs above it, Bulgaria for
a decade — but no country returned toward replacement (ceiling 1.83), the average effect is +0.035,
and most crossings reverse. This is not "policies don't work"; it is a claim about how far and how
long they work.

## 5. Q3 — tipping point: no early-warning signature; diminishing returns confounded by a floor

Autocorrelation **falls** before the transition: **−0.025 (SE 0.008, t = −3.3)** event minus
pseudo-event — the opposite of the predicted rising signature. Variance rises **+0.079 (SE 0.034,
t = +2.3)**, the right sign, but fails the pre-registered surrogate null (share **0.42** of 16,000
surrogates at least as large; autocorrelation 0.57). Minimum detectable differences: **0.095**
(variance) and **0.021** (autocorrelation); the variance effect is below its own MDE, so that null
is weak, while the autocorrelation null is not weak because the sign is wrong. [ews_results.json]

Diminishing returns are real but observationally equivalent to a floor: 3,865 country-years, 238
countries, ten-year fertility change on lower-secondary completion and its square gives a positive
squared term **+0.00019 (t = 18.2)**, marginal effects **−0.0099** at the 10th percentile
(bootstrap CI −0.0116 to −0.0079), **+0.0064** at the median (0.0059 to 0.0070), **+0.0214** at the
90th (0.0199 to 0.0230), turning point ≈ 39 of 100. A concave response and a floor look the same in
this regression; the result is quoted as a boundary condition, not a ratchet. [ews_results.json,
diminishing]

**Verdict: no tipping-point signature.** Whatever enclosure the theory describes is not announced by
classic early warning in national fertility series.

## 6. Verdict table (the paper's value)

| # | prediction | pre-registered killing test | outcome | verdict |
|---|---|---|---|---|
| 1 | care-work loop amplifies schooling–fertility link | income/urbanisation absorption; placebo sectors | absorbed: +0.009 (t 0.17) with GDP (t 2.47) and urban (t 3.38); placebos male +0.179 (t 2.10), manufacturing −0.189 (t −3.47); 36-spec curve both signs | **null** |
| 2 | strong no-off-switch: no sustained fertility above ~1.6 | bound test; persistence; event study; rivals | 8.6% of post-introduction years above 1.6 (upper 11.3%); persistence fires 5/38 within 10y, 9/38 long-run (Bulgaria 10 years, 1.81 in 2023); +0.035 (SE 0.025), MDE 0.070; rivals +0.028 (0.028), trends +0.017 (0.010); ceiling 1.83 | **strong form falsified; weak form supported** |
| 3 | enclosure is a critical transition with early warning | event vs pseudo-event; surrogate null; power | autocorrelation −0.025 (SE 0.008), wrong sign; variance +0.079 (SE 0.034) fails surrogate 0.42; diminishing returns +0.00019 (t 18.2) floor-confounded | **no tipping point; diminishing returns a boundary condition** |

## 7. New vs replicated, and what this does not test

**New:** the placebo-based falsification of the care loop; the explicit pre-registered 1.6 bound
and its persistence test (the strong form's falsification); the paired pseudo-event early-warning
test in 80 national fertility series. **Replicated:** the care-share gradient and the post-socialist
recovery patterns (Frejka & Sobotka 2008; Zakharov 2008; Koytcheva & Philippov 2008), the small
bounded policy effects (Gauthier 2007; Thévenon 2011; Thévenon & Gauthier 2011; Luci-Greulich &
Thévenon 2013), and the skeptical side of the early-warning literature (Hastings & Wysham 2010;
Ditlevsen & Johnsen 2010; Kéfi et al. 2013; Boettiger et al. 2013; Dakos et al. 2015).

This section does not test the framework as a whole. Nulls on three mechanisms are informative
about those mechanisms, not about the broad claim that credential pipelines shape fertility. The
plain attainment channel survives (tertiary attainment correlates −0.62 with fertility in the
companion paper), and the weak no-off-switch form survives; those are what the data support. Five
to eight closest prior works per claim, with DOIs and Crossref status, are in
`paper-f-claims-prior-art.md`.
