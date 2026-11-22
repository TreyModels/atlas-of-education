# Session record, 22 November 2026 — massification, fertility, and what survived testing

**Status: record, not a paper.** One day of work on the panel, the farm–fertility
question, and a set of falsification experiments. Every number below is reproduced
by a script in `scripts/` against series in `data/`.

The rule this session followed: **a result counts only if it survived a test
designed to kill it.** Six did not.

---

## 1. What survived

### 1.1 Wage employment leads higher education (the strongest result)

Paid employment (share of jobs that are wage work) predicts the 10-year growth in
tertiary enrolment: **+1.43 (±0.41)** per point, with country fixed effects, decade
effects, and the country's own starting enrolment controlled. The reverse —
higher education predicting paid employment — is **+0.01 (±0.04)**.

This was then tested against a simulated world in which one latent modernisation
factor drives both series with no chain (`exp1b.py`, 1,200 panels per world):

| | paid jobs → higher ed | higher ed → paid jobs |
|---|---|---|
| **Observed** | **+1.425 (±0.410)** | +0.010 (±0.042) |
| Chain world | +2.201 [+1.54, +2.89] | −0.053 |
| Common-cause world | **+0.000 [−0.26, +0.26]** | −0.001 |

**Zero of 1,200 common-cause panels reached the observed value.** Under a common
driver, the country's own level of higher education already absorbs the factor, so
the partial coefficient goes to zero. A positive partial coefficient is the
signature of a lead–lag relation, not a shared trend.

*Caveat.* This can separate "chain" from "symmetric common cause". It cannot
separate a direct effect from a two-step one, and the observed value sits at the
bottom of the chain distribution, implying a weaker chain than simulated.

### 1.2 Early marriage slows the growth of lower-secondary completion

Adding early marriage (`SP.M18.2024.FE.ZS`, women married by 18) moves the
lower-secondary coefficient from −0.094 to **−0.116 (±0.044)** and it stays
significant on 1,130 observations across 113 countries. This is the only
transmission variable that got stronger under its own control.

### 1.3 Electricity drives the bottom of the pipeline, not the top

- Lower-secondary completion: +16.05 within countries; model-averaging posterior
  inclusion **1.00**.
- Upper-secondary: +0.56 (±0.19), P(>0) = 0.99.
- **Tertiary: +0.19 (±0.45) — nothing**, and inside the common-cause noise band.

So the grid gets children through school and does not get them into university.
The apex is driven by the wage economy; the floor by infrastructure.

### 1.4 The schooling–fertility link is not luck

Across 20,000 simulated worlds in which the education series was time-shifted
within each country (destroying the link, keeping everything else):

- observed: **11.97%** of the within-country fall in births explained
- no-link worlds: median 0.17%, 99th percentile 2.19%, **maximum 4.57%**
- worlds reaching the observed value: **0 of 20,000**

The finding survives measurement error up to roughly 40% (20% noise → 9.1%,
40% → 5.3%, 60% → 3.1%).

---

## 2. What failed

### 2.1 "Higher education pushes the lower levels" — collapsed

The one-way edge from tertiary to primary completion (+0.82 in tight-gate
countries) does not survive controls:

| Controls | Effect on upper-secondary |
|---|---|
| none | +0.106 |
| + electricity | +0.102 |
| **+ cities** | **+0.035** (not significant) |
| + paid jobs | +0.049 |
| all three | +0.066 |

**Cities does the absorbing, not electricity.** The three candidate controls are
collinear at r = 0.69–0.80 (electricity–cities 0.69, electricity–paid jobs 0.80,
cities–paid jobs 0.74), so no entry order can crown one. The honest statement is
that they are one historical package and the panel cannot prise them apart.

### 2.2 Farm decline did not drive the fertility fall

Farm employment share does **not** predict the 10-year change in births:
+0.0013 (±0.0041) with income, and the coefficient wanders across zero as controls
enter. The direction test is decisive:

| | |
|---|---|
| farm share → births | +0.0011 (±0.0041) — nothing |
| **births → farm share** | **+1.54 (±0.41)** — real |

**Fertility leads; farming follows.** In a seven-variable horse race the farm share
is the weakest term (−0.0035, ns) while child survival (+0.0067) and the country's
own prior fertility dominate.

### 2.3 World food prices × farm dependence — wrong sign, wrong window

Using the FAO Food Price Index (Jan 1990 onward), interacted with baseline farm
dependence:

| Outcome | farm share × price change |
|---|---|
| farm employment share | −0.668 (±0.072) |
| paid employment | −0.712 (±0.110) |
| births per woman | −0.733 (±0.045) |

Significant everywhere, but the sign means **rising** prices accelerate farm exit
and fertility decline — a crisis story, not the import-competition story. And the
index begins in 1990, by which time most of the world's farm transition was over.

### 2.4 Gender parity in tertiary education — nothing, everywhere

Zero in every specification, every grouping, every test. Consistent with the
literature, in which the claim was asserted (Van Bavel 2012; McDonald 2000) and
never estimated. Likely because the women:men tertiary ratio is mechanically
saturated once enrolment is high.

### 2.5 The three-condition takeoff conjunction — fails

56 countries, 39 takeoffs: only **38%** had household means, employer demand and
state capacity all present; the additive model beats the joint model out of sample
(0.1222 vs 0.1225); state capacity is null to negative (−0.18, SE 0.20).

### 2.6 The transition has no 20% fertility threshold

Event study on the year fertility first drops below 2.1: a straight line across the
whole window, no break at 15 or 20 years. Consistent with Bongaarts & Watkins
(1996): "no fixed threshold for entry into transition."

---

## 3. Known data defects found this session

| Series | Problem |
|---|---|
| `ter` (economic complexity proxy, ECI) | Crossing year is **1969 for eight of ten** countries — the series never moves. Unusable as an employer-demand measure. |
| Singulate mean age at marriage | **Not in WDI.** Nearest is % married by 18. |
| Paved roads `IS.ROD.PAVE.ZS` | 602 rows, 47 usable countries, 1990–2010 only. Cannot carry weight. |
| FAO Food Price Index | Begins Jan 1990 — too late for the farm transition. |
| `sl.emp.work.zs` | Share of *all* employment that is waged; not formal-sector size. |
| `flfp` | Counts family-farm work; Nigeria at 75% with 4.7 children. Not an outside-option measure. |
| Country clusters | Separation scores 0.21–0.26. These are cuts through a continuum, not natural types. |

---

## 4. Data-driven country groupings

Two cuts, both data-driven. **By level** (194 countries, k=3, separation 0.26):
rich / middle / poor, cutting clean across World Bank regions (East Asia splits
4/19/7; Europe 25/25/0; Latin America 3/34/1).

**By trajectory** (69 countries with 1990 and 2020 observed, k=5, separation 0.21):

- **Stalled basics, expanding universities** (19): Albania, Armenia, Belarus, Cuba,
  Egypt, Georgia, Grenada, Jamaica, Kazakhstan, Kyrgyzstan, Sri Lanka, Macedonia,
  Mongolia, **Philippines**, Russia, Syria, Tajikistan, Tonga, Ukraine.
- **Middle-income fast massifiers** (19): Botswana, Dominican Republic, Algeria,
  Fiji, Honduras, Indonesia, Iran, Jordan, St Lucia, Morocco, Mauritius, Namibia,
  Oman, Peru, El Salvador, Suriname, Tunisia, Turkey, South Africa.
- **Late massifiers** (25): Burundi, Benin, Burkina Faso, Côte d'Ivoire, Cameroon,
  DRC, Comoros, Ethiopia, Ghana, Guinea, Gambia, India, Laos, Lesotho, Madagascar,
  Mali, Mozambique, Mauritania, Malawi, Niger, Nepal, Rwanda, Senegal, Chad, Togo.

The Philippines and Cambodia are in the same World Bank region and opposite types.
Ukraine, Albania, Cuba and the Philippines share a type across four regions.

---

## 5. Scripts

| File | What it does |
|---|---|
| `exp1b.py` | chain vs common cause, 1,200 panels per world — the falsification that validated 1.1 |
| `exp2_battery.py` | every candidate driver vs a pure common-cause noise band |
| `battery.py` | what tracks the fall in births; luck and noise tests |
| `replacement.py` | what countries shared 20/10/5 years before dropping below 2.1 |
| `cluster_countries.py` | k-means groupings on levels |
| `five_groupings.py` | five theory-driven groupings, with within-group estimates |
| `group_matrices3.py` | lead–lag matrices inside each grouping |
| `roads_marriage.py` | progressive controls incl. roads and early marriage |
| `decompose.py` | which of electricity/cities/paid jobs absorbs the tertiary edge |
| `farms.py` | farm share vs fertility, direction test, horse race |
| `foodprice.py` | FAO price index × farm dependence |
| `massification_analysis.py` | standalone bundle version (numpy, no other dependencies) |

## 6. Reproducing

Every script runs against `data/`, which holds the World Bank series as
`[iso3, year, value]` triples, plus `meta.json` with regions. Runtime on a 96-core
box: `exp2_battery.py` 90 s, `exp1b.py` 40 s, everything else under 10 s.

```bash
python3 scripts/exp1b.py
```
