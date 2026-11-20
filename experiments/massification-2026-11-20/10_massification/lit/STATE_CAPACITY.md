<!-- Writer: lit-archivist, 2026-11-20. User directive: state capacity as first-class concept.
Write scope: 10_massification/lit/ only. Labels strict: VERIFIED (primary text read this session) /
OBSERVED (value read from a cited table/series on disk) / STANDARD-CITATION (canonical claim, primary text NOT
read this session) / NOT-FOUND / BLOCKED. Nothing below is a model output. -->

# STATE_CAPACITY — fiscal, delivery and enforcement capacity as driver vs marker of massification

**Why this file exists.** The previous phase discovered that a law without capacity changes nothing (PHL's 1953 RA 896 was unfunded; the 2013 reform stalled at 75% upper-secondary completion), while a law *with* capacity moves completion within a decade (HKG 1971→1974). State capacity therefore has to be modelled explicitly, not treated as a residual. The hard analytical question is whether capacity **drives** massification or merely **marks** it.

## 1. The literature

> **Verification warning.** Everything in this section is **STANDARD-CITATION** — canonical claims I am confident are correctly attributed but did **not** read this session (no full text retrieved; publisher blocks). Do not quote a coefficient from this section. Each line states what the source is needed *for*.

### 1.1 State-building and mass schooling
- **Paglayan (2024, *APSR*)** — mass schooling expanded after **internal conflict** to instil order, not primarily in response to economic demand; the state's motive was political stability and legibility. *(Needed for: the "order" motive vs the "growth" motive; the PHL post-conflict and HKG post-1967 cases.)*
- **Ansell & Lindvall (2020)** — mass education as state-building; the timing of primary-school expansion follows state consolidation. *(Needed for: the comparative-baseline claim.)*
- **Gellner (1983); Tilly (1990)** — standardisation/legibility; extraction requires literate, mobile populations.

### 1.2 Fiscal capacity and public goods
- **Acemoglu, Johnson & Robinson (2001, 2005)** — institutions as the fundamental cause; state capacity as a component of institutional quality. *(Needed for: capacity as an institutional variable, not just a budget line.)*
- **Besley & Persson (2009, 2013)** — fiscal capacity as the state's structured ability to raise revenue; correlates with public-good provision. *(Needed for: the spending-%GDP proxy's theoretical justification.)*
- **Tilly (1990)** — war-making → extraction → administration (the fiscal-capacity mechanism in its classic form).

### 1.3 Administrative / delivery capacity
- Administrative capacity literature: the state's ability to **convert budget into teachers, schools and materials** — hiring, procurement, inspection, payroll integrity (ghost teachers, leakage). *(Needed for: teacher-supply and PTR as delivery proxies.)*
- **NOT FOUND this session:** any reading on procurement/leakage magnitudes for PHL, HKG or CHN. The "delivery" leg of capacity is the least evidenced in this package.

### 1.4 Enforcement of compulsory schooling
- The standard result in the compulsory-schooling-law literature is that **laws bind where they are enforced** (Angrist & Krueger 1991; Oreopoulos 2006 — both high-income settings). In low-capacity states, attendance laws are widely treated as non-binding. *(Needed for: the enforcement leg; the PHL case is the natural test since compulsory age 6–12 was long established — OBSERVED in the 2007 IBE profile — while completion remained far from universal.)*
- **NOT FOUND:** any direct measure of **inspection/sanction intensity** for PHL, HKG, CHN. **There is no observed enforcement-capacity series in this package.** That is a stated gap, not an omission.

### 1.5 The capacity-vs-law distinction
The literature's core claim, which the anchor data can test directly: **a compulsory-schooling law is a necessary but not sufficient condition; the binding constraint is delivery (places + teachers) and enforcement.** The PHL record is the cleanest test available in this programme: compulsory age 6–12 documented in the 2007 profile, yet upper-secondary completion is still 75% in 2024.

## 2. Each theory: capacity as driver or marker, mechanism, falsifier

| Theory | Capacity role | Mechanism (who builds / who enforces) | Prediction for the anchor | Falsifier |
|---|---|---|---|---|
| **Paglayan / state-building** | **Driver** (political) | State builds schools to instil order and build legibility; enforcement follows political will | Expansion clusters after conflict/order shocks; capacity rises *before* completion | Expansion with no capacity rise and no order motive; completions tracking returns instead |
| **Fiscal capacity (Besley-Persson)** | **Driver** (fiscal) | Revenue base → education budget → places; spending %GDP is the instrument | Completion should track spending %GDP and its trend | Completion rising while spending/GDP flat or falling |
| **Administrative/delivery capacity** | **Driver** (mechanical) | Ministry hires teachers, builds/rents places, procures; PTR is the visible output | PTR falls *before* completion rises; teacher-supply constraints delay universalization | Completion rising with PTR flat/rising |
| **Enforcement** | **Driver** (coercive) | Attendance officers, sanctions, inspection; without it laws do not bind | Attendance/completion jumps where enforcement is credible | A compulsory law with no enforcement capacity producing universal completion |
| **World society / neo-institutional** | **Marker** (decoupled) | States adopt the *form* (law, ministry, target) without capacity; decoupling is expected | Law adoption precedes capacity and completion by long lags | Capacity and completion moving tightly with adoption |
| **Human capital** | Neither — capacity is a **cost** | Households invest; state capacity only sets cost of provision | Completion tracks returns; capacity matters only through the cost channel | Completion responding to capacity at constant returns |
| **MMI** | **Marker** | Advantaged groups capture expanded capacity first | New capacity raises the advantaged gradient first, then falls after saturation | Capacity expansion immediately compressing the gradient |

## 3. PHL / HKG / CHN capacity at their universalization moments

**All values OBSERVED** from data-hunter `JOBS_AND_MARKETS_PANEL.csv` (WDI/UIS provenance). Caveat: spending-%GDP and PTR are **crude proxies** — they capture fiscal and delivery capacity, not enforcement or procurement quality.

### 3.1 Philippines — low fiscal capacity, improving delivery, stalled completion
| Indicator | 1995 | 2000 | 2005 | 2015 | 2019 | 2024 |
|---|---|---|---|---|---|---|
| Education spending, % GDP | 2.66 | 3.16 | **2.33** | 2.83 | 3.41 | **3.93** |
| Education, % of government expenditure | 15.24 | 15.21 | 12.42 | 15.15 | 18.16 | 16.55 |
| Pupil–teacher ratio, primary | 33.7 | 35.3 | 35.1 | 30.3 | — | 29.1 (2017) |
| Pupil–teacher ratio, secondary | 36.2 | — | 37.9 | 26.2 | — | 23.9 (2017) |

**Reading.** PHL spending is **low and volatile** (dips to 2.33% of GDP in 2005, still only 3.93% in 2024), while **delivery improved markedly** (secondary PTR fell from 37.9 to 23.9). Yet upper-secondary completion stalled at 75%. **Delivery capacity improved without universalization** — so delivery capacity is *not sufficient*. This is the single most important capacity fact in the programme.

### 3.2 Hong Kong — high delivery capacity at the moment of universalization
| Indicator | 1996 | 2005 | 2010 | 2018/2024 |
|---|---|---|---|---|
| Education spending, % GDP | 2.73 | 4.13 | 3.51 | 3.81 (2024) |
| Pupil–teacher ratio, primary | 23.7 | 18.4 | 15.2 | 13.4 (2018) |
| Pupil–teacher ratio, secondary | 20.1 | 18.1 | 16.7 | 11.2 (2018) |

**Reading.** HKG's PTRs were far below PHL's at every comparable date (13–24 vs 29–38), i.e. **high delivery capacity**. Its primary NER crossed 90 in 1974, three years after the 1971 free-primary reform. **High capacity + law → fast universalization.**

### 3.3 China — high delivery capacity, long enforcement lag
| Indicator | 1995 | 2010 | 2018 | 2023 |
|---|---|---|---|---|
| Education spending, % GDP | 1.83 | — | — | 3.90 |
| Pupil–teacher ratio, primary | 22.9 | 16.8 | 16.4 | — |
| Pupil–teacher ratio, secondary | 15.1 | 15.5 | 13.3 | — |

**Reading.** China had **much lower PTRs than PHL** (16–23 vs 29–38) and a rising spending share, yet the 1986 compulsory law did not produce universal **lower-secondary completion until 2016** (data-hunter series: 84.9 in 2010 → 90.6 in 2016). **High delivery capacity with a ~30-year law-to-completion lag** — consistent with enforcement and rural-capacity constraints, not with a simple places constraint.

### 3.4 Korea — (near-ceiling benchmark, for contrast)
Education spending %GDP: 2.84 (1995) → 5.41 (2022); PTR primary 29.7 (1995) → 16.3 (2017). Completion already at ceiling before the series starts.

## 4. What the capacity evidence says — and what it cannot say

1. **Capacity is a marker and a necessary condition, not a sufficient one.** PHL is the counterexample to a pure capacity-driver account: delivery improved (PTR 38→24) while the top level stalled at 75%.
2. **The fiscal proxy is weak and PHL's is unusually low** — PHL spends ~3–4% of GDP on education against HKG's 3.3–4.1% and KOR's 2.8–5.4%; but HKG spends *more of its budget* (14–22%) and has far lower PTRs, so **the same %GDP buys very different delivery** depending on income level and public-sector wage bill. **Cross-country spending comparisons are close to meaningless without the wage-bill and price context.**
3. **Enforcement capacity has no measurable series in this package.** Every statement about attendance-law enforcement is STANDARD-CITATION or inference. The model must carry it as an unmeasured parameter and say so.
4. **The discriminating test the anchor can run:** if capacity were the driver, rising PTR-adjusted capacity 2005–2024 should have produced upper-secondary completion above 75%. It did not. **The residual must be demand, cost (foregone income), or the structure of the gate — not capacity.**

## 5. Data needed (ASK to data-hunter, joined to the earlier asks)
1. **PHL place-expansion series** (public secondary schools built, SHS places 2015–2024) — the mechanical delivery channel.
2. **PHL teacher hiring/net teacher supply** 2010–2024 (DepEd) — distinguishes "capacity to hire" from "budget".
3. **Any enforcement proxy** — DepEd attendance/inspection reports, LGU school-monitoring — currently **zero** enforcement data in the package.
4. **Public education spending per pupil, real** — not %GDP — for PHL/HKG/CHN, to make delivery comparable.

---

## 6. One-line summary for the Council
**Capacity buys the floor; it does not buy the ceiling.** The evidence in this package (PHL: PTR 38→24 while upper-secondary completion stayed at 75%; HKG: PTR ~18 and completion crossed within 3 years; CHN: PTR ~17 and a 30-year law-to-completion lag) supports treating capacity as a **necessary delivery precondition whose effect is conditional on enforcement and on the demand/cost structure at the top of the system** — not as a sufficient driver of massification.
