# Angkor maintenance repair and separate accounting extension

2026-11-07. Exploratory, uncalibrated. Website unchanged.

## Reproduction
Python 3.10+ standard library only. From this directory:

    python3 run_experiments.py
    python3 sensitivity.py

The first command runs 720 histories: 3 engines × 3 regimes × 2 climate conditions × 40 seeds. The second runs 560 sensitivity histories. Total 1,280 scenario histories, plus reproducibility and limiting-case checks. Each history covers 110 annual steps. Same weather seed across matched scenarios. Original source and CSV retained under original/. Their files came from angkor_kiss_maintenance_v03.zip in the supplied handoff.

## Timing correction, isolated from other edits
Original maintenance_only reduced effort from year zero, despite its README specifying year 55. timing_fixed.py starts the reduction at year55, matching reshuffle. It must match stable through year54, checked exactly for both climates. All other rules remain unchanged.

Median final people in state-linked communities (40 seeds each):

| Regime | Original normal | Fixed normal | Original drought | Fixed drought |
|---|---:|---:|---:|---:|
| Stable | 14,687 | 14,687 | 6,958 | 6,958 |
| Maintenance only | 8,277 | 10,661 | 3,296 | 6,209 |
| Elite reshuffle | 8,855 | 8,855 | 3,787 | 3,787 |

The faulty timing exaggerated the maintenance-only loss. Relative to the stable drought median, the maintenance-only reduction changes from about 53% to 11%. These are differences between scenario medians, not historical estimates or confidence intervals. Refuges remain separately counted. Marginal medians need not sum to median totals.

## Separate extension: accounted.py
No silent replacement of the supplied engine. Added:

* Available labour = population × .45 adults × 180 workdays/year. Farm staffing = farm days/(110 ha × 162 person-days/ha), capped at one. All conversion rates are illustrative, not measured Angkor parameters.
* Work competes among farming, irrigation, military service, monuments, religion and administration; idle time recorded. Default military .08, monuments .04, religion .04, administration .015; irrigation uses the inherited maintenance rule. These are new assumptions. No stone output, military success or religious legitimacy gain is invented.
* Court grain and elite grain now have explicit stores, each with 6% annual spoilage. Court revenue pays resident workers' service rations: paid duty-days/365 × 280 kg. This is a transfer into household food stores. Residents consume once. Unfunded service labour becomes idle, rather than performed for free. Scheduled farm labour is fixed for the year; unused service days are not reassigned instantly. No wages beyond rations, weapons or frontier supply chain.
* Refuge has harvest, seed, storage, spoilage, consumption, births and deaths, using the same climate draw. Its land ceiling is an assumed 3,575 ha; maximum land/person .275 ha; yield 2,150 kg/ha before weather and a .91 productivity factor. This replaces the inherited capacity-only demographic penalty. Refuge newcomers eat there in the arrival year, so their food exposure and birth/death rates during that transition are simplified.
* Each annual step checks population = previous population + births - deaths across both areas; migration cancels. Grain = previous grain + gross harvest - seed - consumption - spoilage; internal transfers cancel. Labour sums exactly. Stocks remain nonnegative.

Initial state population 9,600; zero initial refuge population. Drought is the inherited synthetic nine-year 64% reduction in years65–73, with canal damage in years68 and72. Not the Buckley reconstruction. Maintenance drops TO 35% of baseline, a 65% cut.

Median final population in the separate extension:

| Regime | State, normal | State, drought | Total across state and refuge, drought |
|---|---:|---:|---:|
| Stable | 16,009 | 9,829 | 18,672 |
| Maintenance only | 11,539 | 8,322 | 17,584 |
| Elite reshuffle | 9,612 | 4,918 | 17,107 |

State-linked population losses can exceed total population losses because people move. Relative to stable drought medians, reshuffle reduces state-linked population by about50%, total population by about8%. Births and deaths differ too; movement is not the entire explanation. Reshuffle bundles higher extraction, lower relief, lower maintenance and a trust shock; this does not isolate each effect.

## Sensitivity and an unresolved military interpretation
With drought, changing retained maintenance effort from20%,35%,60%,100% gives median state-linked populations7,945;8,322;8,909;9,829. Higher maintenance reduces food shortfall in this tested range.

Increasing military share from4% to8% to16% gives7,999;8,322;9,019. More paid service redistributes court grain to households while farm staffing remains sufficient. This is a ration-access mechanism. There are no battles, conquest, garrisons or territorial defence outcomes here. It cannot establish that larger armies improve historical resilience, or identify an optimal military allocation. Explicit frontier provisioning belongs in the separate frontier-allocation model, not an interpretation pasted onto this one.

## Checks and limits
All1,280 scenario histories completed with embedded annual accounting assertions in the extension. Example ledger maximum errors: grain1.49e-8 kg; population2.19e-11 people; labour1.17e-9 person-days. Timing identity, exact reproducibility, zero population, zero discretionary service sectors and zero maintenance checks pass. These checks verify implementation, not historical truth.

Temple and elite extraction fractions remain assumptions. Elite stocks accumulate without an expenditure rule; the ledger makes them inspectable but does not explain their use. There is no independently validated famine-insurance institution, geographic map, canal graph, flood cascade, household inequality, captive system, temple transformation or calibrated historical dates. Canal condition has the inherited artificial floor of0.3. Land remains fixed. Results establish conditional behaviour of the declared rules. Original and fixed engines still retain their older accounting limitations.

## Files
runs.csv: all720 main runs; summary.json: medians; sensitivity.csv:560 runs; annual_ledger.csv: one complete extension run; run-log.txt and sensitivity-log.txt: execution output. SHA256SUMS records packaged file hashes.
