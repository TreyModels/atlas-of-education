# The full demographic transition, 1750-2024: from the pre-antibiotic equilibrium to fertility collapse

Worker `un-data`, branch `research/transition-2026-11-23`, 23 Nov 2026. Box2 only (`ssh autodl2`),
working dir `/root/work/transition`. Scripts in `scripts/`, data in `data/`, figures in `figures/`.
Raw downloads are on box2 (`raw/`, ~4 MB) with URLs and hashes in `data/RAW_SOURCES.md`; the tidy panel,
onsets and results are committed.

**Short answer.** The arc runs from a corner where about two in five children died before age five and people
lived about 40 years, to one where child deaths are a few per hundred and people live past 70. Child-mortality
decline precedes fertility decline in the observed era in 78-81% of countries (median gap ~12 years), and a
country-level event study shows fertility falling steadily in the decades after each country's mortality
decline begins. The pre-1950 long-run test cannot be run on observed fertility (no long-run TFR series exists
here; the derived series gives a 52-year median that is demonstrably unreliable), so "mortality-led from 1800"
is suggested by the phase diagram and the early-transitioner series, not identified. Basic schooling precedes
the fertility transition; mass six-year schooling follows it. The antibiotic era is dated but not identified.

## (1) Fertility

**The pre-antibiotic corner, quantified** (median across countries with data, IQR across countries in brackets;
`data/transition_results.json`, figure d):
- 1800-1850: child mortality **41.6 deaths per 100 live births** [38.0-44.4], 184 countries; life expectancy
  **39.7 years** (9 countries); effective fertility **2.54 surviving children per woman** (6 countries).
- 1850-1900: child mortality 41.3 [36.1-44.0]; life expectancy 39.5 (25 countries); effective fertility 2.94.
- 1900-1940: child mortality **38.9** [25.8-41.9]; life expectancy **39.4** (66 countries).
- 1980-2024 (collapse corner): child mortality **2.8** [1.2-7.8], 197 countries; life expectancy **70.7**;
  effective fertility **2.55** surviving children per woman (maximum 5.4 in 1940-1980; median 4.26 then).
A derived "implied total fertility rate" (effective fertility divided by an approximate survival probability)
is in `data/long_run_panel.csv` and gives 3.6-4.0 for 1800-1900; it is lower than national historical TFRs
(about 5) because both the survival conversion and the effective-fertility series are approximations.
**It is therefore shown, not used for any claim.** Uncertainty in the corner is mostly coverage: only 6-15
countries have effective fertility before 1900, while child mortality is reconstructed for 184.

**Figures.** Figure (a) is the phase diagram (child mortality against effective fertility, eight countries,
1800-2024, shaded corners); figure (b) the time series; figure (d) the same diagram with the two corners
annotated and country labels. In figure (b), vertical jumps are splice years between the pre-1950
reconstruction and the post-1950 UN estimates — data artefacts, not history.

**When did the declines start?** Using a peak-relative onset rule (first year at least 10% below the running
peak and sustained for ten years — robust to how much early data a country has): mortality decline begins in a
median year of **1929** in the long-run reconstruction (197 countries) and **1960** in the observed-era data
(195 countries); observed fertility decline begins in a median year of **1971** (192 countries). The onset
rule has roughly ±5-year precision (ten-year sustain window), so that is the minimum detectable lag.

**Does mortality decline lead fertility decline?** In the observed UN data, yes, usually:
- all countries with both onsets dated from 1950+ data: median lag **+12 years** (IQR +3 to +19; 78% positive;
  190 countries);
- late transitioners only (total fertility still ≥4 in 1950, so the series captures the transition rather than a
  late baby-boom correction): median **+12 years** (IQR +4 to +23.5; 81% positive; 142 countries);
- by region: East Asia +9 (30), Latin America +11 (35), Middle East/North Africa +10 (23), South Asia +17.5 (6),
  Sub-Saharan Africa +26 (43), Europe/Central Asia +3 (51 — contaminated: those transitions began before 1950,
  so the 1950+ series dates their last leg, not their start).
- within-country event study around each country's own mortality-decline onset (18 countries with long-run
  onsets): fertility relative to its pre-onset baseline is 1.01 at onset, 0.98 ten years later, **0.85 at +20
  years, 0.66 at +30, 0.59 at +40** — a slow, large fall after mortality begins (figure c is the lag
  distribution, not the event study).

**But the cross-correlations are weak, and the long-run test is not usable.** Twenty-year changes in child
mortality and in fertility co-move only modestly (median correlation 0.39 at zero lag; 43% of countries above
0.5), and the lag that maximises the correlation is centred near zero (median −5 years). The long-run version
of the onset test — mortality onset from the 1800+ reconstruction, fertility onset from the derived implied
series — gives a median lag of +52 years (IQR 36-73; 99.5% positive; 194 countries), but the derived onset
dates are plainly wrong where we can check them (England & Wales 91 years, Japan 44, whereas their historical
gaps are roughly 10-20 years). **That result is a reconstruction artefact and is reported only to show why the
pre-1950 lead-lag question cannot be answered with these data.**

**What is identification and what is description.** The onset ordering and the phase diagram are description:
no exogenous variation is used, and the 1950+ panel shares the same development era. The identification test
already run is E1 (level versus volatility of child mortality, `research/records/2026-11-23-level-volatility/`):
fertility responds to the level, not the volatility, which is consistent with a replacement/quantity-quality
reading but does not separate those from a common cause. The causal question needs the shock designs (E4/E7),
not this record. **What would kill the mortality-led reading:** if fertility decline preceded mortality decline
in most countries (here 22% of observed-era lags are negative), or if exogenous mortality-reducing shocks moved
mortality without moving fertility. Neither is established.

**The antibiotic era, honestly.** Penicillin was mass-produced from 1944-45, streptomycin from 1947, DDT
spraying from the mid-1940s, the WHO was founded in 1948, measles vaccine arrived in 1963 and oral rehydration
in the 1970s-80s. The steepest part of the child-mortality decline in today's poor countries is indeed
post-1945 — but the same decades also brought decolonisation, income growth, schooling expansion, state
capacity and the fertility transition itself. The mortality decline had started in Europe decades before
antibiotics (England 1830s, Sweden 1750s per the reconstructions), showing that the pre-antibiotic decline is
real; whether the post-1945 acceleration caused the later fertility fall cannot be identified from these data.
We date the era; we do not claim a causal break.

## (2) Massification

**Basic schooling comes before the fertility transition; mass schooling comes after.** Comparing each
country's schooling series (mean years of education, 1870+) with its observed fertility-decline onset:
- the year a country reaches **2 years** of average schooling comes a median **15 years before** fertility
  decline begins (IQR −11 to +45; 140 countries; in 67% of countries schooling crosses 2 years first);
- the year a country reaches **6 years** of average schooling comes a median **18 years after** fertility
  decline begins (IQR −32 to −4.75; 124 countries; in 81% of countries the fertility fall starts first).
So in the long arc, basic literacy is a precondition/companion of the transition, while the mass upper-primary
system — the "massification" our project has studied — arrives *after* fertility has already begun falling.
This is consistent with the matrix result that schooling does not drive fertility at country level with trends,
and it is one more reason not to read mass schooling as the trigger of the fertility collapse.

## What this changes in our story

The full arc makes the mortality-led reading more plausible than the post-1960 panel alone: mortality decline
begins first in nearly every country where we can date both, and fertility falls for decades afterwards. But
the long-run, pre-1950 part of that claim is description, not identification; the only causal test we have
(E1) narrows the mechanism to the survival level. The collapse to below-replacement fertility is a late-20th
century phenomenon at low mortality, which fits the same level story. Schooling does not move first.

## Data, provenance and uncertainty

Sources (Our World in Data grapher exports, downloaded 2026-11-23 with a browser user agent; chart citations
from the embedded metadata): child mortality = Gapminder (2015) reconstructions + UN IGME (2025) estimates;
life expectancy = Riley (2005), Zijdeman et al. (2015), HMD (2025), UN WPP (2024); effective fertility =
Malani & Jacob series via OWID; total fertility = UN WPP (2024); mean years of schooling = Barro & Lee (2015),
Lee & Lee (2016); income = Bolt & van Zanden, Maddison Project Database 2023; urban share = UN DESA (2025);
crude birth rate = UN WPP. Exact URLs, raw file sizes and sha256 in `data/RAW_SOURCES.md`.

Flags and limits: pre-1950 child mortality is a **reconstruction**, post-1950 is a **UN model estimate** — no
row here is a raw vital-registration observation. The tidy panel keeps raw years; nothing is interpolated for
estimation (temporary interpolated values, if any, would be only for plotting). Effective fertility is
survival-adjusted and can rise during the early transition while births per woman are unchanged, so it is
not a fertility rate; the implied TFR is derived and approximate. Onset dating precision is about ±5 years;
the cross-correlation grid is 5 years. Countries need at least 25 annual points for an onset to be dated, and
pre-1950 claims use only countries with genuine long-run series (`data/onsets.csv` marks every date).

## Files

`scripts/transition.py` (series assembly, onsets, lags, event study, figures), `scripts/download_raw.sh`
(exact downloads), `data/long_run_panel.csv` (country-year, all series + source flag),
`data/onsets.csv` (per-country onset dates and lags), `data/transition_results.json` (all statistics),
`data/RAW_SOURCES.md` (URLs, citations, hashes), `results/logs/transition.log`.
Figures: `figures/fig_a_phase_diagram.png`, `fig_b_time_series.png`, `fig_c_lag_distribution.png`,
`fig_d_corners_annotated.png`.
