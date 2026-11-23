# Did schooling precede industrialisation? Four historical cases (23 November 2026)

## The question and the short answer
The project's 1965-2010 panel says schooling take-off precedes the release of agricultural labour in 61 of 64
countries, which contradicts "the floor falls first". This record asks the four historical cases where the
sequence can be checked against a century of scholarship. **The answer is split, and the split is the finding:**
schooling came first where the state built the pipeline ahead of demand (Prussia, and the French statutes),
and industrialisation came first in the first industrialiser (Britain). The modern panel's regularity is
therefore a late-industrialiser pattern, not a universal law.

Operational definitions — what counts as a take-off, the 10-year verdict rule, and the evidence classes — were
fixed in `DEFINITIONS.md` and committed (`74e0fe2`) before the dates were assembled.

## (1) Fertility

### The sequence table
| case | schooling take-off (measured) | supply-side policy date | farm exodus | order | verdict |
|---|---|---|---|---|---|
| **Prussia / Germany** | enrolment already high by 1800 (roughly half of school-age children, literature estimate); universal by 1860s | **1763** General-Landschul-Reglement (compulsory); 1794 Landrecht; **1812** Hardenberg edict | agricultural share begins its sustained fall after 1850; under 40% by 1900 | **schooling first, by 80-120 years** | **supply-led** |
| **France** | primary enrolment roughly 45% in the 1830s, ~75-80% by 1880; universal after 1900 | **Guizot law 1833** (a school in every commune); Falloux 1850; **Ferry laws 1881-82** (free and compulsory) | agricultural share ~52% in 1851, ~41% in 1901, ~30% by 1930 | **statute first (1833), attainment take-off late and broadly simultaneous with the farm exodus (1880s)** | **statute-led, attainment demand-following** |
| **Britain** | attendance ~1 child in 8 in 1858; near-universal only by 1900 | 1833 Factory Act (half-time schooling); **1870** Elementary Education Act; compulsory 1880; free 1891 | industrial revolution 1780-1840; agricultural share ~35% in 1800, ~22% in 1851, ~9% in 1901 | **industrialisation and farm exodus first, by 40-90 years** | **demand-led** (the classic puzzle) |
| **United States (North)** | common schools 1830-60; high-school movement 1910-40 | Massachusetts 1852 (first state compulsory law); local public funding from the 1830s | agricultural share ~63% in 1840, ~50% in 1870, ~31% in 1910, ~12% in 1950 | **schooling first nationally, by 60+ years**; high schools coincide with the farm exodus | **supply-led in the local-public-goods sense** |

Evidence classes: the dates in bold are standard literature dates. **None of them was verified against a
primary source in this session** — web searches this session returned only fragments, so the honest label for
the specific dates and every enrolment or agricultural-share percentage above is **UNVERIFIED literature
standard**, and the report says so rather than putting a false tick on them. What *was* verified in-session is
the negative result below: the project's own long-run panel cannot do this.

### Why the project's own data cannot adjudicate this
I checked the long-run panel directly. For all four countries its **mean-years-of-schooling series starts in
1870** (31 decadal points to 2020) and its **urban-share series starts in 1950**. Child mortality does go back
to 1800. So the panel cannot see the Prussian or French take-offs at all, and its first schooling observation
for Britain is already the decade of the 1870 Education Act. Applying the pre-registered take-off rule to it
returns 1870 for all four countries — the start of the data, not a historical event. **The historical
adjudication therefore rests on the literature, and the quantitative bonus the brief asked for cannot be done
from our own series.** This is a data gap, reported as one.

### What the four cases say about the verdict
- **Prussia is the strongest case for supply-led massification.** The compulsory-schooling statute is 1763, a
  century before German industrialisation and 120 years before the farm exodus. The theory's pipeline-first
  claim fits it exactly: the state created the schools before there was an industrial demand for literate
  labour.
- **France shows the two dates coming apart.** The supply-side statute is early (1833) but measured attainment
  lags until the 1880s, when the Ferry laws and the farm exodus arrive together. That is consistent with a
  state pushing schooling and the labour market pulling it at the same time, and it is why the verdict is
  "statute-led, attainment demand-following" rather than cleanly supply-led.
- **Britain is the counterexample, and it is not a small one.** The first industrialiser had its industrial
  revolution and its agricultural exodus before national mass schooling. Britain is where "the floor fell
  first" is true, and it is also where the theory's mechanism should have been *least* needed to be supplied
  by the state — the demand for literacy was there, but schooling was privately and unevenly provided until
  1870.
- **The United States sits in between**: locally financed common schools predate the national farm exodus, but
  they were demand-driven by communities, and the high-school movement (1910-40) is simultaneous with the
  final farm exodus rather than prior to it.

So "schooling take-off precedes the farm exodus" survives the four cases only if the phrase "where the state
built it" is added. In the one case where industrialisation came first — the case that started the whole
question — it fails.

## (2) Massification
This is consistent with, and sharpens, the massification records. Massification is not a single process with
one temporal signature: in state-led systems the pipeline is created ahead of the occupational structure
(Prussia, the French statutes), while in the market-led first industrialiser the occupational change pulled
schooling along, late. That gives a testable implication for the modern panel's 61/64 result: the regularity
should hold where the state was the supplier, and weaken in the early-industrialiser set. It also means the
61/64 finding is **not evidence that schooling causes the labour release**; it is evidence about who built the
pipeline and when.

## Limits
Every specific date and percentage above is UNVERIFIED literature standard, not checked against primary
sources in this session; the four cases are not a sample and no statistical claim is made. Agricultural
employment shares in the 19th century are themselves reconstructed estimates differing between Broadberry,
Bairoch and Mitchell by several points, which matters when a lead of 40 years is being claimed. "Schooling
take-off" mixes statutes with attainment, and this record keeps them separate precisely because they diverge
(France 1833 vs 1880s). For a real test the series needed are: Prussian enrolment 1800-1870 (Flora, *State,
Economy and Society in Western Europe*; Lindert, *Growing Public*), UK school attendance 1850-1900 (Newcastle
Commission 1861; Board of Education annual reports), French primary enrolment 1830-1900 (Diebolt's series; the
French ministry's *Statistique de l'enseignement primaire*), and US high-school enrolment 1890-1940 (US
Historical Statistics, series H-598 onward). With those four series the lead/lag could be quantified properly;
without them this record is a dated argument, not a measurement.

## Files
`DEFINITIONS.md` (first commit), `scripts/hist.py` (the panel-coverage and take-off check that produced the
negative result), `results/sequence_from_panel.json` (its output).
