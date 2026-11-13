# Graduate supply shock: test results

3 November 2026. Education Atlas v0.4.2, uploaded archive. This is a mechanism diagnostic using existing code. No national parameters were fitted to the papers, and no original archive was changed.

## Controlled labour-only test

A single entering group contains 1,000 people. Degree holders increase from 100 to 200; everybody has the same learning (9 model units) and household resources. Formal vacancies stay at 300, including 105 skilled vacancies. The skilled tier requires a degree; routine vacancies are allocated among eligible applicants by lottery. Credential floors are held fixed, tutoring jobs are disabled, and the queue variant allows supported graduates to wait. Results average seeds 7, 19 and 43.

| Model and outcome | 10% degree holders | 20% degree holders |
|---|---:|---:|
| Queue: waiting share among degree holders | 0.0% | 36.5% |
| Queue: mean earnings among employed degree holders | 3.000 | 2.772 |
| Queue: mean earnings with waiting assigned zero | 3.000 | 1.760 |
| Competitive: skilled/unskilled wage premium | 2.577 | 1.671 |
| Competitive: mean degree-holder earnings | 4.258 | 2.761 |

Earnings are in engine wage units. Waiting assigned zero is current labour earnings, not household consumption, welfare or lifetime income. Support transfers are absent from this one-period probe.

The competitive premium falls by 35.2%. This follows its programmed elasticity: doubling the skill share multiplies the premium by `2^(-1/1.6)`. The exact log change is `-log(2)/1.6`. The limiting-case assertion passes.

The queue produces a different employment allocation under fixed tier wages. Mean employed-graduate earnings also fall, by about 7.6%, as graduates move into routine/informal work. Thus a queue can generate falling observed graduate wages alongside unemployment, even without a falling wage within each tier. This probe demonstrates a mechanism built into the model; it does not estimate China's elasticities or unemployment.

## Endogenous schooling scenario

Twelve runs compare the China pack's tertiary admission expansion with a counterfactual holding tertiary admission at its initial 4% of eligible academic candidates. All other gate changes, macro paths and policy events remain in both arms. Schooling is mechanism-only, with no completion anchors. Each cohort contains 600 children; each labour variant uses seeds 7, 19 and 43. The original country parameters are used without tuning.

This freezes one admission probability. It does not reproduce the measured 48% increase in national intake in 1999. The policy affects students already approaching university as well as later cohorts.

| Expansion effect relative to frozen admission | Queue, 2003–07 | Competitive, 2003–07 | Queue, 2022–24 | Competitive, 2022–24 |
|---|---:|---:|---:|---:|
| Additional degree-holding labour entrants per year, out of 600 entering children | +30.5 | +29.8 | +215.1 | +212.0 |
| Change in annual mean log earnings among employed new degree-holding entrants | -0.162 | -0.491 | -0.802 | -1.796 |
| Change in mean learning among new degree-holding entrants, model units | -1.918 | -2.074 | -6.895 | -7.218 |
| Additional degree holders waiting, divided by entering-cohort size | 0.000 | unavailable | +0.242 | unavailable |
| Change in skilled-job credential floor, engine levels | -0.267 | unavailable | +1.000 | unavailable |

Each cell averages within-seed treatment differences and years. Earnings condition on employed fresh leavers; the set of employed people changes. The queue statistic is a stock divided by a cohort size, rather than the official unemployment rate. The competitive module has no unemployment state; missing unemployment outputs cannot be treated as empirical zero unemployment.

The expansion changes graduate composition substantially. The queue model's lower earnings can arise through learning differences, job allocation and employment selection. The competitive model adds a supply-sensitive price. The endogenous-schooling results therefore cannot isolate a pure supply elasticity from the displayed earnings differences.

All six baseline/treatment pairs were identical before 1999 for the captured entering-worker outcomes. The analytical CES check passed. Nine existing validation/planning tests passed separately, with empty-group warnings in small test summaries.

## Does this reproduce the empirical papers?

**Empirical replication remains unestablished.** Neither variant contains the region, sex, participation, occupation and survey observation contracts needed to evaluate the papers' distinct estimands.

The full text of [Ou and Zhao, IZA DP 9643](https://docs.iza.org/dp9643.pdf) was retrieved. Its reported approximately 2-percentage-point reduction concerns the probability of unemployment in its specified sample and exposure design. It also estimates lower participation and wages, with heterogeneous effects. Those coefficients require the paper's precise denominator, cohort, treatment exposure and conditioning set. They are not plug-in targets for the engine's degree-holder queue per cohort. The comparison of the papers does not itself identify partial wage rigidity.

The [published Li–Whalley–Xing article](https://www.sciencedirect.com/science/article/abs/pii/S1043951X13000710) and an [earlier IZA version](https://www.iza.org/en/publications/dp/4974/chinas-higher-education-expansion-and-its-labor-market-consequences) are distinct versions. Their findings and estimators need to be tied to the exact version used before selecting numerical targets.

## What the test changes in the specification

1. Keep wages by occupation/tier separate from the average wage of graduates. Reproduce employment selection and skill composition before interpreting a change in the graduate premium.
2. Add labour-force participation and official survey classifications. Both unemployment and participation changes are needed to compare the competing papers.
3. Estimate sector- and occupation-specific hiring with regional exposure. An observed sector path can support a conditional historical replay; endogenous investment and vacancy creation are needed to explain why a country generates that path.
4. Measure changing credential requirements within comparable tasks. A larger queue under fixed jobs demonstrates congestion. Diploma disease additionally concerns the screening and credential escalation process.

Both country packs keep fiscal feedback off and impose income/job paths. This experiment therefore evaluates education–labour mechanisms conditional on those paths. It cannot explain takeoff or estimate the economy-wide effect of education.

## Reproduce

The accompanying archive contains `graduate_supply_test.py`, its full JSON outputs and the uploaded engine/planning code needed to rerun it. From the extracted directory:

```bash
python -m pip install -r requirements.txt
python graduate_supply_test.py --engine engine
```

Use Python 3.12 with the dependency versions recorded in the JSON manifest for closest numerical reproduction. The output contains Python/NumPy versions and SHA-256 hashes for every engine Python file used. Random seeds are paired, but policy branches can consume different later draws. Three seeds describe this diagnostic's simulation variation, not parameter or structural uncertainty.
