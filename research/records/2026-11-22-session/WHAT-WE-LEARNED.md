# What we learned

**Session record, 22–23 November 2026.** A day of work on the Atlas education panel:
massification, fertility, agricultural change, and a set of falsification experiments
run to find out which of the day's findings were real.

The organising rule was simple and it cost us most of the headline results: **a finding
counts only if it survives a test designed to kill it.** Six hypotheses were killed
today. Three survived. The surviving three are narrower and better than what we
started with.

---

## The ledger

### Survived

| Finding | Evidence |
|---|---|
| **Electricity drives the floor of the school pipeline** | Lower-secondary completion **+16.05** within countries; upper-secondary **+0.562** (SE 0.195, P(>0) = 0.99); Bayesian model averaging inclusion probability **1.00**; replicates on child labour at **−0.417** (P(>0) = 0.02), a different survey instrument entirely |
| **Paid employment leads higher education, directionally** | **+1.425** (SE 0.410); reverse **+0.010** (0.042); **zero of 1,200** simulated common-cause panels reached the observed value (common-cause median 0.000, 5–95% −0.260 to +0.255); jackknife positive in **100%** of 203 country drops |
| **Falling input prices move labour** | Fertiliser price ÷ GDP per head, interacted with baseline farm dependence: farm employment **+0.445** (0.082), wage employment **−0.243** (0.096). Boppart's mechanism, confirmed on labour |
| The schooling–fertility link is not luck | 11.97% of the within-country fertility fall explained; **maximum 4.57%** across 20,000 scrambled worlds, **0 of 20,000** reached the observed value; survives 40% measurement error |

### Killed

| Hypothesis | What killed it |
|---|---|
| **Gender parity in tertiary education drives fertility down** | Zero in six groupings, in the lead–lag matrix, and in Bayesian averaging. Likely mechanical: the women:men ratio saturates at high enrolment. Appears never to have been estimated before — so this is a first test, not a failed replication |
| **Three actors must be present together for massification takeoff** | Only **38%** of 39 takeoffs had household means, employer demand and state capacity all present; additive model beats the conjunction out of sample (0.1222 vs 0.1225); state capacity **−0.18** (SE 0.20), i.e. null to negative |
| **Agricultural decline caused the fertility transition** | Direction reversed: farm share → births **+0.0011** (0.0041); births → farm share **+1.536** (0.406). Farm share is the weakest term in a seven-variable horse race |
| **World food prices test the mechanisation story** | Significant everywhere but the **wrong sign**, and the index begins in 1990, after most of the world's farm transition ended. It prices what farms *sell*, not what they *buy* |
| **Fertility crosses a 20% tertiary threshold** | No break at any lag. A straight line across the entire window, consistent with Bongaarts & Watkins (1996): no fixed threshold for entry into transition |
| **Higher education pulls the lower levels up** | **+0.106 → +0.035** once cities enter. Absorbed by the urban-wage bundle, not by infrastructure |
| **Electricity is a proxy for "the bundle"** | Cross-country correlation 0.64–0.88 collapses to **0.39–0.56** within countries; composite index is null or wrong-signed on three of four outcomes; the state-presence bundle correlates **~0.00** within countries (PC1 only 54.2%) |

---

## Seven lessons

### 1. Between-country and within-country are different questions, and the code must say which

The panel's `matrix.csv` compares countries with each other. `tight/` and `final/`
follow each country over time. The same phrase — "X leads Y" — means two different
tests in the two files, and only the second is a sequence claim. Many pooled findings
vanish within countries: primary completion → tertiary, poverty → tertiary, child
mortality → tertiary, urbanisation → tertiary all die. What survives is lower-secondary
completion → tertiary, a shrinking youth share → tertiary, a small wage-employment
lead, and electricity → secondary.

This is not a technicality. It is the difference between "rich healthy countries
differ from poor ones" and "changing this causes that."

### 2. Specification curves are brutal, and they should be run before anything is written

The headline **+1.43** is real at its specification and absent in most others. Across
1,536 defensible specifications: median ≈ **0**, 5–95% range **−0.040 to +1.371**,
significant and positive in **27.9%**.

Two analyst choices do all the work:

- **Lag.** Contemporaneous **+0.39**; five years **+0.19**; **ten years 0.00**; fifteen **+0.02**. An effect that dies by the second decade is not the delayed human-capital chain the theory requires.
- **Transform.** Levels **+0.86**; **logs 0.00**. The association exists between levels, not between proportional changes.

Adding any control beyond the country's own starting level takes the median from
+0.12 to +0.01. The lesson is not that +1.43 is false. It is that a field reporting
one specification reports the top of a distribution whose median is zero.

### 3. A falsification test run at the maximum is not a robustness test

The chain-versus-common-cause simulation is the best single method we found — it
distinguishes "shared trend" from "lead–lag" without needing exogenous variation,
because under a common driver the country's own starting level already absorbs the
factor and the partial coefficient goes to zero. Zero of 1,200 common-cause panels
reached the observed value.

But we ran it at the specification where the coefficient is largest. It establishes
**direction at a specification**, not stability across specifications. Both results
belong on the same page, and the paper now says so.

### 4. "Development" is not an explanation, and collinearity is not a nuisance

Electricity, cities and paid employment correlate at **r = 0.69–0.80**. Entering them
together does not identify which is causal; it distributes one bundle of variation
across three labels, and the answer depends on entry order. Cities absorbs the
tertiary→secondary edge (+0.106 → +0.035); electricity barely touches it (+0.102).

The honest statement is that they are one historical package the panel cannot prise
apart — and that what a paper can do is show the package is **upstream of schooling**,
not downstream. Paid employment leads higher education (+1.43); higher education does
not lead paid employment (+0.01).

### 5. Cross-country correlation is not co-movement

A bundle looks like one factor across countries and dissolves within them:

| bundle | components | PC1, across countries | correlation **within** countries |
|---|---|---|---|
| household utilities | electricity, water, sanitation, internet | **83.7%** | **0.39–0.56** |
| state presence | electricity, hospital beds, physicians, security | **54.2%** | **~0.00** (beds–physicians **−0.14**) |

Rich countries have all of it; poor countries have none of it. But building is
**sequential**: a country puts up the grid before it lays the sewers, and can
electrify without ever building hospitals. Consequently a composite index is worse
than its best component — the utilities bundle is null or wrong-signed on three of
four outcomes, and the state-presence bundle is null everywhere while electricity
alone returns **+9.60** on lower-secondary completion and **−12.38** on extreme
poverty.

**State presence is a portfolio, not a bundle.** Each capacity moves its own outcome:
electricity the floor and poverty, physicians tertiary enrolment (+10.94).

### 6. The agricultural chain has four links and it breaks at the third

| link | estimate | verdict |
|---|---|---|
| Input prices → farm exit | **+0.445** (0.082) | confirmed |
| Farm exit → wage employment | **−0.243** (0.096) | confirmed |
| Input prices → births | **−0.006** (0.010) | **not confirmed** |
| Fertility → farm exit | **+1.536** (0.406) | confirmed |

The mechanisation shock is real and it moves labour in the direction Boppart et al.
(2023) predict. It stops at the labour market. Farm exit has two drivers — the
falling price of modern inputs and the falling number of births — and fertility
responds to neither.

The reason the earlier output-price test failed is instructive: **it priced the wrong
margin.** Output price acts on the extensive margin (is farming worth doing), input
price on the intensive margin (how much capital per worker). Mechanisation is an
intensive-margin phenomenon, so a test built on grain prices measures distress and
concludes the mechanism is absent.

### 7. Check data availability before designing the test

Half the evening's design work died on missing series:

| what we wanted | what exists |
|---|---|
| Police personnel ("cops") | **Nothing in WDI.** Approximated by inverse homicide — an outcome, not an establishment |
| School counts | **No count series in WDI.** Quality and policy indices exist; institutions don't |
| Paved roads | 602 rows, 58 entities, **1990–2010 only** |
| Multidimensional poverty | **Not in WDI.** OPHI's files are not at a stable URL, the HDR API needs a key |
| Singulate mean age at marriage | **Not in WDI.** Nearest is % of women married by 18 |
| Economic complexity | Present, but the threshold-crossing year is **1969 for eight of ten countries** — the series never moves. Unusable as an employer-demand measure |
| Female labour participation | Counts family-farm work: Nigeria at 75% with 4.7 children. Not an outside-option measure |

---

## What the day actually established

A chain we can defend, with the break located precisely:

> **Falling input prices → farms empty → wage employment grows → credentials acquire
> a cash payoff → higher education expands. And then nothing: fertility does not
> respond, and the credential's expansion outruns the learning it certifies.**

Four of five links hold. The one that fails is the demographic one, and it fails by a
wide margin on 8,419 country-years.

Alongside it, a structural claim worth more than the chain: **the school system has
two regimes.** Infrastructure governs the floor — electricity is decisive for primary
and lower-secondary completion and for poverty, and null for tertiary. The wage economy
governs the apex — paid employment is decisive for tertiary and null for the floor.
Neither substitutes for the other, and neither is a proxy for a single quantity called
"state capacity" or "development."

---

## Methods that earned their keep

1. **Luck test by series-scrambling.** Time-shift each country's predictor, keep
   everything else, and see how often chance reproduces the result. 0 of 20,000.
2. **Common-cause simulation on the real coverage mask.** Separates shared trend from
   lead–lag where exogenous variation does not exist.
3. **Specification curve with a full choice panel.** 1,536 specifications; the answer
   is the distribution, not the point.
4. **Jackknife by country.** Cheap, and it tells you whether one observation carries
   the result. (It didn't: 100% positive, +0.83 to +1.22.)
5. **Direction tests.** Regress both ways and compare predictive content. The farm
   result was decided entirely by this.
6. **Multiple imputation with calibrated noise.** Interpolation error estimated
   leave-one-out from dense series — water 0.10, sanitation 0.14, electricity 1.66,
   internet 1.91 — then 20 imputations pooled by Rubin's rules. Nothing changed,
   which is itself the useful finding: the results are not a coverage artefact.
7. **Shift-share for global prices.** A world price has no cross-country variation and
   is absorbed by year effects; interacting it with baseline exposure is the only way
   to identify anything.

---

## What to do next

1. **Run the specification curve on electricity → lower-secondary (+16.05).** It is
   the same shape of claim as the one that collapsed today and it has never been
   tested the same way. One script change.
2. **Run the curve on the input-price test.** The employment coefficients are large
   enough to survive; the fertility null deserves the same standard as the other nulls.
3. **Build the real state-presence bundle** with UNODC police personnel and a
   school-count register. Two of the five components are currently unmeasurable and
   that is the binding constraint, not the analysis.
4. **Get the OPHI multidimensional poverty file.** The MPI contains water, sanitation
   and electricity as components, which risks circularity against an infrastructure
   predictor — it needs its deprivation sub-indices separated before use.
5. **Test the two-regime claim against the alternative** that it is an artefact of
   measurement scale. Electricity is near-universal where tertiary is high, so the null
   at the apex could be a ceiling. That has not been ruled out.

---

## The one-sentence version

**Massification runs on the wage economy and the floor runs on electricity; the two
regimes do not substitute; the agricultural mechanisation shock moves labour and stops
at fertility; and most of the headline numbers from a single specification do not
survive the 1,536 alternatives.**

Everything above is reproducible from the scripts in this folder against the series in
`data/`. `STATUS.md` grades every individual result as solid, fragile, null, or do-not-cite.
