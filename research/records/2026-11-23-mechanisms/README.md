# Why fertility tracks child survival and life expectancy: literature, what we can test, and a pre-registered experiment plan

Worker `un-data`, branch `research/mechanisms-2026-11-23`, 23 Nov 2026. Design and literature only — nothing was run.
**Server note:** box1 (`ssh autodl`) is retired as of 23 Nov 2026; every reference to "the server" in this record and its
companions means **box2** (`ssh autodl2`), where the panel is at `/root/work/data` (migrated copy also at
`/root/autodl-tmp/migrated/`).
Companion files: `LITERATURE.md` (fuller map with verification status and URLs) and `EXPERIMENTS.md` (full specs).

**Short answer.** The two links are real in our data and big, but country-level data cannot tell the rival explanations
apart, because replacement, insurance against child death, quantity-quality/human capital, life-history, birth-timing and
a common development cause all predict the same two signs. The one mechanism we can separate with data already on the
server is **level versus volatility** of child mortality. Everything else needs household birth histories (DHS/WFS) or
exogenous mortality shocks. I propose seven pre-registered experiments and would run the level-versus-volatility test
first because it is nearly free; the highest-value study is the DHS replacement-versus-insurance design.

## What we are explaining: the numbers from this session's matrix (income logged)

| link, plain words | effect with country trends | standard error | rows / countries | BH q |
|---|---|---|---|---|
| higher child mortality → more births per woman | +0.0060 births per point of child mortality | 0.0011 | 8,567 / 193 | 1.7e-5 |
| longer life expectancy → fewer births per woman | −0.0475 births per year of life expectancy | 0.0078 | 9,266 / 210 | <0.001 |

Both are about twice the minimum effect the design can detect (1.9× and 2.2× the 80%-power/95% threshold), and the
400-grouping multiverse (reported by that job) finds them in about 95% and 81% of groupings — the only fertility links
robust everywhere. Two honest qualifications: (i) they are not independent evidence, because child mortality is a
mechanical component of life expectancy (in the same matrix, higher child mortality predicts shorter life expectancy,
−0.026 ± 0.009); (ii) the dashboard reports that fertility also *leads* child mortality/life expectancy, but our
380-link matrix does **not** reproduce that: fertility → child mortality is −0.83 ± 1.84 and fertility → life expectancy
is −0.11 ± 0.23 (both null). That discrepancy is flagged, not papered over.

## (1) Fertility

**The rivals, and what each predicts.** All of them produce "high child mortality → high fertility" and "long life
expectancy → low fertility", so the signs do not discriminate.

- **Replacement** (Preston 1978; the child-survival hypothesis, Population Studies 1976): parents want a number of
  *surviving* children, so they replace a death. Signature: a birth follows a child death, sooner at higher parity.
- **Insurance / hoarding** (Pörtner 2001): parents hold extra births *against the risk* of loss. Signature: more births
  *before* any death where risk is high, and a weaker response to realised deaths; a response to mortality
  *volatility* as well as its level.
- **Uncertainty / precautionary demand** (Doepke 2005 argues the bare Barro-Becker model fits the facts poorly unless
  uncertainty is added): the same sign, but the driver is risk, not the level.
- **Quantity-quality / human capital** (Becker-Lewis 1973; Becker-Barro 1988; Galor-Weil 2000; Soares 2005;
  Kalemli-Ozcan): fewer survivors raise the return to investing in each child; longer life extends the return horizon.
  Signature: the mortality-fertility link should be **weaker where schooling pays more**, and longer life should raise
  education before fertility falls.
- **Life-history / evolutionary** (Promislow & Harvey 1990; the recent two-tier extrinsic-mortality literature): high
  avoidable mortality favours early and fast reproduction. Signature: earlier first birth and shorter spacing, even at
  the same completed family size.
- **Tempo vs quantum** (Bongaarts & Feeney 1998; Davis 1963 multiphasic response): longer life may change *when* births
  happen, not how many. Signature: the association lives in ages, not in completed family size.
- **Common cause** (Cleland 2001 is the key reassessment; public-health/state-capacity work): both mortality and
  fertility respond to development, public health or state capacity. This is the rival that, if true, invalidates the
  whole family as a causal explanation.

**Contested ground.** The size of replacement (large in the classic comparative work, modest in modern micro work); the
level-versus-volatility decomposition (theory says risk matters, clean aggregate tests are rare); the size and
importance of quantity-quality effects; the mortality → tempo link (essentially untested); and the common-cause rival,
which the literature has not settled.

**Which are observationally equivalent with country panels — plainly.** At country level, **replacement, insurance,
quantity-quality, life-history, tempo and common cause are all indistinguishable**, because each predicts the same two
signs and each operates through the same aggregate change-in-births moment. Our matrix cannot choose between them, and
I make no claim that it does. What *is* separable at country level: (a) **level versus volatility** of child mortality,
because they are distinct regressors that can be entered jointly; (b) **tempo versus quantum**, but only with
age-specific fertility data we do not yet hold; (c) **quantity-quality interaction**, weakly, by testing whether the
link differs where schooling returns differ; (d) **common cause**, only with exogenous mortality shocks or
health-technology instruments; (e) **reverse causation**, which our null reverse-direction links argue against (but do
not rule out).

**What would falsify the whole family (pre-registered).** The family dies if, jointly: fertility responds to neither the
level nor the volatility of child mortality; there is no household replacement response in DHS birth histories;
exogenous mortality-reducing campaigns move mortality but not fertility; and the country association collapses when
state capacity or health-technology instruments are used. Any one is diagnostic; all four together would mean the
association is a development artefact.

## (2) Massification

The mortality/longevity findings **do** touch the schooling story, and this is the uncomfortable part: in the
380-link matrix the survival links dominate schooling as country-level predictors of births (schooling → fertility is
null with country trends, −0.0015 ± 0.0016), so if the survival mechanism family is real, schooling is not the driver
of the fertility transition but at most a co-traveller or a channel. The quantity-quality mechanism is the one place
where the two stories meet: it predicts that the mortality-fertility link should be **weaker where the return to
schooling is high**, which is testable with a returns-to-education interaction (E5) — but our power calculation says
that test is underpowered in the current panel. The UN marriage series are already tested and do not rescue the
missing mediator: no marriage-timing link survives the matrix's falsifiers at country level.

## What our existing assets can and cannot do

- **272/380-link matrix** (country and decade effects, income logged, urbanisation, with and without country trends):
  good at establishing the two associations and their robustness across groupings; **cannot** identify mechanism. It
  is a levels-vs-change design with no household variation and no exogenous instrument.
- **Gap-filled panel**: adds coverage but no new identification; imputation can manufacture links (the imputed-matrix
  job warned about this), so mechanism tests must use the observed arm.
- **Individual-level dose model**: can decompose tempo and quantum and can host survival/longevity channels, but its
  weights are being fixed and must not be leaned on; on country data alone it is under-identified.
- **UN marriage series**: useful for ruling marriage timing out as the missing mediator (it does not survive the
  falsifiers), not for identifying a survival mechanism.
- **400-grouping multiverse**: shows the two links are not group-specific, which is reassuring for generality but says
  nothing about mechanism.

## Part 3 — Pre-registered plan (details and identifying assumptions in `EXPERIMENTS.md`)

| # | Experiment | Estimand (plain words) | Falsifier | Power / MDE | Data gap |
|---|---|---|---|---|---|
| 1 | Level vs volatility of child mortality | extra births from a higher mortality level vs higher volatility | volatility large and level collapses → uncertainty wins; volatility zero → uncertainty dead | 0.003 (level); 0.005-0.006 (volatility) | **none — data in hand** |
| 2 | Replacement vs insurance (DHS/WFS birth histories) | change in next-birth probability after a child death, in points | no household response → aggregate link is not replacement | ≈3 points (10% relative) | **need DHS microdata** |
| 3 | Tempo vs quantum (age-specific fertility) | effect of one more year of life on completed births vs on mean age at birth | all tempo, no quantum → restate the link as timing | 0.02 births; 0.05 years | need UN WPP age-specific tables |
| 4 | Mortality shocks as natural experiments (campaigns, epidemics, famines, conflict) | effect of an exogenous mortality fall on births | strong first stage, no fertility response → replacement/common-cause | 0.06-0.14 births (underpowered for 10-point falls) | need campaign rollout + coverage data |
| 5 | Quantity-quality interaction (education returns) | difference in the mortality link across education-return strata | no difference → human-capital channel not modulating | 0.006-0.007 (underpowered) | need returns-to-education data |
| 6 | Extend the dose model with survival/longevity channels | model-implied response vs country coefficient | model needs a replacement or tempo response outside E2/E3 findings | identification, not sampling: needs 3+ moments | need E2/E3 moments as calibration targets |
| 7 | Common cause / state capacity | mortality link with state-capacity controls and technology-diffusion instruments | coefficient collapses → development artefact | 0.008-0.010 (collinearity) | need vaccination, health spending, governance data |

**Run first: E1 (level vs volatility).** It costs almost nothing (annual child-mortality and fertility series are
already on box2 at `/root/work/data`), its estimand and falsifier can be frozen before touching the data, and the answer decides how
E2 must be designed. If volatility matters, the insurance mechanism becomes the leading explanation and E2 must model
the risk margin explicitly; if it does not, E2 becomes the single highest-value study and should start immediately.
E4 is the most convincing test in principle but needs new data and is likely underpowered at country level; E6 should
wait for E2/E3, otherwise it is fitting four mechanisms to one moment.

## Files and verification

`LITERATURE.md` — annotated map, every source marked `[verified]` (title/record and URL returned this session) or
`[unverified details]` (bibliographic details not captured); no source is asserted without a record. `EXPERIMENTS.md`
— full specs with identifying assumptions and failure modes. No server compute was used; no data were downloaded.
